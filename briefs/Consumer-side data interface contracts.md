# Consumer-side contracts for external data interfaces: which open formats, together

## Goal

Find the smallest set of existing open standards that together express a consumer-side contract for an external data interface, so nothing we need is invented. ODCS v3 is the baseline: what to combine it with for what it doesn't model, and what then stays custom. Don't limit the search to data-contract standards.

"Smallest", in this order: native, schema-validated semantics over extensions; then the fewest custom semantics, overlapping models and integration complexity; only last the number of standards.

Research cutoff: 19 November 2026; "current" means as of that date.

## Context

- We consume data from systems we don't control: HTTP request/response APIs, SFTP file drops, files a third party writes into an object-storage bucket we read, a SQL query interface, and our own database's change log.
- Per interface we write a one-sided contract: how it behaves and what we rely on; the provider never sees it. YAML in git, semver-versioned, reviewed in pull requests; our Python pipelines run checks derived from it.
- Dataset shape is written as ODCS v3, a data product as ODPS. Contracts exchanged inside the organisation use ODCS/ODPS, so any addition must compose with them.
- In a prototype, ODCS-native fields held the dataset fields, the server and one row rule. Everything below went into `customProperties`, unvalidated.

## Concerns ODCS didn't hold in the prototype

1. A contract version's valid period and knowledge time (bitemporal versions)
2. Transport-level integrity checks (sizes, digests, a provider's file catalogue) and the provider's deviations from them
3. Requests and schedules: what we ask for, when, and the tolerance on timing
4. Offer cadence and deadline: which deliveries we expect and by when, following a business or market calendar
5. Retry limits
6. What identifies one delivery, what counts as a new sighting of it, and whether different bytes under the same identity are a new revision or refused
7. Which response or file metadata gives the provider's publication time and revision order
8. Which received metadata is redacted before it is kept
9. Delivery shape: the datasets and files one delivery carries, the file dialect (delimiter, header, trailer with a record count), the population a delivery states whole, and the tokens for "absent" versus "explicitly empty"
10. Per quality rule: a service level (indicator, objective, consequence) and a failure class finer than severity (our fault, the provider's fault, an expected absence)
11. Execution evidence: what one run actually read, under which contract versions. A record of what happened, referencing the contract, not part of it

Coverage classes:
- **Native:** the standard defines the semantics and their validation structure.
- **Standardised extension:** a separately published, reusable specification defines them.
- **Custom extension:** the standard admits arbitrary fields; their meaning and schema are ours to define.
- **None:** no suitable modelling or extension mechanism found.

## Questions

1. Per concern, which open standards model it, and in which coverage class?
2. Does the current ODCS release, or anything changed since v3.1.0, natively cover a concern the prototype put in `customProperties`?
3. Per concern, does it belong in the static contract, a separate referenced specification, or an execution-time evidence record?
4. Can the recommended standards form a coherent set of git-versioned YAML documents, each validated against its own published schema, with explicit cross-document ids and version references and one owner per concern? Where is custom glue unavoidable?
5. Are there published examples of consumer-side contracts for third-party feeds that combine standards this way?

## Bring back

- A matrix of concerns × standards in the four coverage classes, each cell linked to the spec section behind it. For a "none": the spec areas examined and why it is absent; silence is not a prohibition.
- Per standard: version, publication and access date, governance, release cadence, validator tooling (Python preferred), evidence of adoption.
- A recommended minimal set, what stays custom under it, and why.
- A small conceptual composition example: document boundaries, ids, version references, and which published schema validates which part. Explanatory, not an implementation.
- Each claim labelled first-hand (spec text read) or secondary; examples and third-party documentation are secondary unless the standard's maintainers publish them.

## Out of scope

Proprietary formats of commercial data-contract or catalogue products without an open spec; implementation; choosing a storage or orchestration stack.
