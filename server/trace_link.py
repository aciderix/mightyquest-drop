#!/usr/bin/env python3
"""
trace_link.py — link sampled game EIPs to functions and to the server timeline.

Pipeline:
    code_sampler.py  -> samples.jsonl   (epoch_ms, tid, eip)
    aret --split     -> index.csv       (function entry points)
    server           -> trace.jsonl     (epoch of each request) [optional]
    trace_link.py    -> hot functions, overall and inside a time window

The game loads its main module at base 0x400000 (confirmed: crash addresses from the
minidump match the unpacked exe VAs), so a sampled EIP in [.text] maps directly to an
ARET function. We bucket samples by the function whose entry is the greatest entry <=
EIP, and we can restrict to a [--from-ms,--to-ms] window (e.g. right after the server
answered /StartAttack) to see exactly which game code ran to process that answer.

    python trace_link.py --samples samples.jsonl --index split/index.csv \
        [--window-after StartAttack] [--trace trace.jsonl] [--top 40]
"""
import argparse, bisect, csv, json, collections, os

TEXT_LO, TEXT_HI = 0x401000, 0xDEB000     # unpacked .text range (game code)


def load_index(path):
    ents = []
    with open(path) as f:
        for row in csv.DictReader(f):
            ents.append((int(row["entry"], 16), row["name"]))
    ents.sort()
    return [e[0] for e in ents], [e[1] for e in ents]


def load_samples(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def load_trace(path):
    """server requests with epoch_ms (best-effort: parse ts ISO -> ms)."""
    import datetime
    reqs = []
    if not path or not os.path.exists(path):
        return reqs
    for line in open(path):
        try:
            j = json.loads(line)
            ts = j.get("ts", "")
            dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            reqs.append((int(dt.timestamp() * 1000), j.get("method", "?"), j.get("flags", "")))
        except Exception:
            pass
    return reqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", required=True)
    ap.add_argument("--index", required=True)
    ap.add_argument("--trace")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--from-ms", type=int, default=0)
    ap.add_argument("--to-ms", type=int, default=0)
    ap.add_argument("--window-after", help="method name; restrict to [req, req+win-ms]")
    ap.add_argument("--win-ms", type=int, default=1500)
    ap.add_argument("--main-thread-only", action="store_true",
                    help="only the thread with the most in-.text samples (gameplay)")
    a = ap.parse_args()

    starts, names = load_index(a.index)
    samples = load_samples(a.samples)
    reqs = load_trace(a.trace)

    # optional window from a server request
    lo, hi = a.from_ms, a.to_ms
    if a.window_after and reqs:
        for t, m, fl in reqs:
            if m == a.window_after:
                lo, hi = t, t + a.win_ms
                print(f"[window] {a.window_after} @ {t} -> [{lo},{hi}]  (+{a.win_ms}ms)")
                break

    # pick gameplay thread: most samples landing in game .text
    if a.main_thread_only:
        per_tid = collections.Counter()
        for s in samples:
            if TEXT_LO <= s["eip"] < TEXT_HI:
                per_tid[s["tid"]] += 1
        if per_tid:
            main_tid = per_tid.most_common(1)[0][0]
            samples = [s for s in samples if s["tid"] == main_tid]
            print(f"[thread] gameplay tid={main_tid} ({per_tid[main_tid]} text samples)")

    def fn_of(eip):
        i = bisect.bisect_right(starts, eip) - 1
        return names[i] if i >= 0 else "?"

    hot = collections.Counter()
    in_text = 0
    for s in samples:
        if lo and not (lo <= s["t"] <= hi):
            continue
        eip = s["eip"]
        if TEXT_LO <= eip < TEXT_HI:
            hot[fn_of(eip)] += 1
            in_text += 1
    label = f"window [{lo},{hi}]" if lo else "whole capture"
    print(f"\n=== hot game functions ({label}; {in_text} in-.text samples) ===")
    for fn, c in hot.most_common(a.top):
        start = starts[names.index(fn)]
        print(f"  {c:6d}  {fn:16s} 0x{start:x}")

    if reqs:
        print("\n=== server requests (epoch_ms) ===")
        for t, m, fl in reqs[-12:]:
            print(f"  {t}  {m} {fl}")


if __name__ == "__main__":
    main()
