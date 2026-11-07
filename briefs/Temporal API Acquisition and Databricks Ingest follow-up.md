# Follow-up brief: Temporal API Acquisition and Databricks Ingest

User instruction (2026-11-07), verbatim: "Go with the short pass only"

## Scope

The user accepted this scope, which the assistant proposed after the first report:

1. **Long-running vendor jobs (assumption A3).** How does Temporal model them? Look at durable timers
   and the polling patterns Temporal documents.
2. **Detecting late or missing runs on the Temporal side.** Read Temporal's troubleshooting page on
   missed schedule actions.
3. **Replaying files in Auto Loader (assumption A8).** What do the Databricks knowledge base and
   release notes say?
4. **Three conflicts between Databricks pages (assumption A6):**
   - Do file-arrival triggers require file events, or only recommend them?
   - What is the default for `useManagedFileEvents`?
   - What is the default task retry count?

Out of scope: testing in a workspace, comparing operating effort, joint integration patterns,
ingestion byte volumes.
