# Track 03: Vendor Python SDKs (boto3 / azure-storage-blob / google-cloud-storage)

Scope: test the draft remote-store v1 operation catalogue (OP-01..OP-24) against the three vendor
Python SDKs. remote-store's own code and docs were not consulted.

Conventions:
- [documented] = stated in a primary doc page fetched in full on 2026-10-26 (access date for all links below).
- [observed] = seen in the fetched artefact itself (e.g. a method name in a reference page's method list,
  a version string in PyPI JSON). No code was run against live services.
- [inference] = my reasoning, not stated by a source.
- [unreachable] = tried, not obtainable.
- "advisory" marks the only non-factual notes; no semantic proposals are made.

## 1. Sources and versions

SDK versions (PyPI JSON API `https://pypi.org/pypi/<pkg>/json`, fetched 2026-10-26) [observed]:

| Package | Latest version | Upload time (UTC) |
|---|---|---|
| boto3 | 1.43.118 | 2026-10-22 |
| botocore | 1.43.118 | 2026-10-22 |
| s3transfer | 0.19.3 | 2026-10-19 |
| aioboto3 (third party, author Terri Cain, github.com/terricain/aioboto3) | 15.5.0 | 2025-10-30 |
| azure-storage-blob | 12.31.0 | 2026-09-30 |
| azure-storage-file-datalake | 12.26.0 | 2026-09-30 |
| azure-core | 1.41.0 | 2026-05-07 |
| google-cloud-storage | 3.17.1 | 2026-10-15 |
| google-api-core | 2.43.0 | 2026-10-22 |

Doc pages (all fetched in full with curl on 2026-10-26; "latest" pages, versions as rendered on the page):

AWS / boto3
- [A1] S3 conditional requests overview: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-requests.html
- [A2] Conditional writes: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html
- [A3] Conditional deletes: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-deletes.html
- [A4] API DeleteObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html
- [A5] API PutObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html
- [A6] API CopyObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html
- [A7] API GetObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
- [A8] Object key naming: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
- [A9] Object metadata: https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html
- [A10] What is S3 (consistency model section): https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
- [A11] Directory bucket differences: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-differences.html
- [A12] API ListObjectsV2: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html
- [A13] API DeleteObjects: https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObjects.html
- [A14] Copy/move/rename guide: https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html
- [A15] Multipart upload overview: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html
- [A16] API RenameObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_RenameObject.html
- [A17] boto3 S3 client reference (method list), page header "Boto3 1.43.118": https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
- [A18] boto3 put_object / delete_object / copy / rename_object / close pages: `.../reference/services/s3/client/{put_object,delete_object,copy,rename_object,close}.html`
- [A19] boto3 retries guide: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html
- [A20] boto3 error handling guide: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
- [A21] botocore Config reference: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
- [A22] boto3 S3 customizations (TransferConfig/S3Transfer): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html
- [unreachable] S3 error code list https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html (#ErrorCodeList) and ErrorCodeList.html: both return a meta-refresh to Welcome.html / page-not-found on 2026-10-26. S3 error-code strings below (e.g. `PreconditionFailed`, `InvalidRange`) are therefore NOT verified against the list.

Azure
- [Z1] Naming and referencing containers, blobs, metadata: https://learn.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata
- [Z2] Conditional headers for Blob service: https://learn.microsoft.com/en-us/rest/api/storageservices/specifying-conditional-headers-for-blob-service-operations
- [Z3] BlobClient (Python): https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python
- [Z4] ContainerClient: https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python
- [Z5] BlobServiceClient: https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobserviceclient?view=azure-python
- [Z6] azure.storage.blob package (generate_blob_sas etc.): https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python
- [Z7] Properties and metadata (8 KB): https://learn.microsoft.com/en-us/rest/api/storageservices/setting-and-retrieving-properties-and-metadata-for-blob-resources
- [Z8] Put Blob / Put Block / Get Blob / Delete Blob / Copy Blob / Copy Blob From URL / List Blobs / Blob Batch REST pages: `https://learn.microsoft.com/en-us/rest/api/storageservices/{put-blob,put-block,get-blob,delete-blob,copy-blob,copy-blob-from-url,list-blobs,blob-batch}`
- [Z9] Blob service error codes: https://learn.microsoft.com/en-us/rest/api/storageservices/blob-service-error-codes
- [Z10] Retry policy (Python): https://learn.microsoft.com/en-us/azure/storage/blobs/storage-retry-policy-python
- [Z11] Managing concurrency: https://learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage
- [Z12] azure.core.exceptions: https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions?view=azure-python ; MatchConditions: https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.matchconditions?view=azure-python
- [Z13] azure-storage-blob 12.31.0 README (PyPI JSON `description`): https://pypi.org/project/azure-storage-blob/12.31.0/
- [Z14] DataLakeFileClient / DataLakeDirectoryClient: https://learn.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake.datalakefileclient?view=azure-python and `...datalakedirectoryclient...`
- [Z15] Data Lake Path - Create (rename): https://learn.microsoft.com/en-us/rest/api/storageservices/datalakestoragegen2/path/create ; Path - Delete: `.../path/delete`
- [Z16] Hierarchical namespace overview: https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace

Google Cloud
- [G1] Objects (naming): https://cloud.google.com/storage/docs/objects
- [G2] Consistency: https://cloud.google.com/storage/docs/consistency
- [G3] Retry strategy: https://cloud.google.com/storage/docs/retry-strategy
- [G4] Request preconditions: https://cloud.google.com/storage/docs/request-preconditions
- [G5] Python "Configuring Timeouts and Retries" (3.17.1 latest): https://cloud.google.com/python/docs/reference/storage/latest/retry_timeout
- [G6] Class Blob (3.17.1): https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob
- [G7] Class Bucket (3.17.1): https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.bucket.Bucket
- [G8] Class Client (3.17.1): https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.client.Client
- [G9] Class Batch (3.17.1): https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.batch.Batch ; JSON batch doc: https://cloud.google.com/storage/docs/batch
- [G10] Quotas & limits: https://cloud.google.com/storage/quotas
- [G11] Copy, rename, move objects: https://cloud.google.com/storage/docs/copying-renaming-moving-objects ; JSON objects.move: https://cloud.google.com/storage/docs/json_api/v1/objects/move
- [G12] Rename HNS folders: https://cloud.google.com/storage/docs/rename-hns-folders
- [G13] Composing objects: https://cloud.google.com/storage/docs/composing-objects
- [G14] Listing objects: https://cloud.google.com/storage/docs/listing-objects
- [G15] google-api-core exceptions (version not stated on page): https://googleapis.dev/python/google-api-core/latest/exceptions.html
- [G16] storage.retry module: https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.retry ; ObjectContexts: `.../google.cloud.storage.blob.ObjectContexts` ; storage classes: https://cloud.google.com/storage/docs/storage-classes

## 2. Per-SDK OP mapping

Legend for "gated": a feature that exists only for some bucket/account type or setting.

| OP | boto3 (S3 client) | azure-storage-blob (+ datalake) | google-cloud-storage | Gated? |
|---|---|---|---|---|
| OP-01 read whole/streamed | `get_object` (StreamingBody); `download_fileobj` [A17][A22] | `BlobClient.download_blob()` -> `StorageStreamDownloader` [Z3] | `Blob.download_as_bytes`, `download_to_file`, `Blob.open("rb")` [G6] | no |
| OP-02 range read | `get_object(Range="bytes=a-b")` [A7] | `download_blob(offset, length)` [Z3] | `download_as_bytes(start, end)` ("last byte in a range", i.e. inclusive end) [G6] | no |
| OP-03 write whole/streamed | `put_object`; managed `upload_file`/`upload_fileobj` (multipart above `multipart_threshold`, default 8 MiB) [A22] | `upload_blob` (single PUT up to `max_single_put_size` default 64 MiB, else chunked blocks) [Z3] | `upload_from_file/filename/string`, `Blob.open("wb")`, resumable session [G6] | no |
| OP-04 replace atomically | PUT on a key is atomic: readers see old or new, never partial [A10] [documented] | Put Blob overwrites; Put Block List commits staged blocks [Z8]; atomic visibility [inference from block commit model] | Object write; strong read-after-write [G2]; atomicity of upload finalize [inference] | no |
| OP-05 conditional write | `put_object(IfNoneMatch="*" / IfMatch=etag)`; also CopyObject, CompleteMultipartUpload [A2] | `upload_blob(overwrite=False)` -> ResourceExistsError; `etag`+`match_condition` kwargs [Z3] | `if_generation_match=0` (absent) / `=<gen>` (unchanged) [G4][G6] | no (S3: SigV4 required [A2]) |
| OP-06 list children | `list_objects_v2(Prefix, Delimiter="/")` [A12] | `ContainerClient.walk_blobs(delimiter="/")`, `list_blobs`, `list_blob_names` [Z4]; HNS: `get_paths(recursive=False)` [Z14] | `Bucket.list_blobs(prefix, delimiter="/")` -> `prefixes` [G7] | no |
| OP-07 walk subtree (depth) | `list_objects_v2(Prefix)` without delimiter = full subtree; no depth limit param [A12] | `list_blobs(name_starts_with)`; HNS `get_paths(recursive=True)` [Z4][Z14]; no depth param [observed absence] | `list_blobs(prefix)` (no delimiter) [G7]; no depth param | depth limit absent in all 3 [observed absence] |
| OP-08 match pattern | prefix only (`Prefix`, `StartAfter`) [A12] | prefix only (`name_starts_with`); `find_blobs_by_tags` filters on tags, not names [Z4][Z5] | server-side `match_glob=` on `list_blobs` [G7]; also `start_offset`/`end_offset` | GCS only server-side glob |
| OP-09 inspect | `head_object`; `get_object_attributes` [A17] | `get_blob_properties`, `exists` [Z3] | `Blob.reload`, `Blob.exists`, `Bucket.get_blob` [G6][G7] | no |
| OP-10 delete item | `delete_object` [A4] | `delete_blob` [Z3] | `Blob.delete` / `Bucket.delete_blob` [G6][G7] | no |
| OP-11 delete tree | none native; list + `delete_objects` (<=1000 keys/request) [A13] | flat: list + `delete_blobs` (Blob Batch <=256 subrequests) [Z4][Z8]; HNS: `delete_directory` (Path-Delete recursive, may need continuation) [Z14][Z15] | list + `delete_blobs` / `Batch` (<=100 calls) [G7][G9]; HNS folders via separate `storage_control_v2` [G12] | Azure HNS only native |
| OP-12 move/rename | GP buckets: copy+delete ("Rename objects by copying them and deleting the original ones") [A14]; `rename_object` only directory buckets in S3 Express One Zone [A16] | flat: `start_copy_from_url` + `delete_blob` [inference: no rename method in BlobClient list [Z3]]; HNS: `rename_file` / `rename_directory` [Z14] | `Bucket.move_blob` atomic (objects.move) [G7][G11]; `Bucket.rename_blob` = copy+delete [G7]; HNS folder rename via `storage_control_v2.rename_folder` [G12] | S3 Express only; Azure HNS only |
| OP-13 copy within store | `copy_object` (<=5 GB atomic), managed `copy()` (multipart copy) [A6][A18] | `start_copy_from_url` (async, copy_status pending/success), `upload_blob_from_url` (sync, Copy Blob From URL up to 256 MiB per [Z8]) | `Bucket.copy_blob`, `Blob.rewrite` (token loop) [G7][G6] | no |
| OP-14 local disk transfer | `upload_file` / `download_file` (s3transfer) [A22] | `upload_blob(open(...))`, `download_blob().readinto()` [Z13]; DataLake `upload_data` | `upload_from_filename`, `download_to_filename`; `transfer_manager` [G6] | no |
| OP-15 between stores | `copy(..., SourceClient=)` S3->S3 only [A18] | `start_copy_from_url` from any URL readable via SAS/public (incl. other accounts) [Z3] | `Bucket.copy_blob(destination_bucket=)`, `Blob.rewrite` (GCS->GCS) [G7] | intra-vendor only |
| OP-16 scope to folder | none (prefix by convention) | `ContainerClient` is container-scoped; HNS `DataLakeDirectoryClient` / `get_sub_directory_client` [Z4][Z14] | `Bucket` bucket-scoped; no prefix-scoped object | partial |
| OP-17 hand to other libs | StreamingBody file-like; [inference] no fsspec in SDK | `StorageStreamDownloader.readinto`, `chunks()` [Z3] | `Blob.open()` -> `BlobReader`/`BlobWriter` (file-like, `google.cloud.storage.fileio`) [G6][G8 nav] | no |
| OP-18 capability query | none | `get_account_information` (sku/account kind incl. HNS flag) [Z3][Z4] [method observed; return fields not verified] | `Bucket.reload` exposes bucket config (HNS, versioning) [inference] | no SDK has a feature-capability API |
| OP-19 create empty folder | zero-byte `key/` object (console convention) [A8] | flat: none (virtual dirs); HNS: `create_directory`, `create_sub_directory` [Z14] | flat: none; HNS: folders API `storage_control_v2` (separate package) [G12]; `move` auto-creates parent folders [G11] | HNS only |
| OP-20 user metadata | `Metadata=` on put/copy; immutable after upload except by copy [A9] | `metadata=` on upload; `set_blob_metadata` (replace all) [Z3][Z7] | `Blob.metadata` + `patch()` (in place) [G6] | no |
| OP-21 lifecycle close | `client.close()` "Closes underlying endpoint connections" [A18] | clients are context managers with `close()`; aio clients async CMs [Z13] | `Client.close()` "Close the client and clear any cached metadata or active connections" [G8] | no |
| OP-22 native address | `s3://bucket/key` [inference: SDK has no URL parser]; presign gives https | `BlobClient.url`, `from_blob_url` [Z3] | `gs://` via `Blob.from_uri` [inference; not checked in this fetch], `Blob.public_url` [inference] | – |
| OP-23 native handle | boto3 client | Blob/Container/ServiceClient | Client/Bucket/Blob | – |
| OP-24 health check | `head_bucket` [A17] | `ContainerClient.exists`, `get_account_information` [Z4] | `Client.lookup_bucket` / `Bucket.exists` [G7][G8] | no dedicated health API in any [observed absence] |

## 3. Operations with no catalogue entry (count of the 3 SDKs offering each)

| Uncovered capability | boto3 | Azure | GCS | Count | Use case |
|---|---|---|---|---|---|
| Presigned / SAS / signed URL | `generate_presigned_url`, `generate_presigned_post` [A17] | `generate_blob_sas`, `generate_container_sas`, `generate_account_sas` (module functions) [Z6] | `Blob.generate_signed_url`, `Bucket.generate_signed_url` [G6][G7] | 3/3 | delegate access to browsers/third parties |
| Append | `put_object(WriteOffsetBytes=)`, directory buckets in Availability Zones only (not Local Zones) [A5][A11][A18] | append blobs `create_append_blob`/`append_block`/`seal_append_blob`; DataLake `append_data`+`flush_data` [Z3][Z14] | no append method in Blob 3.17.1 reference [observed absence]; GCS "appendable objects" not checked | 2/3 | logs, streaming writers |
| Batch delete | `delete_objects` (<=1000 keys, quiet/verbose) [A13] | `ContainerClient.delete_blobs` (Blob Batch, <=256 subrequests; also batch Set Blob Tier) [Z4][Z8] | `Bucket.delete_blobs`, `Client.batch()` (<=100 calls; no upload/download in batch) [G9] | 3/3 | bulk cleanup / OP-11 implementation |
| Object versions + list versions | `list_object_versions`, `VersionId` params [A17] | `version_id=` kwargs; `list_blobs(include=[... 'versions' ...])` [Z3][Z4] (include list partly read) | `generation=`, `list_blobs(versions=True)` [G7] | 3/3 (S3 not on directory buckets [A11]) | history, recovery, pinned reads |
| Tags (separate from metadata) | `put/get/delete_object_tagging`; max 10 tags [A9] | `set_blob_tags`/`get_blob_tags`, `find_blobs_by_tags`, max 10 tags [Z3][Z5] | no tags; `ObjectContexts` (custom key-value "object contexts") exists in 3.17.1 [G16] | 2/3 (+GCS analog) | indexing, policy, lifecycle filters |
| Annotations (up to 1 MB per annotation) | `put/get/list/delete_object_annotation` [A9][A17] | – | – | 1/3 | large attached payloads without rewriting object |
| Leases | – | `acquire_lease` (BlobLeaseClient), finite 15-60 s or infinite [Z3][Z11]; DataLake `acquire_lease` | – | 1/3 | pessimistic locking |
| Object lock / retention / legal hold | `put/get_object_retention`, `put/get_object_legal_hold` [A17] | `set_immutability_policy`, `delete_immutability_policy`, `set_legal_hold` [Z3] | `Blob.retention`, `temporary_hold`, `event_based_hold` [G6] | 3/3 (S3 not on directory buckets [A11]) | WORM compliance |
| Restore from archive tier | `restore_object` [A17] | rehydrate via `set_standard_blob_tier(..., rehydrate_priority=)` [Z3] | n/a: classes have "no offline data retrieval", ms latency [G16] | 2/3 | cold data access |
| Storage class / tier change | via `copy_object(StorageClass=)` (x-amz-storage-class) [A6]; no in-place op [observed absence] | `set_standard_blob_tier`, `set_premium_page_blob_tier` [Z3] | `Blob.update_storage_class` (rewrite) [G6] | 3/3 | cost management |
| Compose / block list | multipart + `upload_part_copy` [A17] | `stage_block`, `stage_block_from_url`, `commit_block_list`, `get_block_list` [Z3] | `Blob.compose` (1-32 sources) [G13] | 3/3 | server-side concat, parallel upload |
| Multipart management (list/abort incomplete) | `list_multipart_uploads`, `list_parts`, `abort_multipart_upload`; lifecycle AbortIncompleteMultipartUpload [A15][A17] | per-blob `get_block_list("uncommitted")`; uncommitted blocks garbage-collected on commit, <=100,000 uncommitted [Z8 put-block]; `list_blobs(include='uncommittedblobs')` | no list/abort methods on Client/Bucket/Blob [observed absence]; lifecycle `LifecycleRuleAbortIncompleteMultipartUpload` class exists [G8 nav] | 1/3 full, 2 partial | cost leak cleanup |
| Server-side checksums | `ChecksumAlgorithm=` CRC32/CRC32C/SHA1/SHA256/CRC64NVME/SHA512/MD5/XXHASH64/XXHASH3/XXHASH128 [A18 put_object]; `request_checksum_calculation`/`response_checksum_validation` config [A21] | `validate_content` 'auto'/'crc64'/'md5' ("checksum ... is NOT stored with the blob"); `ContentSettings.content_md5` stored [Z3] | `checksum="auto"/"crc32c"/"md5"` on upload/download; `crc32c`, `md5_hash` properties; `DataCorruption` exception [G6] | 3/3 | integrity |
| System properties (content-type, cache-control...) | put/copy params `ContentType`, `CacheControl` [A9] | `ContentSettings`, `set_http_headers` [Z3] | `content_type`, `cache_control` + `patch` [G6] | 3/3 | HTTP serving |
| ACLs | `put/get_object_acl` [A17] | flat: none per blob (container access policy only) [observed absence in [Z3]]; HNS: `set_access_control(_recursive)` [Z14] | `Blob.acl`, `make_public/private` [G6] | 3/3 (Azure HNS only per-path) | sharing |
| Undelete (soft delete) | none direct [observed absence]; versioning delete markers [A4] | `undelete_blob` [Z3]; `undelete_container` [Z5] | `Bucket.restore_blob` (soft delete), `list_blobs(soft_deleted=True)` [G7] | 2/3 | accident recovery |
| Atomic rename | `rename_object` (S3 Express One Zone directory buckets only) [A16] | `rename_file`, `rename_directory` (HNS) [Z14][Z15] | `move_blob` (objects.move, atomic, same bucket) [G11]; HNS `rename_folder` (long-running op) [G12] | 3/3, all gated or bucket-scoped | job commit |
| Query in place | `select_object_content` (not on directory buckets [A11]) | `query_blob` [Z3]; DataLake `query_file` | – | 2/3 | filter CSV/JSON server-side |
| Snapshots | – | `create_snapshot` [Z3] | – | 1/3 | point-in-time copies |
| Abort async copy | – | `abort_copy` [Z3] | – | 1/3 | cancel long copy |
| Conditional on tags | – | `if_tags_match_condition` kwarg [Z3] | – | 1/3 | tag-guarded writes |
| File expiry | – | DataLake `set_file_expiry` [Z14] | – | 1/3 | TTL |

## 4. Conditional operations matrix

Status codes per vendor docs; SDK exception per SDK docs.

| Operation | S3 (boto3) | Azure | GCS |
|---|---|---|---|
| Write if absent | PutObject / CopyObject / CompleteMultipartUpload `If-None-Match: *` -> 412 [A2] | `upload_blob(overwrite=False)` -> ResourceExistsError [Z3]; REST If-None-Match `*` "fail the operation if it does exist" [Z2]; error code BlobAlreadyExists 409 [Z9] | `if_generation_match=0`: only "if no live version" else 412 [G4][G6] |
| Write if unchanged | `If-Match: <etag>` on the same 3 APIs; 412 on mismatch; 404 if object deleted concurrently [A2] | `etag=` + `match_condition=MatchConditions.IfNotModified` [Z3][Z12]; REST If-Match -> 412 [Z2] | `if_generation_match=<gen>`, `if_metageneration_match` -> 412 [G4] |
| Conflict under concurrency | 409 ConditionalRequestConflict; "On a 409 failure you should retry the upload" (PutObject); CompleteMultipartUpload must restart whole MPU [A2][A5] | – | – |
| Conditional read | GetObject/HeadObject If-Match/If-None-Match/If-Modified-Since/If-Unmodified-Since; 304/412 [A7] | Get Blob / Get Blob Properties accept combinations of all four; 304/412 [Z2] | `if_generation_match`, `if_metageneration_match` etc.; HTTP If-Match/If-None-Match for reads (XML) [G4] |
| Conditional copy | dest If-Match/If-None-Match + `x-amz-copy-source-if-*` (4 headers) [A6] | `source_etag`/`source_match_condition`, `source_if_modified_since` + dest conditions [Z3] | dest generation preconditions + `if_source_generation_match` etc. [G4][G7] |
| Conditional delete | `If-Match: <etag>` or `*` on DeleteObject and per-key ETag in DeleteObjects; 412 [A3][A4]. Directory buckets additionally `x-amz-if-match-last-modified-time`, `x-amz-if-match-size` [A4]. (Verifies: S3 has conditional deletes; date of launch not in fetched text.) | `delete_blob(etag=, match_condition=)` and `if_modified_since` [Z3] | `if_generation_match` etc. on `Blob.delete` [G6] |
| Conditional compose / multipart complete | CompleteMultipartUpload If-Match / If-None-Match [A2] | `commit_block_list` with etag kwargs [Z3 param list] | compose: dest generation/metageneration + per-source generation-match [G4] |
| Conditional rename | RenameObject: dest If-Match/If-None-Match/If-(Un)Modified-Since + `x-amz-rename-source-if-*`; idempotency `x-amz-client-token` [A16] | Path-Create rename "supports conditional HTTP requests"; destination overwritten by default [Z15] | `move_blob(if_generation_match=..., if_source_generation_match=...)`; dest replaced unless precondition [G7][G11] |
| Conditional metadata update | n/a (metadata immutable; copy) [A9] | `set_blob_metadata(etag=, match_condition=)` [Z3] | `patch(if_metageneration_match=)` [G6] |
| Error surfaced in SDK | `botocore.exceptions.ClientError`; inspect `error.response['Error']['Code']` [A20]. Code string `PreconditionFailed` for 412 [unverified: error-code list unreachable] | 412 -> `ResourceModifiedError` ("typically 412") ; exists -> `ResourceExistsError`; 404 -> `ResourceNotFoundError`; `.error_code` attribute [Z12][Z13] | `google.api_core.exceptions.PreconditionFailed` (412, subclass of ClientError), `NotModified` (304), `NotFound`, `Conflict` [G15] |

Notes:
- S3 If-None-Match applies to the current version only in versioned buckets; a delete marker counts as absent [A2]. Conditional writes ignore in-flight multipart uploads [A2].
- S3 DeleteObject `If-Match: *` fails 412 if the latest version is a delete marker [A3].
- Azure multiple values in If-Match are ORed for Get Blob / Get Blob Properties [Z2].
- GCS `0` generation precondition is only valid for writes [G4].

## 5. Shared decisions

### 5.1 Retries and timeouts

| | boto3/botocore | azure-storage-blob | google-cloud-storage |
|---|---|---|---|
| Default mode | `legacy` (5 total attempts); `standard` (3 total, circuit-breaking); `adaptive` experimental (client-side rate limiting) [A19] | `ExponentialRetry` default [Z10] | per-method default policy [G5] |
| Count knob | `retries={'mode','max_attempts','total_max_attempts'}`; `max_attempts` in Config excludes initial request, in config file includes it [A19] | `retry_total`, `retry_connect`, `retry_read`, `retry_status`, `retry_to_secondary`; `ExponentialRetry(initial_backoff, increment_base)`, `LinearRetry` [Z10]. CONFLICT: README says `retry_total` "Defaults to 10" [Z13]; Learn page table says 3 [Z10] | `DEFAULT_RETRY.with_timeout(...)` (deadline default 120 s), `.with_delay(initial=1, multiplier=2, maximum=60)`; `retry=None` disables [G5][G3] |
| Idempotency awareness | not documented: retry lists are error-type based (connection errors, throttling, 500/502/503/504 etc.) [A19]; no idempotency statement in guide [observed absence] | not documented in [Z10]/[Z13] [observed absence] | Yes. Always-idempotent ops use DEFAULT_RETRY; conditionally idempotent ops use `ConditionalRetryPolicy` (`DEFAULT_RETRY_IF_GENERATION_SPECIFIED`, `_IF_METAGENERATION_SPECIFIED`, `_IF_ETAG_IN_JSON`); never-idempotent -> `retry=None` [G5]. BUT: [G3] says the Python library "automatically retries Objects: insert, Objects: delete, and Objects: patch by default", and the 3.17.1 signatures show `upload_from_file`, `delete` with `retry=...Retry` (unconditional) while `compose`, `rewrite`, `update`, `update_storage_class`, `move_blob` default to `ConditionalRetryPolicy` [G6][G7] |
| Timeouts | `connect_timeout` 60 s, `read_timeout` 60 s, `max_pool_connections` 10, `tcp_keepalive` [A21] | `connection_timeout` 20 s, `read_timeout` 60 s (client kwargs); "Client-side read timeouts will be automatically retried" [Z13] | `timeout=` per call default 60 s; scalar or `(connect, read)` tuple; `None` = block forever; "a request may be repeated several times using the same timeout each time" [G5] |
| Retryable HTTP codes | legacy: 429,500,502,503,504,509; standard adds named transient codes [A19] | not enumerated in fetched pages | 408, 429, 500, 502, 503, 504 + listed connection errors [G3] |

Advisory: the brief's premise "GCS retries only idempotent or precondition-guarded calls" holds only for some methods in 3.17.1; uploads and deletes retry by default per [G3]/[G6].

### 5.2 Error taxonomy
- boto3: `botocore.exceptions.BotoCoreError` (client-side: `EndpointConnectionError`, `ReadTimeoutError`, `ParamValidationError` ...) vs `ClientError` (any service error; parse `Error.Code`); modeled exceptions via `client.exceptions.X` (e.g. `InvalidWriteOffset` on put_object) [A18][A20].
- Azure: `azure.core.exceptions.AzureError` base; `HttpResponseError`; `ResourceExistsError`, `ResourceNotFoundError`, `ResourceModifiedError`, `ResourceNotModifiedError`, `ClientAuthenticationError`, `ServiceRequestError` (couldn't send), `ServiceResponseError` (sent, response not understood) [Z12]; storage `error_code` attr [Z13]; REST codes BlobNotFound 404, BlobAlreadyExists 409, *ConditionNotMet 412 [Z9].
- GCS: `google.api_core.exceptions.GoogleAPIError` -> `GoogleAPICallError` -> `ClientError` (NotFound, Conflict, PreconditionFailed, RequestRangeNotSatisfiable 416 ...) / `ServerError`; `Redirection` (NotModified 304); `RetryError` [G15]; plus `google.cloud.storage.exceptions.DataCorruption`, `InvalidResponse` [G6][G8 nav].

### 5.3 Consistency
- S3: strong read-after-write for PUT and DELETE of objects, incl. LIST after write/delete; HEAD/metadata/tags/ACL reads strongly consistent; single-key updates atomic; no cross-key atomicity; concurrent PUTs: latest timestamp wins; bucket configuration eventually consistent [A10]. (The Dec 2020 launch date is not in the fetched page.)
- Azure: "strong consistency model ... subsequent read or list operations return the latest update"; snapshot isolation; default last writer wins [Z11]. `retry_to_secondary` may read stale data on RA-GRS [Z13].
- GCS: strong global consistency for object read-after-write/metadata-update/delete and object listing; eventually consistent for IAM changes and bucket recreation; publicly cacheable objects may be stale per Cache-Control [G2].

### 5.4 Async parity
- boto3: no first-party async; aioboto3 15.5.0 is third-party (author Terri Cain) and last released 2025-10-30 [observed PyPI].
- Azure: first-party `azure.storage.blob.aio` ("complete async API"), needs an async transport such as aiohttp; async clients are async context managers with async `close` [Z13].
- GCS: no async module in the 3.17.1 reference navigation (modules listed: acl, batch, blob, bucket, client, constants, exceptions, fileio, hmac_key, notification, retry, transfer_manager) [observed absence, G8 nav].

### 5.5 Closing
- boto3 `S3.Client.close()` [A18]; Azure clients are (async) context managers with `close()` [Z13], DataLake clients have `close` [Z14]; GCS `Client.close()` [G8].

### 5.6 Key / name validation
| | S3 | Azure | GCS |
|---|---|---|---|
| Length | 1-1024 bytes UTF-8, includes prefix [A8] | 1-1024 characters (emulator 256) [Z1] | flat: 1-1024 bytes UTF-8; HNS: folder segment <=512 bytes and base name <=512 bytes [G1] |
| Forbidden | none formally; "safe" set listed; avoid `\ { } ^` non-printables; special handling for `& $ @ = ; / : , ?` and 0x00-0x1F, 0x7F; `soap` key needs path-style [A8] | any characters; reserved URL chars must be escaped; avoid names ending in `.`, `/`, `\`; no path segment should end with `.` [Z1] | no CR/LF; not `.` or `..`; not starting `.well-known/acme-challenge/`; avoid `#`, `[ ] * ?`, XML-illegal control chars [G1] |
| Segments | `.`/`..` segments discouraged (path normalisation) [A8] | flat <=254 segments; HNS <=63 (incl. account+container) [Z1] | – |
| Case | case sensitive [A8] | case sensitive [Z1] | – (not stated in fetched text) |

## 6. Pitfalls per OP-ID

- OP-01/02: Range header follows RFC 9110 [A7]. Unsatisfiable range -> 416: GCS maps 416 to `RequestRangeNotSatisfiable` [G15]; S3/Azure 416 behaviour [inference, error lists not verified]. Azure `x-ms-range-get-content-md5` only for ranges <=4 MiB, else 400 [Z8 get-blob]. GCS checksums cannot be validated on ranged downloads (INFO log only) [G6]. GCS `end` is inclusive [G6].
- OP-03: Azure `upload_blob` default `overwrite=False` (raises if exists) except append blobs, which append instead [Z3]; S3/GCS default overwrite [A2][G4]. Azure Put Blob replaces existing metadata [Z8]. botocore checksum defaults: `request_checksum_calculation` may add checksums on PutObject/UploadPart [A21].
- OP-04: S3 "Amazon S3 does not support object locking for concurrent writers ... latest timestamp wins" [A10].
- OP-05: S3 conditional writes need SigV4; If-Match needs s3:GetObject too [A2]. 409 ConditionalRequestConflict on PutObject is retryable; on CompleteMultipartUpload the whole MPU must restart [A2]. GCS generation 0 only for writes [G4].
- OP-06/07: S3 GP list is UTF-8 binary lexicographic [A8][A12]; S3 directory buckets: not lexicographic, only `/` delimiter, prefixes must end in delimiter, list shows prefixes of in-progress MPUs [A11]. Azure: alphabetical, upper-case first; in HNS `/` sorts lowest [Z8 list-blobs]; page max 5,000 [Z8]. S3 page max 1,000 [A12]. GCS lexicographic by name [G14]. No depth-limited listing in any SDK.
- OP-08: only GCS has server-side glob (`match_glob`) [G7].
- OP-09: S3 `x-amz-missing-meta` when metadata has unprintable chars [A9]. Last-modified granularity: S3/Azure use HTTP-date headers (RFC 1123, whole seconds) [Z2] [inference for S3]; GCS RFC 3339 timestamps [inference].
- OP-10: S3 DeleteObjects reports a non-existent key as deleted [A13]; for DeleteObject on non-existent key the fetched page only shows 204 responses, generic idempotency not stated [A4] (directory-bucket If-Match-size/time conditions return 204 if object doesn't exist [A4]). Versioned S3 delete inserts a delete marker [A4]. Azure delete of missing blob -> BlobNotFound 404 [Z9] -> ResourceNotFoundError [Z12]; Azure requires `delete_snapshots` if snapshots exist [Z3]. GCS `Blob.delete` raises NotFound [G6]; GCS Python retries delete by default [G3][G6] so a retried successful delete can surface NotFound [inference].
- OP-11: S3 directory buckets recursively delete empty parent directories when an object is deleted [A11]. Azure HNS recursive Path-Delete may return `x-ms-continuation`; with ACL auth and paginated mode "the actual directory deletion happens only in the last invocation" [Z15]. Batch limits: S3 1000, Azure 256, GCS 100 [A13][Z8][G9]; GCS batch: only last exception raised by default [G9].
- OP-12: S3 GP: no rename, copy+delete [A14]; RenameObject only S3 Express One Zone [A16]. Azure flat: no rename [observed absence]; HNS rename overwrites destination by default and breaks its lease [Z15]. GCS `rename_blob` is copy+delete (slow/costly for large objects; "not fully supported in a Batch context") vs `move_blob` atomic [G7]; objects.move: same bucket only, replaces existing destination unless preconditioned, new generation, auto-creates parent folders [G11]. GCS copy-based moves of Nearline/Coldline/Archive incur early-deletion charges; atomic move does not [G11].
- OP-13: S3 CopyObject atomic only up to 5 GB; larger needs UploadPartCopy (managed `copy()` does this) [A6][A18]. Azure Copy Blob may be asynchronous (copy_status pending; one pending copy per destination) [Z8 copy-blob]; Copy Blob From URL synchronous up to 256 MiB [Z8]. Azure `start_copy_from_url` with metadata given replaces, not merges, source metadata [Z3]. S3 copy with `MetadataDirective` governs metadata [A6]. GCS `rewrite` may need multiple calls (token) [G6].
- OP-14: s3transfer defaults: threshold/chunk 8 MiB, concurrency 10, `num_download_attempts` 5 [A22]. GCS upload checksum mismatch -> `DataCorruption` and the client tries to delete the uploaded object [G6].
- OP-15: all server-side copies are vendor-internal; cross-vendor must stream through client [inference].
- OP-19: S3 console "folders" are zero-byte objects visible to the API [A8]; S3 directory buckets auto-delete empty directories [A11]; Azure/GCS flat namespaces have no empty folders [Z1][G12]; HNS folder ops in GCS need the separate `storage_control_v2` client [G12].
- OP-20: S3 user metadata <=2 KB (sum of UTF-8 bytes of keys+values) inside 8 KB PUT header; keys stored lowercase; non-ASCII values RFC 2047-encoded; immutable after upload except via copy [A9]. Azure: total 8 KB; names must be C# identifiers, ASCII; case-preserving but case-insensitive, duplicates -> 400; set replaces all [Z1][Z7]. GCS custom metadata total 8 KiB [G10]; patchable in place [G6]. Tags: S3 10, Azure 10 (key 1-128, value 0-256 chars) [A9][Z3].
- OP-21: aio Azure clients must be closed (async) [Z13].
- OP-24: no vendor health endpoint in SDKs [observed absence].

## 7. Open items / not verified
- S3 error-code strings (`PreconditionFailed`, `InvalidRange`, `NoSuchKey`) and generic 204-on-missing for DeleteObject: error code list page unreachable; not confirmed in fetched text.
- Launch dates (S3 strong consistency Dec 2020; S3 conditional writes/deletes 2024/2025) are not stated in the fetched pages.
- GCS appendable objects / async (gRPC) client: not found in 3.17.1 Python reference; not further investigated.
- Azure `retry_total` default: 10 (README [Z13]) vs 3 (Learn [Z10]) conflict unresolved.
