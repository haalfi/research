# Track 01: verification of external-run points and open caveats

Accessed 2026-10-26. Each point below was checked by the lead researcher against the full text of a primary source.

Labels:
- **[doc]**: documented in the source.
- **[src]**: read in source at the stated release tag.
- **[inf]**: inference.

Inputs:
- A ChatGPT run on the identical brief, pasted by the user.
- A Perplexity answer on S3 ETag vs MD5, pasted by the user.
- The caveats section of the first report (branch `research/remote-store-v1-operation-catalogue`).

## A. Points from the ChatGPT run: confirmed

| # | Claim | Source | Result |
|---|---|---|---|
| A1 | OpenDAL Python 0.47.12 still exposes `remove_all` and `scan`. `presign_*` exists only on `AsyncOperator`. `check()` exists on both | https://raw.githubusercontent.com/apache/opendal/v0.59.5/bindings/python/python/opendal/operator.pyi. `AsyncOperator` L34 to 713: `check` L71, `presign_delete/read/stat/write` L309 to 426, `remove_all` L533, `scan` L567. `Operator` L714+: `check` L751, `remove_all` L1024, `scan` L1046, no `presign_*` | **confirmed [src]**. The binding version is 0.47.12 per `bindings/python/Cargo.toml` at the same tag (notes 04 of the first run) |
| A2 | The OpenDAL conditional-operations spec forbids silently dropping a condition | https://opendal.apache.org/docs/specifications/conditional-operations/ ("Last updated on Aug 31, 2026") | **confirmed [doc]**. Verbatim: "OpenDAL never silently ignores a condition." "If it cannot preserve the complete conjunction, it returns Unsupported instead of dropping a condition." "A service advertises a mutation condition only when it can evaluate the condition atomically with the mutation's visible commit. An implementation must not emulate a conditional mutation by issuing stat followed by an unconditional mutation." "For staged or multipart writes, the service evaluates the condition at the final commit. If the condition fails, the previously visible file remains unchanged." "The point at which an operation surfaces a conditional error is unspecified … while constructing an I/O handle, during I/O, or when closing the handle." "Protocol status codes do not determine the error kind on their own" (412/304 map to `ConditionNotMatch` only in response to an explicit condition). "Deleting a file that does not exist remains a successful no-op." "A conditional batch delete evaluates every entry independently." Metadata contract: a service that advertises ETag or version matching "must populate the corresponding Metadata field", and the returned token "must be usable as input to a later matching condition". Conformance: a service "must pass the relevant portable behavior tests before advertising a conditional capability". Historical RFCs: 5485 Conditional Reader, 7818 Rename If Not Exists, 8145 Conflict Error Kind, 8147 Write If Not Changed |
| A3 | object_store ignores unsupported tags and errors on unsupported attributes | https://raw.githubusercontent.com/apache/arrow-rs-object-store/v0.14.2/src/lib.rs L1946 to 1952 and L2018 to 2024 | **confirmed [src/doc comment]**. "Implementations that don't support object tagging should ignore this" (`tags`). "Implementations that don't support an attribute should return an error" (`attributes`). Two policies for unsupported options sit in one struct |
| A4 | fsspec has append mode, `checksum` and `ukey` | https://raw.githubusercontent.com/fsspec/filesystem_spec/2026.9.0/fsspec/spec.py: `AbstractBufferedFile` accepts `{"ab","rb","wb","xb"}` (L1984); `AbstractFileSystem.checksum` L766, `ukey` L1453 | **confirmed [src]**. The base accepts `ab`; whether a backend implements it is up to the backend. **s3fs emulates append** (`_VALID_FILE_MODES` includes `ab`, L127). For existing objects it HEADs the object, and below 5 MiB it downloads and re-uploads (https://raw.githubusercontent.com/fsspec/s3fs/2026.9.0/s3fs/core.py L2597+) [src]. This is a rewrite, not a native append |
| A5 | gocloud `Bucket` implements `io/fs` | https://pkg.go.dev/gocloud.dev/blob@v0.47.0: "*blob.Bucket implements io/fs.FS and io/fs.SubFS, so it can be used with functions in those packages." | **confirmed [doc]**. This fills the OP-17 cell for gocloud, which the first report had as "—" |
| A6 | "Conditional read" and "post-write metadata/property update" are separate intents | Evidence was already in the first run's notes 03 (S3 GetObject If-Match/If-None-Match/If-(Un)Modified-Since; Azure Get Blob conditions; GCS generation preconditions; Azure `set_blob_metadata` replaces all; GCS `patch` in place; S3 metadata immutable except by copy) and notes 05 (object_store `GetOptions{if_match, version}`; OpenDAL `read_with_if_match`) | **confirmed [doc]**. Count conditional read: OpenDAL, object_store, boto3, Azure, GCS = 5/10. Count post-write update: Azure, GCS natively; S3 only for tags (user metadata via copy-replace); s3fs `setxattr` = copy [src]. That is 2/10 native and 3/10 for tags or properties |

## B. Corrections to the ChatGPT run: confirmed

| # | ChatGPT statement | Check | Result |
|---|---|---|---|
| B1 | azure-storage-blob 12.30.2, google-cloud-storage 3.14.1 | PyPI JSON: azure-storage-blob **12.31.0** (2026-09-30T21:23:24), google-cloud-storage **3.17.1** (2026-10-15T17:49:27) | ChatGPT pinned versions that are not the latest |
| B2 | GCS move = "~ rewrite+delete" | https://raw.githubusercontent.com/googleapis/python-storage/main/CHANGELOG.md L218: "Add Bucket.move_blob() for HNS-enabled buckets (#1431)". It is in an older release section (well before 3.14). Later move_blob fixes at L101 and L183 | `move_blob` predates 3.14.1. The first report's atomic `objects.move` (notes 03, G11) stands |
| B3–B10 | pyarrow move ungated, cloudpathlib `mkdir` writes a marker, pyarrow user metadata ✓, presign 6/10, object_store scoping "~", fsspec FS close, GCS conditional retry only, Q5 posed as questions | First run notes 02 ([obs] moto, [src]), 03, 04, 06. fsspec close: AST of `spec.py` 2026.9.0 shows `close` only on `AbstractBufferedFile` (L2270), not on `AbstractFileSystem` [src] | The first report's position stands |

## C. S3 ETag vs MD5 (Perplexity point): confirmed and extended

- https://docs.aws.amazon.com/AmazonS3/latest/API/API_Object.html [doc]:
  - "The ETag may or may not be an MD5 digest of the object data."
  - PUT/POST/Copy/Console with SSE-S3 or plaintext → MD5. With SSE-C or SSE-KMS → not MD5.
  - Multipart Upload or Part Copy → "not an MD5 digest, regardless of the method of encryption".
  - The Console uses multipart above 16 MB.
  - "Directory buckets - MD5 is not supported by directory buckets."
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity-upload.html (WebFetch) [doc]:
  - Multipart ETag construction: "Amazon S3 calculates the MD5 digest of each individual part … concatenates the bytes for the MD5 digests together and then calculates the MD5 digest of these concatenated values … adds a dash with the total number of parts to the end." The `-N` construction is now verified.
  - "the ETag only reflects changes to the content of an object, not changes to its metadata."
  - Copying a multipart object with CopyObject makes the checksum "a direct checksum of the full object", so "the checksum value changes even though the data doesn't".
  - Full-object checksums for multipart uploads exist only for CRC64NVME, CRC32 and CRC32C. Without a checksum, S3 attaches CRC64NVME by default.
  - "AWS SDKs do not automatically calculate MD5 checksums" (checking-object-integrity.html).
- The MinIO points are not verified and not used: their sources are vendor marketing, and MinIO is not a comparable.

## D. Open caveats from the first report

| Caveat | Check | Result |
|---|---|---|
| Azure `retry_total` default: README 10 vs Learn 3 | azure-storage-blob 12.31.0 source (tag `azure-storage-blob_12.31.0`): `_shared/policies.py` `StorageRetryPolicy.__init__` uses `kwargs.pop("retry_total", 10)` (L516); `ExponentialRetry.__init__(retry_total: int = 3, …)` (L720); `_shared/base_client.py` L506 `config.retry_policy = kwargs.get("retry_policy") or ExponentialRetry(**kwargs)` | **Resolved [src]: the default client retry policy is `ExponentialRetry` with `retry_total=3`.** The README's 10 is the base-class default and does not apply unless a caller builds `StorageRetryPolicy` directly [inf] |
| pyarrow S3 copy > 5 GB | https://raw.githubusercontent.com/apache/arrow/apache-arrow-26.0.0/cpp/src/arrow/filesystem/s3fs.cc: copy uses a single `CopyObjectRequest` (L2394 to 2416); there is no `UploadPartCopy` (only the comment "XXX Investigate UploadPartCopy?", L3468) | **Resolved [src + inf]:** pyarrow uses only single-request CopyObject, so S3's documented 5 GB CopyObject limit applies. Not run against S3 |
| Exact fsspec 2023.9.0 glob change | https://raw.githubusercontent.com/fsspec/filesystem_spec/2023.9.0/docs/source/changelog.rst, section 2023.9.0 | **Still unverified**: the section lists no glob item. adlfs's compatibility note remains the only evidence |
| S3 range past EOF (416), S3 DeleteObject missing key (204) | API_GetObject page (curl, 200): the Range text gives no 416 or InvalidRange statement | **Still unverified** on S3 pages |
| S3 error-code strings | not retried | still unreachable |
