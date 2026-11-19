# Track 3 (verification run): B8 OCFL and BagIt; B9 trailers and control totals

Produced by a delegated research agent on 2026-11-19, with spot-checks by the main session (below).
Labels are the agent's unless marked "(spot-check)".
Downloads and tests are in the session scratchpad `b8/`.

**Concern mapping fixed.** The agent guessed the numbering wrongly. In the brief:
- concern 2 = transport integrity (sizes, digests, catalogue) = fixity;
- concern 6 = delivery identity, sighting, revision vs refusal;
- concern 9 = delivery shape (incl. trailer).

The tables below use the brief's numbering.

## Spot-checks (main session) [F]
Grepped in the agent's downloaded texts:
- OCFL `spec.txt` l.284: "The specification takes no position on what [constitutes a version]".
- OCFL l.960: BagIt "[does not provide a mechanism] for content versioning".
- RFC 8493 l.545: "Payload-Oxum: The 'octetstream sum' of the payload".
- GFD.240 header: "GFD-R-P.240 … February 2021 … Updated June 2023".
- GFD.240 l.2094: "The dfdl:assert checks are performed even when validation is off".
- GFD.240 l.9979: "fn:count($arg) Returns the number of items in the value of $arg as an xs:integer".
- BagIt Profiles: "allow creators and consumers of Bags to agree on optional components".

All agree with the agent's report.

## OCFL 1.1 (v1.1.1: 2022-10-07, updated 2024-11-07; CC-BY 4.0; v2 not released)
Read: https://ocfl.io/1.1/spec/, implementation notes, `inventory_schema.json`, validation codes.

- **Identity** [F]. §3.5.1: `id` "MUST be unique in the local context, MUST NOT change between versions … SHOULD be a URI".
- **Versions** [F]:
  - §3.3: a continuous v1…vN sequence; "Once created, the contents of a version directory are expected to be immutable".
  - `head` is the highest version.
  - §3.4: content is addressed by sha512 or sha256.
- **No rule for when a new version is made** [F]: "takes no position on what constitutes a version or a versionable action"; "remains silent on when versioning should occur".
- **No "refuse" outcome** [F]. Purge is not supported; "create a new object" instead.
- **Fixity** [F]: the `manifest` is mandatory; the `fixity` block is optional (md5, sha1, sha256, sha512, blake2b-512); the inventory sidecar digest is required.
- **Character**: describes storage at rest, not transfer [F/I].
- **Tooling**:
  - Inventory JSON Schema draft-07, `additionalProperties:false`, labelled non-normative [F].
  - `ocfl-py` 2.1.0 (PyPI, 2026-06-26) [F PyPI].

## BagIt (RFC 8493, Oct 2018; Independent Submission, Informational, not Standards Track)
Read: https://www.rfc-editor.org/rfc/rfc8493.txt.

- **Identity** [F]: all `bag-info.txt` elements are OPTIONAL.
  - `External-Identifier`: "A sender-supplied identifier for the bag". No uniqueness requirement.
  - `Bag-Group-Identifier`: SHOULD be unique across the sender's content.
  - `Bag-Count` ("N of T"), `Bagging-Date`, `Internal-Sender-Identifier`.
- **Versioning**: none [F].
- **Fixity** [F]:
  - §2.1.3: at least one payload manifest that lists every payload file exactly once.
  - §2.4: tools MUST support SHA-256 and SHA-512.
  - §3: a valid bag means every checksum verified.
  - `Payload-Oxum` "OctetCount.StreamCount" is "strictly an optimization".
  - `fetch.txt` allows holey bags whose payload is fetched from URLs.
- **Consumer-side layer**: BagIt Profiles Specification 1.4.0 (2023-01-13, CC0) [F].
  - A JSON profile at a URI. Consumers "validate incoming Bags against it".
  - It can require bag-info tags and their values, `Manifests-Required`, `Allow-Fetch.txt`, and so on.
  - It has no revision-policy fields [F/I].
- **Tooling**:
  - `bagit` 1.9.0 (2025-06-13) [F PyPI].
  - `bagit-profile` 1.3.1 (2020-03-24), which may lag spec 1.4.0 [F PyPI / I].

## B8 verdict
- **Revision policy** ("different bytes under the same identity = new version or refused"): **none** as a declarable rule in OCFL or BagIt.
  - OCFL has the mechanism (stable `id`, immutable versions) but explicitly no policy.
  - BagIt has no versioning.
- **Delivery identity**: BagIt `External-Identifier` / `Bag-Group-Identifier` + `Bag-Count`. These are mandatory only if a consumer-published BagIt Profile requires them, and only if the provider ships bags.
- **Fixity**: native and strong in both formats. BagIt + Profile is aimed at transfer.

## DFDL 1.0 (OGF GFD-R-P.240, Feb 2021, updated June 2023; "Distribution is unlimited")
Read: https://ogf.org/documents/GFD.240.pdf §1.3, §7.5, §16.1, §17, §18 and function tables.

- A declarative description of text, binary and legacy formats as an XSD extension [F].
- A trailer is an ordinary final element; there is no "trailer" keyword [F/I].
- `dfdl:assert` raises a Processing Error and runs even when validation is off (§7.5) [F].
- `fn:count` exists (table 63) [F].
- `occursCountKind='expression'` reads N from a header field (§16.1) [F].
- **There is no `fn:sum`** [F]. Control sums are possible via `dfdl:inputValueCalc` running totals (§17) [F + test].
- **Agent's test** with Apache Daffodil 4.2.0 (release 2026-07-07, sha512-verified binary, Java 21):
  - The count assert rejects trailer 3 against 2 records.
  - `fn:sum` gives "Unsupported function".
  - A running-total assert rejects 15.49 against 15.50 [F, agent's own test].
- **Tooling**: Daffodil (JVM) and IBM App Connect Enterprise. **No Python DFDL processor**; from Python, call the CLI or use a JVM bridge [F PyPI / I].
- **Community schemas** (DFDLSchemas NACHA 2020, EDIFACT 2023) parse the trailer fields but never check them (no `count(`) [F].

## Fixed domain formats with trailers (not description languages)
- **NACHA ACH**:
  - File Control "9" carries entry/addenda count, entry hash and debit/credit totals [F, free developer guide].
  - The normative Operating Rules are paid (unread).
- **BAI2 v2** (10/2005, © BAI, free PDF):
  - 49 / 98 / 99 trailers with control totals and record counts, e.g. "File Control Total … Algebraic sum of all group control totals" [F].
- **UN/EDIFACT**: UNT E0074 segment count, UNZ E0036 interchange count [S, from the DFDL schema; UNECE returned 403].
- **ASC X12**: SE01 / IEA01. Copyrighted and licensed; not read [S].
- **ISO 20022 pain.001**: GroupHeader `NbOfTxs` (required) and `CtrlSum` (optional). These are header totals; the XSD cannot enforce that they match [S, mirrored XSD; iso20022.org 403].
- **RFC 4180 CSV**: only an "optional header line" [F].
- **Kaitai Struct** (open-source project, not a standards body): `valid: {expr}` halts parsing [F docs]. A trailer check is plausible but untested [I].

## B9 verdict
- Open specifications that declare trailers with counts and totals exist, but they are **fixed domain formats**.
- **DFDL 1.0 is the only open, standards-body description language found** that can declare a trailer and assert count = number of records. Control sums work via running totals.
- From ODCS it can only be referenced:
  - quality `type: custom` with `engine` (free string; examples soda / great-expectations / monte-carlo / dbt) and `implementation` = DFDL schema URL; or
  - `authoritativeDefinitions` [F schema].
- ODCS `rowCount` compares against fixed operator values and cannot read a trailer value [F].

## Coverage-class effect (brief numbering)
| Concern | Effect | Basis |
|---|---|---|
| 2: sizes, digests, provider catalogue | Unchanged for loose SFTP/object files (custom). New **standardised extension** where the provider ships BagIt bags: manifests, Payload-Oxum, fetch.txt, plus a consumer BagIt Profile. | RFC 8493 §2.1.3, §2.4, §3; Profiles 1.4.0 |
| 6: identity | **Standardised extension** only for BagIt deliveries with a Profile requiring `External-Identifier`; otherwise custom. | RFC 8493 §2.2.2 |
| 6: revision vs refusal | **None**, confirmed. Examined: OCFL 1.1 spec and notes, RFC 8493, BagIt Profiles 1.4.0, ODCS 3.2.0. | as above |
| 9: trailer / record count / control total | **None → standardised extension by reference** (a DFDL 1.0 schema with `dfdl:assert`, referenced from ODCS custom quality). The engine name is our convention. JVM-only tooling. | GFD.240 §7.5, §16.1, table 63 |
