# Research brief: synthetic test data that stands in for real data

## Goal

Find out how others build test data that behaves like the real data without containing any of it,
and how they keep it trustworthy as the real data changes. The stand-in should keep whatever about
the real data decides how the platform behaves: its correctness, its failures and its performance.
We want established methods and tools to adapt, with their trade-offs, so we choose rather than
invent. Look beyond work labelled "synthetic data": neighbouring fields may use other terms.

## Context

- A data platform takes in structured data from many external sources. Several sources describe
  the same real-world entities, each with its own identifiers, coverage and delays.
- The real data stays in one protected environment. Only derived information computed inside it,
  such as aggregates, may leave. Development and testing happen outside it.
- Some of the data is confidential or personal. The rest is reference data that is licensed.
- Today's test data is hand-written and far simpler than the real data, so tests on it say little
  about correctness or performance on the real data.

## Questions

1. Which characteristics of the real data must be captured, and which are hard to capture or
   reproduce? Read "characteristics" broadly, well beyond schema. Examples, not a complete list:
   distributions, relationships within and across sources, change over time, how data arrives,
   what shapes performance.
2. Which established methods produce realistic stand-in data, whether generated from a
   characterisation or derived from the real rows inside the protected environment, including
   links between tables and the same entity across sources?
3. How is usefulness demonstrated beyond matching the characterisation the data was generated from?
   Examples: running the same workload inside the protected environment and comparing results.
4. What does a characterisation or derived data disclose, including across repeated releases, and
   which techniques bound that disclosure? Is licensed reference data a separate constraint?
5. How do generators serve different needs from one characterisation: small sets that
   over-represent rare and edge cases, and large sets at real distributions for performance work?
6. How is data that changes over time reproduced: daily churn, corrections, re-deliveries, gaps?
7. How do teams notice that the real data has drifted from the stand-in, and how do they renew it
   automatically while keeping an earlier failing test reproducible?
8. Data validation and drift detection also describe "what is normal". Can they share a foundation
   with generation, given that normal in production is not always correct?
9. Which practices from testing apply: generated data that carries its expected outcome,
   property-based and metamorphic testing, fuzzing of delivery formats?

## Bring back

- Per question: the established methods and the mature open-source tools. For each, give its
  maintenance state, where it needs real rows and what would have to leave the protected
  environment, and why it fits or does not fit the constraints above.
- Fields we may have missed, such as official statistics, microsimulation, database benchmarking,
  query-optimiser statistics or healthcare data.
- A short synthesis: which pieces exist off the shelf, which would need building, and the open trade-offs.
- Sources with dates. Mark what is documented, what is inferred and what is vendor marketing.

## Out of scope

- Commercial products, except as a reference for which capabilities exist.
- Generating unstructured data such as text, images or documents.
- Training ML models on synthetic data.
