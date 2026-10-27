# D-b: EU record-keeping, retention and ICT-logging duties reaching a Swiss regulated asset manager (data-platform operational records)

Not legal advice. These are research notes for a report writer. Grades used:
- **documented**: primary legal text, quoted, with article and act date.
- **documented guidance**: ESA or Commission Q&A or guidelines, with date.
- **secondary**: law-firm, industry or regulator summaries. Treat as leads.
- **inferred**: my reasoning. Labelled as inference.

**Source access and versions (read this first)**
- eur-lex.europa.eu returned HTTP 202 with an empty body (a bot challenge) to curl and to WebFetch. EUR-Lex HTML pages were therefore **unreachable** from this container.
- The same texts were retrieved from the EU Publications Office Cellar, which serves the official OJ text, by CELEX number: `https://publications.europa.eu/resource/celex/<CELEX>`.
- These are the **original OJ versions as adopted, not consolidated versions**. I could not retrieve consolidated versions with consolidation dates. Later amendments to the quoted paragraphs were not checked, except where an amending act was fetched separately: IFR 2019/2033 (for MiFIR Art 46) and Directive (EU) 2024/927 (for AIFMD/UCITS delegation).
- The report must state that every quote below is "as originally adopted". The consolidated text should be checked by compliance (see D3).

Acts retrieved, all in full text (CELEX → Cellar URL; canonical EUR-Lex URL in brackets):

| Short name | Act (date of adoption) | CELEX | Source |
|---|---|---|---|
| MiFID II | Directive 2014/65/EU of 15 May 2014 | 32014L0065 | [Cellar](https://publications.europa.eu/resource/celex/32014L0065) ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014L0065)) |
| MiFID Org Reg | Commission Delegated Regulation (EU) 2017/565 of 25 April 2016 | 32017R0565 | [Cellar](https://publications.europa.eu/resource/celex/32017R0565) |
| MiFIR | Regulation (EU) No 600/2014 of 15 May 2014 | 32014R0600 | [Cellar](https://publications.europa.eu/resource/celex/32014R0600) |
| IFR | Regulation (EU) 2019/2033 of 27 November 2019 (amends MiFIR Art 46) | 32019R2033 | [Cellar](https://publications.europa.eu/resource/celex/32019R2033) |
| DORA | Regulation (EU) 2022/2554 of 14 December 2022, OJ L 333, 27.12.2022 | 32022R2554 | [Cellar](https://publications.europa.eu/resource/celex/32022R2554) |
| DORA RTS RMF | Commission Delegated Regulation (EU) 2024/1774 of 13 March 2024 | 32024R1774 | [Cellar](https://publications.europa.eu/resource/celex/32024R1774) |
| DORA RTS ICT policy (Art 28(10)) | Commission Delegated Regulation (EU) 2024/1773 of 13 March 2024 | 32024R1773 | [Cellar](https://publications.europa.eu/resource/celex/32024R1773) |
| DORA ITS Register | Commission Implementing Regulation (EU) 2024/2956 of 29 November 2024 | 32024R2956 | [Cellar](https://publications.europa.eu/resource/celex/32024R2956) |
| UCITS | Directive 2009/65/EC of 13 July 2009 | 32009L0065 | [Cellar](https://publications.europa.eu/resource/celex/32009L0065) |
| UCITS L2 | Commission Directive 2010/43/EU of 1 July 2010 | 32010L0043 | [Cellar](https://publications.europa.eu/resource/celex/32010L0043) |
| AIFMD | Directive 2011/61/EU of 8 June 2011 | 32011L0061 | [Cellar](https://publications.europa.eu/resource/celex/32011L0061) |
| AIFMD L2 | Commission Delegated Regulation (EU) No 231/2013 of 19 December 2012 | 32013R0231 | [Cellar](https://publications.europa.eu/resource/celex/32013R0231) |
| AIFMD II | Directive (EU) 2024/927 of 13 March 2024 | 32024L0927 | [Cellar](https://publications.europa.eu/resource/celex/32024L0927) |
| GDPR | Regulation (EU) 2016/679 of 27 April 2016 | 32016R0679 | [Cellar](https://publications.europa.eu/resource/celex/32016R0679) |

---

## Q1. When do these EU rules reach a Swiss (third-country) asset manager?

### Takeaway
EU rules bind the Swiss firm **directly** in two cases. The first is an EU-authorised entity: a subsidiary authorised as a MiFID investment firm, a UCITS ManCo or an AIFM, which is also a DORA "financial entity". The second is an EU branch, which under MiFID II Art 41(2) must apply Art 16. Under a MiFIR Art 46 registration, only limited record duties attach, such as Art 46(6b), keeping 5 years of order and transaction data at ESMA's disposal.

In a **delegation** from an EU ManCo/AIFM, the duties stay with the EU manager. They reach the Swiss delegate only **contractually**, through information, access, inspection and instruction rights.

DORA reaches the Swiss firm only as a contractual counterparty, an "ICT third-party service provider". Under the Commission's Q&A, a regulated financial service such as delegated portfolio management is predominantly a financial service and not an ICT service. A **standalone** ICT or data service, for example running the data platform for an EU entity, is an ICT service.

### Cited Findings

**(a) EU-authorised subsidiary: MiFID investment firm, UCITS ManCo, AIFM**
- documented, DORA scope. DORA Art 2(1) lists "(e) investment firms; … (k) managers of alternative investment funds; (l) management companies". Art 2(2): "entities referred to in paragraph 1, points (a) to (t), shall collectively be referred to as 'financial entities'". — [DORA, Reg (EU) 2022/2554 of 14.12.2022](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA exclusion. DORA Art 2(3): "This Regulation does not apply to: (a) managers of alternative investment funds as referred to in Article 3(2) of Directive 2011/61/EU", i.e. sub-threshold AIFMs. — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA application date. DORA Art 64: "It shall apply from 17 January 2025." — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, simplified framework scope. DORA Art 16(1): "Articles 5 to 15 of this Regulation shall not apply to small and non-interconnected investment firms, payment institutions exempted …; … electronic money institutions exempted …; and small institutions for occupational retirement provision."
  - ManCos and AIFMs are **not** in this list.
  - Entities in the list must still "put in place and maintain a sound and documented ICT risk management framework …" and "(b) continuously monitor the security and functioning of all ICT systems". — [DORA](https://publications.europa.eu/resource/celex/32022R2554)

**(b) EU branch of the Swiss firm (MiFID II Art 39 national branch regime)**
- documented. MiFID II Art 39(1): "A Member State may require that a third-country firm intending to provide investment services … to retail clients or to professional clients … in its territory establish a branch in that Member State." — [MiFID II, Dir 2014/65/EU of 15.5.2014](https://publications.europa.eu/resource/celex/32014L0065)
- documented. MiFID II Art 41(2): "The branch of the third-country firm authorised in accordance with paragraph 1, shall comply with the obligations laid down in Articles 16 to 20, 23, 24, 25 and 27, Article 28(1), and Articles 30, 31 and 32 of this Directive and in Articles 3 to 26 of Regulation (EU) No 600/2014 and the measures adopted pursuant thereto …". So Art 16(6)/(7), Delegated Reg 2017/565 Art 72–76 and MiFIR Art 25 apply to the branch. — [MiFID II](https://publications.europa.eu/resource/celex/32014L0065)

**(c) Cross-border services without a branch (MiFIR Art 46–47)**
- documented. MiFIR Art 46(1): "A third-country firm may provide investment services … to eligible counterparties and to professional clients … without the establishment of a branch where it is registered in the register of third-country firms kept by ESMA in accordance with Article 47." — [MiFIR, Reg (EU) No 600/2014](https://publications.europa.eu/resource/celex/32014R0600)
- documented. Under Art 46(4), registration presupposes a Commission equivalence decision under Art 47(1). — [MiFIR](https://publications.europa.eu/resource/celex/32014R0600)
- documented. MiFIR Art 46(3): "Member States shall not impose any additional requirements on the third-country firm in respect of matters covered by this Regulation or by Directive 2014/65/EU". — [MiFIR](https://publications.europa.eu/resource/celex/32014R0600)
- documented, record duty inserted by the IFR. New MiFIR Art 46(6b): "Where a third-country firm provides services or performs activities in accordance with this Article, it shall keep, at the disposal of ESMA, the data relating to all orders and all transactions in the Union in financial instruments which they have carried out, whether on own account or on behalf of a client, for a period of five years." — [IFR, Reg (EU) 2019/2033 of 27.11.2019, amending Art 46 MiFIR](https://publications.europa.eu/resource/celex/32019R2033)
- documented. IFR also inserted Art 46(6a), an annual report to ESMA on the scale and scope of services and on risk-management and governance arrangements. — [IFR](https://publications.europa.eu/resource/celex/32019R2033)
- Gap: whether any Art 47 decision exists for Switzerland. I found no authoritative list. Searches surfaced only Swiss *trading-venue* equivalence under MiFIR Art 23, which is a different regime. — [secondary: ESMA ISRR page Art 47](https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifir/article-47-equivalence-decision)

**(d) Delegation or sub-delegation of portfolio management to a Swiss manager**
- documented, UCITS. UCITS Art 13(1)(d): "where the mandate concerns the investment management and is given to a third-country undertaking, cooperation between the supervisory authorities concerned must be ensured". — [UCITS Dir 2009/65/EC of 13.7.2009](https://publications.europa.eu/resource/celex/32009L0065)
- documented, AIFMD. AIFMD Art 20(1)(c): the delegation "must be conferred only on undertakings which are authorised or registered for the purpose of asset management and subject to supervision". Art 20(1)(d): "where the delegation concerns portfolio management or risk management and is conferred on a third-country undertaking, … cooperation between the competent authorities … must be ensured". Art 20(1)(f): the AIFM must be able "to monitor effectively at any time the delegated activity, to give at any time further instructions to the delegate and to withdraw the delegation with immediate effect". — [AIFMD Dir 2011/61/EU of 8.6.2011](https://publications.europa.eu/resource/celex/32011L0061)
- documented, contractual flow-down (AIFMD L2). Delegated Reg 231/2013 Art 75:
  - "(f) … The AIFM shall set out in the agreement its right of information, inspection, admittance and access, and its instruction and monitoring rights against the delegate."
  - "(h) … the AIFM shall contractually ensure its instruction and termination rights, its rights of information, and its right to inspections and access to books and premises. The agreement shall make sure that sub-delegation can take place only with the consent of the AIFM".
  - Under Art 79(b), effective supervision is deemed impeded where "the delegate does not cooperate with the competent authorities of the AIFM in connection with the delegated functions". — [Reg (EU) 231/2013 of 19.12.2012](https://publications.europa.eu/resource/celex/32013R0231)
- documented, AIFMD II amendment. Art 20(3) as replaced: "The AIFM's liability towards its clients, the AIF and its investors shall not be affected by the fact that the AIFM has delegated functions or services to a third party, or by any further sub-delegation. The AIFM shall not delegate … to the extent that it becomes a letter-box entity." Transposition, Art 3(1): "by 16 April 2026 … They shall apply those measures from 16 April 2026", except some measures from 16 April 2027. The directive also adds delegation information to the authorisation file. This is now in force (today 2026-10-27), subject to national transposition. — [Directive (EU) 2024/927 of 13.3.2024](https://publications.europa.eu/resource/celex/32024L0927)
- documented, MiFID outsourcing of portfolio management to a third country. Delegated Reg 2017/565 Art 32(1): where an investment firm "outsources functions related to the investment service of portfolio management provided to clients to a service provider located in a third country", then "(a) the service provider is authorised or registered in its home country to provide that service and is effectively supervised by a competent authority in that third country; (b) there is an appropriate cooperation agreement …". — [Reg (EU) 2017/565 of 25.4.2016](https://publications.europa.eu/resource/celex/32017R0565)

**(e) DORA via EU financial entities, from the ICT third-party service provider angle**
- documented. DORA Art 3(21): "'ICT services' means digital and data services provided through ICT systems to one or more internal or external users on an ongoing basis …". Art 3(19): "'ICT third-party service provider' means an undertaking providing ICT services". — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented. DORA Art 28(1)(a): financial entities using ICT services "shall, at all times, remain fully responsible for compliance with, and the discharge of, all obligations under this Regulation and applicable financial services law". Art 28(3): they "shall maintain and update at entity level, and at sub-consolidated and consolidated levels, a register of information in relation to all contractual arrangements on the use of ICT services provided by ICT third-party service providers". — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented guidance. Q&A DORA030 (ID 2999), answered by the European Commission, page showing submission date 14 Feb 2024 (answer date not shown on page). It sets two tests: whether the "providing financial entities and the financial services they provide are regulated under Union law … or of a third country". "In case both tests are positive, then the related ICT service should be considered to predominantly be a financial service". Otherwise, or for standalone services, "the service should be considered as an ICT service under Article 3(21) DORA". — [EIOPA Q&A DORA030-2999](https://www.eiopa.europa.eu/qa-regulation/questions-and-answers-database/dora030-2999_pt)
- secondary: commentary dated Jan 2025 on the Commission clarification. — [Regulation Tomorrow](https://www.regulationtomorrow.com/2025/01/european-commission-clarifies-dora-definition-of-ict-services/); [Harneys](https://harneys.com/our-blogs/regulatory/esas-publish-guidance-on-the-definition-of-ict-services-under-dora). Also CSSF notice, Apr 2025: [CSSF](https://www.cssf.lu/en/2025/04/definition-of-ict-services-under-dora-new-forms-for-ict-third-party-arrangements-ict-outsourcing-arrangements/)

### Inferences
- **Inferred.** If the Swiss group has an EU subsidiary (IF/ManCo/full AIFM), that subsidiary carries the full DORA set: Art 6, 9, 10, 12, 17, 28–30 and RTS 2024/1774 Title II. The simplified Art 16 regime is available only if the subsidiary is a "small and non-interconnected investment firm". ManCos and AIFMs cannot use it.
- **Inferred.** If the EU subsidiary uses the Swiss parent's Postgres lake, Azure archive or Dagster platform, this is an intra-group ICT service. It belongs in the EU entity's register of information, and the Art 30 contractual terms apply to the Swiss parent as provider.
- **Inferred.** A pure delegated portfolio management mandate to the Swiss manager is likely "predominantly a financial service" under Q&A DORA030. DORA then does not apply to the mandate as such. The EU manager's UCITS/AIFMD record duties flow down through the delegation contract.
- **Inferred.** If the Swiss firm also supplies data or platform services to the EU manager standalone, for example feeding the ManCo's risk or valuation systems, those services are ICT services under Art 3(21). They pull in the Art 30 terms.
- **Inferred.** For a DORA-scope third-country **branch** of a Swiss investment firm, it is unclear whether DORA Art 2(1)(e) "investment firms" covers a third-country branch. DORA does not define it separately in the extracted text.

### Gaps
- No Swiss-specific Art 47 equivalence status found (unverified).
- National third-country regimes under MiFID II Art 46(4) / Art 39 and national private-placement regimes vary by Member State and were not researched. These include national record duties, such as German WpHG/BaFin practice. Unverified.
- Whether DORA applies to third-country branches: no primary or ESA text found in this run.

---

## Q2. Record class 1: records of data received from external vendors (what, when, from whom)

### Takeaway
No EU text names "vendor data receipts" as a record class. Several duties cover them:
- **MiFID/UCITS/AIFMD general "adequate and orderly records"**, with no period stated.
- **Reconstruction duties.** Records must let the authority "reconstitute each key stage of the processing of each transaction", with 5 years for UCITS/AIFM portfolio-transaction records and MiFIR Art 25.
- **DORA.** Data-transfer security, the register of information on the vendor *arrangement* (not each delivery), and logging of "ICT operations, including ICT system activities" with an entity-defined retention period.

Whether a delivery record must be kept 5 years depends on whether it forms part of a "key stage of the processing" of an order or transaction, or of a NAV or valuation. That is a compliance judgement.

### Cited Findings
- documented, MiFID organisational records (no period). 2017/565 Art 21(1)(f): investment firms shall "maintain adequate and orderly records of their business and internal organisation". Art 21(2): "establish, implement and maintain systems and procedures that are adequate to safeguard the security, integrity and confidentiality of information". — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented, MiFID II Art 16(6): "An investment firm shall arrange for records to be kept of all services, activities and transactions undertaken by it which shall be sufficient to enable the competent authority to fulfil its supervisory tasks … and in particular to ascertain that the investment firm has complied with all obligations …". **No retention period appears in Art 16(6) itself.** — [MiFID II](https://publications.europa.eu/resource/celex/32014L0065)
- documented. The "five years / up to seven years" wording in MiFID II is in the **last subparagraph of Art 16(7)**: "The records kept in accordance with this paragraph shall be provided to the client involved upon request and shall be kept for a period of five years and, where requested by the competent authority, for a period of up to seven years." This is scoped to telephone and electronic-communication recordings ("this paragraph"). — [MiFID II](https://publications.europa.eu/resource/celex/32014L0065)
- documented. A full-text search of 2017/565 (original text) finds "five years" only in Art 76(8) (recordings) and in unrelated disclosure provisions. **Art 72 sets no general period.** — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented, MiFIR Art 25(1): "Investment firms shall keep at the disposal of the competent authority, for five years, the relevant data relating to all orders and all transactions in financial instruments which they have carried out …". — [MiFIR](https://publications.europa.eu/resource/celex/32014R0600)
- documented, MiFID record form. 2017/565 Art 72(1): "The records shall be retained in a medium that allows the storage of information in a way accessible for future reference by the competent authority, and in such a form and manner that the following conditions are met:
  - (a) the competent authority is able to access them readily and to reconstitute each key stage of the processing of each transaction;
  - (b) it is possible for any corrections or other amendments, and the contents of the records prior to such corrections or amendments, to be easily ascertained;
  - (c) it is not possible for the records otherwise to be manipulated or altered;
  - (d) it allows IT or any other efficient exploitation when the analysis of the data cannot be easily carried out due to the volume and the nature of the data; and
  - (e) the firm's arrangements comply with the record keeping requirements irrespective of the technology used."

  Art 72(2): firms "shall keep at least the records identified in Annex I". Annex I is "without prejudice to any other record-keeping obligations arising from other legislation". Art 72(3), second subparagraph: "Competent authorities may require investment firms to keep additional records to the list identified in Annex I". — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented. Annex I ("Minimum list of records") covers client assessment, order handling, client orders and transactions (Art 74–75 / Annex IV), reporting to clients, client assets, communications and so on. **It contains no entry for market or reference data deliveries or for data-quality checks.** — [Reg (EU) 2017/565 Annex I](https://publications.europa.eu/resource/celex/32017R0565)
- documented, UCITS. 2010/43 Art 4(1)(e): management companies must "maintain adequate and orderly records of their business and internal organisation". Art 16(1): "Member States shall require management companies to ensure the retention of the records referred to in Articles 14 and 15 for a period of at least 5 years." Art 16(1), second subparagraph: authorities "may, in exceptional circumstances, require … a longer period". Art 14 covers portfolio transactions and Art 15 subscription and redemption orders. Art 16(3) has the same medium conditions (a)–(c) as MiFID 72(1)(a)–(c): "reconstitute each key stage of the processing of each portfolio transaction". — [Dir 2010/43/EU of 1.7.2010](https://publications.europa.eu/resource/celex/32010L0043)
- documented, AIFMD. 231/2013 Art 57(1): "maintain adequate and orderly records of their business and internal organisation". Art 66(1): "AIFMs shall ensure that all required records referred to in Articles 64 and 65 are retained for a period of at least five years", with authorities able to require longer. Art 66(3): records on a medium such that "(a) the competent authorities are able to access them readily and to reconstitute each key stage of the processing of each portfolio transaction; (b) corrections or other amendments, and the contents of the records prior to such corrections or amendments, may be easily ascertained; (c) no other manipulation or alteration is possible." — [Reg (EU) 231/2013](https://publications.europa.eu/resource/celex/32013R0231)
- documented, DORA data in transit. DORA Art 9(3): ICT solutions shall "(a) ensure the security of the means of transfer of data; (b) minimise the risk of corruption or loss of data …; (d) ensure that data is protected from risks arising from data management, including poor administration, processing-related risks and human error." — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA vendor arrangement. Art 28(3) requires a register of "all contractual arrangements on the use of ICT services". ITS 2024/2956 templates record start and end dates and termination reasons. — [DORA](https://publications.europa.eu/resource/celex/32022R2554); [ITS (EU) 2024/2956 of 29.11.2024](https://publications.europa.eu/resource/celex/32024R2956)
- documented, DORA logging (see Q5). RTS 2024/1774 Art 12(2)(c)(iv) requires logging of "ICT operations, including ICT system activities". — [RTS 2024/1774 of 13.3.2024](https://publications.europa.eu/resource/celex/32024R1774)

### Inferences
- **Inferred.** Data vendors such as market-data or reference-data feeds deliver "digital and data services … on an ongoing basis". They are likely ICT third-party service providers under DORA Art 3(21) and belong in the register. The register is at arrangement level, not delivery level.
- **Inferred.** A per-delivery receipt record (manifest: what, when, from whom, hash) is not itself named anywhere. It becomes subject to the 5-year minimum where it is needed to "reconstitute each key stage of the processing" of a portfolio transaction (UCITS/AIFM) or of an order or transaction (MiFID/MiFIR). Examples are prices or reference data that drove an order, an allocation or a NAV. Otherwise it falls under "orderly records" (no fixed EU period) and DORA logging (entity-set period).
- **Inferred.** The Art 72(1)(b) and (c) form tests (pre-amendment content ascertainable, no other manipulation) point to append-only or versioned storage. They fit an immutable Blob archive plus manifests better than overwritable tables.

### Gaps
- Valuation-record provisions (231/2013 Art 67–74; UCITS NAV rules) were not extracted. They may impose specific duties on pricing-input records and should be checked.
- National transposition of a general 5-year MiFID retention period, which many Member States have, was not researched.

---

## Q3. Record class 2: evidence that a control operated (a data-quality check passed or failed)

### Takeaway
EU texts require internal control mechanisms and their monitoring and evaluation, but **prescribe no named record of each control execution**. DORA requires recording of anomalous activities, with protection against tampering and specified fields. It also requires ICT-incident records and "detection of a failure of logging systems". For a failed data-quality check that indicates data loss or integrity impairment, DORA RTS Art 23 criteria may make it an incident-detection trigger.

### Cited Findings
- documented. 2017/565 Art 21(1)(c): "establish, implement and maintain adequate internal control mechanisms designed to secure compliance with decisions and procedures at all levels of the investment firm". Art 21(5): "Investment firms shall monitor and, on a regular basis, evaluate the adequacy and effectiveness of their systems, internal control mechanisms and arrangements … and take appropriate measures to address any deficiencies." — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented. 2010/43 Art 4(1)(c) (ManCo) and 231/2013 Art 57(1) (AIFM) carry parallel internal-control wording: "adequate internal control mechanisms designed to secure compliance with decisions and procedures at all levels of the management company". — [Dir 2010/43/EU](https://publications.europa.eu/resource/celex/32010L0043); [Reg (EU) 231/2013](https://publications.europa.eu/resource/celex/32013R0231)
- documented, DORA framework documentation and audit. Art 6(5): "The ICT risk management framework shall be documented and reviewed at least once a year …". Art 6(6): the framework "shall be subject to internal audit by auditors on a regular basis". — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA RTS anomalous-activity records. 2024/1774 Art 23(2)(d): the mechanism shall enable entities to "record, analyse, and evaluate any relevant information on all anomalous activities and behaviours automatically or manually". Art 23(2), last subparagraph: tools that "provide automated alerts based on pre-defined rules to identify anomalies affecting the completeness and integrity of the data sources or log collection". Art 23(3): "Financial entities shall protect any recording of the anomalous activities against tampering and unauthorised access at rest, in transit and, where relevant, in use." Art 23(4): "Financial entities shall log all relevant information for each detected anomalous activity enabling: (a) the identification of the date and time of occurrence …; (b) the identification of the date and time of detection …; (c) the identification of the type of the anomalous activity." Art 23(5)(b) lists as an incident-detection criterion "data losses detected in relation to the availability, authenticity, integrity, and confidentiality of data". — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented, DORA incidents. Art 17(2): "Financial entities shall record all ICT-related incidents and significant cyber threats. … to ensure that root causes are identified, documented and addressed". Art 17(3)(b): "establish procedures to identify, track, log, categorise and classify ICT-related incidents …". No retention period is stated. — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented. 2024/1774 Art 12(2)(e): logging procedures shall contain "measures to detect a failure of logging systems". — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)

### Inferences
- **Inferred.** A data-quality check result is evidence that an internal control mechanism exists and operates (MiFID 21(1)(c), 21(5); UCITS/AIFMD parallels). It supports the DORA Art 6(6) internal audit. EU law sets no retention period for it as such.
- **Inferred.** The period is driven by (i) the audit cycle, (ii) linkage to a 5-year transaction or NAV record if the check guarded data used in that record, and (iii) the entity's own DORA retention decision.
- **Inferred.** A failed completeness or integrity check is plausibly an "anomalous activity" under RTS Art 23. Its record then needs the occurrence time, detection time and type fields (Art 23(4)) and tamper protection (Art 23(3)).

### Gaps
- No ESMA or EBA Q&A found specifically on evidencing data-quality control operation for asset managers.

---

## Q4. Record class 3: human overrides of a control (who, when, why, approved by whom)

### Takeaway
No EU text names "override records". The closest documented hooks are these:
- MiFID/UCITS/AIFMD: corrections and amendments must be ascertainable together with the pre-amendment content.
- DORA RTS: user accountability, so users are "identifiable for the actions performed in the ICT systems at all times"; segregation of duties; logging of access-control, identity-management and change-management events; independence of approving and implementing functions for ICT changes.
- DORA Art 9(4)(e): changes "recorded, tested, assessed, approved, implemented and verified".

Whether an override is an "ICT change" or a business decision is a classification compliance must confirm.

### Cited Findings
- documented. 2017/565 Art 72(1)(b): "it is possible for any corrections or other amendments, and the contents of the records prior to such corrections or amendments, to be easily ascertained". 2010/43 Art 16(3)(b) and 231/2013 Art 66(3)(b) have parallel wording. — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565); [Dir 2010/43/EU](https://publications.europa.eu/resource/celex/32010L0043); [Reg (EU) 231/2013](https://publications.europa.eu/resource/celex/32013R0231)
- documented. 2024/1774 Art 21 (Access control):
  - "(b) the segregation of duties designed to prevent unjustified access to critical data or to prevent the allocation of combinations of access rights that may be used to circumvent controls;"
  - "(c) a provision on user accountability, by limiting to the extent possible the use of generic and shared user accounts and ensuring that users are identifiable for the actions performed in the ICT systems at all times".

  Art 21, closing subparagraph: "For the purposes of point (e)(i), financial entities shall establish the retention period taking into account the business and information security objectives, the reasons for recording the event in the logs, and the results of the ICT risk assessment." The cross-reference is quoted as found in the OJ text. — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented. 2024/1774 Art 12(2)(c): the requirement to log events related to "(i) logical and physical access control, as referred to in Article 21, and identity management; … (iii) change management". — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented. 2024/1774 Art 17(1): ICT change management procedures shall include, for "all changes to software, hardware, firmware components, systems, or security parameters", "(a) a verification of whether the ICT security requirements have been met; (b) mechanisms to ensure the independence of the functions that approve changes and the functions responsible for requesting and implementing those changes". — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented. DORA Art 9(4)(e): "implement documented policies, procedures and controls for ICT change management … in order to ensure that all changes to ICT systems are recorded, tested, assessed, approved, implemented and verified in a controlled manner". Art 9(4), final subparagraph: "the ICT change management process shall be approved by appropriate lines of management and shall have specific protocols in place." — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented. 2017/565 Art 21(1)(a): an organisational structure "which clearly and in documented manner specifies reporting lines and allocates functions and responsibilities". — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)

### Inferences
- **Inferred.** An override of a data-quality gate is a deviation from a control. It is therefore an "amendment" whose before and after state should be ascertainable (72(1)(b)) if it altered a record used for a transaction or NAV. The user-accountability (who) and segregation-of-duties (approved by whom) elements map to RTS Art 21(b)–(c). The "why" field is not named in any text extracted; it is inferred from the internal-control and audit duties.
- **Inferred.** If the override changes system configuration, thresholds or code, it is an ICT change under Art 9(4)(e) and RTS Art 17. Recording and independent approval are then explicit. A one-off data release decision is less clearly an ICT change.
- **Inferred.** Override records contain staff identities, so GDPR applies where EU GDPR scope is engaged (see Q5).

### Gaps
- No ESMA or EBA text found on "manual overrides" of data controls specifically.
- Valuation-override records (for example price overrides in NAV) were not checked against 231/2013 Art 67–74.

---

## Q5. Record class 4: job and run logs of the data platform

### Takeaway
This is the class with the most explicit EU text: DORA RTS 2024/1774 Art 12 (Logging). It requires:
- documented logging procedures that identify the events to log and the **retention period**;
- coverage of "ICT operations, including ICT system activities", change management and access control;
- protection against "tampering, deletion, and unauthorised access";
- detection of logging failure;
- clock synchronisation.

**The retention period is set by the entity**, not by the RTS. Art 8 also requires ICT-operations policies covering scheduling and "protocols for audit-trail and system log information". DORA Art 12 (backup) requires a documented backup scope. Simplified-framework entities (Art 16(1)) have RTS Art 34(f) logging.

### Cited Findings
- documented, full text of 2024/1774 **Art 12 "Logging"**:
  - "1. Financial entities shall, as part of the safeguards against intrusions and data misuse, develop, document, and implement logging procedures, protocols and tools.
  - 2. The logging procedures, protocols, and tools referred to in paragraph 1 shall contain all of the following:
    - (a) the identification of the events to be logged, the retention period of the logs, and the measures to secure and handle the log data, considering the purpose for which the logs are created;
    - (b) the alignment of the level of detail of the logs with their purpose and usage to enable the effective detection of anomalous activities as referred to in Article 24;
    - (c) the requirement to log events related to all of the following: (i) logical and physical access control, as referred to in Article 21, and identity management; (ii) capacity management; (iii) change management; (iv) ICT operations, including ICT system activities; (v) network traffic activities, including ICT network performance;
    - (d) measures to protect logging systems and log information against tampering, deletion, and unauthorised access at rest, in transit, and, where relevant, in use;
    - (e) measures to detect a failure of logging systems;
    - (f) without prejudice to any applicable regulatory requirements under Union or national law, the synchronisation of the clocks of each of the financial entity's ICT systems upon a documented reliable reference time source.
  - For the purposes of point (a), financial entities shall establish the retention period, taking into account the business and information security objectives, the reason for recording the event in the logs, and the results of the ICT risk assessment."

  — [RTS (EU) 2024/1774 of 13.3.2024, Art 12](https://publications.europa.eu/resource/celex/32024R1774)
- documented. The RTS supplements DORA "in particular Article 15, fourth subparagraph, and Article 16(3), fourth subparagraph". Entry into force is "on the twentieth day following that of its publication in the Official Journal" (Art 42). Done at Brussels, 13 March 2024. — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented. 2024/1774 Art 8(1): entities "shall develop, document, and implement policies and procedures to manage the ICT operations … specify how financial entities operate, monitor, control, and restore their ICT assets, including the documentation of ICT operations". Art 8(2)(b) lists "controls and monitoring of ICT systems, including all of the following: (i) backup and restore requirements of ICT systems; (ii) scheduling requirements, taking into consideration interdependencies among the ICT systems; (iii) protocols for audit-trail and system log information; …". — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented, simplified framework. 2024/1774 Art 34 "ICT operations security" applies to "financial entities referred to in Article 16(1) of Regulation (EU) 2022/2554". Point (f): "log events related to logical and physical access control, ICT operations, including system and network traffic activities, and ICT change management". Closing subparagraph: "For the purposes of point (f), financial entities shall align the level of detail of the logs with their purpose and usage of the ICT asset producing those logs." **No separate retention or protection wording appears in Art 34**, unlike Art 12. — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented, DORA backup. Art 12(1): entities "shall develop and document: (a) backup policies and procedures specifying the scope of the data that is subject to the backup and the minimum frequency of the backup, based on the criticality of information or the confidentiality level of the data; (b) restoration and recovery procedures and methods." — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA Art 9(2): ICT security policies to "maintain high standards of availability, authenticity, integrity and confidentiality of data, whether at rest, in use or in transit". — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, GDPR (only where logs hold personal data such as user IDs or approver names, and GDPR applies):
  - Art 3(1): "applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not".
  - Art 5(1)(e): personal data to be "kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed" (storage limitation).
  - Art 5(1)(f): "processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage" (integrity and confidentiality).
  - Art 30(1): "Each controller … shall maintain a record of processing activities under its responsibility."
  - Art 32(1) lists "(b) the ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services; (c) the ability to restore the availability and access to personal data in a timely manner …".

  — [GDPR, Reg (EU) 2016/679 of 27.4.2016](https://publications.europa.eu/resource/celex/32016R0679)

### Inferences
- **Inferred.** Dagster or Databricks run and job logs are "ICT operations, including ICT system activities" logs (RTS Art 12(2)(c)(iv)) and scheduling-related records (Art 8(2)(b)(ii)–(iii)). The entity must write down which events it logs and for how long. A 60-day or 365-day period is not excluded by the RTS **if** it is justified by business and infosec objectives and the ICT risk assessment.
- **Inferred.** Where a run log is the only evidence of a "key stage of the processing" of a transaction or NAV, the 5-year UCITS/AIFMD/MiFIR minimum is a regulatory requirement under Union law. RTS Art 12(2)(f) and Art 28(1)(a) acknowledge "applicable regulatory requirements" and "applicable financial services law". It would then override a shorter DORA-only retention choice.
- **Inferred.** The DORA retention choice and the GDPR storage limitation pull in opposite directions for user-identifying log fields. Typical resolutions are pseudonymisation or split retention; this is for the DPO and compliance.
- **Inferred.** GDPR reaches a Swiss firm's logs only through Art 3. The trigger is an EU establishment (subsidiary or branch) processing the logs, or Art 3(2) targeting or monitoring, which is unlikely for staff logs.

### Gaps
- The text of DORA Art 10 (detection) was not quoted. It is referenced by RTS Art 23.
- RTS Art 24 was not extracted. It is referenced by Art 12(2)(b), although the anomaly-detection content appears in Art 23 in the OJ text.
- No ESA guidance found on minimum log retention periods. None appears to exist; the RTS leaves it to the entity.

---

## Q6 (D2). Which duties can be met by logs kept only in a vendor tool, and which need a firm-controlled record?

### Takeaway
Duties where the **retention period is entity-defined** could in principle be met by vendor-tool logs, given a documented, risk-assessed retention decision and tamper and deletion protection. These are DORA RTS Art 12 logging, Art 8 operations and RTS Art 34 for simplified entities. Even then, they need contractual access, audit, location and exit rights under DORA Art 30 or MiFID 2017/565 Art 31.

Duties with a **5-year minimum** cannot be met by a 60-day or 365-day vendor store alone. These are UCITS 2010/43 Art 16, AIFMD 231/2013 Art 66, MiFIR Art 25 and Art 46(6b), and MiFID Art 16(7) recordings. The same holds for duties requiring that **pre-amendment content is ascertainable and no other manipulation is possible**, unless the vendor store guarantees those properties for the full period. Whether a given run log falls into the 5-year set is the key compliance question.

### Cited Findings
- documented, firm remains responsible. DORA Art 28(1)(a) (quoted in Q1). 2017/565 Art 31(1): "Investment firms outsourcing critical or important operational functions shall remain fully responsible for discharging all of their obligations under Directive 2014/65/EU". MiFID II Art 16(5): outsourcing "may not be undertaken in such a way as to impair materially the quality of its internal control and the ability of the supervisor to monitor the firm's compliance with all obligations". — [DORA](https://publications.europa.eu/resource/celex/32022R2554); [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565); [MiFID II](https://publications.europa.eu/resource/celex/32014L0065)
- documented, DORA Art 30 contract terms for all ICT services:
  - Art 30(1): "The full contract … shall be documented in one written document which shall be available to the parties on paper, or in a document with another downloadable, durable and accessible format."
  - Art 30(2):
    - "(b) the locations, namely the regions or countries, where the contracted or subcontracted functions and ICT services are to be provided and where data is to be processed, including the storage location, and the requirement for the ICT third-party service provider to notify the financial entity in advance if it envisages changing such locations;"
    - "(c) provisions on availability, authenticity, integrity and confidentiality in relation to the protection of data, including personal data;"
    - "(d) provisions on ensuring access, recovery and return in an easily accessible format of personal and non-personal data processed by the financial entity in the event of the insolvency, resolution or discontinuation of the business operations of the ICT third-party service provider, or in the event of the termination of the contractual arrangements;"
    - "(h) termination rights and related minimum notice periods".

  — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, DORA Art 30(3) for ICT services supporting critical or important functions:
  - "(e) the right to monitor, on an ongoing basis, the ICT third-party service provider's performance, which entails the following: (i) unrestricted rights of access, inspection and audit by the financial entity, or an appointed third party, and by the competent authority, and the right to take copies of relevant documentation on-site if they are critical to the operations of the ICT third-party service provider …;"
  - "(f) exit strategies, in particular the establishment of a mandatory adequate transition period … (ii) allowing the financial entity to migrate to another ICT third-party service provider or change to in-house solutions".

  Art 28(8): "For ICT services supporting critical or important functions, financial entities shall put in place exit strategies." — [DORA](https://publications.europa.eu/resource/celex/32022R2554)
- documented, MiFID outsourcing. 2017/565 Art 31(2)(i): "the investment firm, its auditors and the relevant competent authorities have effective access to data related to the outsourced functions, as well as to the relevant business premises of the service provider". Art 31(3): "the investment firm shall keep its instruction and termination rights, its rights of information, and its right to inspections and access to books and premises." Art 30(1) defines critical or important as a function whose "defect or failure in its performance would materially impair the continuing compliance of an investment firm with the conditions and obligations of its authorisation …". — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented, AIFM delegation access. 231/2013 Art 75(f), (h) (quoted in Q1). — [Reg (EU) 231/2013](https://publications.europa.eu/resource/celex/32013R0231)
- documented, durable-medium wording. The explicit phrase "durable medium … retained in a format that does not allow the original record to be altered or deleted" is in 2017/565 **Art 76(10)**, which is scoped to telephone and electronic-communication recordings. Art 76(11): "The period of time for the retention of a record shall begin on the date when the record is created." For general records, Art 72(1) uses "medium that allows the storage of information in a way accessible for future reference" plus conditions (a)–(e), not "durable medium". — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented, RTS Art 12(2)(d) tamper and deletion protection of logs and Art 12(2)(e) detection of logging failure (quoted in Q5). — [RTS 2024/1774](https://publications.europa.eu/resource/celex/32024R1774)
- documented, UCITS and AIFMD continuity after termination. 2010/43 Art 16(2): after termination of authorisation, authorities "may require the management company to retain records … for the outstanding term of the 5-year period". 231/2013 Art 66(2): records "are to be retained at least for the outstanding term of the five-year period". — [Dir 2010/43/EU](https://publications.europa.eu/resource/celex/32010L0043); [Reg (EU) 231/2013](https://publications.europa.eu/resource/celex/32013R0231)

### Inferences
**Inferred.** Classification by record class. All of this needs compliance confirmation.

| Record class | Could a vendor-only store (60d Dagster+/Databricks run history; 365d system tables) suffice? | Why (inferred) |
|---|---|---|
| 4. Job/run logs used only for ICT operations and security | Possibly, if the entity's documented RTS Art 12 retention decision is ≤ the vendor period and Art 12(2)(d) protection is demonstrable | Retention is entity-set (RTS Art 12, last subpara). Art 30(2)(b)–(d) and (3)(e)–(f) rights are still needed. |
| 4. Run logs that are the only evidence of a key processing stage of a transaction or NAV | No. A 5-year minimum applies (2010/43 Art 16; 231/2013 Art 66; MiFIR Art 25) | 60d and 365d < 5y. "Reconstitute each key stage" plus no-manipulation conditions. |
| 1. Vendor delivery records (what/when/from whom) feeding transactions or NAV | No, if they are part of a key processing stage; otherwise as for ICT logs | Same 5-year reasoning. Byte archive plus manifests in firm-controlled Azure is the firm-controlled record. |
| 2. Control-execution evidence (DQ pass/fail) | Depends on the audit cycle and linkage. An annual DORA review and internal audit (Art 6(5)–(6)) imply ≥ 1 audit cycle. Anomaly records need Art 23(3) tamper protection. | No fixed EU period. |
| 3. Human overrides (who/when/why/approver) | Unlikely, if the override altered data used for transactions or NAV | Pre-amendment content must be ascertainable for the record's life (72(1)(b), 66(3)(b), 16(3)(b)). User accountability (RTS Art 21(c)). |

- **Inferred.** Vendor run history held by a SaaS provider is "data processed by the financial entity". Under DORA Art 30(2)(d) the contract must ensure "access, recovery and return in an easily accessible format" at termination. Purge-by-age that cannot be suspended or exported may sit uneasily with that and with the exit duty in Art 28(8) and 30(3)(f).
- **Inferred.** The Swiss parent's own platform records are firm-controlled from the Swiss perspective. Seen from an EU subsidiary or delegating EU manager, they are a third-party (intra-group) store, needing the same access and audit flow-down.

### Gaps
- DORA RTS 2024/1773 (policy on ICT services supporting critical or important functions) was downloaded but not analysed in detail.
- The DORA RTS on subcontracting (Art 30(5)) was not retrieved.
- Whether Dagster OSS (self-hosted, no vendor) or Databricks counts as an ICT service "supporting critical or important functions" depends on the entity's function mapping. Not determinable from law.

---

## Q7 (D3). Points needing legal or compliance confirmation; pending revisions

### Takeaway
The main open legal points are four:
1. Whether the 5-year minimum attaches to platform run logs and DQ evidence, which turns on "key stage of the processing".
2. The national general MiFID retention period, since EU text sets none for Art 16(6) records.
3. How the Swiss firm's arrangements are characterised: delegation (financial service) or ICT service.
4. Whether quoted texts were later amended, since only original OJ versions were read.

### Cited Findings
- documented. MiFID II Art 16(6) and 2017/565 Art 72 contain no retention period in their original text. The 5/7-year wording is tied to Art 16(7) recordings. **The brief's premise "Art 16(6)–(7) record-keeping (5 years, up to 7 on request)" is therefore only partly supported by the primary text.** — [MiFID II](https://publications.europa.eu/resource/celex/32014L0065); [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented. 2017/565 Annex I cites "Article 69" and "Article 70 of this Regulation" for client-order and transaction records. In the adopted numbering these are Art 74 and Art 75, which carry the matching titles. This looks like a cross-reference anomaly in the OJ text as retrieved; a corrigendum may exist (unverified). — [Reg (EU) 2017/565](https://publications.europa.eu/resource/celex/32017R0565)
- documented. AIFMD II (Directive (EU) 2024/927) changes the delegation provisions (Art 20) from 16 April 2026, with some measures from 16 April 2027. National transposition status per Member State was not checked. — [Dir (EU) 2024/927](https://publications.europa.eu/resource/celex/32024L0927)
- secondary. I found no evidence of an adopted 2026 amendment to DORA. A Commission "Digital Omnibus" was unveiled 19 Nov 2025 for privacy, cyber, data and AI rules; whether it touches DORA or GDPR Art 5/30 duties relevant here is unverified. — [search summary; JD Supra topic page](https://www.jdsupra.com/topics/digital-operational-resilience-act-dora/cybersecurity/data-protection); [EFAMA on DORA proportionality](https://www.efama.org/newsroom/news/proposed-changes-dora-require-more-proportionality-and-simplicity)
- documented guidance. Q&A DORA030 is interpretive, not binding. Secondary sources note that an earlier register "Dry Run FAQ" carve-out was later withdrawn. — [EIOPA Q&A DORA030-2999](https://www.eiopa.europa.eu/qa-regulation/questions-and-answers-database/dora030-2999_pt)

### Inferences
**Items for legal or compliance confirmation (all inferred as open):**
1. Consolidated versions of MiFID II, 2017/565, MiFIR (also amended by Regulation (EU) 2024/791, not retrieved), UCITS, AIFMD, 231/2013 and DORA: check that the quoted paragraphs are unchanged as of 2026-10-27.
2. The national general retention period for MiFID records in the relevant EU Member State, and any national supervisory requirement for longer retention. Competent authorities may require additional records (2017/565 Art 72(3)) or longer periods (2010/43 Art 16(1); 231/2013 Art 66(1)).
3. Whether data-platform run logs, DQ results and overrides are part of "each key stage of the processing of each (portfolio) transaction", or of NAV and valuation records, and so subject to the 5-year minimum.
4. Characterisation of each Swiss–EU arrangement:
   - delegation of portfolio management (financial service, Q&A DORA030);
   - standalone ICT or data service (DORA Art 30, register);
   - MiFID outsourcing of a critical or important function (2017/565 Art 30–32).
5. Whether the Databricks or Dagster+ service supports a "critical or important function". This triggers DORA Art 30(3) and 28(8) and 2017/565 Art 31.
6. DORA application to an EU third-country branch of a Swiss investment firm.
7. GDPR territorial reach (Art 3) for logs held by the Swiss firm, and reconciliation of DORA or 5-year retention with Art 5(1)(e).
8. Whether vendor-side purge (60 days, 365 days) is compatible with Art 30(2)(d) return-of-data and exit duties, and with RTS Art 12(2)(d) "deletion" protection where the vendor deletes before the entity-set retention period ends.

### Gaps
- Consolidated EUR-Lex versions were unreachable (bot challenge). ESMA/EBA guidelines on outsourcing to cloud service providers (ESMA, 2021) were not reviewed. They may add access and audit expectations for UCITS/AIFM and MiFID firms in relation to SaaS.
