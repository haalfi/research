# Track 01: deep-research workflow (fan-out search, 3-vote verification)

Run 2026-10-26, run id wf_5ee055db-2c2. All claims are documented behaviour read from the sources below; nothing observed by running code.

## Summary

The verified evidence (sources read 2026-10-26) covers fsspec, Rust object_store (0.14.0/0.14.2), Apache OpenDAL (opendal_core 0.59.5 and its Python binding), gocloud.dev/blob v0.47.0, the S3 conditional-writes guide and GCS request preconditions. It does not cover pyarrow.fs, smart_open, cloudpathlib or the Azure SDK. Q1: the comparables offer several operations no catalogue entry covers. These are grouped deferred-commit writes (fsspec Transaction), a key-value mapping view (fsspec FSMap), a FUSE mount and rsync-style sync (fsspec), and in OpenDAL append, presigned URLs, compose, restore, and listing of versions or deleted items, each capability-gated. Q2: the comparables merge where the catalogue splits. object_store makes plain put atomic and puts overwrite, create-if-absent and compare-and-swap into one put call with a PutMode. gocloud and OpenDAL treat conditions as options on the ordinary write, and GCS expresses if-absent as ifGenerationMatch=0. gocloud also folds list, walk and prefix filtering into one List(ListOptions) with no glob and no depth limit. This bears on keeping OP-03/04/05 and OP-06/07/08 as separate entries. Q3: OpenDAL exposes gates as a queryable Capability struct with per-operation and per-option flags and limits, which matches the gated OP-19/OP-20 approach and goes much further. For Q4 the evidence is thin: it shows only distinct error kinds for the conditional-write outcomes and object_store's split between a core trait and a convenience extension trait. The pitfalls for OP-05/OP-13/OP-04 are well documented: S3 412/409/404 races, versioned-bucket semantics, and the gap between atomic put and multipart or rename.

## Verified findings

### Q1 completeness gaps, fsspec  (high, vote 3-0 (claims 0, 1))

Q1 completeness gaps, fsspec: fsspec offers four operations with no catalogue entry. (a) A Transaction context (spec.Transaction, also .transaction on a filesystem) groups several writes for deferred commit, or discard on exception. Its docstring calls this 'semi-atomic', not truly atomic. (b) A MutableMapping key-value view (get_mapper/FSMap), whose keys are files under a root and whose values are bytes. (c) A FUSE mount (fuse.run). (d) generic.rsync, which syncs between filesystems with optional delete_missing and goes beyond OP-15's one-off transfer. open_local returns a local, possibly downloaded or cached, path. It is closer to OP-14 download than to OP-22 address mapping.

Sources:
- https://filesystem-spec.readthedocs.io/en/stable/_sources/api.rst.txt (stable docs, read 2026-10-26; PyPI latest fsspec 2026.9.0)
- https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/transaction.py (master, 2026-10-26)
- https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/mapping.py (master, 2026-10-26)
- https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/generic.py (master, 2026-10-26)

Evidence: api.rst lists spec.Transaction among the base classes, and fuse.run, generic.rsync, get_mapper and open_local among the user functions. transaction.py docstring: 'Gathers files for deferred commit or discard, so that several write operations can be finalized semi-atomically.' mapping.py: 'Wrap a FileSystem instance as a mutable wrapping.' Only fsspec is shown to offer these four, so the library count is 1 of the comparables checked.

### Q1 completeness gaps, OpenDAL  (high, vote 3-0 (claims 7, 10))

Q1 completeness gaps, OpenDAL: OpenDAL offers operations or options that no catalogue entry covers, each gated by a Capability flag. These are append writes (write_can_append), presigned URLs (presign, presign_read/stat/write/delete), composing an object from source objects (compose), restore (restore, restore_with_version), versioned read/stat/delete (read_with_version, stat_with_version, delete_with_version), and listing versions or deleted items (list_with_versions, list_with_deleted). Append, presign, compose and restore are operations in their own right. Versioning and deleted listing are options on existing operations.

Sources:
- https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html (opendal_core 0.59.5, read 2026-10-26)
- https://opendal.apache.org/docs/python/api/capability/ (Python binding, no version shown, read 2026-10-26)

Evidence: Field docs: 'write_can_append: Indicates if append operations are supported'; 'presign: Indicates if presigned URL generation is supported'; 'compose: Indicates if the operator supports composing complete source objects'; 'list_with_versions: If backend supports list with versions'. The library count is not established beyond OpenDAL, because a claim that gocloud offers SignedURL was refuted 1-2 and cannot be counted.

### Q2 the write cut  (high, vote 3-0 (claims 3, 15, 16))

Q2 the write cut: object_store does not have separate write, atomic-replace and conditional-write operations. Every put is documented as atomic, and the PutMode enum (Overwrite, the default; Create; Update(UpdateVersion)) selects the preconditions on one put_opts call. A plain put calls put_opts with PutOptions::default(), which is Overwrite. Streamed multipart upload is a separate required method (put_multipart_opts), and the quoted atomic guarantee does not cover it. Preconditions on copy go through copy_opts/CopyOptions, so they are separate from put.

Sources:
- https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStoreExt.html (0.14.0, read 2026-10-26)
- https://docs.rs/object_store/latest/object_store/enum.PutMode.html (resolved to 0.14.2, read 2026-10-26)

Evidence: put: 'The operation is guaranteed to be atomic ... No clients should be able to observe a partially written object.' PutMode: 'Configure preconditions for the put operation'; Overwrite: 'Perform an atomic write operation, overwriting any object present at the provided path.' The verifier read #[default] on Overwrite in src/lib.rs (main). Cost to a caller, advisory: with the merge, one call covers all three intents, but the streamed path has different guarantees. Keeping OP-03/OP-04/OP-05 separate makes those differences visible in the API but duplicates entry points.

### Q2 the write cut, other comparables  (high, vote 3-0 (claims 5, 8, 11, 21))

Q2 the write cut, other comparables: gocloud.dev/blob v0.47.0 offers conditional write only as 'if absent', through a WriterOptions.IfNotExist flag on the ordinary NewWriter/WriteAll/Upload path. It has no IfMatch, generation or ETag field, and other preconditions are reachable only through driver-specific BeforeWrite callbacks (inference from the As pattern). OpenDAL treats conditions as capability-gated options on write, with separate if_not_exists, if_none_match, if_match and if_version_match/not_match flags. GCS uses a single generation-match parameter for both forms: ifGenerationMatch=0 means 'only if no live object exists'. In all of these, conditional write is a mode of write, not its own operation.

Sources:
- https://pkg.go.dev/gocloud.dev/blob (v0.47.0, read 2026-10-26)
- https://raw.githubusercontent.com/google/go-cloud/v0.47.0/blob/blob.go (tag v0.47.0)
- https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html (0.59.5, read 2026-10-26)
- https://opendal.apache.org/docs/python/api/capability/ (read 2026-10-26)
- https://cloud.google.com/storage/docs/request-preconditions (last updated 2026-10-22, read 2026-10-26)

Evidence: blob.go WriterOptions: 'IfNotExist is used for conditional writes ... gcerrors.PreconditionFailed will be returned by Write or Close.' The drivers map it to S3 IfNoneMatch=*, GCS DoesNotExist, Azure IfNoneMatch any, and FailedPrecondition in fileblob and memblob. GCS: 'The generation-match precondition accepts the value 0 as a special case ... the request only proceeds if no object with the specified name exists in the bucket or if there are only noncurrent versions.'

### Q2 the list cut  (high, vote 3-0 (claims 6, 12, 14))

Q2 the list cut: gocloud.dev/blob folds listing, walking and prefix filtering into one List(ListOptions), with ListPage taking the same options. An empty Delimiter gives a flat recursive listing, and a non-empty Delimiter returns directory entries (IsDir). The options have no glob and no depth limit. fsspec goes the other way: it keeps glob, find and walk as separate operations, and its copy/get/put also accept globs and recursion (recursive=, maxdepth=) with POSIX cp semantics. OpenDAL gates recursive listing separately (list_with_recursive). The comparables therefore differ on whether OP-06/07/08 are one call with options or several calls.

Sources:
- https://pkg.go.dev/gocloud.dev/blob (v0.47.0, read 2026-10-26)
- https://raw.githubusercontent.com/fsspec/filesystem_spec/master/docs/source/copying.rst (master, read 2026-10-26)
- https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html (0.59.5)

Evidence: gocloud: 'An empty delimiter means that the bucket is treated as a single flat namespace.' ListOptions has only Prefix, Delimiter and BeforeList. fsspec copying.rst: sources and targets are 'one or more files, directories and/or glob (wildcard) patterns ... intended to be the same as ... POSIX command line cp'. In spec.py, copy(path1, path2, recursive=False, maxdepth=None) calls expand_path.

### Q2 the copy cut  (medium, vote 3-0 (claim 13))

Q2 the copy cut: fsspec splits copying by locality into copy (remote to remote), get (remote to local) and put (local to remote), and documents the same expected behaviour for all three. This matches the catalogue's OP-13 versus OP-14 split. fsspec's versions also take multiple targets and globs, recurse, and can create directories (auto_mkdir), which goes beyond OP-13/OP-14 as drafted.

Sources:
- https://raw.githubusercontent.com/fsspec/filesystem_spec/master/docs/source/copying.rst (master, read 2026-10-26)
- https://github.com/fsspec/filesystem_spec/pull/1226.patch (cited; unreachable to verifier)

Evidence: copying.rst: 'copy copies from a remote source to a remote target ... get copies from a remote source to a local target ... put copies from a local source to a remote target'. It is rated medium because the cited PR patch was unreachable. The current docs page confirmed the content, but this is a single library.

### Q3 gating  (high, vote 3-0 (claims 4, 6, 9))

Q3 gating: OpenDAL publishes a backend's capabilities as a queryable Capability struct, reached through OperatorInfo::capability. It has about 90 public fields: boolean flags and Option<usize> limits such as write_multi_max_size and delete_max_size. Gates cover nearly every operation and option, including read, write, stat, list, delete, create_dir, copy, rename, recursive listing, user metadata on write, append, presign, and the conditional and versioned variants. A caller finds out about a gate by querying the struct before calling, not only from an error. This matches the catalogue's gated OP-19 (create_dir) and OP-20 (write_with_user_metadata), and suggests that OP-12 move, OP-13 copy and OP-07 walk are gated in practice as well.

Sources:
- https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html (opendal_core 0.59.5, read 2026-10-26)
- https://opendal.apache.org/docs/python/api/capability/ (Python binding, read 2026-10-26)

Evidence: 'Capability defines the supported operations and their constraints for a storage Operator.' 'Developers should use capability to determine available operations.' Fields: 'create_dir: Indicates if directory creation is supported. rename: ... copy: ... list_with_recursive: ... write_with_user_metadata: ...' Inference, not verified: OpenDAL's completion layer may emulate some operations, so a flag may describe native support rather than what the caller actually gets.

### Q4 shared decisions, error taxonomy for conditional outcomes  (high, vote 3-0 (claims 11, 17, 18, 20, 21))

Q4 shared decisions, error taxonomy for conditional outcomes: the comparables give conditional failures dedicated error kinds that every backend shares. object_store separates Error::AlreadyExists (PutMode::Create) from Error::Precondition (PutMode::Update), and keeps NotImplemented and NotSupported as further variants. gocloud maps if-absent conflicts to gcerrors.PreconditionFailed on every driver, fileblob and memblob included. At the wire level, S3 and GCS both use HTTP 412.

Sources:
- https://docs.rs/object_store/latest/object_store/enum.PutMode.html (0.14.2, read 2026-10-26)
- https://raw.githubusercontent.com/google/go-cloud/v0.47.0/blob/blob.go (v0.47.0)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html (read 2026-10-26)
- https://cloud.google.com/storage/docs/request-preconditions (last updated 2026-10-22)

Evidence: PutMode::Create: 'returning Error::AlreadyExists if an object already exists'; Update: 'returning Error::Precondition otherwise'. S3: 'the first write operation to finish succeeds. Amazon S3 then fails subsequent writes with a 412 Precondition Failed response.' These are documented, not observed. Backends without support may return NotImplemented or NotSupported instead.

### Q4 shared decisions, API layering  (high, vote 3-0 (claim 2))

Q4 shared decisions, API layering: object_store keeps a small core trait (put_opts, put_multipart_opts, get_opts, list, list_with_delimiter, delete_stream, copy_opts, with default get_ranges, list_with_offset and rename_opts). Convenience methods (put, put_multipart, get, get_range, head, delete, copy, copy_if_not_exists, rename, rename_if_not_exists) sit in ObjectStoreExt, which is implemented automatically for every store and must not be implemented by hand. Backends implement only the option-taking core, and the intent-level calls are derived once for all of them.

Sources:
- https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStoreExt.html (0.14.0, read 2026-10-26)
- https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStore.html (0.14.0)

Evidence: 'Extension trait for ObjectStore with convenience functions.' 'You MUST NOT implement this trait yourself. It is automatically implemented for all ObjectStore implementations.' This is relevant to the catalogue's cut, because one intent entry can map to one core call with options.

### Q5 pitfalls for OP-05 and OP-13 (S3)  (high, vote 3-0 (claims 19, 20))

Q5 pitfalls for OP-05 and OP-13 (S3): S3 accepts both If-None-Match: * (if absent) and If-Match: <ETag> (if unchanged) on PutObject, CompleteMultipartUpload and CopyObject, so both conditional write forms and a destination-conditioned copy are native. Pitfalls documented on the same page: (a) Concurrent requests can also return 409 Conflict, and under If-Match a delete that wins the race gives 404. A caller should not treat 412 as the only conflict outcome. (b) After a 409 a PutObject may be retried, but a multipart upload must restart from CreateMultipartUpload. (c) In versioned buckets If-None-Match applies only to the current version, and a delete marker counts as absent. (d) If-Match needs both s3:PutObject and s3:GetObject permissions. (e) The destination condition on a copy is separate from the x-amz-copy-source-if-* source conditions.

Sources:
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html (read 2026-10-26)

Evidence: 'You can use the If-None-Match header with the following APIs: PutObject, CompleteMultipartUpload, CopyObject ... You can use the If-Match header with the following APIs: PutObject, CompleteMultipartUpload, CopyObject.' 'If multiple conditional writes or copies occur for the same object name, the first write operation to finish succeeds.' Limits for directory buckets and S3 Express were not checked.

### Q5 pitfalls for OP-05, OP-01 and OP-09 (GCS)  (high, vote 3-0 (claims 5, 10, 21, 22))

Q5 pitfalls for OP-05, OP-01 and OP-09 (GCS): GCS recommends generation and metageneration preconditions over ETags, because they are stronger and consistent across APIs. They come in Match and NotMatch forms, with NotMatch on the JSON API only, and enable safe read-modify-write. Pitfalls: ifGenerationMatch=0 means 'no live version', so noncurrent versions do not block it, and the docs say to use 0 only for writes. Preconditions cannot be used with XML API multipart uploads (400 NotImplemented). A NotMatch check that matches returns 304. OpenDAL likewise exposes conditional read and stat (if_match, if_none_match, if_modified_since, if_unmodified_since) and conditional delete and copy as gated options. Conditions therefore attach to several catalogue entries, not to OP-05 alone.

Sources:
- https://cloud.google.com/storage/docs/request-preconditions (last updated 2026-10-22, read 2026-10-26)
- https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html (0.59.5)
- https://opendal.apache.org/docs/python/api/capability/ (read 2026-10-26)

Evidence: GCS: 'You should generally use generation and metageneration preconditions instead of ETag preconditions.' 'Preconditions are often used to prevent race conditions in mutating requests, such as uploads, deletes, or metadata updates.'

### Q5 pitfalls for OP-03, OP-04 and OP-12 (object_store)  (medium, vote 3-0 (claims 3, 16; the rename detail is verifier evidence, not a standalone claim))

Q5 pitfalls for OP-03, OP-04 and OP-12 (object_store): the atomic-put guarantee is documented for a single-payload put/put_opts and is not stated for the streamed put_multipart path. rename is documented as copy-then-delete by default, so it is not atomic. Of the convenience methods, only copy_if_not_exists is documented as atomic besides put. Advisory note for later sessions: atomic replace and atomic move have different guarantees on object stores.

Sources:
- https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStoreExt.html (0.14.0, read 2026-10-26)
- https://docs.rs/object_store/latest/object_store/enum.PutMode.html (0.14.2)

Evidence: Verifier notes on claim 3: 'rename is documented as copy-then-delete by default, so it is not atomic' and 'The streamed path, put_multipart, is a different method, and the quoted text does not cover it.' Rated medium because these points come from verifier commentary, not from separately voted claims.

## Refuted (do not use)

- (0-3) copy_if_not_exists is gated on the backend's capability. It is atomic only where the store supports that, and on stores without atomic support, S3 among them, it returns an error. A caller learns of the gate from a runtime error, not from a capability query. — https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStoreExt.html
- (1-2) The Bucket surface includes operations with no remote-store catalogue entry: SignedURL (a presigned URL that defaults to GET and a one-hour expiry), ListPage (paginated listing with a page token), and DeleteWithOptions. SignedURL is gated per driver and reports the gate through an Unimplemented error code, not through a capability query. — https://pkg.go.dev/gocloud.dev/blob

## Caveats

Coverage is uneven. No verified claims cover pyarrow.fs, smart_open, cloudpathlib, the Azure Blob SDK, or boto3 beyond the S3 conditional-writes guide. Library counts per gap operation (Q1) are therefore lower bounds, and the catalogue-versus-comparable table can be filled only for fsspec, object_store, OpenDAL, gocloud, S3 and GCS. Q4 is largely unanswered: no verified evidence covers key validation, timeouts and retries, consistency guarantees, closing, or async parity. Two claims were refuted and must not be used. One said object_store's copy_if_not_exists reports its gate only through a runtime error (0-3). The other was about gocloud SignedURL/ListPage/DeleteWithOptions and Unimplemented-error gating (1-2). How object_store and gocloud signal capability gates is therefore unverified. Versions: object_store evidence mixes 0.14.0 and 0.14.2 (docs.rs 'latest'). The OpenDAL Python page shows no version, and the Rust page's 0.59.5 comes from the page header or docs.rs. pkg.go.dev notes that the blob package is not in the latest version of its module. fsspec facts come from stable docs and master source (PyPI 2026.9.0), and the fsspec copy PR patch was unreachable. Everything here is documented behaviour; nothing was observed by running code. Some mappings to catalogue entries are interpretation: open_local to OP-22, FSMap to OP-17, and OpenDAL flags to the OP numbers. Mappings and the advisory remarks are inference, not source statements. Time-sensitivity: the S3 conditional-write support matrix, GCS preconditions (updated 2026-10-22) and pre-1.0 crates (object_store, OpenDAL) change often.

## Open questions

- How do pyarrow.fs, smart_open, cloudpathlib and the Azure Blob SDK cover the catalogue? In particular, does Azure's If-Match/If-None-Match support on uploads and copies match S3 and GCS, and does any of these libraries expose a capability query rather than errors or documentation?
- Which shared policies do the comparables set once for every operation: path/key validation and normalisation, retry and timeout configuration, documented read-after-write and list consistency, close/context-manager semantics, and sync/async parity (for example fsspec async filesystems, OpenDAL blocking vs async Operator)?
- How do object_store and gocloud tell a caller that a backend lacks an operation or mode (for example PutMode::Update on a store without CAS, or a driver without signed URLs)? The two claims on this were refuted.
- Does OpenDAL's completion/emulation layer change what a Capability flag means (native vs emulated create_dir, recursive list, copy, rename), and does it change the atomicity a caller gets for emulated move and copy?

## Sources fetched

| URL | quality | angle |
|---|---|---|
| https://filesystem-spec.readthedocs.io/en/stable/_sources/api.rst.txt | primary | Operation surface of the abstraction layers (completeness) |
| https://docs.rs/object_store/0.14.0/object_store/trait.ObjectStoreExt.html | primary | Operation surface of the abstraction layers (completeness) |
| https://opendal.apache.org/docs/rust/opendal_core/struct.Capability.html | primary | Operation surface of the abstraction layers (completeness) |
| https://opendal.apache.org/docs/python/api/capability/ | primary | Operation surface of the abstraction layers (completeness) |
| https://pkg.go.dev/gocloud.dev/blob | primary | Operation surface of the abstraction layers (completeness) |
| https://github.com/fsspec/filesystem_spec/pull/1226.patch | primary | Operation surface of the abstraction layers (completeness) |
| https://docs.rs/object_store/latest/object_store/enum.PutMode.html | primary | Conditional and atomic writes (the cut) |
| https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html | primary | Conditional and atomic writes (the cut) |
| https://cloud.google.com/storage/docs/request-preconditions | primary | Conditional and atomic writes (the cut) |
| https://docs.cloud.google.com/python/docs/reference/storage/latest/generation_metageneration | primary | Conditional and atomic writes (the cut) |
| https://learn.microsoft.com/rest/api/storageservices/specifying-conditional-headers-for-blob-service-operations | primary | Conditional and atomic writes (the cut) |
| https://developmentseed.org/obstore/latest/api/put | primary | Conditional and atomic writes (the cut) |
| https://opendal.apache.org/docs/rust/opendal/struct.Capability.html | primary | Capability gating and discovery |
| https://pkg.go.dev/gocloud.dev/blob/driver | primary | Capability gating and discovery |
| https://github.com/apache/arrow-rs/pull/6682 | primary | Capability gating and discovery |
| https://docs.rs/object_store/latest | primary | Cross-cutting decisions: errors, retries, timeouts, async, close |
| https://developmentseed.org/obstore/latest/api/store/config/ | primary | Cross-cutting decisions: errors, retries, timeouts, async, close |
| https://pkg.go.dev/gocloud.dev@v0.44.0/internal/gcerr | primary | Cross-cutting decisions: errors, retries, timeouts, async, close |
| https://filesystem-spec.readthedocs.io/en/latest/async.html | primary | Cross-cutting decisions: errors, retries, timeouts, async, close |
| https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/introduction.html | primary | Object-store vs filesystem pitfalls (practitioner issues) |
| https://hadoop.apache.org/docs/r3.3.6/hadoop-aws/tools/hadoop-aws/committer_architecture.html | primary | Object-store vs filesystem pitfalls (practitioner issues) |
| https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html | primary | Object-store vs filesystem pitfalls (practitioner issues) |
| https://github.com/drivendataorg/cloudpathlib/issues/51 | forum | Object-store vs filesystem pitfalls (practitioner issues) |

Stats: {"angles": 5, "sourcesFetched": 23, "claimsExtracted": 115, "claimsVerified": 25, "confirmed": 23, "killed": 2, "unverified": 0, "afterSynthesis": 12, "urlDupes": 3, "budgetDropped": 4, "agentCalls": 105}
