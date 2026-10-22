# Contracts and resource lifecycle: methods for specifying single calls and handed-out resources at a black-box API boundary

Method note: in this session WebFetch could not reach any host (egress proxy refused docs.python.org, pubs.opengroup.org, grpc.io, cs.ucf.edu). Every finding below comes from the cited page as quoted in search-engine extracts. I did not read the full text. Short quotations were checked against the extract, not against the original. Claims that rest only on my background knowledge are marked "(background, unverified)" and kept out of Cited Findings.

Grading: A = peer-reviewed or measured study; B = documented industrial practice with data, or a normative standard or official spec; C = practitioner report or course notes, no data; D = opinion or marketing. Normative standards and official API docs are graded B. They are authoritative about what they specify but are not evidence that the method works.

## Q1. Pre/post/frame contract families (DbC, Hoare, JML, Dafny, model-based/Larch): how they state exceptions, frames and underspecification

### Takeaway
Contract languages express a single call as a two-state relation (pre-state to post-state) over an abstract model of the observable state. JML has the most explicit black-box machinery: separate normal and exceptional behaviours, `signals`/`signals_only` for exceptional postconditions, `assignable` for frames, and model fields so the spec never needs the implementation's state. Dafny adds `modifies`/`reads` frames, plus `old()`/`fresh()` to express handing out a new object. None of these methods can by itself express "the call returned, and the failure surfaces later through a different object". That has to be modelled as state of the returned resource, which leads into Q2.

### Cited Findings
- **Design by Contract (Meyer 1992), grade A (peer-reviewed magazine article, IEEE Computer; conceptual, no empirical data).** The paper builds software components on "carefully designed contracts" and defines reliability as correctness plus robustness — [Meyer 1992 PDF](https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf); [mirror](https://simon.ifi.uzh.ch/rerg/amadeus/teaching/courses/ase_fs10/Meyer1992.pdf)
- **DbC failure model, grade B (official Eiffel docs).** A routine either fulfils its contract or fails. A `rescue` clause either ends in `retry`, which re-runs the body to try again to meet the contract, or the routine fails and raises an exception in its caller. A routine cannot "pretend" it succeeded — [Eiffel: Exception Mechanism](https://www.eiffel.org/doc/solutions/Exception_Mechanism); [I2E: Exceptions](https://eiffel.org/doc/eiffel/I2E-_Exceptions). The secondhand Usenet quotation of Meyer's "rescue never reaches the original goal using a substitute implementation" is grade C — [comp.lang.ada post](https://usenet.ada-lang.io/comp.lang.ada/3421E190.49CC@chimu.com)
- **Critique of rescue/retry as a "disguised backward goto", grade D (opinion)** — [comp.lang.ada, Bob Duff](https://usenet.ada-lang.io/comp.lang.ada/87bne0fbqr.fsf@theworld.com)
- **JML design, grade A (Leavens, Baker, Ruby, ACM SIGSOFT SEN 31(3):1–38, 2006).** JML is a "behavioral interface specification language" that combines Eiffel-style contracts with the model-based approach of VDM and Larch. It adds quantifiers, specification-only variables and frame conditions — [Preliminary Design of JML (Iowa State record)](https://dr.lib.iastate.edu/cs_techreports/136); [PDF](https://www.cs.ucf.edu/~leavens/JML/prelimdesign.pdf)
- **JML exceptional postconditions, grade B (JML reference manual) and C (course slides).**
  - A method's spec can be split into `normal_behavior` and `exceptional_behavior` cases.
  - `exceptional_behavior` implicitly carries `ensures false`, so the method must not return normally. `normal_behavior` implicitly carries `signals (java.lang.Exception) false`.
  - The default for `signals_only` is the method's declared `throws` list.
  - Sources: [JML Reference Manual ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html); [Freiburg lecture slides](https://swt.informatik.uni-freiburg.de/teaching/WS2012-13/fm4j/Resources/Slides/lec04)
- **JML frame default: sources conflict.** Per the reference-manual guidance, an omitted `assignable` clause in a heavyweight spec means "all locations that can otherwise be legally assigned to can be assigned", which is no frame at all — [JML Reference Manual ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html). The Freiburg slides say that with a behaviour keyword there are "no default values" for `diverges`, `signals_only` and `assignable` — [Freiburg slides](https://swt.informatik.uni-freiburg.de/teaching/WS2012-13/fm4j/Resources/Slides/lec04). Prefer the manual.
- **Dafny frames, grade C (course notes and cheatsheet; the reference manual was listed but not read).**
  - A method that mutates state must declare it in `modifies`. Callers may assume every location outside the clause is unchanged.
  - Functions declare `reads` frames.
  - `old(E)` gives E's pre-state value. Two-state predicates include `unchanged(o)`, `allocated(o)` and `fresh(o)`.
  - Sources: [UMD Dafny cheatsheet](https://www.cs.umd.edu/class/summer2026/cmsc433/Dafny_Cheatsheet.html); [Dafny cheatsheet v4.3](https://dafny.org/v4.3.0/DafnyCheatsheet.pdf); [U. Iowa notes](https://homepage.cs.uiowa.edu/~tinelli/classes/181/Fall20/Notes/14-arrays-II.pdf); [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/out/DafnyRef.pdf)
- **Larch two-tiered specs, grade A/B (Guttag, Horning, Wing; SRC Research Report 58; Larch FAQ).**
  - The Larch Shared Language (LSL) is a programming-language-independent tier made of first-order theories that define the vocabulary (abstract values).
  - A language-specific interface tier specifies each module's behaviour as "first-order predicates over two states".
  - Sources: [Larch FAQ (Leavens)](https://www.cs.ucf.edu/~leavens/larch-faq.html); [SRC RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf); [Wing 1987](https://www.cs.columbia.edu/~wing/publications/Wing87.pdf)
- **Behavioural subtyping, grade A (Liskov & Wing, ACM TOPLAS 1994).**
  - A subtype's methods may not throw new exceptions beyond subtypes of those the supertype's methods throw.
  - A "history constraint" forbids subtypes from making state changes that the supertype's spec rules out. The standard example is that a mutable point is not a subtype of an immutable point.
  - The 1999 follow-up replaces the history rule with explicit invariants and constraints.
  - Sources: [Liskov & Wing 1994 PDF](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf); [Wikipedia: Behavioral subtyping](https://en.wikipedia.org/wiki/Behavioral_subtyping) (C); [DTIC 1999 TR](https://apps.dtic.mil/sti/pdfs/ADA367674.pdf)

### Inferences
- (inference) Liskov & Wing is the formal basis for "one API, several realities". If each backend is a behavioural subtype of one abstract spec, a backend may narrow nondeterminism and raise fewer error kinds, but may not add new kinds or new observable state changes. Backend-specific detail then sits in subtype specs, which satisfies P3. This holds only if the abstract spec is written loosely enough to admit every backend.
- (inference) JML's split into normal and exceptional cases, with model fields, maps onto P1 (what, not how) and P5 (no implementation view). Each `requires` → `ensures`/`signals` case is a natural "one claim per unit" (P2). Contract clauses are runtime-checkable assertions, which partly meets P4 (every claim names its check), but only for properties observable at call return.
- (inference) Running example, *once semantics are decided*, as JML-style cases:
  - Case 1: `requires` key exists ∧ readable; `ensures` `\fresh(\result)` ∧ `\result.state == OPEN` ∧ `\result.content == model.entities[key]` ∧ frame `assignable \nothing` over the store model.
  - Case 2: `exceptional_behavior` `requires` ¬exists(key); `signals_only NotFound`.
  - Mid-read failure cannot be a postcondition of `open`. It has to be a `signals` case on `stream.read`, conditioned on a model field such as `stream.failed` or an environment model. That is the limit of single-call contracts.
- Model-based languages (VDM, Z, B): (background, unverified) VDM-SL has `pre`/`post`/`ext rd/wr` (frame), and in VDM-SL `errs` clauses. Z states operations as schemas over Δ/Ξ state, with error cases composed as disjunctions of schemas, and nondeterminism through loose postconditions. B uses generalised substitutions with `ANY`/`CHOICE` for nondeterminism. None of this was sourced in this session.

### Gaps
- Not fetched: the ACSL manual (`assigns`, `behavior`, `complete behaviors`, `disjoint behaviors`), Spec#/Code Contracts docs (`EnsuresOnThrow`), VDM-SL `errs`, Z error-schema conventions, or the B-method. The search budget and blocked fetch prevented it. All are left as background only.
- Exact JML wording on `diverges` and model fields/`represents` was not verified.

## Q2. Resource lifecycle: typestate, session types, protocol state machines, interface automata, close contracts, ownership

### Takeaway
Lifecycle methods treat the handed-out stream as an object whose *state* governs which operations are legal and what they may return. "Outlives the call", "may fail later" and "use-after-close" become state transitions (OPEN → FAILED/EOF → CLOSED) with per-state contracts. Typestate and protocol state machines state this for a single object. Session types and interface automata state it as a two-party protocol with environment assumptions. Linear/affine ownership (Rust) enforces "used at most once / closed exactly once" but, as Rust's own `File` shows, can lose errors reported at close.

### Cited Findings
- **Typestate (Strom & Yemini, IEEE TSE 12(1):157–171, 1986), grade A.** Typestate refines type. A type fixes every operation an object may ever undergo, while typestate fixes the subset allowed at a given program point. Typestate tracking detects at compile time "syntactically legal but semantically undefined execution sequences", for example use before initialisation or use after free — [DBLP](https://dblp.org/pid/41/5885); [Wikipedia: Typestate analysis](https://en.wikipedia.org/wiki/Typestate_analysis) (C). IBM pages give inconsistent bibliographic data — [IBM Research](https://research.ibm.com/publications/typestate-a-programming-language-concept-for-enhancing-software-reliability)
- **Typestate for objects (DeLine & Fähndrich, ECOOP 2004, LNCS 3086:465–490), grade A.**
  - Gives a modular, sound checking algorithm for typestates on objects, covering subclassing, virtual dispatch and downcasting.
  - Subclasses can extend the interpretation of typestates.
  - Aliasing is handled by adapting linear types from Vault.
  - Implemented in Fugue for .NET.
  - The core difficulty is reasoning about sharing and about where invariants hold.
  - Sources: [Microsoft Research](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/); [Springer](https://www.springerprofessional.de/en/typestates-for-objects/14191004)
- **Session types (Honda, Vasconcelos, Kubo, ESOP 1998), grade A; ETAPS 2019 Test-of-Time award.** Session types are "type-theoretic specifications of communication protocols", verified by static type-checking — [ETAPS 2019 Test of Time](https://www.etaps.org/2019/test-of-time-award). Gay & Vasconcelos (JFP 20(1):19–50, 2010) give a linear type theory for *asynchronous* session types with buffered channels — [Cambridge JFP](https://www.cambridge.org/core/journals/journal-of-functional-programming/article/linear-type-theory-for-asynchronous-session-types/605DA26DDDE9B1CCD35D33D0D62DF20C); [PDF](https://homepage.cs.uiowa.edu/~jgmorrs/eecs762f19/papers/gay-vasconcelos.pdf)
- **Interface automata (de Alfaro & Henzinger, FSE 2001, DOI 10.1145/503209.503226), grade A.**
  - Interface automata capture *input assumptions* about the order in which a component's methods are called, and *output guarantees* about the order in which it calls out.
  - Compatibility is optimistic: two components are compatible if *some* environment makes them work together.
  - Refinement is alternating: weaker input assumptions and stronger output guarantees.
  - Sources: [ISTA record](https://research-explorer.ista.ac.at/record/4622)
  - Known limitation: outputs cannot be *required*, since an implementation that accepts all inputs and never outputs is a valid refinement — [Lüttgen & Vogler TR 2012](https://opus.bibliothek.uni-augsburg.de/opus4/files/2006/TR_2012_09.pdf) (A/C, tech report)
- **UML protocol state machines, grade B (vendor API docs and OMG issue tracker); C for course pages.**
  - A protocol state machine is tied to a classifier. It defines which operations may be invoked in each state and under which conditions.
  - Each protocol transition has a precondition (guard), a trigger (operation) and a postcondition.
  - States may not have entry/do/exit behaviours, and transitions have no effects. Operations that are not represented do not change the state.
  - Sources: [Charles Univ. UML PSM notes](https://d3s.mff.cuni.cz/~gergic/statecharts/uml15.html); [MagicDraw ProtocolTransition API](https://jdocs.nomagic.com/200/com/nomagic/uml2/ext/magicdraw/statemachines/mdprotocolstatemachines/ProtocolTransition.html)
  - An OMG issue argues that operation-level pre/postconditions "do not provide a synthetic overview at the classifier level", and that protocol states need not match internal states — [OMG UML14-209](https://issues.omg.org/issues/UML14-209). No BNF exists for protocol transition syntax — [OMG UMLR-659](https://issues.omg.org/issues/UMLR-659)
  - Class contracts (pre/post per triggering operation) can be generated mechanically from deterministic PSMs — [UCC publication](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/) (A)
- **Java close contracts, grade B (JDK Javadoc).**
  - `Closeable.close`: "if the resource is already closed then invoking this method has no effect" (idempotent).
  - `AutoCloseable.close`: "unlike the close method of Closeable, this close method is not required to be idempotent". Calling it more than once "may have some visible side effect", but idempotence is "strongly encouraged".
  - Sources: [AutoCloseable JDK 21](https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html); [JDK 7](https://javadoc.scijava.org/Java7/java/lang/AutoCloseable.html)
  - The compiler cannot check adherence — [Enthuware forum](https://enthuware.com/forum/viewtopic.php?p=7359) (C)
- **Java NIO asynchronous close, grade B.** On an `InterruptibleChannel`, `close()` from another thread makes a thread blocked in I/O on that channel receive `AsynchronousCloseException`. Interrupting the blocked thread closes the channel and raises `ClosedByInterruptException` — [InterruptibleChannel Javadoc](https://javadoc.scijava.org/Java7/java/nio/channels/InterruptibleChannel.html)
- **Java fail-fast iterators, grade B.**
  - `ConcurrentModificationException` is thrown "on a best-effort basis".
  - Iterator implementations "may choose" to throw it.
  - Programs must not depend on it for correctness.
  - Otherwise, results of iteration under modification are undefined.
  - Source: [ConcurrentModificationException Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html)
- **Rust ownership and close errors, grade B (official docs and PRs), C (LWN discussion).**
  - `std::fs::File` closes on drop and has no `close()` returning `Result`, so close-time errors are swallowed. `sync_all` is the recommended way to surface errors before drop — [rust-lang PR #123756 commit](https://cdn05042023.gitlink.org.cn/dnrops/rust/commit/b24d2ad300c4864e6fdb88c872365c559d38b241); [LWN 2025](https://lwn.net/Articles/1009302)
  - The async-fs crate states it explicitly: "any errors detected on closing are ignored" — [async_fs::File docs](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html)
- **POSIX close as deferred-failure reporting, grade B.**
  - POSIX.1-2008 left the state of `fildes` unspecified after `close()` fails with EINTR or EIO — [close(3p) man page](https://man.archlinux.org/man/close.3p.en)
  - The Linux man page notes that errors from earlier writes may surface only at close or fsync. It advises `fsync()` before `close()` to detect I/O errors, and says Linux always releases the descriptor — [close(2)](https://man.archlinux.org/man/close.2.en.txt)
  - The Austin Group revisited this for threads (issue 529) — [Austin Group 529](https://www.austingroupbugs.net/view.php?id=529)
  - Per a NetBSD report quoting POSIX.1-2024, after a signal the outcome is unspecified among EINTR with fildes still open, EINPROGRESS with fildes closed, or success. The same report states that NetBSD, FreeBSD, OpenBSD, Linux and illumos all close unconditionally — [NetBSD PR 58929](https://gnats.netbsd.org/58929)

### Inferences
- (inference) Every method surveyed states deferred failure as a *postcondition of a later operation in a given state*, not as a property of the call that created the resource. "Fail after return" therefore needs:
  1. a typestate or protocol state for the stream;
  2. per-operation exceptional postconditions, e.g. `read` in OPEN may signal a transient or terminal error kind;
  3. a transition rule for what happens after such an error, e.g. OPEN → FAILED, where only `close` is legal.
- (inference) Use-after-close is covered by three distinct precedents, a deliberate choice a spec must make:
  - typestate makes it a static error;
  - Python and Java make it a defined runtime error;
  - Java CME and C undefined behaviour make detection best-effort or behaviour undefined.
- (inference) POSIX close and Rust drop show a recurring hazard: the operation that ends the lifecycle is also where buffered or deferred errors surface. A lifecycle spec should say explicitly whether `close` can report errors, whether the resource is released even when it does, and whether repeated close is a no-op (Java `Closeable`) or unspecified (`AutoCloseable`).
- (inference) Interface automata fit the "realities" problem: backends differ in *input assumptions* (what call orders they tolerate) and *output guarantees*. Alternating refinement gives a precise rule for "backend X refines the abstract stream protocol". The known weakness that output cannot be required means liveness ("read eventually returns or fails") needs a separate mechanism.
- (inference) Running example, once decided, in typestate or PSM form:
  - states: `Open`, `Exhausted`, `Failed`, `Closed`;
  - `read`: Open→Open | Open→Exhausted (returns empty) | Open→Failed (signals E);
  - `close`: any state → Closed;
  - any operation other than `close` in Closed signals the "closed" error;
  - every transition carries a pre- and postcondition.

### Gaps
- Not fetched: Aldrich et al. typestate-oriented programming (Plaid), Bierhoff & Aldrich access permissions, Java `Stream`/`BaseStream.close` and `Iterator` Javadoc, C#/.NET `IDisposable` contract, and Tov & Pucella affine types. All are relevant but unsourced here.

## Q3. Saying "deliberately unspecified": loose specs, C standard terms, RFC 2119

### Takeaway
Established specs separate four strengths of non-commitment:
- **unspecified**: one of a set of allowed outcomes, undocumented;
- **implementation-defined**: one of a set, and the implementation must document which;
- **undefined**: no requirements at all;
- **optional (MAY)**: an allowed variation, with a duty to interoperate.

Contract languages express the first two as loose or nondeterministic postconditions (a relation, not a function). "Implementation-defined" maps cleanly to per-backend documentation (P3).

### Cited Findings
- **C11 §3.4 terms, grade B (ISO standard, via secondary sources quoting it).**
  - Implementation-defined behaviour is "unspecified behavior where each implementation documents how the choice is made".
  - Undefined behaviour is behaviour "for which this International Standard imposes no requirements". It is signalled by violated "shall" clauses, explicit wording, or "omission of any explicit definition".
  - Unspecified behaviour is where the standard provides "two or more possibilities and imposes no further requirements on which is chosen", e.g. argument evaluation order.
  - Sources: [Susam Pal: C Standard Terms for Behaviour](https://susam.net/c-standard-terms-for-behaviour.html) (C, quotes standard); [ISO/IEC JTC1 SC22 WG23 N0245](https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf) (B)
- **RFC 2119 MAY, grade B (IETF BCP 14).**
  - MAY/OPTIONAL means "truly optional". One vendor may include an item for market reasons and another omit it.
  - An implementation that lacks an option "MUST be prepared to interoperate" with one that has it, and vice versa, "though perhaps with reduced functionality".
  - Key words "MUST only be used where it is actually required for interoperation or to limit behavior which has potential for causing harm".
  - Source: [RFC 2119](https://rfc-editor.org/rfc/rfc2119)
- **Best-effort as a spec form, grade B.** Java's fail-fast guarantee is explicitly best-effort and must not be relied on for correctness — [ConcurrentModificationException Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html)
- **Short reads as deliberate underspecification, grade B (PEP 3116).** Raw reads "may return a short read without any particular reason". Buffered reads may return fewer than n bytes only at EOF or when non-blocking — [PEP 3116](https://peps.python.org/pep-3116/)
- **POSIX "unspecified" used for lifecycle state, grade B.** The state of fildes after an interrupted close is unspecified, see Q2. This is an example of a standard choosing "unspecified among listed outcomes" because real implementations differed — [NetBSD PR 58929](https://gnats.netbsd.org/58929); [Austin Group 529](https://www.austingroupbugs.net/view.php?id=529)
- **Rust non-exhaustive error kinds, grade B.** `ErrorKind` is `#[non_exhaustive]`: the list "is intended to grow over time", and exhaustive matching is not recommended. This leaves the error set itself deliberately open — [std::io::ErrorKind (nightly)](https://doc.rust-lang.org/nightly/std/hash/../io/enum.ErrorKind.html)

### Inferences
- (inference) For "latency, request count, buffering", the PEP 3116 pattern is the closest precedent: state the observable envelope (n bytes or fewer, empty means EOF) and say explicitly that how the envelope is filled is unconstrained. In contract terms this is a loose postcondition `0 < len(result) ≤ n ∨ (len(result)=0 ∧ at_eof)`.
- (inference) A four-level vocabulary (unspecified / backend-documented / undefined / optional) gives P3 a home: "implementation-defined" means "stated in the backend's own spec page", never in the shared spec.
- (inference) "Undefined" in the C sense is usually wrong for a library boundary that must work without seeing the implementation (P5), because callers cannot test against it. Python and Java prefer a defined error for use-after-close.

### Gaps
- I could not fetch the C11 text itself (N1570), so the quotations are second-hand. Formal treatments of loose specification (e.g. VDM looseness, refinement calculus) were not sourced.

## Q4. Error classification: separating category from mechanism

### Takeaway
Mature specs put error *category* (what the caller should do) in a small closed or extensible enum, and let the *mechanism* (type, code, message) carry it. gRPC defines the category by the caller's recovery action: retry the call, retry the higher-level transaction, or fix state first. Rust and Python attach categories (`ErrorKind`, the `OSError` subclass hierarchy) to a single error type. POSIX lists errno values per function. HTTP ties retry safety to method idempotency rather than to the error.

### Cited Findings
- **gRPC status codes, grade B (official guide).** The decision test is how far up the caller must go:
  - UNAVAILABLE if the client can retry just the failing call;
  - ABORTED if it should retry at a higher level (restart a read-modify-write);
  - FAILED_PRECONDITION if it should not retry until system state is explicitly fixed (example: rmdir on a non-empty directory).
  - Source: [gRPC Status Codes](https://grpc.io/docs/guides/status-codes/); mirror [gRPC statuscodes.md](https://fuchsia.googlesource.com/third_party/grpc/+/refs/tags/v1.23.1/doc/statuscodes.md)
  - Third-party tables differ on default retry policies, e.g. ABORTED listed as retryable — [YDB gRPC codes](https://ydb.tech/docs/en/reference/ydb-sdk/grpc-status-codes) (C)
- **Rust `io::ErrorKind`, grade B.**
  - `Interrupted`: operations "can typically be retried".
  - `UnexpectedEof`: premature end of file.
  - `read_exact` never returns `Interrupted`. On failure the read position may have advanced by any amount up to the request.
  - Sources: [ErrorKind docs](https://doc.rust-lang.org/nightly/std/hash/../io/enum.ErrorKind.html); [RFC 0980 read_exact](https://rust-lang.github.io/rfcs/0980-read-exact.html)
- **Exceptions in behavioural subtyping, grade A.** Subtype methods may only signal exceptions that are subtypes of the supertype's — [Liskov & Wing 1994](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf). JML's `signals_only` makes the allowed exception set an explicit, checkable clause — [JML Reference Manual ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html)
- **Python exception hierarchy as contract, grade B.** `io.UnsupportedOperation` inherits from both `OSError` and `ValueError` and is raised when an unsupported operation is called on a stream. Operations on a closed file raise `ValueError` ("I/O operation on closed file") — [Python 3.7 io docs](https://docs.python.org/fr/3.7/library/io.html); [CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c)
- **HTTP retry and idempotency.**
  - RFC 9110 §9.2.2 lists GET, HEAD, PUT, DELETE, OPTIONS and TRACE as idempotent. This is per secondary sources; I could not verify the RFC 9110 text — [GitLab client-go MR](https://gitlab.com/gitlab-org/api/client-go/-/merge_requests/2945) (C)
  - An IETF draft states a user agent must not automatically retry a non-idempotent request unless it knows the request is idempotent or was never applied — [draft-nottingham-httpbis-retry](https://datatracker.ietf.org/doc/html/draft-nottingham-httpbis-retry) (B, draft)
  - GitLab's client retries 429 for all methods, reasoning that the request was rejected before processing — [GitLab MR 2945](https://gitlab.com/gitlab-org/api/client-go/-/merge_requests/2945) (C)
- **POSIX per-call errno lists, grade B.** close() lists EBADF, EINTR and EIO, each with stated consequences for descriptor state — [close(3p)](https://man.archlinux.org/man/close.3p.en)

### Inferences
- (inference) The gRPC criterion of classifying by caller recovery action, not by cause, is the most backend-neutral category scheme found. It lets each backend map its own mechanisms (HTTP 503, ECONNRESET, a driver exception) to one category in its own backend spec (P3). The shared spec then states only the category per operation and state (P2).
- (inference) Rust's `read_exact` note ("position may have advanced by any amount") is a precedent for specifying the *observable partial effect* of a failed call loosely, rather than promising atomicity.
- (inference) Python's dual-inheritance trick (`UnsupportedOperation` is both `OSError` and `ValueError`) shows a cost of using exception hierarchies as the category mechanism: one error can belong to two categories, which works against one home per rule (P2).

### Gaps
- Not fetched: Go's `errors.Is`/`errors.As` and `io.EOF` sentinel conventions, `fs.ErrNotExist`, Google AIP-193/194, AWS SDK retryable classification, and the full Python `OSError` subclass-to-errno mapping (PEP 3151). These are strong candidates for the report but unsourced here.

## Q5. Python-relevant and other read-stream boundary specs (form and guarantee style)

### Takeaway
PEP 3116 / `io` is a layered behavioural spec. Each layer (Raw, Buffered, Text) has its own contract strength for the same `read` name:
- raw allows arbitrary short reads and returns `None` when non-blocking with no data;
- buffered returns short only at EOF or when non-blocking, and raises `BlockingIOError` instead of returning `None`.

This is a documented precedent for "same operation, different guarantee strength per layer or reality". fsspec exposes buffering policy as caller-visible parameters (`cache_type`, `block_size`) rather than leaving it unspecified.

### Cited Findings
- **PEP 3116, grade B.** RawIOBase `read` returns `None` for a non-blocking object with no bytes available, and may return a short read "without any particular reason". Buffered `read` "may return fewer than n bytes if end-of-file is reached or the object is non-blocking" — [PEP 3116](https://peps.python.org/pep-3116/)
- **CPython buffered I/O, grade B (source docstring).** Buffered `read`/`readinto`/`write` may raise `BlockingIOError` in non-blocking mode and "will never return None", unlike raw — [CPython bufferedio.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/3.1/Modules/_io/bufferedio.c)
- **Conflict.** The library reference reportedly allows implementations either to raise `BlockingIOError` or to return `None`. I could not read docs.python.org directly to confirm the current wording. The search extract reported this conflict with the source docstring — [Python io docs (3.7 mirror)](https://docs.python.org/fr/3.7/library/io.html)
- **IOBase closed-state contract, grade B.** `close()` on an already-closed file has no effect, and operations on a closed file raise `ValueError` — [CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c); [Python 3.7 io docs](https://docs.python.org/zh-tw/3.7/library/io.html)
- **fsspec, grade B/C (official source pages, third-party doc mirror).**
  - Built-in read caches are `mmap`, `readahead`, `blockcache`, `bytes` and `background`, selected per open via `cache_type`/`block_size`, with filesystem-level defaults.
  - Block cache memory is bounded by `blocksize * maxblocks`.
  - Caching filesystems work only with files deriving from `AbstractBufferedFile`.
  - Sources: [fsspec.caching source](https://filesystem-spec.readthedocs.io/en/stable/_modules/fsspec/caching.html); [fsspec cached.py](https://filesystem-spec.readthedocs.io/en/stable/_modules/fsspec/implementations/cached.html); [tessl fsspec caching doc](https://tessl.io/registry/tessl/pypi-fsspec/files/docs/caching.md) (C)
- **Java NIO channel close semantics, grade B.** See Q2: asynchronous close produces a defined exception in the blocked reader — [InterruptibleChannel](https://javadoc.scijava.org/Java7/java/nio/channels/InterruptibleChannel.html)

### Inferences
- (inference) The io layering is a working instance of P3: the *shared* name `read` carries a weakest common contract, and each class documents its strengthening. A multi-backend library could put "may short-read" in the abstract spec and "returns exactly n unless EOF" in a backend's stronger spec, consistent with behavioural subtyping.
- (inference) fsspec makes buffering an explicit parameter, the opposite pole from "unspecified". A spec has to choose per property whether it is a caller-controlled parameter, a documented per-backend value (implementation-defined), or unspecified.

### Gaps
- Not read: fsspec `AbstractBufferedFile` docstrings (`spec.py`), PyFilesystem2 `FS.openbin` and its error mapping (`fs.errors`, `convert_os_errors`), Java NIO `FileSystemProvider.newInputStream`/`newByteChannel` contract, POSIX `read()` page (EINTR, EAGAIN, EIO, short reads), and Python `io` current docs for `RawIOBase.readinto`/`__del__`. All are high-value but blocked or out of budget.

## Q6. Limits of each method against observers, environment, partial failure, and principles P1–P5

### Takeaway
Single-call contracts meet P1, P2 and P5 well but stop at the call boundary. They need an abstract environment model to talk about failures caused by the outside world, and they cannot state deferred failure on their own. Lifecycle methods (typestate, PSM, session types, interface automata) cover deferred failure and use-after-close, but mainly as *safety* (allowed sequences). They state liveness and data content weakly. Error-classification schemes are the main tool for keeping backend mechanisms apart (P3). P4 (each claim names its check) is best supported where clauses are executable assertions (Eiffel/JML runtime checking) or derivable tests (PSM → contracts → tests).

### Cited Findings
- Interface automata cannot require outputs, so liveness is not expressible — [Lüttgen & Vogler TR](https://opus.bibliothek.uni-augsburg.de/opus4/files/2006/TR_2012_09.pdf)
- Typestate's main technical obstacle is aliasing and sharing; Fugue needs linear-type machinery — [DeLine & Fähndrich 2004](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/)
- Protocol states need not match internal states, so PSMs are an observer-level view. Operation contracts do not give a classifier-level overview — [OMG UML14-209](https://issues.omg.org/issues/UML14-209)
- PSMs can be compiled into per-operation contracts usable as run-time checks or for test generation — [UCC: generating class contracts from UML PSMs](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/)
- Best-effort detection (Java CME) and documented non-idempotence (`AutoCloseable`) show specs knowingly stating guarantees that cannot be checked by the compiler or relied on by the caller — [CME Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html); [Enthuware forum](https://enthuware.com/forum/viewtopic.php?p=7359) (C)
- Ownership or drop-based closing loses close-time errors unless the API adds an explicit fallible finaliser — [LWN](https://lwn.net/Articles/1009302); [async_fs::File](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html)
- Sparing use of normative key words ("only where actually required for interoperation") — [RFC 2119](https://rfc-editor.org/rfc/rfc2119)

### Inferences
Method-by-principle matrix (all inference):

| Method | P1 what-not-how | P2 one claim/unit | P3 backend apart | P4 names its check | P5 no impl view | Partial/deferred failure | Environment |
|---|---|---|---|---|---|---|---|
| DbC/Eiffel | yes, via queries | per clause | via inheritance | runtime assertions | yes, if public queries suffice | only "routine fails"; no later failure | implicit |
| JML/Dafny | yes, model fields | per spec case | behavioural subtyping | RAC/static verification | yes | `signals` per op; later failure needs state | must be modelled |
| Larch/VDM/Z | strongest (abstract math tier) | per op | via refinement | proof, not tests | yes | error schemas/cases | modelled as state |
| Typestate | yes | per transition | subclass refinement (Fugue) | static checker | yes | via FAILED state | no |
| UML PSM | yes | per transition | weak | derivable tests | yes | via states | no |
| Session types/IA | yes | per protocol step | alternating refinement | type/game check | yes | protocol branches | explicit (IA input assumptions) |
| Error-category enums | n/a | one category per meaning | mechanism mapping per backend | test per category | yes | category says recovery action | n/a |

- Weak points against the running example's three hard cases:
  1. **Mid-read failure** needs both a lifecycle model and an error-category scheme.
  2. **Resource outliving the call** needs `fresh(result)` plus typestate.
  3. **Use-after-close** needs an explicit choice between static error, defined runtime error and unspecified/undefined.

  Precedents exist for each choice (typestate / Python ValueError / Java CME best-effort / C UB).

### Gaps
- No measured studies (grade A empirical) were found on how well these methods work for multi-backend library specs. The evidence base is mostly formal-methods papers (A, conceptual) and standards/docs (B). Empirical work on contract usage, e.g. Estler et al. 2014 "Contracts in practice" and Dietrich et al. on Java contracts, was not retrieved and should be checked.
