# remote-store v1 operation catalogue vs comparable libraries

- **Date:** 2026-10-26. All sources were read on this date.
- **Brief:** [`briefs/remote-store v1 operation catalogue.md`](../briefs/remote-store%20v1%20operation%20catalogue.md).
- **Notes:** `research_notes/remote-store v1 operation catalogue/01..06`:
  - 01 workflow
  - 02 pyarrow.fs, smart_open and cloudpathlib
  - 03 vendor SDKs
  - 04 shared decisions
  - 05 pitfalls OP-01..11
  - 06 pitfalls OP-12..24
- **Status:** informs the catalogue and decides nothing. Recommendations are marked **advisory**.
- **Not used as an authority:** remote-store's own stable code and specs.

**Labels.**
- **[doc]**: stated in the cited docs, docstring, changelog, spec or issue.
- **[src]**: read in the released source at the cited tag.
- **[obs]**: seen by running code on 2026-10-26. These runs used pyarrow 26.0.0, smart_open 8.0.4 and cloudpathlib 0.26.0 against local disk and the **moto 5.2.4 S3 emulator**. Nothing was run against real AWS, Azure or GCS.
- **[inf]**: inference by the researcher, not stated by any source.
- **unreachable**: the source could not be fetched.

Bracketed keys such as `[OS]` refer to the source table. Each claim also carries its evidence label.

**The 10 comparables** (the denominator for every "n/10" count):
1. fsspec
2. pyarrow.fs
3. OpenDAL
4. object_store
5. gocloud blob
6. smart_open
7. cloudpathlib
8. boto3 (S3)
9. azure-storage-blob
10. google-cloud-storage

Hadoop FileSystem, paramiko/SFTP and obstore are cited where a question needed them. They are not counted.

---

## Sources and versions

| Key | Source (link) | Version / date |
|---|---|---|
| FS-API | https://filesystem-spec.readthedocs.io/en/latest/api.html | fsspec 2026.9.0 (page build 2026.9.0.post2) |
| FS-FEAT | https://filesystem-spec.readthedocs.io/en/latest/features.html , …/async.html | same |
| FS-COPY | https://raw.githubusercontent.com/fsspec/filesystem_spec/master/docs/source/copying.rst | master, 2026-10-26 |
| FS-CL | https://filesystem-spec.readthedocs.io/en/latest/changelog.html , raw `docs/source/changelog.rst` | to Dev (unreleased) |
| FS-SRC | https://raw.githubusercontent.com/fsspec/filesystem_spec/2026.9.0/fsspec/ (`spec.py`, `asyn.py`, `exceptions.py`, `transaction.py`, `mapping.py`, `generic.py`, `implementations/dirfs.py`, `implementations/arrow.py`); wheels 2025.12.0–2026.9.0 inspected | tag 2026.9.0 / master |
| S3FS | https://raw.githubusercontent.com/fsspec/s3fs/2026.9.0/s3fs/core.py , `errors.py`, `docs/source/changelog.rst` | s3fs 2026.9.0 |
| GCSFS / ADLFS / SSHFS | raw.githubusercontent.com `fsspec/{gcsfs,adlfs,sshfs}` main: `core.py`, `extended_gcsfs.py`, `spec.py`, changelogs | gcsfs 2026.10.1, adlfs 2026.8.0, sshfs 2026.8.0 |
| PA | https://arrow.apache.org/docs/python/api/filesystems.html and `generated/pyarrow.fs.*.html` | Apache Arrow v26.0.0 |
| PA-CPP | https://arrow.apache.org/docs/cpp/api/filesystem.html | v26.0.0 |
| PA-SRC | https://raw.githubusercontent.com/apache/arrow/apache-arrow-26.0.0/cpp/src/arrow/filesystem/s3fs.cc (also `azurefs.*`, `gcsfs.cc`, `filesystem.*`, `python/pyarrow/_fs.pyx`, `fs.py`) | tag apache-arrow-26.0.0 / main |
| OD-CAP | https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html | opendal_core 0.59.5 |
| OD-PY | https://opendal.apache.org/docs/python/api/capability/ ; `bindings/python/python/opendal/*.pyi` | Python binding 0.47.12 |
| OD-SRC | https://raw.githubusercontent.com/apache/opendal/v0.59.5/core/core/src/ (`types/operator/{operator,info,builder}.rs`, `types/capability.rs`, `types/error.rs`, `raw/path.rs`, `layers/{simulate,correctness_check,complete,capability_override}.rs`), `core/layers/*`, `services/{s3,fs,sftp}` | tag v0.59.5 |
| OD-CL | https://raw.githubusercontent.com/apache/opendal/main/CHANGELOG.md | to v0.59.1 entry |
| OS | https://docs.rs/object_store/0.14.2 (`ObjectStore`, `ObjectStoreExt`, `PutMode`, `GetOptions`, `GetRange`, `Error`, `Path`, `LocalFileSystem`, `MultipartUpload`) | object_store 0.14.2 (0.14.0 pages also read) |
| OS-SRC | https://raw.githubusercontent.com/apache/arrow-rs-object-store/v0.14.2/src/ (`lib.rs`, `path/mod.rs`, `client/retry.rs`, `client/mod.rs`, `aws/precondition.rs`, `aws/mod.rs`, `local.rs`, `memory.rs`, `prefix.rs`, `attributes.rs`, `parse.rs`) | tag v0.14.2 |
| OS-CL | https://raw.githubusercontent.com/apache/arrow-rs-object-store/main/CHANGELOG.md (+ `CHANGELOG-old.md`) | to v0.14.2 (2026-09-11) |
| OS-423 | https://github.com/apache/arrow-rs-object-store/issues/423 (WebFetch) | closed 2025-07-04 |
| OBS | https://developmentseed.org/obstore/v0.12.0/ ; raw `pyo3-object_store/src/error.rs`, `obstore/fsspec.py` | obstore 0.12.0 |
| GC | https://pkg.go.dev/gocloud.dev/blob ; https://gocloud.dev/howto/blob/ | gocloud.dev v0.47.0 (2026-10-14) |
| GC-SRC | https://raw.githubusercontent.com/google/go-cloud/v0.47.0/blob/blob.go , `blob/driver/driver.go`, `gcerrors/errors.go`, `blob/{s3blob,gcsblob,azureblob,fileblob,memblob}/*.go`, `internal/website/content/concepts/as.md` | tag v0.47.0 |
| SO | https://raw.githubusercontent.com/piskvorky/smart_open/develop/README.md , `HOWTO.md`, `help.txt`, `CHANGELOG.md`, `MIGRATING_FROM_OLDER_VERSIONS.md`; 8.0.4 wheel | smart_open 8.0.4 (develop docs). `README.rst` and `howto.md` are **unreachable** (404) |
| CP | https://cloudpathlib.drivendata.org/stable/ (api-reference, caching, other_client_settings); raw `HISTORY.md`, `cloudpath.py`, `s3/s3client.py`; 0.26.0 wheel | cloudpathlib 0.26.0 |
| AWS-* | https://docs.aws.amazon.com/AmazonS3/latest/userguide/ `conditional-writes.html`, `conditional-deletes.html`, `UsingMetadata.html`, `object-keys.html`, `Welcome.html` (consistency), `s3-express-differences.html`, `using-folders.html`, `copy-object.html`, `mpuoverview.html`; …/API/ `API_PutObject`, `API_GetObject`, `API_HeadObject`, `API_DeleteObject`, `API_DeleteObjects`, `API_CopyObject`, `API_RenameObject`, `API_ListObjectsV2`, `API_HeadBucket` | "latest", 2026-10-26. The error-code list page is **unreachable** (redirect) |
| B3 | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html , `guide/retries.html`, `guide/error-handling.html`; https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html ; botocore `CHANGELOG.rst` 1.36.0; s3transfer `download.py` | boto3/botocore 1.43.118, s3transfer 0.19.3 |
| AZ-* | https://learn.microsoft.com/en-us/rest/api/storageservices/ `specifying-conditional-headers-for-blob-service-operations`, `naming-and-referencing-containers--blobs--and-metadata`, `setting-and-retrieving-properties-and-metadata-for-blob-resources`, `copy-blob`, `list-blobs`, `blob-batch`, `get-blob`, `put-block`, `blob-service-error-codes`, `datalakestoragegen2/path/{create,delete}`; https://learn.microsoft.com/en-us/python/api/azure-storage-blob/ (BlobClient, ContainerClient, BlobServiceClient, package); `azure-core` exceptions; https://learn.microsoft.com/en-us/azure/storage/blobs/ `storage-retry-policy-python`, `concurrency-manage`, `data-lake-storage-namespace`; PyPI README | azure-storage-blob 12.31.0, azure-storage-file-datalake 12.26.0, azure-core 1.41.0 |
| GCS-* | https://cloud.google.com/storage/docs/ `request-preconditions` (updated 2026-10-22), `objects`, `consistency`, `retry-strategy`, `quotas`, `copying-renaming-moving-objects`, `rename-hns-folders`, `folders-overview`, `composing-objects`, `listing-objects`, `batch`; https://cloud.google.com/python/docs/reference/storage/latest/ (Blob, Bucket, Client, Batch, retry, retry_timeout); https://googleapis.dev/python/google-api-core/latest/exceptions.html | google-cloud-storage 3.17.1, google-api-core 2.43.0 |
| H-* | https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/ `introduction.html`, `filesystem.html`, `fsdatainputstream.html`, `fsdatainputstreambuilder.html`, `outputstream.html`, `pathcapabilities.html`; …/hadoop-aws/tools/hadoop-aws/ `directory_markers.html`, `index.html` | Hadoop 3.5.0 ("current"); some pages read on "stable" = 3.3.5 |
| PY / PARAMIKO / SFTP | https://docs.python.org/3/library/os.html , `pathlib.html`; https://docs.paramiko.org/en/latest/api/sftp.html + raw `paramiko/sftp_client.py`; https://cvsweb.openbsd.org/src/usr.bin/ssh/PROTOCOL ; https://datatracker.ietf.org/doc/html/draft-ietf-secsh-filexfer-02 | Python 3.15 docs; paramiko 5.1.0; OpenSSH HEAD |

---

## Summary

1. **Completeness (Q1).**
   - The most widely offered operations that no entry covers:
     - presigned/signed URLs (8/10)
     - batch delete (6/10)
     - versioned access (6/10)
     - abort of an in-flight write (5/10)
     - append (5/10, all gated)
     - system properties such as content type, apart from user metadata (6/10+)
     - multi-range read (3/10)
   - Vendor-only operations: retention, tier change, compose, restore, tags, leases.
   - fsspec alone offers a transaction, a key-value mapping view, a FUSE mount and rsync.
2. **The cut (Q2).**
   - **Conditions:** comparables merge write, atomic replace and conditional write. A condition is a *mode or option* of put (object_store `PutMode`, gocloud `IfNotExist`, OpenDAL `write_with(if_*)`, GCS `ifGenerationMatch`). Conditions also attach to read, delete, copy, rename and metadata updates, not only to write.
   - **Listing:** they differ most on list, walk and match.
     - gocloud and object_store have no glob, and nobody but fsspec has a depth limit.
     - pyarrow merges inspect, list and walk into one call.
3. **Gating (Q3).** Only OpenDAL (and Hadoop) offers a capability query, and OpenDAL's flags describe the *effective* set, simulations included. Every other comparable reports a gate only when called:
   - as an error: `NotImplemented`/`NotSupported`, `Unimplemented`, `NotImplementedError`
   - or with no signal at all (no-ops, dropped keys)
   - and some gates depend on bucket or account type (HNS, S3 Express), discovered at runtime.
4. **Shared decisions (Q4).** Every abstraction fixes these once per instance: path rules, one error taxonomy, retry and timeout policy, concurrency limit and prefix scope. They choose very differently. `..` is rejected, encoded, escaped or passed through. A missing-key delete succeeds in some and errors in others. Retries are tied to idempotency, to error status, or to an allow-list.
5. **Pitfalls (Q5).** These come per entry, below. Two recur:
   - Bucket or account type, not provider, decides the semantics of move, folder creation and tree delete.
   - In 2025–26 the comparables kept merging overwrite and no-overwrite variants into option structs, and retrofitting `..` containment.

---

## Q1. Completeness: operations no catalogue entry covers

Counts are lower bounds: an operation counts only where the notes found it in a full text. "(g)" means gated per backend or bucket type.

| Operation | Use case | Offered by (name) | Count |
|---|---|---|---|
| **Presigned / signed URL** | Give a browser or third party time-limited access without credentials | fsspec `sign` (base raises `NotImplementedError`) [src FS-SRC]; OpenDAL `presign_read/stat/write/delete` (g) [doc OD-CAP]; object_store `Signer` (PrefixStore forwards it, #738/#739) [doc OS-CL]; gocloud `SignedURL` (g, `Unimplemented`) [doc GC]; cloudpathlib `as_url(presign=True)` [doc CP]; boto3 `generate_presigned_url` [doc B3]; Azure `generate_blob_sas` [doc AZ]; GCS `generate_signed_url` [doc GCS] | 8/10 |
| **Batch / bulk delete** | Delete many keys in few requests; underlies tree delete | object_store `delete_stream` (S3 batches of 1000, Azure 256) [doc OS]; OpenDAL `Deleter`, `delete_max_size` [doc OD-CAP]; fsspec `rm(list)` (s3fs bulk delete) [doc S3FS]; boto3 `delete_objects` (≤1000) [doc AWS-DeleteObjects]; Azure `delete_blobs` (≤256) [doc AZ blob-batch]; GCS `delete_blobs`/`batch()` (≤100) [doc GCS batch] | 6/10 |
| **Versioned access** (read/stat/delete a version, list versions) | History, recovery, reads pinned to a version | OpenDAL `read/stat/delete_with_version`, `list_with_versions` (g) [doc OD-CAP]; object_store `GetOptions.version`, `UpdateVersion` [doc OS]; smart_open `version_id` (S3) [doc SO]; boto3 `VersionId`, `list_object_versions` [doc B3]; Azure `version_id=` [doc AZ]; GCS `generation=`, `list_blobs(versions=True)` [doc GCS] | 6/10 |
| **Abort an in-flight write** | Drop a streamed or multipart upload without committing or leaking parts | object_store `MultipartUpload::abort` [doc OS]; OpenDAL `Writer::abort` [doc OD-SRC]; gocloud cancel `ctx` [doc GC]; smart_open `terminate()` (S3) [src SO]; boto3 `abort_multipart_upload`, `list_multipart_uploads` [doc B3] | 5/10 |
| **Append** | Logs, row appends | pyarrow `open_append_stream` (g: S3 raises) [doc PA; obs]; smart_open mode `ab` (g: Azure append blobs) [doc SO]; OpenDAL `write_with(append)`, `write_can_append` (g) [doc OD-CAP]; boto3 `put_object(WriteOffsetBytes=)` (g: directory buckets) [doc B3]; Azure append blob [doc AZ]. cloudpathlib mode `a` works on the local cache copy [inf from CP] | 5/10 (+1 emulated) |
| **System properties** (content-type, cache-control, encoding) apart from user metadata | HTTP serving, MIME handling | object_store `Attribute::{ContentType, CacheControl, …}` [doc OS-SRC attributes.rs]; OpenDAL `write_with_content_type` etc. (g) [doc OD-CAP]; pyarrow `metadata=` (S3 honours only 6 system keys) [src PA-SRC]; cloudpathlib `content_type_method` [doc CP]; boto3 `ContentType`, `CacheControl` [doc AWS-META]; Azure `ContentSettings` [doc AZ]; GCS `content_type`, `cache_control` [doc GCS] | 7/10 |
| **Multi-range (vectored) read** | Columnar formats read many byte ranges at once | object_store `get_ranges` (coalesces) [doc OS]; OpenDAL `Reader::fetch` (merges with gap) [doc OD-SRC]; fsspec `cat_ranges(max_gap)` [doc FS-API]. Also Hadoop `readVectored`, paramiko `readv` | 3/10 |
| **Server-side compose / block list** | Concatenation, parallel upload | OpenDAL `compose` (g) [doc OD-CAP]; boto3 `upload_part_copy` [doc B3]; Azure `stage_block`/`commit_block_list` [doc AZ]; GCS `Blob.compose` (≤32 sources) [doc GCS] | 4/10 |
| **Restore / undelete** | Archive retrieval, recovery from soft delete | OpenDAL `restore` (g) [doc OD-CAP]; boto3 `restore_object` [doc B3]; Azure `undelete_blob`, rehydrate [doc AZ]; GCS `restore_blob` [doc GCS] | 4/10 |
| **Server-side checksums** | Integrity checks | boto3 `ChecksumAlgorithm` [doc B3]; Azure `validate_content`, `content_md5` [doc AZ]; GCS `checksum=`, `crc32c` [doc GCS]; object_store CRC64NVME support (#633) [doc OS-CL] | 4/10 |
| Storage class / tier change | Cost | boto3 via copy `StorageClass` [doc AWS-COPY]; Azure `set_standard_blob_tier` [doc AZ]; GCS `update_storage_class` [doc GCS] | 3/10 |
| Retention / legal hold / object lock | WORM compliance | boto3, Azure, GCS [doc B3, AZ, GCS] | 3/10 |
| Bucket / container create and delete | Provisioning | pyarrow `allow_bucket_creation/deletion` [doc PA]; fsspec/s3fs `mkdir` creates a bucket [src S3FS]; the three SDKs | 5/10 |
| Transparent compression | Read/write `.gz`, `.bz2` | pyarrow `compression=` [doc PA]; smart_open `compression=`, `register_compressor` [doc SO] | 2/10 |
| Local cache / caching layer | Repeated reads, offline edit | cloudpathlib cache modes [doc CP]; fsspec caching filesystems, `open_local` [doc FS-API] | 2/10 |
| `touch` (create empty / refresh mtime) | Sentinels | cloudpathlib `touch` [src CP]; fsspec `touch` [src FS-SRC] | 2/10 |
| Tags (separate from metadata) | Indexing, lifecycle filters | boto3 (≤10), Azure (≤10, `find_blobs_by_tags`) [doc] | 2/10 |
| Query in place | Server-side CSV/JSON filter | boto3 `select_object_content`, Azure `query_blob` [doc] | 2/10 |
| Transaction (deferred multi-file commit) | Commit or discard a set of writes together; "semi-atomic" | fsspec `Transaction`, `fs.transaction` [doc FS-FEAT; src FS-SRC] | 1/10 |
| Key-value mapping view | Zarr-style stores | fsspec `get_mapper`/`FSMap` [doc FS-API] | 1/10 |
| FUSE mount | Expose the store as a local mount | fsspec `fuse.run` [doc FS-API] | 1/10 |
| Sync (rsync with delete) | Mirror trees | fsspec `generic.rsync` [doc FS-API; src FS-SRC] | 1/10 |
| Leases, snapshots, abort async copy | Pessimistic lock, point-in-time copy | Azure only [doc AZ] | 1/10 |
| Annotations (≤1 MB) | Large attached payloads | S3 only [doc AWS-META] | 1/10 |

**Absent from almost all comparables:**
- **OP-07's depth limit** is offered only by fsspec (`find/walk(maxdepth)`) [doc FS-API]. Arrow C++ has `max_recursion`, but Python pyarrow does not expose it [obs]. cloudpathlib limits depth only by pruning in `walk(lazy=True)` [doc CP].
- **OP-18 (capability query)** exists only in OpenDAL [doc OD-CAP].
- **OP-24 (health check)** exists only in OpenDAL `check()` and gocloud `IsAccessible` [src OD-SRC, GC-SRC].
- None of the three vendor SDKs has OP-07 depth, OP-18 or OP-24 [doc, absence in references].

**Advisory.**
- Presign (8/10), batch delete (6/10), versioned access (6/10), abort (5/10) and system properties (7/10) are the strongest candidates for an entry, a gated entry, or an explicit "out of scope" note.
- Batch delete and abort could also be read as parts of OP-10/11 and OP-03 rather than new intents.

---

## Q2. The cut: where comparables split or merge differently

### Write vs atomic replace vs conditional write (OP-03 / OP-04 / OP-05)

**How the comparables cut it:**
- **object_store merges all three.**
  - Every `put` is atomic: "No clients should be able to observe a partially written object" [doc OS].
  - `PutMode::{Overwrite (default), Create, Update(UpdateVersion)}` selects the precondition on one `put_opts` [doc OS].
  - The streamed path is a separate method, `put_multipart_opts`. The atomic wording is not stated for it [doc OS; inf].
- **gocloud** offers if-absent only, as `WriterOptions.IfNotExist` on the ordinary writer [doc GC]. Other preconditions go through driver `BeforeWrite` with `As` [doc GC].
  - The docs say a failure returns `gcerrors.PreconditionFailed`. That constant does not exist; drivers return `FailedPrecondition` [src GC-SRC `blob.go` L1516, `gcerrors/errors.go`; verified 2026-10-26].
- **OpenDAL** makes conditions options on `write_with`, each with its own capability flag: `write_with_if_not_exists`, `_if_none_match`, `_if_match`, `_if_version_match` [doc OD-CAP].
- **GCS** uses one parameter for both: `ifGenerationMatch=0` means "absent", and `=<gen>` means "unchanged" [doc GCS-PRE].
- **S3** uses the headers `If-None-Match: *` and `If-Match` on PutObject, CopyObject and CompleteMultipartUpload [doc AWS-CW].
- **fsspec** has `mode="create"` / `xb`. The docs say "whether it is checked up front or on commit, and whether it is atomic is implementation-dependent", "trial basis" [doc FS-FEAT, FS-API]. The base implementation is `exists()` then write [src FS-SRC].
- **No conditional write** in pyarrow, smart_open or cloudpathlib [doc/src; obs].
  - cloudpathlib's `open('x')` and its mtime checks are check-then-act [src CP; inf].

**Atomic replace is a separate operation only where the backend is a filesystem:**
- Python split `os.rename` (fails on Windows if the target exists) from `os.replace` (atomic per POSIX) [doc PY].
- paramiko split `rename` (target must not exist) from `posix_rename` [doc PARAMIKO].
- No object-store abstraction has a separate "atomic replace". There, PUT already is one [doc AWS-CONS, OS, GC].

**Abort as its own verb:**
- object_store, OpenDAL, gocloud and smart_open expose abort apart from close [doc OS, OD-SRC, GC, src SO].
- On exception, pyarrow S3 *commits* the partial object and cloudpathlib *uploads* it [obs; src PA-SRC "Close rather than Abort"].

**Trend: conditions were folded into option structs.**
- object_store 0.13.0 merged `rename`/`rename_if_not_exists` into `rename_opts` (#555) and `copy`/`copy_if_not_exists` into `copy_opts` (#548) [doc OS-CL].
- OpenDAL 0.58.0 added `rename_with_if_not_exists` as an option [doc OD-CL].

**Conditions reach beyond write:**
- S3 has conditional GET/HEAD, copy, rename, and DeleteObject `If-Match` (directory buckets also take size and time conditions) [doc AWS-CD, AWS-DEL, AWS-REN].
- Azure accepts conditions on get, delete, copy and metadata set [doc AZ cond. headers, AZ BlobClient].
- GCS accepts them on read, delete, compose and move [doc GCS-PRE, GCS Bucket].
- OpenDAL gates `read_with_if_match`, `delete_with_if_*` and `copy_with_if_not_exists` [doc OD-CAP].

**Cost to a caller.**
- Separate entries make the guarantee of each visible: atomic, conditional, streamed. But they multiply entry points and invite a matrix of streamed × conditional.
- A mode on one call keeps one entry point but hides that the streamed or multipart path has weaker or different guarantees. On S3, a 409 on CompleteMultipartUpload means restarting the whole upload [doc AWS-CW].
- If OP-05 stays write-only, conditional delete, copy, rename and read have no home [inf].

### List vs walk vs pattern (OP-06 / OP-07 / OP-08)

**How each comparable cuts it:**

| Comparable | Shape |
|---|---|
| gocloud | One `List(ListOptions{Prefix, Delimiter})`. An empty delimiter gives a flat recursive listing. No glob, no depth [doc GC] |
| object_store | `list` (recursive) vs `list_with_delimiter` (one level); `list_with_offset`. No glob, no depth [doc OS] |
| OpenDAL | `list` + `list_with(...).recursive(true)` (gated `list_with_recursive`, simulated by default) [doc OD-CAP, OD-SRC]. No glob found |
| pyarrow | **One call for inspect, list and walk:** `get_file_info(path \| [paths] \| FileSelector(base, allow_not_found, recursive))`. No glob; Python has no depth [doc PA; obs] |
| fsspec | Separate `ls`, `find(maxdepth, withdirs)`, `walk(maxdepth, topdown)`, `glob(maxdepth)`, `expand_path`. `copy`/`get`/`put` also accept globs and `recursive=`/`maxdepth=` [doc FS-API, FS-COPY] |
| cloudpathlib | `iterdir`, `walk(lazy=)`, `glob`, `rglob` [doc CP] |
| Vendor SDKs | Prefix + delimiter. Only GCS has a server-side glob (`match_glob`) [doc GCS Bucket] |

**Cost to a caller.**
- With one call plus options, depth and pattern must be emulated client-side. A flat recursive listing then filtered costs O(subtree) whatever depth is asked [inf; H-INTRO "O(child-entries)" doc].
- With separate calls, pruning becomes possible: cloudpathlib added `walk(lazy=True)` precisely so pruning `dirnames` saves calls [doc CP-HIST v0.25.0].
- Glob semantics drift with the reference implementation. fsspec 2023.9 changed glob (the exact change is unverified), and pathlib 3.13 changed trailing `**` [doc FS-CL, PY]. A separate pattern entry carries that drift alone [inf].

### Inspect (OP-09)

- Hadoop deprecated single-attribute probes "to encourage users to make a single call to getFileStatus(p)" [doc H-FS].
- gocloud `Exists` is a shortcut over `Attributes`/`ListPage` [doc GC].
- pyarrow returns `FileType.NotFound` instead of raising [doc PA].

So the comparables lean towards one rich inspect call with derived `exists`/`is_*`, not separate probes.

### Delete (OP-10 / OP-11)

- **OpenDAL** merged them: `remove_all` was deprecated in 0.55.0 for `delete_with(recursive(true))` [doc OD-SRC].
- **fsspec** uses `rm(recursive, maxdepth)` [doc FS-API].
- **pyarrow** splits three ways: `delete_file`, `delete_dir` (removes the dir) and `delete_dir_contents` (keeps it) [doc PA].
- **cloudpathlib** splits `unlink`, `rmdir` (empty only) and `rmtree` [doc CP].
- **object_store and gocloud** have no tree delete; the caller lists, then deletes [doc OS, GC].

### Copy and transfer (OP-13 / OP-14 / OP-15)

- **fsspec** splits by locality: `copy` (remote→remote), `get` (remote→local), `put` (local→remote), with one documented behaviour spec [doc FS-COPY].
- **pyarrow** has `copy_file` within a filesystem and `copy_files` for any pair, local included. This merges OP-14 and OP-15 [doc PA].
- **cloudpathlib** `copy` handles all three. Cross-client copies go through the local cache [src CP].
- **object_store** copies within one store only [doc OS].

### Read (OP-01 / OP-02)

- pyarrow splits sequential `open_input_stream` from random `open_input_file` [doc PA]. Hadoop chose one `openFile()` with a read-policy option [doc H-OPEN].
- object_store merges ranges into `get_opts(GetOptions{range, if_match, version})`. Coalesced multi-range reads are a separate `get_ranges` that takes no options [doc OS].

**Advisory.** The draft's cut matches fsspec and cloudpathlib, the Python path-style APIs. Two splits remain open questions for the catalogue, not decisions:
- conditions as a cross-cutting modifier versus OP-05;
- OP-06/07/08 as one listing with options versus three entries.

---

## Q3. Optional entries: what is gated and how a caller learns

### Four signalling strategies (plus Hadoop)

| Strategy | Who | Mechanism |
|---|---|---|
| **Declared and pre-checked** | OpenDAL | `Operator::info().capability()` → `Capability` (~90–100 bool or limit fields) [doc OD-CAP; src OD-SRC]. `CorrectnessCheckLayer` (always installed) raises `ErrorKind::Unsupported` *before* the backend is called. The opt-in `CapabilityCheckLayer` also checks non-critical arguments [doc+src OD-SRC] |
| **Configured per store + call-time error** | object_store | `S3ConditionalPut::{ETagMatch (default), Disabled}`, `S3CopyIfNotExists::{Header, HeaderWithStatus, Multipart}` (no default) [doc OS-SRC precondition.rs]. Failure is `Error::NotImplemented{operation, implementer}` **or** `Error::NotSupported`, with no stated rule for which. S3 uses both for the same kind of gate [src OS-SRC; inf] |
| **Call-time error only** | gocloud, pyarrow, cloudpathlib, smart_open | gocloud `gcerrors.Unimplemented` (e.g. `SignedURL`) [doc GC]; pyarrow `ArrowNotImplementedError` (append on S3), sometimes a generic `OSError` (S3 dir move) [obs]; cloudpathlib `CloudPathNotImplementedError` [src CP]; smart_open `NotImplementedError` for an unknown scheme or mode [obs] |
| **Silent emulation or no-op** | fsspec, cloudpathlib, pyarrow, smart_open | fsspec `mkdir` body is `pass`, `mv` = copy + rm, `mode="create"` = exists then write [src FS-SRC]. cloudpathlib `mkdir` on S3/GCS writes nothing, and `exists()` stays False [obs]. pyarrow drops unsupported metadata keys ("will be ignored") [doc PA; obs]. smart_open ignores unknown `transport_params` with a log warning [doc SO; obs] |
| (Path-scoped probe) | Hadoop | `hasPathCapability(path, cap)`. It "MUST NOT return True … unless it is known to be supported". False may mean unknown. It must be cheap and side-effect free [doc H-PCAP] |

### What the comparables gate

- **OpenDAL flags** [doc OD-CAP]:
  - create_dir, rename, copy, `list_with_recursive`
  - `write_with_user_metadata`, append
  - presign
  - conditional and versioned variants of read, write, stat, delete and copy
  - multipart limits `write_multi_{min,max}_size`, `delete_max_size`
  - `shared`
- **The catalogue's gated OP-19 and OP-20 match OpenDAL's `create_dir` and `write_with_user_metadata`.** OpenDAL also gates OP-07 (recursive list), OP-12 (rename) and OP-13 (copy) [doc OD-CAP]. Its S3 service reports `rename` and `create_dir` as Unsupported natively [src OD-SRC services/s3].
- **Gates depend on bucket or account type, found at runtime:**
  - pyarrow Azure `move` needs HNS (cached probe) [doc PA-CPP; src PA-SRC].
  - gcsfs probes `_is_bucket_hns_enabled` per bucket [src GCSFS].
  - OpenDAL S3 sets several flags to `!is_s3_express` [src OD-SRC].
  - S3 `RenameObject` exists for Express One Zone only [doc AWS-REN].
  - Azure rename and recursive directory delete exist on HNS only [doc AZ-HNS, AZ Path].

### Pitfalls of a capability query

- **Native vs effective.** OpenDAL had `native_capability()` and `full_capability()` and **removed both in 0.58.0**. `capability()` is now "the composed operator availability contract" (#7747) [doc OD-CL]. `SimulateLayer` (on by default) sets these flags itself when it can emulate them: `create_dir` if list + empty write, `delete_with_recursive` if list + delete, and `read_with_suffix` [src OD-SRC simulate.rs]. A caller cannot tell native from emulated [src].
- **Flags get missed.** OpenDAL fixed missing flags piecemeal: swift copy (#7204), S3 content-disposition (#7349), and a missing conditional-write check (#7320) [doc OD-CL].
- **Python bindings re-type the signal.** obstore maps `NotImplemented` → builtin `NotImplementedError` but `NotSupported` → `obstore.exceptions.NotSupportedError`, two unrelated types [src OBS error.rs].

**Advisory.** A query alone does not settle the gate in any comparable. OpenDAL pairs it with a pre-dispatch check, and Hadoop defines False as "unknown". Silent no-ops (fsspec, cloudpathlib) are the pattern that leaves a caller unable to tell "unsupported" from "done".

---

## Q4. Shared decisions (decided once, not per operation)

| Decision | object_store 0.14.2 | OpenDAL 0.59.5 | gocloud v0.47.0 | fsspec 2026.9.0 | pyarrow 26 / smart_open 8.0.4 / cloudpathlib 0.26 | Vendor SDKs |
|---|---|---|---|---|---|---|
| **Key type and validation** | `Path` type with these rules: no leading or trailing `/`, no empty segments, no `.`/`..`, no control characters. `Path::parse` rejects; `Path::from` percent-encodes (`foo/../bar` → `foo/%2E%2E/bar`). No length check [doc OS-SRC path] | `&str` normalised on every call: trim, strip leading `/`, collapse `//`; trailing `/` = directory; `..` passed through [doc+src OD-SRC raw/path.rs] | Rejects keys that are not UTF-8 (`InvalidArgument`). Per-driver escaping `__0x<hex>__` with a different character set per driver [doc GC driver pkgs; src] | `_strip_protocol` + `root_marker` per implementation [src FS-SRC] | pyarrow rejects a scheme; `normalize_path` is a no-op. smart_open and cloudpathlib need a full URI. None of the three normalises `..` or `//` [obs] | S3 ≤1024 bytes; Azure ≤1024 chars, ≤254 segments (HNS ≤63); GCS ≤1024 bytes, no CR/LF, not `.`/`..` [doc AWS-KEYS, AZ naming, GCS objects] |
| **Error taxonomy** | One `Error` enum: NotFound, AlreadyExists, Precondition, NotModified, NotSupported, NotImplemented, PermissionDenied, Unauthenticated, InvalidPath, Generic… [doc OS] | `ErrorKind` (Unsupported, NotFound, AlreadyExists, ConditionNotMatch, RangeNotSatisfied, IsADirectory, RateLimited, …) plus `ErrorStatus` Permanent / Temporary / Persistent [doc OD-SRC error.rs]. Python classes are not builtins [src] | `gcerrors.ErrorCode` + `ErrorAs` to reach the native error [doc GC] | Builtin `FileNotFoundError`, `FileExistsError`, `NotImplementedError`; each implementation translates (s3fs: `PreconditionFailed` → `FileExistsError` under `If-None-Match`) [src FS-SRC, S3FS errors.py] | pyarrow builtins + `ArrowInvalid`; smart_open S3 missing key → plain `OSError`; cloudpathlib's own hierarchy mixed into builtins [obs] | botocore `ClientError` + code string; Azure `ResourceExistsError`/`ResourceModifiedError`/…; google-api-core `PreconditionFailed`, `NotFound` [doc B3, AZ, GCS] |
| **Retries** | Built in: `RetryConfig` (10 retries, 3 min). Timeouts retried only for idempotent or safe requests; S3 Overwrite put/copy marked idempotent [doc+src OS-SRC retry.rs] | Opt-in `RetryLayer`, retries only `Temporary` errors, then marks them `Persistent` [doc OD-SRC] | Not in the portable API; left to the provider SDK [src absence; inf] | Per implementation (s3fs 5 retries, allow-list + string match) [src S3FS] | pyarrow S3 `retry_strategy` (3 attempts); the others defer to boto3 config [doc PA; SO] | botocore modes legacy / standard / adaptive. Azure `retry_total` (README says 10, Learn says 3: **conflict**). GCS idempotency-aware `ConditionalRetryPolicy`, **but** uploads and deletes retry by default in 3.17.1 [doc B3, AZ, GCS-RETRY] |
| **Timeouts** | `ClientOptions` per store (30 s request, 5 s connect) [doc OS-SRC] | Opt-in `TimeoutLayer` (60 s control, 10 s IO) [doc OD-SRC] | Per call via `ctx` deadline; cancelling the ctx aborts a write [doc GC] | `sync(timeout)` → `FSTimeoutError`; socket timeouts per implementation [src FS-SRC] | pyarrow S3 `request_timeout` "ignored on non-Windows, non-macOS" [doc PA] | botocore 60/60 s; Azure 20/60 s; GCS 60 s per call [doc] |
| **Consistency stated** | Atomic put; list order not guaranteed; keep both ETag and version [doc OS] | None found [absence] | "List is not guaranteed to include all recently-written blobs"; blob not readable until `Close` [doc GC] | None for storage; client listing cache (`DirCache`) can be stale [doc FS-FEAT] | — | S3, Azure and GCS: strong read-after-write including list [doc AWS-CONS, AZ concurrency, GCS-CONS] |
| **Closing** | No close; Drop [src absence; inf] | No `Operator::close`; `Writer` must be closed or aborted, else "data could be lost" [doc OD-SRC] | `Bucket.Close()`; later calls → `FailedPrecondition`; `Writer.Close` commits, "always check the error of Close" [doc GC; src] | Instances cached by args, pinned against GC until `clear_instance_cache`; s3fs `weakref.finalize` [doc+src] | pyarrow: no close, process-global `finalize_s3` at exit; cloudpathlib cache cleanup on GC [doc PA, CP] | `client.close()` (boto3, GCS); Azure clients are (async) context managers [doc] |
| **Async parity** | Async-only trait; obstore adds `_async` twins for every op [doc OS, OBS] | Async `Operator` + `blocking::Operator`; Python `AsyncOperator` / `Operator` [doc OD-SRC, OD-PY] | Synchronous + `ctx` [doc GC] | `AsyncFileSystem` coroutines, sync wrappers on an IO thread [doc FS-FEAT] | None in Python | Azure first-party `aio`; boto3 none (aioboto3 is third party); GCS none in 3.17.1 [doc] |
| **Concurrency limit / instrumentation** | `LimitStore`, `ThrottledStore` [doc OS-SRC] | `ConcurrentLimitLayer`; ~20 optional layers (logging, tracing, metrics, chaos…) [src OD-SRC Cargo] | Built-in OpenTelemetry [doc GC] | `batch_size`; callbacks [doc FS-FEAT] | — | — |
| **Prefix scope (OP-16)** | `PrefixStore` | `root` option | `PrefixedBucket`, `SingleKeyBucket` | `DirFileSystem` | pyarrow `SubTreeFileSystem` | — |

**Observations from the matrix [inf unless cited].**
- `..` is handled four different ways:
  - object_store rejects or encodes it.
  - gocloud escapes the `/` of `../`.
  - OpenDAL passes it through generically.
  - fsspec DirFileSystem guards it only on local disk.
- Retry safety is tied to different things:
  - object_store: per-request idempotency.
  - OpenDAL: error status.
  - s3fs: an allow-list.
  - gocloud: nothing at the portable layer.
- GCS retries deletes by default [doc GCS-RETRY], so a retried delete that already succeeded can surface as NotFound [inf].
- Python bindings diverge from their Rust cores in exception typing (obstore, OpenDAL Python) [src].

---

## Q5. Pitfalls per entry (notes for each entry's later session; no semantics proposed)

Full citations are in notes 02–06. Each line names the comparable that changed or split something.

### OP-01 Read
- The view during a streamed read is undefined unless pinned. Hadoop: later changes "MAY be partially visible" [doc H-FSDIS]. s3fs 2026.3.0 added ETag expiry checks (#1008) [doc S3FS-CL].
- Read-ahead defaults changed results in memory, not in data: gcsfs 2026.7 prefetcher 170→600 MB, reverted for `cat_file` in 2026.8.1 [doc GCSFS-CL].
- On a directory path, object_store 0.6.0 switched `get`/`head` to NotFound (#4231) [doc OS-CL].
- pyarrow S3 streams are unbuffered [doc PA-CPP]. `allow_delayed_open` defers open errors to close [doc PA].
- cloudpathlib downloads the whole object first; a locally edited cache blocks reads (`OverwriteNewerLocalError`) [doc CP; obs].

### OP-02 Read at offsets
- Ranges past EOF were fixed separately in object_store 0.12.0 (#6751), fsspec caches (#2081), adlfs, smart_open (#549, #889) and s3fs [doc *-CL]. object_store `GetRange::Bounded` errors only if the range *starts* past EOF [doc OS].
- Range shapes: Azure has no suffix range [doc AZ range]. S3 serves one range per GET [doc AWS GetObject]. object_store errors if a server ignores Range (#4841) [doc OS-CL].
- Multi-range reads are split out with coalescing: `get_ranges`, `Reader::fetch`, `cat_ranges` [doc]. Pinned ranges need `get_opts` per range [doc OS].
- Hadoop `readVectored`: if the file changes, "Some ranges may have old data, some may have new" [doc H-FSDIS].
- fsspec block caches have had double-read and edge bugs (#1984, #2082, #2163) [doc FS-CL].
- cloudpathlib makes no remote range request at all [doc CP].

### OP-03 Write
- Visible only on close, and close can fail: Hadoop [doc H-OUT], gocloud ("not guaranteed to have succeeded until Close") [doc GC], paramiko pipelined writes [doc PARAMIKO].
- Abort is explicit, and S3 and GCS can't clean up on drop. object_store recommends lifecycle rules [doc OS]. smart_open 7.0.0 fixed orphaned billable multipart parts [doc SO-MIG].
- On exception, pyarrow S3 commits the partial object [obs; src], cloudpathlib uploads it [obs], and smart_open aborts [obs].
- Part-size floor: 5 MiB to 5 GiB, ≤10,000 parts, and R2 needs equal-sized parts [doc AWS, OS]. OpenDAL makes `write_multi_min_size` and `write_can_empty` capabilities [doc OD-CAP].
- Empty files take a separate path and have lost options: s3fs exclusive-create on empty files [doc S3FS-CL].
- Local durability: object_store 0.14.0 `with_fsync` (#643) and close-error checks (#676) [doc OS-CL].
- Parent creation: fsspec reverted `auto_mkdir` in `open()` (#1365) [doc FS-CL].
- Defaults differ: Azure `upload_blob` defaults to `overwrite=False` [doc AZ]; S3 and GCS overwrite [doc]. botocore 1.36.0 changed the default checksums [doc B3-CL].

### OP-04 Replace atomically
- Object-store PUT is atomic [doc AWS-CONS, OS]. On local disk object_store writes temp files `…#<n>` that leak into the key space and are excluded from listing [doc OS].
- Overwriting on rename differs: Windows `os.rename` vs `os.replace` [doc PY]; SFTP `rename` vs `posix_rename` (OpenSSH extension) [doc PARAMIKO, SSH-PROTO].
- Durable replace needs a directory fsync; object_store fixed a create-mode rename fsync bug (#758) [doc OS-CL].
- object_store local copy was not atomic until #4759; it now hard-links and cannot cross filesystems [doc OS].
- fsspec transactions are "semi-atomic" [doc FS-FEAT].
- S3 has "no object locking for concurrent writers … latest timestamp wins" [doc AWS-CONS].

### OP-05 Conditional write
- S3 gained native support late. object_store went from a DynamoDB lock to native (0.11.2) to on by default (0.12.0) [doc OS-CL].
- Conflicts surface as 412, as 409 (retry PutObject, restart a multipart upload), or as 404 when a concurrent delete wins [doc AWS-CW].
- In versioned buckets, a delete marker counts as absent [doc AWS-CW]. GCS `ifGenerationMatch=0` ignores noncurrent versions and is valid for writes only [doc GCS-PRE].
- If-Match needs `s3:GetObject` as well as PutObject [doc AWS-CW]. GCS preconditions can't be used with XML multipart (400) [doc GCS-PRE].
- The local filesystem can't do "if unchanged": object_store declined `PutMode::Update` locally because it would need locking (#423) [doc OS-423]. "If absent" maps to `O_EXCL` (paramiko `'x'`) [doc PARAMIKO].
- When the check runs in a streamed write is undefined in fsspec [doc FS-FEAT]. Hadoop calls `create(overwrite=false)` an unsafe lock on S3A [doc H-FS].
- Error kinds split: object_store `AlreadyExists` (Create) vs `Precondition` (Update) [doc OS]. The gocloud doc names a non-existent code [src GC-SRC].
- obstore's fsspec adapter ignores `mode=` [src OBS].

### OP-06 List children
- Directory markers: Hadoop S3A changed its marker policy in 3.3.1, 3.4.0 and 3.5.0, and the changes are not backward compatible [doc H-MARK]. cloudpathlib reported S3 directories as files (#148) [doc CP-HIST].
- A missing folder is an error in Hadoop, optional in pyarrow (`allow_not_found`), and tolerated in OpenDAL [doc].
- Prefixes match per segment in object_store (`foo/bar` ≠ `foo/bar_baz`) [doc OS]. adlfs and cloudpathlib fixed matches against a shared prefix [doc].
- Ordering:
  - not guaranteed in Hadoop or object_store [doc]
  - not lexicographic in S3 directory buckets [doc AWS-DIRB]
  - Azure sorts upper case first, and `/` lowest on HNS [doc AZ list-blobs]
  - gocloud promises lexicographic order [doc GC]
- Pages can be short or empty: Azure ≤5000, S3 ≤1000 [doc]. s3fs added per-page retries in 2026.9.0 [doc S3FS-CL].
- Listing caches go stale: the s3fs history of cache races [doc S3FS-CL], fsspec `use_listings_cache` [doc FS-FEAT].

### OP-07 Walk subtree
- Flat recursive vs per-level listing is a real split: object_store `list` vs `list_with_delimiter` (#5794), Hadoop `listFiles(recursive)` [doc]. Pruning needs per-level listing (cloudpathlib `lazy`) [doc CP-HIST].
- Depth limits: only fsspec `maxdepth`; pyarrow Python lacks C++ `max_recursion` [doc; obs].
- Whether directories are emitted varies: fsspec `withdirs` [doc FS-API]; the pyarrow selector excludes the base [doc PA].
- The cost is O(entries), and rewrites followed: fsspec MemoryFS `find` (#2055), gcsfs `find` CPU [doc].
- HNS differences: Azure errors on a file name in the middle of a prefix; gcsfs partial prefixes (#831) [doc].
- gocloud: listing may miss recent writes [doc GC].

### OP-08 Match by pattern
- fsspec 2023.9.0 changed glob (the content is unverified; adlfs adapted) [doc ADLFS-CL]. Later fixes: #1825, #2084, #2038, and `/` as the only separator (#2112) [doc FS-CL].
- fsspec 2026.9 rules [doc FS-API]:
  - `**` must be a whole component
  - `maxdepth` applies to the first `**`
  - a trailing `/` matches folders only
  - no braces
- pathlib 3.13 changed what a trailing `**` matches and added `full_match` [doc PY]. cloudpathlib moved to pathlib semantics (#154) [doc CP-HIST].
- Keys can contain glob metacharacters, e.g. `a[1].txt` [doc PY; inf]. gcsfs fixed special characters in `rm` [doc].
- Globs at the bucket level are refused: s3fs `glob("*")`, cloudpathlib #311 [doc]. cloudpathlib also rejects `..` in patterns [obs].
- Only GCS matches server-side (`match_glob`) [doc GCS].

### OP-09 Inspect
- "Is it a directory" is ambiguous: object_store moved to NotFound for directories (#4231) [doc OS-CL]. gocloud `IsDir` entries carry no other fields [doc GC].
- Probing directories costs calls; s3fs and adlfs retuned `isdir`/`exists`/`info` repeatedly [doc S3FS-CL, ADLFS-CL].
- S3 HEAD on a missing key returns 403 without `s3:ListBucket` [doc AWS-HEAD].
- mtime: S3 multipart Last-Modified is the initiation time [doc AWS-META]. Hadoop: granularity ~1 s, and mtime may be the create time or the PUT time [doc H-INTRO]. paramiko exposes minimal stat [doc].
- ETag format bugs: unquoted ETags in object_store 0.14.1 and adlfs; missing or empty ETags in s3fs and cloudpathlib [doc].
- Errors differ: cloudpathlib `stat()` on a directory raises `NoStatError`, not `FileNotFoundError` [obs]. pyarrow inspect never raises [doc PA].

### OP-10 Delete item
- A missing key:
  - Succeeds: S3 (DeleteObjects reports it deleted), OpenDAL, object_store S3 and in-memory [doc].
  - Errors: object_store local/GCP/Azure, gocloud, fsspec (MemoryFS aligned in #2140), Azure (`BlobNotFound`), GCS [doc].
  - Hadoop returns False [doc H-FS].
  - cloudpathlib `unlink` defaults to `missing_ok=True`, unlike pathlib [doc CP].
- Bulk limits are S3 1000, Azure 256, GCS 100. object_store's bulk delete broke Alibaba OSS (#731) and gained an opt-out (#734) [doc OS-CL].
- Partial failure inside a batch: object_store, s3fs #838, gcsfs [doc].
- On a versioned bucket, delete inserts a delete marker [doc AWS-DEL]. S3 DeleteObject `If-Match: *` fails on a delete marker [doc AWS-CD].
- Azure needs `delete_snapshots` when snapshots exist [doc AZ].

### OP-11 Delete folder tree
- Not atomic and O(n) on object stores: Hadoop says so for every non-HDFS filesystem, local included [doc H-INTRO, H-FS]. Azure HNS was built for atomic directory operations [doc AZ-HNS].
- Root and bucket deletion are special-cased: Hadoop root rules; pyarrow `accept_root_dir`, `allow_bucket_deletion` [doc].
- **Without `allow_bucket_deletion`, pyarrow S3 `delete_dir("bucket")` empties the bucket, then raises** [src PA-SRC; obs moto].
- Markers must also be deleted: s3fs #1005 [doc]. S3 directory buckets auto-delete empty parents [doc AWS-DIRB].
- Shape: OpenDAL merged tree delete into `delete_with(recursive)` [doc]. fsspec async `_rm` dropped `maxdepth` until #2106 [doc FS-CL].
- Azure HNS recursive delete is paginated (`x-ms-continuation`) [doc AZ Path-Delete]. Azure flat-namespace `DeleteDirContents` may partially delete [doc PA-CPP]. cloudpathlib `rmtree` failed above 256 blobs (#509) [doc].

### OP-12 Move / rename
- Copy + delete on object stores: not atomic, O(data), and timestamps and version ids change [doc H-FS, H-S3A, OS].
- **Atomic only on certain bucket or account types:**
  - Azure HNS: pyarrow move is HNS-only [doc PA-CPP].
  - GCS `move_blob`/`moveTo`, same bucket only; gcsfs changed `mv` three times in 2026 [doc GCS-MOVE, GCSFS-CL].
  - S3 `RenameObject`, Express One Zone only [doc AWS-REN].
  - OpenDAL S3 reports `Unsupported` [src].
- Overwriting differs: the SFTP v3 RENAME fails if the target exists [doc SFTP]; Hadoop is inconsistent [doc H-FS].
- sshfs falls back to cp, then rm, **in `finally:`**, so the source is deleted even when the copy failed [src SSHFS; consequence inf].
- cloudpathlib `replace` unlinks the target first, leaving a window with no object [src CP].
- Directory moves: refused by OpenDAL ("must be a file"), cloudpathlib and pyarrow S3/GCS [doc/src]. fsspec `mv` could delete files below `maxdepth` uncopied (Dev fix) [doc FS-CL].
- Same-path moves: OpenDAL `IsSameFile`, pyarrow OK, fsspec no-op [doc/src].
- GCS copy-based moves of Nearline/Coldline/Archive objects incur early-deletion charges [doc GCS-MOVE].

### OP-13 Copy within a store
- S3 CopyObject is atomic only up to 5 GB; beyond that `UploadPartCopy` is needed. s3fs split `_copy_basic` and `_copy_managed` [doc AWS-COPY; src S3FS]. pyarrow >5 GB handling was **not verified**.
- S3 copy errors can be embedded in a 200 OK [doc AWS-COPY]. Azure copies may be `pending`; adlfs does not poll [doc AZ-COPY; src ADLFS].
- copy-if-not-exists on S3 needs explicit object_store config. The `multipart` mode does not copy tags or attributes [doc OS-SRC].
- object_store local copy uses a hard link and cannot cross filesystems; sshfs needs shell `cp` [doc OS; src SSHFS].
- Metadata directive and SSE parameters: S3 `MetadataDirective`; cloudpathlib had to forward SSE-C arguments [doc].
- fsspec spec for trailing slashes and `recursive=` (#1225) [doc FS-COPY].

### OP-14 Transfer to or from local disk
- Temp-file strategy differs:
  - s3transfer uses a temp file, then rename [src B3/S3T].
  - fsspec `get_file` writes `lpath` directly, so a partial file can be left behind [src FS-SRC; inf].
  - gocloud fileblob's temp+rename fails across devices (the `NoTempDir` option) [doc GC].
- Progress callbacks and concurrency are part of the surface: fsspec `callback=`, boto3 `TransferConfig` [doc].
- Integrity: botocore 1.36.0 made CRC32 the default and stopped Content-MD5 [doc B3-CL]. Breakage of S3-compatible servers is a lead only, **not verified**. A GCS checksum mismatch raises `DataCorruption` [doc GCS].
- `..` in keys escaped the local download directory: cloudpathlib GHSA-r4f8-3xc4-c8vw (v0.25.0) [doc CP-HIST].
- fsspec `put_file(mode="create")` is check-then-write [src].

### OP-15 Transfer between stores
- The data passes through the client and often the local disk: fsspec `GenericFileSystem` uses a temp directory; cloudpathlib uses its cache [src FS-SRC; doc CP].
- fsspec `copy_file_op` defaults to `on_error="ignore"` [src]. Mixed backends were rejected late (#2302) [doc FS-CL].
- Same provider across buckets is a third case:
  - obstore's fsspec adapter raises "Bucket mismatch" [src OBS].
  - object_store copies within one store only [doc OS].
  - S3 cross-Region copy has restrictions [doc AWS-COPY].
  - Azure copies from any readable URL [doc AZ].
- pyarrow `copy_files` reads the destination as a file when the source is a file [doc PA]. That differs from fsspec's trailing-slash rules [inf].

### OP-16 Scope to a folder
- **`..` escapes were fixed in 2026 by three libraries:**
  - fsspec DirFS 2026.7.0, local only [src; wheels inspected].
  - OpenDAL fs 0.58.0 (#7684) [doc OD-CL].
  - cloudpathlib 0.25.0 (GHSA) [doc].
- pyarrow `SubTreeFileSystem` "makes no security guarantee", and `..` reaches S3 keys [doc PA; obs]. object_store LocalFileSystem follows symlinks outside the root [doc OS].
- Stripping the prefix from results has had bugs: object_store `PrefixStore::head` (#664/#686); the run of fsspec DirFS relative-name fixes [doc].
- Every method must be forwarded; DirFS and PrefixStore gained methods one at a time [doc FS-CL, OS-CL].
- gocloud `PrefixedBucket` closes the parent bucket [doc GC].

### OP-17 Hand items to other libraries
- Bridges drop data:
  - pyarrow `FSSpecHandler` has a TODO for metadata [src PA].
  - object_store_opendal drops unknown attributes and ContentLanguage [src OD].
  - obstore's fsspec adapter ignores `mode` [src OBS].
- Path conventions break: fsspec `ArrowFSWrapper` S3 parent paths (#2072); `root_marker` differs per protocol [doc/src].
- Adapters break when the wrapped library changes: fsspec fixed several pyarrow attribute removals [doc FS-CL]. object_store_opendal asks for the latest versions of both [doc].
- obstore calls its fsspec adapter "best effort" and second-class [doc OBS].
- cloudpathlib `fspath` is a cached copy; writes to it are not uploaded [doc CP].

### OP-18 Capability query
- Coverage: OpenDAL `capability()`, Hadoop `hasPathCapability`; everyone else none [doc].
- OpenDAL removed the native/full split in 0.58.0, and simulations set the flags [doc OD-CL; src].
- Capabilities depend on the path or bucket (HNS, S3 Express), not on the backend class [src PA, GCSFS, OD].
- Hadoop semantics: False = unknown, probes are cheap and side-effect free, and True can still fail [doc H-PCAP].
- OpenDAL flags were missed and fixed piecemeal [doc OD-CL].

### OP-19 Create an empty folder
- Coverage: OpenDAL `create_dir` (S3 simulated), pyarrow `create_dir`, fsspec `mkdir`/`makedirs`, Hadoop `mkdirs`. None in object_store or gocloud [doc/src].
- On S3 a folder is a zero-byte `key/` object [doc AWS-FOLD]. Hadoop's marker policy changed twice [doc H-MARK].
- Same intent, different results:
  - pyarrow writes markers and re-creates parent markers after deletes and moves [src; obs].
  - cloudpathlib silently does nothing [obs].
  - s3fs/gcsfs/adlfs `mkdir` means "create a bucket or container" [src/doc].
  - gcsfs `makedirs` on HNS buckets creates real folders (#906) [doc].
- OpenDAL needs a trailing `/`, and create_dir is recursive and idempotent [doc OD-SRC].
- gocloud escapes a trailing `/` on Azure and file storage, so a marker can't be written verbatim [doc GC].
- pyarrow `check_directory_existence_before_creation`: extra calls can hit GCS mutation rate limits [doc PA-CPP].
- Hadoop requires an atomic probe+create, which stores can't give [doc H-FS; inf].

### OP-20 User metadata
- Limits:
  - S3: 2 KB, keys stored lowercase, US-ASCII; non-ASCII values RFC 2047-encoded; immutable except by copy [doc AWS-META].
  - Azure: C# identifiers, case-insensitive, 8 KB [doc AZ-META].
  - GCS: 8 KiB, patchable in place [doc GCS].
- gocloud lowercases keys (duplicates are an error on write and arbitrary on read) and escapes per driver [doc GC].
- Updating metadata on S3 rewrites the object (s3fs `setxattr` = copy) [src S3FS].
- Support is uneven:
  - object_store Local → `NotImplemented` [src].
  - pyarrow S3 silently drops `x-amz-meta-*` [src; obs].
  - object_store `Attributes` are not returned by list [doc OS-SRC].
- System and user metadata share one namespace in object_store `Attribute` [doc]. gcsfs splits them [doc].

### OP-21 Store lifecycle
- Coverage: gocloud `Bucket.Close` (use after close → `FailedPrecondition`), vendor clients' `close()`. No close in object_store, OpenDAL `Operator`, fsspec or pyarrow [doc/src].
- fsspec's instance cache makes close a shared-state hazard: s3fs "force new session if it was explicitly closed" (#1002) [doc S3FS-CL].
- Closing async sessions at GC is fragile: s3fs `weakref.finalize` with private attributes; fsspec destructors may run after the loop stops [src; doc FS-FEAT].
- pyarrow has global `finalize_s3` (calls fail afterwards) registered with atexit [doc PA-CPP; src].
- Derived handles take over the lifecycle: gocloud prefix wrappers close the original [doc GC]. cloudpathlib `__del__` fixes [doc CP-HIST].

### OP-22 Native address mapping
- Coverage: fsspec `unstrip_protocol`/`url_to_fs`, pyarrow `from_uri`, OpenDAL `from_uri`/`info().root()`, object_store `parse_url` (no inverse found), gocloud `OpenBucket(url)`, smart_open `parse_uri`, cloudpathlib `as_uri`, Azure `BlobClient.url` [doc/src].
- "Native path" can mean a local cache copy (cloudpathlib `__fspath__`) [src CP].
- pyarrow `MakeUri` embeds the access key and secret in the URI [src PA-SRC]. smart_open accepts credentials in URIs [doc SO].
- Many URL forms map to one store: object_store `s3://`, `s3a://`, `az://`, `abfs://`, `https://…` [doc OS-SRC parse.rs].
- The logical key is not always the native key: object_store percent-encoding, gocloud `__0x__` escaping [doc].
- No library normalises `..`, `.` or `//` in pyarrow, smart_open or cloudpathlib [obs].

### OP-23 Native handle escape hatch
- Coverage:
  - gocloud `As`/`ErrorAs` plus `Before*` hooks [doc GC].
  - s3fs `.s3`, adlfs `.service_client` [src].
  - cloudpathlib `S3Client.client` [src].
  - smart_open in reverse: the caller injects the client [doc].
  - object_store concrete store types [doc].
  - Not offered: OpenDAL (no vendor SDK inside) and pyarrow Python [src].
- gocloud: `As` "implies that the resulting code is no longer portable". The type lists are part of the contract and change with SDK migrations [doc GC as.md; inf].
- The handle may be uninitialised or bound to a loop: s3fs async `.s3` raises before `set_session` [src].
- Errors are the most-used escape hatch: gocloud has a separate `ErrorAs` [doc].

### OP-24 Health check
- Coverage: OpenDAL `Operator::check()` (lists `/` with limit 1) and gocloud `Bucket.IsAccessible` (`ListPage` of size 1). Nothing else (vendor callers use `head_bucket` / `exists`) [src OD-SRC verified 2026-10-26; src GC-SRC].
- **The two disagree on NotFound:** OpenDAL treats it as healthy, gocloud returns false [src].
- "Healthy" means "list permission". S3 `HeadBucket` also needs `s3:ListBucket` and answers 400/403/404 with no body [doc AWS-HB]. A write-only credential reports unhealthy [inf].
- OpenDAL checks relative to its root; a missing root prefix is not an error [src].

---

## Catalogue entry × comparable

Legend:
- **name**: the comparable's counterpart
- **(g)**: gated per backend, bucket or account type, or configuration
- **(e)**: emulated or composite (e.g. copy+delete)
- **—**: none found
- **n/c**: not checked in the full texts read

Labels per cell are in notes 02–06.

| OP | fsspec | pyarrow.fs | OpenDAL | object_store | gocloud | smart_open | cloudpathlib | boto3 (S3) | Azure Blob | GCS |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 read | `open`, `cat_file` | `open_input_stream` | `read`, `reader` | `get`, `get_opts` | `NewReader`, `ReadAll` | `open('rb')` | `read_bytes`, `open` (whole download to cache) | `get_object` | `download_blob` | `download_as_bytes`, `Blob.open` |
| 02 read at offsets | `open`+`seek`, `cat_file(start,end)`, `cat_ranges` | `open_input_file`, `read_at` | `read_with(range)`, `Reader::fetch` (suffix simulated) | `get_range`, `get_ranges`, `GetRange` | `NewRangeReader` | `seek` (per transport) | `seek` on cached copy (no remote range) | `Range=` | `offset`/`length` | `start`/`end` (inclusive) |
| 03 write | `open('wb')`, `pipe_file`, `put_file` | `open_output_stream` | `write`, `writer` | `put`, `put_multipart` | `NewWriter`, `WriteAll`, `Upload` | `open('wb')` | `write_bytes`, `open('w')` (upload on close) | `put_object`, `upload_fileobj` | `upload_blob` | `upload_from_*`, `Blob.open('wb')` |
| 04 atomic replace | — (`transaction`, semi-atomic) | — (exception commits partial) | n/c | `put` (documented atomic) | `Writer.Close` (old blob readable until Close) | — | — | PUT atomic per key | Put Blob / commit block list (atomicity inf) | write (atomicity inf) |
| 05 conditional write | `mode="create"`/`xb` (g, impl-dependent) | — | `write_with(if_not_exists, if_match, …)` (g) | `PutMode::Create/Update` (g, config) | `WriterOptions.IfNotExist` (absent only) | — | `open('x')` (e, check-then-act) | `IfNoneMatch`/`IfMatch` | `overwrite=False`, `etag`+`match_condition` | `if_generation_match` |
| 06 list children | `ls` | `get_file_info(FileSelector)` | `list` | `list_with_delimiter` | `List(Delimiter="/")` | — (`iter_bucket`, S3) | `iterdir` | `list_objects_v2(Delimiter)` | `walk_blobs` | `list_blobs(delimiter)` |
| 07 walk (+depth) | `find`/`walk(maxdepth)` | `FileSelector(recursive)`, no depth in Python | `list_with(recursive)` (g, simulated) | `list`, no depth | `List` flat, no depth | — | `walk(lazy)`, `rglob`, no depth | flat prefix, no depth | `list_blobs`; HNS `get_paths(recursive)` | flat prefix, no depth |
| 08 pattern | `glob` | — | n/c (none found) | — | — | — | `glob`, `rglob` | — (prefix only) | — (prefix only) | `match_glob` |
| 09 inspect | `info`, `exists`, `isdir`, `isfile` | `get_file_info` (NotFound type) | `stat` (dir simulated) | `head` | `Attributes`, `Exists` | — (`to_boto3`) | `exists`, `is_file`, `is_dir`, `stat`, `info` | `head_object` | `get_blob_properties`, `exists` | `reload`, `exists` |
| 10 delete | `rm_file`, `rm` | `delete_file` | `delete` | `delete`, `delete_stream` | `Delete` | — | `unlink` | `delete_object(s)` | `delete_blob` | `Blob.delete` |
| 11 delete tree | `rm(recursive)` | `delete_dir`, `delete_dir_contents` | `delete_with(recursive)` (g, simulated) | — (list + `delete_stream`) | — | — | `rmtree` | — (list + `delete_objects`) | HNS `delete_directory` (g); flat: list + `delete_blobs` | — (list + batch) |
| 12 move | `mv` (e) | `move` (g: S3 files e; Azure HNS) | `rename` (g; S3 unsupported) | `rename_opts` (e) | — | — | `rename`/`replace`/`move` (e) | `rename_object` (g: S3 Express); else e | DataLake `rename_file`/`_directory` (g: HNS) | `move_blob` (atomic, same bucket); `rename_blob` (e) |
| 13 copy | `copy`, `cp_file` | `copy_file` | `copy` (g) | `copy_opts` | `Copy` | — | `copy`, `copytree` | `copy_object` (≤5 GB), `copy` | `start_copy_from_url` (may be pending) | `copy_blob`, `rewrite` |
| 14 to/from local | `get`, `put` | `copy_files` | n/c | — | `Download`, `Upload` (io streams) | — (stream copy) | `download_to`, `upload_from` | `upload_file`, `download_file` | `upload_blob`, `download_blob` | `upload_from_filename`, `download_to_filename` |
| 15 between stores | `generic` copy (via temp dir), `rsync` | `copy_files(src_fs, dst_fs)` | n/c | — (same store only) | — | `open` both ends | `copy` across clients (via cache) | `copy(SourceClient=)` (S3 only) | `start_copy_from_url` (any readable URL) | `copy_blob(destination_bucket)` (GCS only) |
| 16 scope | `DirFileSystem` | `SubTreeFileSystem` | `root` option | `PrefixStore` | `PrefixedBucket` | — | — | — | `ContainerClient`; HNS directory client (partial) | `Bucket` (bucket only) |
| 17 hand to libs | hub: `ArrowFSWrapper`, `get_mapper`, file objects | `PyFileSystem(FSSpecHandler)`, `filesystem=` | `object_store_opendal` adapter | (obstore fsspec adapter) | — | file-like objects | `fspath` (read-only cache copy) | file-like body | `StorageStreamDownloader` | `BlobReader`/`BlobWriter` |
| 18 capability query | — (`NotImplementedError` / no-op) | — (`ArrowNotImplementedError`) | `info().capability()` | — (`NotImplemented`/`NotSupported`) | — (`Unimplemented`) | — | — | — | — (`get_account_information`, account kind) | — |
| 19 create folder (g) | `mkdir`/`makedirs` (no-op or bucket; HNS real) | `create_dir` (S3/GCS marker) | `create_dir` (g, simulated on S3) | — | — | — | `mkdir` (silent no-op on S3/GCS) | — (`key/` convention) | DataLake `create_directory` (g: HNS) | `storage_control` folders (g: HNS) |
| 20 user metadata (g) | — generic (s3fs `setxattr`) | `metadata=` (g: S3 drops user keys) | `write_with(user_metadata)` (g) | `Attributes` `Metadata(k)` (g: Local NotImplemented) | `WriterOptions.Metadata` (lowercased) | per-transport kwargs | client-wide `extra_args` | `Metadata=` | `metadata=`, `set_blob_metadata` | `Blob.metadata`, `patch` |
| 21 lifecycle | — (instance cache; `clear_instance_cache`) | — (global `finalize_s3`) | — (Writer close/abort) | — (Drop) | `Bucket.Close` | file `close`; caller owns client | — (cache via GC) | `client.close()` | `close()`, context manager | `Client.close()` |
| 22 address mapping | `unstrip_protocol`, `url_to_fs` | `from_uri` | `from_uri`, `info().root()` | `parse_url`, `Path::from_url_path` | `OpenBucket(url)` | `parse_uri` | `as_uri`, `from_uri` | — | `BlobClient.url`, `from_blob_url` | `Blob.from_uri` (n/c) |
| 23 native handle | `.s3` (s3fs), `.service_client` (adlfs) | — | — (service, not SDK) | concrete store types | `As`, `ErrorAs`, `Before*` | `to_boto3`; inject client | `S3Client.client` | (is native) | (is native) | (is native) |
| 24 health check | — | — | `check()` (NotFound = OK) | — | `IsAccessible` (NotFound = false) | — | — | `head_bucket` | `ContainerClient.exists` | `lookup_bucket`, `Bucket.exists` |

---

## Advisory notes for the catalogue (not decisions)

1. **Possible additions or explicit exclusions:**
   - presign (8/10)
   - system properties next to OP-20 (7/10)
   - batch delete (6/10)
   - versioned access (6/10)
   - abort of an in-flight write (5/10)
   - append (5/10, always gated)
   - multi-range read (3/10)
2. **OP-05's scope.** All three vendor stores and OpenDAL attach conditions to read, delete, copy, rename and metadata update. Whether OP-05 is "conditional write" or "conditions" is a cut decision for the catalogue.
3. **OP-07's depth limit** is offered by one comparable (fsspec), and its cost on object stores is O(subtree) regardless of depth [doc H-INTRO; inf].
4. **OP-18 precedent.** OpenDAL's effective-only flags and pre-dispatch check, and Hadoop's "False = unknown, cheap, path-scoped" rules. Gates that depend on bucket type (HNS, S3 Express) show that a per-backend-class answer can be wrong.
5. **OP-24 precedent** is thin (2/10), and the two precedents disagree on NotFound.
6. **Shared decisions most often retrofitted, to decide once:**
   - `..` containment (three libraries in 2026)
   - missing-key delete (split across comparables)
   - exception typing in Python (bindings diverge)
   - retry coupled to idempotency
   - behaviour on exception during a streamed write (commit / upload / abort split across pyarrow / cloudpathlib / smart_open)

## Caveats

- **Runs:** nothing was run against real AWS, Azure or GCS. The [obs] items come from the moto S3 emulator and local disk.
- **Issue pages and GitHub API:** unreachable (403). Issue and PR numbers are cited through changelog entries; only object_store #423 was read in full.
- **Unreachable S3 error-code list:** the S3 error-code strings (`PreconditionFailed`, `InvalidRange`) are unverified.
- **Not confirmed in the fetched pages:**
  - the general rule that deleting a missing S3 key returns 204
  - S3 behaviour for a range starting past EOF
- **Unverified:**
  - the content of fsspec's 2023.9.0 glob change
  - pyarrow copies over 5 GB
  - reports that botocore 1.36 broke S3-compatible servers
- **Conflicts:**
  - Azure `retry_total` default: README says 10, Learn says 3.
  - Hadoop pages were read at both 3.3.5 ("stable") and 3.5.0 ("current").
- **Versions:**
  - smart_open docs come from `develop`, which may be ahead of 8.0.4.
  - Some fsspec, OpenDAL and object_store source was read on main or master, possibly slightly ahead of the release.
- **Correction to the workflow track (notes 01):**
  - A 1–2 vote refuted the bundled claim about gocloud `SignedURL`/`Unimplemented`. Track 04 then confirmed `SignedURL` → `Unimplemented` in the v0.47.0 source and docs, and that is what this report uses.
  - Track 01's statement that gocloud returns `PreconditionFailed` is superseded: the code is `FailedPrecondition` (verified in source).
- **Version-sensitive areas:** the pre-1.0 crates (object_store, OpenDAL) and the S3 conditional-operation matrix change often.
