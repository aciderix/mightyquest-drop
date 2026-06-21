#include <windows.h>
typedef struct { unsigned int Width,Height,Frames,FrameNum,LastFrameNum; unsigned char pad[0x800]; } BINK;
/* Vectored exception handler: when the game null-derefs (fault addr < 0x10000)
   via a `mov r32,[mem]` (0x8B) or `mov [mem],r32` (0x89) in the main image,
   skip the faulting instruction (zero the dest reg for loads). This generically
   survives the uninitialised font/glyph-manager reads under Wine so the client
   boots past InitFonts to the CEF/HTML UI (which renders text itself). */
static volatile long g_skips=0;
static int insn_len_8x(const unsigned char* p, int* dest_reg, int* is_load){
  int i=0; unsigned char op=p[i++];
  *is_load=(op==0x8B); 
  unsigned char modrm=p[i++];
  int mod=modrm>>6, reg=(modrm>>3)&7, rm=modrm&7;
  *dest_reg=reg;
  if(mod!=3 && rm==4){ unsigned char sib=p[i]; i++; if(mod==0 && (sib&7)==5) i+=4; }
  if(mod==1) i+=1; else if(mod==2) i+=4; else if(mod==0 && rm==5) i+=4;
  return i;
}
static LONG CALLBACK veh(EXCEPTION_POINTERS* ep){
  EXCEPTION_RECORD* er=ep->ExceptionRecord; CONTEXT* c=ep->ContextRecord;
  if(er->ExceptionCode!=0xC0000005) return EXCEPTION_CONTINUE_SEARCH;
  if(er->NumberParameters<2) return EXCEPTION_CONTINUE_SEARCH;
  ULONG_PTR fault=er->ExceptionInformation[1];
  if(fault>=0x10000 && fault<0xFFF00000) return EXCEPTION_CONTINUE_SEARCH;  /* null-ish: low OR null+neg-disp */
  DWORD eip=c->Eip;
  if(eip<0x9C0000 || eip>=0xA0A000) return EXCEPTION_CONTINUE_SEARCH; /* font/text render range only */
  unsigned char* p=(unsigned char*)eip;
  if(IsBadReadPtr(p,8)) return EXCEPTION_CONTINUE_SEARCH;
  DWORD* regs[8]={&c->Eax,&c->Ecx,&c->Edx,&c->Ebx,&c->Esp,&c->Ebp,&c->Esi,&c->Edi};
  unsigned char op=p[0]; int reg=0,is_load=0,len=0;
  if(op==0x0F && (p[1]==0xB6||p[1]==0xB7)){ /* movzx r32, r/m8/16 -> zero dest, skip */
     int rr,dl; len=1+insn_len_8x(p+1,&rr,&dl); reg=rr; *regs[reg]=0; c->Eip+=len; InterlockedIncrement(&g_skips);
     if(g_skips==1){HANDLE m=CreateFileA("Z:\\tmp\\veh_active.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0); if(m!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(m,"veh\n",4,&w,0);CloseHandle(m);} }
     return EXCEPTION_CONTINUE_EXECUTION; }
  if(op==0x8B||op==0x89||op==0x8A||op==0x3B||op==0x33||op==0x03||op==0x0B||op==0x23||op==0x2B){
     len=insn_len_8x(p,&reg,&is_load);
     if(len<2||len>7) return EXCEPTION_CONTINUE_SEARCH;
     if(op==0x8B||op==0x8A||op==0x3B||op==0x33||op==0x03||op==0x0B||op==0x23||op==0x2B) *regs[reg]=0; /* dest=reg loads: zero it */
     c->Eip += len;
  } else if(op==0xFF){
     int rr,dl; len=insn_len_8x(p,&rr,&dl); int digit=rr;
     if(len<2||len>7) return EXCEPTION_CONTINUE_SEARCH;
     if(digit==6){ /* push r/m32 -> push 0 to keep stack balanced */
        c->Esp -= 4; *(DWORD*)(c->Esp)=0; c->Eip += len;
     } else if(digit==2 || digit==3){ /* call indirect -> skip (no call); leaves pushed args, best-effort */
        c->Eip += len;
     } else { /* jmp(4/5)/inc/dec etc through null: cannot safely recover */
        return EXCEPTION_CONTINUE_SEARCH; }
  } else { return EXCEPTION_CONTINUE_SEARCH; }
  InterlockedIncrement(&g_skips);
  if(g_skips==1){ HANDLE m=CreateFileA("Z:\\tmp\\veh_active.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
    if(m!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(m,"veh\n",4,&w,0);CloseHandle(m);} }
  return EXCEPTION_CONTINUE_EXECUTION;
}

BOOL WINAPI DllMain(HINSTANCE h,DWORD r,LPVOID v){ if(r==DLL_PROCESS_ATTACH){ DisableThreadLibraryCalls(h); AddVectoredExceptionHandler(1,veh);} return TRUE; }
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
int __stdcall BinkGetRects(int a1,int a2){ return 0; }
int __stdcall BinkGetSummary(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackData(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackID(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackMaxSize(int a1,int a2){ return 0; }
int __stdcall BinkGetTrackType(int a1,int a2){ return 0; }
int __stdcall BinkGoto(int a1,int a2,int a3){ return 0; }
int __stdcall BinkIsSoftwareCursor(int a1,int a2){ return 0; }
int __stdcall BinkLogoAddress(void){ return 0; }
int __stdcall BinkNextFrame(int a1){ if(a1){((BINK*)a1)->FrameNum+=1;} return 0; }
int __stdcall BinkOpen(int a1,int a2){ return 0; }
int __stdcall BinkOpenDirectSound(int a1){ return 0; }
int __stdcall BinkOpenMiles(int a1){ return 0; }
int __stdcall BinkOpenTrack(int a1,int a2){ return 0; }
int __stdcall BinkOpenWaveOut(int a1){ return 0; }
int __stdcall BinkOpenWithOptions(int a1,int a2,int a3){ return 0; }
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
int __stdcall BinkSetSoundOnOff(int a1,int a2){ return 0; }
int __stdcall BinkSetSoundSystem2(int a1,int a2,int a3){ return 0; }
int __stdcall BinkSetSoundSystem(int a1,int a2){ return 0; }
int __stdcall BinkSetSoundTrack(int a1,int a2){ return 0; }
int __stdcall BinkSetSpeakerVolumes(int a1,int a2,int a3,int a4,int a5){ return 0; }
int __stdcall BinkSetVideoOnOff(int a1,int a2){ return 0; }
int __stdcall BinkSetVolume(int a1,int a2,int a3){ return 0; }
int __stdcall BinkSetWillLoop(int a1,int a2){ return 0; }
int __stdcall BinkShouldSkip(int a1){ return 1; }
int __stdcall BinkStartAsyncThread(int a1,int a2){ return 0; }
int __stdcall BinkUseTelemetry(int a1){ return 0; }
int __stdcall BinkUseTmLite(int a1){ return 0; }
int __stdcall BinkWait(int a1){ return 0; }
int __stdcall BinkWaitStopAsyncThread(int a1){ return 0; }
int __stdcall RADTimerRead(void){ return 0; }
