# Track 2: adjacent open standards, first-hand

Access date: 2026-11-19. Read from shallow clones (raw files) unless a URL is given. All **first-hand** unless marked.

| Spec | Version read | Source (HEAD) |
|---|---|---|
| Frictionless Data Package (Data Package, Data Resource, Table Dialect, Table Schema) | v2.0 (changelog: June 26, 2024) | frictionlessdata/datapackage da3526c (2026-08-25), `content/docs/standard/*.mdx` |
| Arazzo | 1.1.0 (Appendix A: 2026-05-17); 1.0.1 (2025-01-16) | OAI/Arazzo-Specification 12f619e, `versions/1.1.0.md` |
| OpenSLO | v1 (v2alpha = "living document", not stable) | OpenSLO/OpenSLO e025975 (2026-09-25), `website/docs/specification.md`, `enhancements/v2alpha.md` |
| OpenLineage | core spec 2-0-2 (`$id` https://openlineage.io/spec/2-0-2/OpenLineage.json) | OpenLineage/OpenLineage 3e93c95 (2026-11-19), `spec/` |
| CloudEvents | 1.0.x | cloudevents/spec 56b5413, `cloudevents/spec.md` |
| in-toto Attestation Framework | v1 | in-toto/attestation 50bf017 (2026-10-21), `spec/v1/*`, `spec/predicates/*` |
| Croissant | 1.1 | mlcommons/croissant 5be1998, `docs/croissant-spec-1.1.md` |
| W3C CSVW Metadata Vocabulary | W3C Recommendation (2015) | https://www.w3.org/TR/tabular-metadata/ (HTTP 200) |
| Data Contract Specification | — | datacontract/datacontract-specification eeb60a9, README |

## Data Contract Specification: deprecated
README: "With the release of the Open Data Contract Standard v3.1.0, we deprecate the Data Contract Specification … will be supported in
Data Contract CLI and Entropy Data until the end of 2026." → excluded as a candidate.

## Frictionless Data Package v2 (concerns 2, 9; partly 11)
- Data Resource `bytes` ("Size of the file in bytes"), `hash` (MD5 default; other algorithms by prefix `sha1:…`), `path` (one or many
  files), `format`, `mediatype`, `encoding`, `dialect`, `schema` (`data-resource.mdx`). These describe a *concrete* resource: values
  are known only once a delivery exists → fits an execution-time manifest (evidence) better than a static contract (inference).
- Table Dialect (`table-dialect.mdx`): `header`, `headerRows`, `headerJoin`, `commentRows` (positive integers counted from the
  start), `commentChar`, `delimiter`, `lineTerminator`, `quoteChar`, `doubleQuote`, `escapeChar`, `nullSequence`, `skipInitialSpace`,
  `property`, `itemType`, `itemKeys`, `sheetNumber`, `sheetName`, `table`. **No trailer/footer property**; rows can only be
  addressed from the top, so "last line is a trailer with a record count" is not expressible. Section "Excluded": dialect is
  orthogonal to character encoding.
- Table Schema `missingValues` (`table-schema.mdx` #missingValues): array of strings **or of `{value, label}` objects**, e.g.
  `{ "value": "", "label": "OMITTED" }, { "value": "-99", "label": "REFUSED" }`; field-level override `field.missingValues`;
  `[]` disables null conversion. → labelled missing-value tokens are native; "absent vs explicitly empty" can be expressed as two
  labelled tokens, but the label vocabulary is free text (our semantics).
- Extension mechanism (`extensions.mdx`): a profile is a JSON Schema referenced by `$schema` on any descriptor; "the extension
  system completely relies on the JSON Schema Standard" → **standardised mechanism for schema-validated custom extensions**.
- Data Package `version` (SHOULD be semver), `created` (semantics "may vary between publishers"). No valid-time.
- Governance: Data Package Working Group (vetoing + voting members), `overview/governance.md`.

## W3C CSVW (concern 9)
Dialect: `commentPrefix`, `delimiter`, `doubleQuote`, `encoding`, `header`, `headerRowCount`, `lineTerminators`, `quoteChar`,
`skipBlankRows`, `skipColumns`, `skipInitialSpace`, `skipRows`, `trim`. Column-level `null`. No footer/trailer property.
JSON-LD based; 2015 REC, no further versions (inference from the TR page; W3C CSVW WG closed — *secondary*, not re-read).

## Arazzo 1.1.0 (concerns 3, 5 for HTTP/async APIs only)
- Workflows of steps over `sourceDescriptions` of type `openapi`, `asyncapi` (new in 1.1.0) or `arazzo`.
- Failure Action Object `type: retry` with `retryAfter` (seconds; an HTTP `Retry-After` header "SHOULD overrule" it) and
  `retryLimit` ("If not specified then a single retry SHALL be attempted") → **native retry limit** for API steps.
- Steps carry operation, parameters, requestBody, successCriteria → "what we ask for" native for HTTP. No schedule/cron, no
  timing tolerance. Specification Extensions (`x-`) admitted on most objects (custom extension class).
- Schema: only `_archive_/schemas/v1.0/schema.json` in repo at HEAD; 1.1 JSON Schema location not confirmed (*unverified*).

## OpenSLO v1 (concern 10)
- Kinds: DataSource, SLO, SLI, AlertPolicy, AlertCondition, AlertNotificationTarget, Service. SLO = indicator/indicatorRef +
  `timeWindow` (rolling or calendar-aligned with IANA `timeZone`) + `budgetingMethod` (Occurrences|Timeslices|RatioTimeslices,
  required) + `objectives` + `alertPolicies`. SLI `metricSource.spec` is free-form ("anything that is valid YAML").
- Validation is defined by the Go SDK ("The reference uses the OpenSLO Go SDK's object descriptions and validation rules";
  CLI `oslo`). No JSON Schema file in the repo; no Python validator listed in `tools.md`.
- `metadata.annotations` = implementation-specific extension point (custom).
- Fit: indicator/objective/consequence (alert) are native, but it overlaps ODCS `quality[]` operators and targets metric
  back-ends; no failure-class taxonomy.

## OpenLineage 2-0-2 (concern 11; 3 partly)
- RunEvent with run, job, inputs/outputs; facets validated by per-facet JSON Schemas with `_producer` + `_schemaURL`.
- Relevant standard facets (`spec/facets/*.json`): InputStatisticsInputDatasetFacet {rowCount, size, fileCount} ("read");
  DatasetVersionDatasetFacet {datasetVersion}; NominalTimeRunFacet {nominalStartTime, nominalEndTime} (scheduled vs actual time);
  DataQualityAssertionsDatasetFacet; TestRunFacet {tests}; JobDependenciesRunFacet; ErrorMessageRunFacet; StorageDatasetFacet
  (fileFormat enum incl. csv). No facet for a data-contract reference in core or registry (`grep contract` → none).
- Custom facets (`OpenLineage.md`): project prefix, `_schemaURL` MUST be an immutable versioned URL to the facet's JSON Schema;
  "Custom facets can be promoted to the standard" → **schema-validated custom extension with a published mechanism**.
- No per-file digests in standard facets.

## CloudEvents 1.0 (concern 6, 7 for event-shaped deliveries)
`spec.md` §id: "Producers MUST ensure that `source` + `id` is unique for each distinct event. If a duplicate event is re-sent … it
MAY have the same id. Consumers MAY assume that Events with identical `source` and `id` are duplicates." §time: occurrence
timestamp, consistent per source. → native *producer-side* identity/duplicate semantics; says nothing about different payload
bytes under the same id (revision vs refusal) and nothing for files we poll.

## in-toto Attestation Framework v1 (concerns 2, 11)
- Statement = subject[ResourceDescriptor] + `predicateType` (URI) + predicate. ResourceDescriptor {name, uri, digest (DigestSet
  alg→hex), content, downloadLocation, mediaType, annotations}; MUST have one of uri/digest/content.
- Predicate types are published separately (`spec/predicates/`: provenance, link, test-result v0.1, vsa, scai, …); anyone may
  define a new predicate type by URI (template in `predicates/template`) → standardised extension mechanism.
- Fit: "what one run read" as subjects with digests, plus a predicate that references the contract versions (custom predicate).
  Heavier (signing envelope/DSSE) than needed if signatures are not wanted.

## Croissant 1.1 (concern 2, 9)
JSON-LD (schema.org). FileObject with `contentSize`, `sha256`; FileSet with glob `includes`/`excludes`; RecordSets.
ML-dataset oriented; overlaps ODCS schema modelling. Not proposed.

## Bitemporal (concern 1), calendars (4), HTTP metadata (6, 7): standards that define semantics, not contract fields
(Pointers for the report; not all re-read in full today.)
- RFC 9110 (HTTP Semantics): `ETag`, `Last-Modified`, `Retry-After` — header semantics only (*first-hand earlier knowledge; spec
  not re-fetched this run → label secondary*).
- RFC 9530 Digest Fields (`Content-Digest`, `Repr-Digest`) (*secondary in this track*).
- iCalendar RFC 5545 RRULE/EXDATE, JSCalendar RFC 8984 recurrenceRules (*secondary in this track*).
- DCMI `dct:valid`, PROV-O `prov:generatedAtTime`/`invalidatedAtTime` (*secondary in this track*).
