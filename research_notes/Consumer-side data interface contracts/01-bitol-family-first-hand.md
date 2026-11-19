# Track 1: Bitol family (ODCS, ODPS, OORS, open RFCs), first-hand

Access date: 2026-11-19. Sources: shallow `git clone` of the public repos (raw files read locally).
All items below are **first-hand** (spec text or JSON schema read) unless marked otherwise.

| Repo | HEAD read | HEAD date |
|---|---|---|
| bitol-io/open-data-contract-standard | 7c7597e | 2026-11-17 |
| bitol-io/open-data-product-standard | 5f54a17 | 2026-09-11 |
| bitol-io/open-observability-results-standard | e348e71 | 2026-11-09 |
| bitol-io/tsc (RFC index) | 1f1c6d7 | 2026-11-10 |

## Versions and cadence
- ODCS tags: v2.2.1 (2023-12-18), v3.0.2 (2025-03-31), v3.1.0 (2025-12-08), **v3.2.0 (2026-09-08, "APPROVED", CHANGELOG.md)**.
  JSON schemas are re-issued as dated snapshots (`schema/odcs-json-schema-v3.2.0-20261117.json`, …); `CHANGELOG.md` notes that
  "the standard is not the JSON Schema but the textual document" (v3.1.0 section).
- ODPS tags: v0.9.0 (2025-07-15), v1.0.0 (2025-09-24), **v1.1.0 (2026-09-08)**.
- OORS (Open Observability Results Standard): tag **v0.8.0 (2026-10-14)**; v0.8.1 in CHANGELOG as DRAFT; every OORS changelog entry is
  labelled "DRAFT". Founding RFC-0018 approved by the TSC 2026-10-14. tsc/rfcs/README.md lists RFC 0035/0050 "approved for OORS v1.0.0",
  but no v1.0.0 tag/schema exists at HEAD → OORS v1.0.0 is **not released** as of the cutoff.
- Governance: Bitol (Linux Foundation AI & Data project, *secondary*: stated on bitol.io, not re-read here); TSC approves RFCs
  (`tsc/rfcs/README.md`, "accepted by the TSC"). Licence Apache-2.0 (SPDX headers in docs).

## ODCS v3.2.0: what changed since v3.1.0 (CHANGELOG.md, v3.2.0 section)
Added: enum, map, context block, semanticType, synonyms, server `encoding` (RFC 0043), deprecated flag, `customProperties[].vendor`
(RFC 0035), vector type, new server types (hana, iceberg, exasol, teradata, ingres, vectorwise, versant, poet), SLA
`customProperties`/`authoritativeDefinitions` (RFC 0046), variables `${VAR}` (RFC 0050), relationship `id` (RFC 0047),
wider `id` charset, DQ operators `oneOf`→`anyOf`.
**None of these natively covers concerns 1–11.** Nearest touches:
- RFC 0043 `encoding` on SFTP/S3/Local/Custom servers: character encoding only → a sliver of concern 9 (dialect).
- RFC 0046: SLA entries can now carry `customProperties` → concern 10's extra SLO fields become *attached* custom extensions, still unvalidated.
- RFC 0035 `vendor` on customProperties: namespacing for custom extensions, not semantics.

## ODCS native fields relevant to the concerns (schema `odcs-json-schema-v3.2.0.json`)
- Top level: `version` (string, contract version), `status` (examples proposed/draft/active/deprecated/retired, not an enum),
  `contractCreatedTs` (date-time, "when the data contract was created"). No valid-from/valid-to, no knowledge/recorded time → concern 1 not native.
- `slaProperties[]` (`docs/service-level-agreement.md`): `property` (recommended: availability, throughput, errorRate,
  generalAvailability, endOfSupport, endOfLife, retention, frequency, latency, timeToDetect, timeToNotify, timeToRepair),
  `value`, `valueExt`, `unit`, `element`, `driver` (regulatory/analytics/operational), `scheduler`, `schedule` (cron),
  `timeOfAvailability` appears in the example list. `property` is free string ("There is no limit on the type of properties").
  → partial native for concern 4 (frequency + timeOfAvailability, a single time-of-day; no calendar, no per-delivery expectation)
  and for concern 3 only as "schedule of the SLA check", not of our requests.
- `quality[]` (DataQuality def): `id`, `name`, `description`, `dimension` (enum accuracy, completeness, conformity, consistency,
  coverage, timeliness, uniqueness), `severity` (free string; examples info/warning/error), `businessImpact` (free string,
  "Consequences of the rule failure"), `method`, `schedule`/`scheduler`, `type` (text/library/sql/custom), `unit`,
  operators (`mustBe`, `mustBeLessThan`, …), `customProperties`. `unevaluatedProperties: false`.
  → concern 10: indicator (metric/query + unit) and objective (operator threshold) are native; consequence ≈ `businessImpact`
  (free text); failure class finer than severity: **not native** (only customProperties).
- Library metric `missingValues` with argument `missingValues: [null, '', 'N/A']` (`docs/data-quality.md`): declares which tokens
  *count as missing* for a check; it does not distinguish "absent" from "explicitly empty" → concern 9 partial at best.
- Servers (`$defs.ServerSource`): `SftpServer` {location sftp://…, format, encoding, delimiter}, `S3Server` {location, endpointUrl,
  format, encoding, delimiter}, `ApiServer` {location only}. `delimiter` is documented "Only for format = json. How multiple json
  documents are delimited within one file" → **no CSV dialect** (separator, header rows, trailer) natively.
- References (`docs/references.md`, new in v3.1.0): fully qualified `<file>#/<section>/<id>/…`; ids for most array items;
  cross-contract references by file path or URL. "References are currently only supported for foreign key relationships."
  → there is no generic field to point from ODCS to an external non-ODCS spec except `authoritativeDefinitions` (type + url).
- `customProperties[]`: `property`, `value`, optional `id`, `description`, `vendor` (v3.2.0). Values unvalidated by the ODCS schema.

## ODPS v1.1.0 (schema `odps-json-schema-v1.1.0.json`)
Top-level keys: apiVersion, kind, id, name, deprecated, synonyms, version, status, domain, type, context, tenant,
authoritativeDefinitions, description, customProperties, tags, inputPorts, outputPorts, managementPorts, support, team, productCreatedTs.
`InputPort` = {id, name, version, contractId, tags, customProperties, authoritativeDefinitions, deprecated}, additionalProperties: false.
→ the explicit cross-document reference mechanism is `contractId` + `version` (a port pins a contract version). No schedules, no SLOs.

## OORS v0.8.0 / v0.8.1 draft (schemas in repo; draft 2019-09)
Required: apiVersion, kind (`ObservabilityResults`), id, observedAt, source{process, runId, vendor}, results[].
Optional: `run` {state running|completed|aborted, sequence, progress}, `run.startedAt` (0.8.1),
`contract` {contractId, standard (ODCS/ODPS), version, server} — **one** contract per document,
results[] {id, type check|metric, name, status pass|fail|warn|error|skip(|unknown in 0.8.1), relatesTo (path into the contract),
severity, dimension, target{resourceType, resourceIdentifier, filter(0.8.1)}, measure{metric, value, threshold, unit,
rowCount, failedRowCount (0.8.1)}, message, customProperties, tags}.
→ Concern 11: native for "which check ran on what, against which contract version and server, with what outcome".
  Not native: the inventory of what was read (files/objects, byte sizes, digests, provider publication times), several
  contract versions per run (one `contract` object), and our failure classes (status `error` ≠ provider fault vs our fault).
→ Concern 10: OORS `status` distinguishes fail (verdict) from error (no verdict) and skip; still not "provider's fault" vs "expected absence".

## Open (unapproved) Bitol RFCs touching the concerns (tsc/rfcs/README.md "Open RFCs")
Not usable as standards; listed because they show the gap is recognised.
- RFC 0052 `logicalType: blob`: file-properties mode (name, prefix, size, contentType, lastModified, etag, contentMD5, …) →
  concern 2 and 9 (files of a delivery). Open.
- RFC 0040 OOCS (Open Orchestration and Control Standard): "what should happen" (requests/actions) → concern 3/5. Open, no release.
- RFC 0062 Signatures: `signatures` array for every Bitol doc; targets ODCS v3.3.0 / ODPS v1.2.0 / OORS v1.0.0. Open.
- RFC 0032 Imports, RFC 0063 Single Artifact: cross-document reuse/bundling → Q4 glue. Open.
- RFC 0011 Lineage: open.
