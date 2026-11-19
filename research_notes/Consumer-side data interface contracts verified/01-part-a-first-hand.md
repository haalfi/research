# Track 1 (verification run): Part A, decision facts, first-hand

Access date 2026-11-19. Clones are shallow, under the session scratchpad; the HEADs read are listed per item.
Labels: [F] spec text, schema or code read; [S] secondary; [I] inference.

## A1. ODCS v3.2.0 `customProperties`
Source: bitol-io/open-data-contract-standard 7c7597e (2026-11-17), `schema/odcs-json-schema-v3.2.0.json`.
It is byte-identical to the dated snapshot `odcs-json-schema-v3.2.0-20261117.json` (`cmp`) [F].
Draft is 2019-09; there is no `$id` [F].

**Where `customProperties` is allowed** [F]. I walked the schema for every `properties.customProperties` key:
- root;
- root `description` object (usage/purpose/limitations);
- `Server` (every server type);
- `SchemaElement`. `SchemaObject` uses `allOf` → SchemaElement. `SchemaProperty` and `SchemaItemProperty` use `$ref` → `SchemaBaseProperty`, which uses `allOf` → SchemaElement. So schema objects, properties and nested properties all qualify;
- `DataQuality` (quality rules);
- `ServiceLevelAgreementProperty` (SLA entries);
- `SupportItem`, `Team`, `TeamMember`, `Role`;
- `EnumValue`, `Synonym`;
- `RelationshipBase`;
- `Context` `verifiedStatements[]` and `constraints[]` items.

It is **not** allowed on `Pricing` (keys id, priceAmount, priceCurrency, priceUnit) [F].

**`value` typing** [F]:
- `CustomProperty` = {id, property, value, description, vendor}, `required: [property, value]`, `additionalProperties: false`.
- `value` → `$defs/AnyType` = `anyOf` [string, number, integer, boolean, null, array, object]. So any JSON value, objects and arrays included.
- The schema constrains `value` nowhere else: no `if/then` keyed on `property`, no per-vendor branch.

**Spec/schema mismatch** [F]: `docs/custom-other-properties.md` marks `property` and `value` "Required: No", while the schema requires both.
`vendor` has no `pattern` in the schema; the doc says the pattern is a SHOULD, "not enforced".

## A2. ODCS `authoritativeDefinitions`
**Allowed on** [F, same schema walk]:
- root;
- root `description`;
- `SchemaElement` (schema objects, properties, nested properties);
- `DataQuality`;
- `ServiceLevelAgreementProperty` (new in v3.2.0);
- `Team`, `TeamMember`;
- `EnumValue`;
- `Context` items.

**Not allowed on** `Server` (Server keys: id, server, type, description, environment, roles, customProperties) [F], `SupportItem`, `Role`, `Synonym` or `RelationshipBase` [F].

**Relative path as `url`** [F]: the item is {id, url, type, description}, `required: [url, type]`, `additionalProperties: false`.
`url` is `{"type": "string"}` with **no `format: uri`**, so a relative path is schema-valid.
- The doc only says "URL to the authority" (`docs/authoritative-definitions.md`).
- No ODCS example uses a relative path. The examples use https and also `jdbc:` URLs (e.g. `docs/examples/all/postgresql-adventureworks-contract.odcs.yaml`) [F].

**Tool behaviour** [F, code]: datacontract-cli 75160dc (2026-11-18), `datacontract/lint/resolve.py` `inline_definitions_into_data_contract`.
It resolves `authoritativeDefinitions[type in {semantics, definition, businessDefinition}]` on properties: "local file references resolve relative to [the contract's location]", and "a broken reference rejects the contract".
So relative paths are understood by at least one tool, but only for those types and only on properties.

## A3. Overlay validation of `customProperties`
**ODCS repo** [F]: nothing beyond the ODCS schema itself.
- `src/script/negative-tests/vendor-wrong-type.odcs.yaml` only tests that `vendor` is a string.
- No convention or mechanism for a per-property value schema exists in the docs, CHANGELOG or RFC 0035.

**datacontract-cli** [F, code + CHANGELOG]:
- `--json-schema <path|url>` *replaces* the bundled ODCS schema: "the custom schema is the source of truth" (`resolve.py`, `_LaxOpenDataContractStandard`).
- With a custom schema, Pydantic accepts extra top-level fields, and the duplicate-name and enum checks are skipped (CHANGELOG: "checks are skipped with a custom `--json-schema`").
- The flag swaps the schema; it does not overlay one. An org schema that `allOf`-includes the ODCS schema plus `if property == X then value: {...}` rules would work through it [I].
- Cost: the CLI's own extra lint checks are lost (CHANGELOG #1771) [F].

**`vendors.md` entries** [F list; S claims]: no entry describes validating `customProperties` against a separate schema.
- Enkinex ODCS (KCL library, "typed ODCS schemas … with constraints") is the only plausible candidate. Its site returned an empty JS shell, so it is unverified.

**Verdict**: no published tool or convention validates `customProperties` against a separate schema.
Closest: datacontract-cli `--json-schema` with an org-authored wrapper schema [F mechanism, I pattern].

## A4. Frictionless Table Dialect v2 standalone, `nullSequence`, frictionless-py
Source: frictionlessdata/datapackage da3526c, `content/docs/standard/table-dialect.mdx`, `glossary.mdx`; profile `public/profiles/2.0/tabledialect.json`.
The profile is identical to the published https://datapackage.org/profiles/2.0/tabledialect.json (fetched, compared as JSON: equal) [F].

**Standalone file** [F]:
- "A **root level** Table Dialect descriptor `MAY` have a `$schema` property that `MUST` be a profile …; recommended value is `https://datapackage.org/profiles/2.0/tabledialect.json`".
- Glossary: a descriptor is a JSON object, physically a file. YAML "`MAY` be serialized … as an internal part of some project … A descriptor `SHOULD NOT` be externally published in any other format rather than JSON".
- The profile is draft-07, `title: "Table Dialect"`, `type: object`, no `additionalProperties: false`. Unknown keys pass.

**Test** [F, ran `jsonschema` against the profile]:
- `{"$schema": …2.0…, "delimiter": ";", "headerRows": [1], "nullSequence": "NA"}` → valid.
- `{"nullSequence": ["NA", ""]}` → "is not of type 'string'".
- `{"delimiter": ";;"}` → valid. The profile does not enforce a single character.

**`nullSequence`** [F]: "`MAY` have the `nullSequence` property that `MUST` be a string; undefined by default. This property specifies the null sequence, for example, `\N`." → **one value only**.
Several tokens need Table Schema `missingValues` (array, optionally `{value, label}`).

**frictionless-py 5.21.0** [F, code at c08fa29 2026-10-15 + CHANGELOG + `docs/advanced/datapackage-versions.md`]:
- `settings.VERSION = "5.21.0"`.
- `Dialect.metadata_v2_profile = "https://datapackage.org/profiles/2.0/tabledialect.json"`.
- Dialect fields `header_rows`, `header_join`, `comment_rows` and `comment_char` are implemented in row handling (`dialect.py` lines ~169–232).
- Flat v1/v2 CSV keys (delimiter, lineTerminator, quoteChar, doubleQuote, escapeChar, nullSequence, skipInitialSpace) are moved into a `csv` control on import.
- Version resolution: "`$schema` standard profile URL → v1 or v2 (from the URL)"; "an absent `$schema` is an explicit v1".
- v2 features are gated: `missingValues` objects (5.20 notes, #1787), `$schema` (#1784), `fieldsMatch` (#1790), `exclusiveMinimum/Maximum` (5.21, #1840).
- **`nullSequence` is declared but not applied.** The only occurrences are the control field `null_sequence` (`formats/csv/control.py:55`), its metadata profile entry and the v1 key list. The CSV parser passes `delimiter`, `line_terminator`, `escape_char`, `quote_char` and `skip_initial_space` to Python `csv`, and `null_sequence` appears nowhere else in the package [F code; that it has no effect at read time is I].
- I could not run it: a pip install in a scratch venv was refused by the session's permission policy.

**Verdict**: yes, a standalone dialect validates against the published 2.0 profile.
frictionless 5.21 reads v2 dialect fields when `$schema` names the 2.0 profile. It does not appear to apply `nullSequence`.

## A5. OpenAPI 3.2: Header and Response Objects
Source: raw `versions/3.2.0.md` and `versions/3.2.1.md` from OAI/OpenAPI-Specification main (HTTP 200).

**Dates** (Appendix A, Revision History, 3.2.1 text) [F]:
- 3.2.1 = 2026-09-10, "Patch release";
- 3.2.0 = 2025-09-19, "Release";
- 3.1.2 = 2025-09-19.

**Response Object `headers`** [F]: "Map[`string`, Header Object | Reference Object] — Maps a header name to its definition. … If a response header is defined with the name `"Content-Type"`, it SHALL be ignored."

**Header Object** [F]:
- "follows the structure of the Parameter Object … `name` MUST NOT be specified … `in` MUST NOT be specified".
- `required` (boolean): "Determines whether this header is mandatory. The default value is `false`."
- `schema` (Schema Object) or `content` (exactly one media type).
- Values passed "through unchanged". `style` must be `simple`.

**Format** [F]: `schema` is a full Schema Object, so `format` is available.
- The OAI Format Registry (https://spec.openapis.org/registry/format/, fetched) lists `http-date`: "date and time as defined by HTTP-date - RFC7231", type string.
- 3.2.1 §Format Registry: "Support for any registered format is strictly OPTIONAL".

**Verdict**: yes. `required: true` plus `schema: {type: string, format: http-date}`, or `pattern`, is native.
Format enforcement depends on the tool [F].

## A6. Bitol open RFCs 0052 and 0040
Sources: bitol-io/tsc 1f1c6d7 (2026-11-10). History is from a `--filter=blob:none` clone, `git log -- <file>`.

Both RFCs are listed under "Open RFCs" ("proposed / in discussion / awaiting a vote") in `rfcs/README.md` [F].
Process: "When ready, RFCs will be voted on by the TSC at its monthly meeting" [F].
Neither RFC records a vote or decision [F].

**RFC 0052** "File Object Storage Layout via `logicalType: blob`":
- Applies to ODCS only.
- First commit 2026-06-30 (#78); last change 2026-07-14 (#79) [F].
- **No target ODCS version** stated in the text. Its examples use `apiVersion: v3.1.0` [F].
- Context: RFC 0062 targets ODCS v3.3.0, so v3.3.0 is the next open ODCS release [F]. Whether 0052 lands there is unknown [I].

**RFC 0040** "Open Orchestration and Control Standard (OOCS)":
- Applies to OOCS only; ODCS, ODPS and OORS are unchecked [F].
- Text: "**Version**: v0.1.0 (draft)", media type `application/oocs+yaml;version=0.1.0` [F].
- History: 2026-04-10 (first), …, 2026-06-29 "adopt ODCS scheduling vocab" (#64), last 2026-06-30 [F].
- No vote date and no target release of an existing standard [F]. "Slack: TBD. GitHub issue: TBD." [F].
