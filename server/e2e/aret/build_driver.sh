#!/bin/bash
# Relink the ARET-transpiled deserializer project with our custom driver.
set -e
D=${OUT:-/home/user/e2e/aret_deser}
CC="gcc"
CFLAGS="-m32 -w -fno-strict-aliasing -fno-builtin -fno-pie -O0 -c -I $D"

cd "$D"

# 1. route the advance/error vtable sentinels in aret_call -> our native cb
python3 - <<'PY'
p="aret_dispatch.c"; s=open(p).read()
if "aret_drv_call" not in s:
    s=s.replace("uint64_t aret_call(uint32_t va, uint64_t esp, uint64_t a, uint64_t c, uint64_t d) {",
      "extern uint64_t aret_drv_call(uint32_t,uint64_t,uint64_t,uint64_t,uint64_t);\n"
      "uint64_t aret_call(uint32_t va, uint64_t esp, uint64_t a, uint64_t c, uint64_t d) {\n"
      "    if (va==0xAA0001u||va==0xAA0002u) return aret_drv_call(va,esp,a,c,d);",1)
    open(p,"w").write(s); print("patched aret_dispatch.c")
else: print("already patched")
PY

# 2. (re)compile the patched dispatch + our driver
$CC $CFLAGS aret_dispatch.c -o aret_dispatch.c.o
$CC $CFLAGS /home/user/e2e/drv_deser.c -o drv_deser.c.o

# 3. relink everything except aret_main.o, plus our driver
OBJS=$(ls *.c.o | grep -vE '^(aret_main|drv_deser).c.o$'); [ -f aret_layout.S.o ] && OBJS="$OBJS aret_layout.S.o"
$CC -m32 -no-pie $OBJS drv_deser.c.o -lm -o run_deser
echo "[built] $D/run_deser"
echo "=== RUN ==="
./run_deser
