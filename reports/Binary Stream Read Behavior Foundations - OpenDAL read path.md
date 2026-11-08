# Binary Stream Read Behavior Foundations - OpenDAL read path

A follow-up on the topic "Binary Stream Read Behavior Foundations". Earlier reports, left unchanged:
- `reports/Binary Stream Read Behavior Foundations.md`
- `reports/Binary Stream Read Behavior Foundations - transfer protocols.md`, whose track 15 found OpenDAL's taxonomy **CONFIRMED**.

The brief is `briefs/Binary Stream Read Behavior Foundations - OpenDAL read path.md`. Track notes and the verification record are in `research_notes/Binary Stream Read Behavior Foundations - OpenDAL read path/`. Date: 2026-11-08.

This report describes what Apache OpenDAL documents and implements on its read path. It does not judge the design and does not propose a taxonomy. As the brief agreed, retry is treated as a *mechanism* and retryability as an *attribute of an outcome*.

---

## 0. Method and scope

**What was studied.** One track (17) read the official documentation, the RFCs and specifications in the repository, and the source code of `apache/opendal`.

- It pinned commit **`532050ac3c099dd8591cde652a8ed1aaf03ba418`**, and all line numbers refer to that commit.
- Every finding is labelled **DOCUMENTED** (rustdoc, RFC or spec contract), **IMPLEMENTED** (code behaviour), or both.
- Places where the two disagree are listed in §2.

**Coverage.**
- **Services:** S3, GCS and local fs.
- **Behaviour derived from source only:** nothing was built and no tests were run.

**Verification.** Three verifiers checked every claim against the source, one each for fidelity, overreach and currency.
- Result: 24 claims, all verified, none contested or killed.
- Most claims carry corrections. The narrative uses the corrected reading.
- Sources: 11, of which 5 were read in full and 6 in part. The parts read are the relevant functions or sections; the matrix gives line numbers.

**Conventions.** `[17-Cn]` refers to §5 of this report. IDs from other tracks (02-, 07-, 15-) refer to the earlier reports.

---

## 1. Findings by question

### Q1 Read API and reader contract

**Raw exact read.** RFC-7660 defines the raw `oio::Read::read(range)` as "not a syscall-style partial read". For a valid bounded range it "should either return the complete range content or return an error" [17-C1]. This is a design rule ("should"), not a guarantee enforced by the types. The code enforces it in three places:
- `StreamReader` returns Unexpected "reader got unexpected data size" when the size differs [17-C2];
- `PositionReader`;
- `CompleteLayer`.

A custom `oio::Read` implementation is not forced to comply. *DOCUMENTED and IMPLEMENTED.*

**Positioned primitive.** `PositionRead::read_at` "may return fewer bytes", and "returning an empty buffer means EOF" [17-C3]. `PositionReadStream` turns an empty read while bytes of a bounded range are still outstanding into **RangeNotSatisfied**, even after some bytes were delivered. For an unbounded range the same empty read is a clean EOF [17-C4]. *DOCUMENTED (trait) and IMPLEMENTED (stream).*

**Public bounded reads are exact by default.** The default `CompleteLayer`, installed in `Operator::new`, requires a bounded, non-suffix read to deliver exactly the requested size [17-C5]:
- too little data gives Unexpected "reader got too little data" with no status set, i.e. **Permanent**;
- too much data is also an error;
- the check runs only when the inner stream ends, so an inner error such as RangeNotSatisfied or a Temporary HTTP error surfaces first;
- suffix and unbounded ranges are not size-checked.

`Reader::fetch` also rejects any chunk whose length differs from its planned size [17-C12]. *IMPLEMENTED.* The rule is restated only in RFC-7945 and is **not documented in the public `Reader::read` rustdoc** (gap G-4).

**End-of-data in adapters.**
- On the raw stream an empty `Buffer` means EOF.
- `FuturesAsyncReader` and `StdReader` return `Ok(0)` at EOF.
- They treat RangeNotSatisfied as EOF *only* for unbounded reads, where "unbounded" means the size is unknown. A range given the chunk option resolves its length and is then treated as bounded [17-C6].
- When errors are converted to `std::io::Error`, every kind except NotFound and PermissionDenied becomes `io::ErrorKind::Other` [17-C7].

*DOCUMENTED (rustdoc) and IMPLEMENTED.*

**Ranges beyond the object size.** Behaviour differs by service *(inference from code)*:

| Service | Bounded range crossing EOF | HTTP 416 |
|---|---|---|
| fs | RangeNotSatisfied [17-C4] | — |
| S3 | Unexpected, via CompleteLayer | RangeNotSatisfied only with the `InvalidRange` error code [17-C22] |
| GCS | Unexpected, via CompleteLayer | Unexpected; `parse_error` has no 416 arm [17-C23] |

No behaviour test covering past-EOF or empty-object ranges was found (track 17).

### Q2 Truncation detection

There are three independent checks, all *IMPLEMENTED*.

1. **HTTP body against Content-Length.**
   - `HttpBody` compares the bytes consumed with the expected size when the stream ends. A short or oversized body gives **Unexpected, Temporary** [17-C8].
   - The reqwest transport takes the expected size from Content-Length. It leaves the size unset, so **no check runs**, for HEAD requests, for responses with Content-Encoding, and for responses without Content-Length [17-C9]. This applies to the reqwest transport only.
   - Transport body, request and decode errors are mapped to Unexpected, Temporary [17-C10].
2. **Delivered bytes against the requested bounded range:** `CompleteLayer` (Permanent) [17-C5], `StreamReader` [17-C2] and `Reader::fetch` [17-C12].
3. **Early end on positioned reads:** `PositionReadStream` returns RangeNotSatisfied [17-C4].

**Documentation.** RFC-7945 says HTTP Content-Length validation prevents a truncated response being accepted as EOF [17-C11]. RFC-7945 is a *proposal not implemented at this commit*, and the code skips the check in the cases above.

**No dedicated class for truncation.** No ErrorKind marks "content incomplete". Truncation shows up as Unexpected:
- **Temporary** if `HttpBody` detects it, so the optional `RetryLayer` will retry;
- **Permanent** if `CompleteLayer` detects it, so it will not be retried [17-C5, 17-C8].

The retryability of the same phenomenon therefore depends on **which layer detects it**. A std::io `UnexpectedEof` maps to Unexpected, Temporary (15-C9).

### Q3 Version consistency across a read

**Read options.** `ReadOptions` offers:
- `version`, which *selects* a version rather than testing a condition;
- `if_match` and `if_none_match`;
- `if_version_match` and `if_version_not_match`;
- `if_modified_since` and `if_unmodified_since`.

Each option is capability-gated and gives Unsupported if the backend does not advertise it. `if_match` returns ConditionNotMatch on a different ETag and NotFound on a missing file [17-C13]. *DOCUMENTED.*

**Propagation.** The S3 reader keeps the `OpRead` and sends the same versionId and conditions, the time-based ones included, on every range open, so caller conditions cover all chunks and every re-open [17-C14]. That S3 evaluates them on each request is inferred from the headers sent. GCS behaves similarly (track 17). *IMPLEMENTED.*

**No automatic pinning.**
- `ReadContext` caches only the *first* metadata it observes, through a `OnceLock`, and later chunks are not compared with it [17-C15].
- The conditional-operations specification says read conditions check the observed file and are "never silently ignored". It leaves open when a conditional error surfaces and says nothing about reads that span several requests [17-C16].
- *Inference:* without caller-supplied `if_match` or `version`, chunks and resumed segments of one logical read can come from different object versions. This is the splicing risk that HTTP addresses with `If-Range` (07-C3).

### Q4 Retry inside reads (mechanism)

**When RetryLayer applies.** `RetryLayer` is **optional, not a default layer**. It retries only errors with `is_temporary()`, within its backoff budget.
- It retries `Service::read`, `Read::open`, and `Read::read`, the last by re-reading the whole bounded chunk.
- RFC-7660 documents this design [17-C19].

**Resume from offset.**
- `RetryReadStream` counts the bytes already delivered. On a temporary stream error it reopens the same raw reader with the range advanced by that count, so it resumes from the offset rather than starting over [17-C17].
- The resumed request carries the original `OpRead`, so only caller conditions apply. There is **no `If-Range` and no automatic ETag guard** *(inference, 17-C14)*.
- If a bounded range had already been fully delivered when a temporary error arrives, the read ends with EOF instead of reopening an empty range. A permanent error at that point still propagates [17-C18].

**How truncation interacts with retry.**
- An HTTP short body is Temporary, so it is resumed from the offset.
- A `CompleteLayer` short read is Permanent, so it is not retried [17-C5, 17-C8, 17-C17].

**How retryability is relabelled.** `RetryLayer` applies `set_persistent()` to *every* final error, and `set_persistent` sets the status unconditionally. A Permanent error that was never retried therefore leaves the layer marked **Persistent**. The `ErrorStatus` definition says Persistent means "temporary but persisted after retries" (15-C3), so this contradicts it [17-C20]. The relabelling applies to all `RetryLayer` operations, not only reads.

### Q5 How the taxonomy is applied on the read path

**S3 [17-C21, 17-C22].**
- Success: both 200 and 206 count as success, and only byte counts are checked; Content-Range is not.
- 404 maps to NotFound. A recognised S3 error code overrides the status mapping, for example NoSuchBucket becomes ConfigInvalid (15-C8).
- 304 or 412 with a caller condition maps to ConditionNotMatch. A 412 with an unclassified code becomes Unexpected.
- 416 with `InvalidRange` maps to RangeNotSatisfied; any other 416 becomes Unexpected.
- 429 maps to RateLimited and 5xx to Unexpected, both Temporary (track 17 notes).

**GCS [17-C23].**
- 404 maps to NotFound.
- 304 or 412 with a caller condition, or the body reason `conditionNotMet`, maps to ConditionNotMatch.
- 416 maps to Unexpected.

**Local fs [17-C24].**
- Reads go through `PositionReader`, using positioned `read_at`, or `seek_read` on Windows.
- An early end gives RangeNotSatisfied.
- io errors pass through `new_std_io_error`, which keeps NotFound and PermissionDenied and maps UnexpectedEof, Interrupted and other errors to Unexpected, Temporary (15-C9).
- Read conditions are rejected earlier by the capability check.

**Documentation of RangeNotSatisfied.** The rustdoc for RangeNotSatisfied is generic and does not document these per-service differences (gap G-3).

---

## 2. Mismatches between documentation and implementation

| # | Documented | Implemented | Evidence |
|---|---|---|---|
| M1 | `ErrorStatus::Persistent`: "temporary but persisted after retries" (error.rs:165–166) | `RetryLayer` marks every final error Persistent, Permanent ones included | [17-C20] |
| M2 | RFC-7945 specifies `ReadOptions.limit` and a private exact flag | No `limit` field in `ReadOptions` at this commit; RFC-7945 is a proposal | [17-C11]; track notes |
| M3 | RFC-7945: a later empty read in `PositionReadStream` is a clean completion | An empty read while a bounded size is outstanding gives RangeNotSatisfied | [17-C4] |
| M4 | RFC-7945: opening at or beyond EOF gives RangeNotSatisfied | An unbounded fs open past EOF returns a clean empty EOF | [17-C4] |
| M5 | RFC-7945: `CompleteLayer::open` requires the bytes available in a satisfiable range | `CompleteReadStream` requires the full requested size | [17-C5] |
| M6 | RFC-7945: Content-Length validation prevents truncation being accepted as EOF | The check is skipped with Content-Encoding or without Content-Length (reqwest) | [17-C9, 17-C11] |
| — | *(not a doc mismatch)* Per-service divergence | A bounded range crossing EOF is RangeNotSatisfied on fs but Unexpected on S3/GCS; a 416 is RangeNotSatisfied on S3 (with `InvalidRange`) but Unexpected on GCS | [17-C4, 17-C22, 17-C23] *(inference)* |

M2–M6 compare the code against a proposal RFC whose acceptance status is unknown (gap C-4), so they may describe an intended future rather than a defect.

---

## 3. Relation to earlier findings

- **Closes** the track 15 coverage gap: OpenDAL's reader and stream semantics had not been read.
- **Confirms** the track 15 genuine gap (no outcome class for truncated or mid-stream read failure) for OpenDAL. It adds that the retryability of a truncation depends on the detecting layer (Q2).
- **Qualifies 15-C3.** The documented meaning of Persistent is not preserved by `RetryLayer` (M1).
- **Explains 15-C2 in use.** Permanent is the default status, which is why `CompleteLayer` short reads are not retried.
- **Reconfirms 15-C9** on the fs read path. The reverse conversion, `format_std_io_error`, collapses most kinds into `io::ErrorKind::Other` [17-C7]. The distinction between end of stream and unexpected end that 02-C9/02-C10 describe for Rust is lost in both directions at this boundary.
- **Shows 07-C4 implemented.** OpenDAL implements the Content-Length truncation check that RFC 9112 makes possible, but only where Content-Length is present and no Content-Encoding is applied.
- **Contrasts with 07-C3.** HTTP's `If-Range` guards against splicing versions on resume. OpenDAL's resume uses no such guard; protection exists only through caller `if_match`/`version` *(inference)*.
- **Adds an OpenDAL instance to D.1-4 of the first report** ("partial results are usually successful"). OpenDAL's public bounded read does the opposite of POSIX: a short result is an error, not a success. Only the raw `PositionRead` primitive and the read-buffer adapters use the POSIX-style short read.

---

## 4. Knowledge gaps

**Gaps in OpenDAL's own documentation and design** (as read):
- **G-1** No documented or implemented pinning of a version or ETag across chunks, concurrent sub-reads, or resumes after retry. The conditional-operations specification does not cover reads that span several requests.
- **G-2** No dedicated ErrorKind for truncation or "content incomplete". Truncation becomes Unexpected, Temporary or Permanent depending on the detector.
- **G-3** The RangeNotSatisfied rustdoc does not define when it applies versus Unexpected, and fs, S3 and GCS differ.
- **G-4** The public `Reader::read` rustdoc does not state the exact-bounded-range rule. Only RFC-7945 and RFC-7660 do.

**Gaps in this research's coverage:**
- **C-1** azblob and other services were not read, and GCS's `gcs_get_object_request` was read only in part.
- **C-2** No builds or tests were run, so how the layers compose at runtime and what real 416 bodies look like are inferred from source.
- **C-3** `futures_bytes_stream.rs`, the rest of `futures_async_reader.rs`, and retry handling in `ConcurrentTasks` were not read.
- **C-4** GitHub issues #7938, #7661 and #5486 and the related PR discussions were not read, so the acceptance status of RFC-7945 is unknown.

---

## 5. Evidence and provenance matrix

The columns and codes are the same as in the earlier reports. *Finding* shows the claim as extracted, and the narrative uses the corrected reading. The full per-lens record is in `research_notes/Binary Stream Read Behavior Foundations - OpenDAL read path/18-verification.md`.

| ID | Finding (as extracted) | Source and locator | Type | Verification | Applicability | Qualifications from verification |
|---|---|---|---|---|---|---|
| **17** | **Apache OpenDAL read path** | | | | | |
| 17-C1 | OpenDAL's raw oio::Read::read(range) is defined as an exact bounded read that returns the complete range or an error, not a syscall-style partial read. | RFC-7660 move_read_range_to_reader, lines 222-226 (Range operation semantics). <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/7660_move_read_range_to_reader.md> | I | VERIFIED (3S/0R/0U) | Q1 | [overreach] This is a normative design statement in an RFC ("should"), not a type-level guarantee. Code enforces it in StreamReader, PositionReader and CompleteLayer. A custom oio::Read implementation is not forced to comply. |
| 17-C2 | StreamReader::read compares bytes received with the requested range size and returns ErrorKind::Unexpected on mismatch. | core/core/src/raw/oio/read/stream_read.rs, StreamReader::read, lines 59-75. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/raw/oio/read/stream_read.rs> | G | VERIFIED (3S/0R/0U) | Q1/Q2 |  |
| 17-C3 | The PositionRead primitive may return fewer bytes than requested, and an empty buffer signals EOF. | core/core/src/raw/oio/read/position_read.rs, PositionRead trait doc, lines 28-33. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/raw/oio/read/position_read.rs> | I | VERIFIED (3S/0R/0U) | Q1 |  |
| 17-C4 | PositionReadStream returns RangeNotSatisfied whenever read_at returns empty while a bounded remaining size is outstanding, including after some bytes were delivered. For an unbounded range it returns clean EOF. | core/core/src/raw/oio/read/position_read.rs, PositionReadStream::read, lines 179-189. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/raw/oio/read/position_read.rs> | G | VERIFIED (3S/0R/0U) | Q1/Q5 (fs) | [overreach] An exhausted bounded stream (remaining == Some(0)) returns an empty buffer before read_at runs, so the error only fires when bytes are still outstanding. |
| 17-C5 | The default CompleteLayer (added in Operator::new) requires a bounded non-suffix read stream to deliver exactly the requested size. Otherwise it returns Unexpected 'reader got too little data' with no status set, i.e. Permanent. | core/core/src/layers/complete.rs and types/operator/builder.rs, CompleteReader::open lines 290-300; check_complete lines 350-367; builder.rs lines 43-50. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/layers/complete.rs> | G | VERIFIED (3S/0R/0U) | Q1/Q2 | [overreach] A mismatch in either direction is an error: "too much data" too, not only "too little". The stream check runs only when the inner stream yields an empty buffer, so inner errors (RangeNotSatisfied from PositionReadStream, Temporary from HttpBody) surface first. If the user adds RetryLayer outside it, a Permanent error ends up marked Persistent. |
| 17-C6 | FuturesAsyncReader treats RangeNotSatisfied as EOF only for unbounded reads and propagates it for bounded reads. | core/core/src/types/read/futures_async_reader.rs, struct doc lines 42-43; is_unbounded_eof_error lines 105-107. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/types/read/futures_async_reader.rs> | I | VERIFIED (3S/0R/0U) | Q1 | [overreach] "Unbounded" here means the stream's size is unknown. An open-ended range with the chunk option set resolves content_length and is then treated as bounded, so RangeNotSatisfied propagates. |
| 17-C7 | When OpenDAL errors are converted to std::io::Error for the AsyncRead/std::io adapters, every kind except NotFound and PermissionDenied becomes io::ErrorKind::Other. | core/core/src/raw/std_io_util.rs, format_std_io_error, lines 57-65. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/raw/std_io_util.rs> | G | VERIFIED (3S/0R/0U) | Q1/Q5 |  |
| 17-C8 | HttpBody checks bytes consumed against the expected size at end of stream; a short body yields Unexpected marked Temporary. | core/core/src/types/http_transport/body.rs, HttpBody::check, lines 114-134; ReadStream::read lines 137-148. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/types/http_transport/body.rs> | G | VERIFIED (3S/0R/0U) | Q2 | [overreach] An oversized body is also Temporary, and no check runs when the transport did not set a size. |
| 17-C9 | The reqwest transport takes the expected body size from Content-Length, but leaves it unset for HEAD requests and for responses with Content-Encoding, so no size check runs then. | core/http-transports/reqwest/src/lib.rs, fetch, lines 150-159. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/http-transports/reqwest/src/lib.rs> | G | VERIFIED (3S/0R/0U) | Q2 | [overreach] It is also None when the response has no Content-Length header. This applies to the reqwest transport only. |
| 17-C10 | Transport-level body read errors from reqwest are mapped to Unexpected and marked temporary when reqwest reports a request, body or decode error. | core/http-transports/reqwest/src/lib.rs, HttpBody::new map_err lines 189-200; is_temporary_error lines 226-234. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/http-transports/reqwest/src/lib.rs> | G | VERIFIED (3S/0R/0U) | Q2/Q5 |  |
| 17-C11 | RFC-7945 states that the bounded range in current OpenDAL is exact and fails when its end crosses EOF, and that HTTP Content-Length validation prevents a truncated response from being accepted as EOF. | RFC-7945 limited_read, Motivation lines 25-28; Raw read contract lines 169-170. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/7945_limited_read.md> | I | VERIFIED (3S/0R/0U) | Q1/Q2 | [overreach] RFC-7945 is a proposal that is not implemented at this commit (ReadOptions has no limit). Its Content-Length statement is the RFC's own assertion. In code the check is skipped when Content-Encoding is present or Content-Length is missing (reqwest transport), so it is not a universal guarantee. |
| 17-C12 | Reader::fetch independently rejects any chunk whose buffer length differs from its planned size, with ErrorKind::Unexpected. | core/core/src/types/read/reader.rs, push_fetch_output, lines 287-298. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/types/read/reader.rs> | G | VERIFIED (3S/0R/0U) | Q2 |  |
| 17-C13 | ReadOptions documents version as a selector (not a condition) and if_match as returning ConditionNotMatch on a different ETag or NotFound on a missing file, with Unsupported when the capability is not advertised. | core/core/src/types/options.rs, ReadOptions, lines 171-191. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/types/options.rs> | I | VERIFIED (3S/0R/0U) | Q3 |  |
| 17-C14 | The S3 reader stores the operation's OpRead and rebuilds each GetObject (every range open) with the same versionId, If-Match and If-None-Match, so caller conditions apply to every chunk and re-open. | core/services/s3/src/reader.rs and core.rs, S3Reader fields lines 30-37, open lines 50-60; core.rs s3_get_object_request lines 573-603. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services/s3/src/reader.rs> | G | VERIFIED (3S/0R/0U) | Q3/Q4 | [overreach] The time conditions are also re-sent. That S3 evaluates the conditions on each request is inferred from the headers being sent, not shown in the code. |
| 17-C15 | ReadContext caches only the first metadata observed from read opens; later responses from other chunks are not compared with it. | core/core/src/types/context/read.rs, observe_read_response, lines 107-114 (OnceLock field line 41). <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/types/context/read.rs> | G | VERIFIED (3S/0R/0U) | Q3 |  |
| 17-C16 | The conditional-operations spec says read conditions check the observed file and are never silently ignored, and leaves unspecified when a conditional error surfaces. It says nothing about multi-request reads. | core/core/src/docs/specs/conditional-operations.md, lines 16, 33-35, 126-129. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/specs/conditional-operations.md> | N | VERIFIED (3S/0R/0U) | Q3 |  |
| 17-C17 | RetryReadStream tracks bytes already delivered. On a temporary stream error it reopens the same raw reader with the range advanced by those bytes, so it resumes from the offset rather than re-reading. | core/layers/retry/src/lib.rs, RetryReadStream::read, lines 636-706. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/layers/retry/src/lib.rs> | G | VERIFIED (3S/0R/0U) | Q4 | [overreach] This happens only for errors with is_temporary() and within the backoff budget. RetryLayer is optional, not a default layer, and the reopen response's RpRead is discarded. |
| 17-C18 | If a bounded range stream fails after its last byte, RetryLayer ends the read with EOF instead of reopening the empty remaining range. | core/layers/retry/src/lib.rs, lines 659-664; test test_retry_read_bounded_range_does_not_reopen_at_eof lines 1460-1484. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/layers/retry/src/lib.rs> | G | VERIFIED (3S/0R/0U) | Q4 | [overreach] This applies only when the post-last-byte failure is temporary (so the retry path runs). A permanent error after the last byte still propagates, marked Persistent. |
| 17-C19 | RFC-7660 specifies the read retry model: retry reader creation and open-before-bytes, wrap streams to track emitted bytes, reopen with the remaining range on temporary errors, and retry read(range) as an idempotent exact bounded operation. | RFC-7660 move_read_range_to_reader, Retry layer section, lines 372-389. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/7660_move_read_range_to_reader.md> | I | VERIFIED (3S/0R/0U) | Q4 |  |
| 17-C20 | RetryLayer applies set_persistent() to every final read error, and set_persistent sets the status unconditionally. A Permanent error that was never retried therefore leaves the layer as Persistent, contrary to the ErrorStatus definition of Persistent. | core/layers/retry/src/lib.rs and core/core/src/types/error.rs, retry lib.rs lines 353, 572, 603, 705; error.rs set_persistent lines 409-415, ErrorStatus::Persistent lines 165-170. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/layers/retry/src/lib.rs> | G | VERIFIED (3S/0R/0U) | Q4 (mismatch) | [overreach] This applies to all RetryLayer operations, not only reads, and only when the optional RetryLayer is installed. |
| 17-C21 | The S3 read path accepts both 200 and 206 as success and routes all other statuses to parse_error. | core/services/s3/src/reader.rs, S3Reader::open, lines 62-72. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services/s3/src/reader.rs> | G | VERIFIED (3S/0R/0U) | Q5 (S3) |  |
| 17-C22 | S3 maps error code InvalidRange to RangeNotSatisfied (non-retryable). A status-only fallback has no 416 arm, so other 416s become Unexpected, while 404 maps to NotFound and 412/304 with a caller condition to ConditionNotMatch. | core/services/s3/src/core.rs, parse_error lines 2215-2225; parse_s3_error_code line 2300. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services/s3/src/core.rs> | G | VERIFIED (3S/0R/0U) | Q5 (S3) | [overreach] An S3 error-code classification overrides the status mapping (for example NoSuchBucket on a 404 becomes ConfigInvalid). A 412 with an unclassified code becomes Unexpected. |
| 17-C23 | GCS parse_error has no 416 arm, so a 416 read becomes Unexpected (non-retryable). 404 maps to NotFound, and 304/412 with a caller condition map to ConditionNotMatch. | core/services/gcs/src/core.rs, parse_error, lines 2256-2273. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services/gcs/src/core.rs> | G | VERIFIED (3S/0R/0U) | Q5 (GCS) | [overreach] A body reason of conditionNotMet also maps to ConditionNotMatch under caller_condition. The internal_condition and delete_match_condition arms come before these, but they do not apply to reads. |
| 17-C24 | The fs service reads through PositionReader using positioned read_at, maps io errors via new_std_io_error, and ignores OpRead (read conditions are rejected earlier by capability). | core/services/fs/src/backend.rs and reader.rs, backend.rs read lines 208-213, read_at lines 280-283; reader.rs read_at lines 64-84. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services/fs/src/backend.rs> | G | VERIFIED (3S/0R/0U) | Q5 (fs) | [overreach] On Windows it uses seek_read rather than read_at. |

---

## 6. Sources

Access status: *read in full*, or *partially read* (the relevant functions or sections; see the locators in §5).

### H.17 Apache OpenDAL read path

- **Apache OpenDAL source at commit 532050ac (core/core/src/types/read/*, types/context/read.rs, raw/oio/read/*, layers/complete.rs, layers/correctness_check.rs, types/http_transport/body.rs, raw/std_io_util.rs, types/error.rs, types/options.rs, types/operator/{operator,builder}.rs)**. <https://github.com/apache/opendal/tree/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src>. *read in full*. Sections: files and line ranges listed in notes. Public Reader API, raw read contract, default layers, truncation checks, EOF handling, error conversion
- **OpenDAL RetryLayer (core/layers/retry/src/lib.rs)**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/layers/retry/src/lib.rs>. *partially read*. Sections: lines 31-800, tests 1250-1484. Read retry points, resume-from-offset, Persistent marking
- **OpenDAL reqwest HTTP transport**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/http-transports/reqwest/src/lib.rs>. *partially read*. Sections: lines 135-235. Content-Length source for HttpBody check, temporary classification of body errors
- **OpenDAL services s3, gcs, fs (reader.rs, core.rs, backend.rs)**. <https://github.com/apache/opendal/tree/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/services>. *partially read*. Sections: S3Reader/GcsReader/FsReader; parse_error; get_object_request. Per-service status/error mapping on the read path and condition propagation
- **OpenDAL spec: Conditional operations**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/specs/conditional-operations.md>. *read in full*. Sections: whole. Normative condition contract for read
- **OpenDAL RFC-7945 limited_read**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/7945_limited_read.md>. *read in full*. Sections: whole. States the exact bounded-range rule, EOF and RangeNotSatisfied semantics, Content-Length validation; proposed limit not implemented
- **OpenDAL RFC-7660 move_read_range_to_reader**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/7660_move_read_range_to_reader.md>. *partially read*. Sections: Summary, Range operation semantics, Retry layer, Rationale. Exact raw read, retry model for reads
- **OpenDAL RFC-5871 read_returns_metadata**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/5871_read_returns_metadata.md>. *partially read*. Sections: lines 16, 84-95, 205-216. First-observed metadata cache; stat/read version skew motivation
- **OpenDAL RFC-5485 conditional_reader**. <https://github.com/apache/opendal/blob/532050ac3c099dd8591cde652a8ed1aaf03ba418/core/core/src/docs/rfcs/5485_conditional_reader.md>. *read in full*. Sections: whole. History of read conditions
- **docs.rs opendal-core 0.59.5 Reader**. <https://docs.rs/opendal-core/latest/opendal_core/struct.Reader.html>. *read in full*. Sections: Reader methods. Confirms published rustdoc matches HEAD for read/fetch/metadata/into_futures_async_read
- **opendal.apache.org Rust docs Reader**. <https://opendal.apache.org/docs/rust/opendal/struct.Reader.html>. *partially read*. Sections: n/a. Reached; same doc strings present; not read in detail
