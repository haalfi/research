# Track 02: MinIO probe of the S3 open items

- **Run:** by the user on 2026-10-26 against MinIO, using boto3 with the user's own client arguments.
- **Versions:** the user described the server as "latest officially released and supported free to use minio" as of 2026-10-26. No exact `RELEASE.*` tag was given. The boto3 version was not stated.
- **Script:** given in the conversation. It puts one 10-byte object (`0123456789`), runs the probes, then deletes the object.
- **Label:** every row is **[obs, MinIO]**. MinIO is S3-compatible, not AWS, so these results do not verify AWS behaviour. They do show that MinIO matches the behaviour RFC 9110 and AWS document.

| Probe | HTTP | Result |
|---|---|---|
| `Range: bytes=2-5` | 206 | `Content-Range: bytes 2-5/10`, body `2345` |
| `bytes=5-99` (end past EOF) | 206 | `bytes 5-9/10`, body `56789` (clamped) |
| `bytes=10-12` (start == size) | 416 | `InvalidRange`, "The requested range 'bytes=10-12' is not satisfiable" |
| `bytes=50-60` (start past EOF) | 416 | `InvalidRange` |
| `bytes=50-` (open range past EOF) | 416 | `InvalidRange`; the message renders the range as `'bytes=50--1'` (cosmetic quirk in MinIO's message) |
| `bytes=-3` (suffix) | 206 | `bytes 7-9/10`, body `789` |
| `bytes=-99` (suffix > size) | 206 | `bytes 0-9/10`, whole object |
| `delete_object` on a missing key | 204 | no error |
| `delete_objects` on a missing key | 200 | key listed under `Deleted` |
| `get_object` on a missing key | 404 | `NoSuchKey` |
| `head_object` on a missing key | 404 | code `'404'`, "Not Found" (a HEAD response has no error body) |
| `put_object(IfNoneMatch="*")` on an existing key | 412 | `PreconditionFailed` |
| `put_object(IfMatch='"deadbeef"')` | 412 | `PreconditionFailed` |

## Effect on the open items in the verified report

- **Range past EOF (OP-02):**
  - A start at or past the size gives 416 `InvalidRange`.
  - An end past EOF is clamped.
  - A suffix larger than the object returns the whole object.
  - This matches object_store's documented `GetRange::Bounded` rule (an error only if the range *starts* past the end) [doc OS].
  - AWS itself is still unverified.
- **Missing-key delete (OP-10):**
  - Single delete gives 204; batch delete reports the key as deleted.
  - This matches object_store's doc ("S3 and in-memory will return Ok") and the AWS DeleteObjects doc.
  - AWS single delete is still unverified on an AWS page.
- **Error codes (Q4):**
  - Strings observed on MinIO: `NoSuchKey`, `InvalidRange`, `PreconditionFailed`.
  - HEAD on a missing key returns no code string, only the status code (`'404'`). So status-based mapping is needed for `head_object` [obs; inf].
  - The AWS error-code list is still unreachable.
- **fsspec 2023.9 glob change:** not addressed by this probe.
