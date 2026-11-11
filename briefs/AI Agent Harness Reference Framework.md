# AI Agent Harness Reference Framework

## Goal
Build a source-traceable reference framework for AI agent harnesses from existing
research, published architectures, working implementations and standards.
Do not invent a taxonomy; derive one and mark every new element as such.

Target: one harness framework that scales — not a single-team setup. It must grow
with the number of teams, disciplines and topics without being redesigned: new teams
onboard, new use cases and tools plug in, governance keeps up. It is operated by
experienced DevOps/platform teams. Governance, policy, identity, audit, cost and
operations are first-class requirements, not afterthoughts.

## Working definitions (hypotheses, to be tested)
- Harness: the execution and orchestration infrastructure around a model that lets it
  act iteratively, use tools, manage context and memory, and operate under constraints.
- Model / harness / agent system are distinct layers.
- Candidate responsibilities: Loop, Tools, Context, Memory, Control.
  Functional responsibilities, not modules. Confirm, merge, split or reject each.

## Research questions
RQ1 How do primary sources define "harness" and its synonyms (agent scaffold, runtime,
    agent architecture, cognitive architecture, orchestration layer)? Where do they
    draw the model / harness / agent-system / environment boundaries?
RQ2 Which harness responsibilities recur across sources and implementations?
    Do the five candidates cover them? What is missing (e.g. durable execution,
    observability, evaluation, sandboxing, multi-agent handoff, governance)?
RQ3 For each responsibility: which mechanisms and patterns are documented and
    implemented, and with what evidence?
RQ4 Which standards and protocols (e.g. MCP, A2A, OpenTelemetry GenAI conventions)
    fix interfaces at which boundary?
RQ5 Where do sources disagree or leave gaps?
RQ6 Does the derived framework map cleanly onto the validation set (below)?
RQ7 Enterprise governance and operations: how do the validation systems handle
    policy hierarchy (enterprise / org / team / repo / user), managed settings,
    model and MCP-server allowlists, tool and permission policies, identity/SSO,
    audit logs, content exclusion, data residency and retention, cost controls and
    quotas, telemetry/observability, and deployment options (SaaS, cloud-hosted,
    self-hosted, air-gapped)? How well does each control hold up as teams and use
    cases are added? Which belong in the framework as harness responsibilities
    versus a surrounding platform layer?
RQ8 Which harness concepts are coding-specific and which transfer to other
    disciplines (analysis, documentation, operations, business processes)?
RQ9 Growth and extensibility: which architectural properties let a harness framework
    grow from one team to many teams, disciplines and topics without redesign?
    Examine, with evidence:
    - extension points: how new tools, MCP servers, skills/instructions, agent
      definitions and workflows are added without touching the core;
    - layering: what stays central (core loop, policy, identity, audit) versus what
      each team or topic owns, and how inheritance and overrides work;
    - shared, versioned assets: registries, reuse across teams, rollout,
      deprecation and supply-chain trust;
    - onboarding: self-service for new teams and topics within guardrails
      (golden paths, templates, tiered risk profiles);
    - scaling of governance and operations: policy, observability, evaluation and
      cost attribution that stay manageable as teams and topics multiply;
    - known failure modes when single-team harness setups were scaled up.
    Reference established platform-engineering practice where the agent literature
    is thin, and label such transfers as Synthesized.

## Source tiers (keep evidentiary strength separate)
1 Scientific research (peer-reviewed and arXiv; flag non-peer-reviewed)
2 Reference architectures (vendor engineering posts and docs = design claims, not evidence)
3 Working implementations (SDK and product docs, admin/policy docs, source code)
4 Standards and protocols (specifications)

Seed leads (verify title, date, URL; label unreachable ones):
- Anthropic, "Building Effective Agents" (2024)
- Anthropic, "Effective Harnesses for Long-Running Agents" (2025)
- Anthropic, "Scaling Managed Agents: Decoupling the Brain from the Hands" (2026)
- OpenAI Agents SDK, "Running Agents"; guardrails and human-in-the-loop docs
- MCP specification; Temporal durable agent execution
- GitHub Copilot enterprise/organization policy and coding-agent docs
- Academic anchors to check: CoALA, ReAct, agent surveys 2023–2026

## Validation set (light pass: docs, admin docs, key source files where open)
SDKs / runtimes: OpenAI Agents SDK, Claude Agent SDK, LangGraph.
Coding-agent harnesses: Claude Code, OpenAI Codex (CLI/cloud), OpenCode,
GitHub Copilot (agent mode and coding agent).
Hypothesis to test, not assume: Copilot is less capable as an agent harness than
Claude Code, Codex or OpenCode, but stronger in enterprise policy and governance.
Capability claims need sources; vendor benchmarks count as vendor claims.

## Scope
In: single- and multi-agent LLM harnesses, enterprise governance of agent harnesses,
2022–present, English sources.
Out: model training/fine-tuning, pure prompt engineering, agent-based simulation,
procurement and pricing comparisons beyond cost-control mechanisms.

## Claim labels
Established / Synthesized / Proposed, plus Unreachable and Inference.
Verdicts rest on full texts; search snippets are leads only.
Product features carry the doc date or version checked.

## Deliverable
Report with: definition and boundaries; derived responsibility taxonomy (with
changes vs. the five candidates); per-responsibility mechanisms; standards map;
enterprise governance matrix (RQ7 controls × validation systems);
growth and extensibility model (RQ9): core vs. extension layers, ownership and
onboarding path; cross-discipline applicability (RQ8); disagreements and gaps;
validation matrix (framework × systems); recommendations for a reference harness
that scales with teams and topics, marked Proposed.
Traceability table per framework element:
element | definition | origin source(s) | implementation examples | consensus level | open disagreements.
