# Research brief: Stand in test data cross check

Follow-up on the topic of `briefs/Synthetic stand in test data.md` and `briefs/Production relevant test fixtures.md`.
Input: an external report on the first brief, produced independently by another system and supplied by the user,
saved verbatim and unverified at `research_notes/Stand in test data cross check/external_report_unverified.md`.

Brief as proposed and approved by the user ("go ahead with the full cross check run"):

One follow-up run on this branch, under a new title such as `Stand in test data cross check`, with four tracks:

1. **Precedents:** Lu, Miklau & Gupta 2011 and what cites it; the NHS artificial data pilot via the repo or another route.
2. **Temporal and delivery test harnesses:** TestStream, Flink DataGen and SimPy, plus testing incremental results against a full recompute. Enzyme and pg_trickle are already leads in our notes.
3. **Overlap and margin theory:** Fréchet and Dobra–Fienberg bounds for what released overlap counts imply and disclose; DPSynth and the JMLR 2026 paper.
4. **Non-circular evaluation:** precedents for time-split, out-of-window validation of synthetic test data and fixtures.

The report would give verdicts on the other report's unique claims and record the corrections above. It would not repeat either earlier run, and both earlier reports stay untouched. I'd also save the other report verbatim under that run's notes folder, marked as unverified external input, so its provenance can be diffed.

## Corrections referred to above (from the documented notes of the earlier runs)

- dbldatagen is called an open-source candidate. It is under the Databricks License, which is not OSI-approved.
- Maintenance: sdcMicro, ARX and Anonymeter are called "uncertain", but there are dated releases: 5.8.2 in June 2026, 3.9.2 in September 2025 and 1.1.0 in July 2026. TAPAS is dormant since 2023.
- Touchstone and MyBenchmark are called established. Touchstone has been dormant since 2020, and no code was found for MyBenchmark.
- It misses: Private-PGM/`mbi`; DBRepro and Mirage; Simulacrum and OpenSAFELY; Statistics Netherlands' term "simulated data"; transport of optimiser statistics in PostgreSQL 18 and 19; the limits of the free SDV edition; the Census reconstruction result.
