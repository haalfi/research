## Research brief (follow-up / verification run)

User request (2026-10-26): "yes, start the verified run"

Agreed scope of the verified run, as proposed in the conversation before that request:

- Base: the original brief `remote-store v1 operation catalogue` (same goal, questions, comparables,
  rules and output format) and its report on branch `research/remote-store-v1-operation-catalogue`
  (not edited; this run is a separate report so the two can be diffed).
- Fold in the points from a ChatGPT run on the identical brief that were verified against primary
  sources:
  1. OpenDAL Python binding differs from Rust core (`remove_all`, `scan` still present; `presign_*`
     only on `AsyncOperator`).
  2. OpenDAL conditional-operations specification ("never silently ignores a condition"; atomic with
     visible commit; no stat-then-mutate emulation).
  3. object_store `PutOptions`: unsupported `tags` are ignored, unsupported `attributes` must error.
  4. fsspec base file accepts mode `ab`; fsspec `checksum` and `ukey`.
  5. gocloud `Bucket` implements `io/fs.FS` (OP-17).
  6. Conditional read and post-write metadata/property update as separate Q1 rows.
- Add the S3 ETag vs MD5 point (from a Perplexity answer, checked against AWS `API_Object`).
- Keep the corrections to the ChatGPT run that were verified (versions, GCS `move_blob`, pyarrow
  move gating, cloudpathlib `mkdir`, pyarrow S3 metadata drop, presign count, scoping, fsspec close,
  GCS retries, Q5 change history).
- Where cheap, close open items left in the first report's caveats.
