# Track 02: pyarrow.fs, smart_open, cloudpathlib vs the draft OP catalogue

Accessed 2026-10-26. I did not consult remote-store's own code or docs.

## Labels

- **[documented]**: stated in the library's published prose docs (doc site, README, HOWTO, help.txt, docstring rendered on the doc site).
- **[source]**: read in the released source of the stated version, either via raw.githubusercontent.com at the release tag or in the wheel installed from PyPI. It is primary evidence, but it is not a promise in the prose docs.
- **[observed]**: I ran it on 2026-10-26 in a scratchpad venv (Python 3.13) against the local disk and an S3 emulator (moto 5.2.4 `ThreadedMotoServer`). Moto is not AWS, so a behaviour that depends on the server, such as multipart or metadata handling, can differ on real S3.
- **[inference]**: my reading, not stated anywhere.
- **unreachable**: I could not fetch the source.

## Sources and versions

| # | Source | Version / date | Notes |
|---|---|---|---|
| A1 | https://arrow.apache.org/docs/python/api/filesystems.html | page title "Apache Arrow v26.0.0" | API index |
| A2 | https://arrow.apache.org/docs/python/generated/pyarrow.fs.FileSystem.html | v26.0.0 | base class methods |
| A3 | https://arrow.apache.org/docs/python/generated/pyarrow.fs.S3FileSystem.html | v26.0.0 | constructor options |
| A4 | https://arrow.apache.org/docs/python/filesystems.html | v26.0.0 | user guide |
| A5 | https://arrow.apache.org/docs/python/generated/pyarrow.fs.{FileSelector,FileInfo,copy_files,SubTreeFileSystem,LocalFileSystem,GcsFileSystem,AzureFileSystem,FileSystemHandler,finalize_s3}.html | v26.0.0 | |
| A6 | https://arrow.apache.org/docs/cpp/api/filesystem.html | v26.0.0 | C++ API reference; holds the per-backend semantics (Azure Move, GCS markers, S3Options) |
| A7 | https://arrow.apache.org/docs/cpp/io.html | v26.0.0 | I/O guide |
| A8 | https://raw.githubusercontent.com/apache/arrow/apache-arrow-26.0.0/cpp/src/arrow/filesystem/s3fs.cc | tag apache-arrow-26.0.0 | [source] |
| A9 | pyarrow 26.0.0 wheel (PyPI, uploaded 2026-10-09) | 26.0.0 | [observed] runs; `pyarrow/fs.py` [source] |
| S1 | https://raw.githubusercontent.com/piskvorky/smart_open/develop/README.md | `develop` branch, fetched 2026-10-26 | `README.rst` returns 404; the README is now Markdown |
| S2 | https://raw.githubusercontent.com/piskvorky/smart_open/develop/help.txt | develop, 2026-10-26 | API reference (output of `help()`) |
| S3 | https://raw.githubusercontent.com/piskvorky/smart_open/develop/HOWTO.md | develop, 2026-10-26 | `howto.md` (lowercase) returns 404 |
| S4 | smart_open 8.0.4 wheel (PyPI, uploaded 2026-10-17): `s3.py`, `smart_open_lib.py`, `utils.py`, `azure.py`, `gcs.py` | 8.0.4 | [source] / [observed]. Note that S1–S3 come from `develop`, which may be ahead of 8.0.4. |
| C1 | https://cloudpathlib.drivendata.org/stable/api-reference/cloudpath/ | stable = v0.26.0 (changelog top entry 2026-10-01) | method list; the docs embed the source |
| C2 | https://cloudpathlib.drivendata.org/stable/caching/ | v0.26.0 | cache semantics and conflict errors |
| C3 | https://cloudpathlib.drivendata.org/stable/api-reference/{client,s3client,exceptions}/ | v0.26.0 | |
| C4 | https://cloudpathlib.drivendata.org/stable/other_client_settings/ | v0.26.0 | `content_type_method` |
| C5 | cloudpathlib 0.26.0 wheel (PyPI, uploaded 2026-10-02): `cloudpath.py`, `s3/s3path.py`, `s3/s3client.py`, `azure/azblobclient.py`, `gs/gspath.py` | 0.26.0 | [source] / [observed] |

My scratch scripts and their outputs are in `/tmp/claude-0/-home-user-research/1d762f77-d79e-5bb5-9ee3-6439664df376/scratchpad/t02/` (`scripts/obs_pa.py`, `obs_pa.out`, `scripts/obs_cp_so.py`, `obs_cp_so.out`). The repo does not hold them.

---

## 1. pyarrow.fs (26.0.0)

The public surface of `FileSystem` is `copy_file, create_dir, delete_dir, delete_dir_contents, delete_file, equals, from_uri, get_file_info, move, normalize_path, open_append_stream, open_input_file, open_input_stream, open_output_stream, type_name` [observed: `dir(pyarrow.fs.FileSystem)`; matches A2]. The module-level functions are `copy_files, initialize_s3, finalize_s3, ensure_s3_initialized, ensure_s3_finalized, resolve_s3_region` [observed]. The backends are Local, S3, GCS, HDFS, Azure, SubTree and PyFileSystem/FSSpecHandler [A1].

### OP mapping

| OP | pyarrow name | Gated? | How the caller learns |
|---|---|---|---|
| OP-01 read whole/streamed | `open_input_stream(path, compression='detect', buffer_size=None)` → `NativeFile` (`.read()`, `.readall()`) [documented A2] | no | n/a. On S3, reads are "synchronous and unbuffered"; the docs suggest wrapping in `BufferedInputStream` [documented A6, S3FileSystem::OpenInputStream] |
| OP-02 read at offsets | `open_input_file(path)` → RandomAccessFile with `seek`, `read_at(n, offset)` [documented A2; `read_at` observed on S3]. `ReadAt` "allow[s] parallel reading from multiple threads" [documented A7] | no | n/a |
| OP-03 write whole/streamed | `open_output_stream(path, compression='detect', buffer_size=None, metadata=None)`; "If the target already exists, existing data is truncated" [documented A2] | no | n/a |
| OP-04 replace atomically | **no op** | n/a | On S3 the object is not visible until `close()` [observed]. But an exception inside `with` still **commits** the partial object [observed; source A8 `~ObjectOutputStream`: "Close rather than Abort"]. On local disk the file is truncated in place, so a partial file remains [observed] |
| OP-05 conditional write | **no op**. `s3fs.cc` has no If-None-Match / If-Match [source A8, grep] | n/a | n/a |
| OP-06 list children | `get_file_info(FileSelector(base_dir))` [documented A2, A5] | no | A missing base raises `FileNotFoundError` unless `allow_not_found=True`, which returns `[]` [documented A5; observed] |
| OP-07 walk subtree | `get_file_info(FileSelector(base_dir, recursive=True))` returns a flat list, not a tree walk [documented A5] | Depth limit: C++ `FileSelector::max_recursion` exists [documented A6], but the **Python `FileSelector` has no such argument** (`TypeError`) [observed] | n/a |
| OP-08 glob | **no op** | n/a | Callers filter the `FileInfo` list themselves [inference] |
| OP-09 inspect | `get_file_info(path \| [paths])` → `FileInfo(type ∈ {NotFound, File, Directory, Unknown}, size, mtime, mtime_ns)`. A missing path **does not raise**; it returns `type=NotFound` [documented A2, A4; observed]. There is no `exists()` | no | n/a |
| OP-10 delete item | `delete_file(path)`. Raises `FileNotFoundError` if missing [observed local + S3] | no | n/a |
| OP-11 delete folder tree | `delete_dir(path)` deletes the directory itself. `delete_dir_contents(path, *, accept_root_dir=False, missing_dir_ok=False)` keeps it [documented A2] | Root: `delete_dir_contents("/")` raises `ArrowInvalid` [observed]. S3/GCS/Azure `DeleteRootDirContents` return NotImplemented [documented A6, source A8] | errors |
| OP-12 move/rename | `move(src, dest)`. Contract: replace if dest has the same type; error if dest is a non-empty dir; otherwise "unspecified (implementation-dependent)" [documented A2] | **Yes.** S3: files only, done as CopyObject then DeleteObject. Directories are not implemented "as it would be too expensive" [source A8]. Azure: **only on HNS accounts, atomic via leases**; no move across containers [documented A6] | S3 dir move fails with a generic `OSError` (`NO_SUCH_KEY during CopyObject`), **not** `NotImplementedError` [observed]. Azure limits are in the docs only |
| OP-13 copy within store | `copy_file(src, dest)`, files only; replaces dest; error if dest is a dir [documented A2] | no | n/a |
| OP-14 to/from local | `copy_files(source, destination, source_filesystem=None, destination_filesystem=None, *, chunk_size=1MB, use_threads=True)`, recursive for directories [documented A5] | no | n/a |
| OP-15 between stores | the same `copy_files` with two filesystems or two URIs [documented A5] | no | n/a |
| OP-16 scope to folder | `SubTreeFileSystem(base_path, base_fs)`. "makes no security guarantee … symlinks may allow to 'escape'" [documented A5]. `..` is passed through as a literal key segment on S3 [observed: prefix `e/../d/` sent to the server] | no | n/a |
| OP-17 hand to other libs | NativeFile objects; `filesystem=` arguments across pyarrow (`pq.read_table(path, filesystem=s3)`); `fsspec.implementations.arrow.ArrowFSWrapper` exposes a pyarrow fs as fsspec; `PyFileSystem(FSSpecHandler(fs))` goes the other way [documented A4] | no | n/a |
| OP-18 capability query | **no op** | n/a | Learnt from exceptions (`ArrowNotImplementedError`, a subclass of `NotImplementedError`, e.g. `open_append_stream` on S3 [observed]) or from the docs. `type_name` names the backend [documented A2] |
| OP-19 create empty folder | `create_dir(path, *, recursive=True)`. "succeeds if the directory already exists" [documented A2] | S3: writes a marker object `key/` with `Content-Type: application/x-directory` [source A8 `CreateEmptyDir`; observed key `emptydir/`]. GCS: "creates marker objects for a directory" [documented A6]. S3 `create_dir("bucket")` creates a bucket only if `allow_bucket_creation=True` [documented A3] | docs |
| OP-20 user metadata | `metadata=` on `open_output_stream` / `open_append_stream`, plus `default_metadata` on S3/GCS/Azure. "Some filesystems support storing metadata … Unsupported metadata keys will be ignored" [documented A2]. Read back via `NativeFile.metadata()` [observed] | **Yes, silently.** S3 honours only `ACL, Cache-Control, Content-Encoding, Content-Type, Content-Language, Expires` [source A8 `ObjectMetadataSetter`]. `x-amz-meta-foo` was dropped [observed: `head_object` Metadata `{}`] | none (silent drop) |
| OP-21 lifecycle | No `FileSystem.close()` [observed: no such method]. Streams are context managers. S3 has process-global `initialize_s3`/`finalize_s3`; C++ says you "MUST call FinalizeS3 … to avoid a segmentation fault at shutdown" [documented A6]. Python registers `atexit.register(ensure_s3_finalized)` [source A9 `fs.py:69-70`] | n/a | n/a |
| OP-22 native address mapping | `FileSystem.from_uri(uri)` → `(fs, path)` [documented A2]. Paths **must not** carry a scheme: `get_file_info("s3://b/x")` raises `ArrowInvalid` [observed]. C++ has `MakeUri(path)` / `PathFromUri` [documented A6], but Python exposes neither [observed `dir`] | n/a | n/a |
| OP-23 native handle | **none in Python.** The AWS/Azure/GCS client object is not exposed; only `S3FileSystem.region` [documented A3] | n/a | n/a |
| OP-24 health check | **none.** `resolve_s3_region(bucket)` is the nearest thing [documented A1] | n/a | n/a |

### pyarrow operations with no catalogue entry

- `open_append_stream(path, …)`: append or create. Local and SubTree support it [documented A5]. S3 raises `ArrowNotImplementedError: It is not possible to append efficiently to S3 objects` [source A8; observed]. Use case: log or row appends.
- On-the-fly `compression='detect'|'gzip'|…` on all open_* calls [documented A2].
- `buffer_size` on streams; `LocalFileSystem(use_mmap=True)` [documented A5].
- `normalize_path(path)`: the C++ default "is a no-op" [documented A6]. For Local and S3 it returned its input unchanged, including `//`, `..` and even an `s3://` prefix [observed].
- `equals(other)` and `type_name` [documented A2].
- Bucket and container administration: `allow_bucket_creation` / `allow_bucket_deletion` on S3 [documented A3]. Azure "containers will be created or deleted during relevant directory operations" [documented A5 AzureFileSystem].
- `delete_dir_contents(accept_root_dir=…)` [documented A2].
- S3 connection tuning: `allow_delayed_open` (open errors surface "at worst, when attempting to close"), `background_writes`, `proxy_options`, `force_virtual_addressing`, `tls_ca_file_path`, `role_arn`/STS, `check_directory_existence_before_creation` [documented A3]. C++ also has `sse_customer_key` [documented A6]; the Python signature does not include it [documented A3].
- Logging: `ARROW_S3_LOG_LEVEL` / `S3LogLevel` [documented A4, A1].
- Custom backends: `PyFileSystem(FileSystemHandler)` and `FSSpecHandler` [documented A1].
- C++-only async: `GetFileInfoAsync`, `GetFileInfoGenerator` (streaming listing), `DeleteDirContentsAsync`, `DeleteFiles` (batch) [documented A6]. None is on the Python `FileSystem` [observed].

---

## 2. smart_open (8.0.4)

The public API is `__all__ = ['open', 'parse_uri', 'register_compressor']` [documented S2; observed]. Everything else lives in transport-specific `transport_params` or helper functions per transport module.

### OP mapping

| OP | smart_open name | Gated? | How the caller learns |
|---|---|---|---|
| OP-01 read | `open(uri, 'r'/'rb', …)`: a streaming file-like object, line iteration, transparent decompression by extension [documented S1, S2] | Per-scheme. HTTP/HTTPS are read-only [documented S1] | `NotImplementedError` for an unsupported mode [documented S2; observed] |
| OP-02 read at offsets | `seek()` on the returned object. The S3 reader is seekable [documented S1 example; observed `seekable()=True`]. S3: "Forward seeks within the current buffer are satisfied without additional GET requests. Backward seeks always open a new GET request"; `range_chunk_size` caps the bytes per GET; `defer_seek` [documented S2] | per transport | n/a |
| OP-03 write | `open(uri, 'w'/'wb')`. S3 uses multipart by default (`min_part_size`, default 50 MB [documented S3], clamped to 5 MB–5 GB [documented S2]) or `multipart_upload=False` (single PUT; "allows seek() before upload") [documented S1]. `writebuffer` can spill to disk [documented S2, S3] | per transport (GCS/HDFS/WebHDFS/FTP: `rb`/`wb` only [documented S2]) | `NotImplementedError` |
| OP-04 replace atomically | **no op.** S3: the object is absent until `close()` [observed]. An exception inside `with` → `terminate()` → `AbortMultipartUpload`, so no object and no leftover upload [source S4 `MultipartWriter.__exit__`; observed for binary, text, `.gz` text and single-part modes]. `utils.TextIOWrapper` exists so the text layer "does not close the buffer on exceptions" [source S4] | S3 behaviour shown; other transports not checked | n/a |
| OP-05 conditional write | **no op.** [inference, not tested] `client_kwargs={'S3.Client.put_object': {'IfNoneMatch': '*'}}` could reach single-part PUTs, because `put_object` is listed as an "influential function" [documented S3]. This is not a documented feature | n/a | n/a |
| OP-06 / OP-07 / OP-08 | **no op** in `open()`. The S3-only helper `smart_open.s3.iter_bucket(bucket, prefix=, accept_key=, workers=, key_limit=)` **lists and downloads** in parallel, yielding `(key, content)` [documented S1]. The HOWTO tells GCS users to list with `google.cloud.storage` directly [documented S3] | S3 only | docs |
| OP-09 inspect | **no op.** Use `fin.to_boto3(resource)` → `boto3.s3.Object` for content_type, LastModified, etc. [documented S3] | S3 only | docs ("This works only when reading and writing via S3") |
| OP-10 … OP-13 | **no op.** The HOWTO says to use boto3 directly for copy and ACLs [documented S3] | n/a | n/a |
| OP-14 to/from local | **no dedicated op.** Local paths and `file://` are just another URI (open both sides and copy the stream) [documented S1; the copy loop is inference] | n/a | n/a |
| OP-15 between stores | as OP-14 (README example: read `.gz`, write `.bz2`) [documented S1] | n/a | n/a |
| OP-16 scope | **no op** | n/a | n/a |
| OP-17 hand to other libs | The returned object is IO-like ("drop-in replacement for Python's built-in open()") [documented S1]. HOWTO shows `zipfile.ZipFile(fin)` [documented S3]. `patch_pathlib()` replaces `Path.open` [documented S1] | n/a | n/a |
| OP-18 capability query | **no op** | n/a | Errors only: an unknown scheme raises `NotImplementedError("Unable to handle scheme …, expected one of (…)")`. The list contained only schemes whose extras were installed (`azure`, `gcs`, `ssh` were missing in my venv) [observed]. **Unknown `transport_params` are ignored with a logged warning** [documented S2; observed: no exception] |
| OP-19 create folder | **no op** | n/a | n/a |
| OP-20 user metadata | No generic op. Pass-through per transport: S3 `client_kwargs={'S3.Client.create_multipart_upload': {'Metadata': …}}`; GCS `blob_properties={'metadata': …}`; Azure `blob_kwargs={'metadata': …}` [documented S1] | per transport, using different names | docs |
| OP-21 lifecycle | File-object `close()` / context manager. S3 writers also have `terminate()` [source S4; observed attribute]. No client lifecycle: the caller passes or reuses its own client, and "long-lived clients can leak memory" [documented S3] | n/a | n/a |
| OP-22 address mapping | `parse_uri(uri)` → namedtuple. It does **not** normalize: `s3://bkt/a/../b` → `key_id='a/../b'` [observed]. Credentials may be embedded in the URI (`s3://key:secret@bucket/key`) [documented S1] | n/a | n/a |
| OP-23 native handle | `to_boto3(resource)` (S3 only) [documented S3]; inject a native client via `transport_params={'client': …}` for S3/GCS/Azure [documented S1] | S3 only | docs |
| OP-24 health check | **no op** | n/a | n/a |

### smart_open operations with no catalogue entry

- **Compression**: `compression='infer_from_extension'|'disable'|'.gz'|…`, `compression_kwargs`, `register_compressor(ext, cb)` [documented S1, S2].
- **Append**: Azure `mode='ab'` creates or extends Append Blobs (max 195 GiB) [documented S1]. S3 `ab` raises `NotImplementedError("bad mode: 'ab' expected one of ('rb', 'wb')")` [observed].
- **Versioned read**: `version_id` (S3) [documented S3].
- **Requester-pays and per-call SDK kwargs**: `client_kwargs` [documented S3].
- **Transport extras**: HTTP `headers`/`kerberos`/`cert`/`timeout`/`session`; SSH `connect_kwargs`/`prefetch_kwargs`; Azure `max_concurrency` [documented S2].
- **Bulk parallel S3 download**: `iter_bucket` [documented S1].

---

## 3. cloudpathlib (0.26.0)

`CloudPath` is a pathlib-style object (`S3Path`, `GSPath`, `AzureBlobPath`, HTTP paths) bound to a `Client` (`S3Client`, …). All content I/O goes through a **local file cache** [documented C1, C2].

### OP mapping

| OP | cloudpathlib name | Gated? | How the caller learns |
|---|---|---|---|
| OP-01 read | `read_bytes()`, `read_text()`, `open('r'/'rb')`. "In order to read the file, we do have to download the data": the **whole file goes to the cache**, then a local handle is returned [documented C2] | no | n/a |
| OP-02 read at offsets | `open('rb')` returns a local `BufferedReader`, so `seek`/`read` act on the cached copy [observed]. There are no ranged GETs [inference from C2] | no | n/a |
| OP-03 write | `write_bytes`, `write_text`, `open('w'/'wb'/'a'/'x'/'+')`. Writes go to the cache file and are uploaded "on the close of that file" [documented C2] | no | n/a |
| OP-04 replace atomically | **no op.** The object is invisible until `close()` [observed]. An **exception inside `with` still uploads the partial content**, because the upload is patched onto `buffer.close` [observed; source C5 `_patched_close_upload`] | n/a | n/a |
| OP-05 conditional write | **No atomic op.** Two related, non-atomic mtime checks: (a) `OverwriteNewerCloudError` when "the one on the cloud is newer than our local version", overridable with `force_overwrite_to_cloud` or `CLOUDPATHLIB_FORCE_OVERWRITE_TO_CLOUD` [documented C2]; (b) `open(mode='x')` raises `CloudPathFileExistsError` if `exists()` at open time [source C5]. Both are check-then-act [inference] | n/a | n/a |
| OP-06 list children | `iterdir()` [documented C1; observed] | Listing all buckets works; recursive listing of all buckets raises `NotImplementedError` [source C5 `s3client._list_dir`] | error |
| OP-07 walk | `walk(top_down=True, on_error=None, follow_symlinks=False, lazy=False)`. Default: "entire subtree is listed up front with a single recursive listing". `lazy=True` lists per directory and allows pruning `dirnames` [documented C1, C2]. **No depth argument**; depth is limited by pruning [documented C2]. Also `rglob` | no | n/a |
| OP-08 glob | `glob(pattern, case_sensitive=None, recurse_symlinks=True)`, `rglob`, and the pure `match`/`full_match` [documented C1] | `..` in a pattern, absolute or prefixed patterns, and globbing at the bucket-list level raise `CloudPathNotImplementedError` [source C5 `_glob_checks`; observed for `..`] | error |
| OP-09 inspect | `exists()`, `is_file()`, `is_dir()`, `stat()` (an `os.stat_result` with only size and mtime set) [observed], `info()` → `CloudPathInfo` [documented C1], `etag` (S3Path) [observed attribute]. `stat()` on a directory or missing key raises `NoStatError` ("may be a directory or not exist"), which is **not** a `FileNotFoundError` [source C5; observed] | no | n/a |
| OP-10 delete item | `unlink(missing_ok=True)`. **The default is True, unlike pathlib**; the source comment says changing it "would be a breaking change" [source C5; observed: no error on a missing key]. A directory raises `CloudPathIsADirectoryError` [source C5] | no | n/a |
| OP-11 delete tree | `rmtree()` [documented C1]. `rmdir()` only when empty; otherwise `DirectoryNotEmptyError` [source C5; observed] | no | n/a |
| OP-12 move/rename | `rename(target)` == `replace(target)`, **files only**. A directory raises `CloudPathIsADirectoryError` [observed]. It works as: if the target exists, `target.unlink()`, then server-side copy, then delete the source [source C5]. Also `move(target)` / `move_into(dir)`: "Move self to target location, removing the source", accepting cloud or local targets [documented C1] | no | n/a |
| OP-13 copy within store | `copy(target)`, `copy_into(dir)`, `copytree(dest, ignore=)` [documented C1]. Same client: server-side copy; raises `OverwriteNewerCloudError` if the destination mtime ≥ the source mtime, unless forced [source C5 `_copy`] | no | n/a |
| OP-14 to/from local | `download_to(local)`, `upload_from(local file or dir)`; `copy(target=pathlib.Path)` downloads [documented C1; source C5]. `CloudPathLocalPathTraversalError` guards keys that contain `..` [documented C2] | no | n/a |
| OP-15 between stores | `copy()` to a CloudPath with a **different client** works as `destination.upload_from(self.fspath)`, i.e. through the local cache [source C5] | no | n/a |
| OP-16 scope | **no op.** Paths are absolute URIs. `client.CloudPath(...)` binds a client, not a root [documented C2] | n/a | n/a |
| OP-17 hand to other libs | `os.PathLike` / `.fspath` gives the path of the **cached local file**. This is read-only: "Writes directly to fspath will not be uploaded" [documented C2]. Pydantic `validate` [documented C1] | n/a | n/a |
| OP-18 capability query | **no op** | n/a | Learnt from silent no-ops (see OP-19) or `NotImplementedError` (HTTP presign, listing all buckets) [source C5] |
| OP-19 create folder | `mkdir(parents, exist_ok, …)`. **Silent no-op on S3 and GCS** ("not possible to make empty directory") [source C5]. After `mkdir()`, `exists()` is False and no key is written [observed]; `exist_ok=False` twice does not raise [observed]. Azure: a real directory only on HNS, otherwise the same no-op [source C5 `azblobclient._mkdir`] | **yes, silent** | none |
| OP-20 user metadata | No per-path API. Client-wide `extra_args` (boto3 upload, download, copy and list args, e.g. `Metadata`) [documented C3 S3Client]; `content_type_method` [documented C4]. `touch()` on an existing S3 object copies it onto itself with `MetadataDirective=REPLACE`, keeping the existing user metadata [source C5] | client-level | docs |
| OP-21 lifecycle | No `close()`. Cache lifetime follows `file_cache_mode ∈ {persistent, tmp_dir (default), cloudpath_object, close_file}` or `CLOUDPATHLIB_FILE_CACHE_MODE`; `clear_cache()` exists on the path and on the Client. Cleanup in `tmp_dir`/`cloudpath_object` modes **depends on GC** [documented C2] | n/a | n/a |
| OP-22 address mapping | `CloudPath("s3://…")` dispatches by prefix. A scheme-less string raises `InvalidPrefixError` (a `ValueError`) [observed]. `as_uri()`, `bucket`/`key`/`blob`, `from_uri` [documented C1]. **No normalization**: `"a/../b/./c"` and `"a//b"` are kept verbatim [observed]. `is_file()` on `"a/f.txt/"` returned True because the trailing slash is stripped for HEAD [observed; source C5 `rstrip("/")`] | n/a | n/a |
| OP-23 native handle | `S3Client.client` (boto3 client) and `.s3` (boto3 resource) [source C5 `__init__`; docs example `client.s3.Object(...)` in C4]; `boto3_session=` injection [documented C3] | n/a | n/a |
| OP-24 health check | **no op** | n/a | n/a |

### cloudpathlib operations with no catalogue entry

- **`as_url(presign=False, expire_seconds=3600)`** [documented C1]. The public URL comes from an unsigned client; presign uses `generate_presigned_url('get_object')` [source C5]. HTTP paths raise `NotImplementedError("Presigning not supported…")` [source C5]. Use case: give a time-limited GET link to a browser or third party. Observed output: `http://127.0.0.1:5056/bkt/b/g.txt?AWSAccessKeyId=…&Signature=…`.
- **Local cache control**: `local_cache_dir` / `CLOUDPATHLIB_LOCAL_CACHE_DIR`, `file_cache_mode`, `clear_cache()`, `force_overwrite_from_cloud`, `OverwriteNewerLocalError` [documented C2].
- **`touch(exist_ok=True)`**: creates an empty object, or refreshes mtime by copying onto itself [source C5]. On an existing object `exist_ok=False` raises `FileExistsError` [observed].
- `set_as_default_client()` / `get_default_client()` [documented C3]; `AnyPath` (local or cloud polymorphism; docs page listed, not read); pure path algebra (`with_suffix`, `parents`, `relative_to`, …).
- `content_type_method` (MIME guessing on upload) [documented C4]; `extra_args` requester-pays / `ExpectedBucketOwner` [source C5].
- `walk(lazy=True)` with pruning [documented C2].

---

## 4. Where they cut differently

1. **List, walk and inspect are one call in pyarrow.** `get_file_info` takes a path, a list of paths, or a `FileSelector(base_dir, allow_not_found, recursive)` and always returns `FileInfo`s [documented A2]. Inspect never raises for a missing path (`NotFound` type), but list does raise unless `allow_not_found` [documented; observed]. cloudpathlib splits the same ground into `exists/is_file/is_dir/stat/info`, `iterdir`, `walk`, `glob/rglob`. smart_open has none of them.
2. **Directory deletion in pyarrow comes in two forms.** `delete_dir` removes the directory; `delete_dir_contents` keeps it. On S3, `delete_dir_contents` re-creates the marker afterwards ("Directory may be implicitly deleted, recreate it") [source A8]; after deleting the contents, `get_file_info("bkt/h").type == Directory` [observed]. cloudpathlib likewise has `rmtree` vs `rmdir` (empty only).
3. **Move**
   - pyarrow:
     - One generic contract, with behaviour left "unspecified" when dest has another type [documented A2].
     - S3: files only, copy+delete [source A8].
     - Azure: HNS only, with an atomicity guarantee via leases [documented A6].
     - On S3, `move` and `delete_file` also call `EnsureParentExists` and write a `src-parent/` marker so the parent "directory" does not vanish [source A8]. Observed: key `d/` appeared after moving `d/f1.txt` away.
   - cloudpathlib `rename`/`replace`: files only; unlink the target, then copy, then delete [source C5].
   - None of the three offers an atomic replace on S3.
4. **Copy across stores**
   - pyarrow `copy_files` streams in chunks, threaded, between any two filesystems [documented A5].
   - cloudpathlib goes through the local cache (`upload_from(self.fspath)`) [source C5].
   - smart_open leaves it to the caller's stream copy.
5. **smart_open is only `open()`.** Everything else (inspect, copy, metadata reads) is "use boto3 directly" through `to_boto3` or `client_kwargs` [documented S3]. Its unit is a single stream; it has no filesystem object.
6. **cloudpathlib is cache-first.** Read and write are download, local edit, then upload on close. "Streaming" and "range read" do not exist as remote operations [documented C2].
7. **Folder creation**
   - pyarrow writes marker objects on S3 and GCS [source A8; documented A6].
   - cloudpathlib silently does nothing on S3 and GCS [source C5; observed].
   - So the same intent produces a visible empty folder in one library and nothing in the other.
8. **Append is a separate verb in pyarrow** (`open_append_stream`) and a mode in smart_open (`'ab'`, Azure and local only). Both refuse on S3.

## 5. Shared decisions

| Decision | pyarrow.fs 26.0.0 | smart_open 8.0.4 | cloudpathlib 0.26.0 |
|---|---|---|---|
| Not-found error | builtin `FileNotFoundError` (an `OSError`) for open, delete, list and `delete_dir_contents`; inspect returns `FileType.NotFound` [observed local + S3] | S3: plain **`OSError`** wrapping botocore `NoSuchKey` (the botocore error is smuggled in `.backend_error`). Local: `FileNotFoundError` [observed; source S4 `_get`] | `CloudPathFileNotFoundError(CloudPathException, FileNotFoundError)` on read [observed]; `unlink(missing_ok=False)` raises builtin `FileNotFoundError` [observed]; `stat` raises `NoStatError` (not an OSError) [observed]; `copy` of a missing source raises `ValueError` [source C5] |
| Other error types | `ArrowInvalid` (a `ValueError`) for bad paths or URIs and root deletion; `ArrowNotImplementedError` (a `NotImplementedError`) for unsupported ops; generic `OSError` for SDK failures such as S3 dir move or bucket deletion [observed] | `NotImplementedError` for an unsupported mode or scheme; `TypeError`/`ValueError` for arguments [documented S2; observed] | A hierarchy rooted at `CloudPathException`, mixed into builtins (`FileNotFoundError`, `IsADirectoryError`, `NotImplementedError`, `ValueError`) [observed MROs; documented C3 list] |
| Path form | Abstract `/`-separated paths "shouldn't include special path components such as . and .." [documented A4]; **a scheme is rejected** (`ArrowInvalid`); `normalize_path` is a no-op [observed]; the S3 path is `bucket/key` | Full URI per call; no normalization [observed `parse_uri`] | Full URI **required** (`InvalidPrefixError` without a prefix); no normalization [observed] |
| Retries | S3: `retry_strategy=AwsStandardS3RetryStrategy(max_attempts=3)` by default, or `AwsDefaultS3RetryStrategy` [documented A3]. GCS: `retry_time_limit` (C++ default: retry up to 15 min) [documented A5, A6]. The Python Azure signature has no retry option [documented A5] | Delegated to the boto3 client config. If smart_open creates the client, it uses `retries={"max_attempts": 6, "mode": "adaptive"}` [documented S3; source S4]; there is also an internal read retry with backoff `(1,2,4,8,16)` s [source S4]; `iter_bucket(retries=3)` [source S4] | No retry option on `S3Client`. [inference] Retries come from the boto3 session/config (`boto3_session=` / `botocore_session=` [documented C3]) |
| Timeouts | S3: `connect_timeout` (SDK default ~1 s) and `request_timeout`, which is **"ignored on non-Windows, non-macOS systems"** [documented A3] | HTTP `timeout`, FTP `timeout` transport params [documented S2]; S3 via the botocore Config | Not exposed [inference: via the boto3 session] |
| Closing | Streams: `close()` / context manager. **S3 output streams have no abort.** Close is called even on exception and commits the data [observed; source A8]. Global `finalize_s3` at exit [source A9] | `close()` commits; an exception in `with` calls `terminate()` (abort) on S3 writers [source S4; observed] | `close()` uploads, **also on exception** [observed]; cache cleanup per `file_cache_mode` [documented C2] |
| Async | None in Python. C++ has `*Async` and `GetFileInfoGenerator` [documented A6]. S3 `background_writes=True` by default issues writes "in the background, without blocking" [documented A3] | None | None |
| Thread safety | `RandomAccessFile.ReadAt` allows "parallel reading from multiple threads" [documented A7]; `copy_files(use_threads=True)` [documented A5]. FileSystem object thread safety is not stated in the pages read | boto3 clients are "generally thread-safe … cannot be shared across processes" [documented S3]. smart_open's own client is built thread-safe because "boto3.client re-uses the default session which is not thread-safe" [source S4] | Not documented in the pages read. Several default clients can share one cache dir "and could overwrite each other's content" [documented C2] |
| Pickling | `S3FileSystem` pickles (587 bytes) [observed] | n/a | `__getstate__` drops `_client` [source C5] |

## 6. Pitfalls by OP-ID

- **OP-01/02**
  - pyarrow S3 reads are unbuffered; wrap them for readahead [documented A6].
  - With `allow_delayed_open`, open errors surface late, "at worst, when attempting to close" [documented A3].
  - smart_open: backward seeks cost a new GET [documented S2].
  - cloudpathlib downloads the whole object before the first byte. Stale cache is detected by mtime: a remote change was re-downloaded [observed]. A **locally edited cache file blocks reads** with `OverwriteNewerLocalError` [documented C2; observed].
- **OP-03/04**
  - pyarrow S3: a partial object **is committed** when the `with` body raises [observed]. Local: a truncated or partial file remains [observed].
  - cloudpathlib: the partial content **is uploaded** on exception [observed].
  - smart_open S3: aborted, so no object [observed].
  - All three: the object is not visible before `close()` on S3 [observed].
  - smart_open multipart: parts must be 5 MB–5 GB (clamped), max 10,000 parts, 50 MB in RAM by default [documented S2, S3]. An empty multipart write is turned into a `put_object(b"")` [source S4; observed `empty.bin` exists].
- **OP-05**: none of the three has an atomic conditional write. cloudpathlib's mtime checks are advisory and race-prone [inference].
- **OP-07**: the pyarrow Python `FileSelector` lacks C++'s `max_recursion` [observed]. cloudpathlib `walk` has no depth; default `lazy=False` lists the full subtree up front [documented C2].
- **OP-08**: cloudpathlib glob rejects `..` and absolute patterns with `CloudPathNotImplementedError` [observed].
- **OP-09**
  - pyarrow inspect does not raise on missing paths, but list does [observed].
  - cloudpathlib `stat()` on a directory raises `NoStatError` [observed].
  - On S3 a "directory" exists only if some key has the prefix or a marker exists [source A8, C5]. After `cloudpathlib.mkdir`, `exists()` is False [observed].
- **OP-10**: cloudpathlib `unlink` is silent on missing keys by default (pathlib default inverted) [source C5; observed]. pyarrow raises [observed].
- **OP-11**
  - **pyarrow S3 `delete_dir("bucket")` without `allow_bucket_deletion` first deletes all objects in the bucket, then raises `OSError("Would delete bucket … enable the allow_bucket_deletion option")`** [source A8 `DeleteDir`; observed: a recursive listing returned `[]` afterwards].
  - Azure `DeleteDirContents` "can return a bad Status after only partially deleting" [documented A6]. Azure `DeleteDir` is atomic only on HNS [documented A6].
- **OP-12**
  - pyarrow S3 directory move raises a misleading `OSError` (NO_SUCH_KEY), not `NotImplementedError` [observed].
  - S3 file move is copy+delete, so not atomic [source A8].
  - Azure move needs HNS and works only within one container [documented A6].
  - cloudpathlib `replace` unlinks the target first, which leaves a window with no object [source C5].
- **OP-13**: cloudpathlib same-client `copy` refuses when the destination is not older, unless forced [source C5].
- **OP-16**: pyarrow `SubTreeFileSystem` "makes no security guarantee" [documented A5]. `..` passes through to S3 keys [observed].
- **OP-17**: cloudpathlib `fspath` writes are lost (not uploaded) [documented C2].
- **OP-19**
  - pyarrow creates marker objects (`key/`, `application/x-directory`) [source A8; observed], and re-creates parent markers after deletes and moves [source A8; observed].
  - cloudpathlib: a silent no-op on S3/GCS/flat Azure [source C5; observed].
  - GCS `create_dir` on a root creates a bucket [documented A6].
  - pyarrow `check_directory_existence_before_creation=False` by default means `create_dir` does not check for a same-named file [source A8 comment; documented A3].
- **OP-20**: pyarrow S3 silently drops non-whitelisted metadata keys, including `x-amz-meta-*` [source A8; observed]. smart_open needs different keys per transport [documented S1].
- **OP-21**: pyarrow needs S3 finalization at exit (handled by atexit in Python) [documented A6; source A9]. cloudpathlib cache cleanup depends on GC [documented C2]. smart_open: long-lived boto3 clients can leak memory [documented S3].
- **OP-22**: none of the three normalizes `..`, `.` or `//` [observed]. pyarrow rejects schemes; cloudpathlib requires them.
- **Credentials in URIs**: smart_open accepts `s3://key:secret@bucket/key` [documented S1]. If a client is also passed, "smart_open will ignore the latter" [documented S1].

## 7. Unreachable or not checked

- `https://raw.githubusercontent.com/piskvorky/smart_open/develop/README.rst` and `…/howto.md` return 404. I used `README.md` and `HOWTO.md` instead.
- The cloudpathlib pages `patching_builtins`, `anypath-polymorphism`, `authentication` and `why_cloudpathlib` are not cited (only fetched or listed).
- I did not run anything against real AWS, GCS or Azure. Every S3 observation is against moto 5.2.4. I made no observations for Azure HNS or GCS.
