# Consumer-side data interface contracts verified

Verification run for the report `reports/Consumer-side data interface contracts.md`. That report is not edited here; this file states where it changes.

- Brief: `briefs/Consumer-side data interface contracts verified.md`.
- Notes: `research_notes/Consumer-side data interface contracts verified/` (tracks 01–04).
- Cutoff and access date: 2026-11-19.

Labels: **[F]** first-hand (spec text, schema or code read), **[S]** secondary, **[I]** inference.

Who did the work:
- **Part A:** the main session read every source itself.
- **Part B:** three delegated research agents did the reading.
  - The main session spot-checked each agent's decisive quotes against the fetched texts. Those quotes are marked **[F, spot-checked]**.
  - Other B claims carry the agent's label.

---

## Summary

**Changes to the first report's matrix** (brief's concern numbering):

| # | Concern (part) | First report | Now | Driver |
|---|---|---|---|---|
| 2 | Sizes, digests, catalogue | Digests custom; deviation policy none | Unchanged for loose files. **Standardised extension** when the provider ships BagIt bags, plus a consumer BagIt Profile. Deviation policy still none. | B8 |
| 4 | Business-day adjustment, named calendar | None | **Custom, with standardised values**: FpML `BusinessDayConventionEnum` and the `businessCenterScheme` code list. Holiday dates are still external. | B7 |
| 6 | Delivery identity | Custom | Custom. **Standardised extension** only for BagIt deliveries whose Profile requires `External-Identifier`. | B8 |
| 6 | Revision vs refusal | None | **None, confirmed** (OCFL, BagIt, BagIt Profiles). | B8 |
| 9 | Trailer, record count, control total | None | **Standardised extension by reference**: a DFDL 1.0 schema with `dfdl:assert`, referenced from an ODCS custom quality rule. JVM-only tooling. | B9 |
| 9 | Population stated whole | None | **Custom, with referenceable semantics**: RFC 5005 `fh:complete`, GTFS-RT `FULL_DATASET`, ISO 20022 `COMP`/`DELT`. | B10 |
| 10 | Failure class | None | **Custom, with partial referenceable semantics**: RFC 9110 4xx/5xx, OTel span-status rules, SARIF `notApplicable`. No three-way standard exists. | B11 |

"Custom, with standardised values" is still the *custom* class from the brief. It means only the key is ours; its values or meaning come from a published standard.

**Changes to the first report's recommendations from part A:**
- **Missing tokens:** for "absent" vs "explicitly empty", use Table Schema `missingValues` objects, not Table Dialect `nullSequence`. `nullSequence` is a single string (A4) [F]. frictionless 5.21 declares it but does not apply it at read time [F code / I].
- **Overlay validation has no published tool** (A3). The workable route is datacontract-cli `--json-schema` with an org schema that wraps the ODCS schema [F mechanism / I pattern]. It replaces the bundled schema, and some CLI lint checks are skipped [F].
- **Server-level links:** `authoritativeDefinitions` is not allowed on `servers` [F]. Server-level references must go through `customProperties` or a root-level link.
- **Relative paths** in `authoritativeDefinitions.url` are schema-valid [F]. datacontract-cli resolves them relative to the contract, but only for the definition types it resolves, and only on properties [F code].
- **OpenAPI header facts** in the first report were labelled [S]. They are now [F] (A5).

---

## Part A: decision facts

### A1. ODCS v3.2.0 `customProperties` [F]
Source: `schema/odcs-json-schema-v3.2.0.json` at bitol-io/open-data-contract-standard 7c7597e (2026-11-17). It is identical to the dated snapshot `-20261117`.

- **Allowed on:**
  - root;
  - root `description`;
  - `servers[]` (every type);
  - schema objects;
  - properties, at any nesting level, via `SchemaElement`;
  - quality rules (`DataQuality`);
  - SLA entries (`ServiceLevelAgreementProperty`);
  - support items, team, team members, roles;
  - enum values, synonyms;
  - relationships;
  - context statements and constraints.
- **Not allowed on:** `price`.
- **`value`:** `$ref: AnyType` = anyOf string, number, integer, boolean, null, array, object. Objects and arrays are valid.
- **No other constraint** on `value` anywhere in the schema: no `if/then` on `property`, no per-vendor branch.
- **Item shape:** `required: [property, value]`, `additionalProperties: false`, `vendor` without a pattern.
- **Doc/schema mismatch:** the prose ([custom-other-properties.md](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/custom-other-properties.md)) marks `property` and `value` "Required: No"; the schema requires both.

### A2. ODCS `authoritativeDefinitions` [F]
- **Allowed on:**
  - root;
  - root `description`;
  - schema objects and properties;
  - quality rules;
  - SLA entries;
  - team, team members;
  - enum values;
  - context items.
- **Not allowed on:** servers, support items, roles, synonyms, relationships.
- **Relative path:** `url` is `{"type": "string"}` with no `format: uri`, so a relative path is schema-valid.
  - The doc says only "URL to the authority" ([authoritative-definitions.md](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/authoritative-definitions.md)).
  - No ODCS example uses a relative path; examples do use `jdbc:` URLs.
- **Tool support:** datacontract-cli (`lint/resolve.py`, 75160dc) resolves local files "relative to" the contract for property-level definitions of type semantics, definition or businessDefinition. A broken reference rejects the contract [F code].

### A3. Overlay validation of `customProperties`
**Verdict: none published** [F/S].
- **ODCS repo** [F]: no mechanism. The only related negative test checks that `vendor` is a string.
- **datacontract-cli** [F code + CHANGELOG]: `--json-schema` *replaces* the ODCS schema ("the custom schema is the source of truth").
  - Unknown top-level fields are then accepted.
  - Duplicate-name and enum checks are skipped.
  - An org schema that `allOf`s ODCS and adds `if property == X then value: {…}` would work through this flag [I]. This is a pattern, not a published convention.
- **`vendors.md`** [F list / S claims]: no entry describes it. Enkinex ODCS (KCL, "typed … with constraints") could not be checked: the site returned an empty JavaScript shell.

### A4. Frictionless Table Dialect v2 standalone
- **Standalone file: yes** [F].
  - "A root level Table Dialect descriptor `MAY` have a `$schema` property", recommended `https://datapackage.org/profiles/2.0/tabledialect.json` ([table-dialect](https://datapackage.org/standard/table-dialect/#dollar-schema)).
  - The published profile equals the repo copy.
  - Tested with `jsonschema`:
    - a valid sample passes;
    - `nullSequence: ["NA", ""]` fails ("is not of type 'string'");
    - `delimiter: ";;"` passes, so single characters are not enforced.
  - The glossary allows YAML internally, but a descriptor "`SHOULD NOT` be externally published in any other format rather than JSON".
- **`nullSequence`: one value** [F]. "`MUST` be a string; undefined by default. This property specifies the null sequence, for example, `\N`" ([#nullSequence](https://datapackage.org/standard/table-dialect/#nullSequence)).
- **frictionless 5.21.0** [F code, CHANGELOG, `docs/advanced/datapackage-versions.md`]:
  - Resolves v2 from a standard `$schema` URL; an absent `$schema` is treated as v1.
  - `Dialect.metadata_v2_profile` is the 2.0 Table Dialect profile.
  - `headerRows`, `headerJoin`, `commentRows` and `commentChar` are implemented.
  - v2 `missingValues` objects are supported since 5.20.
  - `null_sequence` is declared in the CSV control, but no read path uses it. That this means "not applied" is [I].
  - Not run: the pip install was refused by the session's permission policy.

### A5. OpenAPI 3.2 Header and Response Objects [F]
Source: raw `versions/3.2.0.md` and `3.2.1.md`. Revision history: **3.2.0 = 2025-09-19**, **3.2.1 = 2026-09-10**.

- **Response Object `headers`:** "Maps a header name to its definition … If a response header is defined with the name "Content-Type", it SHALL be ignored." ([response-headers](https://spec.openapis.org/oas/v3.2.1.html#response-headers))
- **Header Object:**
  - `required`: "Determines whether this header is mandatory. The default value is `false`."
  - `schema`: a Schema Object, so `format` and `pattern` apply ([header-object](https://spec.openapis.org/oas/v3.2.1.html#header-object)).
- **Formats:** the OAI Format Registry lists `http-date` ("HTTP-date - RFC7231"). Support for registered formats "is strictly OPTIONAL".
- **Verdict:** a required response header with `format: http-date` is native. Enforcement depends on the tool.

### A6. Bitol open RFCs 0052 and 0040 [F]
Both are listed under "Open RFCs" ([rfcs/README.md](https://github.com/bitol-io/tsc/blob/main/rfcs/README.md)). No vote is recorded for either; the TSC votes "at its monthly meeting".

| RFC | Applies to | Target | Dates (git) | Vote |
|---|---|---|---|---|
| [0052 `logicalType: blob`](https://github.com/bitol-io/tsc/blob/main/rfcs/0052-blob-storage-file-logical-type.md) | ODCS | **None stated**; examples use `apiVersion: v3.1.0` | Added 2026-06-30, last change 2026-07-14 | None |
| [0040 OOCS](https://github.com/bitol-io/tsc/blob/main/rfcs/0040-oocs.md) | OOCS only (ODCS, ODPS and OORS unchecked) | Own "v0.1.0 (draft)" | 2026-04-10 → 2026-06-30 | None; "Slack: TBD. GitHub issue: TBD." |

The next open ODCS release is v3.3.0, which is RFC 0062's target. Whether 0052 lands there is unknown [I].

---

## Part B: "none" verdicts re-tested

### B7. Business-day adjustment and named calendars (concern 4)

**Verdict: the first report's "none" is wrong for open standards in general.** It holds only for RFC 5545, RFC 8984 and DCAT 3.

**Adjustment conventions** are defined in:
- **FpML `BusinessDayConventionEnum`** [F via mirror of the ISDA 5.13 XSD]:
  - Values: FOLLOWING, MODFOLLOWING, PRECEDING, MODPRECEDING, NEAREST, FRN, NONE, NotApplicable.
  - Definition: "The convention for adjusting any relevant date if it would otherwise fall on a day that is not a valid business day."
  - Licence: FpML Public License 3.0, royalty-free [F].
  - The current release is 5.14 (2026-10-20); its HTML documentation needs a login (unreachable).
- **FINOS CDM** (CSL 1.0) [F]:
  - Same enum and `BusinessDayAdjustments`.
  - Executable `AdjustDateToBusinessDayConvention` ("only FOLLOWING, PRECEDING, and MODFOLLOWING … implemented").
- **FIX Latest `BusinessDayConventionCodeSet`** [F].
- **ACTUS BDC** [F].
- **ISO 20022 `BusinessDayConventionCode`** FWNG/MODF/PREC/NEAR [S; iso20022.org returned 403].

**Named calendar code list:**
- **FpML `businessCenterScheme`**, coding scheme [§5.19](https://www.fpml.org/spec/coding-scheme/fpml-schemes.html), genericode at a versioned URI, **[F, spot-checked]**:
  - https://www.fpml.org/coding-scheme/business-center, version **9-4**, published **2025-04-25**, 212 codes.
  - Examples: `GBLO` "London", `EUTA` "TARGET Settlement Day", `USGS` "U.S. Government Securities Business Day".
- CDM validates its `BusinessCenter` against this list (bundled copy 9-3) [F]. FIX references it [F].
- `commodityBusinessCalendarScheme` (§5.39) covers exchange calendars [F].

**Gaps:**
- **No standard publishes the holiday dates.** CDM's `BusinessCenterHolidays` is a "data provider" hook [F].
- **ISO 10383 MIC** has no calendar, holiday or trading-hours field [F, CSV/XSD header and FAQ]. FpML only derives exchange calendar codes from MIC acronyms [F].
- **SDMX** removed its release calendar in 3.0 [F].

**Coverage change for concern 4: none → custom, with standardised values** [I].
- ODCS still has no field [F].
- An overlay key could carry `businessDayConvention: MODFOLLOWING` and `businessCenters: [EUTA]`, with `authoritativeDefinitions` pointing at the versioned scheme URI.
- Deadline computation still needs an external holiday source.
- This replaces the first report's `.ics` exclusion file as the way to *name* the calendar. iCalendar remains useful for the *dates*.

### B8. Delivery identity, revisions, fixity (concerns 2, 6)

**OCFL 1.1** ([spec](https://ocfl.io/1.1/spec/); v1.1.1, updated 2024-11-07, CC-BY 4.0):
- Identity [F]: `id` "MUST NOT change between versions" (§3.5.1).
- Versions [F]: immutable, continuous v1…vN (§3.3); sha256/sha512 content addressing (§3.4).
- But [F, spot-checked]: "The specification takes no position on what constitutes a version or a versionable action". It has no "refuse" outcome.
- It is a storage-at-rest format, not a transfer format [F/I].
- Tooling: inventory JSON Schema (non-normative); `ocfl-py` 2.1.0 [F PyPI].

**BagIt** ([RFC 8493](https://www.rfc-editor.org/rfc/rfc8493), Informational, 2018):
- Fixity [F]:
  - payload manifests MUST list every file (§2.1.3);
  - SHA-256/512 MUST be supported (§2.4);
  - `Payload-Oxum` is "the 'octetstream sum' of the payload" plus the file count, as an optimisation [F, spot-checked];
  - `fetch.txt` allows remote payload.
- Identity: `External-Identifier` is "sender-supplied", optional, with no uniqueness requirement. `Bag-Group-Identifier` + `Bag-Count` [F].
- Versioning: none [F; OCFL §5.4 says the same].
- **BagIt Profiles 1.4.0** ([spec](https://bagit-profiles.github.io/bagit-profiles-specification/), 2023, CC0) is the consumer-side layer [F, spot-checked]. It lets "creators and consumers of Bags … agree on optional components". It can require tags and manifests, but has no revision policy.

**Verdicts:**
- **Revision vs refusal (6): none, confirmed.** Examined: OCFL 1.1 spec and implementation notes, RFC 8493, BagIt Profiles 1.4.0, ODCS v3.2.0.
- **Identity (6) and fixity (2): standardised extension** only where the provider ships bags and we publish a BagIt Profile (referenced from ODCS). For loose SFTP or object-store files they stay custom; the BagIt manifest line format can be reused as a convention [I].

### B9. Trailer records and control totals (concern 9)

**Fixed domain formats with trailers** (usable only if the feed *is* that format):
- NACHA ACH File Control "9": entry/addenda count, entry hash, totals [F, free developer guide]. The normative Rules are paid.
- BAI2 49/98/99 trailers: "File Control Total … Algebraic sum of all group control totals" [F, © BAI, free PDF].
- EDIFACT UNT/UNZ [S; UNECE returned 403].
- X12 SE01/IEA01 [S, licensed].
- ISO 20022 `NbOfTxs`/`CtrlSum`. These are header totals [S].

**General description language: DFDL 1.0** ([OGF GFD-R-P.240](https://ogf.org/documents/GFD.240.pdf), Feb 2021, updated June 2023, "Distribution is unlimited"):
- `dfdl:assert` raises a Processing Error; "The dfdl:assert checks are performed even when validation is off" [F, spot-checked].
- `fn:count($arg)` [F, spot-checked].
- `occursCountKind='expression'` reads a header count (§16.1) [F].
- There is no `fn:sum`; control sums are possible via `inputValueCalc` running totals (§17) [F].
- Agent's test with Apache Daffodil 4.2.0 [F]:
  - a count mismatch was rejected;
  - `fn:sum` failed with "Unsupported function";
  - a running-total mismatch was rejected.
- Tooling is JVM only (Daffodil, IBM ACE). No Python processor exists [F PyPI / I].
- Community DFDL schemas (NACHA, EDIFACT) parse trailers but never assert them [F].

**Other areas, no trailer:** RFC 4180 ("optional header line" only) [F]; Kaitai Struct (`valid: {expr}`, not a standards body, untested) [F/I]; plus Table Dialect and CSVW from the first run.

**Coverage change for concern 9 (trailer): none → standardised extension by reference** [I].
- ODCS quality `type: custom` with `engine` (free string, so our convention) and `implementation` = DFDL schema URL; or `authoritativeDefinitions`.
- ODCS `rowCount` cannot read a value from the file [F].

### B10. Snapshot vs delta (concern 9, "population stated whole")

**Full-state declarations exist, each bound to its own payload:**
- **GTFS-Realtime** `FeedHeader.incrementality` = `FULL_DATASET` | `DIFFERENTIAL`, default FULL_DATASET [F, spot-checked proto].
  - FULL_DATASET "expected to provide a full snapshot" [F agent, [reference](https://gtfs.org/documentation/realtime/reference/)].
  - DIFFERENTIAL is "unsupported and behavior is unspecified".
- **RFC 5005 `fh:complete`** (Standards Track) [F, spot-checked; [§2](https://www.rfc-editor.org/rfc/rfc5005#section-2)]: "indicates that the feed document it occurs in is a complete representation of the logical feed's entries"; "any entry not actually in the feed document SHOULD NOT be considered part of that feed".
- **ISO 20022 `UpdTp`** `COMP` "Statement is complete." / `DELT` "Statement contains changes only." [S, mirrors].

**Increment markers only, or no flag** [F unless noted]:
- OData v4.01 delta payload.
- RFC 3229 226.
- SDMX Append/Merge. A whole-dataset Replace is not possible; only a wildcard Delete + Merge idiom.
- Iceberg `summary.operation`, where `overwrite` may be partial.
- Delta Lake (no field).
- Delta Sharing (mode set by request; `limitHint` may return "only some files").
- Debezium `op=r` / `source.snapshot` (project, not a standard).
- Hudi INSERT_OVERWRITE_TABLE (implementation).
- OpenLineage OVERWRITE (scope undefined).

**None in:** CloudEvents, DCAT 3, DCMI `accrualMethod`, Frictionless, DQV, ODCS v3.2.0 [F].

**Coverage change for concern 9 (population): none → custom, with referenceable semantics** (link RFC 5005 §2 or GTFS-RT `FULL_DATASET`) [I].

### B11. Failure attribution (concern 10)

**By fault side:**
- **RFC 9110 §15** [F, spot-checked; [§15.5](https://www.rfc-editor.org/rfc/rfc9110#section-15.5), [§15.6](https://www.rfc-editor.org/rfc/rfc9110#section-15.6)]:
  - 4xx: the "client seems to have erred"; 5xx: the server "is aware that it has erred".
  - Absence (404 "does not indicate whether … temporary or permanent"; 410 "intentionally unavailable") sits inside the client-error class [F].
- **OpenTelemetry HTTP/gRPC span conventions** (Stable) [F]:
  - 4xx "MUST be left unset … SERVER and SHOULD be set to Error … CLIENT".
  - "a 404 … is not an error when the application is simply checking whether the resource exists".
  - Fixed list of server-side gRPC error codes.

**By remediation or audience:**
- gRPC codes (retry guidance; "Generated at Client or Server" shows origin, not fault) [F].
- SARIF 2.1.0: `result.kind` `notApplicable`; notifications split by who must act [F].

**Outcome type only:** JUnit XML, TAP 14, in-toto test-result, Open Test Reporting, OORS (`error` = "query failed, or the source was unreachable", which mixes both sides), OpenLineage, DQV, ODCS [F].

**Coverage change for concern 10 (failure class): none → custom, with partial referenceable semantics** [I].
- No standard gives consumer fault / provider fault / legitimate absence for a data check.
- An overlay enum can cite RFC 9110 classes and OTel's absence rule as its definitions.

---

## Effect on the recommended set (first report §6)

The core set is unchanged [I]:
- ODCS v3.2.0;
- Table Dialect + Table Schema v2;
- OpenAPI 3.2 / Arazzo 1.1;
- OORS + Data Package manifest;
- the org overlay schema.

Additions, each optional and scoped:
1. **FpML coding schemes as referenced value sets.** For concern 4, the overlay's `businessDayConvention` and `businessCenters` take FpML values, linked by versioned URI. No new document type and no XSD processing are needed [I].
2. **DFDL 1.0, only for fixed-width or trailer-bearing feeds** (concern 9). It costs a JVM dependency (Daffodil), plus an ODCS `custom` quality engine name we define [F/I].
3. **BagIt Profile, only where a provider delivers bags** (concerns 2, 6). Python `bagit` 1.9.0 validates bags; `bagit-profile` 1.3.1 (2020) may lag Profiles 1.4.0 [F PyPI / I].

Still custom after this run:
- valid time (1);
- request timing tolerance (3);
- non-HTTP retries (5);
- revision policy (6);
- publication-time role mapping (7);
- redaction action (8);
- population flag (9, semantics referenced);
- failure class (10, semantics partly referenced);
- provider deviation policy (2).

## Limits
- **Delegated reading:** Part B quotes not marked "spot-checked" rest on the agents' reading.
- **Unreachable:**
  - iso20022.org (Akamai 403), so ISO 20022 claims are [S] from mirrors;
  - UNECE (403);
  - FpML 5.14 HTML documentation (login);
  - ISO 10383 standard text (paid);
  - NACHA Rules (paid);
  - X12 (licensed).
- **Not run:** frictionless 5.21 (install refused). ocfl-py, bagit-python and Kaitai were not run.
- **DFDL test:** run by an agent with a downloaded, sha512-checked Daffodil binary on the agent's own test files, not on real feed data.
