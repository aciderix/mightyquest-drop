#include <windows.h>
typedef struct { unsigned int Width,Height,Frames,FrameNum,LastFrameNum; unsigned char pad[0x800]; } BINK;
/* Gemini #3: neutralise render_text_element @0x991A80 by forcing its existing
   early-return (je 0x991ACE at 0x991A8A) to an unconditional jmp. 1 byte:
   0x74 (je) -> 0xEB (jmp). Skips all engine text rendering (loading screen etc.)
   so the uninitialised glyph manager is never touched -> no crash, no infinite
   layout; CEF/HTML UI still renders its own text. Applied at movie time (after
   the packer has unpacked .text). */
static volatile int g_done=0;
static void apply_patch(void){
  unsigned char* je=(unsigned char*)0x991A8A;  /* the conditional jump byte */
  DWORD old;
  if(g_done) return;
  if(IsBadReadPtr(je,2)) return;
  if(je[0]!=0x74) return;                       /* not unpacked yet / already patched */
  if(VirtualProtect(je,2,PAGE_EXECUTE_READWRITE,&old)){
    je[0]=0xEB;                                 /* je -> jmp (always skip text render) */
    VirtualProtect(je,2,old,&old);
    FlushInstructionCache(GetCurrentProcess(),je,2);
    g_done=1;
    HANDLE m=CreateFileA("Z:\\tmp\\binkpatch_ok.txt",GENERIC_WRITE,0,0,CREATE_ALWAYS,0,0);
    if(m!=INVALID_HANDLE_VALUE){DWORD w;WriteFile(m,"ok\n",3,&w,0);CloseHandle(m);}
  }
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
