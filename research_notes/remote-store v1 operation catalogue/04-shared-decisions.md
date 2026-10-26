# Track 04: Shared decisions and capability-gate signalling (fsspec, object_store/obstore, OpenDAL, gocloud blob)

Question: what does each abstraction library decide **once for every operation** rather than per operation,
and how does it tell a caller that a backend lacks a capability?

Access date for every source: **2026-10-26**. remote-store's own code and docs were not consulted.

Labels: **[documented]** means a doc comment, docstring or doc page states it. **[observed]** means I read it in
source code at the pinned tag, not in prose. **[inference]** means my reading, not stated anywhere.

## Sources and versions

Latest versions were taken from the registries (crates.io API, PyPI JSON, proxy.golang.org `@latest`) on 2026-10-26.
Raw source was fetched from `raw.githubusercontent.com` at the release tag. The doc comments in that source are the
same text that docs.rs and pkg.go.dev render.

| ID | Library | Version / tag | Files read (full text) |
|---|---|---|---|
| OS | Rust `object_store` | 0.14.2, tag `v0.14.2` of `apache/arrow-rs-object-store` | `src/lib.rs` (crate docs, `ObjectStore`, `ObjectStoreExt`, `Error`, `PutMode`, `CopyMode`, `RenameTargetMode`), `src/path/mod.rs`, `src/client/retry.rs`, `src/client/mod.rs` (ClientOptions), `src/aws/precondition.rs`, `src/aws/mod.rs`, `src/http/mod.rs`, `src/local.rs`, `src/memory.rs`, `src/prefix.rs`, `src/limit.rs`, `src/throttle.rs`. Base URL: https://raw.githubusercontent.com/apache/arrow-rs-object-store/v0.14.2/src/ (docs.rs mirror: https://docs.rs/object_store/0.14.2) |
| OBS | `obstore` (Python) | 0.12.0 (PyPI), git tag `py-v0.12.0`, depends on `object_store = 0.14.0` | https://developmentseed.org/obstore/v0.12.0/api/exceptions/ , https://developmentseed.org/obstore/v0.12.0/getting-started/ , https://developmentseed.org/obstore/latest/ (versions.json shows that `latest` = v0.12.0), https://raw.githubusercontent.com/developmentseed/obstore/py-v0.12.0/pyo3-object_store/src/error.rs |
| OD | Apache OpenDAL (Rust) | `opendal` 0.59.5, tag `v0.59.5`. The facade crate re-exports `opendal_core`, and optional layers are separate `opendal-layer-*` crates | `core/src/lib.rs`, `core/Cargo.toml`, `core/README.md`, `core/core/src/{types/error.rs, types/capability.rs, types/operator/{operator.rs,info.rs,builder.rs}, types/write/writer.rs, raw/path.rs, layers/{mod.rs,complete.rs,correctness_check.rs,simulate.rs,capability_override.rs,error_context.rs}, blocking/{mod.rs,operator.rs}}`, `core/layers/{retry,timeout,concurrent-limit,logging,capability-check}/src/lib.rs`. Base URL: https://raw.githubusercontent.com/apache/opendal/v0.59.5/ |
| ODPY | OpenDAL Python | 0.47.12 (PyPI). `bindings/python/Cargo.toml` at the same tag v0.59.5 says 0.47.12 | `bindings/python/python/opendal/{operator.pyi,exceptions.pyi,layers.pyi}`, `bindings/python/src/errors.rs` |
| GC | Go CDK `gocloud.dev/blob` | v0.47.0 (proxy.golang.org @latest, 2026-10-14) | `blob/blob.go`, `blob/driver/driver.go`, `gcerrors/errors.go`, `internal/gcerr/gcerr.go`, `internal/escape/escape.go`, `blob/{fileblob,memblob,s3blob,gcsblob,azureblob}/*.go` at https://raw.githubusercontent.com/google/go-cloud/v0.47.0/ ; how-to page https://gocloud.dev/howto/blob/ |
| FS | fsspec | 2026.9.0 (PyPI), tag `2026.9.0` | `fsspec/{spec.py,asyn.py,exceptions.py,implementations/dirfs.py}`; docs https://filesystem-spec.readthedocs.io/en/latest/features.html , .../async.html , .../api.html (the pages render "fsspec 2026.9.0.post2") |
| S3FS | s3fs (fsspec implementation, as a retry example) | 2026.9.0, tag `2026.9.0` | `s3fs/core.py`, `s3fs/errors.py` at https://raw.githubusercontent.com/fsspec/s3fs/2026.9.0/ |

Unreachable or not used:
- The api.github.com tag listing for apache/opendal was refused for this session. The tag `v0.59.5` was confirmed by raw fetches instead.
- The fsspec changelog page was not fetched.
- I found no OpenDAL "consistency" doc page. Only the source files listed above were searched.

## Matrix: decision x library

| Decision | object_store 0.14.2 (+ obstore 0.12.0) | OpenDAL 0.59.5 (+ Python 0.47.12) | gocloud blob v0.47.0 | fsspec 2026.9.0 |
|---|---|---|---|---|
| **Key / path type & validation** | Dedicated `Path` type with these invariants: `/` delimited, no leading or trailing `/`, no `.`/`..`, no empty segments, no ASCII control characters. No length limit is enforced. The docs note that most stores cap keys at 1024 bytes. [documented, path/mod.rs] | Plain `&str`. Every Operator method runs `normalize_path` first (43 call sites in operator.rs) [observed]. Normalization trims whitespace, trims leading `/`, collapses `//`, and turns an empty path into `/` [documented, raw/path.rs]. `.`/`..` are **not** rejected or resolved [observed: no such rule in `normalize_path`]. | Plain `string`. Each Bucket method rejects keys that are not UTF-8 with `InvalidArgument` (for example "NewWriter key must be a valid UTF-8 string") [observed, blob.go]. "Go CDK supports all UTF-8 strings" [documented, driver package docs]. | Plain `str`. `_strip_protocol` (a classmethod) removes `proto://` or `proto::`, strips trailing `/`, and returns `root_marker` if the result is empty [observed, spec.py L246-262]. `root_marker` is `""` by default, and "some FSs may require leading '/'" [documented, comment]. |
| **Path construction modes** | `Path::from` / `from_iter` *encode* problematic segments (RFC 1738 percent-encoding), so `"foo/../bar"` becomes `foo/%2E%2E/bar` and `"foo//bar"` becomes `foo/bar`. `Path::parse` *validates* and errors on `..`, empty segments and control characters, but allows arbitrary unicode and existing `%` sequences. Also `from_url_path`, `from_filesystem_path` and `from_absolute_path`. [documented] | One mode (normalize). | One mode. Escaping is per driver and transparent: keys are escaped on write and unescaped on read using `__0x<hex>__`. The escaped set differs per driver: s3blob escapes ASCII 0-31 and the `/` of `../`; gcsblob escapes 10 and 13 and `../`; azureblob escapes 0-31, `"#%?\` and 127, `../` and a trailing `/`; fileblob escapes 0-31, the OS separator if it is not `/`, `../`, `//` and a trailing `/`. [documented, "# Escaping" section of each driver's package doc] | One mode. Each implementation may override `_strip_protocol`. |
| **Directory notion** | No directories. `list_with_delimiter` returns `common_prefixes`. Prefixes match "on a path segment basis" (`foo/bar` is a prefix of `foo/bar/x` but not of `foo/bar_baz/x`). [documented, lib.rs] | A trailing `/` means a directory and anything else is a file [documented, raw/path.rs `normalize_path` doc]. `read`/`write` on a dir path → `ErrorKind::IsADirectory` [observed, operator.rs `validate_path`]. | No directories. `ListOptions.Delimiter`. `ListObject.IsDir` is true for prefixes [documented, blob.go]. | Directories exist in the API. The base `mkdir`/`makedirs` are a no-op `pass` with the comment "not necessary to implement, may not have directories" [observed, spec.py]. |
| **Error taxonomy** | One `Error` enum: `Generic{store}`, `NotFound`, `InvalidPath`, `JoinError`, `NotSupported`, `AlreadyExists`, `Precondition`, `NotModified`, `NotImplemented{operation, implementer}`, `PermissionDenied`, `Unauthenticated`, `UnknownConfigurationKey` [documented, lib.rs]. `From<Error> for std::io::Error` maps only `NotFound` to `io::ErrorKind::NotFound`; everything else becomes `Other` [observed]. **obstore** (Python): `NotFound` → builtin `FileNotFoundError`; `NotImplemented` → builtin `NotImplementedError`; the rest → `obstore.exceptions.*Error`, which subclass `BaseError(Exception)`. There is no `NotImplementedError` subclass of `BaseError`. [observed, pyo3-object_store error.rs; documented in the exceptions page note "Some operations also raise a built-in ValueError or FileNotFoundError"] | `ErrorKind`: `Unexpected`, `Unsupported`, `ConfigInvalid`, `NotFound`, `PermissionDenied`, `IsADirectory`, `NotADirectory`, `AlreadyExists`, `RateLimited`, `IsSameFile`, `ConditionNotMatch`, `RangeNotSatisfied`, `Conflict` [documented, types/error.rs]. Each error also has an `ErrorStatus`: `Permanent` ("MUST never retry"), `Temporary` ("MAY retry"), `Persistent` ("temporary but persisted after retries… SHOULD NOT retry") [documented]. **Python**: one exception class per kind (for example `opendal.exceptions.NotFound`). These are **not** builtin `FileNotFoundError`s, and despite an `Error` class existing they subclass `Exception` directly [observed, bindings/python/src/errors.rs `create_exception!(…, PyException, …)`]. | `gcerrors.ErrorCode`: `OK`, `Unknown`, `NotFound`, `AlreadyExists`, `InvalidArgument`, `Internal`, `Unimplemented`, `FailedPrecondition`, `PermissionDenied`, `ResourceExhausted`, `Canceled`, `DeadlineExceeded`, plus `Err*` sentinels for `errors.Is` [documented, gcerrors]. `gcerrors.Code(err)` maps `context.Canceled`/`DeadlineExceeded` [documented]. `Bucket.ErrorAs` / `errors.As` reach the driver's native error [documented, blob package doc]. Each driver implements `ErrorCode(error)` [documented, driver.go]. | Builtin Python exceptions by convention: `FileNotFoundError` (for example `_ls_from_cache`, `info`), `FileExistsError` (`pipe_file`/`put_file` with `mode="create"`), `NotImplementedError` as the default body of `fsid`, `ls`, `cat_ranges`, `cp_file`, `_rm`, `touch`, `created`, `modified`, `sign` [observed, spec.py AST scan]. Package exceptions: `FSTimeoutError(asyncio.TimeoutError)` and `BlocksizeMismatchError(ValueError)` [observed, exceptions.py]. Implementations translate natively. For example s3fs maps `NoSuchKey`→`FileNotFoundError`, `AccessDenied`→`PermissionError`, `PreconditionFailed` with `If-None-Match`→`FileExistsError`, other `PreconditionFailed`→`OSError(EINVAL)`, `NotImplemented`/501→`OSError(ENOSYS)`, and unknown codes→`OSError(EIO)` [observed, s3fs/errors.py]. |
| **Retries** | Built into the HTTP client and configured once per store with `RetryConfig { backoff, max_retries (default 10), retry_timeout (default 3 min) }` [documented + observed defaults]. Retried: "5xx server errors, connection errors, dropped connections, timeouts for safe/read-only requests" [documented]. Also retried: 429 and 408, plus 409 when a request opts in with `retry_on_conflict`, which S3 `PutMode::Update` uses [observed, retry.rs and aws/mod.rs]. Timeouts or interruptions are retried only if the request is `idempotent` or the method is HTTP-safe. "An idempotent request will be retried on timeout even if the request method is not safe" [documented]. S3 `PutMode::Overwrite` and `CopyMode::Overwrite` are marked `.idempotent(true)` [observed]. | Retries are **not** built in. `RetryLayer` is an opt-in layer, and it retries only when `Error::is_temporary()`. After it gives up it marks the error `Persistent` [documented, layers/retry]. Its docs warn that layer order matters with `TimeoutLayer` [documented]. Python exposes `RetryLayer` [observed, layers.pyi]. | Retries are not covered by the portable API. The blob docs and the five driver files I read do not mention retries [observed absence]. [inference] Retries are left to each provider SDK's client configuration. | Per implementation. The base class has none. s3fs: `retries = 5`; `_error_wrapper` backs off `min(1.7**i * 0.1, 15)` s on `S3_RETRYABLE_ERRORS` (socket timeout, HTTPClientError, IncompleteRead, FSTimeoutError, ResponseParserError) and on `ClientError`s matching SlowDown, "reduce your request rate" or XAmzContentSHA256Mismatch. Extension points: `add_retryable_error` and `CUSTOM_ERROR_HANDLER` [observed, s3fs/core.py]. |
| **Timeouts** | `ClientOptions` per store: `timeout` (whole request, default 30 s), `connect_timeout` (default 5 s), `read_timeout`, pool idle and HTTP/2 keep-alive. "Timeout errors are retried, subject to the RetryConfig" [documented + observed defaults, client/mod.rs]. | `TimeoutLayer` (opt-in). `timeout` (default 60 s) bounds control operations (`stat`, `create_dir`, `rename`, `presign`). `io_timeout` (default 10 s) bounds IO operations and every call on the returned reader, writer, lister, deleter or copier [documented]. It works by dropping the future [documented]. | Each call takes a `context.Context`, so deadlines and cancellation are per call. The Writer stores its ctx: "To abort a write, cancel ctx" [documented, NewWriter]. `Close` may fail if ctx was cancelled [documented]. The code is `DeadlineExceeded` / `Canceled` [documented]. | `sync(loop, func, timeout=…)` raises `FSTimeoutError` [observed, asyn.py]. Socket timeouts are per implementation (s3fs `connect_timeout = 5`, `read_timeout = 15`) [observed]. |
| **Concurrency limits** | `LimitStore::new(inner, n)` limits concurrent operations [documented, limit.rs]. | `ConcurrentLimitLayer::new(n)`. A cloned layer shares one semaphore across operators. There is also an optional HTTP-level semaphore [documented]. | Not in the portable API [observed absence]. | `batch_size` for the bulk methods of async implementations [documented, async page]. |
| **Consistency statements** | No general consistency section in the crate docs [observed absence: lib.rs, aws/mod.rs]. Stated guarantees are about atomicity: "All operations are atomic, and readers cannot observe partial and/or failed writes", and `put_opts` "is guaranteed to be atomic" [documented]. `list` order is "not guaranteed" [documented]. ETag and version are surfaced in `ObjectMeta` / `UpdateVersion`. "Stores will use differing combinations of e_tag and version… applications [should] preserve both" [documented]. `rename` is "by default… copy and then delete source. It may not check… that it was the same object" [documented]. | No general consistency statement found [observed absence in the files read]. A conditional-operation spec is referenced (`docs::specs::conditional_operations`) but I did not fetch it. Writer: "make sure either `close` or `abort` has been called before dropping the writer otherwise the data could be lost" [documented, writer.rs]. | Stated explicitly and repeated: "List is not guaranteed to include all recently-written blobs; some services are only eventually consistent". A blob "is not guaranteed to be readable until Close… until then, any previous blob will still be readable" [documented, blob.go List/NewWriter]. `List` order is lexicographic by UTF-8 key [documented]. | No storage consistency statement. fsspec adds a client-side listings cache (`DirCache`, `use_listings_cache`, `listings_expiry_time`), which can be stale. `invalidate_cache` exists [documented, spec.py `__init__` doc]. Transactions defer writes until the context exits, "semi-atomic", and not every implementation supports them [documented, features page]. |
| **Lifecycle / close** | No close or shutdown method on `ObjectStore` [observed: trait method list]. [inference] Resources are released when the value is dropped. Multipart: S3 `copy_if_not_exists` cleanup is "best effort"; "consider using a lifecycle rule" [documented]. | `Operator` has no close method in operator.rs [observed]. Per-operation objects do: `Writer::close`/`abort`, plus `close` on Deleter and Copier [observed + documented]. | `Bucket.Close()` releases resources [documented]. After Close, methods return `FailedPrecondition` "blob: Bucket has been closed", and a second Close returns the same error [observed, `errClosed`]. `Writer.Close` commits, and "you must always check the error of Close" [documented, howto]. `Reader` "must be closed" [documented]. | Instances are cached by constructor arguments (`_Cached` metaclass). The cache "prevents the filesystem from being garbage collected"; you must call `clear_instance_cache`. Opt out with `skip_instance_cache=True` [documented, spec.py and features page]. s3fs registers `weakref.finalize(self, close_session, …)` [observed]. Async users should "explicitly await resource destructors" (`await session.close()`) [documented, async page]. |
| **Async vs sync parity** | Async-only trait [documented: "high-performance async API"]. `LocalFileSystem` uses `spawn_blocking` inside tokio [documented]. **obstore**: "All operations have a comparable async method with the same name plus an `_async` suffix" [documented, getting-started]. | `Operator` is async. `blocking::Operator` wraps it and calls the runtime's `block_on`; "avoid using blocking::Operator in async context" [documented]. **Python**: `AsyncOperator` and `Operator` ("the blocking equivalent of AsyncOperator"), convertible with `to_operator()` / `to_async_operator()` [documented, operator.pyi]. | Synchronous Go API. Every call takes `ctx` [documented]. | `AsyncFileSystem` holds the `_*` coroutines. Sync methods are generated with `sync_wrapper` and run "on the same IO-dedicated thread" [documented, async page]. `asynchronous=True` gives direct await use. You can also pass `loop=` [documented]. The only built-in async implementation is HTTP [documented]. |
| **Capability introspection** | None. The trait has no capability query; you find out by calling [observed, trait method list]. | `OperatorInfo::capability()` returns the operator's *effective* capabilities [documented, info.rs]. | None. You find out by calling (for example `SignedURL` → `Unimplemented`) [documented]. | None generic. Unimplemented methods raise `NotImplementedError` [observed]. `async_impl` tells you whether an implementation is async [documented]. |
| **Instrumentation** | `ThrottledStore` (deterministic sleeps "for performance testing") [documented]. Option types carry an `extensions` field "for… tracing spans", which built-in backends ignore [documented]. Retries log through `info!` [observed]. | Opt-in layer crates: logging, tracing, fastrace, otel-trace, otel-metrics, metrics, fastmetrics, prometheus, prometheus-client, dtrace, await-tree, async-backtrace, hotpath, chaos, throttle, tail-cut, route, foyer, immutable-index, mime-guess, capability-check [observed, Cargo.toml features `layers-*`]. Always-on internal `ErrorContextLayer` [observed, builder.rs]. | Built-in OpenTelemetry traces and metrics (`completed_calls`, `latency`, `bytes_read`, `bytes_written`) on Attributes, Copy, Delete, ListPage, NewRangeReader and NewWriter [documented, blob package doc]. | Callbacks (`callback=`) and `logging`. |

## Capability-gate signalling (the open question)

### object_store 0.14.2: two variants, chosen by convention, plus per-store config

- **Two error variants.** `Error::NotSupported { source }` ("the attempted operation is not supported") and
  `Error::NotImplemented { operation, implementer }` ("Operation {operation} not yet implemented by {implementer}")
  [documented, lib.rs]. Since 0.13 the trait docs ask implementers to put the method name into `NotImplemented`
  [documented, lib.rs ~L906].
- **What the built-in stores do [observed in source]:**
  - S3 with `S3ConditionalPut::Disabled`:
    - `PutMode::Create` → `NotImplemented`, with operation "`put_opts` with mode `PutMode::Create` when conditional put is disabled".
    - `PutMode::Update` → `NotImplemented`.
  - S3 `CopyMode::Create` (`copy_if_not_exists`) with no `S3CopyIfNotExists` configured → `NotSupported`, with source "S3 does not support copy-if-not-exists".
  - `HttpStore` (WebDAV):
    - any `PutMode` other than Overwrite → `NotImplemented`.
    - `put_multipart_opts` → `NotImplemented`.
  - `LocalFileSystem`:
    - `PutMode::Update` → `NotImplemented`.
    - non-empty `attributes` → `NotImplemented`.
- **[inference]** There is no rule in the docs for when a store uses `NotSupported` and when it uses `NotImplemented`.
  The S3 store uses both for the same kind of gate (a conditional mode the backend can't provide).
  A caller who wants to detect "capability absent" has to match both variants.
- **The gate is configured per store instance, once:**
  - `S3ConditionalPut`: `ETagMatch` (the **default**; uses If-Match / If-None-Match) or `Disabled`.
  - `S3CopyIfNotExists`: `Header(k,v)`, `HeaderWithStatus(k,v,status)` or `Multipart`, with **no default** (None → NotSupported).
  - Both are parsed from config strings such as `etag`, `disabled`, `header: cf-copy-destination-if-none-match: *` or `multipart` [documented, aws/precondition.rs].
  - Normalization across stores [observed, aws/mod.rs]:
    - S3 404 on `If-Match` is converted to `Precondition` "for consistency with R2".
    - `NotModified`/`Precondition` on `If-None-Match` is converted to `AlreadyExists`.
    - InMemory also returns `Precondition` instead of `NotFound` "for consistency with stores" [observed, memory.rs comment].
- **Rename is never a gate.** `rename_opts` has a default implementation (copy, then delete), so it always "works".
  `RenameTargetMode::Create` maps to `CopyMode::Create`, so on S3 without config it fails as `NotSupported` [observed, lib.rs default impl].
  The docs say "there is currently NO flag to control the atomicity" of deleting the source [documented].
- **obstore** maps `NotSupported` → `obstore.exceptions.NotSupportedError` but `NotImplemented` → **builtin `NotImplementedError`**
  [observed, pyo3-object_store error.rs at py-v0.12.0]. In Python, the two forms of "capability absent" therefore have unrelated types.

### OpenDAL 0.59.5: a declared Capability struct, checked before dispatch, with simulation in between

- **Signal:** `ErrorKind::Unsupported` ("Underlying service doesn't support this operation") [documented].
  It is raised before the backend is called by `CorrectnessCheckLayer`, with the message "The service {scheme} does not support the operation {op} with the arguments {args}…".
  The layer checks, for example, `write` with `append`, `if_not_exists`, `if_match` or `if_none_match`, and `delete` with `version`, `recursive` or `if_*` [observed, layers/correctness_check.rs].
  Its docs: "OpenDAL applies this checker to every service by default"; it covers arguments "which might affect the correctness of the call" [documented].
  A stricter opt-in `CapabilityCheckLayer` also checks non-critical arguments such as `write_with_content_type` and `list_with_versions` [documented].
- **Stack applied once, in `Operator::new`:** `ErrorContextLayer` → `SimulateLayer::default()` → `CompleteLayer` → `CorrectnessCheckLayer` [observed, types/operator/builder.rs].
- **Emulation: native and effective capability really do differ.**
  - `SimulateLayer` ("Simulate missing capabilities for backends in a configurable way") can be toggled per simulation: `read_with_suffix`, `list_recursive`, `stat_dir`, `create_dir`, `delete_recursive`, all default `true` [documented].
  - It **rewrites the advertised capability** [observed, `simulate_capability`]:
    - `read_with_suffix = true` if `read`.
    - `create_dir = true` if `list && write_can_empty`.
    - `delete_with_recursive = true` if `list && delete`.
  - `create_dir` is emulated by writing an empty object at the dir path [observed].
  - In this version `CompleteLayer` only "keeps validation wrappers for read/write operations" [documented, complete.rs]. In older releases the emulation lived in `CompleteLayer`; it has moved to `SimulateLayer`.
    *[inference: the history is from my memory of earlier releases. I did not re-verify it against old tags.]*
- **Native vs full capability.**
  - `OperatorInfo` in 0.59.5 exposes **only** `capability()`, "the operator's effective capabilities" [documented, info.rs].
  - `Capability` docs: it "represents all operations available on the current operator, including those implemented through layers" [documented, capability.rs].
  - A grep of the fetched sources found no `native_capability` / `full_capability` methods [observed].
  - `CapabilityOverrideLayer` "updates [the effective] Capability… without changing the service's native capability", for example to switch off `write_with_if_match` for a given endpoint. It is exposed in Python too [documented, capability_override.rs; layers.pyi].
  - Conclusion: callers see one effective flag set. Whether a flag is native or simulated is not visible through `OperatorInfo` [observed].
- Capability fields that matter for the catalogue: `create_dir`, `rename`, `rename_with_if_not_exists`, `copy`, `copy_with_if_not_exists`, `write_with_if_not_exists`, `write_with_if_match`, `list_with_recursive`, `presign_*`, and `shared` ("supports shared access") [documented, capability.rs].
- Python: `Operator.capability()` / `AsyncOperator.capability()` [documented]. Unsupported → `opendal.exceptions.Unsupported` [observed].

### gocloud blob v0.47.0: error code at call time, no introspection

- **Signal:** `gcerrors.Unimplemented` ("the feature is not implemented") [documented].
  It is documented for `SignedURL` ("If the driver does not support this functionality, SignedURL will return an error for which gcerrors.Code will return gcerrors.Unimplemented") and for `SignedURLOptions.ContentType` / `EnforceAbsentContentType` [documented].
- **Drivers [observed]:**
  - s3blob → Unimplemented for signed DELETE and for content-type enforcement.
  - azureblob → Unimplemented for content-type enforcement.
  - gcsblob → Unimplemented without signing credentials.
  - fileblob → Unimplemented without `URLSigner`.
- **Rename / Move:** `*Bucket` has no rename or move method. Its methods are `As, ErrorAs, ReadAll, Download, List, ListPage, IsAccessible, Exists, Attributes, NewReader, NewRangeReader, WriteAll, Upload, NewWriter, Copy, Delete, DeleteWithOptions, SignedURL, Close` [observed].
- **Conditional create:** `WriterOptions.IfNotExist` is documented to fail with "gcerrors.PreconditionFailed". **No such code exists.** The gcerrors constant is `FailedPrecondition`, which is what fileblob and memblob actually return [observed: grep of errors.go/gcerr.go; fileblob.go L858, memblob.go L391]. This is a doc defect in v0.47.0.
  All five drivers I read handle `IfNotExist` [observed]. Whether an unsupporting driver would return Unimplemented is not documented.
- Provider-specific preconditions are possible only through `BeforeWrite` / `BeforeCopy` / `BeforeDelete` with `As` escape hatches. `DeleteOptions.BeforeDelete` is documented as the place for "a driver-specific precondition (for example a generation or If-Match condition)" [documented].

### fsspec 2026.9.0: NotImplementedError by default, otherwise emulation in the base class

- Capability absence is signalled by inheriting base-class bodies that `raise NotImplementedError`: `ls`, `cp_file`, `_rm`, `touch`, `cat_ranges`, `created`, `modified`, `sign`, `fsid` [observed].
- Many operations are **emulated** in the base class, with no flag:
  - `mv` = `copy(on_error="raise")` + `rm` [observed].
  - `pipe_file`/`put_file` `mode="create"` = `exists()` check, then write. The comment says "non-atomic but simple way" [observed].
  - `mkdir`/`makedirs` = no-op [observed].
- There is no capability query. A caller cannot tell a native operation from an emulated one [inference from the above].

## Scoping (OP-16 counterparts)

| Library | Name | Notes |
|---|---|---|
| object_store | `PrefixStore` (`object_store::prefix`) | "Store wrapper that applies a constant prefix to all paths handled by the store", stripping the prefix from results [documented, prefix.rs]. Path errors include `PrefixMismatch` [documented, path/mod.rs]. `LocalFileSystem` "can optionally be created with a directory prefix" [documented]. |
| obstore | `prefix=` constructor argument and `.prefix` property on `S3Store` | "Get the prefix applied to all operations in this store, if any" [documented, https://developmentseed.org/obstore/v0.12.0/api/store/aws/]. Only the S3 page was checked; I did not verify other stores. The page also exposes `retry_config` and `client_options` (`ClientConfig`) per store [documented]. |
| OpenDAL | `root` service option, normalized by `normalize_root` to `/abc/def/` | `OperatorInfo::root()` [documented]. No `PrefixLayer` exists in the layer list [observed, Cargo.toml features]. |
| gocloud | `blob.PrefixedBucket(bucket, prefix)`, the `?prefix=` URL parameter, and `blob.SingleKeyBucket` / `?key=` | The original bucket "will be closed and no longer usable" [documented, blob.go and howto]. The driver-level `driver.NewPrefixedBucket` just concatenates `prefix+key` [observed, driver.go]. |
| fsspec | `DirFileSystem` (protocol `"dir"`) | "assumes every path… is relative to the `path`". `_join` raises `ValueError` if `..` escapes the root, **only when the wrapped fs is `LocalFileSystem`**. The comment says that on object stores `..` "is a literal path part" [observed, implementations/dirfs.py]. |

## Notes

1. Four strategies for gate signalling are visible:
   - **declared + pre-checked** (OpenDAL `Capability` + `CorrectnessCheckLayer` → `Unsupported`);
   - **configured + call-time error** (object_store `S3ConditionalPut`/`S3CopyIfNotExists` → `NotImplemented` *or* `NotSupported`);
   - **call-time error only** (gocloud `Unimplemented`);
   - **silent emulation / NotImplementedError** (fsspec).

   OpenDAL is the only one with an introspectable flag set. Its flag set is the *effective* set, and it includes simulations by default.
2. Every library treats the following as an instance-wide decision, set once: path normalization rules, the error taxonomy, the retry and timeout policy, the concurrency limit, and the prefix scope. gocloud is the exception for retries and timeouts: they are per call via `ctx`, plus SDK configuration.
3. Retry safety:
   - object_store couples retry to idempotency per request.
   - OpenDAL couples it to error status (`Temporary` → retry, then `Persistent`).
   - s3fs couples it to an exception allowlist plus string matching.
   - gocloud does not decide at the portable layer.
4. The behaviour of `..` differs across all four libraries:
   - object_store rejects it (`parse`) or percent-encodes it (`from`).
   - gocloud escapes the `/` of `../` per driver.
   - OpenDAL passes it through.
   - fsspec DirFileSystem guards it only for local.
5. Doc defect: gocloud v0.47.0 `WriterOptions.IfNotExist` names a non-existent `gcerrors.PreconditionFailed`. The real code is `FailedPrecondition`.
6. Python bindings diverge from their Rust cores in exception typing:
   - obstore uses builtin `FileNotFoundError` and `NotImplementedError` for two variants.
   - OpenDAL Python uses no builtins, and its exception classes do not inherit from its `Error` class.
