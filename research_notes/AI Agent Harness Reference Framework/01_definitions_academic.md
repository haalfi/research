# Academic and primary-source definitions of the agent "harness" and the responsibilities they assign to it

Scope: research literature from 2022 to the present, plus one primary industry source used for comparison. All arXiv items were read as full-text PDFs (downloaded from arxiv.org/pdf and extracted with pdftotext) unless marked otherwise.

Claim labels:
- **[Established]**: stated directly in the cited full text.
- **[Synthesized]**: combined across several cited full texts.
- **[Proposed]**: a framework or position that a source puts forward and does not demonstrate.
- **[Unreachable]**: the source could not be fetched or read in full.
- **[Inference]**: my own reasoning.

Venue flags (pre-print status):
- **Peer-reviewed:**
  - CoALA: TMLR, 02/2024 (stated in the PDF footer).
  - Generative Agents: UIST 2023, ACM reference in the PDF.
- **Peer-reviewed according to my background knowledge; the venue is not printed in the fetched PDF:**
  - ReAct: ICLR 2023.
  - Reflexion: NeurIPS 2023.
  - Toolformer: NeurIPS 2023.
  - SWE-agent: NeurIPS 2024.
  - Wang et al. survey: Frontiers of Computer Science.
- **Treated as arXiv-only / non-peer-reviewed:**
  - MRKL (AI21 whitepaper)
  - MemGPT
  - Voyager
  - Xi et al.
  - Mei et al. (context engineering survey)
  - Agentless
  - Kapoor et al. "AI Agents That Matter"
  - HAL
  - every 2026 paper below
- **Caveat:** Some of these may have been published in a venue later. I did not verify that.

---

## Q1. How is "harness" defined, where is the term used, and what synonyms exist?

### Takeaway
"Harness" as a term for agents is a 2025–2026 coinage. It spread from industry blog posts into arXiv papers. The canonical 2023–2024 academic papers do not use it; they say "agent architecture", "cognitive architecture", "agent framework", "agent-computer interface", or "system". The 2026 papers converge on one meaning: the runtime or infrastructure layer around a fixed model that assembles context, runs the loop, executes tools, persists state and verifies or governs execution. One survey explicitly treats "scaffold" and "harness" as synonyms.

There is a term collision: in evaluation papers, "harness" still means the *evaluation* harness. The agent wrapper there is called a "scaffold".

### Cited findings

**Definitions of "harness" (2026, all arXiv-only)**
- **[Established]** Guo et al. (2026) "use harness to denote the runtime infrastructure that surrounds the model and realizes closed-loop agent execution." The full definition continues:
  - "The harness is broader than an individual tool, memory module, prompt template, or workflow script. It is the coordinating layer that decides which observations reach the model, how context is assembled, how the agent loop advances, how actions are executed, how state and artifacts persist, and how failures are detected, governed, and recovered."
  - The authors state they follow their refs [7], [22], [64] for this usage. They also write that "the harness is therefore not an optional engineering wrapper; it is the runtime layer that turns model capability into sustained, inspectable interaction with an environment."
  - Source: [Guo et al., "From Question Answering to Task Completion: A Survey on Agent System and Harness Design", arXiv 2606.20683](https://arxiv.org/abs/2606.20683)
- **[Established]** Zhang et al. (2026) define the agent execution harness as "the infrastructure layer that governs context construction, tool interaction, orchestration, and verification around a language model."
  - They formalize "the harness as the controller of a closed-loop dynamical system and the LLM as the stochastic policy it governs."
  - Source: [Zhang et al., "Stop Comparing LLM Agents Without Disclosing the Harness" (position paper), arXiv 2605.23950](https://arxiv.org/abs/2605.23950)
- **[Established]** Pan et al. (2026) define the harness as "the external execution system around a model that organizes a task run." They add that harness logic "is usually buried in tightly coupled controller code."
  - They recast harness policy as an editable natural-language document (NLAH) that a shared runtime (IHR) interprets into "agent calls, handoffs, state updates, validation gates, and artifact contracts."
  - Their stated harness concerns include "contracts, evidence discipline, retry logic, state handoff, and validation strategy."
  - Source: [Pan et al., "Natural-Language Agent Harnesses", arXiv 2603.25723](https://arxiv.org/abs/2603.25723)
- **[Established]** Wang et al. (HIT, 2026): "Agent harnesses shape language-model performance by controlling tool use, feedback, verification, memory, and repair."
  - Source: [Wang et al., "Scaling Laws for Agent Harnesses via Effective Feedback Compute", arXiv 2605.29682](https://arxiv.org/abs/2605.29682)
  - Note: a search engine attributed this arXiv ID to a different survey (Meng et al.). The full text shows that attribution is wrong.

**"Scaffold" as a synonym**
- **[Established]** Ren et al. (2026) call the "operational scaffold" a structure "comprising instruction schemes …, memory systems …, tool interfaces …, and control logic."
  - They add: "such an operational scaffold is often also referred to as an agent harness (Rajasekaran, 2026; Trivedy, 2026; Zhang et al., 2026b; Zhong & Zhu, 2026), while this survey uses the term scaffold to emphasize the modifiable structures surrounding the foundation model. Operationally, this scaffold acts as a controller that constructs context, selects actions, and enforces constraints."
  - Source: [Ren et al. (incl. Schmidhuber), "Self-Improvements in Modern Agentic Systems: A Survey", arXiv 2607.13104](https://arxiv.org/abs/2607.13104)
- **[Established]** Starace (2026) uses "scaffold" for the agent wrapper and frames the issue as an "elicitation gap": "Published agent capability scores conflate what a model can do with what its scaffold lets it do."
  - Source: [Starace, "Scaffold Effects on GAIA: A Controlled Comparison", arXiv 2606.08529](https://arxiv.org/abs/2606.08529)

**The evaluation-harness collision**
- **[Established]** In HAL (2025), "harness" means the *evaluation* infrastructure: "a standardized evaluation harness that orchestrates parallel evaluations across hundreds of VMs."
  - HAL calls agent wrappers "scaffolds": "Scaffolds dramatically impact both accuracy and cost, yet comparisons across scaffolds are rare."
  - Its evaluation harness is "framework-agnostic, requiring light-weight modifications to integrate scaffolds."
  - Source: [Kapoor, Stroebl et al., "Holistic Agent Leaderboard", arXiv 2510.11977](https://arxiv.org/abs/2510.11977)

**Earlier synonyms (2022–2024)**
- **[Established]** *Cognitive architecture* (CoALA).
  - CoALA proposes "a conceptual framework to characterize and design general purpose language agents."
  - The term comes from cognitive architectures such as Soar, which "specified control flow for selecting, applying, and even generating new productions."
  - CoALA draws the analogy that LLMs are like production systems and "controls from cognitive architectures … might be equally applicable to transform LLMs into language agents."
  - Source: [Sumers, Yao, Narasimhan, Griffiths, CoALA, arXiv 2309.02427 (TMLR 2024)](https://arxiv.org/abs/2309.02427)
- **[Established]** *Agent-computer interface (ACI)*, defined as "an abstraction layer between the LM agent and computer, to enhance the LM agent's abilities in computer environments."
  - SWE-agent is "an agent composed of an LM and ACI."
  - Source: [Yang et al., SWE-agent, arXiv 2405.15793](https://arxiv.org/abs/2405.15793)
- **[Established]** *Augmented LLM* (industry). "The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory." The same post distinguishes:
  - "Workflows are systems where LLMs and tools are orchestrated through predefined code paths"
  - "Agents … are systems where LLMs dynamically direct their own processes and tool usage."
  - It also says to invest "just as much effort in creating good agent-computer interfaces (ACI)."
  - Source: [Anthropic, "Building effective agents", Dec 19 2024](https://www.anthropic.com/engineering/building-effective-agents)
- **[Established]** *Modular neuro-symbolic system (MRKL).* "A MRKL system consists of an extendable set of modules, which we term 'experts', and a router that routes every incoming natural language input to a module that can best respond." Modules are neural (including the LLM itself) or symbolic (calculator, API, database).
  - Source: [Karpas et al., MRKL Systems, arXiv 2205.00445 (AI21, arXiv-only)](https://arxiv.org/abs/2205.00445)
- **[Established]** *"Unified framework" / agent architecture design* (Wang et al.).
  - They frame "architecture design" as analogous to "defining the network structure" and "capability acquisition" as analogous to learning parameters.
  - They also call these "hardware fundamentals" and "software resources."
  - Source: [Wang et al., "A Survey on LLM-based Autonomous Agents", arXiv 2308.11432](https://arxiv.org/abs/2308.11432)
- **[Established]** *Agent framework of brain, perception and action* (Xi et al.). This is a "general framework for LLM-based agents … [that] can be tailored for different applications."
  - Source: [Xi et al., "The Rise and Potential of LLM-Based Agents", arXiv 2309.07864](https://arxiv.org/abs/2309.07864)
- **[Established]** *Context engineering* (Mei et al., 2025): "a formal discipline that transcends simple prompt design to encompass the systematic optimization of information payloads for LLMs."
  - The authors position it as "a unifying abstraction" linking RAG ("external memory"), tool use ("a method for context acquisition") and prompt engineering ("the language for orchestrating these components").
  - The survey covers 1,400+ papers.
  - Source: [Mei et al., "A Survey of Context Engineering for LLMs", arXiv 2507.13334](https://arxiv.org/abs/2507.13334)

**Industry origin of the term**
- **[Established, secondary]** Ren et al. cite "Rajasekaran, 2026" and "Trivedy, 2026" for the "harness" usage. Guo et al. say "Anthropic's public…" industrial systems are part of "the same transition," and they cite "Agentic Harness Engineering (AHE)" and "Meta-Harness."
  - This suggests the term enters academia through industry engineering posts. I did not open the primary industry posts behind those citations.
  - Sources: [Ren et al.](https://arxiv.org/abs/2607.13104); [Guo et al.](https://arxiv.org/abs/2606.20683)

### Inferences
- **[Inference]** "Agent architecture" and "cognitive architecture" (2023) describe the *design* of an agent: what modules exist.
  - "Harness" and "runtime" (2026) describe the *execution infrastructure* that runs a fixed model: what code surrounds it at run time.
  - "Scaffold" sits between the two. It is used for the swappable wrapper in evaluations.
  - The shift tracks a move from training-free agent design research to benchmark and production engineering, where the model is a fixed, swappable component.
- **[Inference]** A reference framework should state explicitly that "agent harness" is not "evaluation harness". HAL uses the word in the latter sense.

### Gaps
- **[Unreachable]** Several harness-specific surveys were found by search but not fetched within budget:
  - Meng et al., "Agent Harness for Large Language Model Agents: A Survey": Preprints.org / ResearchGate, DOI 10.20944/preprints202604.0428 per search; companion catalog at github.com/Gloriaameng/Awesome-Agent-Harness.
  - Li, Wu, Chang, "Harness Engineering for LLM Agents: A Survey of Harness Component Taxonomy…" (Preprints.org, June 2026).
  - "Code as Agent Harness", arXiv 2605.18747.
  - "HarnessBridge", arXiv 2606.12882.
  - The primary industry posts cited as Rajasekaran 2026 and Trivedy 2026.
- **[Unreachable]** Guo et al.'s refs [7], [22], [64], which they credit for the term, were not resolved.

---

## Q2. Where do sources draw boundaries between model, harness/scaffold, agent system and environment?

### Takeaway
Most sources use a three-way split: model (policy) ↔ wrapper (harness, ACI, architecture) ↔ environment.

They disagree on where *reasoning, planning and memory management* sit:
- CoALA and MemGPT place them in the agent but execute them *by the LLM* through internal actions or function calls.
- The 2026 harness papers treat them as harness-run policies around a fixed model.
- Toolformer moves tool-call decisions into the model's weights.

### Cited findings
- **[Established]** CoALA draws three levels of LLM use:
  - (A) plain text-in/text-out;
  - (B) "language agents" that "place the LLM in a direct feedback loop with the external environment by transforming observations into text and using the LLM to choose actions";
  - (C) "cognitive language agents" that "additionally use the LLM to manage the agent's internal state via processes such as learning and reasoning."

  In CoALA's Fig. 4:
  - The LLM is one box.
  - "Agent code" sits in procedural memory.
  - "The decision procedure executes the agent's source code. This source code consists of procedures to interact with the LLM (prompt templates and parsers), internal memories (retrieval and learning), and the external environment (grounding)."
  - The decision cycle "is analogous to a program's 'main' procedure."

  Source: [CoALA, arXiv 2309.02427](https://arxiv.org/abs/2309.02427)
- **[Established]** ReAct places reasoning inside the action space: "we augment the agent's action space to Â = A ∪ L, where L is the space of language." A thought "does not affect the external environment, thus leading to no observation feedback"; it updates the context c_{t+1} = (c_t, â_t).
  - Here the boundary is between environment-affecting actions and context-only actions. There is no separate harness concept.
  - Source: [Yao et al., ReAct, arXiv 2210.03629](https://arxiv.org/abs/2210.03629)
- **[Established]** SWE-agent puts the boundary between LM and computer. The ACI is the interface layer, and the agent is the LM plus the ACI. Its motivation is that Linux-shell UIs are "designed for human users" and LMs "would benefit from specially-built interfaces."
  - Source: [SWE-agent, arXiv 2405.15793](https://arxiv.org/abs/2405.15793)
- **[Established]** MemGPT uses an OS analogy:
  - "main context (analogous to main memory/physical memory/RAM)" vs. "external context (analogous to disk)."
  - The LLM is the "processor." "The LLM completion tokens (outputs) are interpreted as function calls by the function executor."
  - "MemGPT provides function calls that the LLM processor [uses] to manage its own memory."
  - So the boundary is: the model decides, and the system (queue manager, function executor) executes and enforces.
  - Source: [Packer et al., "MemGPT: Towards LLMs as Operating Systems", arXiv 2310.08560](https://arxiv.org/abs/2310.08560)
- **[Established]** Toolformer moves tool-use decisions into the model: it is "a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction."
  - Source: [Schick et al., Toolformer, arXiv 2302.04761](https://arxiv.org/abs/2302.04761)
- **[Established]** Voyager treats the model as a black box: "VOYAGER interacts with GPT-4 via blackbox queries, which bypasses the need for model parameter fine-tuning." All learning lives outside the weights, in a skill library of code.
  - Source: [Wang et al., Voyager, arXiv 2305.16291](https://arxiv.org/abs/2305.16291)
- **[Established]** Reflexion likewise reinforces agents "not by updating weights, but instead through linguistic feedback" stored in "an episodic memory buffer."
  - Source: [Shinn et al., Reflexion, arXiv 2303.11366](https://arxiv.org/abs/2303.11366)
- **[Established]** Guo et al. separate "runtime responsibilities from the model itself." The harness H is distinct from the model and the environment, and the environment is reached through observation and action interfaces.
  - They state that "this perspective is now extending beyond single-model scaffolds": recent systems "treat the harness as a compositional runtime over multiple models, and increasingly as a learnable object."
  - Source: [Guo et al., arXiv 2606.20683](https://arxiv.org/abs/2606.20683)
- **[Established]** Zhang et al. write performance as B(M, H). The model M is the policy π_θ and the harness configuration C_H is the controller.
  - They classify "hallucination spirals, context overflow, and execution runaway" as "controller failures rather than policy failures."
  - Source: [Zhang et al., arXiv 2605.23950](https://arxiv.org/abs/2605.23950)
- **[Established]** Anthropic separates agentic *systems* by who controls the path. In workflows, code paths are predefined; in agents, the LLM directs the process.
  - Source: [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- **[Established]** Agentless explicitly removes model control of the loop: a fixed "three-phase process of localization, repair, and patch validation, without letting the LLM decide future actions or operate with complex tools."
  - Source: [Xia et al., Agentless, arXiv 2407.01489](https://arxiv.org/abs/2407.01489)

### Inferences
- **[Inference]** The model/harness boundary is not fixed. It moves with training:
  - Toolformer puts tool selection into the model weights.
  - Agent-native training and co-evolution, a stage Guo et al. name, pulls loop behaviors into the model.
  - Harness papers pull them back out as editable policy (NLAH).

  A framework should define the harness *functionally* (what it does around whatever the model does not internalize) rather than by a fixed list of features.
- **[Inference]** The "who decides" axis (Anthropic's workflow vs. agent split, and Agentless) is orthogonal to the "what components" axis. Even a workflow has a harness: it just has a hard-coded loop.

### Gaps
- No source I read gives a crisp, formal boundary between "harness" and "agent system". Guo et al. come closest: they treat MCP, A2A, sandboxes and SDKs as "instantiat[ing] specific harness responsibilities" rather than as concepts parallel to the harness.

---

## Q3. Which functional components do the key frameworks use to decompose agents?

### Takeaway
The decompositions cluster into two eras.

| Era | Decomposition style | Emphasis |
|---|---|---|
| 2023 design-centric | Profile, memory, planning, action; or brain, perception, action; or CoALA's memory, action space, decision loop | What the agent knows and plans |
| 2026 runtime-centric | Observation, context, loop, action, state, verification; or execution, tool, context, scheduling, observability, verification | How a run is executed and governed |

Memory, action/tools and a decision loop are near-universal. Planning and reflection appear as modules in the early work and as loop policies in the later work. Verification/governance and observability appear only in the later work.

### Cited findings (one line per framework)

**CoALA [Established; Proposed framework]**
- Three dimensions: "information storage (divided into working and long-term memories); their action space (divided into internal and external actions); and their decision-making procedure (which is structured as an interactive loop with planning and execution)."
- Long-term memory is procedural, semantic or episodic.
- Internal actions are retrieval, reasoning and learning. External actions are grounding (physical, dialogue, digital).
- In each cycle the agent "uses retrieval and reasoning to plan by proposing and evaluating candidate learning or grounding actions. The best action is then selected and executed."
- Source: [CoALA](https://arxiv.org/abs/2309.02427)

**ReAct [Established]**
- Interleaved thought, action and observation over a growing context. Components are implicit: an action space extended with language, plus the context/trajectory.
- Source: [ReAct](https://arxiv.org/abs/2210.03629)

**Reflexion [Established]**
- "three distinct models: an Actor … an Evaluator model … and a Self-Reflection model," plus short- and long-term (episodic) memory.
- Evaluation signals come from "simple binary environment feedback, pre-defined heuristics … and self-evaluation."
- Source: [Reflexion](https://arxiv.org/abs/2303.11366)

**MRKL [Established]**
- A router plus an extendable set of neural or symbolic expert modules.
- Source: [MRKL](https://arxiv.org/abs/2205.00445)

**Toolformer [Established]**
- No external decomposition: tool-call decisions are learned in-model.
- Source: [Toolformer](https://arxiv.org/abs/2302.04761)

**SWE-agent ACI [Established]**
- "The ACI comprises several principal components, including search/navigation, file viewer, file editor, and context management."
- It runs a ReAct-style thought-and-command loop.
- "The ACI uses guardrails to prevent common mistakes, and an agent receives specific, concise feedback about a command's effects at every turn" (e.g. a linter on edits).
- Source: [SWE-agent](https://arxiv.org/abs/2405.15793)

**Voyager [Established]**
- "three key components: 1) an automatic curriculum that maximizes exploration, 2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and 3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification."
- Source: [Voyager](https://arxiv.org/abs/2305.16291)

**MemGPT [Established]**
- Main context, made of system instructions (read-only), working context and a FIFO queue.
- External context: archival storage and recall storage.
- A queue manager, which handles eviction, recursive summaries and context-overflow control.
- A function executor.
- Control flow through events and "request heartbeat=true" for function chaining.
- Source: [MemGPT](https://arxiv.org/abs/2310.08560)

**Generative Agents [Established]**
- "Our architecture comprises three main components." The first is "the memory stream, a long-term memory module." Retrieval combines "relevance, recency, and importance."
- The others are reflection and planning.
- Ablations show "observation, planning, and reflection—each contribute critically to the believability of agent behavior."
- Source: [Park et al., Generative Agents, arXiv 2304.03442 (UIST 2023)](https://arxiv.org/abs/2304.03442)

**Wang et al. survey [Established]**
- "a profiling module, a memory module, a planning module, and an action module."
- Profile "identif[ies] the role of the agent."
- A separate axis covers capability acquisition, with or without fine-tuning.
- Source: [Wang et al.](https://arxiv.org/abs/2308.11432)

**Xi et al. survey [Established]**
- "brain, perception, and action."
- The brain "stores crucial memories, information, and knowledge but also undertakes essential tasks of information processing, decision-making, reasoning, and planning." That is, memory and planning sit *inside* the LLM-centered brain.
- Perception expands the agent "from text-only to a multimodal space."
- Source: [Xi et al.](https://arxiv.org/abs/2309.07864)

**Context engineering survey [Established]**
- Foundational components: "(1) Context Retrieval and Generation …; (2) Context Processing …; (3) Context Management, covering memory hierarchies, compression…"
- System implementations: "Retrieval-Augmented Generation, Memory Systems, Tool-Integrated Reasoning, and Multi-Agent Systems."
- Source: [Mei et al.](https://arxiv.org/abs/2507.13334)

**Guo et al. harness survey (2026) [Established; Proposed formalism]**
- H = ⟨I_obs, C, L, I_act, S, V⟩:

| Symbol | Component | What the source says it covers |
|---|---|---|
| I_obs | Observation interface | "transforms raw environment signals into model-usable observations" (terminal output, diffs, screenshots, DOM, logs, retrieved passages) |
| C | Context manager | "what information enters the model context, when it enters, and in what form," covering prompt construction, retrieval, memory selection, compression, summarization, tool descriptions and task state |
| L | Control loop | "orchestrates the observe-reason-act-feedback cycle, including step scheduling, stopping criteria, retries, reflection, delegation, handoffs, and multi-agent coordination" |
| I_act | Action interface | function calls, MCP tools, shell/code, browser, files, APIs, "sub-agent invocations" |
| S | State and artifact store | "conversation history, plans, scratchpads, checkpoints, logs, traces, diffs, memory records, generated files" |
| V | Verification and governance layer | "tests, assertions, verifier models, sandbox policies, permission gates, rollback, retry, budget control, safety constraints, and audit traces" |

- The mapping from conceptual operations to components "is many-to-many rather than one-to-one."
- Source: [Guo et al.](https://arxiv.org/abs/2606.20683)

**Zhang et al. (2026) [Established]**
- Harness "layers" used to code their evidence table: "E = Execution, T = Tool, C = Context, S = Scheduling, O = Observability, V = Verification."
- Source: [Zhang et al.](https://arxiv.org/abs/2605.23950)

**Ren et al. (2026) [Established]**
- Scaffold = instruction schemes, memory systems, tool interfaces, control logic. Its job is to "construct context, select actions, and enforce constraints."
- Source: [Ren et al.](https://arxiv.org/abs/2607.13104)

**Wang et al. HIT (2026) [Established]**
- Tool use, feedback, verification, memory, repair.
- Source: [arXiv 2605.29682](https://arxiv.org/abs/2605.29682)

**Pan et al. NLAH (2026) [Established]**
- Agent calls, handoffs, state updates, validation gates, artifact contracts. Also task contract, retry logic, state handoff.
- Source: [arXiv 2603.25723](https://arxiv.org/abs/2603.25723)

### Inferences: mapping onto the candidate taxonomy (Loop, Tools, Context, Memory, Control)

- **[Synthesized] Loop.** Present everywhere:
  - CoALA decision cycle; ReAct; MemGPT events/heartbeat; Voyager iterative prompting; Guo L; Zhang S (scheduling); Ren control logic.
  - **Confirmed.** In 2026 sources the loop absorbs reflection, retries, delegation and multi-agent coordination (Guo L).
- **[Synthesized] Tools.** Present everywhere:
  - CoALA grounding; MRKL experts; SWE-agent ACI; Guo I_act; Zhang T; Ren tool interfaces; Xi action.
  - **Confirmed.** Two candidates to split off: an *observation/perception interface* (Guo I_obs, Xi perception, SWE-agent "concise feedback") and an *execution environment/sandbox* (Zhang E).
- **[Synthesized] Context vs. Memory.** These are frequently *merged*:
  - MemGPT's "virtual context management"
  - CoALA working memory, which is effectively the context
  - Mei et al., where context management "cover[s] memory hierarchies"
  - Guo C, which includes "memory selection"

  They are *split* in Guo (C vs. S) and in Wang/Ren (memory module vs. instructions).
  - **[Inference]** A defensible split is: Context = per-call assembly; Memory/State = persistence across calls, steps or sessions. Guo's S is broader than "memory": it includes checkpoints, logs, traces and artifacts. That suggests *Memory → State* (durable state) as a better label.
- **[Synthesized] Control.** In 2026 sources this splits into two distinct things:
  - (a) verification/evaluation: Reflexion Evaluator, Voyager self-verification, Agentless patch validation, Guo V, Zhang V, Wang-HIT verification/repair, Pan validation gates;
  - (b) governance/safety: sandbox policies, permission gates, budget, audit (Guo V, Zhang E).

  2023 decompositions have no control/governance component at all.
  - **[Inference]** "Control" should either be split into Verification and Governance, or defined explicitly to cover both. Verification is the most frequently recurring responsibility missing from the five candidates.
- **[Synthesized] Planning.** A first-class module in Wang, Generative Agents, CoALA (inside the decision procedure), Voyager (curriculum) and Xi (inside the brain). It is absent as a harness component in 2026 sources, which leave it to the model or the loop.
  - **[Inference]** Planning is a model capability that the harness may scaffold (planner-executor scaffolds in Starace), not a harness responsibility in its own right.
- **[Synthesized] Profile / instructions** (Wang profiling; Ren instruction schemes; Guo C "system instructions"). This is a recurring element absent from the candidate five. It fits under Context.
- **[Synthesized] Observability** appears only in 2025–2026 sources: Zhang O; Guo S "logs, traces"; HAL's evaluation harness "capturing complete execution traces." So does **durable execution**: Guo S "checkpoints", V "rollback".
- **[Synthesized] Multi-agent handoff** appears in Guo L and I_act ("delegation, handoffs", "sub-agent invocations"), Pan ("handoffs, state handoff") and Mei (Multi-Agent Systems as an implementation). Sources fold it into Loop and Tools rather than giving it its own component.
- **[Synthesized] Evaluation as an external activity** (HAL, Kapoor) is distinct from in-loop verification. It is a property of the evaluation harness, not the agent harness.

### Gaps
- I could not reach the harness-specific surveys by Meng et al. and Li/Wu/Chang. Each reportedly has its own component taxonomy (see Q1 gaps), so their decompositions are not compared here.
- I did not verify where Guo et al.'s six-tuple originated beyond their own citations.

---

## Q4. Is there empirical evidence that the scaffold or harness, and not just the model, changes outcomes?

### Takeaway
Yes, and the effects are large. Controlled same-model comparisons show:
- 7 points on SWE-bench Lite (SWE-agent ACI vs. shell, GPT-4 Turbo);
- up to 28 points on GAIA (Starace);
- secondary reports of 34–48 points on SWE-bench Verified Mini across scaffolds (HAL as cited by Zhang).

Simpler pipelines and baselines sometimes beat complex agents, so "more harness" is not monotonically better.

### Cited findings
- **[Established]** SWE-agent, GPT-4 Turbo, SWE-bench Lite:

  | Setting | % Resolved | Cost per instance |
  |---|---|---|
  | RAG | 2.67% | — |
  | Shell-only agent | 11.00% | $1.46 |
  | SWE-agent ACI | 18.00% | $1.67 |

  - The authors describe the ACI result as "SWE-agent's 64% relative increase compared to Shell-only, both with GPT-4 Turbo." The abstract calls it "10.7 percentage points more instances than the baseline agent." Note that this does not match the table difference of 7.0 points: the abstract appears to refer to a different baseline or version.
  - Full test set: 12.47% vs. RAG 1.31%.
  - Ablations on Lite, against the 18.0% default:

    | Ablation | Result | Change |
    |---|---|---|
    | No edit command | 10.3% | −7.7 |
    | Iterative search | 12.0% | −6.0 |
    | Full-file viewer | 12.7% | −5.3 |
    | 30-line viewer | 14.3% | −3.7 |
    | Full history instead of last-5 observations | 15.0% | −3.0 |
    | No demonstration | 16.3% | −1.7 |

  - Source: [SWE-agent](https://arxiv.org/abs/2405.15793)
- **[Established]** Starace runs a pre-registered study: 3 scaffolds (ReAct, Planner-Actor-Rater, planner-then-executor) × 5 models (Claude Opus 4.7, Sonnet 4.6, Haiku 4.5; Gemini 3.1 Pro Preview; GPT-5.5) on GAIA L1/L2, with 3 attempts.
  - "Scaffold choice alone moves measured accuracy by as much as 28 percentage points within a single model (Opus, Level 2)."
  - "The pre-registered prediction that more capable models would be less scaffold-sensitive is rejected in direction."
  - The multi-agent advantage holds within the Anthropic family but not across providers.
  - Conclusion: "single-scaffold capability numbers are scaffold-conditional estimates and … the elicitation gap is not guaranteed to shrink as models improve."
  - Single independent author, arXiv-only.
  - Source: [arXiv 2606.08529](https://arxiv.org/abs/2606.08529)
- **[Established, secondary compilation]** Zhang et al. Table 1, with the model fixed and only infrastructure changed:

  | Benchmark | Model | Harness change | Δ |
  |---|---|---|---|
  | SWE-bench Pro | Claude Opus 4.5 | SEAL → Claude Code | +9.5 pp (45.9% → 55.4%) |
  | SWE-bench Verified | Grok 4 | SWE-agent → xAI scaffold | +14–16 pp (58.6% → 72–75%) |
  | TerminalBench 2.0 | fixed | prompt + middleware + verification | +13.7 pp (52.8% → 66.5%) |
  | Terminal-Bench 2 | GPT-5.4 high | AHE harness evolution | +7.3 pp (69.7% → 77.0%) |
  | SWE-bench Pro | various | + WarpGrep search subagent | +2.1–2.2 pp, enough to flip the MiniMax 2.5 vs. Claude Opus 4.6 ordering |
  | Agent tasks (Vercel) | fixed | 15 tools → 2 tools | 80% → 100% |

  - Zhang et al. also cite "up to 11 to 15 percentage points of scaffold-only variation on SWE-bench Verified" from independent third-party monitoring.
  - Many of these figures come from vendor or blog sources (Morph, Vals AI, Vercel, Trivedy) that Zhang et al. cite. I did not check them against the primaries.
  - Source: [Zhang et al.](https://arxiv.org/abs/2605.23950)
- **[Established secondary; not verified in primary]** Zhang et al. report HAL "double-digit cross-scaffold gaps under SWE-Agent versus HAL Generalist":
  - 34 points for Claude Sonnet 4.5 (68% → 34%);
  - 34 points for GPT-5 Medium (46% → 12%);
  - "nearly 48 points for o4-mini."

  The HAL v1 arXiv text I read shows these scaffolds only in Pareto plots, with no extractable numbers. Its model list (Opus 4.1, Sonnet 4, 3.7 Sonnet, GPT-5 Medium, o4-mini, …) does not include Sonnet 4.5, so Zhang's figures likely come from the live leaderboard. Flag them as not verified against the HAL paper.
  - Sources: [Zhang et al.](https://arxiv.org/abs/2605.23950); [HAL](https://arxiv.org/abs/2510.11977)
- **[Established]** HAL ran 21,730 rollouts across 9 models and 9 benchmarks for about $40,000. It found that "scaffolds dramatically impact both accuracy and cost," and that "higher reasoning effort reduc[es] accuracy in the majority of runs."
  - Source: [HAL](https://arxiv.org/abs/2510.11977)
- **[Established]** Agentless: a simple three-phase pipeline reached 32.00% (96 fixes) on SWE-bench Lite at $0.70, "the highest performance … compared with all existing open-source software agents" at the time.
  - Source: [Agentless](https://arxiv.org/abs/2407.01489)
- **[Established]** Kapoor et al.: simple baselines (retry, warming) "outperform many SoTA complex agent architectures on HumanEval … while costing much less." Hence "agent evaluations must be cost-controlled."
  - Source: [Kapoor et al., "AI Agents That Matter", arXiv 2407.01502](https://arxiv.org/abs/2407.01502)
- **[Established]** Generative Agents' ablations show that the observation, planning and reflection components each "contribute critically" to believability.
  - Source: [Generative Agents](https://arxiv.org/abs/2304.03442)
- **[Lead only; search snippet, full text not read]** ReCreate (arXiv 2601.11100) is reported to compare five open-source agents with the same base model (gpt-4o) on SWE-bench Lite. It reportedly finds that much apparent "model limitation" is recoverable under another scaffold.
  - Source: [ReCreate, arXiv 2601.11100](https://arxiv.org/abs/2601.11100)

### Inferences
- **[Inference]** The evidence supports three claims:
  - Harness effects are often comparable to, or larger than, model-generation gaps.
  - The size of the effect is task- and model-dependent: the interaction term is non-zero, and Starace rejects a "capable models need less scaffold" prediction.
  - Added complexity can hurt (Agentless, Kapoor baselines, HAL's reasoning-effort result).

  The strongest controlled primary evidence is SWE-agent's ablations and Starace's pre-registered study. The largest numbers (34–48 points) are secondary.

### Gaps
- I did not verify the HAL per-scaffold numbers or the vendor and blog figures in Zhang Table 1 against primary sources.
- I could not access the full text of ReCreate within budget.

---

## Q5. Which responsibilities recur, and which fall outside Loop, Tools, Context, Memory and Control?

### Takeaway
All five candidates recur. Memory and Context are frequently merged, and Control is ambiguous. The strongest out-of-taxonomy candidates are:
1. **Verification/evaluation** (in-loop checking and repair);
2. **Governance/sandboxing** (permissions, isolation, budget, audit);
3. **Observability/tracing**;
4. **Durable state** (checkpoints, rollback, artifacts);
5. **Observation/perception interface**.

Planning and reflection are treated as loop policies in recent work. Multi-agent handoff is folded into Loop and Tools.

### Cited findings (each responsibility, with the sources that name it)
- **Verification/repair** [Synthesized]:
  - Reflexion Evaluator ([link](https://arxiv.org/abs/2303.11366))
  - Voyager self-verification ([link](https://arxiv.org/abs/2305.16291))
  - Agentless patch validation ([link](https://arxiv.org/abs/2407.01489))
  - SWE-agent linter guardrails ([link](https://arxiv.org/abs/2405.15793))
  - Guo V ([link](https://arxiv.org/abs/2606.20683))
  - Zhang V ([link](https://arxiv.org/abs/2605.23950))
  - Wang-HIT "verification … repair" ([link](https://arxiv.org/abs/2605.29682))
  - Pan "validation gates" ([link](https://arxiv.org/abs/2603.25723))
- **Sandboxing/governance**:
  - [Established] Guo V: "sandbox policies, permission gates, rollback, … budget control, safety constraints, and audit traces." Approval policies "determine when human authorization is required before an action is dispatched."
  - [Established] Zhang E (Execution).
  - [Established] Ren: the scaffold "enforces constraints."
  - Sources: [Guo](https://arxiv.org/abs/2606.20683), [Zhang](https://arxiv.org/abs/2605.23950), [Ren](https://arxiv.org/abs/2607.13104)
- **Observability** [Established]:
  - Zhang O.
  - Guo S "logs, traces," and AHE "evolves harness components from observability-driven feedback."
  - Sources: [Zhang](https://arxiv.org/abs/2605.23950), [Guo](https://arxiv.org/abs/2606.20683)
- **Durable execution/state** [Established]: Guo S "checkpoints … diffs … generated files, and task artifacts," and V "rollback."
  - Source: [Guo](https://arxiv.org/abs/2606.20683)
  - No 2023 source names durable execution. [Inference]
- **Multi-agent handoff** [Established]:
  - Guo L "delegation, handoffs, and multi-agent coordination"; A2A maps to L and I_act.
  - Pan "handoffs".
  - Mei "Multi-Agent Systems".
  - Sources: [Guo](https://arxiv.org/abs/2606.20683), [Pan](https://arxiv.org/abs/2603.25723), [Mei](https://arxiv.org/abs/2507.13334)
- **Planning** [Established] as a module:
  - Wang ([link](https://arxiv.org/abs/2308.11432))
  - CoALA ([link](https://arxiv.org/abs/2309.02427))
  - Generative Agents ([link](https://arxiv.org/abs/2304.03442))
  - Voyager curriculum ([link](https://arxiv.org/abs/2305.16291))
- **Reflection** [Established]:
  - Reflexion and Generative Agents have it as a module.
  - Guo places reflection inside L.
- **Profile/instructions** [Established]: Wang profiling; Ren instruction schemes.
- **Evaluation (external)** [Established]: HAL, Kapoor. This is the evaluation harness, a distinct object.

### Inferences
- **[Inference]** A revised taxonomy that is consistent with the sources, offered as a proposal and not taken from any single source:

  | Revised category | What it merges or covers |
  |---|---|
  | Loop / orchestration | includes reflection, retries, delegation, multi-agent handoff, stopping |
  | Action interface (Tools) | including sandboxed execution |
  | Observation + Context assembly | merging perception with context, or splitting I_obs out |
  | State & Memory | durable: long-term memory, checkpoints, artifacts, traces |
  | Verification | in-loop checks, tests, verifiers, repair |
  | Governance | permissions, approvals, budgets, sandbox policy, audit |

  - Observability could stand alone, as Zhang does, or be a cross-cutting concern over State.
  - This is closest to Guo et al.'s six-tuple. Zhang's six layers (E, T, C, S, O, V) differ mainly by lacking memory and by having explicit observability.

### Gaps
- Without the Meng and Li/Wu/Chang harness surveys, I cannot say whether a consensus taxonomy already exists in the 2026 literature.

---

## Q6. Where do the sources disagree?

### Takeaway
There are five disagreements:
1. Terminology: harness, scaffold and evaluation harness.
2. Whether memory and planning belong to the model (the "brain") or the wrapper.
3. Whether tool-use decisions live in weights or in the harness.
4. Whether the harness or the model is the dominant performance factor.
5. Whether richer harnesses help or hurt.

### Cited findings
- **Terminology** [Established]:
  - Ren deliberately prefers "scaffold" over "harness" ([link](https://arxiv.org/abs/2607.13104)).
  - Guo prefers "harness" ([link](https://arxiv.org/abs/2606.20683)).
  - HAL uses "harness" for the evaluation infrastructure and "scaffold" for the agent ([link](https://arxiv.org/abs/2510.11977)).
- **Locus of memory and planning** [Established]:
  - Xi puts memory, reasoning and planning inside the LLM "brain" ([link](https://arxiv.org/abs/2309.07864)).
  - Wang has separate memory and planning modules ([link](https://arxiv.org/abs/2308.11432)).
  - CoALA has memory as modules, with planning executed by LLM-driven internal actions within agent code ([link](https://arxiv.org/abs/2309.02427)).
  - MemGPT lets the LLM manage its own memory through functions, with the system enforcing overflow ([link](https://arxiv.org/abs/2310.08560)).
- **Tools in weights vs. wrapper** [Established]:
  - Toolformer internalizes call decisions ([link](https://arxiv.org/abs/2302.04761)).
  - MRKL externalizes them to a router ([link](https://arxiv.org/abs/2205.00445)).
  - SWE-agent and Anthropic argue that interface design is a first-class engineering task ([SWE-agent](https://arxiv.org/abs/2405.15793), [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)).
- **Dominance** [Proposed vs. Established]:
  - Zhang's "Binding Constraint Thesis" holds that harness variance "is often comparable to or larger than" model variance for long-horizon tasks with comparable frontier models. This is a position paper with an explicitly scoped claim ([link](https://arxiv.org/abs/2605.23950)).
  - Starace finds scaffold effects vary by model family and do not shrink with capability ([link](https://arxiv.org/abs/2606.08529)).
  - Guo frames it as an interaction: outcomes emerge "from the interaction between model capability, runtime infrastructure, task structure, and evaluation design" ([link](https://arxiv.org/abs/2606.20683)).
- **More vs. less harness** [Established]:
  - Agentless ([link](https://arxiv.org/abs/2407.01489)) and Kapoor ([link](https://arxiv.org/abs/2407.01502)) show simple pipelines or baselines matching or beating complex agents.
  - Zhang's Vercel case (15 → 2 tools: 80% → 100%) shows *removing* tools can help ([link](https://arxiv.org/abs/2605.23950)).
  - SWE-agent shows richer interfaces help, but also that too much information hurts: the full-file viewer and full history both reduced performance ([link](https://arxiv.org/abs/2405.15793)).

### Inferences
- **[Inference]** The "more vs. less" disagreement resolves if the harness is judged by *fit* (information shaping, the right action granularity) rather than by amount of machinery. SWE-agent's own ablations show both directions within one system.
- **[Inference]** The dominance claims are mostly from 2026 arXiv-only papers, several of which rely on vendor or blog numbers. A reference framework should present "the harness materially changes outcomes" as Established, and "the harness dominates the model" as Proposed.

### Gaps
- I found no peer-reviewed 2025–2026 paper (as opposed to arXiv-only) that formally defines "agent harness". The term's academic formalization is currently pre-print only.
