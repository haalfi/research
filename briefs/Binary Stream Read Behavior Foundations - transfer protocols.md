Follow-up brief on the topic "Binary Stream Read Behavior Foundations" (original brief:
briefs/Binary Stream Read Behavior Foundations.md; its rules, scope and task boundary apply unchanged).

User question, verbatim:

why are (S)FTP and similiar not covered in B.7 Network and object-storage read protocols?

Proposal answered (assistant, summarized): run a follow-up track on file-transfer and remote-access
protocols (FTP, FTPS, SFTP, SCP, WebDAV, rsync and similar) under a new title on the same branch,
same method (full texts, 3-lens verification, medium-effort subagents), and record the coverage gap
of the earlier report; optionally include block-level protocols (NBD, NVMe-oF, Fibre Channel).

User instruction, verbatim:

yes, run it including block-level protocols

---

Addendum (track 15). User question, verbatim:

btw: why did openDAL not appear? it is a well known solution of the transport part and has its well founded taxonomy at least for that

User instruction on the assistant's first proposal (a track on storage abstraction layers), verbatim:

good idea, but it should search & confirm, that they have build, defined, and well documented taxonomy on which each founds it product/solution. The focus is in that and NOT in another "are the storage abstractions" out there. Got the point? Re propose

Revised proposal answered (assistant, summarized): per candidate, test whether a taxonomy of storage
access/read behavior is (1) defined, (2) principled, (3) foundational (backends must map onto it,
visible in code), (4) maintained; verdict CONFIRMED / PARTIAL / NOT FOUND with verbatim evidence;
extract the taxonomy for CONFIRMED/PARTIAL and relate it to the prior report's classifications.
Full depth: OpenDAL, Hadoop FileSystem specification, Arrow object_store, fsspec; others screened
only for taxonomy evidence, one line each. 3-lens verification; overreach lens guards against
"an enum exists" being upgraded to "a well-founded taxonomy".

User instruction, verbatim:

yes, start track 15
