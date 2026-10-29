# D3: Python-native and single-source options (with disconfirming search §4(c))

How to read the tags. Each finding carries `[grade | full text read | n and setting | what "correct" meant | transfer | agents | independence]`.
- *Transfer* is *direct* (library or API behaviour specs), *analogous* (other spec domains) or *inference*.
- *Agents* says whether agents or LLMs were measured doing this step. "human-only" means no agent evidence.
- *Independence*: **TA** = tool authors evaluating their own tool; **V** = vendor post or vendor repo; **ind** = independent of the tool authors.
- "Own trial" means this track's own small measurement, run in a scratchpad venv. Setup: Python 3.13.17; crosshair-tool 0.0.112, deal 4.24.6, icontract 2.7.3, hypothesis 6.170.13, hypothesis-crosshair 0.0.31, detangle 0.1.0, itf-py 0.5.0, Quint 0.33.1 (npm). Scripts are in `/tmp/claude-0/-home-user-research/8464aabb-24d6-53c7-af9a-cc609bb4c0f8/scratchpad/d3/scripts/`. Each trial is n = 1 toy operation, so these are illustrations, not effectiveness data.
- Maturity data comes from the PyPI JSON API (`pypi.org/pypi/<pkg>/json`, read 2026-10-29) and from `git log` on blob-less clones. GitHub API data (stars, open issues) could **not** be read: `gh api` returned "GitHub access to this repository is not enabled for this session".

---

## Q1. Python tools: capability, maturity and measured effectiveness

### Takeaway
- **Hypothesis**, including `RuleBasedStateMachine`, is the only tool here that is mature, actively maintained and backed by independent effectiveness data. That data covers mutant kills by PBTs in Python projects, and it is stateless.
- **CrossHair** is actively developed but is a 0.0.x tool, essentially single-maintainer, with no peer-reviewed evaluation. It is useful as a per-function counterexample search over contracts, not as a gate that claims proof.
- deal's prover is experimental by its own docs. icontract is in maintenance mode. icontract-hypothesis is dormant.
- No mature Python linearizability or history checker exists. The options are a one-month-old library (detangle), an unreleased causal-consistency checker (c3py), or calling Porcupine (Go) or Elle (JVM) out of process.

### Cited Findings

**Maturity (PyPI and git; B, full text read; V/TA by nature).**

| Package | Releases (first → latest) | Releases in last 12 months | Commit activity | Maintainers in last 12 months |
|---|---|---|---|---|
| hypothesis | 1,592 (2013-03 → 6.170.13, 2026-10-28) | 144 | — | — |
| crosshair-tool | 112 (0.0.1, 2020-02 → 0.0.112, 2026-10-23) | 15 | 305 (2024), 163 (2025), 285 (2026) | 224 of ~287 commits by Phillip Schanely; next: "Claude" 39, one other person 16 |
| hypothesis-crosshair | 29 (2024-03 → 0.0.31, 2026-10-06) | 6 | — | — |
| deal | 68 (2018-01 → 4.24.6, 2025-11-30) | 1 | 343 (2021) → 16 (2024), 25 (2025); last 2025-11-30 | 3 commits in total |
| deal-solver | 3 (latest 0.1.2, 2023-09-28) | 0 | — | — |
| icontract | 64 (2018-07 → 2.7.3, 2026-01-29) | 2 | 8 (2025), 2 (2026) | Marko Ristin only |
| icontract-hypothesis | 11 (2020-12 → 1.1.7, 2021-07-23) | 0 | last commit 2022-06-05 | dormant |

Sources: [PyPI crosshair-tool](https://pypi.org/pypi/crosshair-tool/json); [PyPI deal](https://pypi.org/pypi/deal/json); [PyPI icontract](https://pypi.org/pypi/icontract/json); [PyPI icontract-hypothesis](https://pypi.org/pypi/icontract-hypothesis/json); [PyPI hypothesis](https://pypi.org/pypi/hypothesis/json); [PyPI hypothesis-crosshair](https://pypi.org/pypi/hypothesis-crosshair/json); git clones of [CrossHair](https://github.com/pschanely/CrossHair), [deal](https://github.com/life4/deal), [icontract](https://github.com/Parquery/icontract) and [icontract-hypothesis](https://github.com/mristin/icontract-hypothesis).

**CrossHair: capability and limits.**
- **What it does.** It calls functions with symbolic proxy inputs and an SMT solver to find counterexamples to contracts. It supports PEP 316 docstrings, icontract and deal (postconditions and invariants for icontract; postconditions for deal). It also offers `cover` (test generation) and `diffbehavior` (finds inputs on which two functions differ). It now runs as an optional Hypothesis backend. — [CrossHair README](https://raw.githubusercontent.com/pschanely/CrossHair/main/README.md); repo docs `kinds_of_contracts.rst`, `diff_behavior.rst` [B | yes | docs | — | direct | human-only | TA]
- **Limitations, verbatim from its docs.**
  - "the absence of a counterexample does not guarantee that the property holds"
  - the proxy "illusion is not complete" (for example identity `x is y`)
  - "Only deterministic behavior can be analyzed"
  - only top-level functions and classes are analyzed
  - sandboxing via audit hooks "is not perfect"

  — [limitations.rst](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/limitations.rst) [B | yes | docs | — | direct | human-only | TA]
- **Measured effectiveness.** No peer-reviewed or arXiv evaluation of CrossHair was found. The search returned only a Tessl "tile" rubric, which is an agent-skill registry, not an evaluation. The only quantitative self-measurement is the repo's `doc/source/measured.json` (refreshed 2026-07-21), which covers 2,403 stdlib callables:

  | Colour | Count |
  |---|---|
  | green | 507 |
  | red | 159 |
  | yellow | 36 |
  | black | 25 |
  | "?" | 1,676 |

  The most common verdicts are "no inputs" 781, "no drivable signature" 621, "handled at every size" 436, "no valid input found" 133, "only the trivial case" 120 and "side effect" 88. The colour semantics are not defined in the files read. *Inference*: about 21 % of stdlib callables are handled symbolically "at every size", and about 70 % of the drivable ones. — [measured.json](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/measured.json) [C | yes | 2,403 stdlib callables | symbolic support, not bug finding | inference | human-only | TA]

**deal.**
- **Features.** Runtime DbC (pre, post, ensure, raises, side-effect tracking), a linter, Hypothesis-based test generation and a z3-based prover. The verification docs say verbatim: "This feature is **experimental** and always will be" and "It will work for only 1% of your code". The prover requires pure, fully annotated functions, and "some mutability bugs … cannot be detected by deal-solver because there is no conception of mutability". — [deal README](https://raw.githubusercontent.com/life4/deal/master/README.md); [verification.md](https://raw.githubusercontent.com/life4/deal/master/docs/basic/verification.md) [B | yes | docs | — | direct | human-only | TA]
- **Effectiveness data.** None found.

**icontract-hypothesis.** It infers Hypothesis strategies from icontract preconditions and falls back to filtering for the rest. The earlier report already notes "no effectiveness data". This track adds that it has had no release since 2021-07 and no commit since 2022-06 (git, above).

**Hypothesis, independent effectiveness.**
- **Ravi & Coblenz**, "An Empirical Evaluation of Property-Based Testing in Python", PACMPL OOPSLA 2025 (venue verified via [Crossref 10.1145/3764068](https://api.crossref.org/works/10.1145/3764068)). Full text **[unreachable]**: dl.acm.org returned 403 to both curl and WebFetch. The artifact README states the claims verbatim:
  - "Unit tests comprised 98.4% of our sample and killed 84.7% of the total mutations found, while PBTs (comprising 1.6%) killed 15.3% … On a per-test basis, property-based tests were more effective"
  - "55% [of mutations] were found with a single input to a PBT. 76% … within the first 20 inputs … 96% within the first 350 inputs"
  - The most common PBT types are "equality with constants (41%…), commutative paths (24%…), and roundtrips (7%…)".

  The corpus size (426 programs; mutation testing on 40 projects) and the "about 50× per test" figure come from a search extract only. — [python-pbt-eval README](https://raw.githubusercontent.com/ucsd-salad/python-pbt-eval/main/README.md) [A venue, claims from the artifact README; full paper unreachable | no | Python OSS projects with Hypothesis tests | mutant killed | analogous (general Python code, not behaviour specs) | human-only (human-written PBTs) | ind]
  - It does not appear to separate stateful (`RuleBasedStateMachine`) tests. *Inference* from the README categories; unverified without the full text.
- **MacIver & Donaldson**, "Test-Case Reduction via Test-Case Generation: Insights from the Hypothesis Reducer", ECOOP 2020, LIPIcs 166, 13:1–13:27. Full text read. — [PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf) [A | yes | Csmith/gcc/clang, yapf/black differential, SymPy via TSTL harness, SmartCheck benchmarks | "correct" = reduced test still triggers the same failure | analogous | human-only | TA (MacIver wrote Hypothesis)]
  - The authors call the evaluation "mostly intended to be descriptive".
  - **Formatter study**: Hypothesis, Picire and C-Reduce produced comparable sizes, with non-significant differences. Hypothesis made about 50 % more SUT calls than Picire.
  - **Csmith study**: C-Reduce and Picire produced substantially smaller programs. Hypothesis made about 4× fewer SUT calls than Picire.
  - **SymPy** (2,930 non-flaky failing cases, 33 distinct errors): Hypothesis made 20.6× as many SUT calls as delta debugging, for tests 83 % of the size.
  - The key property is "reduced test cases are ones that could have been generated" (no test-case validity problem). This matters for state-machine tests, because shrunk call sequences still respect rule preconditions. *Inference*.
- **Hypothesis JOSS paper** (MacIver, Hatfield-Dodds et al., JOSS 4(43) 1891, 2019). A two-page software paper: "over 100,000 downloads per week", "more than 4% of Python users surveyed by the PSF" (2018), bugs found in astropy and numpy. It has no effectiveness evaluation. — [JOSS PDF](https://www.theoj.org/joss-papers/joss.01891/10.21105.joss.01891.pdf) [B | yes | — | — | analogous | human-only | TA]

**Own trial 1: CrossHair on icontract and deal contracts** (`t/ic_store.py`, `t/ic_fixed.py`). [own trial | yes | 1 toy `put` with capacity 3 and a seeded off-by-one | "correct" = the contract `len(store) <= CAP` holds | direct (toy API op) | human-only | ind]
- `crosshair check --analysis_kind=icontract` found a counterexample for the seeded bug in **40.5 s** wall time. The deal analysis kind found it in **27.7 s**.
- After the bug was fixed, CrossHair **still** reported a counterexample: an input store that already had 4 keys. The contract lacked the precondition `len(store) <= CAP`, so CrossHair exposed a **missing precondition** (spec incompleteness), not an implementation bug.
- With the precondition added, it found no counterexample in **150 s** (both analysis kinds, per-condition timeout 30 s). That is absence of a counterexample, not proof.
- *Inference*: this behaviour is useful to Pipeline A as an "under-constrained contract" probe, the same pattern IronSpec reports below for too-weak specs.

**Own trial 2: `deal test`.** It produced no output for the mutating `put`. Its help says it runs against "pure functions", so it does not apply to stateful operations without refactoring. [own trial | yes | same toy | — | direct | human-only | ind]

**Own trial 3: Hypothesis `RuleBasedStateMachine`** (`t/sm_store.py`). An implementation is compared step by step to a dict reference model. The seeded bug needs the sequence put → delete → put(negative) → get.
- **Default backend** (200 examples): found in **10 of 10** seeds, 0.6–1.5 s per run. It shrank every time to the minimal 4-step sequence `put(c,0); delete(c); put(c,-1); get(c)`.
- **CrossHair backend** (100 examples, 1 run): **did not find it** in 31 s.

[own trial | yes | n = 1 bug, 10 seeds (default) and 1 run (CrossHair) | "correct" = impl output equals model output on every `get` | direct (toy store API) | human-only | ind]

**Python history and linearizability checkers.**
- **Porcupine** is Go, Knossos is Clojure, Elle is Clojure/JVM. Elle can be driven from any language via **elle-cli**, which takes EDN input (JSON via a converter). These are search leads; the elle-cli page was not fetched. — [elle-cli](https://www.github.com/ligurio/elle-cli) [lead only | no]
- **detangle 0.1.0.** One release (2026-09-26). It is a deterministic asyncio simulation tester with "a linearizability checker (Jepsen-style)": "A Wing & Gong / Lowe search with P-compositionality, like Knossos and Porcupine, with ready-made models (register, KV, queue, set, counter, mutex) and support for operations of unknown outcome". It offers a pytest plugin and replay tokens. Simulated I/O only ("Real sockets, subprocesses and signal handlers raise `detangle.RealIOError`"). — [PyPI detangle](https://pypi.org/pypi/detangle/json) [B | yes (PyPI long description) | — | — | direct | human-only | TA]
- **Own trial 4: detangle.** A non-atomic counter with 3 concurrent clients raised `NotLinearizable` in 0.43 s, with a replay token. The atomic version passed (0.48 s). `detangle.lin.check(operations, model, budget=5000000)` accepts recorded `Operation` lists, so offline histories from R could be checked. Only the signature was inspected; that path was not exercised. [own trial | yes | 1 seeded race | linearizable w.r.t. the counter model | direct | human-only | ind]
- **c3py** (shumbo) is a Python causal-consistency checker based on Bouajjani et al. Its README says "still under active development and the API is subject to change". The last commit was 2024-02-23. The PyPI name `c3py` belongs to an unrelated numerics package. — [c3py README](https://raw.githubusercontent.com/shumbo/c3py/main/README.md) [B | yes | — | — | direct | human-only | TA]
- No neutral benchmark of any Python history checker was found. This extends the earlier report's open item 17.

### Inferences
- *Inference*: for Pipeline A's G6 ("contract → PBT and state-machine conformance"), the Python stack has a clear split:
  - Hypothesis stateful testing carries the weight.
  - icontract (or deal) provides runtime contracts on R.
  - CrossHair is an optional, time-boxed counterexample search per pure helper. It catches under-constrained contracts as a side effect.
- *Inference*: CrossHair's bus factor (≈ 1 human maintainer, 0.0.x versioning) and its determinism requirement make it unsuitable as a blocking gate. Treat its silence as "no counterexample within budget".
- *Inference*: for history forms, the practical Python route today is one of:
  - record histories from R or the implementation and check them out of process with Porcupine (Go) or elle-cli;
  - adopt detangle with the risk of a brand-new single-release project;
  - write a small WGL checker against R's sequential mode, which is a known algorithm but untested code.

### Gaps
- No peer-reviewed effectiveness data for CrossHair, deal or icontract. The only data are author self-measurements.
- The Ravi & Coblenz full text is unreachable (ACM 403). The n, the stateful-vs-stateless split and threats to validity are not verified.
- GitHub stars and open-issue counts are unavailable (GitHub API blocked).
- No empirical study of `RuleBasedStateMachine` effectiveness specifically was found. Only one source (Ravi & Coblenz, via its README) carries the "Python PBT effectiveness" answer.

---

## Q2. One executable source: Dafny→Python, Lean, Quint, P

### Takeaway
- Only **Dafny** literally generates a Python reference model from a verified source. Its compilers, including the Python back-end, have a documented record of miscompilation and soundness bugs found by fuzzing, and the interop documentation is thin.
- **Lean** gives a fast, proof-backed executable model (the Cedar precedent), but no Python binding was found. It would be an oracle called over FFI or a subprocess, not the Python R.
- **Quint** is the most usable oracle: its simulator is seedable and emits machine-readable ITF traces that a Python R can replay. But it does not generate Python. It checks a separately written R, which is a two-source design.
- **P** has no Python output. PObserve checks logs against P specs on the JVM. It is usable as an independent log or history check, not as R.

### Cited Findings

**Dafny → Python.**
- The integration guide covers `dafny build --target:py` and `dafny run --target:py`. It needs the Python runtime library, which is bundled only when `dafny` compiles, not when it only translates. "There is no syntax in Dafny to insert such `import` statements in the `.py` file", and "To call python from Dafny, one must edit the translation". The type table maps Dafny `int`, `int64`, `char` and bitvectors to Python `int`. The doc still says "currently (as of v3.9.1)". — [IntegrationPython.md](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/integration-py/IntegrationPython.md) [B | yes | docs | — | direct | human-only | V (Dafny project)]
- The runtime is published as `DafnyRuntimePython` 4.11.0 on PyPI. — [PyPI](https://pypi.org/pypi/DafnyRuntimePython/json) [B | yes]
- **Donaldson, Sheth, Tristan & Usher, ICST 2024** (venue via Crossref 10.1109/icst60714.2024.00044). The fuzzers fuzz-d and DafnyFuzz found "24 previously-unknown Dafny compiler bugs … of which 9 are soundness issues". The campaign "led to changes to the Dafny language specification via the identification of ambiguous or under-documented language features". — [PDF](https://www.doc.ic.ac.uk/~afd/papers/2024/ICST.pdf) [A | yes | Dafny compiler, 5+ back-ends | "correct" = agreement across back-ends, metamorphic relations, known expected output | analogous (compiler fidelity) | human-only | TA (tool authors; one AWS co-author)]
  - The bug table's component column implicates the Python back-end in 5 rows: "Compiler (Python)" ×3, "(C#, Python)", "(Python, JS)". The column alignment came from pdftotext and should be re-checked against the PDF.
  - Python examples include a runtime overflow on multiset multiplicity 2^64. The paper calls this "a missed implementation detail in the C# and Python back-ends".
- **Irfan et al., "Testing Dafny (experience paper)", ISSTA 2022.** XDsmith found "31 bugs across the Dafny verifier and compilers", using differential testing over the C#, Java, Go and JS compilers. Python was not targeted at the time. — [PDF](https://ahmed-irfan.github.io/papers/issta22.pdf) [A | yes (abstract and intro sections read) | Dafny toolchain | known verification outcome, back-end agreement | analogous | human-only | V (Amazon authors)]
- **CompFuzzCI, ICST 2025 industry track** (Crossref 10.1109/icst62969.2025.10988954). Running in Dafny's CI, it "found and reported three previously-unknown bugs in the Dafny compiler". — [PDF](https://www.doc.ic.ac.uk/~afd/papers/2025/ICST-Industry.pdf) [A (industry track) | partial (abstract and intro) | Dafny CI | — | analogous | human-only | TA]
- The fuzz-d MEng report reportedly lists 4 Python-back-end miscompilations. That is a search extract only; the report was not read. [lead only | no]
- Generated-code readability and performance of Dafny→Python: **no source found**. No own trial was possible: the GitHub release download returned 404 and no dotnet is installed.

**Lean 4 (Cedar pattern).**
- Cedar's DRT harness calls the Lean model from Rust. Verbatim: "uses Lean's foreign function interface to call the relevant parts of the Cedar lean formalization", with Protobuf serialisation between Rust and Lean and `libleanshared.so` at runtime. — [cedar-lean-ffi README](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/cedar-lean-ffi/README.md); [cedar-spec README](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/README.md) [B | yes | — | — | analogous | human-only | V]
- Performance, vendor post: "On average, Lean takes 5 microseconds to evaluate a differential testing input, compared to 7 microseconds for Rust". Lean was adopted "because of its fast runtime, extensive libraries, and small trusted computing base". The validator model is "10X smaller than its corresponding Rust implementation". — [AWS Open Source blog](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/) [C | yes | Cedar | — | analogous | human-only | V]
- The earlier verified report already gives Cedar's DRT and bug counts; they are not repeated here.
- No Lean→Python binding or Lean-generated Python was found, though the search for one was not exhaustive. *Inference*: calling a Lean model from pytest needs a subprocess (JSON over stdin/stdout) or a ctypes binding to Lean's compiled C. Neither has a published precedent in the sources read.

**Quint.**
- **Own trial 5** (`scripts/q/`): Quint 0.33.1 simulator plus an ITF replay against a Python R. [own trial | yes | 1 toy store spec (4 keys, capacity 3) | "correct" = `alpha(R state)` equals the ITF `kv` state at every step | direct (toy) | human-only | ind]
  - **Sandbox dependency.** The default `--backend=rust` downloads an evaluator binary from GitHub at first use. That failed here ("Failed to fetch from GitHub: Forbidden"). `--backend=typescript` works.
  - **Simulator speed.** `quint run --invariant` found the seeded capacity bug in the spec in 20 ms. 10,000 samples × 20 steps of the correct spec took 3.4 s.
  - **Determinism.** The same `--seed` gave identical ITF `states` across runs; only the `#meta` timestamp differs.
  - **`--mbt` output.** The flag ("(experimental)") adds `mbt::actionTaken` and `mbt::nondetPicks`. `actionTaken` was the **empty string** for the `doPut` action (whose body is an `any`), while `doDel` was labelled. The cause was not investigated.
  - **itf-py bug.** `itf-py` 0.5.0 **crashed** decoding the `--mbt` output (`ValueError: Type names and field names cannot be a keyword: 'None'`, from the Option `None` variant).
  - **Replay result.** With a 25-line plain-JSON replay, 50 traces gave **0 divergences** for the correct Python R and **20/50 divergent traces** for an R seeded to admit a 4th key.
- `itf-py` ("parse and emit Apalache/Quint traces in ITF JSON") is at 0.5.0 (2026-02-17). — [PyPI itf-py](https://pypi.org/pypi/itf-py/json) [B | yes]
- Quint's npm package 0.33.1 was published 2026-10-28, with 0.33.0 on 2026-09-28. — [npm registry](https://registry.npmjs.org/@informalsystems/quint) [B | yes]
- No Quint→Python code generator was found.

**P.**
- The compiler's output enum is `PChecker, PObserve, PEx, PVerifier`. The PObserve back-end contains `JavaSourceGenerator.cs` and `FFIStubGenerator.cs`, so P monitors compile to Java for PObserve. There is no Python target. The last commit is 2026-08-03. — git clone of [p-org/P](https://github.com/p-org/P), `Src/PCompiler/CompilerCore/CompilerOutput.cs`, `Backend/PObserve/` [B | yes (source tree) | — | — | analogous | human-only | V (AWS-led)]
  - The official site page fetched says C# and C, with Java "in progress", which conflicts with the repo; the repo is newer.
- **PObserve**: "checks formal correctness specifications on systems implementation using service logs". It needs a log parser into PObserve events, a sequencer and a demultiplexer (Java Streams). The page states no limitations. — [PObserve docs](https://p-org.github.io/P/advanced/pobserve/pobserve/) [B | yes (via fetch summary) | — | — | analogous | human-only | V]

### Inferences
- *Inference*: by the brief's own setting ("an **executable reference model in Python**"), only Dafny→Python makes R *the generated artefact of a single source*. With Lean or Quint, R is a second, separately written Python artefact checked against the source by DRT or trace replay. Strictly, that is not a single source. It is a source plus a mechanically checked bridge, closer to Pipeline A or B with a strong F↔R bridge.
- *Inference*: choosing "R itself" as the single source (one of the earlier report's three options) leaves nothing to *generate* the formal layers or the prose. None of the Python tools above derives TLA+, Alloy or prose from Python. CrossHair and deal only check contracts written in Python. "R itself as the source" therefore collapses Pipeline C into Pipeline A.
- *Inference*: Dafny→Python fidelity has to be checked, not assumed. The fuzzing literature's own method suggests one way: build the same Dafny source for Python and for a second back-end (C# or Java), then run DRT between them on Hypothesis-generated inputs. This catches back-end-specific miscompilations. It cannot catch front-end or AST-level errors shared by all back-ends; the fuzz-d report names that limitation, per the search extract.
- *Inference*: usability as an oracle from pytest or Hypothesis:

  | Option | Ranking | How it is called | Main caveat |
  |---|---|---|---|
  | Quint | best | seeded, offline traces | trace replay only covers simulator-reachable paths, not arbitrary Hypothesis inputs |
  | Dafny→Python | good | in-process | — |
  | Lean | medium | subprocess or FFI; deterministic and fast per Cedar | — |
  | P | low | log checking on the JVM | — |

### Gaps
- No measurement of Dafny-generated Python's readability, size or speed.
- No Lean–Python interop precedent.
- No published Quint MBT study with Python.
- No P→Python path.
- Each of these rests on documentation plus one toy trial at most. Only one source carries the Lean performance figure (vendor blog), and only one carries the Python-back-end bug list (ICST 2024).

---

## Q3. Which choice makes Pipeline A or Pipeline C feasible

### Takeaway
- **Pipeline A is feasible today in pure Python.** It uses Hypothesis stateful tests, runtime contracts and optional CrossHair, plus an out-of-process or young history checker.
- **Pipeline C is feasible only in a weakened form.**
  - Strict single source to Python R means Dafny→Python, which needs a back-end-fidelity DRT leg.
  - The practical form is Quint as the executable spec source, with ITF replay against a separately written Python R. That form is no longer single-source.

### Cited Findings
Baseline text being qualified, quoted verbatim from the verified edition §4, Pipeline C:
- "1. One executable formal source per operation (R itself, Quint, or Lean; left open)."
- "2. Markdown prose and other models are **generated** from it."

From Pipeline A: "7. R built; G6 contract → PBT and state-machine conformance."

From the check map, history row: "Spec.: R run concurrently, Porcupine-style check against R's sequential mode".

Evidence used:
- Hypothesis stateful testing works and shrinks well on a sequence bug (own trial 3).
- PBTs are effective per test in Python projects (Ravi & Coblenz, via the artifact README; [A venue, full text unreachable]).
- The Hypothesis reducer keeps shrunk cases valid ([ECOOP 2020, A, TA](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf)).
- CrossHair finds contract counterexamples, including missing preconditions (own trial 1). It has no external evaluation and one main maintainer (PyPI and git, above).
- Dafny back-ends have fuzzing-found soundness bugs, with Python implicated ([ICST 2024, A, TA](https://www.doc.ic.ac.uk/~afd/papers/2024/ICST.pdf)).
- The Quint seeded simulator, ITF and Python replay work, with interop defects (own trial 5).
- Lean via FFI is fast in Cedar ([vendor blog, C](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/)).

### Inferences: recommendations

**R-D3-1. Pipeline A, G6 stack.**
- **Recommendation.** Use Hypothesis `RuleBasedStateMachine` as the conformance driver. Rules mirror operations, the model is R or the spec state through `alpha`, and invariants are spec invariants. Put runtime contracts on R with icontract (maintained, low activity) or deal. Run CrossHair time-boxed on pure helpers and contract-bearing functions as an *advisory* "under-constrained contract" probe.
- **Confidence.** Medium-high for Hypothesis. Low for CrossHair as anything beyond advisory.
- **Load-bearing sources.** Ravi & Coblenz (README claims); ECOOP 2020; own trials 1 and 3; PyPI and git maturity data.
- **Would be overturned by.** A study showing that Python stateful PBT misses most seeded clause misreadings that example-based expectation tests catch, at equal test counts.

**R-D3-2. Pipeline A and C, history forms.**
- **Recommendation.** Record histories from R or the implementation as JSON and check them with Porcupine (Go, subprocess) against R's sequential semantics re-expressed as a Porcupine model. Alternatively, pilot detangle's `lin.check`, but only after it survives a seeded-history calibration (a known non-linearizable and a known linearizable set).
- **Confidence.** Medium.
- **Load-bearing sources.** The earlier report's Porcupine row; detangle PyPI; own trial 4.
- **Would be overturned by.** detangle (or any Python WGL checker) disagreeing with Porcupine on a shared history corpus, or a Python checker with published neutral benchmarks appearing.
- Caveat: R's sequential semantics would have to exist twice, once in Python and once in the Porcupine model. That is itself a bridge to review (*Inference*).

**R-D3-3. Pipeline C, the executable source.** Drop "R itself" from the option list.
- **(a) If a literal single source to Python R is required, use Dafny→Python**, with a mandatory back-end DRT leg (Python build vs C#/Java build, Hypothesis inputs) and a pinned Dafny version.
- **(b) Otherwise use Quint as the executable spec source.** Generate seeded `--mbt` traces and replay them against a Python R through the reviewed `alpha`. Write and own a small ITF decoder rather than depending on itf-py 0.5.0. Treat this as Pipeline C' ("source plus mechanically bridged R"), not single source.
- **Lean** fits when proofs about the model are wanted (the Cedar pattern), at the cost of FFI or subprocess plumbing with no Python precedent.
- **Confidence.** Low-medium.
- **Load-bearing sources.** ICST 2024 Dafny bugs; Dafny Python integration doc; own trial 5; Cedar FFI README and vendor blog.
- **Would be overturned by:**
  - for (a), a measurement showing Dafny→Python miscompilations are negligible on the operation's feature subset (making the DRT leg pure cost), or that generated Python is too slow or unreadable to serve as R;
  - for (b), Quint MBT label defects (like the empty `actionTaken` observed here) proving systematic and not just an experimental-flag quirk.

**R-D3-4. Pipeline C, the prose-generation step.** Keep the earlier report's independent, differently structured property set as mandatory. The disconfirming evidence in Q4 shows that single formal sources checked only by proofs carry intent errors.
- **Confidence.** Medium.
- **Load-bearing sources.** IronSpec (OSDI); Fonseca et al. (EuroSys 2017); Sail-RISC-V vs Spike.
- **Would be overturned by.** A same-fault comparison showing that generated-layer round-trip diffs alone catch as many seeded record misreadings as an independent property set.

### Gaps
- No pipeline in the literature combines Python R + Quint/Dafny/Lean + an independent check set and reports measured results.
- Every recommendation here is assembled from tool docs, author-run evaluations and toy trials.

---

## Q4. Disconfirming search §4(c): do single-source pipelines miss more intent errors than separately authored layers?

### Takeaway
- **No study directly compares** single-source and separately authored pipelines on the same intent errors. The direct answer is a gap.
- Three full-text sources show the same pattern: a single formal or executable source, validated only through its own derived artefacts (proofs or generated code), carried intent errors that only a *separately authored* artefact exposed. That artefact was a spec test, a negative-test patch or an independent simulator.
- This supports the earlier report's Pipeline C failure mode. It does **not** show that Pipeline C *with* an independent check set misses more than Pipeline B.

### Cited Findings
Baseline being supported, quoted verbatim from verified edition §4, Pipeline C, Expected failure modes: "A misreading in the single source propagates consistently into every generated layer; SpecTec can detect it only via the test suite."

**Goldweber, Yu, Vakil Ghahani & Kapritsos, "IronSpec: Increasing the Reliability of Formal Specifications".** OSDI; the venue comes from the PDF's acknowledgement of "anonymous OSDI reviewers"; Crossref lookup failed. — [PDF](https://par.nsf.gov/servlets/purl/10550356) [A | yes (abstract, §5.1) | 14 Dafny specs, 6 of real open-source verified systems | "correct" = the spec matches developer intent; confirmed by writing buggy implementations that still verify | analogous (verified systems; includes the AWS Dafny Encryption SDK) | human-only | TA]
- They found "ten specification bugs across all six real-world verified systems".
- Of the 5 bugs found by the automatic sanity checker, "The corresponding implementation for all five spec bugs appeared correct, but the specs were buggy, being too weak". The proofs still passed for trivially wrong implementations, for example ESDK Encrypt/Decrypt "returning a ciphertext or plaintext consisting of a zero byte regardless of the input".
- The recurring cause was outputs with "many sub-fields and having postconditions concerning only a subset of these fields".

**Fonseca, Zhang, Wang & Krishnamurthy, EuroSys 2017.** — [PDF](https://www.cs.purdue.edu/homes/pfonseca/papers/eurosys2017-dsbugs.pdf) [A | yes (§5) | IronFleet, Verdi, Chapar; 16 bugs in total | "correct" = the guarantee applications expect | analogous | human-only | ind]
- Two of the 16 bugs were specification bugs.
- **Bug I1**: IronFleet's RSM spec "did not ensure linearizability because it did not specify … exactly-once semantics". A 7-line patch disabling deduplication "still verified". The developers said "their understanding of linearizability does not include exactly-once semantics" and "had been aware". This is a clear intent-interpretation gap carried by the single formal source.
- **Bug C4**: a Chapar client assertion "always evaluated to true".
- Their **Finding 6**: "Incomplete or incorrect specification can prevent correct verification … we need techniques to test specifications". Their remedy was negative testing (mutating the implementation and checking that verification fails).

**Schlägl, Ruep & Große, "Sail-RISC-V and Spike for RISC-V Vector: Toward Consistent Golden Reference Behavior", RISC-V Summit Europe 2026.** A 2-page summit paper; review status unknown. — [PDF](https://ics.jku.at/files/2026RISC-V_Summit_Europe_RVVTS_SailRV_Spike.pdf) [B | yes | ~77k negative-test and ~100k positive-test cases, RVV | "correct" = agreement with Spike, adjudicated against the RVV spec | analogous (ISA executable spec) | human-only | ind of Sail authors]
- Sail-RISC-V is a single formal source that generates the executable emulator. Against the independently written Spike it showed **0.23 %** deviations on valid sequences and **3.73 %** on invalid+valid sequences.
- Of the 2,868 invalid-set deviations, 62.87 % were "Invalid Accept (Missing trap)" and 36.19 % were "Valid Reject (Sail-RISC-V terminated)".
- The abstract attributes them to "remaining issues in Sail-RISC-V's RVV instruction validity checking". The per-deviation split between Sail bugs and Spike bugs was not fully read in the extracted text.

**Dafny ICST 2024 (above).** Multi-back-end differential testing exposed "ambiguous or under-documented language features" of the Dafny language spec itself. This is independent artefacts disagreeing and revealing a spec ambiguity (A, TA; analogous).

**Already covered by the earlier reports, not re-surveyed.** SpecTec (10 errors in 5 proposals; intent checked only via the human test suite), Arm ASL (12 bugs found by an independent property set), JEST, and Knight's correlated failures (verified edition §2.6 and §4).

### Inferences
- *Inference*: the evidence is consistent with "a single source validated only by its own derived layers misses intent errors". In IronSpec and Fonseca, proofs passed with too-weak or misinterpreted specs. In Sail, the generated emulator inherited the model's legality gaps.
- In every case, a separately authored artefact found the errors: STPs, negative-test patches or Spike. That is the independent check set Pipeline C already prescribes.
- So these sources disconfirm a *pure* single-source pipeline, not Pipeline C as specified. They do not show that separately authored *layers* (Pipeline B's dual slot-filling) catch more than an independent check set.
- *Inference*: the IronSpec failure class (postconditions over a subset of output fields) maps directly onto API behaviour specs with record-shaped results. A Pipeline A or C gate can probe it mechanically: CrossHair or Hypothesis with a mutant implementation that randomises unspecified fields must be *rejected* by the spec.
- Own trial 1 showed CrossHair surfacing the sibling defect, a missing precondition.

### Gaps
- No same-fault comparison of single-source vs separately authored layers exists in the sources found. Arm, SpecTec, Sail, IronSpec and Fonseca each report only one arm.
- WebAssembly reference interpreter vs WasmCert, and Arm ASL shared-bug studies beyond the earlier report, were not newly fetched.
- No "spec and implementation share a bug" study with a measured rate was found, beyond Knight (earlier report).
- Fonseca is the only fully independent (non-tool-author) source here.

---

## What this track did not do
- It did not read the Ravi & Coblenz full text (ACM 403). Claims come from the artifact README; the n is from a search extract.
- It did not read the fuzz-d MEng report, the elle-cli page or the full ISSTA 2022 and ICST 2025 papers. Abstracts and intros only for the latter two.
- It did not run Dafny→Python, Lean or P (no dotnet; GitHub release downloads unavailable; no elan). It did not measure generated-code performance or readability.
- It did not obtain GitHub stars or issue activity (GitHub API blocked), so issue responsiveness is unassessed.
- It did not benchmark detangle against Porcupine, and did not exercise `detangle.lin.check` on offline histories.
- Own trials are n = 1 toy operations with seeded bugs chosen by this track. They show feasibility and plumbing, not effectiveness. The CrossHair-backend miss in trial 3 is a single run.
- It did not research agent use of any of these tools. No agent measurements were found, and all evidence is human-only.

## Self-check
- **Pipeline C's definition.** I treat "single executable source" as meaning that R is generated from, or is, the source. If the brief's author meant "one *formal* source, with Python R allowed as a separate artefact", then the Quint and Lean options are fully Pipeline C, and my "C′" relabelling overstates the difference.
- **Ravi & Coblenz.** Unread in full. The "per test more effective" claim could depend on test-size normalisation I could not check.
- **ICST 2024 table.** pdftotext linearised it, so the five Python-implicated rows may be misaligned with their categories. The count of rows naming Python is reliable; their categories are not.
- **Colour semantics in CrossHair's `measured.json`.** I inferred them from the verdict strings, not from documentation.
- **IronSpec venue.** Taken from the PDF's acknowledgements, not from Crossref (the lookup failed).
- **Quint `--mbt` empty `actionTaken`.** This could be a misuse on my part (an `any` inside a parameterised action) rather than a tool defect. I report it as an observation.
- **Sail deviations.** I did not verify that all of them are Sail bugs. The paper attributes "some" deviations to Sail after checking the spec.
- **Brief scope.** The brief's history-checker list included "Porcupine bindings". None were found for Python, but the absence rests on searches, not on exhaustive registry enumeration.
