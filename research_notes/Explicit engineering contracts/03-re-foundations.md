# Track 3: RE foundations (assumptions, oracles, keywords, independence, naming, traceability, ADRs, glossaries, 29148)

Method: a verifier agent read primary full texts where it could reach them.
UNREACHABLE sources are marked; for those only an abstract, a secondary source or a search extract was read.
Single-pass, not 3-vote verified.

## 1a. Zave & Jackson, "Four dark corners of requirements engineering", TOSEM 6(1), 1997
- Author copy: https://pamelazave.com/4dc.pdf (full text read)
- Evidence type: conceptual analysis.
- Indicative mood: statements about the environment as it is; these are assumptions or domain knowledge.
- Optative mood: statements about how we want the environment to be; these are requirements.
- "Correct specifications, in conjunction with appropriate domain knowledge, imply the satisfaction of the requirements."
- Each phenomenon must be labelled as environment- or machine-controlled, and as shared or unshared.
- "All the terminology used in requirements engineering should be grounded in the reality of the environment."
- Not empirically validated.

## 1b. van Lamsweerde & Letier, "Handling obstacles in goal-oriented RE", TSE 26(10), 2000
- Preprint: https://webperso.info.ucl.ac.be/~avl/files/TSE-Obstacles.pdf (full text read)
- Evidence type: formal method, illustrated by examples.
- Goals and assumptions "tend to be too ideal"; failing to anticipate exceptional behaviour gives "unrealistic, unachievable and/or incomplete requirements".
- An obstacle is a condition under which a goal may not be achieved; the paper gives ways to generate and resolve obstacles.
- The full formalism (temporal logic) is heavy for a small team. The lightweight transfer is to ask "what makes this false?" of each requirement and assumption (inference).

## 2. Barr et al., "The Oracle Problem in Software Testing: A Survey", TSE 41(5), 2015
- Read via course mirror: https://web.eecs.umich.edu/~weimerw/2018-481/readings/testoracles.pdf. The UCL copy was blocked by Cloudflare.
- Evidence type: literature survey, no effect sizes.
- §5.3: regression testing "rests on the implicit assumption that the previous version can serve as an oracle".
- Derived oracles are used because "specifications rapidly fall out of date when they exist at all".
- §5.5: textual documentation is "often partial and ambiguous".
- §6: implicit oracles (crashes etc.) need no spec but are "not universal".

## 3. RFC 2119 (1997) and RFC 8174 (2017), both BCP 14
- Full texts: https://www.rfc-editor.org/rfc/rfc2119.txt, https://www.rfc-editor.org/rfc/rfc8174.txt
- RFC 2119 §6: imperatives "must be used with care and sparingly … only … where it is actually required for interoperation or to limit behavior which has potential for causing harm"; "not … to impose a particular method on implementors".
- RFC 8174 §2: only UPPERCASE keywords carry the special meaning; lowercase words have their normal English meaning; "Normative text does not require the use of these key words."

## 4. Knight & Leveson, TSE 12(1), 1986 (primary text UNREACHABLE)
- Read: abstract, plus a secondary summary at https://www.kth.se/social/files/564df871f2765419e306178d/KnightLeveson.pdf
- Evidence type: controlled experiment.
- 27 versions were written independently from one spec and run on 1,000,000 tests. The number of tests on which more than one version failed was substantially higher than independence predicts.
- Detailed figures come only from the secondary summary: 551 tests with two versions failing together, up to 8 versions failing on one test, independence rejected at α=0.01.

## 5. Naming
- Arnaoudova, Di Penta, Antoniol, "Linguistic antipatterns", EMSE 21(1), 2016.
  - Manuscript: https://www.veneraarnaoudova.ca/wp-content/uploads/2014/10/2014-EMSE-Arnaodova-et-al-Perception-LAs.pdf (full text read)
  - Catalogue of 17 linguistic antipatterns: inconsistencies between name, documentation and implementation.
  - 69% of external and 51% of internal developers perceive them as poor practice.
  - Measures perception, not defects.
- Lawrie et al., "Effective identifier names for comprehension and memory", ISSE 2007.
  - https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf (full text read)
  - Over 100 programmers took part.
  - Full words gave the best comprehension, but often with no significant difference from abbreviations.
- Butler et al., CSMR 2010: UNREACHABLE.
  - Search extract only: flawed identifiers were associated with FindBugs warnings (correlational).

## 6. Mäder & Egyed, EMSE 20(2), 2015 (journal text UNREACHABLE)
- Read: the authors' 2-page SE 2016 summary, https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f
- Evidence type: controlled experiment.
- 71 subjects; 8 real tasks on Gantt Project and iTrust; 461 tasks solved, with solutions on paper rather than implemented.
- With traces, subjects were 24% faster and produced 50% more correct solutions, consistently across experience levels.
- The cost of creating and maintaining traces was not measured.

## 7. ADRs
- Nygard 2011 (practitioner, full text read): https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - Numbered ADRs in the repo; superseded ADRs are kept; template is Context, Decision, Status, Consequences.
- Buchgeher et al., IEEE Access 11, 2023, DOI 10.1109/ACCESS.2023.3287654: UNREACHABLE.
  - Extracts: adoption on GitHub is low but rising; about 50% of ADR repositories have 1–5 ADRs.
- Su et al., arXiv 2602.07609, 2026 (skimmed).
  - 980 ADRs in 109 repositories.
  - LLMs detect violations of explicit, code-inferable decisions well; implicit or deployment-oriented decisions poorly.
- No study shows that ADRs reduce defects.

## 8. Glossaries and ubiquitous language
- No empirical study of effects on defects or consistency was found (search-level check, not exhaustive).
- Özkan et al., DDD systematic literature review, arXiv 2310.01905 (abstract only): empirical evaluation is lacking.
- Evidence for glossaries is therefore expert opinion.

## 9. ISO/IEC/IEEE 29148:2018 (standard text UNREACHABLE, paywalled)
- Table of contents confirmed: 5.2.5 individual requirement characteristics, 5.2.6 set characteristics, 5.2.7 language criteria.
- Secondary sources give the individual characteristics as: necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming.
- Set characteristics: complete, consistent, feasible, comprehensible, able to be validated.
- Femmer et al. (JSS 2017) operationalise the 29148:2011 language criteria as requirement smells.
