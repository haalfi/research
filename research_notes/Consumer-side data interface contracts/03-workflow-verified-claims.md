# Track 3: deep-research workflow output (fan-out search, fetch, 3-vote verification)

Run 2026-11-19. Five search angles, 23 sources fetched, 110 claims extracted, 25 verified, 23 confirmed, 2 refuted.
Recorded as returned. Review of the two refutations: see track 4.

## Summary

ODCS v3.2.0 (current, APPROVED; tag dated 2026-09-08) does not natively cover any of the 11 concerns the prototype put in customProperties. Its schema is strict, so every unknown field has to go into customProperties, whose value is unvalidated AnyType. v3.2.0 adds only an unenforced `vendor` label, a server `encoding` field and SLA-level customProperties/authoritativeDefinitions. Its SLA `scheduler`/`schedule` fields say when checks run, not when a provider delivers. Several concerns are native in other open standards with published schemas. Data Package v2 covers file dialect and headers (Table Dialect), missing-value tokens (Table Schema), and per-file size and hash (Data Resource). For HTTP interfaces, Arazzo 1.1.0 covers retry limits (`retryLimit`/`retryAfter`), OpenAPI 3.2 covers response-header metadata, and RFC 9530 covers HTTP digests. CSVW covers the dialect natively too, but it has no JSON Schema, so Data Package fits the "each document validated against its own published schema" requirement better. My inferred minimal set is ODCS v3.2.0 + Data Package v2 + OpenAPI 3.2 / Arazzo 1.1, with RFC 9530 referenced. The verified evidence leaves these custom or uncovered: bitemporal contract validity, a calendar-based offer cadence and deadline, request timing tolerance, delivery identity and revision rules, the meaning of publication-time metadata, redaction, trailers and record counts, the provider catalogue and its deviations, failure classes per quality rule, and execution evidence.

## Findings

### F1 (confidence high, vote 3-0 (version facts); 2-1 (strictness / customProperties consequence))

ODCS v3.2.0 is the current release (APPROVED; git tag dated 2026-09-08, no later tag by 2026-11-19). v3.1.0 is dated 2025-12-08. Both versions use a strict JSON Schema: additionalProperties/unevaluatedProperties is false at the root and on most objects. Any field outside the schema is an error, so extensions must go in customProperties, which only checks that `property` is a string and that `value` is AnyType (meaning is not validated). Two other places are schema-legal: quality rules of type `custom` (the `implementation` field takes any string or object) and authoritativeDefinitions entries (url + type), which can point to a separately validated external document.

*Evidence:* First-hand: the announcement says 'No undefined fields ... custom additions outside the schema will now be flagged as errors'. The v3.1.0 and v3.2.0 schemas were inspected: additionalProperties:false at the root; CustomProperty requires only property and value, and value is $ref AnyType. The CHANGELOG lists '# v3.2.0 Peter Flook - APPROVED' with no date and '# v3.1.0 - 2025-12-08 - APPROVED'. The README says 'Its current version is v3.2.0' (Apache 2.0). The GitHub releases page and API could not be reached; the version facts come from the CHANGELOG and README on raw.githubusercontent.com and from a git clone (tag date). The claim that extensions 'have to go into customProperties' is slightly overstated, because of the custom-quality and authoritativeDefinitions slots.

*Sources:* https://bitol.io/bitol-announces-odcs-v3-1-0-stronger-smarter-and-stricter/, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/CHANGELOG.md, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/README.md, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-v3.1.0.json, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-v3.2.0.json

### F2 (confidence high, vote 3-0)

No change since v3.1.0 natively covers a concern the prototype put in customProperties. v3.1.0 (RFC-0025) adds `scheduler` and `schedule` (free strings, e.g. cron) to SLA properties, matching the existing DataQuality fields. These say when checks run, not when the provider delivers or what timing tolerance applies. v3.2.0 adds enum, map, vector, semanticType, synonyms, context, deprecated, variables, relationship id, new server types, an optional `encoding` string on the S3, SFTP, Azure, Glue, Custom, Kafka, Kinesis and Local servers (a small part of concern 9), an optional unenforced `vendor` attribution on customProperties (RFC 0035, shared with ODPS v1.1.0 and OORS v1.0.0), and customProperties and authoritativeDefinitions on slaProperties[] (RFC 0046). Comparing the v3.1.0 and v3.2.0 schemas shows no new field for delimiter, header, trailer, record count, digest or size, delivery identity, retries, calendars, or validity and knowledge time.

*Evidence:* First-hand comparison of the v3.0.2, v3.1.0 and v3.2.0 schemas plus the CHANGELOG text. Quote: 'New optional `vendor` string on `customProperties` items ... SHOULD be a stable, lowercase identifier (`^[a-z0-9][a-z0-9-]*$`); not enforced, and tools MUST preserve unknown vendor values.' The vendor field has no `pattern` in the schema. ODCS has older SLA properties (`frequency`, `latency`, `timeOfAvailability`) that touch delivery timing, but they are loosely typed property/value pairs with no calendar or tolerance structure. The older server `delimiter` (new_line/array) on S3, SFTP and Azure describes record framing, not a CSV dialect. The RFC-0025 file itself returned 404, so the schema diff is the evidence. v3.2.0 also loosened DataQualityOperators from oneOf to anyOf.

*Sources:* https://bitol.io/bitol-announces-odcs-v3-1-0-stronger-smarter-and-stricter/, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/CHANGELOG.md, https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-v3.2.0.json, https://github.com/bitol-io/open-data-contract-standard/releases

### F3 (confidence high, vote 3-0)

File dialect (concern 9) is native and schema-validated in Frictionless Table Dialect v2: delimiter (default ','), lineTerminator (default CRLF), quoteChar, doubleQuote, escapeChar, header (boolean, default true), headerRows (array of positive integers, default [1]), headerJoin, commentRows/commentChar, skipInitialSpace and nullSequence, each with a MUST type constraint in the profile /profiles/2.0/tabledialect.json. W3C CSVW (Metadata Vocabulary for Tabular Data, REC 2015-12-17, §5.9) natively defines an overlapping set: delimiter, encoding, quoteChar, doubleQuote, lineTerminators, commentPrefix, header/headerRowCount, skipRows, skipColumns, skipBlankRows, skipInitialSpace and trim. The two differ: Table Dialect has headerJoin and nullSequence, which CSVW lacks; CSVW has skipBlankRows, skipColumns and trim, which Table Dialect lacks.

*Evidence:* First-hand: Table Dialect says 'delimiter ... `MUST` be a string; with default value `,`', 'header ... If `true` the first row in the file `MUST` be interpreted as a header row' and 'headerRows ... `MUST` be an array of positive integers starting from 1 with default value `[1]`'. CSVW: 'headerRowCount: A numeric atomic property ... MUST be a non-negative integer. The default is 1.' Caveats: the JSON profile does not enforce quoteChar/escapeChar length or their mutual exclusivity, and implementations need not support every property. CSVW dialect properties are 'hints', and the CSVW parsing procedure (Tabular Data Model §8) is non-normative. The comparison comes from the Data Package maintainers' guide (first-hand for the mapping, but not neutral) and was cross-checked against both specs.

*Sources:* https://datapackage.org/standard/table-dialect, https://datapackage.org/profiles/2.0/tabledialect.json, https://raw.githubusercontent.com/frictionlessdata/datapackage/main/content/docs/standard/table-dialect.mdx, https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/, https://www.w3.org/ns/csvw, https://datapackage.org/guides/csvw-data-package/

### F4 (confidence high, vote 3-0)

No candidate standard examined natively models a trailer or footer row, or a record count stated in a trailer (concern 9). Table Dialect v2 and CSVW define no such property. Their skip mechanisms (commentChar/commentRows, commentPrefix/skipRows) can only drop a row; they cannot declare what the row is or check a count. CSVW also states that dialect descriptions cannot handle several tables in one file. This part of concern 9 therefore stays custom.

*Evidence:* First-hand text search: 'trailer', 'footer', 'rowcount' and 'record count' have 0 hits in table-dialect.mdx, in the tabledialect.json profile, and across the CSVW metadata, data-model and namespace documents (apart from 'header row count'). CSVW §5.9: 'Dialect descriptions do not provide a mechanism for handling CSV files in which there are multiple tables within a single file.' The absence is an inference from the property lists; neither spec prohibits it. ODCS v3.2.0 also adds no trailer field (see the ODCS finding).

*Sources:* https://datapackage.org/standard/table-dialect, https://www.w3.org/TR/tabular-metadata/, https://www.w3.org/TR/tabular-data-model/, https://www.w3.org/ns/csvw, https://datapackage.org/guides/csvw-data-package/

### F5 (confidence high, vote 3-0 (one sub-claim on empty-list behaviour 2-1))

'Absent' versus 'explicitly empty' tokens (concern 9) are only partly covered, by configuration and not by semantics. Table Dialect has a single `nullSequence` string (undefined by default). Table Schema v2 `missingValues` (at schema level, or at field level, where it fully replaces the schema-level list) takes strings or {value, label} objects. Labels are free human-readable text (OMITTED/REFUSED appear only in an example). The default [""] turns empty strings into null, and [] turns off conversion. CSVW column `null` (a string or array) plus `default` (used only when a cell is empty) can tell a declared null token apart from an empty cell, if `null` is overridden. None of these standards defines what 'present but empty' versus 'absent' means. A contract can express the distinction by choosing which tokens to list, but what each token means stays custom.

*Evidence:* First-hand. Table Schema: 'missingValues MUST be an array where each entry is a unique string, or an array where each entry is an object ... optional label property MUST be a string that provides a human-readable label'; 'The default value [""] means that empty strings will be converted to null ... Providing the empty list [] means that no conversion to null will be done'; field-level 'completely replaces it for the field without combining the values'. Implementations MAY convert to null, load inline, or use a separate column. CSVW: 'null: ... If not specified, the default for the null property is the empty string'; `default` applies 'in cases where the original string value is an empty string'. The CSVW `null` property accepts several tokens; labels are what it lacks. Using these as a fit for concern 9 is inference. Field-level and labelled missingValues are new in v2.

*Sources:* https://datapackage.org/standard/table-dialect, https://datapackage.org/standard/table-schema, https://raw.githubusercontent.com/frictionlessdata/datapackage/main/content/docs/standard/table-schema.mdx, https://www.w3.org/TR/tabular-metadata/, https://www.w3.org/TR/tabular-data-model/, https://datapackage.org/guides/csvw-data-package/

### F6 (confidence high, vote 3-0)

The per-file size and digest parts of concern 2 are native in Data Package v2 Data Resource: `bytes` (integer) and `hash` (MD5 by default, otherwise an 'algorithm:hex' prefix, checked by a schema regex). For HTTP interfaces, RFC 9530 (IETF Standards Track, Proposed Standard, February 2024; obsoletes RFC 3230 Digest/Want-Digest; not updated or obsoleted) defines Content-Digest (message content after content-coding) and Repr-Digest (the whole selected representation; still valid for range or 206 responses). Both depend on Content-Encoding and Content-Type, so a contract must say which one it relies on (inference). Neither standard models a provider's file catalogue or the provider's deviations from it, so those stay custom.

*Evidence:* First-hand. Data Resource: 'bytes: Size of the file in bytes. hash: The MD5 hash for this resource. Other algorithms can be indicated by prefixing the hash's value with the algorithm name in lower-case.' The schema pattern is ^([^:]+:[a-fA-F0-9]+|[a-fA-F0-9]{32}|)$ and does not enforce a lower-case prefix or an algorithm list. With a multi-file `path` array, bytes and hash apply to the concatenation, so per-file values hold only for single-file resources. RFC 9530 §1-3 and Appendix B.3 were read in full. RFC 9530 is a wire protocol, not a contract-document schema, so recording an expected digest in YAML is a referenced or custom use of it (inference).

*Sources:* https://datapackage.org/standard/data-resource, https://datapackage.org/profiles/2.0/dataresource.json, https://www.rfc-editor.org/rfc/rfc9530.html, https://www.rfc-editor.org/rfc/rfc9530.txt, https://www.rfc-editor.org/rfc/rfc9530.json

### F7 (confidence high, vote 3-0 (retry); 2-1 (absence of schedules, verified against the full text))

For HTTP request/response interfaces, Arazzo natively models retry limits (concern 5). A Failure Action of type `retry` has `retryLimit` (non-negative integer; if unspecified, one retry SHALL be attempted) and `retryAfter` (seconds; an HTTP Retry-After header SHOULD override it), validated by the published JSON Schema. The limit applies per step and per failure action and can be scoped by criteria (e.g. $statusCode == 503). It covers only operations described in OpenAPI (and, in 1.1.0, AsyncAPI), not SFTP, object storage, SQL or change-log interfaces. Arazzo, including the current 1.1.0 (2026-05-17), defines no schedules, cron, calendars or start triggers. Its only timing fields are retryAfter, dependsOn ordering, and 1.1.0's Step `timeout`, so concerns 3 (timing and tolerance) and 4 are not native. Arazzo does model the request content part of concern 3 (parameters, request bodies, operationId).

*Evidence:* First-hand: 'retryLimit | integer | A non-negative integer indicating how many attempts to retry the step MAY be attempted before failing the overall step. If not specified then a single retry SHALL be attempted.' The text is the same in 1.0.0, 1.0.1 and 1.1.0. Schema $defs/failure-action-object: retryLimit {type: integer, minimum: 0}, unevaluatedProperties:false. Full-text search of 1.0.1 and 1.1.0: 0 hits for schedul, cron or calendar. The absence sub-claim started from a tool summary (vote 2-1), and the verifier then confirmed it against the full text.

*Sources:* https://spec.openapis.org/arazzo/v1.0.html, https://raw.githubusercontent.com/OAI/Arazzo-Specification/main/versions/1.0.1.md, https://raw.githubusercontent.com/OAI/Arazzo-Specification/main/versions/1.1.0.md, https://spec.openapis.org/arazzo/1.1/schema/2026-04-15, https://spec.openapis.org/arazzo/latest.html

### F8 (confidence medium, vote 3-0 (headers); 2-1 (extensions))

OpenAPI 3.2 (3.2.0 released 2025-09-19; 3.2.1 patch 2026-09-10 is current) natively declares response metadata a consumer relies on through the Response Object `headers` map and the Header Object (required, schema). An example is requiring a strong ETag. OAS gives no meaning to a header, such as 'publication time' or 'revision order'; that meaning comes from the HTTP RFCs (e.g. RFC 9110 ETag/Last-Modified), so the semantic mapping for concern 7 stays custom. Anything OAS does not model (retry limits, schedules, delivery identity, redaction) can be added only as `x-` Specification Extensions: arbitrary JSON, optional per tool, with x-oai-/x-oas- reserved. The OAI extension registry has no entry for retries, scheduling or delivery identity.

*Evidence:* First-hand: §4.17.1 'headers: Maps a header name to its definition'; §4.21.4 strong-ETag example 'ETag: required: true schema: type: string pattern: ^"'. Specification Extensions: 'The value can be any valid JSON value ... Support for any one extension is OPTIONAL'. The headers mechanism had a 3-0 vote. The 'only via extensions' claim had a 2-1 vote, and its 'can only' wording is the claimant's inference. OAS is normally written by the provider; a consumer-side OAS document is a usage choice (inference).

*Sources:* https://spec.openapis.org/oas/v3.2, https://spec.openapis.org/oas/v3.2.0.html, https://spec.openapis.org/oas/latest.html, https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/versions/3.2.0.md, https://spec.openapis.org/registry/extension/

### F9 (confidence high, vote 3-0)

For the requirement that each document be validated against its own published schema, Data Package v2 qualifies better than CSVW. Data Package (v2.0, 2024) is defined as JSON Schema profiles and is extended by referencing a JSON Schema. CSVW (2015 REC) is defined in JSON-LD with XML Schema datatypes and CURIEs, has no official JSON Schema, and is validated by conformance tools tested against the W3C test suites (e.g. Python `csvw`/csvwvalidate, csvlint).

*Evidence:* From the maintainers' guide, read first-hand: 'Data Package is defined as a JSON Schema and is designed to be extensible ... CSVW is not defined as a JSON Schema.' The verifier found no official W3C JSON Schema for CSVW. The source is the Data Package maintainers, who are not neutral, but the fact can be checked. That this affects the requirement is inference.

*Sources:* https://datapackage.org/guides/csvw-data-package/, https://929-contribution-guide.datapackage-6gp.pages.dev/guides/csvw-data-package, https://www.w3.org/TR/tabular-metadata/

### F10 (confidence low, vote n/a (synthesis))

Recommended minimal set (inference, built from the verified findings). ODCS v3.2.0 holds dataset shape and quality, as the baseline. Data Package v2 (Data Resource + Table Dialect + Table Schema) holds file delivery shape, dialect, missing-value tokens, and per-file bytes and hash; ODCS can reference it via authoritativeDefinitions. OpenAPI 3.2 + Arazzo 1.1 hold HTTP request shape, relied-on response headers, and retry limits. RFC 9530 is referenced by name for HTTP digest expectations. CSVW is left out because it overlaps Table Dialect and has no JSON Schema. Under this set the following stays custom, in a separately schema'd consumer extension document or in vendor-tagged customProperties: bitemporal contract validity and knowledge time (1); the provider catalogue and deviations (2); request timing tolerance (3); calendar-based offer cadence and deadline (4); retries for non-HTTP interfaces (5); delivery identity, sighting and revision rules (6); the meaning of publication-time and revision-order metadata (7); redaction (8); trailer/record count and 'stated whole' population (9); SLO and failure class per quality rule (10). Execution evidence (11) belongs in a separate run record, not in the contract.

*Evidence:* This is a synthesis. No single verified claim states it. Concerns 1, 4, 6, 8, 10 and 11 were not tested against the candidate standards that might cover them (iCalendar/JSCalendar, OpenSLO, DQV, PROV-O, OpenLineage, CloudEvents, in-toto/SLSA), so their 'custom' status is unverified, not shown to be absent. The ODPS composition and the cross-document id/version references were not verified.

*Sources:* https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-v3.2.0.json, https://datapackage.org/standard/data-resource, https://spec.openapis.org/arazzo/latest.html, https://spec.openapis.org/oas/latest.html, https://www.rfc-editor.org/rfc/rfc9530.html

## Refuted

- (0-3) A Tabular Data Resource MAY carry a `dialect` property (file dialect) and SHOULD carry a `schema` property (Table Schema). Dialect is therefore native for the file-dialect part of concern 9, through Table Dialect. — https://datapackage.org/standard/data-resource
- (1-2) OpenLineage accepts arbitrary custom facets on run, job and dataset objects. The only condition is that a facet follows BaseFacet and carries the two mandatory fields _producer and _schemaURL. For the requester's concern 11 (execution evidence), this makes a custom run facet a 'custom extension' class mechanism, not native semantics. — https://openlineage.io/docs/spec/facets/custom-facets

## Caveats

Coverage is uneven. The 23 surviving claims cover ODCS, Frictionless Data Package v2, CSVW, Arazzo, OpenAPI 3.2 and RFC 9530. They do not cover iCalendar/JSCalendar (concern 4 calendars), OpenSLO or DQV (concern 10), PROV-O, OpenLineage or CloudEvents (concern 11), in-toto/SLSA/SPDX, DCAT 3, Croissant, AsyncAPI 3, the Data Contract Specification, or ODPS. Where a concern has no verified standard, that means no verified evidence, not that the concern is absent. Two claims were refuted and are left out: (a) that a Tabular Data Resource carries a native `dialect`/`schema` link (0-3), so how Data Resource, Table Dialect and Table Schema link in v2 needs rechecking before composition; (b) that OpenLineage custom facets give custom-extension coverage for execution evidence (1-2), so concern 11 is still open. Split votes (2-1) apply to ODCS strictness forcing customProperties (overstated: custom quality rules and authoritativeDefinitions are other slots), the Table Schema empty-list sub-claim, Arazzo's lack of schedules (verified later against the full text), and OAS 'extensions only'. The GitHub releases page and API were unreachable. ODCS version data comes from the CHANGELOG, the README and a git clone; v3.2.0 has no changelog date (tag 2026-09-08). Some sources are preview deploys (datapackage pages.dev) or maintainer guides comparing a competing standard; they were cross-checked against the specs. Time sensitivity: Arazzo 1.1.0 (2026-05) and OAS 3.2.1 (2026-09) are recent, and ODCS schema snapshots go up to 20261117, so later ODCS patches may exist. The recommended set and the custom list are inference. Question 5 (published consumer-side contract examples) went unanswered. Per-standard governance, release cadence, adoption and Python validator details are mostly missing, apart from CSVW tooling.

## Open questions

- Do iCalendar (RFC 5545) or JSCalendar (RFC 8984) recurrence rules, with a business or market holiday calendar, give native, schema-validated coverage of offer cadence and deadlines (concern 4) in a form a YAML contract can reference, and is there a JSON Schema for JSCalendar?
- Which standard should hold execution evidence (concern 11), given that the OpenLineage custom-facet claim was refuted: OpenLineage run/dataset facets, W3C PROV-O, or in-toto/SLSA attestations? Can it reference ODCS contract ids and versions?
- Can OpenSLO or W3C DQV express a per-quality-rule SLI/SLO/consequence and a failure class finer than severity (concern 10) and be linked from ODCS quality rules, or does that stay custom?
- Are there published consumer-side contracts for third-party feeds that combine ODCS with Data Package, OpenAPI or Arazzo, and how does v2 actually link a Data Resource to its dialect and schema, given that the native-link claim was refuted?

## Sources

- [secondary] https://barc.com/odcs-3-2-data-contract-standard/ (ODCS baseline and recent changes)
- [blog] https://jgp.ai/2026/06/02/odcs-v3-2-and-odps-v1-1-making-ai-smart-about-your-data/ (ODCS baseline and recent changes)
- [primary] https://bitol.io/bitol-announces-odcs-v3-1-0-stronger-smarter-and-stricter/ (ODCS baseline and recent changes)
- [blog] https://dataintelligenceplatform.substack.com/p/odcs-v310-is-here-relationships-richer (ODCS baseline and recent changes)
- [primary] https://github.com/bitol-io/open-data-contract-standard/releases (ODCS baseline and recent changes)
- [blog] https://dataintelligenceplatform.substack.com/p/bitol-is-a-graduated-project (ODCS baseline and recent changes)
- [primary] https://datapackage.org/standard/table-dialect (File delivery shape and integrity)
- [primary] https://datapackage.org/standard/data-resource (File delivery shape and integrity)
- [primary] https://datapackage.org/standard/table-schema (File delivery shape and integrity)
- [primary] https://www.w3.org/ns/csvw (File delivery shape and integrity)
- [primary] https://929-contribution-guide.datapackage-6gp.pages.dev/guides/csvw-data-package (File delivery shape and integrity)
- [unreliable] https://lightrun.com/answers/frictionlessdata-specs-hash-should-be-an-object (File delivery shape and integrity)
- [primary] https://spec.openapis.org/arazzo/v1.0.html (HTTP interface, schedules and metadata)
- [blog] https://redocly.com/blog/arazzo-specification-1-1-release (HTTP interface, schedules and metadata)
- [primary] https://www.rfc-editor.org/rfc/rfc9530.html (HTTP interface, schedules and metadata)
- [primary] https://spec.openapis.org/oas/v3.2 (HTTP interface, schedules and metadata)
- [primary] https://openlineage.io/docs/spec/facets/custom-facets (SLOs, provenance and run evidence)
- [primary] https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions (SLOs, provenance and run evidence)
- [primary] https://github.com/OpenSLO/OpenSLO (SLOs, provenance and run evidence)
- [primary] https://www.w3.org/TR/vocab-dqv/ (SLOs, provenance and run evidence)
- [blog] https://datakitchen.io/blog/the-data-contract-is-your-receipt/ (Practitioner composition examples)
- [primary] https://bitol-io.github.io/open-data-product-standard/latest (Practitioner composition examples)
- [primary] https://pypi.org/project/airflow-provider-datacontract/ (Practitioner composition examples)
