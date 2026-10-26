# Track 06: Q5 pitfalls for OP-12..OP-24

Scope: object-store and filesystem behaviours that made comparable libraries **change or split** an
operation. These are notes for the per-entry design session. They contain **no proposals of semantics**.
remote-store's own code and docs were not consulted.

Accessed 2026-10-26. Full texts (docs pages, changelogs, source files) were downloaded with curl into the
scratchpad and read by section. Search-engine extracts were not used. The GitHub REST API and issue pages
were not reachable from this session (`gh api` returned "GitHub access to this repository is not enabled").
Issue and PR numbers below are therefore cited **through changelog entries**. The issue texts themselves
were not read and are marked *unreachable*.

Labels:
- **[documented]**: stated in a doc page, spec, changelog entry, or API docstring.
- **[observed]**: read in the library's source code at the cited revision. Nothing was executed, except
  where a released wheel was inspected (this is stated where it applies).
- **[inference]**: my reading, not stated by the source.
- **unreachable**: the source could not be fetched.

## Sources and versions

Released versions come from PyPI, crates.io and proxy.golang.org, queried 2026-10-26. Source files come
from `main`/`master`/`develop` on raw.githubusercontent.com, fetched 2026-10-26. The source may be
slightly ahead of the release.

| Key | Source | Version / date |
|---|---|---|
| HADOOP-FS | hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html | Hadoop 3.5.0 (banner) |
| HADOOP-INTRO | …/filesystem/introduction.html | 3.5.0 |
| HADOOP-PATHCAP | …/filesystem/pathcapabilities.html | 3.5.0 |
| HADOOP-S3A | hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html | 3.3.5 (banner on "stable") |
| HADOOP-MARKERS | hadoop.apache.org/docs/current/hadoop-aws/tools/hadoop-aws/directory_markers.html | 3.5.0, last published 2026-03-24 |
| OS-LIB / OS-PREFIX / OS-ATTR / OS-PARSE / OS-PATH / OS-LOCAL / OS-AWS-PRECOND | raw.githubusercontent.com/apache/arrow-rs-object-store/main/src/{lib.rs, prefix.rs, attributes.rs, parse.rs, path/mod.rs, local.rs, aws/precondition.rs} | object_store 0.14.2 (crates.io, 2026-09-15); Cargo.toml on main = 0.14.2 |
| OS-CL | …/arrow-rs-object-store/main/CHANGELOG.md + CHANGELOG-old.md | to v0.14.2 (2026-09-11) |
| FSSPEC-SPEC / -DIRFS / -ARROW / -GENERIC | raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/{spec.py, implementations/dirfs.py, implementations/arrow.py, generic.py} | fsspec 2026.9.0 (PyPI 2026-09-18) |
| FSSPEC-COPY | …/filesystem_spec/master/docs/source/copying.rst | same |
| FSSPEC-ASYNC | …/docs/source/async.rst | same |
| FSSPEC-CL | …/docs/source/changelog.rst | "Dev" section (unreleased) down to 2026.9.0 and older |
| FSSPEC-WHL | fsspec wheels 2025.12.0, 2026.3.0, 2026.6.0, 2026.7.0, 2026.9.0 from PyPI (inspected with `python3 -I` zipfile) | as named |
| S3FS | raw.githubusercontent.com/fsspec/s3fs/main/s3fs/core.py; docs/source/{changelog,index}.rst | s3fs 2026.9.0 |
| GCSFS | raw.githubusercontent.com/fsspec/gcsfs/main/gcsfs/{core.py, extended_gcsfs.py}; docs/source/changelog.rst | gcsfs 2026.10.1 (PyPI); changelog top = 2026.10.0 |
| ADLFS | raw.githubusercontent.com/fsspec/adlfs/main/adlfs/spec.py | adlfs 2026.8.0 |
| SSHFS | raw.githubusercontent.com/fsspec/sshfs/main/sshfs/spec.py | sshfs 2026.8.0 |
| OBSTORE-FSSPEC | raw.githubusercontent.com/developmentseed/obstore/main/obstore/python/obstore/fsspec.py | obstore 0.12.0 (PyPI 2026-10-15) |
| PA-PYX / PA-PY / PA-S3PYX | raw.githubusercontent.com/apache/arrow/main/python/pyarrow/{_fs.pyx, fs.py, _s3fs.pyx} | pyarrow 26.0.0 (PyPI 2026-10-09) |
| PA-H / PA-CC | …/apache/arrow/main/cpp/src/arrow/filesystem/{filesystem.h, filesystem.cc, s3fs.h, s3fs.cc, azurefs.h, azurefs.cc, gcsfs.h, gcsfs.cc, path_util.cc} | same |
| OD-OP / OD-CAP / OD-INFO / OD-PATH / OD-SIM / OD-BUILDER | raw.githubusercontent.com/apache/opendal/main/core/core/src/{types/operator/operator.rs, types/capability.rs, types/operator/info.rs, raw/path.rs, layers/simulate.rs, types/operator/builder.rs} | opendal 0.59.5 (crates.io 2026-10-18) |
| OD-S3 / OD-FS / OD-SFTP | …/opendal/main/core/services/{s3,fs,sftp}/src/backend.rs, services/fs/src/core.rs | same |
| OD-OSSTORE | …/opendal/main/integrations/object_store/{README.md, src/store.rs} | object_store_opendal on main |
| OD-CL | …/opendal/main/CHANGELOG.md | to v0.59.1 (2026-09-05) |
| GOCLOUD | raw.githubusercontent.com/google/go-cloud/master/blob/{blob.go, driver/driver.go, s3blob/s3blob.go, azureblob/azureblob.go, fileblob/fileblob.go}; internal/website/content/concepts/as.md | gocloud.dev v0.47.0 (2026-10-14) |
| CLOUDPATH | raw.githubusercontent.com/drivendataorg/cloudpathlib/master/{cloudpathlib/cloudpath.py, cloudpathlib/s3/s3client.py, HISTORY.md} | cloudpathlib 0.26.0 (2026-10-02) |
| SMART | raw.githubusercontent.com/piskvorky/smart_open/develop/README.md | smart_open 8.0.4 |
| PARAMIKO | raw.githubusercontent.com/paramiko/paramiko/main/paramiko/sftp_client.py | paramiko 5.1.0 |
| SFTP-02 | datatracker.ietf.org/doc/html/draft-ietf-secsh-filexfer-02 | IETF draft (the version OpenSSH implements) |
| S3T | raw.githubusercontent.com/boto/s3transfer/develop/s3transfer/{download.py, utils.py}; boto/boto3/develop/boto3/s3/transfer.py | s3transfer 0.19.3, boto3 1.43.118 |
| BOTOCORE-CL | raw.githubusercontent.com/boto/botocore/develop/CHANGELOG.rst | entry 1.36.0 |
| AWS-COPY | docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html; …/userguide/copy-object.html | accessed 2026-10-26 |
| AWS-META | docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html | accessed 2026-10-26 |
| AWS-FOLDERS | docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html | accessed 2026-10-26 |
| AWS-RENAME | docs.aws.amazon.com/AmazonS3/latest/API/API_RenameObject.html | accessed 2026-10-26 |
| AWS-HEADBUCKET | docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html | accessed 2026-10-26 |
| AZ-META | learn.microsoft.com/en-us/rest/api/storageservices/setting-and-retrieving-properties-and-metadata-for-blob-resources; …/naming-and-referencing-containers--blobs--and-metadata | accessed 2026-10-26 |
| AZ-COPY | learn.microsoft.com/en-us/rest/api/storageservices/copy-blob | accessed 2026-10-26 |
| AZ-HNS | learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace | accessed 2026-10-26 |
| GCS-MOVE / GCS-FOLDERS / GCS-QUOTAS | cloud.google.com/storage/docs/{copying-renaming-moving-objects, folders-overview, quotas} | accessed 2026-10-26 |

---

## OP-12 move / rename

1. **On object stores, rename is copy + delete: it is not atomic and costs O(data).** Hadoop's spec says
   that the core rename "MUST be atomic". Its object-store notes say that directory rename and delete are
   applied "a file at a time, and are not atomic. If an operation fails part way through … the object store
   reflects the partially completed operation". Callers assume O(1), but on stores rename is "more likely to
   be O(child-entries)" [documented, HADOOP-FS §rename "Concurrency requirements"; HADOOP-INTRO
   "Atomicity"]. S3A docs: the time to rename a directory is "proportional to the number of files … and the
   size of the files", and "Directory renames are not atomic" [documented, HADOOP-S3A]. Copy-based renames
   can also change timestamps (HADOOP-INTRO) and version ids (HADOOP-S3A: "copied files may have a different
   version number") [documented].
   - object_store: `rename_opts` defaults to `copy_opts` and then `delete`. "It may not check when deleting
     source that it was the same object that was originally copied" [documented, OS-LIB docstring;
     observed, default impl].
   - pyarrow S3 `Move`: files only. The source comment says "We don't implement moving directories as it
     would be too expensive". It does CopyObject + DeleteObject, then `EnsureParentExists(src)` to recreate a
     directory marker the delete may have removed [observed, PA-CC s3fs.cc `S3FileSystem::Move`]. pyarrow GCS
     `Move` returns IOError "Moving directories or buckets cannot be implemented in GCS" [observed, gcsfs.cc].
2. **Split by bucket or account type: hierarchical namespaces have an atomic rename, flat ones do not.**
   - Azure: HNS enables "atomic directory manipulation" and processes renames "by updating a single entry".
     Without HNS, "applications must process potentially millions of individual blobs" [documented, AZ-HNS].
     pyarrow `AzureFileSystem::Move` is **HNS-only**: on flat accounts it returns `NotImplemented` "… without
     Hierarchical Namespace support (see arrow/issues/40405)". Cross-container moves are also
     NotImplemented. HNS moves use leases so the pre-checks and the rename are atomic [documented, PA-H
     azurefs.h Move docstring; observed, azurefs.cc].
   - GCS: "some tools perform atomic object move operations, other tools simulate … by copying … and then
     deleting". Copy-based moves of Nearline/Coldline/Archive objects "can incur early deletion charges",
     but atomic moves do not. HNS buckets add "atomic folder renames" [documented, GCS-MOVE, GCS-FOLDERS].
     gcsfs **changed** its `mv` three times in 2026: "make mv_file atomic (#758)" (2026.3.0); "use moveTo in
     standard buckets (#800)" (2026.4.0); and HNS support on by default from 2026.3.0
     (`ExtendedGcsFileSystem`) [documented, GCSFS changelog]. In code, `_mv_file` tries
     `POST …/moveTo/…` and falls back to copy/delete on any non-NotFound error, logging a warning. The HNS
     `_mv` uses `rename_folder` only when the source is a folder in the same bucket; otherwise it falls back
     to the object-level mv [observed, GCSFS core.py / extended_gcsfs.py].
   - S3: `RenameObject` exists, but it "is only supported for objects stored in the S3 Express One Zone
     storage class" (directory buckets). It supports `If-None-Match` to avoid overwrite [documented,
     AWS-RENAME]. General-purpose S3 has no rename, and console "folders … can't be renamed" [documented,
     AWS-FOLDERS]. OpenDAL's S3 service returns `Unsupported` for `rename` [observed, OD-S3 backend.rs].
3. **Overwrite-on-existing differs by backend, and libraries split the operation into two.**
   - Hadoop: renaming a file onto an existing file is specified to fail. Local FS replaces it; HDFS "returns
     false". There is "no consistent behavior" when the destination's parent is missing: HDFS returns false,
     local and S3A create parents, others raise [documented, HADOOP-FS].
   - SFTP: the v3 protocol RENAME says "It is an error if there already exists a file with the name specified
     by newpath" [documented, SFTP-02]. paramiko exposes two methods, `rename` ("must not exist already") and
     `posix_rename` (OpenSSH extension, "will be overwritten") [documented, PARAMIKO docstrings]. sshfs `_mv`
     tries `posix_rename`. On `SFTPOpUnsupported` it falls back to `_cp_file` (a remote shell `cp` over
     exec) and then `_rm_file` **inside a `finally:` block**, so the source is deleted even if the copy
     raised [observed, SSHFS spec.py `_mv`; data-loss consequence is inference].
   - object_store split `rename` / `rename_if_not_exists`. In 0.13.0 it consolidated them into
     `rename_opts(RenameTargetMode::{Overwrite, Create})` ("refactor!: Consolidate … => rename_opts #555")
     [documented, OS-CL v0.13.0]. OpenDAL added `rename_with_if_not_exists` / "conditional rename option"
     (#7815, RFC #7818) in v0.58.0 [documented, OD-CL; OD-CAP field]. pyarrow `move`: if the destination is a
     non-empty directory it errors; if it has the same type it is replaced; otherwise "unspecified
     (implementation-dependent)" [documented, PA-PYX `move` docstring].
4. **Directory moves: some libraries refuse them, others recurse; maxdepth bugs.** OpenDAL `rename`:
   "`from` and `to` must be a file" [documented, OD-OP]. cloudpathlib `replace`/`rename` raise
   `CloudPathIsADirectoryError` ("rename/replace the files recursively"). It **unlinks an existing target
   first and then moves**, so there is a window where neither exists [observed, CLOUDPATH cloudpath.py
   `replace`; window is inference]. It added separate `move`/`move_into` in v0.23.0 [documented, CLOUDPATH
   HISTORY]. An older fix: "Prevent data loss when renaming by skipping files that would be renamed to the same
   thing (#277/#278)", v0.11.0 [documented]. fsspec `mv` = `copy(..., on_error="raise")` then `rm`. Dev
   changelog: "Keep files deeper than `maxdepth` in the source of a recursive `mv` instead of deleting them
   uncopied". Earlier entries are "mv() should not swallow errors (#1576)" and "remove mv_file (#1585)"
   (2024.5.0) and "fix: pass on_error when mv calls copy (#2030)" (2026.6.0) [documented, FSSPEC-CL;
   observed, spec.py `mv`]. Dev changelog: "Raise an error when WebHDFS refuses a rename instead of reporting
   success (#2327)" [documented].
5. **Same-path move.** OpenDAL `rename`/`copy` raise `IsSameFile` [documented, OD-OP]. pyarrow S3 returns OK
   [observed]. fsspec logs and does nothing [observed]. In Hadoop, a file renamed to itself returns True,
   and a directory renamed onto itself has an "undefined" result (POSIX False, HDFS True) [documented,
   HADOOP-FS].

## OP-13 copy within a store

1. **The S3 single-request copy limit is 5 GB, which forces a split into a multipart copy.** CopyObject copies
   "up to 5 GB in size in a single atomic action". Above that "you must use the multipart upload Upload
   Part - Copy" [documented, AWS-COPY]. s3fs has `_copy_basic` ("Not allowed where the origin is >5GB -
   use copy_managed") and `_copy_managed`, which takes blocks of 5 MB to 5 GB. Its changelog has "smaller
   threshold for copy_managed (#921)", and it adds an optional `preserve_etag` that replays the source's
   part layout [observed, S3FS core.py; documented, S3FS changelog]. OpenDAL S3 declares `copy_can_multi`,
   `copy_multi_min_size = 5 MiB` and `copy_multi_max_size = 5 GiB` capabilities [observed, OD-S3]. pyarrow S3
   `CopyFile` uses CopyObject. It has a source comment "XXX Investigate UploadPartCopy?" (in the append
   path) [observed, PA-CC]. Whether pyarrow handles >5 GB copies was not verified (unknown).
2. **A copy can fail inside a 200 response, and it is not always synchronous.** S3: "If the error occurs during
   the copy operation, the error response is embedded in the 200 OK response. For example, in a cross-region
   copy, you may encounter throttling and receive a 200 OK response" [documented, AWS-COPY]. Azure Copy Blob
   returns `x-ms-copy-status: <success ¦ pending>`. Pending copies are polled with Get Blob Properties or
   cancelled with Abort Copy Blob [documented, AZ-COPY]. adlfs `_cp_file` calls `start_copy_from_url` and
   returns without polling the copy status [observed, ADLFS spec.py; that a pending copy may be reported as
   done is inference].
3. **copy-if-not-exists is backend-dependent, and libraries split it out.** object_store `copy_if_not_exists`:
   "If atomic operations are not supported by the underlying object storage (like S3) it will return an
   error" [documented, OS-LIB]. For S3 it needs explicit config `S3CopyIfNotExists`: a `header` variant for
   R2-style headers, `header-with-status`, or `multipart`. The multipart variant "does not copy tags or
   attributes" and makes "only a best effort attempt to clean up the multipart upload" [documented,
   OS-AWS-PRECOND]. In 0.13.0, `copy` and `copy_if_not_exists` became `copy_opts(CopyMode)` (#548), "Add
   CopyOptions (#116)" [documented, OS-CL]. Earlier fixes: DynamoDB-lock based support (#4880) and "Allow
   403 Forbidden for copy_if_not_exists S3 status code (#5132)" [documented, OS-CL-old]. OpenDAL has
   `copy_with_if_not_exists` and others as capability flags [documented, OD-CAP].
4. **Local "copy" may not be a byte copy.** object_store `LocalFileSystem::copy_opts` "is implemented using
   `std::fs::hard_link`, and therefore does not support copying across filesystem boundaries" [documented,
   OS-LOCAL]. sshfs copies with a remote shell `cp` over SSH exec, which needs shell access beyond SFTP
   [observed, SSHFS].
5. **Metadata and encryption parameters on copy.** S3 CopyObject has `x-amz-metadata-directive`
   (COPY/REPLACE). Cross-Region copies of SSE-KMS objects are restricted in the console [documented, AWS-COPY,
   AWS copy-object guide]. cloudpathlib v0.25.0 "Fixed S3 copy and move operations to forward copy-specific
   extra args such as `CopySourceSSECustomerKey`" (#500/#527/#576) [documented, CLOUDPATH HISTORY]. On a
   same-path "copy", cloudpathlib does a `copy_from` with `MetadataDirective="REPLACE"` (a touch)
   [observed, CLOUDPATH s3client.py].
6. **Trailing-slash and recursive semantics for directory copy.** fsspec wrote a full spec of cp/get/put
   behaviour (scenarios 1a–1h, 2a–…). The trailing slash on a source directory means "contents only".
   `recursive=True` is required, "otherwise the call does nothing". A target without a trailing slash is
   read as a filename [documented, FSSPEC-COPY]. The changelog records this as "#1225, comprehensive docs of
   expected behaviour of cp/get/put and tests" (2023.4.0) and "#1199, 1163, get/put/cp consistency and empty
   directories" (2023.3.0) [documented, FSSPEC-CL]. Default `on_error` is "ignore" when `recursive=True`
   and "raise" otherwise [observed, spec.py `copy`].

## OP-14 transfer to/from local disk

1. **Partial files and temp-file strategy differ.** s3transfer downloads into a temp file named with a random
   8-hex suffix. It then runs an `IORenameFileTask`, and the temp file is removed on failure [observed,
   S3T download.py / utils.py]. fsspec's default `get_file` opens `lpath` directly with `"wb"`. There is no
   temp file and no cleanup on error [observed, FSSPEC-SPEC `get_file`; partial file left behind is
   inference]. gocloud fileblob (local writes) writes a temp file and renames it on Close. With the default
   `os.TempDir` on another mount, "the `os.Rename` will fail with `invalid cross-device link`", so the
   `NoTempDir` option was added [documented, GOCLOUD fileblob.go package doc].
2. **Progress and concurrency knobs are part of the operation's surface.** fsspec `get_file`/`put_file` take
   `callback=` (set_size / relative_update). Changelog: "callbacks/branching kwargs handling and scopes
   (#1496, 1495, 1460)" (2024.2.0) and "Accept a `callback=` on the caching filesystems" (Dev) [observed,
   spec.py; documented, FSSPEC-CL]. sshfs maps the callback to asyncssh `progress_handler` [observed]. boto3
   `TransferConfig` defaults: `multipart_threshold=8 MiB`, `max_concurrency=10`, `multipart_chunksize=8 MiB`,
   and a `preferred_transfer_client` (auto/CRT) [observed, boto3 s3/transfer.py]. s3fs 2026.1.0 added
   "concurrent downloads in get/cat_file (#1007)" [documented, S3FS changelog].
3. **Integrity checks changed underneath callers.** botocore 1.36.0: the S3 client now "always calculate[s] a
   CRC32 checksum by default for operations that support it" and validates response checksums. It "will no
   longer automatically compute and populate the Content-MD5 header". This can be turned off with
   `request_checksum_calculation` / `response_checksum_validation` = `when_required` [documented,
   BOTOCORE-CL 1.36.0]. That this broke some S3-compatible servers is a widely reported lead, but it is
   **not verified** on a full text here. object_store: "Multi-part s3 uploads fail when using checksum
   (#6793)"; "Add CRC64NVME checksum support (#633)" (0.14.x) [documented, OS-CL]. s3fs: "allow checksum
   error to retry (#858)" [documented, S3FS changelog].
4. **Directory transfer: destination-is-directory rules and path traversal.** cloudpathlib `download_to`:
   v0.4.x "Fixed `download_to` … when source is a file and destination is a directory (#121)"; v0.19.0
   "Fixed `download_to` to check for the existence of the cloud file (#430/#433)". v0.25.0 **security
   fix GHSA-r4f8-3xc4-c8vw**: keys with `..` "could escape … a download destination
   (`download_to`/`copytree`/`copy`/`move` to a local path)". Downloads now raise
   `CloudPathLocalPathTraversalError` [documented, CLOUDPATH HISTORY; observed,
   `_ensure_local_path_within_base` in `download_to`]. fsspec `get_file` creates local parent dirs with
   `LocalFileSystem(auto_mkdir=True)` ("#1282, create parent directories in get_file") [observed; documented,
   FSSPEC-CL].
5. **Put with "create" mode is check-then-write.** fsspec `put_file(mode="create")` does
   `if self.exists(rpath): raise FileExistsError` and then writes [observed, FSSPEC-SPEC; race is inference].
   obstore's fsspec `_pipe_file` accepts `mode` but ignores it (`# noqa: ARG002`) and always calls `put`
   [observed, OBSTORE-FSSPEC].
6. **A local cache used as the transfer mechanism.** cloudpathlib's default I/O downloads to a local cache.
   v0.26.0+/UNRELEASED adds `FileCacheMode.streaming`, in which "`fspath` raises
   `CloudPathNotImplementedError`" and copy/rename "stream between clients" [documented, CLOUDPATH HISTORY
   UNRELEASED].

## OP-15 transfer between stores

1. **Cross-store copy goes through the client machine (and often local disk).** cloudpathlib v0.4.1:
   `copy`/`copytree` between clients — "the file transits through the local machine" [documented,
   CLOUDPATH HISTORY]. fsspec `GenericFileSystem._cp_file`: if the two filesystems differ, it uses
   `copy_file_op`, which `get_file`s into a `tempfile.TemporaryDirectory` and then `put_file`s. The whole
   object lands on local disk [observed, FSSPEC-GENERIC].
2. **Default error handling for bulk cross-store copy is "ignore".** `copy_file_op(..., on_error="ignore")`
   is the default signature. `_cp_file` passes `on_error="raise"`, but direct callers of `copy_file_op`
   get swallowed errors [observed, FSSPEC-GENERIC].
3. **Mixed backends in one call were rejected late.** fsspec Dev: "Reject mixed source or destination
   backends in `GenericFileSystem.copy` (#2302)". Also "#1345, implement async-sync and async-async generic cp
   and rsync" and Dev "Reject `generic.rsync` source names whose '..' segments would place …" [documented,
   FSSPEC-CL].
4. **pyarrow has a separate free function for this.** `pyarrow.fs.copy_files(source, destination,
   source_filesystem=, destination_filesystem=, chunk_size=1 MiB, use_threads=True)`. When the source is a
   file, "`destination` is also interpreted as the destination file (not directory)". "Directories will be
   created as necessary" [documented, PA-PY docstring]. *Inference*: the destination's directory semantics
   differ from fsspec's trailing-slash rules (FSSPEC-COPY).
5. **Same-provider but cross-bucket/region/account is a third case.** obstore's fsspec `_cp_file` raises
   `ValueError("Bucket mismatch …")` across buckets [observed, OBSTORE-FSSPEC]. object_store's
   `copy`/`rename` are documented "in the same object store" only [documented, OS-LIB]. S3 server-side
   cross-Region copies exist but have restrictions: transfer acceleration "does not support cross-Region
   copies", "VPC endpoints don't support cross-Region requests", and errors can arrive inside 200 [documented,
   AWS-COPY]. adlfs `_cp_file` builds a different container client when the containers differ and copies by
   URL [observed]. The Azure URL-copy authorization requirements across accounts were not read (unknown).

## OP-16 scope a store to a folder

1. **Escape via `..` and its fixes, all in 2026.**
   - fsspec `DirFileSystem._join` raises `ValueError("… escapes the … root")` when `..` would climb above
     the root, **only when the wrapped fs is `LocalFileSystem`**. The code comment reads: "on object stores
     it is a literal path part" [observed, FSSPEC-DIRFS]. Wheel inspection shows `_escapes_root` is absent
     in 2025.12.0, 2026.3.0 and 2026.6.0 and present in 2026.7.0 and 2026.9.0 [observed, FSSPEC-WHL].
   - OpenDAL v0.58.0: "fix(services/fs): confine object keys to the configured root by rejecting parent-dir
     traversal (#7684)" and the same for compfs/monoiofs (#7702) [documented, OD-CL]. `root_join` comment:
     `PathBuf::join` is lexical, "so a key such as `../../etc/passwd` would otherwise escape" [observed,
     OD-FS core.rs]. OpenDAL's generic `normalize_path` collapses `//` and trims leading `/` and whitespace,
     but does not touch `..` [observed, OD-PATH].
   - cloudpathlib v0.25.0 GHSA-r4f8-3xc4-c8vw: "some backends (e.g. Google Cloud Storage) accept `..`",
     which allowed escape from the local cache dir [documented].
   - pyarrow `SubTreeFileSystem`: "makes no security guarantee. For example, symlinks may allow to 'escape'
     the subtree" [documented, PA-PYX/PA-H]. `ValidateSubPath` rejects only URIs, not `..` [observed,
     PA-CC filesystem.cc; whether `..` escapes on LocalFileSystem is inference].
   - object_store `Path` forbids `.`/`..` segments: `Path::from("foo/../bar")` → `foo/%2E%2E/bar`
     (percent-encoded, i.e. a literal key) [documented, OS-PATH]. `LocalFileSystem` "Symlinks that resolve to
     paths outside the root **will** be followed" [documented, OS-LOCAL].
2. **Stripping the prefix from results has had bugs.** object_store `PrefixStore`: "PrefixStore::head doesn't
   strip prefix from meta.location (#664)", fixed by "strip_meta from get_opts result in PrefixStore (#686)"
   (0.14.0) [documented, OS-CL]. `strip_prefix` returns the path unchanged if it does not match the prefix
   [observed, OS-PREFIX]. pyarrow `SubTreeFileSystem::StripBase` raises `UnknownError` "Underlying
   filesystem returned path … which is not a subpath" [observed, PA-CC]. fsspec DirFileSystem `_relpath` uses
   `assert path.startswith(prefix)` and special-cases S3 paths without a leading `/` [observed]. Its
   changelog shows a run of relative-name fixes: "Return relative names from DirFileSystem.glob and find
   (#2127)", "Make names relative in DirFileSystem.walk(detail=True) (#2160)", "dir/info consistency in dirfs
   (#1798)", "paths without '/' in dirFS (#1638)" [documented, FSSPEC-CL].
3. **Wrapping can consume the parent.** gocloud `PrefixedBucket(bucket, prefix)`: "bucket will be closed and no
   longer usable after this function returns". The same holds for `SingleKeyBucket` [documented, GOCLOUD
   blob.go]. *Inference*: scoping interacts with lifecycle (OP-21).
4. **Delegation gaps: every wrapped method must forward.** fsspec changelog: DirFileSystem missing
   `open_async` (#1698), `pipe_file` (#1465), delete/write_test (#2022). "Delegate `sizes` and `cat_ranges`"
   (#2144). "Forward the wrapped filesystem's `local_file` flag" (#1110). "Report `DirFileSystem.async_impl`
   from the wrapped filesystem" [documented, FSSPEC-CL]. object_store PrefixStore gained `list_with_offset`
   (#4203), `MultipartStore` (#587) and `Signer` (#738/#739) one at a time [documented, OS-CL].
5. **Root conventions differ.** OpenDAL `info().root()` is "in a format like `/path/to/dir/`" [documented,
   OD-INFO]. fsspec's `ArrowFSWrapper` sets `root_marker = ""` for `{"gcs","s3"}` [observed, FSSPEC-ARROW].
   object_store PrefixStore was renamed from `PrefixObjectStore` (#3870) [documented, OS-CL-old].

## OP-17 hand items to other libraries (pyarrow FileSystem / fsspec / object_store adapters)

1. **Bridges lose metadata and options.** pyarrow `FSSpecHandler`: the source comment reads
   `# TODO can we read/pass metadata (e.g. Content-Type) in the methods below?`. Its `move` maps to
   `fs.mv(src, dest, recursive=True)`, and `create_dir` maps to `fs.mkdir(create_parents=recursive)` with
   `FileExistsError` swallowed [observed, PA-PY]. OpenDAL's `object_store_opendal` maps
   `Attribute::ContentLanguage` to "no support" (skipped). Unknown attributes are dropped (`_ => {}`), and
   conditional put without an etag gives `NotSupported` [observed, OD-OSSTORE store.rs].
2. **Path conventions break across the bridge.** fsspec: "Fix ArrowFSWrapper parent paths for S3 (#2072)"
   (2026.7.0). `_EMPTY_ROOT_MARKER_FILESYSTEMS = {"gcs","s3"}` [documented, FSSPEC-CL; observed,
   FSSPEC-ARROW]. pyarrow `PathFromUri` "only checks to ensure the URI scheme is valid. It will not detect
   inconsistencies like a mismatching region or endpoint override" [documented, PA-H].
3. **Adapters break when the wrapped library changes.** fsspec 2026.9.0: "Compute
   `HadoopFileSystem.fsid` … instead of accessing attributes no longer exposed by PyArrow (#1870)". "Mirror
   `readinto` from the PyArrow stream onto ArrowFile (#2111)". "Forward an Arrow file's `flush` and
   `closed` state (#2134)". "fix parquet tests for pyarrow 20 (#1831)" [documented, FSSPEC-CL].
   `object_store_opendal` README: "Please make sure to always use the latest versions of both" [documented,
   OD-OSSTORE README].
4. **The adapters warn that they are second-class.** obstore's fsspec module: "best effort and may not provide
   the same performance". It quotes object_store's "Why not a Filesystem Interface?" and says "Only where
   this is not possible should users fall back to this fsspec integration" [documented, OBSTORE-FSSPEC].
5. **Async/sync impedance.** fsspec async doc: destructors "will run from normal code, and possibly after
   the loop has stopped/closed". fsspec added "async wrapper for sync FSs (#1745)" (2024.12.0) and multiple
   follow-ups [documented, FSSPEC-ASYNC, FSSPEC-CL].

## OP-18 ask what a store supports (capability query)

Coverage names:

| Library | Name of the facility |
|---|---|
| OpenDAL | `Operator::info().capability()` → `Capability` struct (≈100 bool/limit fields) [observed, OD-CAP/OD-INFO] |
| Hadoop | `PathCapabilities.hasPathCapability(path, "fs.capability.…")`, and `StreamCapabilities` [documented, HADOOP-PATHCAP] |
| object_store | none. Errors `NotSupported` / `NotImplemented{operation, implementer}` at call time, plus backend config enums (`S3CopyIfNotExists`, `S3ConditionalPut`) [observed, OS-LIB, OS-AWS-PRECOND] |
| fsspec (+ s3fs/gcsfs/adlfs/sshfs) | none. Methods may `raise NotImplementedError` or be silent no-ops (`mkdir`, `makedirs`, `rmdir` bodies are `pass`). Class attrs `async_impl`, `cachable`, `local_file` only [observed, FSSPEC-SPEC] |
| pyarrow.fs | none. `Status::NotImplemented` at call time (e.g. Azure Move on flat accounts, S3 `OpenAppendStream`) [observed, PA-CC] |
| gocloud.dev/blob | none. `gcerrors.Unimplemented` at call time (e.g. `SignedURL`, `EnforceAbsentContentType`) [documented, GOCLOUD] |
| cloudpathlib | none. `CloudPathNotImplementedError` (e.g. `fspath` in streaming mode) [observed] |
| smart_open | none found [inference, README only] |

Pitfalls:
1. **Native vs emulated capability: OpenDAL split, then merged.** OpenDAL had `native_capability()` and
   `full_capability()`. v0.58.0 **removed** them: "Use `OperatorInfo::capability()` as the composed operator
   availability contract" (#7747, RFC "Capability API" #7700). Bindings dropped their `full`/`native` APIs
   too [documented, OD-CL v0.58.0]. The struct doc says "Some operations might be available even when not
   natively supported by the backend", e.g. via layers [documented, OD-CAP].
2. **Capabilities depend on runtime facts, not on backend type.** OpenDAL S3 sets several flags to
   `!is_s3_express` (versions, restore) [observed, OD-S3]. pyarrow Azure Move depends on whether the account
   has HNS, detected at runtime with a cached `ForceCachedHierarchicalNamespaceSupport` [observed, PA-H].
   gcsfs probes `_is_bucket_hns_enabled(bucket)` per bucket [observed]. Hadoop's capability takes a
   **path** so that viewfs can route to the nested fs [documented, HADOOP-PATHCAP].
3. **False must mean "unknown or unavailable", and the probe must be cheap.** Hadoop: an fs "MUST NOT
   return True for any capability unless it is known to be supported". False can mean unknown, known
   unavailable, or "known but this local class does not know". The probe "is intended to be low cost. If
   it requires remote calls … SHOULD conclude … unknown and return False". It must be side-effect free.
   Even a True can still lead to a failed operation (example: append on a directory) [documented,
   HADOOP-PATHCAP].
4. **Capability flags get missed or fixed piecemeal.** OpenDAL: "fix(services/swift): add missing copy
   capability flag (#7204)". "fix(s3): add missing content write content disposition capability (#7349)".
   "fix(correctness check): add missing conditional write capability check (#7320)", "validate copy
   capability and request (#7322)". "refactor: Split capability check to separate layer (#6952)".
   "capability override layer (#7520, RFC-6707)". webdav "deprecate capability toggles (#7562)"
   [documented, OD-CL]. SFTP `enable_copy` deprecated in 0.57.0 because "copy capability is enabled by
   default" [observed, OD-SFTP].
5. **Silent no-op vs error.** fsspec base `mkdir`: "For systems that don't have true directories, may create
   an for this instance only and not touch the real filesystem" and its body is `pass`. A caller cannot tell
   "unsupported" from "done" [observed, FSSPEC-SPEC]. pyarrow `open_output_stream(metadata=)`: "Unsupported
   metadata keys will be ignored" [documented, PA-PYX].

## OP-19 create an empty folder (gated)

Coverage names: OpenDAL `create_dir("a/b/")` (`Capability.create_dir`). pyarrow `create_dir(path,
recursive=True)`. fsspec `mkdir` / `makedirs(exist_ok=)`. Hadoop `mkdirs`. cloudpathlib `mkdir` (abstract
here; per-client implementations not read). gocloud: **none** (no method on `Bucket`) [observed, method
list]. object_store: **none** (no method on the trait) [observed, OS-LIB].

1. **On S3 a "folder" is a zero-byte `key/` object, and its retention policy changed in Hadoop twice.** The S3
   console "creates a 0-byte object. This object key is set to the folder name … plus a trailing forward
   slash" [documented, AWS-FOLDERS]. Hadoop S3A: 3.3.1 made marker retention optional (HADOOP-13230); 3.4.0
   "markers are not deleted by default" (HADOOP-18752); 3.5.0 "markers are never deleted" (HADOOP-19278).
   Older releases are "potentially not backwards compatible" [documented, HADOOP-MARKERS]. s3fs 2026.2.0:
   "do delete placeholders with rm(recursive=True) (#1005)" [documented].
2. **Emulation of create_dir is a layer, on by default.** OpenDAL's S3 service returns `Unsupported` for
   `create_dir` [observed, OD-S3]. The default `SimulateLayer` (`create_dir: true`) writes an empty object at
   the `dir/` path when `write_can_empty && list` [observed, OD-SIM, OD-BUILDER installs
   `SimulateLayer::default()`]. The path must end with `/`, "Omitting the trailing slash may cause OpenDAL to
   return a `NotADirectory` error"; creation is always recursive and idempotent [documented, OD-OP].
   OpenDAL also had "Implement SimulateLayer … (#6822)" and webdav "disable_create_dir for servers without
   PROPFIND (#7177)" [documented, OD-CL].
3. **mkdir on fsspec object stores means "create bucket", not a folder.** s3fs `_mkdir`: if the bucket exists
   and a key is given, it does nothing ("do nothing as bucket is already created"). If the bucket is missing
   and `create_parents`, it calls `create_bucket` [observed, S3FS]. gcsfs `_mkdir`: "New bucket … If contains
   '/' … will have no effect because GCS doesn't have real directories" [documented, GCSFS docstring]. Its
   changelog has "Implement makedirs for HNS buckets (#906)" (2026.7.0) and "pass trailing / to createFolder
   (#839)" (2026.6.0), so HNS buckets get real folders [documented]. adlfs: "Mkdir is a no-op for creating anything except
   top-level containers" [documented, ADLFS docstring].
4. **pyarrow writes markers, guards bucket creation, and has a rate-limit option.** S3 `CreateEmptyDir`
   PUTs `key/` with a directory content type [observed, PA-CC]. `allow_bucket_creation = false` by default
   [documented, PA-H]. `check_directory_existence_before_creation`: by default CreateDir tries to create
   without checking; "for key/value storage like Google Cloud Storage, too many creation calls will breach
   the rate limit for object mutation operations" [documented, PA-H s3fs.h]. Azure flat namespace: "no real
   directories. Directories are implied by empty directory marker blobs with names ending in '/'". HNS
   accounts use `hdi_isFolder` metadata [observed, PA-CC azurefs.cc].
5. **Hadoop's mkdirs requires atomic probe+create; stores cannot give that.** "The probe for the existence and
   type of a path and directory creation MUST be atomic. The combined operation, including
   mkdirs(parent(F)) MAY be atomic" [documented, HADOOP-FS]. *Inference*: a marker PUT after a HEAD is not
   atomic.
6. **Key escaping interacts with markers.** gocloud azureblob/fileblob escape "a trailing '/' in a key (e.g.,
   'foo/')" to `__0x2f__`, so a marker key cannot be written verbatim through gocloud [documented, GOCLOUD
   azureblob.go, fileblob.go].

## OP-20 user metadata (gated)

Coverage names: object_store `Attributes` / `Attribute::Metadata(key)` (in `PutOptions`, returned by `get`,
**not by list**). OpenDAL `write_with(...).user_metadata(...)` gated by `Capability.write_with_user_metadata`.
gocloud `WriterOptions.Metadata` / `Attributes.Metadata`. fsspec: no generic API. s3fs uses
`setxattr`/`getxattr`, gcsfs uses `setxattrs`/`getxattr`. pyarrow `open_output_stream(metadata=)`, which on
S3 carries only fixed system keys. Hadoop `setXAttr`/`getXAttr`. cloudpathlib: S3 `Metadata` via
`_get_metadata(...)["extra"]` [observed, s3client.py].

1. **Provider limits and character rules differ.**
   - S3: "user-defined metadata is limited to 2 KB" within an 8 KB PUT header. "Amazon S3 stores
     user-defined metadata keys in lowercase". REST requires US-ASCII. Values with non-ASCII are RFC 2047
     encoded, and unprintable metadata is not returned and is signalled by `x-amz-missing-meta`
     [documented, AWS-META].
   - Azure: names "must adhere to the naming rules for C# identifiers". They are case-insensitive but
     case-preserving, and duplicate names give 400. Total "up to 8KB" [documented, AZ-META].
   - GCS: "Maximum combined size of all custom metadata keys and values per object: 8 KiB" [documented,
     GCS-QUOTAS].
2. **gocloud normalises keys and escapes per provider.** Keys "are lowercased before being written"; on write,
   "Duplicate case-insensitive keys … will result in an error"; on read, "only one value will be kept, and it
   is undefined which one" [documented, GOCLOUD blob.go]. s3blob: metadata keys are URL-encoded, plus `@:=` as
   `__0x<hex>__` ("determined by experimentation"); values are URL-encoded. azureblob: characters outside
   `[a-zA-Z0-9_]`, and a leading digit, are hex-escaped because "URL encoding would not work since '%' is not
   valid" [documented, GOCLOUD s3blob.go/azureblob.go package docs]. fileblob stores metadata in `.attrs`
   sidecar files and can skip them (`metadata=skip`) [documented].
3. **Updating metadata on S3 rewrites the object.** s3fs `setxattr` reads the current metadata, merges, and
   calls `copy_object` (a full copy). It also turns `_` in kwarg names into `-` (cf. changelog "Fix '_' in
   xattrs tests (#732)") [observed, S3FS; documented, changelog]. object_store's S3 copy-if-not-exists
   multipart mode "does not copy tags or attributes" [documented, OS-AWS-PRECOND].
4. **Support is uneven, and libraries error or silently drop.** object_store `LocalFileSystem` returns
   `NotImplemented` for `put_opts` "with `opts.attributes` specified" [observed, OS-LOCAL]. Test comments:
   "Fake GCS server doesn't currently support attributes", "Azurite doesn't support attributes properly"
   [observed]. pyarrow S3 `SetObjectMetadata` honours only `ACL, Cache-Control, Content-Encoding,
   Content-Type, Content-Language, Expires` and skips other keys, so user `x-amz-meta-*` cannot be set
   through it [observed, PA-CC]; this matches "Unsupported metadata keys will be ignored" [documented,
   PA-PYX]. object_store_opendal drops ContentLanguage [observed].
5. **History of the change in object_store.** "Support User-Defined Object Metadata (#4754)". "Add Attributes
   API (#5329/#5650)". "Add more attributes (#5689/#5690)". "Add user defined metadata (#5915)". A bug
   report: "Generic S3 error: Metadata value for 'x-amz-meta-..' contained non UTF-8 characters (#509)"
   [documented, OS-CL]. `Attributes` "are not returned by listing APIs" [documented, OS-ATTR].
6. **System metadata vs user metadata share one namespace in some APIs.** object_store `Attribute` mixes
   ContentType/CacheControl/StorageClass with `Metadata(k)` [documented, OS-ATTR]. gcsfs `setxattrs` splits
   them out as `fixed_key_metadata=` (an older parameter is deprecated in its favour) [documented, GCSFS
   docstring].

## OP-21 store lifecycle (close, context manager)

Coverage names: gocloud `Bucket.Close()` (later calls → `FailedPrecondition "blob: Bucket has been
closed"`; a second Close returns that error). fsspec: no `close` on the filesystem. Async users call
`await fs.set_session()` … `await session.close()`; sync users rely on `weakref.finalize`; plus the
`clear_instance_cache()` classmethod. pyarrow: no per-instance close; process-global
`initialize_s3`/`finalize_s3`/`ensure_s3_finalized` (registered with `atexit`). object_store: none (Rust
`Drop`) [inference from absence in OS-LIB]. OpenDAL: none on `Operator` [observed, method list in OD-OP].
cloudpathlib: `Client.__del__` cleanup of the cache. smart_open: the caller owns the client
(`transport_params={"client": …}`) [documented, SMART README]. Hadoop: `FileSystem.close()` with a shared
cached instance (`FileSystem.get` "MAY return a pre-existing instance … in use in other threads")
[documented, HADOOP-FS].

1. **Instance caching makes close a shared-state hazard.** fsspec instances are cached by constructor args
   (`cachable = True`, opt out with `skip_instance_cache=True`). The cache "prevents Python's normal rules
   around garbage collection from working" until `clear_instance_cache` [documented, FSSPEC-SPEC
   docstring]. s3fs 2026.2.0: "force new session if it was explicitly closed (#1002)" [documented, S3FS
   changelog]. *Inference*: one user closing a cached instance affected others. The issue text is unreachable.
2. **Closing aiohttp/aiobotocore sessions at GC is fragile.** s3fs uses `weakref.finalize(self,
   self.close_session, …)`, with the comment "use of privates might break in the future, would cause
   exception at gc time". `close_session` falls back to `s3._client._endpoint.http_session._connector._close()`
   [observed, S3FS core.py]. fsspec async doc: destructors may run "after the loop has stopped/closed"
   [documented, FSSPEC-ASYNC]. fsspec changelog: "Stop the fsspec IO loop and join its thread at interpreter
   exit, so a callback firing on it after `Py_Finalize` …" (Dev) [documented]. adlfs and gcsfs also use
   `weakref.finalize` for client close [observed]. gcsfs 2026.3.0: "graceful close (#763)" [documented].
3. **Global SDK lifecycle in pyarrow.** `FinalizeS3()`: "After this function has been called, all S3 calls
   will fail with an error". Init/finalize calls "should be serialized by the application"; pyarrow
   registers `ensure_s3_finalized` with `atexit` [documented, PA-H; observed, PA-PY].
4. **Derived handles inherit or steal lifecycle.** gocloud `PrefixedBucket`/`SingleKeyBucket` close the
   original bucket [documented]. pyarrow `FileSystem.__reduce__` rebuilds the fs from `MakeUri("/_")` on
   unpickle, so a "copy" is a new instance [observed, PA-PYX]. cloudpathlib had to fix `__del__` when the
   client failed during init ("#372/#373", v0.17.0; "Fixed CloudPath cleanup via CloudPath.__del__",
   v0.19.0) [documented, CLOUDPATH HISTORY].
5. **Files outlive or depend on the store.** fsspec Dev: "Reject reads on closed asynchronous HTTP streams
   without reopening a request". "Close sync HTTP download files on success or failure, without closing
   caller-owned streams". "Finalize zip-fs file contexts on explicit close (#2311)". "Close cached readers
   when exiting an `open_files` context (#2131)" [documented, FSSPEC-CL]. adlfs file `close()` also closes
   the container client [observed, ADLFS `close`].

## OP-22 native address mapping (key ↔ native path/URL)

Coverage names: fsspec `unstrip_protocol(name)` / `_strip_protocol` (+ `url_to_fs`). pyarrow
`FileSystem.from_uri` / C++ `PathFromUri` / `MakeUri`. object_store `parse_url` / `ObjectStoreScheme::parse`
(URL → store+path), `Path::from_url_path`, `Path::from_filesystem_path`, and
`LocalFileSystem::path_to_filesystem`; no general store → URL inverse was found [observed]. OpenDAL
`Operator::from_uri` plus `info().scheme()/root()/name()`. gocloud `OpenBucket(ctx, urlstr)` (URL → bucket
only) plus `SignedURL`. cloudpathlib `as_uri()`, `as_url(presign=)`, `__fspath__`/`fspath`. Hadoop
`getUri`/`makeQualified` (not re-read here).

1. **"Native path" may mean a local cache copy.** cloudpathlib `__fspath__` downloads the file into the
   local cache and returns the cache path. In streaming mode it raises `CloudPathNotImplementedError`
   [observed, CLOUDPATH; documented, HISTORY UNRELEASED]. The `..`-in-key cache-escape security fix belongs
   to this mapping (v0.25.0) [documented].
2. **The URI may embed credentials.** pyarrow `S3FileSystem::MakeUri` prepends `access_key:secret_key@` when
   an access key is configured, and appends region, scheme, endpoint_override and allow_bucket_* query
   params [observed, PA-CC s3fs.cc]. `PathFromUri` "will not detect inconsistencies like a mismatching
   region or endpoint override" [documented, PA-H].
3. **Scheme aliases and URL shapes are many-to-one.** object_store recognises `s3://` and `s3a://`;
   `az://`, `abfs[s]://container@account…`; `https://…blob.core.windows.net`, `dfs.core.windows.net`,
   `*.fabric.microsoft.com`, `amazonaws.com` and `r2.cloudflarestorage.com` hosts [documented, OS-PARSE].
   pyarrow `from_uri` recognises "file", "mock", "s3fs", "gs", "gcs", "hdfs", "viewfs" [documented,
   PA-PYX]. fsspec `unstrip_protocol` uses the first of several protocols and returns names already starting
   with any of them unchanged [observed, FSSPEC-SPEC]. fsspec "rename protocols for sync-http (#1810)"
   [documented].
4. **Key encoding differs between the logical key and the native key.** object_store percent-encodes
   problematic segments (`foo/../bar` → `foo/%2E%2E/bar`) and warns that already-encoded input is
   re-encoded [documented, OS-PATH]. gocloud escapes control chars, `../`, trailing `/`, and Windows-illegal
   chars to `__0x<hex>__` per driver [documented, GOCLOUD]. *Inference*: native key ≠ logical key for some
   inputs, so a mapping is not the identity. fsspec "Percent-encode GitHub file paths … with `#`, `?` or `%`"
   [documented, FSSPEC-CL].
5. **Native paths of local stores expose symlinks and roots.** object_store
   `LocalFileSystem::path_to_filesystem` returns an absolute path, and "Symlinks that resolve to paths outside
   the root **will** be followed" [documented, OS-LOCAL]. OpenDAL fs canonicalizes its root at build time
   [observed, OD-FS backend.rs].

## OP-23 native handle escape hatch

Coverage names:

| Library | Name |
|---|---|
| gocloud | `Bucket.As(i any) bool`, `Bucket.ErrorAs(err, i)`, plus `As` on ListObject/Reader/Attributes and `Before*` option callbacks; per-driver type lists (s3blob `*s3.Client`, azureblob `*container.Client`, fileblob `os.FileInfo`) [documented, GOCLOUD] |
| s3fs | `.s3` property (aiobotocore client; async users must `await set_session()` first, otherwise `RuntimeError`) [observed] |
| adlfs | `.service_client` attribute [observed] |
| gcsfs | `.session` (aiohttp) — not verified in detail |
| cloudpathlib | `S3Client.client` (boto3 client), `.s3` (resource), `.sess` [observed, s3client.py] |
| smart_open | inverted: the caller passes the native client in `transport_params={"client": …}` [documented] |
| object_store | concrete store types (e.g. `AmazonS3::credentials()`), plus per-request `extensions: http::Extensions` ("ignored entirely by backends offered through this crate") [observed/documented, OS-LIB] |
| OpenDAL | no native SDK client (OpenDAL speaks HTTP itself). `Operator::into_parts` / `base_service` expose the raw OpenDAL service, not a vendor SDK [observed, OD-OP] |
| pyarrow.fs | none found at the Python level [inference from PA-PYX surface] |
| Hadoop | none in the spec. Store-specific `fs.<scheme>.capability.*` probes [documented, HADOOP-PATHCAP] |

1. **The escape hatch is explicitly non-portable, and the type list is part of the contract.** gocloud:
   "Using `As` implies that the resulting code is no longer portable". `As` "might be used as an interim
   solution until a feature request … is implemented. Or, the Go CDK may choose not to support specific
   features, and the use of `As` will be permanent" [documented, GOCLOUD as.md]. *Inference*: every SDK
   migration changes the `As` types. s3blob now exposes `*transfermanager.UploadObjectInput` for
   `BeforeWrite` [documented].
2. **The handle can be uninitialised or tied to an event loop.** s3fs `.s3` raises "please await
   `.set_session` before anything else" in async mode, and connects lazily otherwise [observed, S3FS].
   *Inference*: the handle's lifetime is bound to the fs instance's loop and session (see OP-21).
3. **Errors are the most-used escape hatch.** gocloud has a separate `ErrorAs` (azureblob → `*azcore.ResponseError`;
   s3blob → `smithy.APIError`) [documented]. fsspec/s3fs translate boto errors (`translate_boto_error`), and
   s3fs 2026.2.0 "add custom error handling (#1003)" [observed; documented].
4. **Hooks into the request instead of a handle.** gocloud `BeforeRead/BeforeWrite/BeforeCopy/BeforeList`
   callbacks expose the per-request SDK input structs [documented, GOCLOUD s3blob doc]. object_store
   `extensions` is a pass-through only for custom `ObjectStore` implementations [documented]. s3fs passes
   extra kwargs to boto calls, filtered by `_filter_kwargs` [observed].

## OP-24 health check

Coverage names:

| Library | Name | What it does |
|---|---|---|
| OpenDAL | `Operator::check()` (**verified**) | "Check if this operator can work correctly. We will send a `list` request to path and return any errors we met". The code lists `/` with `limit(1)` and treats `NotFound` as OK [documented + observed, OD-OP] |
| gocloud | `Bucket.IsAccessible(ctx) (bool, error)` | `ListPage(FirstPageToken, 1)`. `NotFound` → `(false, nil)`, other errors → `(false, err)` [documented + observed, GOCLOUD] |
| fsspec / s3fs / gcsfs / adlfs | none | (inference: callers use `ls`/`exists` on the bucket) |
| pyarrow.fs | none | (`resolve_s3_region(bucket)` exists, but it is not a health check) [observed, PA-S3PYX] |
| object_store | none | [observed, OS-LIB trait] |
| cloudpathlib, smart_open, Hadoop | none found | |

1. **"Healthy" is defined as "a minimal list succeeds", which needs list permission.** Both OpenDAL and gocloud
   use list-1. S3 `HeadBucket` also requires `s3:ListBucket` [documented, AWS-HEADBUCKET]. *Inference*: a
   write-only or get-only credential reports unhealthy, or errors, although reads or writes would work.
2. **NotFound vs Forbidden ambiguity.** HeadBucket: "If the bucket doesn't exist or you don't have permission
   to access it, the HEAD request returns a generic 400 Bad Request, 403 Forbidden, or 404 Not Found …
   without a response body" [documented, AWS-HEADBUCKET]. OpenDAL `check()` maps `NotFound` to **OK**, but
   gocloud `IsAccessible` maps it to **false**. The two libraries disagree on whether an empty or missing
   root is healthy [observed].
3. **Root path semantics.** OpenDAL checks `/` relative to the operator root. A non-existent root prefix on
   an object store is not an error there [observed]. gocloud lists the (possibly prefixed) bucket
   [observed; prefix interaction is inference].
4. **The cost and side effects of probes matter.** Hadoop's capability probe must be "low cost" and
   "side-effect free" [documented, HADOOP-PATHCAP]. This is a design norm stated for probes, not for health
   checks [inference: applicable by analogy]. The pyarrow `check_directory_existence_before_creation` note
   shows that extra calls can hit GCS mutation rate limits [documented, PA-H].

---

## Cross-cutting patterns (inference, for the per-entry session)

- **Bucket or account type, not provider, decides semantics** for move (Azure HNS, GCS HNS/moveTo, S3
  Express RenameObject) and create_dir (GCS HNS folders, Azure `hdi_isFolder`). Libraries responded by
  adding runtime probes (pyarrow, gcsfs) or capability flags (OpenDAL).
- **Pairs of overwrite and no-overwrite variants were consolidated into options** in 2025–2026: object_store
  `copy_opts`/`rename_opts` (0.13.0) and OpenDAL `rename_with_if_not_exists` (0.58.0).
- **`..` containment was retrofitted in 2026 by three libraries independently**: fsspec DirFS 2026.7.0,
  OpenDAL fs 0.58.0, and cloudpathlib 0.25.0 (GHSA).
- **Silent drops are common at bridges and adapters** (metadata keys, `mode=`, ContentLanguage). Only
  object_store LocalFileSystem errors on unsupported attributes.

## Unreachable / not verified

- GitHub issue and PR pages (gh API blocked in this session). All issue numbers are cited from changelogs.
- Whether pyarrow S3 `CopyFile` handles objects >5 GB (not traced in s3fs.cc).
- Reports that the botocore 1.36 default-checksum change broke S3-compatible servers (lead only).
- Azure Copy Blob authorization requirements for cross-account copies (page not read in that section).
- gcsfs `.session` as an escape hatch (attribute not inspected).
