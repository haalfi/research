# Track 15: Access-layer taxonomies of storage read behaviour

Question: does each data-access layer have a taxonomy of storage access and read behaviour that it has **built, defined and documented**, and on which the product is **founded**? The candidates are Apache OpenDAL, the Apache Hadoop FileSystem specification, the Apache Arrow `object_store` crate and fsspec. Other candidates were only screened.

This is not a survey of features. An enum alone never counts as a taxonomy.

Criteria:
- **C1 Defined**: the classes are named and each has a written definition.
- **C2 Principled**: the classification axis is stated, along with any coverage or exclusivity rules.
- **C3 Foundational**: backends must map native outcomes onto the classes, and the mapping is both documented and visible in code.
- **C4 Maintained**: the taxonomy has its own design record or versioning.

## Sources read (full text, local clones or raw files)

| Source | Version read |
|---|---|
| apache/opendal, shallow clone | commit 532050ac, 2026-11-04 |
| apache/arrow-rs-object-store, shallow clone | commit c216edef, 2026-11-01; Cargo version 0.14.2 |
| fsspec/filesystem_spec, shallow clone | commit 12c823bc, 2026-11-04 |
| Hadoop trunk, raw.githubusercontent.com, fetched 2026-11-08 | `filesystem/{index,introduction,model,notation,filesystem,fsdatainputstream,fsdatainputstreambuilder,testing,extending,pathcapabilities}.md`, `fs/contract/ContractOptions.java`, `hadoop-aws/.../s3a/S3AUtils.java`, `S3ARetryPolicy.java` |
| Screening only | go-cloud `internal/gcerr/gcerr.go` and `blob/driver/driver.go`; rclone `fs/fserrors/error.go` |

## Criteria table

| Candidate | C1 | C2 | C3 | C4 | Verdict |
|---|---|---|---|---|---|
| Apache OpenDAL | Met. Every `ErrorKind` variant has a doc comment. `ErrorStatus` Permanent, Temporary and Persistent are defined with MUST / MAY / SHOULD NOT retry rules (`core/core/src/types/error.rs`). | Met. RFC-8145 states that the two axes are independent: "Error kind and retry status remain independent". It gives exclusivity rules for ConditionNotMatch, Conflict, AlreadyExists and NotFound, and an `Unexpected` fallback for unknown 409/412. | Met. `docs/internals/service.rs` says "An implementation must: … Return structured OpenDAL errors with the correct `ErrorKind`". RFC-8145 has a mapping table. The code maps in `services/s3/src/core.rs` (`parse_error`, `parse_s3_error_code`), `raw/std_io_util.rs` and `raw/http_util/error.rs`. `RetryLayer` keys on `is_temporary()` and calls `set_persistent()`. | Met. RFC series: 0044 error_handle (2022-02-23), 0247 retryable_error (2022-04-12), 0977 refactor_error (2022-11-21), 8145 conflict_error_kind (2026-08-25). Capability RFCs: 0409, 0627, 2852, 6707, 7700 (2026-06-05). | **CONFIRMED** |
| Hadoop FileSystem specification | Partial. Read semantics are defined formally as pre- and postconditions over the model `FSDIS = (pos, data, isOpen)`. The outcome classes are JDK and Hadoop exception classes that are named per precondition. The spec does not define a set of outcome classes. | Partial. The rules are stated: "MUST NOT be a superclass", "earlier elements … preferred", network failures "MUST be an instance of IOException", unimplemented operations raise UnsupportedOperationException. There is no retryability axis, only "Implementations MAY retry". | Partial. Conformance is enforced by contract tests and `ContractOptions` flags, including `supports-strict-exceptions`. The translation from native errors is connector code (`S3AUtils.translateException`, `S3ARetryPolicy`) and is not specified. | Partial. The spec calls itself a "live document" that should be extended along with the APIs. It has no separate versioning or design-record series (based on the files read; JIRA history not read). | **PARTIAL** (C1, C2, C4 partial; C3 partial for error mapping) |
| Arrow `object_store` | Partial. Each `Error` variant has a one-line definition, e.g. "Error when the object is not found at given location". The public `client::HttpErrorKind` has a written retry rule for each variant. | Not met. No classification axis is stated. `Generic` is "A fallback error type when no variant matches". Retryability exists only on the HTTP-transport enum and is not on `Error`. | Partial. Per-method contracts name the outcome (e.g. PutMode Create gives `AlreadyExists`, Update gives `Precondition`). The status mapping is visible in `src/client/retry.rs` (`RetryError::error`), but there is no documented rule that backends must follow. | Not met. No design record. Only CHANGELOG entries. | **PARTIAL** (C2, C4 failed; C1, C3 partial) |
| fsspec | Not met. The project uses Python built-in exceptions by convention. `fsspec/exceptions.py` has only BlocksizeMismatchError and FSTimeoutError. | Not met. | Not met at the layer level. The HTTP retry classification (`_RETRYABLE_STATUSES`, `_is_retryable`) is local to `implementations/http.py`. | Not met. | **NOT FOUND** |

## Extracted taxonomies

### Apache OpenDAL (CONFIRMED)

**Axis 1: `ErrorKind`, why the operation failed.** Each class is quoted from its doc comment in `core/core/src/types/error.rs`. The enum is `#[non_exhaustive]`.

| Class | Definition |
|---|---|
| Unexpected | "OpenDAL don't know what happened here, and no actions other than just returning it back. For example, s3 returns an internal service error." |
| Unsupported | "Underlying service doesn't support this operation." |
| ConfigInvalid | "The config for this service is invalid." It also covers invalid option values or combinations. |
| NotFound | "The given path is not found." |
| PermissionDenied | "The given path doesn't have enough permission for this operation" |
| IsADirectory | "The given path is a directory." |
| NotADirectory | "The given path is not a directory." |
| AlreadyExists | "The given path already exists thus we failed to the specified operation on it." |
| RateLimited | "Requests that sent to this path is over the limit, please slow down." |
| IsSameFile | "The given file paths are same." |
| ConditionNotMatch | "A condition supplied through the OpenDAL operation evaluated to false." It is returned only for conditions the caller supplied. |
| RangeNotSatisfied | "The range of the content is not satisfied." |
| Conflict | "The operation conflicts with the current or transitional state of the resource. … This error kind does not indicate whether retrying the same operation is safe." |

**Axis 2: `ErrorStatus`, retry status.** This is a private enum, exposed through `is_temporary()` and `is_persistent()`.

| Status | Definition |
|---|---|
| Permanent | "The error is stable and will not change without external changes … Users MUST never retry this operation." This is the default in `Error::new`. |
| Temporary | "The error is temporary … Users MAY retry an operation to resolve this error." |
| Persistent | "The error was temporary but persisted after retries … Users SHOULD NOT retry this operation." `RetryLayer` sets it after retries are exhausted. |

**Principles from RFC-8145**
- Kind and status are independent. Retry status "describes whether the current layer can replay an operation, not why the operation failed".
- `set_temporary()` means "the receiving OpenDAL layer can safely replay the same operation method with its retained state".
- Services classify "by native error code and operation context before using an HTTP status fallback".
- Unknown 409 and 412 responses map to `Unexpected`.
- The same native code can need a different retry status depending on the operation. S3 ConditionalRequestConflict is temporary on PutObject but not on CompleteMultipartUpload.

**Capability taxonomy**
- The `Capability` struct in `types/capability.rs` documents naming families: basic, compound, variants, parameterized (`read_with_if_match`), limitations, and metadata results (`stat_has_*`).
- The conditional-operations spec (`docs/specs/conditional-operations.md`) is normative. A condition the service does not support returns `Unsupported`, and "OpenDAL never silently ignores a condition."

**Mapping examples in code**
- S3 (`services/s3/src/core.rs`): 403 maps to PermissionDenied, 404 to NotFound, 304/412 with a caller condition to ConditionNotMatch, 429 to RateLimited (temporary), and 499/5xx to Unexpected (temporary). Error codes take precedence over status: `NoSuchBucket` maps to ConfigInvalid even though the status is 404, `OperationAborted` maps to Conflict (temporary), and `SlowDown` maps to RateLimited (temporary).
- std::io (`raw/std_io_util.rs`): NotFound, PermissionDenied, AlreadyExists and Unsupported keep their meaning and are permanent. Interrupted, UnexpectedEof, TimedOut and WouldBlock map to Unexpected (temporary). Every other io error, `_`, also maps to Unexpected (temporary).
- fs (`services/fs/src/core.rs`): an io AlreadyExists maps to ConditionNotMatch.

**Limits and open issues**
- RFC-8145's tracking issue is the placeholder "#0000".
- The RFC itself says "Backends with incomplete error documentation will continue to return `Unexpected` until their behavior is verified".
- No error kind exists for truncated bodies or mid-stream failures; they fall into Unexpected with temporary status. That this is coarse is inference.
- Treating every unknown io error as temporary is a design choice visible in code. Whether it is justified is undocumented in what I read (inference).

**Read semantics**
- Not examined in this track: Reader range semantics, short reads, and whether `RetryLayer` reader retry resumes mid-stream.
- RFC-0247 only states "retry the operation if no actual IO happens". It is a 2022 design and may have been superseded.

### Hadoop FileSystem specification (PARTIAL)

**Purpose (index.md):** "define the Hadoop FileSystem model and APIs so that multiple filesystems can implement the APIs and present a consistent model of their data to applications".

**Read model (fsdatainputstream.md)**
- `read(buffer, off, len)` may return any l in `1..min(...)`. It "must block until at least one byte is returned".
- It returns -1 at or after EOF.
- "For any operations that fail, the contents of the destination `buffer` are undefined."
- If data changes during a read, the stream's value "is undefined". Changes "MAY or MAY NOT be visible" and may be "partially visible".

**Outcome rules**
- Exceptions are named per precondition, e.g. `pos >= 0 else raise EOFException, IOException`.
- From notation.md: "earlier elements of the set are preferred".
- From introduction.md: a named exception "MAY be an instance or subclass … MUST NOT be a superclass".
- Network failures "MUST be an instance of IOException".
- The spec has no transient or permanent classification. "Implementations MAY retry failed operations" only if the happens-before relationship is preserved.

**Capabilities**
- PathCapabilities strings: common ones use the `fs.capability.` prefix; store-specific ones use `fs.<scheme>.capability.`.
- Contract-test flags in `ContractOptions.java`, e.g. `is-blobstore` ("Implies it's not a real directory tree and consistency is below that which Hadoop expects") and `supports-strict-exceptions`.

**Connector mapping (code only, S3A)**
- `S3AUtils.translateException`: 404/410 map to FileNotFoundException, 401/403 to AccessDeniedException, 416 to RangeNotSatisfiableEOFException, and 503 or GCS 429 to AWSServiceThrottledException.
- `S3ARetryPolicy` assigns each exception class a retry policy, e.g. `FileNotFoundException` → fail, `SocketTimeoutException` → connectivityFailure, `AWSServiceThrottledException` → throttlePolicy.

That retry classification is connector-local. It is not part of the specification.

**Limits:** extending.md says "The FileSystem specification is incomplete … failure modes, and other unexpected outcomes".

### Arrow object_store (PARTIAL)

**`Error` (src/lib.rs, `#[non_exhaustive]`)**

| Class | Definition |
|---|---|
| Generic | "A fallback error type when no variant matches" |
| NotFound | "Error when the object is not found at given location" |
| InvalidPath | Invalid path |
| JoinError | `tokio::spawn` failed |
| NotSupported | "Error when the attempted operation is not supported" |
| AlreadyExists | "Error when the object already exists" |
| Precondition | "Error when the required conditions failed for the operation" |
| NotModified | "Error when the object at the location isn't modified" |
| NotImplemented | Operation not implemented by the implementer |
| PermissionDenied | "Error when the used credentials don't have enough permission" |
| Unauthenticated | "lack valid authentication" |
| UnknownConfigurationKey | Unknown configuration key |

**Retry axis (public `client::HttpErrorKind`, src/client/http/connection.rs)**

| Kind | Retry rule |
|---|---|
| InvalidRequest | "Retrying the same input cannot succeed. Will not be automatically retried" |
| Connect | Retried |
| Request | Retried |
| Timeout | "retried if the request is idempotent" |
| Interrupted | "retried if the request is idempotent" |
| Decode | Not retried |
| Unknown | Not retried |

HTTP statuses are retried when they are 5xx, 429, 408, or 409 if `retry_on_conflict` is set (`retry.rs`).

**Mapping (`RetryError::error`):** 404 → NotFound, 304 → NotModified, 412 → Precondition, 409 → AlreadyExists, 403 → PermissionDenied, 401 → Unauthenticated, everything else → Generic.

The 409 → AlreadyExists default is the conflation that OpenDAL RFC-8145 argues against. The comparison is my inference.

**Purpose (crate docs):** the interface "is designed to mirror the APIs of object stores and *not* filesystems … stateless APIs instead of cursor based interfaces".

### fsspec (NOT FOUND)

- The backend guidance in developer.rst points to builtins: "raise PermissionError, OSError 30 or some read-only exception".
- HTTP retry classification was added in a changelog entry (#2124): "retry transient failures (408/425/429/5xx, dropped connections, timeouts, truncated range bodies, a 416 inside the file)".
- This is a per-implementation policy, not a layer taxonomy.

## Screening list (one line each)

**Read (raw source, screening depth only):**
- **Go CDK (gocloud.dev) gcerrors:** a strong lead. `ErrorCode` "describes the error's category". Each code has a definition (NotFound, AlreadyExists, FailedPrecondition, ResourceExhausted, DeadlineExceeded, …). The blob driver interface requires `ErrorCode(error) gcerrors.ErrorCode`. C2 and C4 not assessed, so this is not a verdict: COVERAGE-GAP.
- **rclone fserrors:** retry-axis interfaces (`Retrier`, `Fataler`, `NoRetrier`) with short definitions. It has no error-kind axis in that file and no design record was seen. Screened as a retry-classification convention.

**Not read in this track (no claims):**
- Apache jclouds
- Apache libcloud
- Alluxio
- JuiceFS
- AWS, GCS and Azure SDK retry classifiers
- POSIX-like FUSE layers

## Relations to prior report (read after extraction)

The prior report has no entry for OpenDAL, Hadoop, object_store or fsspec (grep count 0). The relations below are mine; any marked "inference" is not stated by the sources.

**OpenDAL**
- `ErrorStatus` relates to G.1 "Transient vs sticky/persistent" (IRON 05-C1, Lampson & Sturgis 08-C9, Avižienis 08-C6) and to "Interrupted (retryable) vs failed" (POSIX 01-C3, Rust 02-C9).
- OpenDAL's "Persistent" has a different basis: an error that was temporary and *persisted after retries*. It is a status the retry layer assigns, not a property of the fault. This adds a third basis to the "definitions differ in basis" caveat in G.1 (inference).
- The retry-status semantics ("the receiving layer can safely replay") resemble NVMe DNR retry advice (03-C2) and RFC 9110 idempotent methods (07-C3/C6). That analogy is inference.
- ConditionNotMatch vs Conflict reflects the RFC 9110 412 vs 409 distinction, which RFC-8145 cites. It relates to the C row "Strong vs weak validators; safe/idempotent methods".
- The std::io mapping relates to the C row "Ok(n)/Err with ErrorKind (Rust std::io)": OpenDAL collapses UnexpectedEof and Interrupted into Unexpected+Temporary. This loses the G.1 "End-of-stream vs error vs unexpected end" distinction at this layer (inference from code).

**Hadoop**
- The read postconditions match G.1 "Short (partial) success vs failure" (POSIX 01-C1) and "End-of-stream vs error" (Java 02-C12).
- "buffer undefined on failure" parallels the NVMe row in C ("buffer undefined on error").
- The consistency clauses ("MAY or MAY NOT be visible", partial visibility) sit below the C rows on safe, regular and atomic registers (06-C1–C3). A changing file read through FSDIS gives at most safe-register-like guarantees (inference).

**object_store**
- NotModified and Precondition relate to the C row on RFC 9110 validators (07-C3).
- The "stateless, not cursor" design statement contrasts with the C rows on stream contracts (Go, Rust, WHATWG).

**Prior report scope:** none of the four layers appears in section C, so its list of classifications is missing the access-layer level.

## Gaps

- **COVERAGE-GAP:** OpenDAL Reader and stream semantics (short reads, retry after partial IO) were not read.
- **COVERAGE-GAP:** Go CDK gcerrors C2 and C4 were not assessed.
- **COVERAGE-GAP:** JIRA and HADOOP issue history for the Hadoop spec was not read.
- **COVERAGE-GAP:** jclouds, libcloud, Alluxio, JuiceFS and the cloud SDKs were not read.
- **GENUINE-GAP (within sources read):** none of the four layers defines an outcome class for truncated or mid-stream read failure separate from generic or unexpected errors. Hadoop uses EOFException only for range and seek preconditions. OpenDAL and object_store route such failures to Unexpected or Generic.
- **GENUINE-GAP (within sources read):** none states a coverage proof or exclusivity rule for the whole kind set. OpenDAL states exclusivity only among the condition, conflict and existence kinds, and relies on Unexpected as the catch-all.
