# Wire format — login / boot vertical slice

First reversed slice of the client↔server protocol. Recovered by decompiling the
contract copy-constructors (field layout) and the serializer methods (JSON field
names), then **verified by emulating the serializer under Unicorn**.

- Raw decompiler output: `re/catalog/decompiled/login_constructors.c`,
  `re/catalog/decompiled/login_serializers.c`
- Verification harness: `re/tools/demo_loginresult.py`

## Method
1. The tracked allocator `FUN_009788c0(size, "Anonymous New", "<src>.cpp", line)`
   reveals each DTO's **size** and source file; its copy-constructor reveals the
   **field offsets / types** (e.g. inline `String_Z` buffers).
2. Each `*Serializer` registers a singleton whose vtable holds the
   **serialize / deserialize** methods. Those methods contain the literal **JSON
   key names** (deserialize does `strcmp(field, "Key")` chains; serialize does
   `writeKey("Key"); writeValue(...)`).
3. The JSON writer primitives were identified from the serialize methods:
   - `FUN_009ab550(name)` — **writeKey**
   - `FUN_009aad80(&int)` — **writeInt**
   - `FUN_009ab060(&String_Z)` — **writeString**
   And the unknown-field handler `FUN_009a9ce0("<TypeName>", field, 0)`.

## Recovered schemas

### LoginResult  (`FUN_00468770` ctor, 72 B; serialize `FUN_0049de80`)
```json
{ "AccountId": <int>, "ConnectionToken": "<string>", "ProfileId": "<string>" }
```
The server's login response: an account id plus the **ConnectionToken** the
client then uses to authenticate to the game server, plus a ProfileId.

### GameServerConnectionConfig  (`FUN_0041af40` ctor, 788 B; deserialize `FUN_00444fb0`)
```json
{ "AccountName": "<string>", "AccountPassword": "<string>",
  "GameServerUrl": "<string>", "HttpCompression": <bool> }
```
The connection descriptor: **game server URL + credentials**. Directly defines
what a community server must accept / what the client expects to be pointed at.

### AccountLite  (`FUN_005ef2f0` ctor, 800 B; serialize `FUN_00615db0`)
```json
{ "AccountId": <int>, "ActivationStatus": <int>, "DisplayName": "<string>",
  "Email": "<string>", "Password": "<string>", "Privileges": <int> }
```

### SessionTracking / ProxyLoadLoginPage
Constructors recovered (sizes 32 B / 264 B); serializer key extraction pending
(see the decompiled serializers file).

## Verification (Unicorn)
`demo_loginresult.py` builds a `LoginResult` in emulated memory
(AccountId=12345, ConnectionToken="TESTTOKEN", ProfileId="PROFILE42"), runs the
real `serialize` method, and intercepts the writer primitives. Output:
```
"AccountId": 12345
"ConnectionToken": 'TESTTOKEN'
"ProfileId": 'PROFILE42'
[+] matches static schema
```
i.e. the emulated method emits exactly the field order/types recovered
statically — the schema is confirmed, not guessed.

## Next
- Extract the remaining serializers (SessionTracking, ProxyLoadLoginPage, the
  full AccountInformationBase set) the same way.
- Find the controller dispatch that issues the login HTTP request (URL + verb)
  near `BootManager` / `EnvironmentManager.ServerInfo` usage to complete the
  end-to-end login transaction for the community server stub.
