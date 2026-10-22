# Input: verification pass on "Black box boundary spec methods"

## 0. Preflight (stop if it fails)

The previous run could not fetch full texts (proxy 403, DNS `ENOTFOUND`).
Before anything else, run:

    curl -sS -o /dev/null -w "%{http_code}\n" https://arxiv.org/abs/2509.22908

Anything other than `200` means the network policy still blocks it. Stop
and report which hosts fail; do not continue on search extracts.

## 1. Material

Fetch branch `research/black-box-boundary-spec` from `origin`. It holds:

- `briefs/original-brief.md`: the research question and its § 9 deliverable.
  It stays authoritative for scope, grading (A–D) and constraints.
- `reports/Black box boundary spec methods.md`: the report under review.
- `research_notes/Black box boundary spec methods/*.md`: six notes files
  behind it, one per research track.

Every finding in them rests on search-engine extracts, not full texts.

## 2. Task

This is a verification pass, not a new study. The question is what
survives contact with the full texts.

1. **Verify claims.** Check against the full text:
   - every item marked † (23 in the report);
   - every figure, percentage and quotation;
   - every claim graded A or B.

   For each one, record a verdict: *confirmed*, *corrected* (give the right
   value), *not found in source*, or *refuted*.
2. **Close named gaps.** Do this only where the full text is reachable:
   - EARS RE'09 figures (Mavin et al.);
   - which flags replaced Hadoop's `is-blobstore` (HADOOP-13501/13502), and
     the current wording of `open()`/`openFile()` in the FileSystem spec;
   - Python `io`: whether buffered `read` may return `None` or must raise
     `BlockingIOError` (docs vs CPython);
   - AWS S3 consistency wording for an overwrite during an open read;
   - Newcombe et al. (CACM 2015) DynamoDB figures; SQLite test-code ratio;
   - ACSL, Spec#/Code Contracts, VDM/Z/B error handling;
   - Go error conventions, Google AIP-193/194, PEP 3151, POSIX `read()`;
   - fsspec `spec.py`, Arrow FileSystem, Estler et al. 2014 (contracts in
     practice), TorXakis, Spec Explorer data.
3. **Look for disconfirming evidence.** Search specifically for:
   - (a) any published rule that maps spec category or claim type to
     notation or form (the report says none exists);
   - (b) any controlled study comparing spec formats (EARS, Gherkin,
     tables, prose, formal) for LLM agents (the report says none exists);
   - (c) any method that models a long-lived stream as an operation with
     an extent, or that treats an out-of-band store actor as distinct from
     another client.

   Report what you find either way.
4. **Check the agent figures again** in § 6 of the report against the
   published versions of the papers. Some cited works were preprints and
   may since have been peer-reviewed or revised.

## 3. Output

- `reports/Black box boundary spec methods verified.md`: the corrected
  report. Keep the § 9 structure. Keep the original file unchanged so the
  two can be diffed. Drop the † marks that verification removed. Remove
  or downgrade claims that fail.
- `research_notes/Black box boundary spec methods/verification_log.md`:
  one row per checked claim, with location, claim, source URL, verdict and
  correction.
- At the top of the corrected report, a short "What changed" list covering
  any change to the Kernsatz, the form rule, the scorecard or the
  shortlist.

## 4. Constraints

- Grade sources A–D as in the brief. C and D never outweigh A and B. Mark
  inference as inference.
- Change conclusions only where the evidence changes. Note anything that
  is merely restyled.
- Do not design the library's semantics and do not choose a format.
- Do not use the project's existing specs or code.
- Commit to the branch above and push.
