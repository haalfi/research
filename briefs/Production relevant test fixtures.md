# Research brief: Production-relevant test fixtures without production data

## Goal

Find out how others ensure that tests using entirely fictional data exercise the implementation logic and expose the defects that would otherwise only become apparent when processing real data.

Identify prior art: established methods, existing tools, documented engineering practices and empirical research. Look beyond work labelled “synthetic data”. The objective is to discover and assess existing solutions, not to invent a new methodology.

## Context

- A data platform ingests structured data from multiple external sources. Several sources describe the same entities, with different identifiers, coverage, attributes and reporting delays.
- Implementation logic includes ingestion, transformation, entity resolution, reconciliation, validation and incremental processing.
- Real data remains in a protected environment where tests can be executed. Only approved derived information may leave. Some data is confidential or personal; the rest is licensed reference data.
- Development and routine automated testing happen outside that environment.
- Existing hand-written fixtures are much simpler than real data, so passing tests provides limited confidence in implementation correctness on real inputs.
- The objective is correctness and defect detection, not statistical resemblance or performance benchmarking.

## Research questions

1. **Prior art:** Who has addressed this problem before, under what terminology, and with what results? Which approaches are established in practice, experimentally demonstrated or still research proposals?
2. **Test adequacy:** How do others determine whether fictional fixtures exercise the relevant implementation logic and expose meaningful defects? How do they distinguish inadequate inputs, inadequate assertions and incorrect implementations, including tests that pass vacuously?
3. **Learning from real executions:** How have others used observations of real data or production executions to construct, select or improve fictional test inputs without transferring original records? What information must be captured, and can it substitute for explicit statistical characterisation?
4. **Automated generation:** Which existing methods generate inputs that expose implementation defects? How well do they handle relational and multi-source data, ambiguous identities, conflicts, missing records, temporal dependencies and delivery sequences? What domain knowledge and instrumentation do they require?
5. **Independent evaluation:** How is fixture effectiveness demonstrated beyond the criteria used to generate it? What evidence exists for detection of actual and previously unseen defects? What can and cannot be established about equivalence to real inputs?
6. **Fixture minimisation:** How do others reduce complex datasets and event sequences to small, understandable regression fixtures while retaining their defect-detection capability?
7. **Evolution:** How do teams discover gaps in existing fixtures as real data and implementation logic change, automate fixture renewal and preserve reproducibility of historical failures?
8. **Disclosure:** What information do production-derived test artefacts reveal, including through repeated or interactive releases? Which established methods bound disclosure? How do licensed reference data restrictions differ from privacy constraints?
9. **Alternatives:** How do others achieve comparable confidence in implementation correctness without generating production-relevant fixtures? When are these approaches preferable?

## Search scope

Search broadly across software testing, test adequacy, automated test-input generation, database application testing, data-intensive software testing, production-derived testing, program analysis, verification, failure reproduction and privacy-preserving testing. Follow citation chains and terminology discovered during the research. Do not assume any particular generation or testing technique is the preferred solution.

## Bring back

- **Prior-art catalogue:** For each relevant approach, identify the original problem, methodology, documented applications, empirical results, limitations and relevance to our constraints. Distinguish directly comparable solutions from neighbouring techniques whose applicability is only inferred.
- **Open-source tools:** Capabilities, maintenance state, licensing, support for relational and stateful inputs, required domain knowledge and instrumentation, computational costs, where real rows are needed and what must leave the protected environment.
- **Comparative assessment:** Maturity, evidence of real defect detection, suitability for complex structured inputs, disclosure implications and maintenance burden. Include unsuccessful approaches where documented.
- **Short synthesis:** Has this problem already been addressed, under what terminology, and what are the closest existing solutions? What can be adopted directly, what requires adaptation, and what genuinely remains unresolved? Distinguish absence of evidence from evidence that a problem is unsolved.
- **Dated sources:** Prioritise original research, systematic reviews, documented engineering case studies, official documentation and repositories. Clearly distinguish theoretical results, empirical findings, documented practices, engineering inferences and unverified vendor claims.

## Out of scope

- Designing new architectures, methodologies or algorithms.
- Commercial products, except as references for established capabilities.
- Unstructured data generation or training ML models on synthetic data.
- Statistical resemblance as an objective in itself, and full-scale performance benchmarking.
- Exporting real rows or unapproved derived information.
