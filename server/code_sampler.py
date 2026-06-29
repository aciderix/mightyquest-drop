#!/usr/bin/env python3
"""
code_sampler.py — sampling profiler that links the RUNNING game's native code to
our server/game logs.

Idea (user's): while the game runs, repeatedly read every thread's instruction
pointer (EIP) and timestamp it. Map each EIP -> function via the ARET decompiler's
index. Then a sample taken right after the server answered (say) /StartAttack tells
us *which game functions were executing* to process that answer — e.g. where the
mob levels get computed. aret then decompiles those exact addresses to readable C.

We use SuspendThread + GetThreadContext (NOT the Win32 Debug API / DebugActiveProcess)
on purpose: the game is UBX-packed with anti-tamper, and a real debugger attach can
trip it. Reading thread contexts is passive and the existing launcher already proves
plain ReadProcessMemory works on this process.

Usage:
    python code_sampler.py --pid <pid> --seconds 60 --out samples.jsonl
    python code_sampler.py --name MightyQuest --hz 2000 --out samples.jsonl
Each line: {"t": <epoch_ms>, "tid": <id>, "eip": <int>}  (symbolization is a
separate step so sampling stays as fast as possible — see trace_link.py).
"""
import argparse, ctypes as C, json, time, sys
from ctypes import wintypes

k32 = C.WinDLL("kernel32", use_last_error=True)
adv = C.WinDLL("advapi32", use_last_error=True)

TH32CS_SNAPTHREAD = 0x00000004
THREAD_SUSPEND_RESUME = 0x0002
THREAD_GET_CONTEXT = 0x0008
WOW64_CONTEXT_CONTROL = 0x00010001    # WOW64 (i386) CONTEXT_CONTROL (Eip/Esp/Ebp)


def enable_debug_privilege():
    """SeDebugPrivilege so OpenThread on the game's threads succeeds."""
    TOKEN_ADJUST_PRIVILEGES = 0x20; TOKEN_QUERY = 0x8; SE_PRIVILEGE_ENABLED = 0x2
    class LUID(C.Structure):
        _fields_ = [("Low", wintypes.DWORD), ("High", wintypes.LONG)]
    class LUID_AND_ATTR(C.Structure):
        _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]
    class TOKEN_PRIVILEGES(C.Structure):
        _fields_ = [("Count", wintypes.DWORD), ("Priv", LUID_AND_ATTR)]
    h = wintypes.HANDLE()
    if not adv.OpenProcessToken(k32.GetCurrentProcess(),
                                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, C.byref(h)):
        return False
    luid = LUID()
    if not adv.LookupPrivilegeValueW(None, "SeDebugPrivilege", C.byref(luid)):
        return False
    tp = TOKEN_PRIVILEGES(1, LUID_AND_ATTR(luid, SE_PRIVILEGE_ENABLED))
    adv.AdjustTokenPrivileges(h, False, C.byref(tp), 0, None, None)
    return C.get_last_error() == 0


class THREADENTRY32(C.Structure):
    _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                ("th32ThreadID", wintypes.DWORD), ("th32OwnerProcessID", wintypes.DWORD),
                ("tpBasePri", wintypes.LONG), ("tpDeltaPri", wintypes.LONG),
                ("dwFlags", wintypes.DWORD)]


# i386 CONTEXT — we only need EIP, but the struct must be the right size/layout.
class FLOATING_SAVE_AREA(C.Structure):
    _fields_ = [("ControlWord", wintypes.DWORD), ("StatusWord", wintypes.DWORD),
                ("TagWord", wintypes.DWORD), ("ErrorOffset", wintypes.DWORD),
                ("ErrorSelector", wintypes.DWORD), ("DataOffset", wintypes.DWORD),
                ("DataSelector", wintypes.DWORD), ("RegisterArea", C.c_byte * 80),
                ("Cr0NpxState", wintypes.DWORD)]


class CONTEXT(C.Structure):
    _fields_ = [("ContextFlags", wintypes.DWORD),
                ("Dr0", wintypes.DWORD), ("Dr1", wintypes.DWORD), ("Dr2", wintypes.DWORD),
                ("Dr3", wintypes.DWORD), ("Dr6", wintypes.DWORD), ("Dr7", wintypes.DWORD),
                ("FloatSave", FLOATING_SAVE_AREA),
                ("SegGs", wintypes.DWORD), ("SegFs", wintypes.DWORD),
                ("SegEs", wintypes.DWORD), ("SegDs", wintypes.DWORD),
                ("Edi", wintypes.DWORD), ("Esi", wintypes.DWORD), ("Ebx", wintypes.DWORD),
                ("Edx", wintypes.DWORD), ("Ecx", wintypes.DWORD), ("Eax", wintypes.DWORD),
                ("Ebp", wintypes.DWORD), ("Eip", wintypes.DWORD), ("SegCs", wintypes.DWORD),
                ("EFlags", wintypes.DWORD), ("Esp", wintypes.DWORD), ("SegSs", wintypes.DWORD),
                ("ExtendedRegisters", C.c_byte * 512)]


def find_pid(name):
    import subprocess
    out = subprocess.check_output(["tasklist", "/FI", f"IMAGENAME eq {name}.exe", "/FO", "CSV", "/NH"],
                                  text=True, errors="replace")
    for line in out.splitlines():
        if name.lower() in line.lower():
            return int(line.split(",")[1].strip('"'))
    return None


def thread_ids(pid):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    te = THREADENTRY32(); te.dwSize = C.sizeof(te)
    ids = []
    if k32.Thread32First(snap, C.byref(te)):
        while True:
            if te.th32OwnerProcessID == pid:
                ids.append(te.th32ThreadID)
            if not k32.Thread32Next(snap, C.byref(te)):
                break
    k32.CloseHandle(snap)
    return ids


def sample(pid, seconds, hz, out):
    handles = {}
    def hopen(tid):
        if tid not in handles:
            handles[tid] = k32.OpenThread(THREAD_SUSPEND_RESUME | THREAD_GET_CONTEXT, False, tid)
        return handles[tid]
    period = 1.0 / hz
    end = time.time() + seconds
    n = 0; open_fail = 0; ctx_fail = 0
    last_refresh = 0
    tids = thread_ids(pid)
    f = open(out, "w")
    ctx = CONTEXT()
    # 32-bit (WOW64) thread context — must use Wow64GetThreadContext from 64-bit py
    GetCtx = getattr(k32, "Wow64GetThreadContext", k32.GetThreadContext)
    while time.time() < end:
        now = time.time()
        if now - last_refresh > 1.0:           # refresh thread list (new combat threads)
            tids = thread_ids(pid); last_refresh = now
        for tid in tids:
            h = hopen(tid)
            if not h:
                open_fail += 1; continue
            if k32.SuspendThread(h) == 0xFFFFFFFF:
                continue
            ctx.ContextFlags = WOW64_CONTEXT_CONTROL
            ok = GetCtx(h, C.byref(ctx))
            eip = ctx.Eip if ok else 0
            k32.ResumeThread(h)
            if not ok:
                ctx_fail += 1
            if eip:
                f.write('{"t":%d,"tid":%d,"eip":%d}\n' % (int(now * 1000), tid, eip))
                n += 1
        time.sleep(period)
    f.close()
    print(f"[sampler] open_fail={open_fail} ctx_fail={ctx_fail}")
    for h in handles.values():
        if h:
            k32.CloseHandle(h)
    print(f"[sampler] wrote {n} samples to {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int)
    ap.add_argument("--name", default="MightyQuest")
    ap.add_argument("--seconds", type=float, default=60)
    ap.add_argument("--hz", type=float, default=2000)
    ap.add_argument("--out", default="samples.jsonl")
    a = ap.parse_args()
    print("[sampler] SeDebugPrivilege:", enable_debug_privilege())
    pid = a.pid or find_pid(a.name)
    if not pid:
        print("game process not found"); sys.exit(1)
    print(f"[sampler] pid={pid} hz={a.hz} for {a.seconds}s -> {a.out}")
    sample(pid, a.seconds, a.hz, a.out)


if __name__ == "__main__":
    main()
