#!/usr/bin/env python3
"""
bp_trace.py — hardware-breakpoint tracer. Set Dr0..Dr3 access breakpoints on up to
4 memory addresses in the running game; whenever the game reads/writes one, log the
instruction pointer (EIP) and resolve it to an ARET function. Used to find the code
that touches a creature's LEVEL field (e.g. the 4713 garbage value displayed above a
mob): a READ breakpoint fires every frame from the display code -> the creature
struct; a WRITE breakpoint catches whoever sets (or fails to set) the level.

Hardware breakpoints don't modify code (stealthier than INT3) and the game already
tolerates a debugger attach (see dbg_attach_test.py).

    python bp_trace.py --pid <pid> --addr 0x200ba3c 0x28bf9b0 ... --rw --seconds 6
"""
import argparse, bisect, csv, ctypes as C, sys, time, collections
from ctypes import wintypes

k32 = C.WinDLL("kernel32", use_last_error=True)
TH32CS_SNAPTHREAD = 0x4
CONTEXT_DEBUG_REGISTERS = 0x00010010   # i386 CONTEXT_CONTROL|DEBUG_REGISTERS-ish
CONTEXT_FULL_DBG = 0x00010017
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
EXCEPTION_SINGLE_STEP = 0x80000004
EXCEPTION_BREAKPOINT = 0x80000003


class THREADENTRY32(C.Structure):
    _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                ("th32ThreadID", wintypes.DWORD), ("th32OwnerProcessID", wintypes.DWORD),
                ("tpBasePri", wintypes.LONG), ("tpDeltaPri", wintypes.LONG),
                ("dwFlags", wintypes.DWORD)]


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


class EXCEPTION_RECORD(C.Structure):
    _fields_ = [("Code", wintypes.DWORD), ("Flags", wintypes.DWORD),
                ("Record", C.c_void_p), ("Address", C.c_void_p),
                ("NumberParameters", wintypes.DWORD), ("Information", C.c_void_p * 15)]


class DEBUG_EVENT(C.Structure):
    class _U(C.Union):
        _fields_ = [("ExceptionRecord", EXCEPTION_RECORD),
                    ("FirstChance", wintypes.DWORD), ("pad", C.c_byte * 184)]
    _fields_ = [("Code", wintypes.DWORD), ("ProcessId", wintypes.DWORD),
                ("ThreadId", wintypes.DWORD), ("u", _U)]


GetCtx = getattr(k32, "Wow64GetThreadContext", k32.GetThreadContext)
SetCtx = getattr(k32, "Wow64SetThreadContext", k32.SetThreadContext)
THREAD_ALL = 0x1F03FF


def thread_ids(pid):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    te = THREADENTRY32(); te.dwSize = C.sizeof(te); ids = []
    if k32.Thread32First(snap, C.byref(te)):
        while True:
            if te.th32OwnerProcessID == pid:
                ids.append(te.th32ThreadID)
            if not k32.Thread32Next(snap, C.byref(te)):
                break
    k32.CloseHandle(snap)
    return ids


def dr7_for(addrs, rw):
    """Dr7: enable L0..Ln, each as 4-byte read/write (cond=11) or write (cond=01)."""
    cond = 0b11 if rw else 0b01     # 11=read/write, 01=write-only
    length = 0b11                   # 4 bytes
    dr7 = 0
    for i in range(len(addrs)):
        dr7 |= (1 << (2 * i))                          # Ln local enable
        dr7 |= (cond << (16 + 4 * i))                  # R/W condition
        dr7 |= (length << (18 + 4 * i))                # LEN
    return dr7


def set_bps(tid, addrs, dr7):
    h = k32.OpenThread(THREAD_ALL, False, tid)
    if not h:
        return
    # Dr writes only stick on a SUSPENDED thread — true for both arming AND clearing.
    # A clear that doesn't stick leaves a live Dr that fires post-detach -> crash.
    k32.SuspendThread(h)
    try:
        ctx = CONTEXT(); ctx.ContextFlags = CONTEXT_FULL_DBG
        if GetCtx(h, C.byref(ctx)):
            ctx.Dr0 = ctx.Dr1 = ctx.Dr2 = ctx.Dr3 = 0
            ctx.Dr6 = 0
            for i, a in enumerate(addrs):
                setattr(ctx, f"Dr{i}", a)
            ctx.Dr7 = dr7
            ctx.ContextFlags = CONTEXT_FULL_DBG
            SetCtx(h, C.byref(ctx))
    finally:
        k32.ResumeThread(h)
        k32.CloseHandle(h)


def clear_all(pid):
    """Fully zero debug registers on every thread before detaching."""
    for tid in thread_ids(pid):
        set_bps(tid, [], 0)


def load_index(path):
    ents = []
    for row in csv.DictReader(open(path)):
        ents.append((int(row["entry"], 16), row["name"]))
    ents.sort()
    return [e[0] for e in ents], [e[1] for e in ents]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int, required=True)
    ap.add_argument("--addr", nargs="+", required=True, help="up to 4 hex addresses")
    ap.add_argument("--rw", action="store_true", help="read+write (default: write only)")
    ap.add_argument("--seconds", type=float, default=6)
    ap.add_argument("--index", default="aret_index.csv")
    ap.add_argument("--max-hits", type=int, default=200)
    a = ap.parse_args()
    addrs = [int(x, 16) for x in a.addr][:4]
    starts, names = load_index(a.index)
    def fn(eip):
        i = bisect.bisect_right(starts, eip) - 1
        return (names[i], starts[i]) if i >= 0 else ("?", 0)

    dr7 = dr7_for(addrs, a.rw)
    k32.DebugSetProcessKillOnExit(False)
    if not k32.DebugActiveProcess(a.pid):
        print("attach failed", C.get_last_error()); sys.exit(1)
    print(f"[bp] attached; {'R/W' if a.rw else 'WRITE'} bps on", [hex(x) for x in addrs])
    for tid in thread_ids(a.pid):
        set_bps(tid, addrs, dr7)

    evt = DEBUG_EVENT()
    hits = collections.Counter()
    examples = {}
    end = time.time() + a.seconds
    total = 0
    while time.time() < end and total < a.max_hits:
        if not k32.WaitForDebugEvent(C.byref(evt), 200):
            continue
        cont = DBG_CONTINUE
        if evt.Code == 1:  # EXCEPTION
            exc = evt.u.ExceptionRecord.Code
            if exc == EXCEPTION_SINGLE_STEP:
                h = k32.OpenThread(THREAD_ALL, False, evt.ThreadId)
                ctx = CONTEXT(); ctx.ContextFlags = CONTEXT_FULL_DBG
                if h and GetCtx(h, C.byref(ctx)):
                    which = ctx.Dr6 & 0xF
                    idx = (which & 1 and 0) or (which & 2 and 1) or (which & 4 and 2) or (which & 8 and 3)
                    n, s = fn(ctx.Eip)
                    key = (idx, n)
                    hits[key] += 1
                    if key not in examples:
                        examples[key] = (ctx.Eip, addrs[idx] if idx < len(addrs) else 0)
                    ctx.Dr6 = 0                       # clear status
                    ctx.ContextFlags = CONTEXT_FULL_DBG
                    SetCtx(h, C.byref(ctx))
                    total += 1
                if h:
                    k32.CloseHandle(h)
            elif exc == EXCEPTION_BREAKPOINT:
                pass
            else:
                cont = DBG_EXCEPTION_NOT_HANDLED
        elif evt.Code == 2:  # CREATE_THREAD -> arm it too
            set_bps(evt.ThreadId, addrs, dr7)
        k32.ContinueDebugEvent(evt.ProcessId, evt.ThreadId, cont)

    # clear breakpoints on EVERY thread (twice, to catch races) before detaching
    clear_all(a.pid); clear_all(a.pid)
    k32.DebugActiveProcessStop(a.pid)
    print(f"\n[bp] {total} hits. By (Dr#, function):")
    for (idx, n), c in hits.most_common(20):
        eip, addr = examples[(idx, n)]
        print(f"  Dr{idx} @0x{addr:x}  {c:5d}x  EIP 0x{eip:x}  {n}")
    print("[bp] game alive:", bool(k32.OpenProcess(0x1000, False, a.pid)))


if __name__ == "__main__":
    main()
