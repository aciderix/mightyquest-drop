#!/usr/bin/env python3
"""debuglog.py — structured, AI-friendly tracing of every request the live game
makes against the server.

Goal: when a problem is seen in-game, any AI (even with NO prior context) can open
trace.jsonl, find the matching request, and read exactly:
  - which Service.Method was called and with what body,
  - WHERE the response came from (a real handler, the social router, or the
    schema-example FALLBACK — the #1 reason something looks "inert" in-game),
  - any FLAGS worth attention (fallback used, value derived/not-from-catalog,
    command rejected, uncertain enum, missing handler, exception),
  - for SendCommands: each command and whether it mutated state.

Every line is one JSON object. Read with diagnose.py for a summary.

Env:
  MQ_TRACE   path to the trace file (default: <server>/trace.jsonl)
  MQ_DEBUG   "1" to also echo a one-line summary to stdout
"""
from __future__ import annotations
import datetime, json, os, threading

HERE = os.path.dirname(os.path.abspath(__file__))
TRACE_PATH = os.environ.get("MQ_TRACE", os.path.join(HERE, "trace.jsonl"))
DEBUG = os.environ.get("MQ_DEBUG", "") in ("1", "true", "yes")
_lock = threading.Lock()
_seq = 0
_MAXLEN = 6000


def _now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _short(obj):
    try:
        s = json.dumps(obj, default=str, ensure_ascii=False)
    except Exception:
        s = str(obj)
    return s if len(s) <= _MAXLEN else s[:_MAXLEN] + "...<truncated>"


def trace(event: dict):
    """Append one structured event. Never raises (logging must not break serving)."""
    global _seq
    try:
        with _lock:
            _seq += 1
            rec = {"ts": _now(), "seq": _seq}
            rec.update(event)
            line = json.dumps(rec, default=str, ensure_ascii=False)
            if len(line) > _MAXLEN * 2:
                line = line[:_MAXLEN * 2] + '...<truncated>"}'
            with open(TRACE_PATH, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            if DEBUG:
                flags = rec.get("flags") or []
                print(f"[trace #{_seq}] {rec.get('method','-')} <- {rec.get('source','-')}"
                      + (f"  FLAGS={flags}" if flags else ""))
    except Exception:
        pass


def banner():
    return f"[debug] tracing -> {TRACE_PATH}" + ("  (MQ_DEBUG on)" if DEBUG else "")
