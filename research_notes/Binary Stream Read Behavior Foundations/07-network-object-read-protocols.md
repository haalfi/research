# Track 07: Network and object-storage read protocols (ranges, validators, truncation, retries)

Scope: what a client can observe when reading a byte stream over HTTP, object-storage APIs (S3, GCS, Azure Blob) and network file/block protocols (NFSv4.1, SMB2, iSCSI). Terminology is kept as each source uses it. Anything marked **[inference]** is my reading and is not a statement from the source.

Download dir (scratch, not in repo): `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/network-object-read-protocols/`

## Sources consulted (access status)

| # | Source | Type | Access | Sections read |
|---|---|---|---|---|
| S1 | RFC 9110 HTTP Semantics (2022) | normative | full text (rfc-editor .txt) | 6.1, 8.6, 8.8.1, 9.2.1, 9.2.2, 13.1.5, 14, 14.2, 14.3, 14.4, 15.3.7, 15.5.17, 15.6.4 |
| S2 | RFC 9112 HTTP/1.1 (2022) | normative | full text | 8, 9.3.1, 9.3.2, 9.8 |
| S3 | RFC 9113 HTTP/2 (2022) | normative | full text | 8.1.1, 8.7 |
| S4 | RFC 9111 HTTP Caching (2022) | normative | full text | 3.3, 3.4, 4.2.4 |
| S5 | RFC 8881 NFSv4.1 (2020) | normative | full text | 10.3, 10.3.1, 18.22.3, 18.22.4, p. near 13.10 (close-to-open) |
| S6 | MS-SMB2 §3.3.5.12 "Receiving an SMB2 READ Request" (rev. 2024-06-07) | normative (vendor open spec) | full text of section | 3.3.5.12 |
| S7 | RFC 7143 iSCSI (2014) | normative | full text (grep + section read) | SCSI Response flags (Residual Underflow/Overflow), ~line 9025 |
| S8 | AWS S3 API Reference: GetObject | implementation doc | full page | Storage classes, URI params (partNumber, Range, versionId), Response elements, Errors |
| S9 | AWS S3 API Reference: Object data type (ETag) | implementation doc | full page | ETag |
| S10 | AWS S3 User Guide: What is S3 / data consistency model | implementation doc | full page | "Amazon S3 data consistency model" |
| S11 | AWS S3 User Guide: Performance design patterns | implementation doc | full page | "Timeouts and retries for latency-sensitive applications" |
| S12 | AWS S3 User Guide: Checking object integrity | implementation doc | PARTIAL (page rendered as overview only, 62 lines) | intro; not used for claims |
| S13 | GCS docs: Consistency | implementation doc | full page | Strongly consistent ops; Cache control and consistency |
| S14 | GCS docs: Data validation and change detection with checksums | implementation doc | full page | "Checksums for data reads and downloads" |
| S15 | GCS docs: Retry strategy | implementation doc | full page | Overview of retries; Idempotency; Conditional idempotency |
| S16 | GCS docs: Object metadata (generation/metageneration) | implementation doc | full page | "Generation and metageneration numbers" |
| S17 | GCS docs: Transcoding of gzip-compressed files | implementation doc | full page | "Using the Range header" |
| S18 | GCS docs: Storage classes | implementation doc | full page | "Archive storage" |
| S19 | Azure REST: Get Blob | implementation doc | full page | x-ms-range, x-ms-range-get-content-md5/crc64, Remarks |
| S20 | Azure Blob: Rehydrate overview | implementation doc | full page | intro, Rehydration priority |
| S21 | Azure Blob: Manage concurrency | implementation doc | full page | snapshot isolation, ETag/If-Match |
| S22 | Stone & Partridge, "When the CRC and TCP Checksum Disagree", ACM SIGCOMM 2000, pp. 309-319, doi:10.1145/347059.347561 | peer-reviewed empirical | full text (conference PostScript from conferences2.sigcomm.org, crude text extraction; spacing lost) | Abstract, Section 4 (P_ue estimates) |
| - | S3 ErrorResponses page (SlowDown code list) | implementation doc | UNREACHABLE (page body empty via curl) | - |

## Extracted findings

### HTTP semantics (RFC 9110), normative

- **Range support is optional; a 200 can answer a Range request.** §14: "Range requests are an OPTIONAL feature of HTTP, designed so that recipients not implementing this feature ... can respond as if it is a normal GET request". §14.2: "A server MAY ignore the Range header field."
- **206 may cover only part of what was asked.** §14.2: "The above does not imply that a server will send all requested ranges." §15.3.7: "a server might want to send only a subset of the data requested for reasons of its own, such as temporary unavailability, cache efficiency, load balancing, etc." and "A client MUST inspect a 206 response's Content-Type and Content-Range field(s) to determine what parts are enclosed and whether additional requests are needed."
- **A 416 is not guaranteed.** §15.5.17 note: "clients cannot depend on receiving a 416 (Range Not Satisfiable) response even when it is most appropriate." A 416 SHOULD carry `Content-Range: bytes */<current length>`.
- **Accept-Ranges is advisory and says nothing about future requests.** §14.3: "a client MUST NOT assume that receiving an Accept-Ranges field means that future range requests will return partial responses. The content might change..."
- **If-Range carries version-consistent resumption.** §13.1.5: "if the representation is unchanged, send me the part(s) that I am requesting in Range; otherwise, send me the entire representation." "A client MUST NOT generate an If-Range header field containing an entity tag that is marked as weak."
- **Strong and weak validators.** §8.8.1: a strong validator "changes value whenever a change occurs to the representation data that would be observable in the content of a 200 (OK) response to GET"; "Strong validators are usable for all conditional requests, including cache validation, partial content ranges ... Weak validators are only usable when the client does not require exact equality". A one-second Last-Modified can be weak "if it is possible for the representation to be modified twice during a single second".
- **Completeness depends on framing.** §6.1: "A message is considered 'complete' when all of the octets indicated by its framing are available. ... a response message that is ended by the underlying connection's close is considered complete even though it might be indistinguishable from an incomplete response, unless a transport-level error indicates that it is not complete."
- **Safe and idempotent.** §9.2.1: GET, HEAD, OPTIONS and TRACE are safe. §9.2.2: idempotent methods "can be repeated automatically if a communication failure occurs before the client is able to read the server's response"; "even if the original request succeeded, though the response might differ." The property "only applies to what has been requested by the user".
- **503.** §15.6.4: "temporary overload or scheduled maintenance"; MAY send Retry-After; "Some servers might simply refuse the connection."

### HTTP/1.1 (RFC 9112), normative

- §8: "A client that receives an incomplete response message, which can occur when a connection is closed prematurely or when decoding a supposedly chunked transfer coding fails, MUST record the message as incomplete." A chunked body is incomplete without the zero-sized chunk. A Content-Length body is incomplete "if the size of the message body received (in octets) is less than the value given by Content-Length". A body delimited only by close is "considered complete unless an error was indicated by the underlying connection (e.g., an 'incomplete close' in TLS ...)".
- §9.8: TLS "incomplete close ... could indicate that subsequent data might have been truncated. As TLS is not directly aware of HTTP message framing, it is necessary to examine the HTTP data itself"; "A response that has neither chunked transfer coding nor Content-Length is complete only if a valid closure alert has been received."
- §9.3.1: "Connections can be closed at any time, with or without intention."

### HTTP/2 (RFC 9113), normative

- §8.1.1: a message is malformed "if the value of a content-length header field does not equal the sum of the DATA frame payload lengths"; "Clients MUST NOT accept a malformed response." This is treated as a stream error (PROTOCOL_ERROR).
- §8.7: GOAWAY and REFUSED_STREAM "guarantee to a client that a request has not been processed"; "Requests that have not been processed have not failed; clients MAY automatically retry them, even those with non-idempotent methods."

### HTTP caching (RFC 9111), normative

- §3.3: a cache MAY store an incomplete 200 response if it is recorded as incomplete. "A cache MUST NOT send a partial response to a client without explicitly marking it using the 206 (Partial Content) status code."
- §3.4: a cache MAY combine ranges "if they all share the same strong validator".
- §4.2.4: "A cache MUST NOT generate a stale response unless it is disconnected or doing so is explicitly permitted by the client or origin server". So a stale read is possible under max-stale, RFC 5861 extensions or out-of-band contracts.

### NFSv4.1 (RFC 8881), normative

- §18.22.3: "If offset is greater than or equal to the size of the file, the status NFS4_OK is returned with a data length set to zero and eof is set to TRUE." "The server may choose to return fewer bytes than specified by the client. The client needs to check for this condition".
- §18.22.4: "If the server returns a 'short read' (i.e., fewer data than requested and eof is set to FALSE), the client should send another READ". Causes: truncation "by another client or perhaps on the server itself", reduced transfer size, "Server resource exhaustion". Delegation conflicts give NFS4ERR_DELAY. Mandatory lock conflicts give NFS4ERR_LOCKED.
- §10.3.1: cached data "must be revalidated after doing an OPEN" using the change attribute. "any cache validation approach by the client MUST include the use of the change attribute" because time_modify "is guaranteed to change only at the granularity of the time_delta attribute".
- pNFS section (around the start of 13.11): "The NFSv4.1 protocol only provides close-to-open file data cache semantics". Also: "if the READ response indicates EOF and/or contains fewer bytes than requested, the client will interpret such a response as a hole in the file, and the NFS client will substitute zeroes".

### SMB2 (MS-SMB2 §3.3.5.12), normative vendor spec

- "If the underlying object store returns fewer bytes than specified by the MinimumCount field of the request, the server MUST fail the request with STATUS_END_OF_FILE." Otherwise DataLength is set to the number of bytes returned, capped at Length. "If the read is not finished in 0.5 milliseconds, the server MUST send an interim response". The status list includes STATUS_END_OF_FILE, STATUS_FILE_LOCK_CONFLICT, STATUS_CANCELLED, STATUS_NETWORK_SESSION_EXPIRED and others.

### iSCSI (RFC 7143), normative

- SCSI Response flag U: "Residual Underflow. In this case, the Residual Count indicates the number of bytes that were not transferred out of the number of bytes that were expected to be transferred." O (overflow) and U are mutually exclusive.

### Amazon S3 (implementation docs)

- GetObject, Storage classes: for Glacier Flexible Retrieval, Glacier Deep Archive and Intelligent-Tiering Archive/Deep Archive Access, "you must first restore a copy using RestoreObject. Otherwise, this operation returns an InvalidObjectState error." Errors: "InvalidObjectState: Object is archived and inaccessible until restored. ... HTTP Status Code: 403".
- Range: "Amazon S3 doesn't support retrieving multiple ranges of data per GET request." partNumber "Effectively performs a 'ranged' GET request for the part specified."
- A missing object returns 404 or 403 depending on s3:ListBucket permission. A versionId that names a delete marker returns 405.
- The response-element description of `accept-ranges` reads "Indicates that a range of bytes was specified in the request." This wording differs from the RFC 9110 §14.3 meaning (advertised range-unit support). Noted as a terminology discrepancy.
- Object.ETag (S9): "The ETag may or may not be an MD5 digest of the object data"; objects from Multipart Upload or Part Copy have an ETag that "is not an MD5 digest, regardless of the method of encryption".
- Consistency (S10): "Updates to a single key are atomic. ... you will get either the old data or the new data, but never partial or corrupt data." "Any read (GET or LIST request) that is initiated following the receipt of a successful PUT response will return the data written by the PUT request." Bucket configurations are eventually consistent.
- 503 (S11): "If an application generates high request rates (typically sustained rates of over 5,000 requests per second to a small number of objects), it might receive HTTP 503 slowdown responses." While S3 scales internally "you will receive HTTP 503 request responses temporarily". The guidance is to retry the slowest 5%/1% of requests, use a new connection and a fresh DNS lookup, and back off (2 s, then 4 s).

### Google Cloud Storage (implementation docs)

- Consistency (S13): "you never receive a 404 Not Found response or stale data for an object read-after-write". If an unreplicated dual- or multi-region location is unavailable: "attempts to access the object return a retryable 500 error response." "Cached objects that are publicly readable might not exhibit strong consistency." Default cache lifetime is up to 60 minutes.
- Read checksums (S14): "Server-side checksums are based on the complete object as it's stored ... the following types of downloads can't be validated against server-supplied checksums: Downloads that undergo decompressive transcoding ... A response that contains only a portion of the object data". The exception is gRPC ranged reads, which carry "a unique CRC32C checksum inside every individual response chunk". A mismatch "indicates that the data was corrupted in transit ... discard the corrupted data and ... retry". MD5 is not available for composite objects.
- Transcoding (S17): "if the request for the object includes a Range header, that header is silently ignored ... you still receive the entire 10 GB object."
- Generation (S16): "An object version's generation value is unique"; "Generation numbers might not increase for future versions".
- Retry (S15): retryable responses are "HTTP 408, 429, and 5xx response codes" and "Socket timeouts and TCP disconnects". "All get and list requests" are "Always idempotent". Some mutations are "Conditionally idempotent" with ifGenerationMatch/etag.
- Archive class (S18): "Unlike the 'coldest' storage services offered by other Cloud providers, your data is available within milliseconds, not hours or days." This contrasts with S3 and Azure, where an archived object is not readable.

### Azure Blob (implementation docs)

- Get Blob (S19): x-ms-range-get-content-md5/crc64 return a hash for the range only when it is "less than or equal to 4 MiB". Above that: "400 (Bad Request)". Content-MD5 on a ranged read returns the whole-blob MD5 in a separate header, which "might or might not be equal" to the range's Content-MD5. Page blob: unwritten or cleared pages "returns zeros for those bytes". "A Get Blob operation is allowed two minutes per MiB to be completed ... the operation will time out." "A Get Blob operation on an archived block blob will fail."
- Rehydrate (S20): "An archived blob is offline and can't be read or modified." Standard priority "might take up to 15 hours"; the account limit is 10 GiB/hour for priority retrieval.
- Concurrency (S21): "Azure Storage uses snapshot isolation to allow read operations concurrently with write operations within a single partition. Snapshot isolation guarantees that all read operations return a consistent snapshot of the data even while updates are occurring." The ETag "is updated every time a write operation is performed on an object". A mismatched If-Match returns 412.

### Peer-reviewed empirical evidence

- S22 Stone & Partridge (SIGCOMM 2000), Abstract: "between 1 packet in 1,100 and 1 packet in 32,000 fails the TCP checksum, even on links where link-level CRCs should catch all but 1 in 4 billion errors"; "the checksum will fail to detect errors for roughly 1 in 16 million to 10 billion packets"; "the highly non-random distribution of errors strongly suggests some applications should employ application-level checksums or equivalents." Section 4: "It suggests that some hosts could regularly be accepting bad TCP data." (Spacing was restored by hand from the PostScript extraction.)

## Existing models and classifications found (source terminology)

1. **RFC 9110 validator strength model**: strong vs weak validators, with conditions on use (ranges and If-Range need strong validators).
2. **RFC 9110 method property classes**: safe ⊂ idempotent. These are a contract about requested semantics, not about side effects.
3. **RFC 9110/9112 message completeness model**: complete or incomplete, judged by framing (Content-Length, chunked terminator, close-delimited, TLS closure alert).
4. **RFC 9113 "not processed" guarantee**: GOAWAY and REFUSED_STREAM.
5. **RFC 9111 freshness model**: fresh, stale, validation; incomplete stored responses.
6. **NFSv4.1 close-to-open cache consistency**, plus the READ result triple (status, eof, data length) and the short-read definition.
7. **GCS idempotency classes**: Always, Conditionally, Never idempotent.
8. **Online vs offline (archived) tiers**: S3 InvalidObjectState/RestoreObject and Azure rehydration, versus GCS Archive "available within milliseconds".
9. **iSCSI residual model**: Residual Underflow / Overflow flags with Residual Count.

## Convergences

- In HTTP, NFSv4.1 and iSCSI, "fewer bytes than requested" is legal and is signalled in band: 206 + Content-Range, eof=FALSE short read, Residual Underflow. The client must inspect the response. SMB2 differs: the client can set MinimumCount, and falling below it turns a short read into STATUS_END_OF_FILE.
- Version consistency across separate reads needs a strong validator or version identifier: If-Range + strong ETag (RFC 9110), the change attribute (NFS), generation (GCS), versionId or ETag (S3), ETag (Azure).
- Reads are classed as safe or idempotent and retryable in RFC 9110 and the GCS docs. However, "the response might differ" (RFC 9110 §9.2.2), so a retry can return a different version.

## Contradictions and tensions

- RFC 9110 §14.3 defines Accept-Ranges as advertising range-unit support. The S3 GetObject doc describes `accept-ranges` as "Indicates that a range of bytes was specified in the request."
- Archive semantics differ: S3 and Azure archive tiers are offline and fail reads (403 InvalidObjectState / failure), while GCS Archive is online with millisecond access.
- RFC 9110 lets a server send multipart/byteranges for multiple ranges. S3 does not support multiple ranges per GET.
- End-to-end checksum coverage of ranged reads differs: GCS HTTP ranged reads cannot be validated against the stored checksum (gRPC can). Azure supplies a per-range MD5/CRC64 only for ranges of 4 MiB or less. S3 range-checksum behavior was not established here (S12 partial).
- RFC 9110 permits close-delimited responses to be "complete" even when indistinguishable from truncation. HTTP/2 makes a content-length mismatch a hard malformed-message error. Truncation detectability therefore depends on the HTTP version and framing.
- Transport integrity: the HTTP RFCs presume "a reliable transport" (RFC 9112 §9). Stone & Partridge measure an undetected-error rate of roughly 1 in 16M to 10B packets for TCP checksums. **[inference]** The "reliable transport" assumption is an abstraction, not a guarantee of bit-exactness. The TLS record MAC would change this, but this track did not read it.

## Gaps

- COVERAGE-GAP: S3 checksum behavior on ranged GET / ChecksumMode (checking-object-integrity page only partly rendered). S3 ErrorResponses page (SlowDown code) unreachable via curl.
- COVERAGE-GAP: TLS 1.3 (RFC 8446) record integrity and its relation to truncation; RFC 9110 §14.6 multipart/byteranges details; RFC 9110 §13.2.2 precondition evaluation order; RFC 9114 HTTP/3.
- COVERAGE-GAP: MS-SMB2 client-side read processing and the 2.2.19 request structure (MinimumCount semantics on the client side); NFSv3 (RFC 1813) READ.
- GENUINE-GAP (as far as this track found): no peer-reviewed measurement of how often object-store reads return truncated or mismatched-version data in practice; evidence is vendor documentation.
- GENUINE-GAP: no cross-protocol normative model of "mid-stream version change". Each protocol handles it locally (If-Range, change attribute, snapshot isolation, single-key atomicity).
