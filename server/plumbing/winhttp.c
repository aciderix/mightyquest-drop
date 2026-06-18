/*
 * WinHTTP Proxy DLL for MQEL
 * ===========================
 * Sits in GameData/Bin/ next to MightyQuest.exe. Windows DLL search order
 * loads this before system32\winhttp.dll.
 *
 * All calls are forwarded to the real winhttp.dll, but after every
 * WinHttpSendRequest we inject SECURITY_FLAG_IGNORE_ALL_CERT_ERRORS
 * so the game accepts our local proxy's self-signed certificate.
 *
 * Compile (MinGW i686):
 *   i686-w64-mingw32-gcc -shared -o winhttp.dll winhttp.c winhttp.def \
 *       -lkernel32 -O2 -s
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <winhttp.h>
#include <stdio.h>

/* ── Real DLL handle & function pointers ─────────────────────────── */

static HMODULE hReal = NULL;

/* Typedefs for every exported function */
typedef HINTERNET (WINAPI *pWinHttpOpen_t)(LPCWSTR, DWORD, LPCWSTR, LPCWSTR, DWORD);
typedef HINTERNET (WINAPI *pWinHttpConnect_t)(HINTERNET, LPCWSTR, INTERNET_PORT, DWORD);
typedef HINTERNET (WINAPI *pWinHttpOpenRequest_t)(HINTERNET, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR*, DWORD);
typedef BOOL      (WINAPI *pWinHttpSendRequest_t)(HINTERNET, LPCWSTR, DWORD, LPVOID, DWORD, DWORD, DWORD_PTR);
typedef BOOL      (WINAPI *pWinHttpReceiveResponse_t)(HINTERNET, LPVOID);
typedef BOOL      (WINAPI *pWinHttpQueryDataAvailable_t)(HINTERNET, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpReadData_t)(HINTERNET, LPVOID, DWORD, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpWriteData_t)(HINTERNET, LPCVOID, DWORD, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpCloseHandle_t)(HINTERNET);
typedef BOOL      (WINAPI *pWinHttpSetOption_t)(HINTERNET, DWORD, LPVOID, DWORD);
typedef BOOL      (WINAPI *pWinHttpQueryOption_t)(HINTERNET, DWORD, LPVOID, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpQueryHeaders_t)(HINTERNET, DWORD, LPCWSTR, LPVOID, LPDWORD, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpAddRequestHeaders_t)(HINTERNET, LPCWSTR, DWORD, DWORD);
typedef BOOL      (WINAPI *pWinHttpSetCredentials_t)(HINTERNET, DWORD, DWORD, LPCWSTR, LPCWSTR, LPVOID);
typedef BOOL      (WINAPI *pWinHttpQueryAuthSchemes_t)(HINTERNET, LPDWORD, LPDWORD, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpSetTimeouts_t)(HINTERNET, int, int, int, int);
typedef WINHTTP_STATUS_CALLBACK (WINAPI *pWinHttpSetStatusCallback_t)(HINTERNET, WINHTTP_STATUS_CALLBACK, DWORD, DWORD_PTR);
typedef BOOL      (WINAPI *pWinHttpCrackUrl_t)(LPCWSTR, DWORD, DWORD, LPURL_COMPONENTS);
typedef BOOL      (WINAPI *pWinHttpCreateUrl_t)(LPURL_COMPONENTS, DWORD, LPWSTR, LPDWORD);
typedef BOOL      (WINAPI *pWinHttpCheckPlatform_t)(void);
typedef BOOL      (WINAPI *pWinHttpDetectAutoProxyConfigUrl_t)(DWORD, LPWSTR*);
typedef BOOL      (WINAPI *pWinHttpGetDefaultProxyConfiguration_t)(WINHTTP_PROXY_INFO*);
typedef BOOL      (WINAPI *pWinHttpSetDefaultProxyConfiguration_t)(WINHTTP_PROXY_INFO*);
typedef BOOL      (WINAPI *pWinHttpGetIEProxyConfigForCurrentUser_t)(WINHTTP_CURRENT_USER_IE_PROXY_CONFIG*);
typedef BOOL      (WINAPI *pWinHttpGetProxyForUrl_t)(HINTERNET, LPCWSTR, WINHTTP_AUTOPROXY_OPTIONS*, WINHTTP_PROXY_INFO*);
typedef BOOL      (WINAPI *pWinHttpTimeFromSystemTime_t)(const SYSTEMTIME*, LPWSTR);
typedef BOOL      (WINAPI *pWinHttpTimeToSystemTime_t)(LPCWSTR, SYSTEMTIME*);
typedef HRESULT   (WINAPI *pDllCanUnloadNow_t)(void);
typedef HRESULT   (WINAPI *pDllGetClassObject_t)(REFCLSID, REFIID, LPVOID*);
typedef HRESULT   (WINAPI *pDllRegisterServer_t)(void);
typedef HRESULT   (WINAPI *pDllUnregisterServer_t)(void);

/* Actual function pointers (resolved at load time) */
static pWinHttpOpen_t                          real_WinHttpOpen;
static pWinHttpConnect_t                       real_WinHttpConnect;
static pWinHttpOpenRequest_t                   real_WinHttpOpenRequest;
static pWinHttpSendRequest_t                   real_WinHttpSendRequest;
static pWinHttpReceiveResponse_t               real_WinHttpReceiveResponse;
static pWinHttpQueryDataAvailable_t            real_WinHttpQueryDataAvailable;
static pWinHttpReadData_t                      real_WinHttpReadData;
static pWinHttpWriteData_t                     real_WinHttpWriteData;
static pWinHttpCloseHandle_t                   real_WinHttpCloseHandle;
static pWinHttpSetOption_t                     real_WinHttpSetOption;
static pWinHttpQueryOption_t                   real_WinHttpQueryOption;
static pWinHttpQueryHeaders_t                  real_WinHttpQueryHeaders;
static pWinHttpAddRequestHeaders_t             real_WinHttpAddRequestHeaders;
static pWinHttpSetCredentials_t                real_WinHttpSetCredentials;
static pWinHttpQueryAuthSchemes_t              real_WinHttpQueryAuthSchemes;
static pWinHttpSetTimeouts_t                   real_WinHttpSetTimeouts;
static pWinHttpSetStatusCallback_t             real_WinHttpSetStatusCallback;
static pWinHttpCrackUrl_t                      real_WinHttpCrackUrl;
static pWinHttpCreateUrl_t                     real_WinHttpCreateUrl;
static pWinHttpCheckPlatform_t                 real_WinHttpCheckPlatform;
static pWinHttpDetectAutoProxyConfigUrl_t      real_WinHttpDetectAutoProxyConfigUrl;
static pWinHttpGetDefaultProxyConfiguration_t  real_WinHttpGetDefaultProxyConfiguration;
static pWinHttpSetDefaultProxyConfiguration_t  real_WinHttpSetDefaultProxyConfiguration;
static pWinHttpGetIEProxyConfigForCurrentUser_t real_WinHttpGetIEProxyConfigForCurrentUser;
static pWinHttpGetProxyForUrl_t                real_WinHttpGetProxyForUrl;
static pWinHttpTimeFromSystemTime_t            real_WinHttpTimeFromSystemTime;
static pWinHttpTimeToSystemTime_t              real_WinHttpTimeToSystemTime;
static pDllCanUnloadNow_t                      real_DllCanUnloadNow;
static pDllGetClassObject_t                    real_DllGetClassObject;
static pDllRegisterServer_t                    real_DllRegisterServer;
static pDllUnregisterServer_t                  real_DllUnregisterServer;

/* ── Debug logging ───────────────────────────────────────────────── */

static FILE *logfile = NULL;

static void dbg(const char *fmt, ...) {
    if (!logfile) return;
    va_list ap;
    va_start(ap, fmt);
    vfprintf(logfile, fmt, ap);
    va_end(ap);
    fflush(logfile);
}

/* ── Initialization ──────────────────────────────────────────────── */

static BOOL load_real_dll(void) {
    WCHAR sysdir[MAX_PATH];
    WCHAR path[MAX_PATH];

    GetSystemDirectoryW(sysdir, MAX_PATH);
    wsprintfW(path, L"%s\\winhttp.dll", sysdir);

    hReal = LoadLibraryW(path);
    if (!hReal) {
        dbg("[MQEL-WinHTTP] FATAL: Cannot load real winhttp.dll from %ls\n", path);
        return FALSE;
    }

    dbg("[MQEL-WinHTTP] Loaded real winhttp.dll from %ls\n", path);

    /* Resolve all exports */
    #define RESOLVE(name) \
        real_##name = (p##name##_t)GetProcAddress(hReal, #name); \
        if (!real_##name) dbg("[MQEL-WinHTTP] WARN: " #name " not found in real DLL\n");

    RESOLVE(WinHttpOpen);
    RESOLVE(WinHttpConnect);
    RESOLVE(WinHttpOpenRequest);
    RESOLVE(WinHttpSendRequest);
    RESOLVE(WinHttpReceiveResponse);
    RESOLVE(WinHttpQueryDataAvailable);
    RESOLVE(WinHttpReadData);
    RESOLVE(WinHttpWriteData);
    RESOLVE(WinHttpCloseHandle);
    RESOLVE(WinHttpSetOption);
    RESOLVE(WinHttpQueryOption);
    RESOLVE(WinHttpQueryHeaders);
    RESOLVE(WinHttpAddRequestHeaders);
    RESOLVE(WinHttpSetCredentials);
    RESOLVE(WinHttpQueryAuthSchemes);
    RESOLVE(WinHttpSetTimeouts);
    RESOLVE(WinHttpSetStatusCallback);
    RESOLVE(WinHttpCrackUrl);
    RESOLVE(WinHttpCreateUrl);
    RESOLVE(WinHttpCheckPlatform);
    RESOLVE(WinHttpDetectAutoProxyConfigUrl);
    RESOLVE(WinHttpGetDefaultProxyConfiguration);
    RESOLVE(WinHttpSetDefaultProxyConfiguration);
    RESOLVE(WinHttpGetIEProxyConfigForCurrentUser);
    RESOLVE(WinHttpGetProxyForUrl);
    RESOLVE(WinHttpTimeFromSystemTime);
    RESOLVE(WinHttpTimeToSystemTime);
    RESOLVE(DllCanUnloadNow);
    RESOLVE(DllGetClassObject);
    RESOLVE(DllRegisterServer);
    RESOLVE(DllUnregisterServer);

    #undef RESOLVE
    return TRUE;
}

/* ── SSL bypass helper ───────────────────────────────────────────── */

static void disable_cert_checks(HINTERNET hRequest) {
    /* Set all ignore flags on this request handle */
    DWORD flags = SECURITY_FLAG_IGNORE_UNKNOWN_CA
                | SECURITY_FLAG_IGNORE_CERT_DATE_INVALID
                | SECURITY_FLAG_IGNORE_CERT_CN_INVALID
                | SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE;

    if (real_WinHttpSetOption) {
        BOOL ok = real_WinHttpSetOption(
            hRequest,
            WINHTTP_OPTION_SECURITY_FLAGS,
            &flags,
            sizeof(flags)
        );
        dbg("[MQEL-WinHTTP] Set SECURITY_FLAGS on %p: %s\n",
            hRequest, ok ? "OK" : "FAILED");
    }
}

/* ── Exported wrappers ───────────────────────────────────────────── */

HINTERNET WINAPI WinHttpOpen(
    LPCWSTR pszAgentW, DWORD dwAccessType,
    LPCWSTR pszProxyW, LPCWSTR pszProxyBypassW, DWORD dwFlags
) {
    HINTERNET h = real_WinHttpOpen(pszAgentW, dwAccessType, pszProxyW, pszProxyBypassW, dwFlags);
    dbg("[MQEL-WinHTTP] WinHttpOpen() -> %p\n", h);
    return h;
}

HINTERNET WINAPI WinHttpConnect(
    HINTERNET hSession, LPCWSTR pswzServerName,
    INTERNET_PORT nServerPort, DWORD dwReserved
) {
    HINTERNET h = real_WinHttpConnect(hSession, pswzServerName, nServerPort, dwReserved);
    dbg("[MQEL-WinHTTP] WinHttpConnect(%ls:%d) -> %p\n",
        pswzServerName, nServerPort, h);
    return h;
}

HINTERNET WINAPI WinHttpOpenRequest(
    HINTERNET hConnect, LPCWSTR pwszVerb, LPCWSTR pwszObjectName,
    LPCWSTR pwszVersion, LPCWSTR pwszReferrer,
    LPCWSTR *ppwszAcceptTypes, DWORD dwFlags
) {
    HINTERNET h = real_WinHttpOpenRequest(
        hConnect, pwszVerb, pwszObjectName,
        pwszVersion, pwszReferrer, ppwszAcceptTypes, dwFlags
    );
    dbg("[MQEL-WinHTTP] WinHttpOpenRequest(%ls %ls, flags=0x%x) -> %p\n",
        pwszVerb ? pwszVerb : L"GET",
        pwszObjectName ? pwszObjectName : L"/",
        dwFlags, h);

    /* Disable SSL certificate verification on HTTPS requests */
    if (h && (dwFlags & WINHTTP_FLAG_SECURE)) {
        disable_cert_checks(h);
    }

    return h;
}

BOOL WINAPI WinHttpSendRequest(
    HINTERNET hRequest, LPCWSTR lpszHeaders, DWORD dwHeadersLength,
    LPVOID lpOptional, DWORD dwOptionalLength,
    DWORD dwTotalLength, DWORD_PTR dwContext
) {
    /* Re-apply cert bypass right before sending (belt & suspenders) */
    disable_cert_checks(hRequest);

    BOOL ok = real_WinHttpSendRequest(
        hRequest, lpszHeaders, dwHeadersLength,
        lpOptional, dwOptionalLength, dwTotalLength, dwContext
    );
    dbg("[MQEL-WinHTTP] WinHttpSendRequest(%p) -> %s\n",
        hRequest, ok ? "OK" : "FAILED");
    return ok;
}

BOOL WINAPI WinHttpReceiveResponse(HINTERNET hRequest, LPVOID lpReserved) {
    return real_WinHttpReceiveResponse(hRequest, lpReserved);
}

BOOL WINAPI WinHttpQueryDataAvailable(HINTERNET hRequest, LPDWORD lpdwNumberOfBytesAvailable) {
    return real_WinHttpQueryDataAvailable(hRequest, lpdwNumberOfBytesAvailable);
}

BOOL WINAPI WinHttpReadData(HINTERNET hRequest, LPVOID lpBuffer, DWORD dwNumberOfBytesToRead, LPDWORD lpdwNumberOfBytesRead) {
    return real_WinHttpReadData(hRequest, lpBuffer, dwNumberOfBytesToRead, lpdwNumberOfBytesRead);
}

BOOL WINAPI WinHttpWriteData(HINTERNET hRequest, LPCVOID lpBuffer, DWORD dwNumberOfBytesToWrite, LPDWORD lpdwNumberOfBytesWritten) {
    return real_WinHttpWriteData(hRequest, lpBuffer, dwNumberOfBytesToWrite, lpdwNumberOfBytesWritten);
}

BOOL WINAPI WinHttpCloseHandle(HINTERNET hInternet) {
    return real_WinHttpCloseHandle(hInternet);
}

BOOL WINAPI WinHttpSetOption(HINTERNET hInternet, DWORD dwOption, LPVOID lpBuffer, DWORD dwBufferLength) {
    return real_WinHttpSetOption(hInternet, dwOption, lpBuffer, dwBufferLength);
}

BOOL WINAPI WinHttpQueryOption(HINTERNET hInternet, DWORD dwOption, LPVOID lpBuffer, LPDWORD lpdwBufferLength) {
    return real_WinHttpQueryOption(hInternet, dwOption, lpBuffer, lpdwBufferLength);
}

BOOL WINAPI WinHttpQueryHeaders(HINTERNET hRequest, DWORD dwInfoLevel, LPCWSTR pwszName, LPVOID lpBuffer, LPDWORD lpdwBufferLength, LPDWORD lpdwIndex) {
    return real_WinHttpQueryHeaders(hRequest, dwInfoLevel, pwszName, lpBuffer, lpdwBufferLength, lpdwIndex);
}

BOOL WINAPI WinHttpAddRequestHeaders(HINTERNET hRequest, LPCWSTR lpszHeaders, DWORD dwHeadersLength, DWORD dwModifiers) {
    return real_WinHttpAddRequestHeaders(hRequest, lpszHeaders, dwHeadersLength, dwModifiers);
}

BOOL WINAPI WinHttpSetCredentials(HINTERNET hRequest, DWORD AuthTargets, DWORD AuthScheme, LPCWSTR pwszUserName, LPCWSTR pwszPassword, LPVOID pAuthParams) {
    return real_WinHttpSetCredentials(hRequest, AuthTargets, AuthScheme, pwszUserName, pwszPassword, pAuthParams);
}

BOOL WINAPI WinHttpQueryAuthSchemes(HINTERNET hRequest, LPDWORD lpdwSupportedSchemes, LPDWORD lpdwFirstScheme, LPDWORD pdwAuthTarget) {
    return real_WinHttpQueryAuthSchemes(hRequest, lpdwSupportedSchemes, lpdwFirstScheme, pdwAuthTarget);
}

BOOL WINAPI WinHttpSetTimeouts(HINTERNET hInternet, int nResolveTimeout, int nConnectTimeout, int nSendTimeout, int nReceiveTimeout) {
    return real_WinHttpSetTimeouts(hInternet, nResolveTimeout, nConnectTimeout, nSendTimeout, nReceiveTimeout);
}

WINHTTP_STATUS_CALLBACK WINAPI WinHttpSetStatusCallback(HINTERNET hInternet, WINHTTP_STATUS_CALLBACK lpfnInternetCallback, DWORD dwNotificationFlags, DWORD_PTR dwReserved) {
    return real_WinHttpSetStatusCallback(hInternet, lpfnInternetCallback, dwNotificationFlags, dwReserved);
}

BOOL WINAPI WinHttpCrackUrl(LPCWSTR pwszUrl, DWORD dwUrlLength, DWORD dwFlags, LPURL_COMPONENTS lpUrlComponents) {
    return real_WinHttpCrackUrl(pwszUrl, dwUrlLength, dwFlags, lpUrlComponents);
}

BOOL WINAPI WinHttpCreateUrl(LPURL_COMPONENTS lpUrlComponents, DWORD dwFlags, LPWSTR pwszUrl, LPDWORD pdwUrlLength) {
    return real_WinHttpCreateUrl(lpUrlComponents, dwFlags, pwszUrl, pdwUrlLength);
}

BOOL WINAPI WinHttpCheckPlatform(void) {
    return real_WinHttpCheckPlatform ? real_WinHttpCheckPlatform() : TRUE;
}

BOOL WINAPI WinHttpDetectAutoProxyConfigUrl(DWORD dwAutoDetectFlags, LPWSTR *ppwstrAutoConfigUrl) {
    return real_WinHttpDetectAutoProxyConfigUrl(dwAutoDetectFlags, ppwstrAutoConfigUrl);
}

BOOL WINAPI WinHttpGetDefaultProxyConfiguration(WINHTTP_PROXY_INFO *pProxyInfo) {
    return real_WinHttpGetDefaultProxyConfiguration(pProxyInfo);
}

BOOL WINAPI WinHttpSetDefaultProxyConfiguration(WINHTTP_PROXY_INFO *pProxyInfo) {
    return real_WinHttpSetDefaultProxyConfiguration(pProxyInfo);
}

BOOL WINAPI WinHttpGetIEProxyConfigForCurrentUser(WINHTTP_CURRENT_USER_IE_PROXY_CONFIG *pProxyConfig) {
    return real_WinHttpGetIEProxyConfigForCurrentUser(pProxyConfig);
}

BOOL WINAPI WinHttpGetProxyForUrl(HINTERNET hSession, LPCWSTR lpcwszUrl, WINHTTP_AUTOPROXY_OPTIONS *pAutoProxyOptions, WINHTTP_PROXY_INFO *pProxyInfo) {
    return real_WinHttpGetProxyForUrl(hSession, lpcwszUrl, pAutoProxyOptions, pProxyInfo);
}

BOOL WINAPI WinHttpTimeFromSystemTime(const SYSTEMTIME *pst, LPWSTR pwszTime) {
    return real_WinHttpTimeFromSystemTime(pst, pwszTime);
}

BOOL WINAPI WinHttpTimeToSystemTime(LPCWSTR pwszTime, SYSTEMTIME *pst) {
    return real_WinHttpTimeToSystemTime(pwszTime, pst);
}

/* COM exports — forward directly */
HRESULT WINAPI DllCanUnloadNow(void) {
    return real_DllCanUnloadNow ? real_DllCanUnloadNow() : S_FALSE;
}
HRESULT WINAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID *ppv) {
    return real_DllGetClassObject ? real_DllGetClassObject(rclsid, riid, ppv) : E_FAIL;
}
HRESULT WINAPI DllRegisterServer(void) {
    return real_DllRegisterServer ? real_DllRegisterServer() : E_FAIL;
}
HRESULT WINAPI DllUnregisterServer(void) {
    return real_DllUnregisterServer ? real_DllUnregisterServer() : E_FAIL;
}

/* ── DLL Entry Point ─────────────────────────────────────────────── */

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    (void)hinstDLL; (void)lpvReserved;

    switch (fdwReason) {
    case DLL_PROCESS_ATTACH:
        /* Open debug log next to the DLL */
        logfile = fopen("winhttp_proxy.log", "w");
        dbg("[MQEL-WinHTTP] === MQEL WinHTTP Proxy DLL loaded ===\n");

        if (!load_real_dll()) {
            if (logfile) fclose(logfile);
            return FALSE;
        }

        DisableThreadLibraryCalls(hinstDLL);
        break;

    case DLL_PROCESS_DETACH:
        dbg("[MQEL-WinHTTP] Unloading\n");
        if (hReal) FreeLibrary(hReal);
        if (logfile) fclose(logfile);
        break;
    }

    return TRUE;
}
