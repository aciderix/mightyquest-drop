#!/usr/bin/env python3
"""Minimal: can we attach a debugger to the game without UBX anti-debug killing it?
Attaches, pumps a few debug events, detaches (without killing the game)."""
import ctypes as C, sys, time
from ctypes import wintypes

k32 = C.WinDLL("kernel32", use_last_error=True)


class EXCEPTION_RECORD(C.Structure):
    _fields_ = [("Code", wintypes.DWORD), ("Flags", wintypes.DWORD),
                ("Record", C.c_void_p), ("Address", C.c_void_p),
                ("NumberParameters", wintypes.DWORD),
                ("Information", C.c_void_p * 15)]


class EXCEPTION_DEBUG_INFO(C.Structure):
    _fields_ = [("ExceptionRecord", EXCEPTION_RECORD), ("FirstChance", wintypes.DWORD)]


class DEBUG_EVENT(C.Structure):
    class _U(C.Union):
        _fields_ = [("Exception", EXCEPTION_DEBUG_INFO), ("pad", C.c_byte * 160)]
    _fields_ = [("DebugEventCode", wintypes.DWORD), ("ProcessId", wintypes.DWORD),
                ("ThreadId", wintypes.DWORD), ("u", _U)]


DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001


def main():
    pid = int(sys.argv[1])
    k32.DebugSetProcessKillOnExit(False)      # detaching must NOT kill the game
    if not k32.DebugActiveProcess(pid):
        print("DebugActiveProcess failed err", C.get_last_error()); sys.exit(1)
    print("[attach] OK, pumping events for ~4s...")
    evt = DEBUG_EVENT()
    end = time.time() + 4
    n = 0
    while time.time() < end:
        if k32.WaitForDebugEvent(C.byref(evt), 200):
            n += 1
            code = evt.DebugEventCode
            cont = DBG_CONTINUE
            if code == 1:   # EXCEPTION_DEBUG_EVENT
                exc = evt.u.Exception.ExceptionRecord.Code
                # pass non-breakpoint first-chance exceptions back to the app
                if exc not in (0x80000003, 0x80000004):
                    cont = DBG_EXCEPTION_NOT_HANDLED
            k32.ContinueDebugEvent(evt.ProcessId, evt.ThreadId, cont)
    print(f"[attach] pumped {n} debug events; detaching...")
    k32.DebugActiveProcessStop(pid)
    alive = k32.OpenProcess(0x1000, False, pid)
    print("[attach] detached. game still alive:", bool(alive))


if __name__ == "__main__":
    main()
