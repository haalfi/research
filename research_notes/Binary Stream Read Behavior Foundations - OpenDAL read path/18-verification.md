# Verification notes

Method: 3 independent verifiers per track (lenses: fidelity, overreach, currency), each re-reading the cited full text and trying to refute every claim of the track. A claim is KILLED on >=2 refutes, CONTESTED on 1 refute, VERIFIED on >=2 supports with no refute.

Result: Counter({'VERIFIED': 24})

Per-claim verdicts and all verifier qualifications:

## 17-C1 - VERIFIED (3S/0R/0U)

OpenDAL's raw oio::Read::read(range) is defined as an exact bounded read that returns the complete range or an error, not a syscall-style partial read.

- [overreach] This is a normative design statement in an RFC ("should"), not a type-level guarantee. Code enforces it in StreamReader, PositionReader and CompleteLayer. A custom oio::Read implementation is not forced to comply.

## 17-C2 - VERIFIED (3S/0R/0U)

StreamReader::read compares bytes received with the requested range size and returns ErrorKind::Unexpected on mismatch.


## 17-C3 - VERIFIED (3S/0R/0U)

The PositionRead primitive may return fewer bytes than requested, and an empty buffer signals EOF.


## 17-C4 - VERIFIED (3S/0R/0U)

PositionReadStream returns RangeNotSatisfied whenever read_at returns empty while a bounded remaining size is outstanding, including after some bytes were delivered. For an unbounded range it returns clean EOF.

- [overreach] An exhausted bounded stream (remaining == Some(0)) returns an empty buffer before read_at runs, so the error only fires when bytes are still outstanding.

## 17-C5 - VERIFIED (3S/0R/0U)

The default CompleteLayer (added in Operator::new) requires a bounded non-suffix read stream to deliver exactly the requested size. Otherwise it returns Unexpected 'reader got too little data' with no status set, i.e. Permanent.

- [overreach] A mismatch in either direction is an error: "too much data" too, not only "too little". The stream check runs only when the inner stream yields an empty buffer, so inner errors (RangeNotSatisfied from PositionReadStream, Temporary from HttpBody) surface first. If the user adds RetryLayer outside it, a Permanent error ends up marked Persistent.

## 17-C6 - VERIFIED (3S/0R/0U)

FuturesAsyncReader treats RangeNotSatisfied as EOF only for unbounded reads and propagates it for bounded reads.

- [overreach] "Unbounded" here means the stream's size is unknown. An open-ended range with the chunk option set resolves content_length and is then treated as bounded, so RangeNotSatisfied propagates.

## 17-C7 - VERIFIED (3S/0R/0U)

When OpenDAL errors are converted to std::io::Error for the AsyncRead/std::io adapters, every kind except NotFound and PermissionDenied becomes io::ErrorKind::Other.


## 17-C8 - VERIFIED (3S/0R/0U)

HttpBody checks bytes consumed against the expected size at end of stream; a short body yields Unexpected marked Temporary.

- [overreach] An oversized body is also Temporary, and no check runs when the transport did not set a size.

## 17-C9 - VERIFIED (3S/0R/0U)

The reqwest transport takes the expected body size from Content-Length, but leaves it unset for HEAD requests and for responses with Content-Encoding, so no size check runs then.

- [overreach] It is also None when the response has no Content-Length header. This applies to the reqwest transport only.

## 17-C10 - VERIFIED (3S/0R/0U)

Transport-level body read errors from reqwest are mapped to Unexpected and marked temporary when reqwest reports a request, body or decode error.


## 17-C11 - VERIFIED (3S/0R/0U)

RFC-7945 states that the bounded range in current OpenDAL is exact and fails when its end crosses EOF, and that HTTP Content-Length validation prevents a truncated response from being accepted as EOF.

- [overreach] RFC-7945 is a proposal that is not implemented at this commit (ReadOptions has no limit). Its Content-Length statement is the RFC's own assertion. In code the check is skipped when Content-Encoding is present or Content-Length is missing (reqwest transport), so it is not a universal guarantee.

## 17-C12 - VERIFIED (3S/0R/0U)

Reader::fetch independently rejects any chunk whose buffer length differs from its planned size, with ErrorKind::Unexpected.


## 17-C13 - VERIFIED (3S/0R/0U)

ReadOptions documents version as a selector (not a condition) and if_match as returning ConditionNotMatch on a different ETag or NotFound on a missing file, with Unsupported when the capability is not advertised.


## 17-C14 - VERIFIED (3S/0R/0U)

The S3 reader stores the operation's OpRead and rebuilds each GetObject (every range open) with the same versionId, If-Match and If-None-Match, so caller conditions apply to every chunk and re-open.

- [overreach] The time conditions are also re-sent. That S3 evaluates the conditions on each request is inferred from the headers being sent, not shown in the code.

## 17-C15 - VERIFIED (3S/0R/0U)

ReadContext caches only the first metadata observed from read opens; later responses from other chunks are not compared with it.


## 17-C16 - VERIFIED (3S/0R/0U)

The conditional-operations spec says read conditions check the observed file and are never silently ignored, and leaves unspecified when a conditional error surfaces. It says nothing about multi-request reads.


## 17-C17 - VERIFIED (3S/0R/0U)

RetryReadStream tracks bytes already delivered. On a temporary stream error it reopens the same raw reader with the range advanced by those bytes, so it resumes from the offset rather than re-reading.

- [overreach] This happens only for errors with is_temporary() and within the backoff budget. RetryLayer is optional, not a default layer, and the reopen response's RpRead is discarded.

## 17-C18 - VERIFIED (3S/0R/0U)

If a bounded range stream fails after its last byte, RetryLayer ends the read with EOF instead of reopening the empty remaining range.

- [overreach] This applies only when the post-last-byte failure is temporary (so the retry path runs). A permanent error after the last byte still propagates, marked Persistent.

## 17-C19 - VERIFIED (3S/0R/0U)

RFC-7660 specifies the read retry model: retry reader creation and open-before-bytes, wrap streams to track emitted bytes, reopen with the remaining range on temporary errors, and retry read(range) as an idempotent exact bounded operation.


## 17-C20 - VERIFIED (3S/0R/0U)

RetryLayer applies set_persistent() to every final read error, and set_persistent sets the status unconditionally. A Permanent error that was never retried therefore leaves the layer as Persistent, contrary to the ErrorStatus definition of Persistent.

- [overreach] This applies to all RetryLayer operations, not only reads, and only when the optional RetryLayer is installed.

## 17-C21 - VERIFIED (3S/0R/0U)

The S3 read path accepts both 200 and 206 as success and routes all other statuses to parse_error.


## 17-C22 - VERIFIED (3S/0R/0U)

S3 maps error code InvalidRange to RangeNotSatisfied (non-retryable). A status-only fallback has no 416 arm, so other 416s become Unexpected, while 404 maps to NotFound and 412/304 with a caller condition to ConditionNotMatch.

- [overreach] An S3 error-code classification overrides the status mapping (for example NoSuchBucket on a 404 becomes ConfigInvalid). A 412 with an unclassified code becomes Unexpected.

## 17-C23 - VERIFIED (3S/0R/0U)

GCS parse_error has no 416 arm, so a 416 read becomes Unexpected (non-retryable). 404 maps to NotFound, and 304/412 with a caller condition map to ConditionNotMatch.

- [overreach] A body reason of conditionNotMet also maps to ConditionNotMatch under caller_condition. The internal_condition and delete_match_condition arms come before these, but they do not apply to reads.

## 17-C24 - VERIFIED (3S/0R/0U)

The fs service reads through PositionReader using positioned read_at, maps io errors via new_std_io_error, and ignores OpRead (read conditions are rejected earlier by capability).

- [overreach] On Windows it uses seek_read rather than read_at.
