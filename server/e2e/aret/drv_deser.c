/* drv_deser.c — ARET save-state driver: run the game's REAL deserializers
 * headless, fed our server's JSON. Covers every contract whose deserializer
 * address + field layout are known (LoginResult, AccountLite — same set the
 * Unicorn validator re/tools/validate_codec.py proves), but here on ARET-lifted
 * native code. Calls each deserializer by VA through aret_call, so any recovered
 * function works without a per-symbol declaration.
 *
 * ABI (from validate_codec.py): deser(CTX, OBJ, NAME) cdecl.
 *   CTX={STREAM@0,cur@4,0,0}; STREAM={SVT@0}; SVT: advance@+4, error@+0x1c
 *   advance(): push next JSON byte into CTX+4, return 1 (0 at EOF)
 *   per call: NAME=field name, value JSON streamed; result written into OBJ.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>

void __aret_map_memory(void);
void __aret_patch_iat(void);
extern uint64_t aret_call(uint32_t va, uint64_t esp, uint64_t a, uint64_t c, uint64_t d);

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

static const char *g_json; static int g_len, g_cur;

uint64_t aret_drv_call(uint32_t va, uint64_t esp, uint64_t a, uint64_t c, uint64_t d){
    (void)esp;(void)a;(void)c;(void)d;
    if (va == ADV_VA) {
        if (g_cur < g_len) { w8(CTX+4, (uint8_t)g_json[g_cur]); g_cur++; return 1; }
        w8(CTX+4, 0); return 0;
    }
    return 0; /* error() */
}

static uint8_t mstack[1u<<20];

static void call_deser(uint32_t va, uint32_t a0, uint32_t a1, uint32_t a2){
    uint8_t *top = mstack + sizeof(mstack) - 64;
    uint32_t *sp = (uint32_t*)top;
    sp[0]=0; sp[1]=a0; sp[2]=a1; sp[3]=a2;          /* [esp+4]=CTX,[esp+8]=OBJ,[esp+12]=NAME */
    aret_call(va, (uint64_t)(uintptr_t)top, a0, a1, a2);
}

struct field { const char *name; uint32_t off; int is_str; uint32_t cap; const char *val; };
struct contract { const char *name; uint32_t deser; struct field f[8]; int n; };

static struct contract CONTRACTS[] = {
    { "LoginResult", 0x00493440, {
        {"AccountId",       0x04, 0, 0,     "1000"},
        {"ConnectionToken", 0x0c, 1, 0x08,  "tok-ABC"},
        {"ProfileId",       0x2c, 1, 0x28,  "prof-42"},
    }, 3 },
    { "AccountLite", 0x00615db0, {
        {"AccountId",        0x04,  0, 0,     "2000"},
        {"ActivationStatus", 0x08,  0, 0,     "7"},
        {"DisplayName",      0x10,  1, 0x0c,  "Sir-Test"},
        {"Email",            0x114, 1, 0x110, "a@b.co"},
        {"Password",         0x218, 1, 0x214, "hunter2"},
    }, 5 },
};

int main(void){
    __aret_map_memory();
    __aret_patch_iat();
    if (mmap((void*)(uintptr_t)SCR, 0x100000, PROT_READ|PROT_WRITE,
             MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0) == MAP_FAILED){
        perror("mmap scratch"); return 70;
    }
    w32(STREAM, SVT); w32(SVT+4, ADV_VA); w32(SVT+0x1c, ERR_VA);

    printf("ARET save-state driver — real client deserializers run headless on our JSON\n");
    int total=0, pass=0;
    for (unsigned ci=0; ci<sizeof(CONTRACTS)/sizeof(CONTRACTS[0]); ci++){
        struct contract *C = &CONTRACTS[ci];
        printf("\n=== %s (sub_%x) ===\n", C->name, C->deser);
        for (int i=0;i<C->n;i++){
            struct field *F=&C->f[i];
            char jb[160];
            if (F->is_str) snprintf(jb,sizeof jb,"\"%s\",",F->val);
            else           snprintf(jb,sizeof jb,"%s,",F->val);
            g_json=jb; g_len=(int)strlen(jb); g_cur=1;
            w32(CTX,STREAM); w8(CTX+4,(uint8_t)jb[0]); w32(CTX+8,0); w32(CTX+12,0);
            memset((void*)(uintptr_t)OBJ,0,0x400);
            for (int k=0;k<C->n;k++) if (C->f[k].is_str) w32(OBJ+C->f[k].cap, 0x40);
            strcpy((char*)(uintptr_t)NAME, F->name);
            call_deser(C->deser, CTX, OBJ, NAME);
            total++;
            if (F->is_str){
                char *s=(char*)(uintptr_t)(OBJ+F->off);
                int good=strcmp(s,F->val)==0; pass+=good;
                printf("  %-16s in=\"%s\"  -> got=\"%s\"  %s\n", F->name, F->val, s, good?"OK":"X");
            } else {
                uint32_t v=r32(OBJ+F->off);
                int good=v==(uint32_t)atoi(F->val); pass+=good;
                printf("  %-16s in=%s  -> got=%u  %s\n", F->name, F->val, v, good?"OK":"X");
            }
        }
    }
    printf("\n%s: %d/%d fields deserialized correctly through the real client code (headless).\n",
           pass==total?"PASS":"FAIL", pass, total);
    return pass==total?0:1;
}
