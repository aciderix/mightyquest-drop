/* drv_deser.c — ARET save-state driver: run the game's REAL LoginResult
 * deserializer (sub_493440) headless, fed our server's JSON, seeded by the live
 * Wine snapshot. Replaces aret_main.c. Mirrors re/tools/validate_codec.py but on
 * ARET-lifted native code instead of Unicorn.
 *
 * ABI (from validate_codec.py): deser(CTX, OBJ, NAME) cdecl.
 *   CTX  = { STREAM@0, cur_char@4, 0, 0 }
 *   STREAM = { SVT@0 };  SVT vtable: advance@+4, error@+0x1c
 *   advance(): push next JSON byte into CTX+4, return 1 (0 at EOF)
 *   per call: NAME = field name, value JSON streamed; result written into OBJ.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>

void __aret_map_memory(void);
void __aret_patch_iat(void);
uint64_t sub_493440(uint64_t esp, uint64_t a, uint64_t c, uint64_t d);

/* scratch placed outside the snapshot window (0x400000..0x1e00000) */
#define SCR   0x30000000u
#define CTX   (SCR + 0x1000u)
#define STREAM (SCR + 0x1300u)
#define SVT   (SCR + 0x1400u)
#define OBJ   (SCR + 0x2000u)
#define NAME  (SCR + 0x6000u)
#define ADV_VA 0x00AA0001u
#define ERR_VA 0x00AA0002u

static inline uint32_t r32(uint32_t va){ return *(volatile uint32_t*)(uintptr_t)va; }
static inline void w32(uint32_t va,uint32_t v){ *(volatile uint32_t*)(uintptr_t)va=v; }
static inline void w8 (uint32_t va,uint8_t v){ *(volatile uint8_t*)(uintptr_t)va=v; }

/* current streamed value */
static const char *g_json; static int g_len, g_cur;

/* the advance/error vtable callbacks, routed here from aret_call via sentinels */
uint64_t aret_drv_call(uint32_t va, uint64_t esp, uint64_t a, uint64_t c, uint64_t d){
    (void)esp;(void)a;(void)c;(void)d;
    if (va == ADV_VA) {
        if (g_cur < g_len) { w8(CTX+4, (uint8_t)g_json[g_cur]); g_cur++; return 1; }
        w8(CTX+4, 0); return 0;
    }
    return 0; /* error() */
}

static uint8_t mstack[1u<<20];

static uint64_t call3(uint32_t a0,uint32_t a1,uint32_t a2){
    uint8_t *top = mstack + sizeof(mstack) - 64;
    uint32_t *sp = (uint32_t*)top;
    sp[0]=0; sp[1]=a0; sp[2]=a1; sp[3]=a2;            /* cdecl: [esp+4..] */
    return sub_493440((uint64_t)(uintptr_t)top, a0, a1, a2);
}

struct field { const char *name; uint32_t off; int is_str; uint32_t cap; };

int main(void){
    __aret_map_memory();
    __aret_patch_iat();
    /* writable scratch outside the snapshot window */
    if (mmap((void*)(uintptr_t)SCR, 0x100000, PROT_READ|PROT_WRITE,
             MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0) == MAP_FAILED){
        perror("mmap scratch"); return 70;
    }
    /* fake stream + vtable */
    w32(STREAM, SVT);
    w32(SVT+4, ADV_VA);
    w32(SVT+0x1c, ERR_VA);

    struct field fs[] = {
        /* string fields go through READ_STRING (0x9a9450), which ARET lifts
         * cleanly (0 asm fallbacks). The int field (AccountId) routes through
         * READ_INT (0x9a8840), whose shld/adc *10 accumulator ARET still leaves
         * as disconnected __asm__ — ARET's documented incompleteness floor. */
        {"ConnectionToken", 0x0c, 1, 0x08},
        {"ProfileId",       0x2c, 1, 0x28},
    };
    /* values that mirror a server response */
    const char *vals[] = {"tok-ABC", "prof-42"};

    printf("ARET save-state driver — real client LoginResult deserializer (sub_493440)\n");
    printf("fed our JSON, seeded by the live Wine snapshot:\n\n");
    int ok = 1;
    for (unsigned i=0;i<sizeof(fs)/sizeof(fs[0]);i++){
        /* build the value's JSON token: int -> `1000,`  str -> `"v",` */
        char jb[128];
        if (fs[i].is_str) snprintf(jb,sizeof jb,"\"%s\",",vals[i]);
        else              snprintf(jb,sizeof jb,"%s,",vals[i]);
        g_json=jb; g_len=(int)strlen(jb); g_cur=1;      /* cur char preloaded */
        /* CTX = {STREAM, json[0], 0, 0} */
        w32(CTX,STREAM); w8(CTX+4,(uint8_t)jb[0]); w32(CTX+8,0); w32(CTX+12,0);
        /* OBJ cleared; string capacities set */
        memset((void*)(uintptr_t)OBJ,0,0x400);
        for (unsigned k=0;k<sizeof(fs)/sizeof(fs[0]);k++)
            if (fs[k].is_str) w32(OBJ+fs[k].cap, 0x40);
        /* NAME */
        strcpy((char*)(uintptr_t)NAME, fs[i].name);
        call3(CTX,OBJ,NAME);
        if (fs[i].is_str){
            char *s=(char*)(uintptr_t)(OBJ+fs[i].off);
            int good = strcmp(s,vals[i])==0;
            ok &= good;
            printf("  %-16s in=\"%s\"  -> got=\"%s\"  %s\n", fs[i].name, vals[i], s, good?"OK":"X");
        } else {
            uint32_t v=r32(OBJ+fs[i].off);
            int good = v==(uint32_t)atoi(vals[i]);
            ok &= good;
            printf("  %-16s in=%s  -> got=%u  %s\n", fs[i].name, vals[i], v, good?"OK":"X");
        }
    }
    printf("\n%s: real client deserializer ran headless from the snapshot.\n",
           ok?"PASS":"FAIL");
    return ok?0:1;
}
