# Follow-up: Consumer-side data interface contracts (verification run)

Same branch, new title "Consumer-side data interface contracts verified". Don't edit the first report. Same labels ([F]/[S]/[I]), same cutoff (2026-11-19).

## A. Facts a decision will rest on: read first-hand

1. **ODCS v3.2.0 `customProperties`**: in the published JSON Schema, on which objects is it allowed (root, servers, schema objects, properties, quality rules, SLA entries)? Is `value` typed as any JSON (object, array), and does the schema constrain it anywhere?
2. **ODCS `authoritativeDefinitions`**: on which objects is it allowed? Is a relative path a valid `url`?
3. **ODCS overlay validation**: does any published tool or convention validate `customProperties` against a separate schema (datacontract-cli, the ODCS repo, `vendors.md` entries)? If none, say so.
4. **Frictionless Table Dialect v2 on its own**: can a standalone Table Dialect file be validated against a published profile, outside a Data Package? Quote the semantics of `nullSequence` (one value or several?). Does `frictionless` 5.21 read v2 dialects? Read the release notes or code, not just PyPI.
5. **OpenAPI 3.2**: re-read first-hand the Header Object and Response Object: can a response header be declared required, with a format? Version and date of 3.2.0 and 3.2.1.
6. **Bitol open RFCs 0052 (blob) and 0040 (OOCS)**: status, target ODCS version, and whether a vote or draft date is set.

## B. "None" verdicts to test where the first run didn't look

7. **Business-day adjustment and named holiday calendars (concern 4)**: search any domain for a published standard that defines business-day adjustment conventions or a code list naming holiday or business calendars. Also look for an ISO code list that identifies trading venues or their calendars.
8. **Delivery identity, revisions and fixity (concerns 2, 6)**: examine OCFL 1.1 (object identity, versions, inventory, fixity) and BagIt (RFC 8493: manifests, tag files, payload oxum). Does either express "what identifies one delivery" or "different bytes under the same identity are a new version"?
9. **Trailer records and control totals (concern 9)**: any open flat-file or tabular description standard that declares a footer or trailer record with a record count or control total.
10. **Snapshot vs. delta (concern 9, "population a delivery states whole")**: any open standard field that declares a delivery to be the complete state of a stated scope, as opposed to an increment (change-data-capture, data-sharing or table-format specs included).
11. **Failure attribution (concern 10)**: any standard that classifies a failed check or call by fault, as consumer fault vs. provider fault vs. an expected or legitimate absence, beyond pass/fail/error.

## Bring back

Per item: verdict, spec section linked, label. For B: the coverage class it changes in the first report's matrix, if any. Each "none" names the areas examined.
