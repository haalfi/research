# Consumer-side data interface contracts: which open formats, together

Brief: `briefs/Consumer-side data interface contracts.md`. Notes: `research_notes/Consumer-side data interface contracts/` (tracks 01–04).
Cutoff and access date: 2026-11-19.

Labels: **[F]** first-hand (spec text or published schema read), **[S]** secondary, **[I]** inference.

---

## 1. Answer in brief

1. **ODCS v3.2.0 is current and natively covers none of the 11 concerns** [F]. It was approved on 2026-09-08 and is the newest tag.
   - v3.1.0 added `schedule`/`scheduler` to SLA entries. These say when *checks* run, not when the provider delivers.
   - v3.2.0 added three things that come close:
     - a server `encoding` field, which covers a sliver of concern 9;
     - `customProperties` on SLA entries;
     - an unenforced `vendor` tag on `customProperties`.
   - ODCS does have native *labels* that cover parts of concerns 4, 8, 9 and 10: SLA `frequency`/`timeOfAvailability`, property `classification`, the `missingValues` metric, and the quality-rule operators. They have no structure for calendars, redaction actions, trailers or failure classes.
2. **Recommended minimal set** [I, built on F]:
   - **ODCS v3.2.0** as the contract hub.
   - **Frictionless Table Dialect and Table Schema v2** for file interfaces, as separate referenced documents.
   - **OpenAPI 3.2 (+ Arazzo 1.1)** for HTTP interfaces.
   - **OORS v0.8** for run results, plus a **Frictionless Data Package v2 manifest** for what each run read.

   That set gives native, schema-validated coverage of the file dialect, missing-value tokens, HTTP request shape, relied-on response headers, HTTP retry limits, per-file sizes and digests (as evidence) and check results.
3. **Still custom** [F/I]:
   - bitemporal validity (1);
   - request timing tolerance (3);
   - calendar-based deadlines (4);
   - non-HTTP retries (5);
   - delivery identity and revision policy (6);
   - the *meaning* of publication-time and revision-order metadata (7);
   - redaction actions (8);
   - trailer record count and "stated whole" population (9);
   - failure class (10).

   Most of these can reuse standardised *values*:
   - RFC 5545 RRULE strings for cadence;
   - RFC 9110 header names for publication-time and change signals;
   - CloudEvents `sequence` semantics for revision order;
   - DCMI `dct:valid` for the valid period.

   Put them in one org-owned JSON Schema that validates vendor-tagged ODCS `customProperties`.
4. **Coherent document set** [I]: yes. Each document validates against its own published JSON Schema. ODCS `id`/`version`, Data Resource `dialect`/`schema` URL-or-Path, ODPS `contractId`+`version` and the OORS `contract{contractId, version, server}` block give explicit references. The unavoidable glue is:
   - linking ODCS to non-Bitol documents, which only works through `authoritativeDefinitions` (an open `type` plus a URL);
   - keeping Table Schema fields consistent with ODCS properties;
   - the org overlay schema for `customProperties`.
5. **Published examples combining standards this way: none found** [S]. This rests on two web searches, the workflow's practitioner angle and the ODCS `docs/examples` tree. It is absence of evidence, not proof of absence.

---

## 2. What changed in ODCS since v3.1.0 (Q2)

Source: `CHANGELOG.md`, the v3.2.0 section, and `schema/odcs-json-schema-v3.2.0.json` at HEAD 7c7597e (2026-11-17) [F].

| v3.2.0 change | Touches concern | Native coverage? |
|---|---|---|
| Server `encoding` (RFC 0043) on SFTP, S3, Azure, Glue, Custom, Kafka, Kinesis and Local servers | 9 (dialect) | Character encoding only. The `delimiter` field remains "Only for format = json". No CSV dialect. |
| `slaProperties[].customProperties` and `authoritativeDefinitions` (RFC 0046) | 4, 10 | No. Only gives a place to attach custom fields. |
| `customProperties[].vendor` (RFC 0035) | all custom | No. A namespace label, "not enforced". |
| Variables `${VAR}` (RFC 0050), enum, map, vector, semanticType, synonyms, context, deprecated, relationship `id`, new server types | — | No. |

Open, *unapproved* Bitol RFCs show the gaps are recognised (`tsc/rfcs/README.md`, "Open RFCs") [F]:
- RFC 0052 `logicalType: blob` would add file properties: size, `contentMD5`, `etag`, `lastModified`.
- RFC 0040 OOCS would add orchestration directives.
- RFC 0062 would add signatures; it targets ODCS v3.3.0.
- RFC 0032 would add imports.

None of them can be used yet.

The Data Contract Specification is deprecated in favour of ODCS. Its tooling support ends at the close of 2026 [F, README].

---

## 3. Coverage matrix (Q1)

Classes: **N** native · **SE** standardised extension · **C** custom extension (the standard admits arbitrary fields) · **—** none (examined; the reasons are in §4) · blank: not applicable to this standard. "(p)" means partial.

| # | Concern | ODCS 3.2.0 | Frictionless DP v2 | OpenAPI 3.2 | Arazzo 1.1 | OORS 0.8 | OpenLineage 2-0-2 | CloudEvents 1.0 | Value-level semantics available |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bitemporal contract versions | C ([customProperties][odcs-cp]); `version`, `contractCreatedTs` N(p) | C ([profile][dp-ext]); `version`, `created` N(p) | C (`x-`) | C (`x-`) | | | | DCMI [`dct:valid`][dct-valid], `dct:issued` (RDF) |
| 2 | Sizes, digests, catalogue, deviations | Catalogue *as a dataset*: N(p) ([schema][odcs-schema] + [quality][odcs-dq]); digests C | `bytes`, `hash` N ([data-resource][dp-res]); catalogue — | Header Object for `Repr-Digest` N(p) ([headers][oas-hdr]) | | Deviation *results* N(p) ([results][oors-res]) | `InputStatistics` size N(p) ([facet][ol-in]) | | [RFC 9530][rfc9530]; in-toto [DigestSet][intoto-rd]; DCAT `dcat:byteSize` |
| 3 | Requests, schedules, timing tolerance | `schedule` is for checks only; C | | Request shape N ([operation][oas]) | Steps, params N; schedule — ([spec][arazzo]) | | `NominalTimeRunFacet` N(p), evidence side ([facet][ol-nt]) | | RFC 5545 RRULE |
| 4 | Offer cadence, deadline, calendar | SLA `frequency`, `timeOfAvailability` N(p) ([SLA][odcs-sla]); calendar — | | | | | | | [RFC 5545 §3.3.10][rfc5545] / [RFC 8984 §4.3.3][rfc8984]; DCAT [Dataset Series][dcat-ds] |
| 5 | Retry limits | C | | C (`x-`) | `retryLimit`, `retryAfter` N, HTTP and AsyncAPI only ([failure action][arazzo-fa]) | | | | [RFC 9110 Retry-After][rfc9110-ra] |
| 6 | Delivery identity, sighting, revision vs refusal | C | | C | | | | `source`+`id` duplicate rule N(p), events only ([id][ce-id]) | [RFC 9110 ETag][rfc9110-etag] (change, not order) |
| 7 | Publication time and revision order metadata | Metadata as dataset N(p); role C | | Header declared N, meaning C ([headers][oas-hdr]) | | | | `time` N; [`sequence`][ce-seq], [`recordedtime`][ce-rt] SE | [RFC 9110 Last-Modified][rfc9110-lm] (modification time) |
| 8 | Redaction of received metadata | `classification` label N(p) ([schema][odcs-schema]); action C | | C | | | | [`data-classification`][ce-dc] SE (labels, not redaction) | — |
| 9 | Delivery shape: files, dialect, trailer, population, absent vs empty | Multiple schema objects N; `encoding` N; `missingValues` metric N(p) ([DQ][odcs-dq]); trailer and population — | Dialect N ([table-dialect][dp-td]); `missingValues` {value,label} N(p) ([table-schema][dp-ts]); trailer — | | | | | | CSVW §5.9 dialect, also no trailer ([tabular-metadata][csvw]) |
| 10 | SLO per rule; failure class | Indicator and objective N ([DQ][odcs-dq]); `businessImpact`, `severity` free text; failure class C | | | | `status` pass/fail/warn/error/skip/unknown N(p) ([results][oors-res]) | | | OpenSLO SLO/SLI N ([spec][openslo]); DQV metric (RDF) |
| 11 | Execution evidence | (out of the contract by design) | Per-delivery manifest N(p) ([data-resource][dp-res]) | | | Check results with `contract{contractId, version, server}`, `source.runId` N ([fundamentals][oors-fund]) | RunEvent inputs and stats N; contract reference C ([custom facets][ol-cf]) | | in-toto Statement plus [test-result][intoto-tr] SE; PROV-O |

Each cell's basis is [F] (tracks 01, 02 and 04), except OpenAPI 3.2. That column rests on the workflow's first-hand reads (track 03, F7), which I did not re-read [S for me].

---

## 4. Per concern: classification, placement and "none" reasoning (Q1, Q3)

Placement: **K** static contract · **R** separate referenced specification · **E** execution-time evidence.

1. **Bitemporal versions**
   - **Placement:** valid period in K; knowledge time in E/git.
   - **Native coverage:** ODCS has `version` (string) and `contractCreatedTs` ("when the data contract was created") [F]. There is no valid-from/valid-to and no recorded-time field [F]. Frictionless `created` has publisher-dependent semantics [F].
   - **Standardised semantics:** DCMI defines `dct:valid` ("Date (often a range) of validity") and `dct:issued` [F]. They are RDF terms, so in YAML they are custom fields borrowing that meaning [I].
   - **Recommendation:** knowledge time is the git merge time of the contract version. Record it in evidence; don't author it [I].
2. **Integrity**
   - **Placement:** expectations in K; observed values and deviations in E.
   - **Expectations:** the provider's catalogue file is a dataset, so model it as an ODCS schema object and write cross-checks as ODCS quality rules (`sql`/`custom`) [I, on F field set]. Which digest algorithm and header to rely on stays custom; the header *declaration* can be native in OpenAPI.
   - **Observed:** sizes and digests per received file fit a Data Resource `bytes`/`hash` [F] in the run's manifest.
   - **None:** I found no standard for a *provider's deviation policy*, i.e. which mismatches are tolerated. I examined Data Resource, CSVW, ODCS servers and quality, RFC 9530 and in-toto ResourceDescriptor. All of them describe values, none tolerances [F/I].
3. **Requests and schedules**
   - **Placement:** request shape in R (OpenAPI/Arazzo); schedule and tolerance in K (custom).
   - **None:** I found nothing for "when we ask and the tolerance". Arazzo has no schedule, cron or calendar; its only timing fields are `retryAfter`, `dependsOn` and 1.1's step `timeout` [F, track 03 F6]. ODCS `schedule` is for checks [F]. OOCS is an open RFC [F].
   - **Scope:** OpenLineage `nominalTime` records the scheduled time on the evidence side only [F].
4. **Offer cadence and deadline**
   - **Placement:** K, with the calendar as R (an iCalendar file or URL).
   - **Native coverage:**
     - ODCS SLA `frequency` and `timeOfAvailability` give a period and a single time of day [F].
     - RFC 5545 RRULE/EXDATE and RFC 8984 `recurrenceRules`/`excludedRecurrenceRules` generate expected dates [F].
   - **None:** I found no standard that defines business-day adjustment or a reference to a named holiday or market calendar.
     - I examined RFC 5545 §3.3.10 and §3.8.5, RFC 8984 §4.3 and DCAT 3 Dataset Series.
     - Holidays are only expressible as enumerated exclusions [F/I].
     - RFC 8984 does not mention JSON Schema [F]. Whether one exists elsewhere is unverified.
5. **Retry limits**
   - **Placement:** K or R.
   - **Native:** Arazzo `retryLimit` and `retryAfter`, validated by its JSON Schema [F]. This covers OpenAPI and AsyncAPI steps only.
   - **Custom:** SFTP, object storage, SQL and the change log [F/I].
6. **Delivery identity, sighting and revision**
   - **Placement:** policy in K; sightings in E.
   - **Native, but producer-side:** CloudEvents `source`+`id` ("Consumers MAY assume that Events with identical `source` and `id` are duplicates") [F]. It applies only where the interface emits CloudEvents, e.g. a change log. It says nothing about different bytes under the same id.
   - **Change detection only:** RFC 9110 ETag is "an opaque validator" [F]. It detects a change but gives no revision order.
   - **None:** I found no standard for consumer-side rules on "new revision vs refused". The custom part is identity key, sighting rule and conflict policy.
7. **Publication time and revision order**
   - **Placement:** mapping in K; values in E.
   - **Native:** OpenAPI declares *which* headers must be present [S via track 03]. RFC 9110 `Last-Modified` is a *modification* time, not a publication time [F]. CloudEvents `time`, the `sequence` extension (lexicographic order) and `recordedtime` are documented extensions [F].
   - **Custom:** the *role mapping*, e.g. "publication time = header X / file-name token Y" [I].
8. **Redaction**
   - **Placement:** K.
   - **Native labels:** ODCS `classification` and `criticalDataElement` [F]. CloudEvents `data-classification` [F].
   - **None:** I found no standard for a "redact before keep" action. I examined ODCS property fields, OpenAPI Header Object, CloudEvents extensions, OpenLineage facets and OORS. The action stays custom.
   - **Tip:** model received metadata (headers, file attributes) as an ODCS schema object. Its fields then get native names, types and classification, and only the action is custom [I].
9. **Delivery shape**
   - **Placement:** files and datasets in K; dialect and missing tokens in R; observed manifest in E.
   - **Native:** several ODCS schema objects per contract [F]. Table Dialect (header, headerRows, delimiter, quoteChar, nullSequence…) [F]. Table Schema `missingValues` as `{value, label}` [F].
   - **Custom:** the label vocabulary, e.g. "absent" vs "explicitly empty" [F/I].
   - **None, trailer and record count:** I examined Table Dialect (`commentRows` counts from the top only), CSVW §5.9 (`skipRows`, `commentPrefix`) and ODCS servers. None defines a trailer [F].
   - **None, "population a delivery states whole":** I examined ODCS (`dataGranularityDescription` is free text), Data Package, DCAT Dataset Series and OpenLineage `lifecycleStateChange`. None states snapshot-vs-delta completeness for a delivery [F/I].
10. **SLO and failure class**
    - **Placement:** K.
    - **Native in ODCS:** indicator (metric, query, unit) and objective (operators) [F]. The consequence is only `businessImpact`/`severity` as free strings [F].
    - **OpenSLO** has native SLO/SLI/alert policy, but its validation is defined by the Go SDK, with no JSON Schema or Python validator [F]. It overlaps ODCS operators [I], so I don't recommend it.
    - **None:** I found no failure class (our fault / provider fault / expected absence). OORS `error` vs `fail` vs `skip` is the closest outcome taxonomy [F], but it is runtime, not a classification of the rule.
11. **Execution evidence**
    - **Placement:** E.
    - **Native in OORS:** results reference `contract{contractId, version, server}` and `relatesTo` (a path to the rule). `source.runId` groups the documents of one run [F].
    - **OORS limits:** one `contract` per document [F]. A run that reads under several contract versions emits one OORS document per contract version, linked by `runId` [I]. OORS records no file inventory [F].
    - **Files read:** a Data Package manifest per delivery (`path`, `bytes`, `hash`) covers that [F/I].
    - **Alternative, if the organisation already emits OpenLineage:** a RunEvent with `InputStatistics` and `DatasetVersion` facets, plus a custom facet with its own `_schemaURL` for contract references [F]. The workflow refuted this 1-2; I reviewed it against the spec text and it stands with narrower wording (track 04).

---

## 5. Standards profile (bring-back list)

Accessed 2026-11-19 for all rows.

| Standard | Current version (date) | Governance | Cadence | Validator, Python preferred | Adoption evidence |
|---|---|---|---|---|---|
| ODCS | v3.2.0, approved and tagged 2026-09-08; dated schema snapshots up to 20261117 [F] | Bitol TSC, RFC process; Linux Foundation AI & Data project [F for the TSC; S for LF status] | v3.0.2 2025-03 → v3.1.0 2025-12 → v3.2.0 2026-09, roughly every 6–9 months [F] | JSON Schema (draft 2019-09 family) plus `jsonschema`; `open-data-contract-standard` 3.2.0 (Pydantic); `datacontract-cli` 1.2.11 [S, PyPI] | `vendors.md` lists commercial and open-source tools: Data Contract CLI, OpenMetadata import, FLUID Forge, vowl… [F list; S claims] |
| ODPS | v1.1.0, tagged 2026-09-08 [F] | Bitol TSC [F] | v1.0.0 2025-09 → v1.1.0 2026-09 [F] | JSON Schema [F] | Same ecosystem [S] |
| OORS | v0.8.0, tagged 2026-10-14; v0.8.1 draft; all changelog entries say "DRAFT"; v1.0.0 not released [F] | Bitol TSC; RFC-0018 approved 2026-10-14 [F] | Several drafts in 2026 [F] | JSON Schema in the repo [F]; no dedicated Python package found [S] | None found [S]. Pre-1.0. |
| Frictionless Data Package (Dialect, Schema, Resource) | v2.0, 2024-06-26 [F] | Data Package Working Group with vetoing and voting members [F] | Rare: v1 → v2 took years [F/I] | JSON Schema profiles at `datapackage.org/profiles/2.0/*` [S via track 03]; `frictionless` 5.21.0 [S]; v2 support not checked | `overview/adoption.mdx` exists, not read [S] |
| W3C CSVW | REC 2015-12-17 [F] | W3C; WG closed [S] | None since 2015 [F/I] | No JSON Schema [S, track 03 F8]; `csvw` 4.2.0 [S] | Not assessed |
| OpenAPI | 3.2.0 2025-09-19; 3.2.1 2026-09-10 [S via track 03] | OpenAPI Initiative (Linux Foundation) [S] | Minor about yearly, patches between [S] | JSON Schema published [S] | Ubiquitous [S] |
| Arazzo | 1.1.0 2026-05-17; 1.0.1 2025-01-16; 1.0.0 2024-05-29 [F] | OpenAPI Initiative [F, repo] | About yearly [F] | JSON Schema at `spec.openapis.org/arazzo/1.1/schema/2026-04-15` [S via track 03] | Not assessed |
| RFC 9110, RFC 9530 | 2022, 2024-02, IETF Standards Track [F] | IETF | — | — | — |
| RFC 5545, RFC 8984 | 2009, 2021 [F] | IETF | — | `icalendar` 7.3.0 [S] | — |
| CloudEvents | v1.0.2 release; main is 1.0.3-wip [F] | CNCF [S] | Slow [F/I] | `cloudevents` 2.2.0 [S] | Not assessed |
| OpenLineage | spec 2-0-2; facets versioned individually [F] | LF AI & Data [S] | Frequent client releases [S] | Per-facet JSON Schemas [F]; `openlineage-python` 1.55.0 [S] | Not assessed |
| in-toto Attestation | v1; test-result predicate v0.1 [F] | CNCF in-toto project [S] | — | `in-toto-attestation` 0.9.3, last upload 2023 [S] | Not assessed |
| OpenSLO | v1; v2alpha unstable [F] | Community [S] | Slow [F/I] | Go SDK and `oslo` only [F] | Not assessed |
| DCAT 3, PROV-O, DQV, DCMI | REC 2024-08-22; REC 2013-04-30; Note 2016-12-15; DCMI Terms [F] | W3C, DCMI | — | SHACL/RDF, not JSON Schema [S] | Not assessed |

---

## 6. Recommended minimal set and what stays custom

I applied the brief's ordering: native and schema-validated first, then fewest custom semantics and overlap, then count [I].

| Role | Standard | Owns concerns | Why it's in the set |
|---|---|---|---|
| Contract hub (K) | **ODCS v3.2.0** | Dataset shape; metadata and catalogue as datasets (2, 7, 8 partial); SLA frequency and time (4 partial); quality indicator and objective (10 partial); custom overlay host | Org baseline. Strict schema. Stable ids and versions. |
| File dialect and tokens (R) | **Table Dialect + Table Schema v2** (separate files) | 9: dialect, missing tokens | Only option that is native *and* JSON-Schema validated. CSVW overlaps it and has no JSON Schema [S, track 03 F8]. |
| HTTP interface (R) | **OpenAPI 3.2**, plus **Arazzo 1.1** where calls are sequenced or retried | 3 (request shape), 5 (HTTP), 7 (headers declared) | Native and validated. Only for HTTP interfaces. |
| Evidence (E) | **OORS v0.8** + **Data Package v2 manifest** | 11; observed side of 2, 6, 7, 9 | OORS references ODCS ids and versions natively. The manifest records files, sizes and digests. |
| Org overlay (K) | **Own JSON Schema** for `customProperties` where `vendor: <org>` | 1, 3 (timing), 4 (RRULE and deadline), 5 (non-HTTP), 6, 7 (role mapping), 8 (action), 9 (trailer, population, token labels), 10 (failure class) | Unavoidable. Values reuse RFC 5545, RFC 9110, CloudEvents `sequence` and `dct:valid` semantics. |

Left out, and why [I]:
- **OpenSLO:** overlaps ODCS quality and has Go-only validation.
- **CSVW:** overlaps Table Dialect and has no JSON Schema.
- **DCAT, PROV-O, DQV:** RDF/SHACL is a second validation stack; borrow their term meanings instead.
- **in-toto:** only worth adding if signed evidence becomes a requirement.
- **CloudEvents:** use it as referenced semantics only, and natively where the change log already emits it.
- **Croissant:** ML-oriented and overlaps ODCS.
- **Data Contract Specification:** deprecated.

Why the custom part stays: across the standards examined, each of these concerns either has no field, or has a field with free-text semantics. The specific gaps are trailer, failure class, deviation policy, redaction action and population completeness (§4).

**Watch item:** if Bitol approves RFC 0052 (`blob`) or RFC 0040 (OOCS), part of concerns 2, 3 and 9 could move from the overlay to native [I].

---

## 7. Conceptual composition example (Q4)

Explanatory only. One SFTP feed; file names, ids and versions are illustrative.

```text
contracts/acme-prices/
  acme-prices.odcs.yaml        # ODCS v3.2.0       → validated by odcs-json-schema-v3.2.0.json
                               #   + org overlay   → validated by org-consumer-ext-1.0.0.schema.json (customProperties, vendor: org)
  prices.dialect.json          # Table Dialect v2  → datapackage.org/profiles/2.0/tabledialect.json
  prices.tableschema.json      # Table Schema v2   → .../tableschema.json   (fields generated from ODCS; missingValues authored)
  xetra.ics                    # iCalendar holiday calendar (RFC 5545), referenced
products/market-data.odps.yaml # ODPS v1.1.0 → inputPorts[].contractId: acme-prices, version: 2.1.0
evidence/<runId>/              # not in git review; written per run
  delivery-manifest.json       # Data Package v2 → datapackage.json profile (path, bytes, hash per received file)
  results-acme-prices.oors.yaml# OORS v0.8.0 → contract{contractId: acme-prices, version: 2.1.0, server: sftp-prod},
                               #   source.runId: <runId>, results[].relatesTo: schema/prices/quality/row_count
```

Key fragments, sketched:

```yaml
# acme-prices.odcs.yaml (ODCS v3.2.0)
apiVersion: v3.2.0
kind: DataContract
id: acme-prices
version: 2.1.0
servers:
  - id: sftp-prod
    server: sftp-prod
    type: sftp
    location: sftp://${ACME_HOST}/out/prices_*.csv
    format: csv
    encoding: ISO-8859-1
schema:
  - id: prices
    name: prices
    authoritativeDefinitions:              # glue: open `type`, opaque link
      - type: tableDialect
        url: ./prices.dialect.json
      - type: tableSchema
        url: ./prices.tableschema.json
    quality:
      - id: row_count
        metric: rowCount
        mustBeGreaterThan: 0
        customProperties:
          - property: failureClass         # concern 10, overlay-validated
            vendor: org
            value: providerFault
  - id: provider_catalogue                 # concern 2: catalogue modelled as a dataset
    name: catalogue
slaProperties:
  - id: offer
    property: frequency
    value: 1
    unit: d
    customProperties:
      - property: offerCalendar            # concern 4, overlay-validated
        vendor: org
        value:
          rrule: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"
          exclude: ./xetra.ics
          deadline: "18:30"
          tz: Europe/Berlin
customProperties:
  - property: validTime                    # concern 1, meaning of dct:valid
    vendor: org
    value: {from: 2026-12-01}
  - property: deliveryIdentity             # concern 6
    vendor: org
    value: {key: [fileName, businessDate], onDifferentBytes: newRevision}
  - property: publicationTime              # concern 7
    vendor: org
    value: {source: sftpMtime}
  - property: trailer                      # concern 9
    vendor: org
    value: {pattern: "^TRL;(\\d+)$", recordCountGroup: 1}
```

References and owners:

| Reference | Mechanism | Validated? |
|---|---|---|
| ODPS → ODCS | `inputPorts[].contractId` + `version` | Yes, by the ODPS schema (strings) [F] |
| ODCS → Dialect, Table Schema, calendar | `authoritativeDefinitions{type, url}` | Link shape only; target resolution is our CI [F/I] |
| Data Resource → dialect, schema | `dialect` / `schema` as URL-or-Path | Yes, by the Data Package profile [F] |
| OORS → ODCS | `contract{contractId, version, server}` + `relatesTo` path | Shape yes; target resolution is our CI [F/I] |
| Evidence → evidence | `source.runId` shared by the OORS documents and the manifest folder | Convention, custom [I] |

Unavoidable custom glue [I]:
1. The org overlay schema, plus a CI step that validates `customProperties` by `property` name.
2. Resolving `authoritativeDefinitions` URLs and OORS `relatesTo` paths. No standard tool resolves cross-standard references.
3. Generating Table Schema `fields` from ODCS properties, so field definitions have one owner (ODCS).
4. Grouping the OORS documents and the manifest by `runId`.

---

## 8. Published examples (Q5)

None found that combine ODCS with another standard for a consumer-side, third-party feed [S]. Related leads [S]:
- ODCS docs show SFTP server examples.
- lakeFS recommends contracting "the first internal dataset downstream" of vendor feeds ([lakeFS][lakefs]).
- The search also returned general ODCS guidance and tooling ([Entropy Data][entropy], [ODCS v3.0.2 docs][odcs302], [OpenMetadata ODCS import][omd]).

## 9. Limits

- **ODCS release date:** the v3.2.0 date comes from the git tag. The changelog section carries no date.
- **OpenAPI 3.2:** facts rest on the workflow agents' reads, not mine.
- **Python tooling:** versions are from PyPI metadata; nothing was installed or run.
- **JSCalendar:** no JSON Schema is mentioned in RFC 8984. Whether one exists elsewhere is unverified.
- **Adoption:** evidence is thin outside ODCS's own vendor list.
- **OORS:** still pre-1.0 and labelled DRAFT, so field changes are likely.
- **Workflow refutations:** the workflow refuted two claims; I overruled one (Data Resource `dialect`/`schema`) and narrowed the other (OpenLineage custom facets) on first-hand text (track 04).

[odcs-cp]: https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/custom-other-properties.md
[odcs-schema]: https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/schema.md
[odcs-dq]: https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/data-quality.md
[odcs-sla]: https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/service-level-agreement.md
[dp-ext]: https://datapackage.org/standard/extensions/
[dp-res]: https://datapackage.org/standard/data-resource/
[dp-td]: https://datapackage.org/standard/table-dialect/
[dp-ts]: https://datapackage.org/standard/table-schema/#missingValues
[csvw]: https://www.w3.org/TR/tabular-metadata/
[oas]: https://spec.openapis.org/oas/v3.2.0.html
[oas-hdr]: https://spec.openapis.org/oas/v3.2.0.html#header-object
[arazzo]: https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.1.0.md
[arazzo-fa]: https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.1.0.md#failure-action-object
[oors-res]: https://github.com/bitol-io/open-observability-results-standard/blob/main/docs/results.md
[oors-fund]: https://github.com/bitol-io/open-observability-results-standard/blob/main/docs/fundamentals.md
[ol-in]: https://github.com/OpenLineage/OpenLineage/blob/main/spec/facets/InputStatisticsInputDatasetFacet.json
[ol-nt]: https://github.com/OpenLineage/OpenLineage/blob/main/spec/facets/NominalTimeRunFacet.json
[ol-cf]: https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md#custom-facet-naming
[ce-id]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md#id
[ce-seq]: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/sequence.md
[ce-rt]: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/recordedtime.md
[ce-dc]: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/data-classification.md
[intoto-rd]: https://github.com/in-toto/attestation/blob/main/spec/v1/resource_descriptor.md
[intoto-tr]: https://github.com/in-toto/attestation/blob/main/spec/predicates/test-result.md
[openslo]: https://github.com/OpenSLO/OpenSLO/blob/main/website/docs/specification.md#slo
[rfc9530]: https://www.rfc-editor.org/rfc/rfc9530
[rfc9110-etag]: https://www.rfc-editor.org/rfc/rfc9110#section-8.8.3
[rfc9110-lm]: https://www.rfc-editor.org/rfc/rfc9110#section-8.8.2
[rfc9110-ra]: https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3
[rfc5545]: https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10
[rfc8984]: https://www.rfc-editor.org/rfc/rfc8984#section-4.3.3
[dct-valid]: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/valid/
[dcat-ds]: https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset_Series
[lakefs]: https://lakefs.io/data-contracts/
[entropy]: https://www.entropy-data.com/learn/what-is-a-data-contract
[odcs302]: https://bitol-io.github.io/open-data-contract-standard/v3.0.2/
[omd]: https://docs.open-metadata.org/v1.13.x/api-reference/data-contracts/odcs
