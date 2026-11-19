# Track 4: verification of workflow output and gap-fill, first-hand

Access date: 2026-11-19. RFCs fetched as text from rfc-editor.org (HTTP 200); W3C/DCMI pages fetched as HTML (HTTP 200).

## Review of the workflow's two refutations
1. **Refuted 0-3: "A Tabular Data Resource MAY carry `dialect` and SHOULD carry `schema`."** The repository text at
   frictionlessdata/datapackage da3526c (`content/docs/standard/data-resource.mdx`, section "Tabular") says verbatim:
   "A Tabular Data Resource `MAY` have a `dialect` property … `MUST` be a Table Dialect descriptor in a form of an object or
   URL-or-Path" and "A Tabular Data Resource `SHOULD` have a `schema` property … object or URL-or-Path". **I overrule the
   refutation** (first-hand). The URL-or-Path form also gives a cross-document reference from a resource to separate
   dialect/schema files.
2. **Refuted 1-2: "OpenLineage custom facets give custom-extension coverage for concern 11."** `spec/OpenLineage.md`
   (OpenLineage 3e93c95) says custom facets "must use a distinct prefix", carry `_schemaURL` that "must be an immutable pointer
   to the version of the facet schema", and "can be promoted to the standard". The mechanism exists as described (first-hand).
   The refutation probably targeted the wording "the only condition"; the class assignment (custom extension with a
   schema URL per facet) stands. Treated as **confirmed with that wording narrowed**.

## RFC 5545 iCalendar / RFC 8984 JSCalendar (concern 4)
- RFC 5545 §3.3.10 RECUR: FREQ required; UNTIL/COUNT; BYxxx parts incl. BYSETPOS, WKST; §3.8.5.1 EXDATE, §3.8.5.2 RDATE,
  §3.8.5.3 RRULE. Expected delivery dates can be generated from a rule minus explicit exception dates.
- RFC 8984 §4.3.3 `recurrenceRules`, §4.3.4 `excludedRecurrenceRules`: "A RecurrenceRule object is a JSON object mapping of a
  RECUR value type in iCalendar [RFC5545] [RFC7529] and has the same semantics." `skip` handles invalid dates in calendar systems
  (`rscale`), not business days.
- Neither defines a business-day adjustment ("next business day if a holiday") or a reference to a named holiday/market calendar;
  holidays are only expressible as an enumerated exclusion list or exclusion rule (first-hand, by reading the rule parts; absence
  is inference). No JSON Schema is published with RFC 8984 (searched the text for "JSON Schema": not present; inference that none
  exists elsewhere is unverified).
- Python: `icalendar` 7.3.0 (PyPI, 2026-08-19) parses RFC 5545 (secondary, PyPI metadata).

## RFC 9110 HTTP Semantics (concerns 5, 6, 7)
- §8.8.2 Last-Modified: "the date and time at which the origin server believes the selected representation was last modified" →
  a modification time, not a publication time.
- §8.8.3 ETag: "an opaque validator for differentiating between multiple representations of the same resource" → detects that bytes
  changed; defines **no order** between tags. Revision order therefore cannot come from ETag.
- §10.2.3 Retry-After: server hint for delay; Arazzo `retryAfter` defers to it.

## RFC 9530 Digest Fields (concern 2)
Fetched (HTTP 200); content as in workflow F5 (Content-Digest, Repr-Digest; Proposed Standard, Feb 2024; obsoletes RFC 3230).

## W3C / DCMI vocabularies (concerns 1, 2, 4, 10, 11)
- DCMI Terms `dct:valid`: "Date (often a range) of validity of a resource"; `dct:issued`: "Date of formal issuance of the resource".
  → the vocabulary for a contract version's valid period and issue (knowledge) time exists; it is RDF, not a YAML/JSON-Schema field.
- PROV-O (W3C Recommendation 30 April 2013): `prov:generatedAtTime`, `prov:invalidatedAtTime`, `prov:wasRevisionOf` listed in the
  starting-point terms → execution evidence and revision chains, RDF.
- DCAT 3 (W3C Recommendation 22 August 2024): `dcat:DatasetSeries` (new in DCAT 3), versioning (`dcat:version`,
  `dcat:previousVersion`, `dcat:hasCurrentVersion`), `dcat:byteSize`, checksum (`spdx:checksum`), frequency
  (`dcterms:accrualPeriodicity`) → frequency of a series, sizes and checksums of distributions, version chains. RDF; validation via
  SHACL (e.g. DCAT-AP shapes, *secondary*), no JSON Schema.
- DQV (W3C Working Group Note 15 December 2016, not a Recommendation): `dqv:Metric`, `dqv:QualityMeasurement`,
  `dqv:QualityPolicy` → indicator and measurement; no objective/consequence structure, no failure class.

## Question 5: published consumer-side examples
Two web searches (2026-11-19) plus the workflow's "practitioner composition" angle found **no published consumer-side contract
for a third-party feed that combines ODCS with another standard**. Leads only (secondary): lakeFS "Data Contracts" page advises
contracting "the first internal dataset downstream" of vendor feeds (https://lakefs.io/data-contracts/); ODCS docs show an SFTP
server example; ODCS `docs/examples/` holds no consumer-side or SFTP feed example (grep, first-hand). Absence of evidence, not
proof of absence.

## Python tooling (PyPI JSON API, 2026-11-19; *secondary*: metadata only, not tested)
| Package | Version | Upload | Use |
|---|---|---|---|
| open-data-contract-standard | 3.2.0 | 2026-09-02 | Pydantic model of ODCS (listed in ODCS `vendors.md`) |
| datacontract-cli | 1.2.11 | 2026-11-17 | ODCS lint/test (listed in ODCS `vendors.md`) |
| frictionless | 5.21.0 | 2026-10-15 | Data Package validate (v2 support not checked here) |
| openlineage-python | 1.55.0 | 2026-10-29 | OpenLineage client |
| cloudevents | 2.2.0 | 2026-06-11 | CloudEvents SDK |
| in-toto-attestation | 0.9.3 | 2023-12-13 | in-toto bindings (stale) |
| icalendar | 7.3.0 | 2026-08-19 | RFC 5545 |
| csvw | 4.2.0 | 2026-11-06 | CSVW |
| jsonschema | 4.26.0 | 2026-01-07 | generic validator for ODCS/ODPS/OORS/Data Package/Arazzo/OpenLineage JSON Schemas |
OpenSLO: validation defined by the Go SDK / `oslo` CLI; no Python validator listed (first-hand, `website/docs/tools.md`).

## Addendum (same run)
- CloudEvents documented extensions (cloudevents/spec main, 1.0.3-wip; latest release v1.0.2 per README), first-hand:
  `extensions/sequence.md` ("a string that can be lexicographically compared … lower … comes first"; meaning left to
  out-of-band agreement), `extensions/recordedtime.md` (time the occurrence was recorded, distinct from `time` → event-level
  bitemporality), `extensions/data-classification.md` (classifies payloads for GDPR/HIPAA-style handling; classification, not redaction).
- ODCS v3.2.0 `SchemaBaseProperty.classification` (free string, e.g. confidential/restricted/public) and `criticalDataElement`:
  native labels; no redaction action. `SchemaObject` keys: logicalType, physicalName, dataGranularityDescription, properties,
  relationships, quality, context.
- ODCS `authoritativeDefinitions[]` = {id, url, type, description}, `type` open ("Custom `type` values are allowed; tooling that
  does not recognise a custom value should treat the entry as an opaque link", `docs/authoritative-definitions.md`).
- ODCS SFTP/S3 `location` examples use a `{model}` placeholder (`sftp://123.123.12.123/{model}/*.json`); the placeholder's meaning
  is not defined in the field description (first-hand), so a file→dataset mapping by placeholder is example-level only (inference).
