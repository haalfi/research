# Track 2 (verification run): B7, business-day adjustment and named calendars

Produced by a delegated research agent on 2026-11-19. I spot-checked one claim myself (below).
Labels are the agent's unless marked "(spot-check)".
The agent's downloads are in the session scratchpad `b7/`.

## Spot-check (main session) [F]
I fetched https://www.fpml.org/coding-scheme/business-center (HTTP 200, OASIS genericode XML):
- ShortName `businessCenterScheme`;
- Version `9-4`;
- CanonicalUri `http://www.fpml.org/coding-scheme/business-center`;
- CanonicalVersionUri `…/business-center-9-4`;
- publicationDate `2025-04-25`;
- 212 rows.

Sample rows:
- `GBLO` "London, United Kingdom";
- `EUTA` "TARGET Settlement Day";
- `USGS` "U.S. Government Securities Business Day (as defined in 2006 ISDA Definitions Section 1.11 …)";
- `DEFR` "Frankfurt, Germany".

The columns are code, source and description only; the list carries no holiday dates.
This agrees with the agent's report.

## FpML (ISDA)
**Version and source**
- XSD read: FpML 5.13 Recommendation build 7, `fpml-enum-5-13.xsd` and `fpml-shared-5-13.xsd`. Read via the Apache-2.0 mirror `rosetta-models/rune-fpml`; the file text is ISDA's [F via mirror].
- Current release per fpml.org: 5.14 Recommendation, 2026-10-20, build 5.
- The 5.14 HTML documentation requires a login (**unreachable**).
- Coding Schemes catalogue: 2026-10-30, version 2.27 [F].

**Licence**: FpML Public License 3.0, effective 2026-02-01. "world-wide, royalty-free, non-exclusive license … to use, reproduce, modify … distribute the FpML Specifications" [F].

**Findings**
- `BusinessDayConventionEnum` (`fpml-enum-5-13.xsd` l.188) [F]:
  - Values: FOLLOWING, FRN, MODFOLLOWING, PRECEDING, MODPRECEDING, NEAREST, NONE, NotApplicable.
  - Definition: "The convention for adjusting any relevant date if it would otherwise fall on a day that is not a valid business day."
- `BusinessDayAdjustments` (`fpml-shared-5-13.xsd` l.764) [F]: `businessDayConvention` plus business centers.
- `BusinessCenter` (l.696) [F]: "A code identifying a business day calendar location … drawn from the list identified by the business day calendar location scheme".
  - Attribute `businessCenterScheme`, default `http://www.fpml.org/coding-scheme/business-center`.
  - The XSD does not enumerate the codes; they are checked against the external scheme.
- Coding scheme §5.19, https://www.fpml.org/spec/coding-scheme/fpml-schemes.html [F]: "accepts a 4 character code of the real geographical business calendar location or FpML format of the rate publication calendar".
- `commodityBusinessCalendarScheme` §5.39 (v3-6, 2020-02-04): exchange and price-source calendars [F].
- **No holiday dates are published behind the codes** [F/I].

## FINOS CDM
**Source**: finos/common-domain-model master 9f0d6d8 (2026-11-18); latest non-dev tag 7.10.0.
**Licence**: Community Specification License 1.0 [F].

**Findings**
- `enum BusinessDayConventionEnum` (`base-datetime-enum.rosetta` l.125): same eight values as FpML [F].
- `type BusinessDayAdjustments` and `type BusinessCenters` ("enumerated list that is maintained by the FpML standard") [F].
- There is no `BusinessCenterEnum` any more [F]. Instead:
  - `typeAlias BusinessCenter: FpMLCodingScheme(domain: "business-center")`;
  - validated by `ValidateFpMLCodingSchemeDomain` against the bundled `business-center-9-3.json`, one version behind live 9-4 [F].
- `AdjustDateToBusinessDayConvention`: "only FOLLOWING, PRECEDING, and MODFOLLOWING conventions are implemented" [F].
- `func BusinessCenterHolidays: [codeImplementation] // data provider` [F]. Holiday data is external.
- A JSON Schema artifact `org.finos.cdm:cdm-json-schema` is stated in `docs/download.md` [F for the statement]; the artifact was not opened.

## FIX Latest (Orchestra, Extension Pack 313, 2026-11-06)
- `BusinessDayConventionCodeSet`: NotApplicable, None, FollowingDay, FloatingRateNote, ModifiedFollowingDay, PrecedingDay, ModifiedPrecedingDay, NearestDay [F].
- Business-center fields (e.g. tag 40067) say: "See https://fpml.org/coding-scheme/business-center for standard 4-character code values" [F].
- Repository README: Apache-2.0; the file itself says "Copyright (c) FIX Protocol Ltd." [F].

## ACTUS Data Dictionary 1.4 (2023-12-08, CC BY-SA 4.0)
- `businessDayConvention`: 9 shift-and-calculate variants (SCF, SCMF, CSF, …) [F].
- `calendar`: only `noCalendar` and `mondayToFriday`; "Custom calendars can be added as additional enum options" [F].
- So there is **no named holiday-calendar list**.

## ISO 20022
**Primary site unreachable**: iso20022.org catalogue and code-set pages returned 200 Connection Established, then 403 from AkamaiNetStorage.
- Mirrors (Prowide, tools20022) show `BusinessDayConvention1Code` FWNG/PREC and `BusinessDayConventionCode` FWNG/MODF/PREC/NEAR [S].
- No calendar-naming code set was found [I, mirror only].

## ISO 10383 MIC
https://www.iso20022.org/market-identifier-codes (HTTP 200). Latest list 2026-11-09, effective 2026-11-23. Registration Authority: SWIFT [F].
- The CSV/XSD fields have **no calendar, holiday, trading-hours or time-zone field** [F].
- FpML derives exchange calendar codes from MIC acronyms or codes ("it would be the acronym of the MIC…") [F]. That is a naming rule, not a mapping table [I].
- The ISO 10383:2012 standard text itself is paid (unreachable).

## SDMX 3.1 (March 2025)
- The Advanced Release Calendar was removed in 3.0 (change histories) [F]. No `ReleaseCalendar` in the 3.1 XSDs [F].
- The legacy construct had periodicity, offset and tolerance, but no business-day adjustment [F doc text].

## Agent's verdict
- Business-day adjustment **is** defined by open standards: FpML, CDM, FIX, ACTUS, and ISO 20022 [S].
- A named business-calendar code list **exists**: FpML `businessCenterScheme` (genericode, versioned URI). CDM validates against it; FIX references it.
- No standard publishes the holiday dates; CDM explicitly delegates them to a data provider.
- MIC carries no calendar data.

**Coverage class for concern 4 with ODCS**: custom extension carrying standardised code values. Not native, and not a published ODCS extension [I].

**"None" areas**: ACTUS, MIC, ISO 20022 (mirror), SDMX 3.1, ODCS v3.2.0, plus RFC 5545/8984 and DCAT 3 from the first run.
