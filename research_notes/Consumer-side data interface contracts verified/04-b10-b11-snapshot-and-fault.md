# Track 4 (verification run): B10 snapshot vs delta; B11 failure attribution

A delegated research agent produced this on 2026-11-19; the main session spot-checked it (below).
Labels are the agent's unless marked "(spot-check)". The agent's downloads are in the session scratchpad `b10/`.

## Spot-checks (main session) [F]
- **GTFS-RT proto** (raw.githubusercontent.com/google/transit/master/gtfs-realtime/proto/gtfs-realtime.proto, HTTP 200):
  `enum Incrementality { FULL_DATASET = 0; DIFFERENTIAL = 1; }` and `optional Incrementality incrementality = 2 [default = FULL_DATASET];` (l.65–69).
- **RFC 5005** (rfc-editor txt, HTTP 200; "Category: Standards Track"):
  - "A complete feed is a feed document that contains all of the entries of a logical feed; any entry not actually in the feed document SHOULD NOT be considered part of that feed."
  - "The fh:complete element, when present in a feed's head section, indicates that the feed document it occurs in is a complete representation of the logical feed's entries."
- **RFC 9110** (local copy): §15.5 "…seems to have erred" (l.7535); §15.6 "…is aware that it has erred or is incapable of performing…" (l.7855).

## B10: full snapshot vs increment
**Fields that declare full state** [F unless noted]:
- **GTFS-Realtime** `FeedHeader.incrementality` (MobilityData; reference page last-modified 2026-11-03).
  - FULL_DATASET: "this feed update will overwrite all preceding realtime information for the feed … expected to provide a full snapshot".
  - DIFFERENTIAL: "currently, this mode is unsupported and behavior is unspecified".
  - `FeedEntity.is_deleted` is for DIFFERENTIAL only.
- **RFC 5005** Feed Paging and Archiving (IETF Standards Track, 2007): `fh:complete`, namespace `http://purl.org/syndication/history/1.0` (quotes above).
  §3 says "clients SHOULD NOT present paged feeds as coherent or complete".
- **ISO 20022** `Statement/UpdTp`, StatementUpdateType1Code (e.g. semt.002) [S, mirrors; iso20022.org 403]:
  - `COMP` "Statement is complete."
  - `DELT` "Statement contains changes only."
  - Pagination1 `LastPageIndicator` marks that a multi-message delivery is finished, not that it is full state [S].

**Increment markers only**:
- OData JSON v4.01 §15 delta payload (`$delta`, `@removed`, `@deltaLink`). A non-delta response is not declared complete [F/I].
- RFC 3229: 226 IM Used, "might not be available except by combining this response with other previous or future responses" [F]. RFC 9110 206 is byte ranges [F].
- SDMX 3.0 `action`: Append/Replace/Delete/Information [F]. SDMX 3.1: Merge/Replace/Delete, where "Replace … cannot be used to replace a whole dataset". A full replace is only an idiom (wildcard Delete + Merge/Replace) [F].
- Debezium (open-source project, not a standard): `op` r = snapshot read; `source.snapshot` TRUE/FIRST/…/LAST/FALSE/INCREMENTAL. Record-level only [F].
- Iceberg snapshot `summary.operation` append/replace/overwrite/delete. `overwrite` may be partial; no full-refresh value [F].
- Delta Lake `dataChange`; `commitInfo` is free JSON; no full/increment field [F].
- Delta Sharing: the mode is set by the request (`startingVersion`); `limitHint` lets "the server … return only some files" [F].
- Hudi: INSERT_OVERWRITE_TABLE "overwrite the entire table". An implementation operation type, not a standard [F].
- OpenLineage LifecycleStateChange OVERWRITE etc. Scope is undefined [F].

**None found in**: CloudEvents, DCAT 3, DCMI `accrualMethod`, Frictionless, DQV (only a `populationCompletenessMetric` example measurement), and ODCS v3.2.0 (`dataGranularityDescription` is grain only) [F].

**Verdict**: full-state declarations exist (GTFS-RT, RFC 5005, ISO 20022 COMP/DELT), but each is bound to its own payload.
- With ODCS, concern 9's "population stated whole" is **custom**, with referenceable semantics (RFC 5005 §2 / GTFS-RT FULL_DATASET via `authoritativeDefinitions`).
- It is no longer "none".

## B11: failure attribution
- **RFC 9110 §15** (STD 97) [F]:
  - 4xx "client seems to have erred"; 5xx "server is aware that it has erred". This attributes fault side explicitly.
  - 404: "does not indicate whether this lack of representation is temporary or permanent".
  - 410: "intentionally unavailable".
  - Absence is filed under client error.
- **RFC 9457** Problem Details: open `type` URI; the IANA registry (updated 2026-06-26) has about:blank + 5 types, all 400. No fault taxonomy [F].
- **gRPC status codes** [F]:
  - Text names the side on some codes (INVALID_ARGUMENT "The client specified…").
  - The UNAVAILABLE / ABORTED / FAILED_PRECONDITION split is by retry guidance.
  - The "Generated at Client or Server" table shows origin, not fault.
- **OpenTelemetry semconv** (Stable for HTTP and gRPC spans) [F]:
  - HTTP 4xx: span status "MUST be left unset … SERVER and SHOULD be set to Error … CLIENT".
  - "a 404 … is not an error when the application is simply checking whether the resource exists".
  - The gRPC server error list is UNKNOWN, DEADLINE_EXCEEDED, UNIMPLEMENTED, INTERNAL, UNAVAILABLE, DATA_LOSS.
  - `error.type` has only `_OTHER` well-known.
- **SARIF 2.1.0** (OASIS) [F]:
  - `result.kind` pass/fail/open/informational/notApplicable/review. notApplicable: "does not apply to the analysis target".
  - Notifications are split by audience (tool developers vs configuring engineers vs code developers).
  - A failed run "SHALL NOT" be assumed complete.
- **Outcome type only** [F]: JUnit XML (failure vs error), TAP 14 (SKIP/TODO/Bail out), in-toto test-result (PASSED/WARNED/FAILED), Open Test Reporting, OORS (error "query failed, or the source was unreachable", which mixes both sides), OpenLineage, DQV, ODCS.

**Verdict**: no standard gives the three-way class (consumer fault / provider fault / legitimate absence) for a data check.
- RFC 9110 and OTel give a two-sided perspective for calls. SARIF gives "not applicable".
- Coverage class for concern 10's failure class: **custom**, with values mappable to RFC 9110 classes, gRPC codes or OTel conventions. It is no longer "none" in the sense of "no reusable semantics".
