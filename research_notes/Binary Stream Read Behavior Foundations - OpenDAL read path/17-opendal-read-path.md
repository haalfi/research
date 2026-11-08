# Track 17: Apache OpenDAL read path (primary sources)

## Scope and method

- Subject: the OpenDAL **read path**: public `Operator`/`Reader` API, the raw `oio::Read` contract, the default layers, `RetryLayer`, HTTP body handling, and the S3, GCS and fs services.
- Boundary: this track describes what OpenDAL documents and implements. It proposes no taxonomy and judges no design.
- Labels used below:
  - **DOCUMENTED**: rustdoc, RFC or spec text in the repo, or docs.rs / opendal.apache.org.
  - **IMPLEMENTED**: code behaviour at the pinned commit, read from source. No cargo build or test run was done, so "test asserts X" means that the test source asserts X. The test was not executed.
  - **INFERENCE**: my reading of how several code paths combine. No single source states it.
- Retryability is recorded as an outcome attribute (ErrorStatus). Retry behaviour (RetryLayer) is recorded as a mechanism.
- Prior track 15 already confirmed the ErrorKind x ErrorStatus taxonomy (15-C1..C8), the std::io mapping (15-C9) and S3 code-first classification (15-C8). These are not repeated here; they are cited where relevant.

## Sources and access status

Repository: `git clone --depth 1 https://github.com/apache/opendal`
**Commit: `532050ac3c099dd8591cde652a8ed1aaf03ba418`** (committed 2026-11-04 +0800). All paths below are relative to the repo root.

| Source | Access |
|---|---|
| `core/core/src/types/read/reader.rs` (public `Reader`) | full-text |
| `core/core/src/types/read/buffer_stream.rs` (`StreamingReader`, `ChunkedReader`, `BufferStream`) | full-text |
| `core/core/src/types/read/futures_async_reader.rs` | read in part (lines 35-345 plus selected tests) |
| `core/core/src/blocking/read/std_reader.rs` (`std::io::Read` adapter) | full-text |
| `core/core/src/types/context/read.rs` (`ReadContext`, `ReadGenerator`) | full-text |
| `core/core/src/raw/oio/read/{api,stream_read,position_read}.rs` | full-text |
| `core/core/src/layers/complete.rs` (`CompleteLayer`) | read in part (read path, lines 20-370) |
| `core/core/src/layers/correctness_check.rs` | read in part (`read`, lines 181-221) |
| `core/core/src/types/operator/builder.rs` (`Operator::new` default layers) | read in part |
| `core/core/src/types/operator/operator.rs` (`read`, `read_with`, `reader*`) | read in part (lines 589-787) |
| `core/core/src/types/options.rs` (`ReadOptions`) | read in part (lines 159-300) |
| `core/core/src/raw/ops.rs` (`OpRead`, `OpReader`) | read in part |
| `core/core/src/types/http_transport/body.rs` (`HttpBody`) | full-text |
| `core/http-transports/reqwest/src/lib.rs` | read in part (lines 135-235) |
| `core/core/src/raw/std_io_util.rs` | full-text (non-test part) |
| `core/core/src/raw/http_util/header.rs` (`parse_into_metadata`) | read in part |
| `core/core/src/types/error.rs` | read in part (ErrorKind tail, ErrorStatus, setters) |
| `core/layers/retry/src/lib.rs` (`RetryLayer`) | read in part (lines 31-800, tests 1250-1484) |
| `core/services/s3/src/{reader.rs,core.rs}` | reader full-text; core: `s3_get_object_request`, `parse_error`, `parse_s3_error_code` |
| `core/services/gcs/src/{reader.rs,core.rs}` | reader full-text; core: `gcs_get_object_request` (partial), `parse_error` |
| `core/services/fs/src/{reader.rs,backend.rs,core.rs}` | reader full-text; `read`, `read_at`, `fs_open` |
| `core/core/src/docs/specs/conditional-operations.md` | full-text |
| `core/core/src/docs/rfcs/7945_limited_read.md` | full-text |
| `core/core/src/docs/rfcs/5485_conditional_reader.md` | full-text |
| `core/core/src/docs/rfcs/7660_move_read_range_to_reader.md` | read in part (summary, range semantics, retry layer, rationale) |
| `core/core/src/docs/rfcs/5871_read_returns_metadata.md` | read in part (grep plus lines 84-95, 205-216) |
| `core/core/src/docs/internals/service.rs` | read in part (lines 60-95) |
| `core/tests/behavior/async_read.rs` | read in part (test list, if_match test) |
| docs.rs `opendal-core` 0.59.5 `struct.Reader.html` | full-text (rustdoc text matches HEAD for `read`, `fetch`, `metadata`, `into_futures_async_read`) |
| opendal.apache.org/docs/rust/opendal/struct.Reader.html | reached (HTTP 200, contains the same doc strings); not read in detail |
| docs.rs `opendal/latest/opendal/struct.Reader.html` | redirected to the crate page; struct page not reached |

Issues and PRs were **not read**. RFC headers name tracking issues #7938, #7661 and #5486, but I did not open them.

---

## Q1. Read API and reader contract

### Public API surface (DOCUMENTED + IMPLEMENTED)

- **`Operator::read`** (operator.rs:589-615): "Read the entire file into bytes from given path." It takes no options. `read_with` and `read_options` add `range`, conditions, `concurrent` and `chunk`. Implementation (`read_inner`, operator.rs:684-707): build `ReadContext`, then `Reader::read(range)`.
- **`Operator::reader` / `reader_with`** (operator.rs:709-787) return a `Reader`. No I/O happens at creation. `reader_inner` carries the annotation "Allow this unused async".
- **`ReadOptions.range`** (options.rs:160-170):
  - "`..` means read bytes in range `[0, n)`"
  - "`BytesRange::suffix(1024)` means read the last `min(1024, n)` bytes of file".
- **`concurrent` / `chunk` / `gap`** (options.rs:256-291):
  - concurrent: "opendal will fetch chunks concurrently with the give chunk size."
  - gap: ranges are merged and "discard the unrequested data in between."
- **`Reader::fetch`** (reader.rs:166-177): "merge given ranges into a list of non-overlapping ranges ... Merged ranges will be split by `chunk`, then executed with `concurrent` and `prefetch`."
- **Execution choice** (IMPLEMENTED, buffer_stream.rs:246-286): "If chunk is None, BufferStream will use StreamingReader ... Otherwise ... ChunkedReader".
  - StreamingReader opens one `oio::Read::open(range)` stream.
  - ChunkedReader issues bounded `oio::Read::read(range)` calls through `ConcurrentTasks`.
  - When `chunk` is set, the range is first resolved by `parse_into_range`. For an unbounded range this calls `content_length()`, which uses `content_length_hint`, then cached metadata, then `stat` (context/read.rs:116-133).

### Can a read return fewer bytes than requested?

- **Raw `oio::Read::read` (exact)**. Both DOCUMENTED and IMPLEMENTED.
  - RFC-7660 (lines 222-226): "`read` is not a syscall-style partial read ... For a valid bounded planner range, `read` should either return the complete range content or return an error."
  - `StreamReader::read` (stream_read.rs:59-75) compares `buffer.len()` with `range.size()` and returns `ErrorKind::Unexpected` "reader got unexpected data size".
  - `PositionReader::read` (position_read.rs:105-135) loops over short `read_at` results. An empty result returns `RangeNotSatisfied` "range exceeds content length".
- **Positioned primitive `PositionRead::read_at` (may be short)**. DOCUMENTED (position_read.rs:28-33): "`size` is the maximum number of bytes to read, and implementations may return fewer bytes. Returning an empty buffer means EOF."
- **Public `Reader::read(range)`** (reader.rs:136-143) collects the `BufferStream`. Its rustdoc is silent on short results.
  - IMPLEMENTED: with the default `CompleteLayer` (builder.rs:43-50), a bounded non-suffix range must be returned exactly.
  - `CompleteReadStream` checks at EOF and returns `Unexpected` "reader got too little data" or "reader got too much data" (complete.rs:335-367).
  - A suffix or unbounded range is not size-checked by CompleteLayer (complete.rs:290-295: `size = if range.is_suffix() { None } else { range.size() }`).
  - RFC-7945 restates the current rule: "Today a caller can use `range(0..N)`, but a bounded range is exact. When its starting byte exists but its end crosses EOF, the read fails even if the available bytes are sufficient" (7945:25-28).
- **`Reader::fetch`** also checks each chunk itself in `push_fetch_output` (reader.rs:287-298): "reader got unexpected data size" (Unexpected).
- **Adapters (may be short)**. `FuturesAsyncReader::read_buffer` (futures_async_reader.rs:177-181) and `StdReader::read_buffer` (std_reader.rs:48-52): "It can return fewer bytes than requested, including an empty buffer at EOF."

### End-of-data signalling

- **Raw stream**. IMPLEMENTED (api.rs:113-126; buffer_stream.rs:84-91): an **empty `Buffer`** means end. `read_all` loops until `buf.is_empty()`. `StreamingReader` treats an empty buffer as the end of the current sub-reader and moves to the next.
- **`BufferStream` / `FuturesBytesStream`** (futures `Stream`): the stream ends (`None`) after the last buffer. INFERENCE from `BufferStream` built on `StreamingReader`/`ChunkedReader` returning empty.
- **`FuturesAsyncReader`** (`futures::AsyncRead`). DOCUMENTED (futures_async_reader.rs:42-43): "An unbounded read treats [`ErrorKind::RangeNotSatisfied`] as EOF. Bounded reads and other errors are propagated."
  - IMPLEMENTED: `is_unbounded_eof_error` (lines 105-107). `poll_read` returns `Ok(0)` at end (line 283).
  - Errors are converted by `format_std_io_error`. Only NotFound and PermissionDenied keep their kind; everything else becomes `io::ErrorKind::Other` (std_io_util.rs:57-65).
- **`StdReader`** (`std::io::Read`, blocking). IMPLEMENTED: `block_on(FuturesAsyncReader::read)`, so it inherits the same EOF and error conversion (std_reader.rs:92-101).
- **Seek beyond end**. DOCUMENTED (reader.rs:416-420): "Seeking from the start or current position can move beyond the end without resolving the length, and subsequent reads return EOF. Explicit bounded ranges continue to reject seeks beyond their logical end." IMPLEMENTED as `io::ErrorKind::InvalidInput` "invalid seek to a position beyond the end of the range" (futures_async_reader.rs:321-323).

### Ranges beyond object size; empty objects

- **DOCUMENTED** (`ErrorKind::RangeNotSatisfied`, error.rs:90-93): "OpenDAL returns this error to indicate that the range of the read request is not satisfied."
- **IMPLEMENTED** cases:
  - `parse_into_range`: start > end returns `RangeNotSatisfied` "range starts after the end of the object"; offset+size overflow returns RangeNotSatisfied (context/read.rs:136-170). This path runs only with `chunk` set or when the length is needed.
  - **fs (positioned)**, bounded range crossing EOF: `PositionReadStream::read` returns `RangeNotSatisfied` on any empty `read_at` while `remaining` is `Some` (position_read.rs:179-188). This includes the case after some bytes have already been delivered.
  - **fs**, unbounded range starting at or past EOF: empty, i.e. clean EOF (`remaining` None, lines 179-189).
  - **S3**: 416 with XML code `InvalidRange` gives `RangeNotSatisfied`, Permanent (s3 core.rs:2300). 416 without a parsed code falls to `_ => (ErrorKind::Unexpected, false)` (core.rs:2224).
  - **GCS**: `parse_error` has no 416 arm. 416 gives `Unexpected`, Permanent (gcs core.rs:2256-2273). INFERENCE: GCS never yields RangeNotSatisfied from an HTTP status.
  - **S3/GCS bounded range crossing EOF** (INFERENCE from code): the service returns 206 with the available bytes; `HttpBody` passes, because Content-Length equals the bytes received; then `CompleteReadStream` returns `Unexpected` "reader got too little data", Permanent.
  - Result (INFERENCE): the same caller situation, "bounded range whose end crosses EOF", yields `RangeNotSatisfied` on fs but `Unexpected` on S3/GCS.
- **Empty object** (INFERENCE from code): `..` sends no Range header (`if !range.is_full()`, s3 core.rs:586-588), so 200 with an empty body leads to an empty Buffer. RFC-7945 (lines 41-44, 112-114) discusses empty objects only for the proposed `limit`. No behaviour test was found for empty-object or past-EOF ranges in `async_read.rs` (grep). `test_read_suffix_larger_than_file` covers suffix > size, which returns the whole content (async_read.rs:157-170).

## Q2. Truncation detection

Three independent checks exist on the read path (IMPLEMENTED):

1. **HTTP body vs Content-Length** (`HttpBody::check`, body.rs:114-134). At stream end `consumed` is compared with `size`.
   - Short body: `Unexpected` "http response got too little data, expect: {expect}, actual: {actual}" with `.set_temporary()`.
   - Long body: "too much data", also Temporary.
   - `size` comes from the transport. The reqwest transport says "Get content length from header so that we can check it", and leaves size `None` for HEAD or when `Content-Encoding` is present (reqwest lib.rs:150-159). With no Content-Length (chunked or close-delimited), `check` returns Ok and **no truncation check exists at this layer** (body.rs:115-117). This relates to 07-C4.
   - Transport body errors (connection reset etc.) become `Unexpected` "read data from http response", Temporary when `is_request() || is_body() || is_decode()` (reqwest lib.rs:189-200, 226-234).
2. **Requested range size** (`CompleteLayer`, default layer; complete.rs:26 "CompleteLayer keeps validation wrappers for read/write operations").
   - Bounded non-suffix `open` and `read`: exact size, otherwise `Unexpected` "reader got too little data" / "too much data". Status is **not** set, so it is the default **Permanent** (complete.rs:350-367; Permanent default per 15-C2).
   - Also `StreamReader::read` (stream_read.rs:66-72) and `Reader::fetch` (reader.rs:292-298): "reader got unexpected data size", Unexpected, Permanent.
3. **Positioned EOF** (fs): `RangeNotSatisfied` (position_read.rs:119-126, 179-188). `read_at` returning more than asked gives Unexpected (lines 202-212).

- **std::io `UnexpectedEof`** maps to `Unexpected` + Temporary (std_io_util.rs:38). Track 15 already recorded this (15-C9).
- **No stat-size check**: content length from stat is used only for range planning (`parse_into_range`), not to validate a streaming read. RFC-7945 (lines 163-170) states: "HTTP services still validate the response body's `Content-Length`, so accepting object EOF does not turn a truncated network response into success."
- **"Content incomplete" signal**: there is **no dedicated ErrorKind**. Truncation surfaces as `Unexpected`, with Temporary (HTTP) or Permanent (CompleteLayer), and is distinguishable only by message and context strings. DOCUMENTED + IMPLEMENTED.
- **Test evidence** (test source, not run): `test_chunked_unbounded_reader_propagates_truncation_error` (futures_async_reader.rs:876-895). Content "Hello" with a declared length of 10 and `chunk(4)` gives `read_to_end` an error of kind `io::ErrorKind::Other`, after "Hell" has been delivered.

## Q3. Version consistency across a read

- **Options** (DOCUMENTED, options.rs:171-247):
  - `version`: "This selects which stored version the read returns; it is not a condition on the file."
  - `if_match`: "A file with a different ETag returns `ConditionNotMatch`; a missing file returns `NotFound`."
  - Also `if_none_match`, `if_version_match`, `if_version_not_match`, `if_modified_since`, `if_unmodified_since`. Each is capability-gated, giving `Unsupported`.
  - `content_length_hint`: "must not be used as an object identity or consistency condition" (options.rs:249-254).
  - `ReadOptions` has **no `if_not_changed`**. That field exists only on other operations' option structs (options.rs:120, 776, ...).
- **Spec** (conditional-operations.md):
  - "`stat` and `read` check the file being observed" (line 16).
  - "OpenDAL never silently ignores a condition" (line 35).
  - "The point at which an operation surfaces a conditional error is unspecified ... during I/O" (lines 126-129).
  - The spec says **nothing about multi-request reads or pinning a version across chunks**. GENUINE-GAP within the sources read.
- **Enforcement** (IMPLEMENTED): `CorrectnessCheckLayer::read` returns Unsupported for each unadvertised `read_with_*` option (correctness_check.rs:181-221). fs advertises only `read: true` (fs backend.rs:140) and ignores `OpRead` (`fn read(&self, _ctx, path, _: OpRead)`, backend.rs:208).
- **Per-chunk propagation** (IMPLEMENTED): `S3Reader`/`GcsReader` store `args: OpRead` and add the same `If-Match`, `versionId` / `generation` / `ifGenerationMatch` to **every** `open(range)` (s3 reader.rs:30-60; s3 core.rs:573-603; gcs core.rs:180-196). A caller-supplied `version` or `if_match` therefore applies to every chunk, concurrent sub-read and retry re-open. INFERENCE from code.
- **No automatic pinning** (IMPLEMENTED): no code in `reader.rs`, `buffer_stream.rs`, `context/read.rs`, `complete.rs` or the retry layer reads an observed ETag or version and adds it as a condition. A grep for etag / if_match / version in those files found only licence headers and an unrelated list field.
  - `ReadContext::observe_read_response` caches only the **first** metadata (`OnceLock`, "if ... self.metadata().is_none()"; context/read.rs:107-114).
  - DOCUMENTED in RFC-5871 (lines 90-91): "If several reads are opened by the same reader, the cache stores the first object metadata observed by those reads."
  - Later chunks with a different ETag are neither compared nor rejected.
- **If the object changes between chunks** (INFERENCE from code): with no caller condition, chunks may come from different versions. A length change may be caught by the CompleteLayer size check; a same-length change is not detected. With caller `if_match` / `version`, a changed object yields 412 and `ConditionNotMatch` on the next request (s3 core.rs:2218; gcs core.rs:2265-2267).
- **fs** (INFERENCE): one file handle is opened lazily per `Reader` and shared by all chunks (`Arc<OnceCell<Handle>>`, position_read.rs:50-54, 86-88). Sub-reads read the same open file, with no version notion.

## Q4. Retry inside reads

- **DOCUMENTED** (retry lib.rs:31-47): "This layer retries an operation when [`Error::is_temporary`] returns `true`. If the operation still fails, the layer marks the error as `Persistent`." On stateful bodies: "Otherwise, `RetryLayer` can lose the inner body state and fail subsequent calls with an `Unexpected` error." The doc covers layer order with TimeoutLayer. It has **no read-specific caveat** about version change.
- **IMPLEMENTED, four retry points**:
  1. `Service::read` (creating the raw reader; lines 338-356).
  2. `oio::Read::open(range)` (lines 554-584).
  3. `oio::Read::read(range)`: the **whole bounded chunk is re-read** (lines 586-605). RFC-7660 (line 388): "Because `read` is an exact bounded range operation, retrying it is idempotent for the same path and read condition set."
  4. `RetryReadStream::read` (lines 636-706): counts bytes delivered (`read += buf.len()`). On a temporary stream error it drops the stream and, on the next attempt, does `range.advance(read)` and `reader.open(range)`. It **resumes from the offset** with the remaining range on the same inner reader (same `OpRead`). DOCUMENTED as the design in RFC-7660 (lines 378-386): "if a stream read fails with a temporary error, reopen the same raw reader with the remaining range and continue".
- **Bounded range fully read, then error**: the retry layer returns empty (EOF) instead of reopening. Code at lines 659-664: "Broke after the last byte: nothing is left to fetch". Test source `test_retry_read_bounded_range_does_not_reopen_at_eof` (lines 1460-1484) states "Two retries, one full read, then the error at EOF. No reopen". The temporary error is thus turned into success.
- **Guard against version change on resume**: **none** beyond caller-supplied conditions, which are re-sent because `OpRead` is reused. No If-Range and no observed-ETag pinning (IMPLEMENTED, by absence; see Q3). This is the hazard 07-C3 describes. OpenDAL does not use If-Range in the files read. INFERENCE.
- **ErrorStatus during read retries** (IMPLEMENTED):
  - `.when(|e| e.is_temporary())` controls retry.
  - Every final error passes `.map_err(|err| err.set_persistent())`, and `set_persistent` sets the status unconditionally (error.rs:409-415). A **Permanent** error, e.g. NotFound, ConditionNotMatch or the CompleteLayer short-read, therefore leaves RetryLayer marked **Persistent**, without having been retried.
  - **MISMATCH** with the ErrorStatus doc: "Persistent: The error was temporary but persisted after retries" (error.rs:165-170; 15-C3).
- **Truncation retry by origin** (INFERENCE): HTTP "too little data" (Temporary) is retried by resume. CompleteLayer "reader got too little data" (Permanent) is not retried. RetryLayer is added by the user after `Operator::new`, so it sits outside CompleteLayer. INFERENCE from layer order in builder.rs:43-50 and `.layer` composition.
- **ChunkedReader / fetch**: each chunk is a bounded `read`, so a failing chunk is re-read in full (point 3).

## Q5. Taxonomy on the read path (codes actually produced)

| Situation | S3 (`services/s3`) | GCS (`services/gcs`) | fs (`services/fs`) |
|---|---|---|---|
| 200 / 206 | both accepted as success; metadata from headers (s3 reader.rs:64-67) | both accepted (gcs reader.rs:68-74) | n/a |
| 404 | NotFound, Permanent (core.rs:2217); `NoSuchKey` maps to NotFound | NotFound, Permanent (core.rs:2260) | io NotFound gives NotFound, Permanent (std_io_util.rs:33) |
| 412 / 304 with caller condition | ConditionNotMatch, Permanent (core.rs:2218, 2301-2303) | ConditionNotMatch, Permanent (core.rs:2265-2267) | conditions Unsupported (capability) |
| 412 without caller condition | Unexpected (code-first fallback, core.rs:2237-2238) | Unexpected (core.rs:2302-2308, if reason present) | n/a |
| 416 | `InvalidRange` code gives RangeNotSatisfied, Permanent (core.rs:2300); otherwise Unexpected, Permanent | Unexpected, Permanent (no 416 arm) | n/a; past-EOF gives RangeNotSatisfied via PositionReader |
| 429 / 5xx / 499 | RateLimited / Unexpected, Temporary | RateLimited / Unexpected, Temporary | n/a |
| body short vs Content-Length | Unexpected, Temporary (HttpBody) | same | n/a |
| short vs requested bounded range | Unexpected, Permanent (CompleteLayer) | same | RangeNotSatisfied, Permanent (PositionReader) |
| io `UnexpectedEof` / `Interrupted` / other | n/a | n/a | Unexpected, Temporary (std_io_util.rs:38-39) |
| range offset > length (planned) | RangeNotSatisfied (context/read.rs:160-166), all services | | |

The parse_error tables are shared with non-read operations; track 15 (15-C5, 15-C8) already covered their code-first structure. For HTTP 206, neither S3 nor GCS checks that `Content-Range` matches the requested range. Only the byte count is checked. INFERENCE from reader code. `parse_into_metadata` reads the total from Content-Range for metadata only (header.rs:161-163).

## Mismatches (documented vs implemented)

1. **Persistent relabelling**:
   - Doc: "The error was temporary but persisted after retries" (error.rs:165-166).
   - Code: RetryLayer applies `set_persistent()` to every final error, including Permanent ones that were never retried (retry lib.rs:353, 572, 603, 705; error.rs:412-415).
   - Effect: after RetryLayer, Permanent read errors (NotFound, ConditionNotMatch, RangeNotSatisfied) report Persistent. Label: IMPLEMENTED vs DOCUMENTED.
2. **RFC-7945 `limit` not implemented at this commit**:
   - The RFC (start date 2026-07-24) specifies `ReadOptions.limit` and a private `exact` flag.
   - `ReadOptions` has no `limit` field. The only `limit` is in `ListOptions` (options.rs:131-133). A grep for "exact" in read code found nothing.
   - RFC-7945 describes `CompleteLayer::open` as "requires exactly the bytes available in a satisfiable range" when RpRead has the full length. The current `CompleteReadStream` requires the full requested size (complete.rs:290-300).
   - The RFC is in the doc tree (`docs/rfcs/mod.rs:341-342`), but its RFC status was not determined; the issue was not read.
3. **RFC-7945 on `PositionReadStream`**:
   - RFC: it "returns `RangeNotSatisfied` if its first read for a non-empty bounded range returns no bytes, but treats a later empty read as clean completion" (7945:158-161).
   - Code: it returns RangeNotSatisfied for **any** empty read while `remaining` is Some (position_read.rs:179-188). The RFC describes proposed behaviour, not current code.
4. **RFC-7945 on `open`** (7945:151-154): "an offset at or beyond EOF is `RangeNotSatisfied`". fs unbounded `open` at or past EOF returns a clean empty EOF (position_read.rs:179-189: returns `Ok(Buffer::new())` when `remaining` is None). Proposed rule vs current code.
5. **Cross-service divergence** (INFERENCE, not a doc mismatch): a bounded range crossing EOF gives RangeNotSatisfied on fs and Unexpected on S3/GCS. A 416 gives RangeNotSatisfied on S3 (with code) and Unexpected on GCS. The `RangeNotSatisfied` rustdoc does not say which.

## Relations to prior findings

- **02-C9** (Rust `Read`: `Ok(0)` = EOF; Err means no bytes read): OpenDAL's raw stream uses an empty `Buffer` as EOF, mirroring `Ok(0)`. `FuturesAsyncReader`/`StdReader` return `Ok(0)` at end. However, an error from `read_to_end` may follow bytes already copied (test at futures_async_reader.rs:876-895: content "Hell" plus an error). That matches std `read_to_end` semantics, not single-`read` semantics. INFERENCE.
- **07-C4** (Content-Length truncation detectable; close-delimited not): OpenDAL implements exactly the Content-Length check (HttpBody). It explicitly disables it when Content-Encoding is present (reqwest lib.rs:153-159), so truncation of an encoded or close-delimited body is not detected at the HTTP layer. For bounded ranges the CompleteLayer size check still applies. INFERENCE.
- **07-C3** (If-Range prevents version splicing on resume): the OpenDAL resume (RetryReadStream) uses no If-Range or automatic ETag. Splicing protection exists only if the caller passes `if_match` or `version`.
- **15-C9** (unknown io errors map to Unexpected+Temporary): confirmed again in the read path (fs `read_at`, `fs_open`). Reverse direction added here: `format_std_io_error` collapses all kinds except NotFound and PermissionDenied into `io::ErrorKind::Other` at the AsyncRead/std::io boundary.
- **15-C3** (Persistent definition): see mismatch 1.
- **15-C2** (Permanent default): explains why CompleteLayer short-read errors are not retried.
- Track 15 COVERAGE-GAP "OpenDAL Reader and stream semantics (short reads, retry after partial IO) were not read" is **closed** by this track.
- Track 15 GENUINE-GAP "no outcome class for truncated or mid-stream read failure": **confirmed** for OpenDAL at this commit, with more detail. Truncation is `Unexpected`, with status depending on which layer detects it.

## Documented limits / RFC discussions bearing on Q1-Q5

- RFC-7945 Drawbacks: "`range` and `limit` are similar size controls with different EOF semantics." Rationale: "Making every bounded range accept EOF would weaken file validation and safe concurrent chunk planning"; "Calling `stat` first adds latency and cannot make the read atomic with its metadata."
- RFC-5871 motivation: a separate stat "can also observe a different object version if the object changes between read and stat" (5871:16). Read-open metadata is the documented mitigation for metadata-vs-data skew, but not for chunk-vs-chunk skew.
- RFC-7660: raw `read` is exact by design; "Partial-read syscall semantics would push fill loops, EOF handling, retry progress ... into core and layers" (7660:523-525).
- RetryLayer doc: state loss with TimeoutLayer ordering gives an `Unexpected` "retry layer is in bad state" (retry lib.rs:39-69, 725-731).
- Issues #7938 (limited read), #7661 and #5486 are named in RFC headers. They were **not read**.

## Gaps

- **GENUINE-GAP** (within sources read): no documented or implemented version pinning across chunks, concurrent sub-reads or retry resumes. The conditional-operations spec does not address multi-request reads.
- **GENUINE-GAP**: no dedicated "content incomplete" / truncation ErrorKind. Truncation is Unexpected, with Temporary (HTTP layer) or Permanent (CompleteLayer).
- **GENUINE-GAP**: the `RangeNotSatisfied` rustdoc does not define when it is returned versus Unexpected, and services differ (Q5).
- **GENUINE-GAP**: the public `Reader::read` rustdoc does not state the exact-bounded-range rule. Only RFC-7945/7660 state it.
- **COVERAGE-GAP**: azblob, oss, http and other services were not read. The gcs `gcs_get_object_request` was read only in part.
- **COVERAGE-GAP**: no tests or builds were run. Conclusions about runtime composition (layer order, 416 bodies from real S3/GCS) are inferences from source.
- **COVERAGE-GAP**: `futures_bytes_stream.rs` and the rest of `futures_async_reader.rs` were not read in full. Neither was `ConcurrentTasks` (retry handling inside the queue is mentioned in upgrade.md line 7, not examined).
- **COVERAGE-GAP**: GitHub issues and PR discussions were not read. The RFC-7945 acceptance status is unknown.
