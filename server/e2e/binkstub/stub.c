#include <windows.h>
typedef struct { unsigned int Width,Height,Frames,FrameNum,LastFrameNum; unsigned char pad[0x800]; } BINK;
/* Gemini #3: neutralise render_text_element @0x991A80 by forcing its existing
   early-return (je 0x991ACE at 0x991A8A) to an unconditional jmp. 1 byte:
   0x74 (je) -> 0xEB (jmp). Skips all engine text rendering (loading screen etc.)
   so the uninitialised glyph manager is never touched -> no crash, no infinite
   layout; CEF/HTML UI still renders its own text. Applied at movie time (after
   the packer has unpacked .text). */
static volatile int g_done=0;

/* The native "shader text element" class (vtable @0xF4F1E4, see the "ERROR -
   Shader <" string right after it) stores its GPU shader resource at this+0x2f0.
   The ctor (0xA06076) sets it NULL; it is only filled when the native shader is
   created -- which never happens under our software-rendered headless Wine. The
   well-behaved vtable methods guard `if(this+0x2f0==NULL) return;`. The DRAW /
   BUILD / glyph-lookup methods forgot the guard and dereference NULL (or do a
   glyph lookup with index -1 -> edi=0xFFFFFFC0). We force every crash-prone
   method of this one class to early-return with its correct stdcall arg cleanup.
   Skipping them only skips ENGINE-side text rendering -- the real UI is CEF/HTML
   and renders independently. */
static int patch_one(unsigned char* p,const unsigned char* code,int nlen,int total){
  DWORD o; int k;
  if(IsBadReadPtr(p,total)) return 0;
  if(p[0]!=0x55 && p[0]!=0x56) return 0;          /* not unpacked / already patched */
  if(!VirtualProtect(p,total,PAGE_EXECUTE_READWRITE,&o)) return 0;
  memcpy(p,code,nlen);
  for(k=nlen;k<total;k++) p[k]=0x90;              /* pad with NOPs */
  VirtualProtect(p,total,o,&o);
  FlushInstructionCache(GetCurrentProcess(),p,total);
  return 1;
}
static void patch_ssl(void);
static void apply_patch(void){
  unsigned char* je=(unsigned char*)0x991A8A;  /* the conditional jump byte */
  DWORD old;
  patch_ssl();                /* SSL CA-path string (retried each bink call) */
  static const unsigned char RET[1]   ={0xC3};            /* ret      (0 args) */
  static const unsigned char RET4[3]  ={0xC2,0x04,0x00};  /* ret 4    (1 arg)  */
  static const unsigned char RET8[3]  ={0xC2,0x08,0x00};  /* ret 8    (2 args) */
  static const unsigned char XRET4[5] ={0x33,0xC0,0xC2,0x04,0x00}; /* xor eax,eax; ret 4 */
  if(g_done) return;
  if(IsBadReadPtr(je,2)) return;
  if(je[0]!=0x74) return;                       /* not unpacked yet / already patched */
  if(VirtualProtect(je,2,PAGE_EXECUTE_READWRITE,&old)){
    je[0]=0xEB;                                 /* je -> jmp (always skip text render) */
    VirtualProtect(je,2,old,&old);
    FlushInstructionCache(GetCurrentProcess(),je,2);
    /* shader-text-class crash-prone methods -> early-return (correct ret size) */
    patch_one((unsigned char*)0xA060E0,XRET4,5,9); /* text-DRAW (glyph blit), ret 4 */
    patch_one((unsigned char*)0xA06550,RET8 ,3,3); /* glyph lookup(idx), ret 8       */
    patch_one((unsigned char*)0xA065C0,RET4 ,3,3); /* glyph lookup(idx) variant,ret4 */
    patch_one((unsigned char*)0xA061D0,RET  ,1,1); /* Draw (shader call), ret 0      */
    patch_one((unsigned char*)0xA06250,RET  ,1,1); /* SetVisible/fade, ret 0         */
    patch_one((unsigned char*)0xA06CD0,RET  ,1,1); /* Build geometry, ret 0          */
    /* SSL fix: the game's static libcurl/OpenSSL was built with
       OPENSSLDIR=/usr/local/ssl, so it calls load_verify_locations(
       "/usr/local/ssl/cert.pem") which doesn't exist under Wine -> empty trust
       store -> "unable to get local issuer certificate". Rewrite that .rdata
       string (VA 0xF6D7E0, 23 bytes) to the cwd-relative "ca.pem"; the launcher
       drops our CA as Bin/ca.pem and the game's cwd is Bin. (Same fix as
       plumbing/patch_binary.py, applied at runtime since the shipped exe is
       packed.) */
    /* SSL: the game's static libcurl 7.38 was built with no CA bundle, so with
       verifypeer (default on) and no CAINFO it has an EMPTY trust store and every
       cert is rejected inside SSL_connect (ssl3_get_server_certificate ->
       CERTIFICATE_VERIFY_FAILED 0x1407E086) -- no CA path can ever satisfy it.
       Neutralise the server-cert verify gate: the 'je 0xAC18A0' at 0xAC1803
       (taken when verify_mode==NONE) becomes an unconditional jmp to the same
       success path, so the chain-verify result is ignored. This is the curl
       equivalent of the winhttp shim's IGNORE_ALL_CERT_ERRORS, scoped to our
       self-signed local server. */
    { unsigned char* v=(unsigned char*)0xAC1803; DWORD ov;
      static const unsigned char J[6]={0xE9,0x98,0x00,0x00,0x00,0x90}; /* jmp 0xAC18A0; nop */
      if(!IsBadReadPtr(v,6) && v[0]==0x0F && v[1]==0x84 &&
         VirtualProtect(v,6,PAGE_EXECUTE_READWRITE,&ov)){
        memcpy(v,J,6);
        VirtualProtect(v,6,ov,&ov); FlushInstructionCache(GetCurrentProcess(),v,6);
        HANDLE s=CreateFileA("Z:\\tmp\\sslverify_off.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
        if(s!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(s,"ok\n",3,&w,0);CloseHandle(s);}
      } }
    /* curl also re-checks the result post-handshake via SSL_get_verify_result()
       (0xABE0E0: return ssl->verify_result@+0xEC) and closes if != X509_V_OK.
       Force it to always return 0 (X509_V_OK) -> xor eax,eax; ret. */
    { unsigned char* g=(unsigned char*)0xABE0E0; DWORD og;
      static const unsigned char Z[3]={0x33,0xC0,0xC3}; /* xor eax,eax; ret */
      if(!IsBadReadPtr(g,4) && g[0]==0x8B && g[1]==0x44 && g[2]==0x24 &&
         VirtualProtect(g,3,PAGE_EXECUTE_READWRITE,&og)){
        memcpy(g,Z,3);
        VirtualProtect(g,3,og,&og); FlushInstructionCache(GetCurrentProcess(),g,3);
      } }
    g_done=1;
    HANDLE m=CreateFileA("Z:\\tmp\\binkpatch_ok.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
    if(m!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(m,"ok\n",3,&w,0);CloseHandle(m);}
  }
}

/* SSL CA-path patch, decoupled from the code patches because .rdata may be
   unpacked later than .text. Retried on every bink entry point until it sticks.
   Also probes the current bytes at the string VA so we can confirm the address. */
static volatile int g_ssl_done=0;
static void patch_ssl(void){
  unsigned char* sp=(unsigned char*)0xF6D7E0; /* "/usr/local/ssl/cert.pem" .rdata */
  /* absolute path (Z:=unix root) so it works regardless of curl-time cwd; fits in
     the 23-byte slot. Our CA is dropped at /tmp/ca.pem by the launcher. */
  static const unsigned char CA[23]={'Z',':','\\','t','m','p','\\','c','a','.','p','e','m',0,0,0,0,0,0,0,0,0,0};
  DWORD os; static int probed=0;
  if(g_ssl_done) return;
  if(IsBadReadPtr(sp,23)) return;
  if(!probed){ /* one-time probe of what's actually at the VA */
    HANDLE p=CreateFileA("Z:\\tmp\\sslprobe.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
    if(p!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(p,sp,23,&w,0);CloseHandle(p);}
    probed=1;
  }
  if(sp[0]=='/' && sp[1]=='u'){
    if(VirtualProtect(sp,23,PAGE_READWRITE,&os)){
      memcpy(sp,CA,23);
      VirtualProtect(sp,23,os,&os);
      g_ssl_done=1;
      HANDLE m=CreateFileA("Z:\\tmp\\sslpatch_ok.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
      if(m!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(m,"ok\n",3,&w,0);CloseHandle(m);}
    }
  } else if(sp[0]=='c' && sp[1]=='a'){ g_ssl_done=1; } /* already patched */
}

BOOL WINAPI DllMain(HINSTANCE h,DWORD r,LPVOID v){ if(r==DLL_PROCESS_ATTACH) DisableThreadLibraryCalls(h); return TRUE; }
int __stdcall BinkBufferBlit(int a1,int a2,int a3){ return 0; }
int __stdcall BinkBufferCheckWinPos(int a1,int a2,int a3){ return 0; }
int __stdcall BinkBufferClear(int a1,int a2){ return 0; }
int __stdcall BinkBufferClose(int a1){ return 0; }
int __stdcall BinkBufferGetDescription(int a1){ return 0; }
int __stdcall BinkBufferGetError(void){ return 0; }
int __stdcall BinkBufferLock(int a1){ return 0; }
int __stdcall BinkBufferOpen(int a1,int a2,int a3,int a4){ return 0; }
int __stdcall BinkBufferSetDirectDraw(int a1,int a2){ return 0; }
int __stdcall BinkBufferSetHWND(int a1,int a2){ return 0; }
int __stdcall BinkBufferSetOffset(int a1,int a2,int a3){ return 0; }
int __stdcall BinkBufferSetResolution(int a1,int a2,int a3){ return 0; }
int __stdcall BinkBufferSetScale(int a1,int a2,int a3){ return 0; }
int __stdcall BinkBufferUnlock(int a1){ return 0; }
int __stdcall BinkCheckCursor(int a1,int a2,int a3,int a4,int a5){ return 0; }
int __stdcall BinkClose(int a1){ return 0; }
int __stdcall BinkCloseTrack(int a1){ return 0; }
int __stdcall BinkControlBackgroundIO(int a1,int a2){ return 0; }
int __stdcall BinkControlPlatformFeatures(int a1,int a2){ return 0; }
int __stdcall BinkCopyToBuffer(int a1,int a2,int a3,int a4,int a5,int a6,int a7){ return 0; }
int __stdcall BinkCopyToBufferRect(int a1,int a2,int a3,int a4,int a5,int a6,int a7,int a8,int a9,int a10,int a11){ return 0; }
int __stdcall BinkDDSurfaceType(int a1){ return 0; }
int __stdcall BinkDX9SurfaceType(int a1){ return 0; }
int __stdcall BinkDoFrame(int a1){ return 0; }
int __stdcall BinkDoFrameAsync(int a1,int a2,int a3){ return 0; }
int __stdcall BinkDoFrameAsyncMulti(int a1,int a2,int a3){ return 0; }
int __stdcall BinkDoFrameAsyncWait(int a1,int a2){ return 0; }
int __stdcall BinkDoFramePlane(int a1,int a2){ return 0; }
int __stdcall BinkFreeGlobals(void){ return 0; }
int __stdcall BinkGetError(void){ return 0; }
int __stdcall BinkGetFrameBuffersInfo(int a1,int a2){ return 0; }
int __stdcall BinkGetGPUDataBuffersInfo(int a1,int a2){ return 0; }
int __stdcall BinkGetKeyFrame(int a1,int a2,int a3){ return 0; }
int __stdcall BinkGetPalette(int a1){ return 0; }
int __stdcall BinkGetPlatformInfo(int a1,int a2){ return 0; }
int __stdcall BinkGetRealtime(int a1,int a2,int a3){ return 0; }
int __stdcall BinkGetRects(int a1,int a2){ apply_patch(); return 0; }
int __stdcall BinkGetSummary(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackData(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackID(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackMaxSize(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackType(int a1,int a2){ return 0; }
int __stdcall BinkGoto(int a1,int a2,int a3){ return 0; }
int __stdcall BinkIsSoftwareCursor(int a1,int a2){ return 0; }
int __stdcall BinkLogoAddress(void){ return 0; }
int __stdcall BinkNextFrame(int a1){ if(a1){((BINK*)a1)->FrameNum+=1;} return 0; }
int __stdcall BinkOpen(int a1,int a2){ apply_patch(); return 0; }
int __stdcall BinkOpenDirectSound(int a1){ return 0; }
int __stdcall BinkOpenMiles(int a1){ return 0; }
int __stdcall BinkOpenTrack(int a1,int a2){ return 0; }
int __stdcall BinkOpenWaveOut(int a1){ return 0; }
int __stdcall BinkOpenWithOptions(int a1,int a2,int a3){ apply_patch(); return 0; }
int __stdcall BinkOpenXAudio2(int a1){ return 0; }
int __stdcall BinkPause(int a1,int a2){ return 0; }
int __stdcall BinkRegisterFrameBuffers(int a1,int a2){ return 0; }
int __stdcall BinkRegisterGPUDataBuffers(int a1,int a2){ return 0; }
int __stdcall BinkRequestStopAsyncThread(int a1){ return 0; }
int __stdcall BinkRestoreCursor(int a1){ return 0; }
int __stdcall BinkService(int a1){ return 0; }
int __stdcall BinkSetError(int a1){ return 0; }
int __stdcall BinkSetFileOffset(int a1,int a2){ return 0; }
int __stdcall BinkSetFrameRate(int a1,int a2){ return 0; }
int __stdcall BinkSetIO(int a1){ return 0; }
int __stdcall BinkSetIOSize(int a1){ return 0; }
int __stdcall BinkSetMemory(int a1,int a2){ return 0; }
int __stdcall BinkSetOSFileCallbacks(int a1,int a2,int a3,int a4){ return 0; }
int __stdcall BinkSetPan(int a1,int a2,int a3){ return 0; }
int __stdcall BinkSetSimulate(int a1){ return 0; }
int __stdcall BinkSetSoundOnOff(int a1,int a2){ apply_patch(); return 1; }
int __stdcall BinkSetSoundSystem2(int a1,int a2,int a3){ return 0; }
int __stdcall BinkSetSoundSystem(int a1,int a2){ apply_patch(); return 1; }
int __stdcall BinkSetSoundTrack(int a1,int a2){ apply_patch(); return 0; }
int __stdcall BinkSetSpeakerVolumes(int a1,int a2,int a3,int a4,int a5){ return 0; }
int __stdcall BinkSetVideoOnOff(int a1,int a2){ return 0; }
int __stdcall BinkSetVolume(int a1,int a2,int a3){ apply_patch(); return 1; }
int __stdcall BinkSetWillLoop(int a1,int a2){ return 0; }
int __stdcall BinkShouldSkip(int a1){ apply_patch(); return 1; }
int __stdcall BinkStartAsyncThread(int a1,int a2){ return 0; }
int __stdcall BinkUseTelemetry(int a1){ return 0; }
int __stdcall BinkUseTmLite(int a1){ return 0; }
int __stdcall BinkWait(int a1){ apply_patch(); return 0; }
int __stdcall BinkWaitStopAsyncThread(int a1){ return 0; }
int __stdcall RADTimerRead(void){ return 0; }
