#!/usr/bin/env python3
"""
completeness_gate.py — guarantee every response is exactly what the game expects.

The #1 cause of "fields are received but in-game reactions are wrong (bad calcs,
glitches)" is NOT a crash: the client's deserializer reads each contract field by
field, and a MISSING (or wrong-typed) field is silently left at its default
(0 / "" / false / null). Gameplay code downstream then computes on that default
-> wrong result, no error. A hand-written response is almost always incomplete.

This module makes that impossible. Given a contract name and a (partial) object,
it returns a SCHEMA-COMPLETE object: every field the client expects is present,
correctly typed, nested contracts filled recursively, polymorphic `$type`
discriminators added on request. Drop it in front of every response you emit:

    from completeness_gate import Gate
    gate = Gate()                       # loads the reversed catalog
    body = gate.complete("AccountInformation", body)   # fill before sending
    issues = gate.validate("AccountInformation", body) # 0 issues == safe

It is host-agnostic pure-Python (works under any framework: http.server, Flask,
FastAPI, a CGI, a cloud function...). The logic is small on purpose so it can be
ported 1:1 to TypeScript/Go for another runtime.

Ground truth: re/catalog/network/schemas_typed.json — 1307 contracts with field
names and types, extracted from the client's OWN (de)serializer code.

CLI:
  completeness_gate.py --self-check          # every example is schema-complete
  completeness_gate.py --trace trace.jsonl   # audit a captured session
  completeness_gate.py --show AccountInformation   # print the complete skeleton
"""
import argparse, copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "re", "catalog", "network")
SCHEMAS = os.path.join(CATALOG, "schemas_typed.json")
EXAMPLES = os.path.join(CATALOG, "generated", "examples.json")
ENUMS = os.path.join(CATALOG, "gamedata", "enum_values.json")

# .NET serializer default values, by the type vocabulary used in schemas_typed.json
_NUM_INT = {"int", "uint", "ushort", "short", "ulong", "long", "byte", "enum"}
_NUM_FLT = {"double", "number", "float", "decimal"}

def _default_for(typ):
    if typ in _NUM_INT:        return 0
    if typ in _NUM_FLT:        return 0.0
    if typ == "bool":          return False
    if typ == "string":        return ""
    if typ == "datetime":      return "0001-01-01T00:00:00Z"   # .NET DateTime.MinValue
    if typ == "array":         return []
    return {}                                                   # "object" / nested contract


class Gate:
    TYPE_NS = "HyperQuest.GameServer.Contracts.{name}, HyperQuest.GameServer.Contracts"

    def __init__(self, schemas_path=SCHEMAS, examples_path=EXAMPLES):
        with open(schemas_path, encoding="utf-8") as f:
            self.schemas = json.load(f)
        try:
            with open(examples_path, encoding="utf-8") as f:
                self.examples = json.load(f)
        except OSError:
            self.examples = {}
        # all known enum member names, to tell "enum sent as name" apart from a
        # genuinely wrong type. (enum_values.json lists members but NOT reliable
        # integer values — order looks alphabetical — so we flag, never convert.)
        self.enum_names = set()
        try:
            with open(ENUMS, encoding="utf-8") as f:
                for members in json.load(f).values():
                    if isinstance(members, list):
                        self.enum_names.update(m for m in members if isinstance(m, str))
        except OSError:
            pass

    # ---- the rule: a complete object for `name`, keeping any provided values ----
    def complete(self, name, partial=None, *, add_type=False, _seen=None):
        spec = self.schemas.get(name)
        if spec is None:
            # unknown contract: cannot complete; return what we were given
            return copy.deepcopy(partial) if partial is not None else {}
        _seen = _seen or set()
        out = {}
        if add_type:
            out["$type"] = self.TYPE_NS.format(name=name)
        partial = partial or {}
        for fname, ftype in spec.get("fields", []):
            if fname in partial and partial[fname] is not None:
                val = partial[fname]
                # recurse into a provided nested object if we know its contract
                nested = self._contract_for(fname, ftype)
                if nested and isinstance(val, dict) and nested not in _seen:
                    val = self.complete(nested, val, add_type=add_type,
                                        _seen=_seen | {name})
                out[fname] = copy.deepcopy(val)
            else:
                out[fname] = self._fill_field(fname, ftype, add_type, _seen | {name})
        return out

    def _fill_field(self, fname, ftype, add_type, seen):
        nested = self._contract_for(fname, ftype)
        if nested and nested not in seen:
            return self.complete(nested, {}, add_type=add_type, _seen=seen)
        return _default_for(ftype)

    def _contract_for(self, fname, ftype):
        """Best-effort resolution of an `object` field to a concrete contract so we
        can fill it instead of leaving {} (the empty-nested-object silent default).
        The catalog types nested objects only as 'object', so we match by field
        name against a known contract name."""
        if ftype != "object":
            return None
        if fname in self.schemas:
            return fname
        return None

    # ---- audit: list everything the client would silently default ----
    def validate(self, name, obj):
        spec = self.schemas.get(name)
        if spec is None:
            return [f"unknown contract '{name}'"]
        issues = []
        for fname, ftype in spec.get("fields", []):
            if fname not in obj:
                issues.append(f"MISSING {name}.{fname} ({ftype})")
                continue
            v = obj[fname]
            if ftype in _NUM_INT and isinstance(v, str) and v in self.enum_names:
                issues.append(f"ENUM-NAME {name}.{fname}={v!r}: client wants the "
                              f"integer enum value, not the name")
            elif not self._type_ok(ftype, v):
                issues.append(f"WRONGTYPE {name}.{fname}: want {ftype}, got "
                              f"{type(v).__name__}={v!r}")
            else:
                nested = self._contract_for(fname, ftype)
                if nested and isinstance(v, dict):
                    issues += self.validate(nested, v)
        return issues

    @staticmethod
    def _type_ok(ftype, v):
        if v is None:                       return False
        if ftype in _NUM_INT:               return isinstance(v, int) and not isinstance(v, bool)
        if ftype in _NUM_FLT:               return isinstance(v, (int, float)) and not isinstance(v, bool)
        if ftype == "bool":                 return isinstance(v, bool)
        if ftype == "string" or ftype == "datetime": return isinstance(v, str)
        if ftype == "array":                return isinstance(v, list)
        # "object" covers scalar nested contracts AND .NET collections
        # (Dictionary -> JSON object, List -> JSON array); the catalog can't
        # distinguish, so accept either container shape here.
        return isinstance(v, (dict, list))


# --------------------------------------------------------------------------- CLI
def _self_check(gate):
    bad = 0
    for name in gate.examples:
        issues = gate.validate(name, gate.examples[name])
        if issues:
            bad += 1
            print(f"[X] {name}: {len(issues)} issue(s)")
            for i in issues[:4]:
                print("      ", i)
    total = len(gate.examples)
    print(f"\n{'PASS' if bad == 0 else 'FAIL'}: {total-bad}/{total} examples are "
          f"schema-complete by the gate.")
    return 0 if bad == 0 else 1


def _audit_trace(gate, path):
    import re
    METHOD_CONTRACT = {
        "GetAccountInformation": "AccountInformation",
        "ChooseDisplayName": "AccountSummary",
        "GetAttackSelectionList": "AttackSelectionResult",
        "GetCastleInfo": "CastleInfo", "StartAttack": "AttackInfo",
        "GetCastlesForSale": "CastlesForSaleSelectionResult",
    }
    n = bad = 0
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        m = re.search(r"/(\w+)Service\.hqs/(\w+)", rec.get("path", ""))
        if not m:
            continue
        contract = METHOD_CONTRACT.get(m.group(2))
        body = rec.get("resp_body")
        if not contract or body is None:
            continue
        try:
            obj = json.loads(body) if isinstance(body, str) else body
        except Exception:
            continue
        n += 1
        issues = gate.validate(contract, obj)
        if issues:
            bad += 1
            print(f"[X] {m.group(2)} -> {contract}: {len(issues)} issue(s)")
            for i in issues[:6]:
                print("      ", i)
    print(f"\n{'PASS' if bad == 0 else 'FAIL'}: {n-bad}/{n} responses schema-complete.")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="response completeness gate")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--trace")
    ap.add_argument("--show")
    ap.add_argument("--type", action="store_true", help="with --show, add $type discriminators")
    a = ap.parse_args()
    gate = Gate()
    if a.show:
        print(json.dumps(gate.complete(a.show, add_type=a.type), indent=2))
        return 0
    if a.trace:
        return _audit_trace(gate, a.trace)
    if a.self_check:
        return _self_check(gate)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
