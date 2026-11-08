Follow-up brief on the topic "Binary Stream Read Behavior Foundations" (original brief:
briefs/Binary Stream Read Behavior Foundations.md; its rules and task boundary apply unchanged).
Prior reports: reports/Binary Stream Read Behavior Foundations.md and
reports/Binary Stream Read Behavior Foundations - transfer protocols.md (track 15: OpenDAL CONFIRMED).

User message, verbatim:

leave out The Fibre Channel, ATA over Ethernet and dm-multipath texts were unreachable: the real pyhsics layer is already abstracted away by any high level transport & file abstraction stack. so not worth digging further.
OpenDAL detailed read would be worth it.
Truncation or retry are two things: truncation is a real issue to solve at protocol or higher lever (were all bytes read), but retry is already a pattern how to solve any kind of interrupts or lower layer identified retriable errors. So its a mean, not a taxnomony. agree?

Proposal answered (assistant, summarized): a detailed OpenDAL read-path track recording, per item,
the observable behavior, where it is documented vs implemented, with verbatim evidence:
(1) read API / reader contract (range reads, short reads, end-of-data signalling, streaming);
(2) truncation detection (bytes received vs Content-Length / requested range; resulting ErrorKind);
(3) version consistency across a read (ETag/version/if-match on multi-part or resumed reads);
(4) retry inside reads (RetryLayer after partial IO: resume offset, version guard);
(5) how ErrorKind/ErrorStatus is applied on the read path (S3, one other backend, local fs).
Retry is treated as a means; retryability as an outcome attribute. FC/AoE/dm-multipath dropped.

User instruction, verbatim:

yes, start the OpenDAL track
