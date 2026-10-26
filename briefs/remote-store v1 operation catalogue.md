## Research brief

**Goal.** Test the drafted operation catalogue of `remote-store` v1, a Python
library that gives one API over local disk, in-memory, S3, SFTP, Azure and more
storage, against what comparable libraries offer. The catalogue lists *what*
v1 offers, one entry per intent; *how* each entry behaves is designed later,
one entry per session. The research informs the catalogue; it decides nothing.


**Draft entries** (one per intent):

| ID | Intent | stable version counterpart |
| --- | --- | --- |
| OP-01 | Read an item, whole or streamed | `read`, `read_bytes`, `read_text` |
| OP-02 | Read an item at offsets | `read_seekable` (SEEKABLE_READ) |
| OP-03 | Write an item, whole or streamed | `write`, `write_text` |
| OP-04 | Replace an item atomically | `write_atomic`, `open_atomic` |
| OP-05 | Write conditionally (if absent, if unchanged) | `write(overwrite=False)`, if absent only |
| OP-06 | List a folder's children | `iter_children`, `list_files`, `list_folders` |
| OP-07 | Walk a subtree, optionally depth-limited | `list_files(recursive, max_depth)`, `list_folders(max_depth)` |
| OP-08 | Match keys by pattern | `glob`, `list_files(pattern)`, `list_folders(pattern)` |
| OP-09 | Inspect: exists, kind, size, time | `exists`, `is_file`, `is_folder`, `get_file_info`, `get_folder_info`, `head` |
| OP-10 | Delete an item | `delete` |
| OP-11 | Delete a folder tree | `delete_folder` |
| OP-12 | Move or rename | `move` |
| OP-13 | Copy within a store | `copy` |
| OP-14 | Transfer to or from local disk | `ext.transfer.upload`, `download` |
| OP-15 | Transfer between stores | `ext.transfer.transfer` |
| OP-16 | Scope a store to a folder | `child` |
| OP-17 | Hand items to other libraries | `ext.arrow.pyarrow_fs` |
| OP-18 | Ask what a store supports | `supports` |
| OP-19 | Create an empty folder (optional, gated) | — |
| OP-20 | User metadata (optional, gated) | `write(metadata=)`, USER_METADATA |
| OP-21 | Store lifecycle (close, context manager) | `close` |
| OP-22 | Native address mapping | `native_path`, `to_key` |
| OP-23 | Native handle escape hatch | `unwrap` |
| OP-24 | Health check | `ping` |


**Questions.**

1. **Completeness.** Which operations do the comparable libraries offer that
   no catalogue entry covers? For each, the use case it serves and how many of
   the libraries offer it.
2. **The cut.** Where would the comparables split or merge entries
   differently, for example write against atomic replace against conditional
   write, or list against walk against pattern match? What each choice costs a
   caller.
3. **Optional entries.** Which operations do the comparables gate on a
   backend's capability, and how does a caller learn of the gate (a query, an
   error, documentation)?
4. **Shared decisions.** What do the comparables decide once for every
   operation rather than per operation: key validation, error taxonomy,
   timeouts and retries, consistency, closing, async parity?
5. **Pitfalls.** Per entry, the object-store or filesystem behaviours that
   made comparables change or split an operation, cited, as notes for the
   entry's later session. No proposal of semantics.

**Comparables.** fsspec, `pyarrow.fs`, Apache OpenDAL (Rust core and its
Python binding), Rust `object_store` (arrow-rs), Go `gocloud.dev/blob`,
`smart_open`, `cloudpathlib`, and the AWS S3, Azure Blob and Google Cloud
Storage SDKs. Others where a question needs them.

**Rules.** Cite every claim with a link and the version or date read. Tell
documented behaviour apart from observed. Do not read `remote-store`'s stable
code or specs as an authority; the catalogue's stable version column is only an
omission check.

**Output.** One Markdown doc: a dated header, the sources with versions, one
section per question, and a table of catalogue entry against comparable (who
offers it, under which name, gated or not). Recommendations are marked
advisory.
