# Standards and protocols that fix interfaces in AI agent harness architectures

Date checked: 2026-11-11 for every source below unless stated. Fetch method: curl of primary pages and raw.githubusercontent.com files (full text read locally). Labels: **[Established]** = stated in a primary full text I read; **[Synthesized]** = my combination of several Established facts; **[Proposed]** = draft / in-development / roadmap items; **[Inference]** = my reasoning, not stated by a source; **[Unreachable]** = source could not be fetched.

## Standards map (summary table)

| Spec | Boundary standardized | Governance | Version / date / maturity (checked 2026-11-11) | Adoption evidence | Security provisions |
|---|---|---|---|---|---|
| Model Context Protocol (MCP) | harness to tools/data (host-client to server); also harness to instructions/assets via Prompts, Resources, Skills-over-MCP extension | "Model Context Protocol a Series of LF Projects, LLC"; founding project of Agentic AI Foundation (AAIF, Linux Foundation); BDFL + Core Maintainers + SEP process | Current revision **2026-07-28** (stateless redesign); prior 2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05 | LF (Dec 2025): >10,000 published servers; adopted by Claude, Cursor, Microsoft Copilot, Gemini, VS Code, ChatGPT | OAuth 2.1 based authorization (resource server model, RFC 8707 resource indicators, RFC 9207 iss), Security Best Practices page (confused deputy, token passthrough, SSRF, session hijacking, local server compromise, scope minimization), "tool annotations untrusted" principle |
| MCP Registry | harness to tool discovery/supply chain | MCP Registry Working Group (MCP project) | API freeze v0.1 (2025-10-24); preview since 2025-09-08; live API answers `/v0.1/servers`; server.json schema 2025-12-11 | Live registry with entries (registry.modelcontextprotocol.io) | Namespace-based publishing (e.g. reverse-DNS names); not verified further |
| Agent2Agent (A2A) | harness to harness / agent to agent (opaque agents) | Linux Foundation project contributed by Google; README now "Part of the Agentic AI Foundation"; AAIF projects page lists A2A | **1.0.0 (2026-03-12)**, patch **1.0.1 (2026-05-26)**; earlier 0.3.0 (2025-07-30) | Absorbed IBM's ACP; SDKs (a2a-sdk on PyPI); framework support via ADK, LangGraph, BeeAI (README) | TLS required in production; auth schemes declared in Agent Card `securitySchemes`; credentials out-of-band; `TASK_STATE_AUTH_REQUIRED` in-task authorization; JWS-signed Agent Cards with RFC 8785 canonicalization |
| Agent Communication Protocol (ACP, IBM/BeeAI) | agent to agent (REST) | Was LF project; **now part of A2A** | Merged/retired into A2A | n/a | n/a |
| Agent Client Protocol (ACP, Zed) | user-facing client/editor to agent harness | agentclientprotocol GitHub org (originated at Zed); formal foundation not verified | Stable protocol version **1** (schema v1 and v2 artifacts exist) | Official SDKs in Kotlin, Java, Python, Rust, TypeScript; agent/client lists on agentclientprotocol.com | Not reviewed (gap) |
| OpenTelemetry GenAI semantic conventions | harness to telemetry | OpenTelemetry (CNCF); moved to separate repo `open-telemetry/semantic-conventions-genai` | Status **Development** (not stable) for GenAI, agent, and MCP conventions; pins core semconv v1.45.0 | MCP 2026-07-28 spec documents OTel trace-context propagation in `_meta` | Content capture is opt-in style attributes (not verified in detail) |
| AGENTS.md | harness to instructions (repo-level) | Contributed by OpenAI to AAIF (Dec 2025) | No version number; convention (plain Markdown at repo root) | LF: >60,000 OSS projects; agents.md lists Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, GitHub Copilot, Windsurf, Augment Code, etc. | None in format |
| Agent Skills (SKILL.md) | harness to assets/procedural knowledge | Originally Anthropic, published as open standard at agentskills.io; GitHub `agentskills/agentskills` | Spec page undated; `allowed-tools` field Experimental | Client showcase lists ~45 clients incl. Claude Code, ChatGPT and Codex, Cursor, Gemini CLI, GitHub Copilot, VS Code, Goose, Junie, Kiro, OpenCode, OpenHands, Roo Code, Snowflake Cortex Code, Databricks, Mistral Vibe, Spring AI | `allowed-tools` pre-approval field (experimental); no signing/provenance |
| OWASP Top 10 for LLM Apps 2025 / Top 10 for Agentic Applications 2026 | cross-cutting security guidance (not an interface) | OWASP GenAI Security Project | LLM Top 10 2025; Agentic Top 10 published 2025-12-09 | Peer reviewed by >100 experts (OWASP) | Risk taxonomy (ASI01-ASI10) |
| NIST AI RMF 1.0 | governance framework (harness to policy/oversight) | NIST | Released 2023-01-26; "being revised as part of the White House AI Action Plan" | Voluntary | Risk mgmt functions; no protocol-level controls |
| ISO/IEC 42001 | AI management system (organizational) | ISO/IEC JTC 1/SC 42 | [Unreachable] iso.org returned 403 | n/a | n/a |

## Model Context Protocol (MCP): version, primitives, transports, authorization, governance, registry, security

### Takeaway
MCP's current revision is 2026-07-28, a major redesign that made MCP stateless (no initialize handshake, no sessions), introduced Multi Round-Trip Requests, moved Tasks to an extension, and **deprecated Roots, Sampling and Logging** and Dynamic Client Registration. Core server features are now Tools, Resources, Prompts; the client feature is Elicitation. Governance sits in an LF Projects series under the Linux Foundation's Agentic AI Foundation.

### Cited Findings
- [Established] "The current protocol version is 2026-07-28." Version identifiers are YYYY-MM-DD marking the last backwards-incompatible change; revisions are Draft / Current / Final; features can be Deprecated (min 12 months, or 90 days under expedited exception) before Removal. — [MCP Versioning](https://modelcontextprotocol.io/specification/versioning)
- [Established] Prior revisions referenced on the spec site: 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25. — [MCP spec latest](https://modelcontextprotocol.io/specification/latest)
- [Established] Schema is defined in TypeScript first (`schema/2026-07-28/schema.ts`) and published as JSON Schema; the repo is MIT-licensed (README) while governance doc says new contributions are Apache-2.0. — [MCP README](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/README.md); [Governance](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/community/governance.mdx)
- [Established] Architecture: JSON-RPC 2.0 between Hosts (LLM applications), Clients (connectors within host) and Servers; inspired by Language Server Protocol. Base protocol: "Stateless, self-contained requests; per-request capability negotiation." Server features: Resources, Prompts, Tools. Client features: Elicitation. Extensions: Tasks, Skills over MCP (working group), MCP Apps (interactive UI). — [MCP 2026-07-28 spec index](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/index.mdx)
- [Established] 2026-07-28 major changes: removed protocol-level sessions and `Mcp-Session-Id` (SEP-2567); removed `initialize` handshake; protocol version and client capabilities travel in each request's `_meta` (SEP-2575); new mandatory `server/discover` RPC; `subscriptions/listen` replaces HTTP GET stream and resources/subscribe; removed `ping`, `logging/setLevel`, `notifications/roots/list_changed`; Tasks moved to official extension `io.modelcontextprotocol/tasks` (SEP-2663); Multi Round-Trip Requests (`InputRequiredResult`) replace server-initiated requests such as `roots/list`, `sampling/createMessage`, `elicitation/create` (SEP-2322); required `resultType`; SSE resumability removed. — [2026-07-28 changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)
- [Established] Minor changes in 2026-07-28: `extensions` capability field; OpenTelemetry trace context propagation via `_meta` keys `traceparent`, `tracestate`, `baggage` (SEP-414); deterministic `tools/list` ordering for prompt-cache hit rates; required `Mcp-Method`/`Mcp-Name` headers on Streamable HTTP and `x-mcp-header` (SEP-2243); `ttlMs`/`cacheScope` caching (SEP-2549); RFC 9207 `iss` validation (SEP-2468); credentials bound to issuing authorization server (SEP-2352); JSON Schema 2020-12 for `inputSchema`/`outputSchema` (SEP-2106). — [same changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)
- [Established] Deprecated in 2026-07-28: **Roots, Sampling and Logging** (SEP-2577; migrate to tool parameters/resource URIs, direct provider APIs, stderr or OpenTelemetry); HTTP+SSE transport (migrate to Streamable HTTP); `includeContext` values `thisServer`/`allServers`; **OAuth Dynamic Client Registration (RFC 7591) deprecated in favor of Client ID Metadata Documents**. Also adopted a feature lifecycle/deprecation policy (SEP-2596) and PR-based SEP workflow (SEP-1850). — [same changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)
- [Proposed] Draft (post-2026-07-28) changelog: updates referenced Client ID Metadata Document draft to -03; restores `_meta` on several types dropped in 2026-07-28. — [draft changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/draft/changelog.mdx)
- [Established] Transports: stdio and Streamable HTTP (HTTP+SSE deprecated). — [2026-07-28 changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)
- [Established] Authorization (2026-07-28): built on OAuth 2.1 (draft-ietf-oauth-v2-1-13), RFC 6750, RFC 8414, RFC 7591, RFC 9728 (Protected Resource Metadata), Client ID Metadata Documents, OIDC Discovery. Protected MCP server = OAuth 2.1 resource server; MCP client = OAuth 2.1 client. Clients MUST implement RFC 8707 Resource Indicators with the server's canonical URI in both authorization and token requests. — [MCP Authorization 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [Established] Security Best Practices page sections: Confused Deputy, Token Passthrough, SSRF, Session Hijacking, Local MCP Server Compromise, Scope Minimization. — [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices)
- [Established] Spec security principles: user consent and control; data privacy; tools "represent arbitrary code execution"; "descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a trusted server." — [spec index](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/index.mdx)
- [Established] Governance: "Model Context Protocol a Series of LF Projects, LLC"; hierarchy Lead Maintainers (BDFL) > Core Maintainers > Maintainers > Contributors; individual (not company) membership; spec changes via SEPs; Lead Maintainer: David Soria Parra. — [Governance](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/community/governance.mdx)
- [Established] AAIF formed 2025-12-09 by the Linux Foundation with founding contributions of Anthropic's MCP, Block's goose and OpenAI's AGENTS.md; Platinum members AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. MCP had ">10,000 published MCP servers" and is "adopted by Claude, Cursor, Microsoft Copilot, Gemini, VS Code, ChatGPT". — [LF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [Established] MCP Registry: "like an app store for MCP servers"; preview launched 2025-09-08; API freeze v0.1 on 2025-10-24 ahead of v1 GA; maintained by Registry Working Group (Stacklok, PulseMCP, others). — [Registry README](https://raw.githubusercontent.com/modelcontextprotocol/registry/main/README.md). Live endpoint `registry.modelcontextprotocol.io/v0.1/servers` returns entries using server.json schema dated 2025-12-11. — [Registry API](https://registry.modelcontextprotocol.io/v0.1/servers?limit=1)

### Inferences
- [Inference] The 2026-07-28 deprecation of Sampling and Roots narrows MCP to a harness-to-tools/context boundary and pushes model access back to the harness (model↔harness is not MCP's job any more). Elicitation (via MRTR) remains the only client-provided feature in core.
- [Inference] Statelessness plus caching hints (`ttlMs`, deterministic ordering) indicate MCP is being optimized for remote, horizontally scaled servers and prompt-cache-friendly harnesses.
- [Synthesized] "Tool poisoning" is not a named section of the spec's security page as found; the spec's mitigation is the "annotations untrusted unless from trusted server" principle plus user consent; named risks covered are auth-centric (confused deputy, token passthrough, SSRF, session hijacking).

### Gaps
- Registry GA (v1) status as of Nov 2026 not confirmed; README still shows v0.1 freeze notice.
- Did not read the full Security Best Practices text for prompt-injection or tool-poisoning guidance; only section titles confirmed.
- Exact AAIF transfer date of MCP's LF Projects entity not confirmed beyond the Dec 2025 announcement.

## Agent2Agent (A2A): spec, governance, Agent Cards, relation to MCP

### Takeaway
A2A reached 1.0.0 on 2026-03-12 (1.0.1 on 2026-05-26), is a Linux Foundation project contributed by Google that now brands itself as part of AAIF, has three bindings (JSON-RPC, gRPC, HTTP+JSON/REST), uses Agent Cards at `/.well-known/agent-card.json` (optionally JWS-signed), and positions itself as complementary to MCP (agent↔agent vs. agent↔tool).

### Cited Findings
- [Established] Latest released version 1.0.0; previous 0.3.0, 0.2.6, 0.1.0. — [A2A spec](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] Release dates: 1.0.1 (2026-05-26), 1.0.0 (2026-03-12), 0.3.0 (2025-07-30), 0.2.x mid-2025. — [A2A CHANGELOG](https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md)
- [Established] Purpose: "communication and interoperability between opaque agentic applications"; agents discover capabilities, negotiate modalities, collaborate on long-running tasks "without exposing their internal state, memory, or tools." README states "Part of the Agentic AI Foundation" and "an open source project under the Linux Foundation, contributed by Google", Apache 2.0. — [A2A README](https://raw.githubusercontent.com/a2aproject/A2A/main/README.md)
- [Established] AAIF projects page lists Agent2Agent, AGENTS.md, agentgateway, goose, MCP (and Agent Router among others). — [aaif.io](https://aaif.io/)
- [Established] Version negotiation: clients MUST send `A2A-Version` header; agents MUST return `VersionNotSupportedError` for unsupported versions. Bindings: JSON-RPC (§9), gRPC (§10), HTTP+JSON/REST (§11). — [A2A spec](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] Security: production MUST use HTTPS/TLS (1.3+ recommended); clients SHOULD verify server TLS certs; auth requirements discovered via Agent Card `securitySchemes`, credentials obtained out-of-band and sent per request; server MUST authenticate every request; authorization is implementation-specific (skills, actions, data policies, OAuth scopes); in-task authorization via `TASK_STATE_AUTH_REQUIRED`, chainable across agents. — [A2A spec §7](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] Agent Card discovery at `https://{server_domain}/.well-known/agent-card.json`; Agent Cards MAY be signed with JWS (RFC 7515) after RFC 8785 JSON canonicalization, `signatures` field excluded. — [A2A spec §8](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] Appendix B: MCP standardizes agent connection to tools/APIs/data; A2A standardizes agent-to-agent collaboration; an A2A server agent may use MCP internally. — [A2A spec App. B](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] IBM's Agent Communication Protocol: "ACP is now part of A2A under the Linux Foundation!" — [agentcommunicationprotocol.dev](https://agentcommunicationprotocol.dev/)

### Inferences
- [Inference] A2A covers delegation of authorization but deliberately leaves authorization policy implementation-specific, which is a policy gap.

### Gaps
- Date A2A moved under the AAIF umbrella not found in sources read.
- Quantitative adoption (number of A2A agents in production) not found.

## OpenTelemetry GenAI semantic conventions

### Takeaway
GenAI conventions (client inference, agents, tools, evaluation, memory, MCP) have moved to a dedicated repo `open-telemetry/semantic-conventions-genai`; every document read is still Status: **Development** (not Stable).

### Cited Findings
- [Established] Main semconv repo and opentelemetry.io pages now say "GenAI semantic conventions have moved to the OpenTelemetry GenAI semantic conventions repository". — [semconv gen-ai-spans.md stub](https://raw.githubusercontent.com/open-telemetry/semantic-conventions/main/docs/gen-ai/gen-ai-spans.md); [opentelemetry.io gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/index.md)
- [Established] New repo covers spans, metrics and events for GenAI clients, MCP and provider-specific conventions (OpenAI, etc.); namespaces `gen_ai.*`, `mcp.*`, `openai.*`; managed with Weaver; Schema URL "TODO". — [semconv-genai README](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/README.md); [docs README](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/README.md)
- [Established] GenAI README: Status Development. Agent spans doc: Status Development; spans include Create agent (`create_agent`), Invoke agent client and internal spans (`invoke_agent`), `invoke_workflow`, Plan span, Execute tool span. Client spans doc: Inference, Embeddings, Retrievals, Fetch response, Memory spans, all Development. Pins core semconv v1.45.0. — [gen-ai README](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md); [agent spans](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md); [client spans](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md)
- [Established] MCP conventions: Status Development; client and server spans, context propagation; status description should match `JSONRPCError.message`. — [MCP semconv](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/mcp.md)
- [Established] MCP 2026-07-28 documents trace-context propagation via `_meta` and recommends OpenTelemetry instead of the deprecated Logging feature. — [MCP changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)

### Inferences
- [Synthesized] Telemetry is the boundary where MCP and OTel now explicitly interlock (trace context in `_meta`, `mcp.*` attributes), but stability is still Development, so attribute names can change.

### Gaps
- GitHub API blocked, so no release tag/date for semantic-conventions-genai could be retrieved; date of the repo split not found.
- AAIF has an "Observability & Traceability" working group (aaif.io) but no output was found.

## Instruction and asset conventions: AGENTS.md, Agent Skills, CLAUDE.md-like files

### Takeaway
AGENTS.md (OpenAI-originated, now AAIF) is the de facto repo-instruction file with broad tool support; Agent Skills (SKILL.md, Anthropic-originated open standard at agentskills.io) standardizes packaged procedural assets with progressive disclosure and is listed as supported by ~45 clients including OpenAI, Google, GitHub and Cursor products. Neither has a version number or security model beyond an experimental `allowed-tools` field.

### Cited Findings
- [Established] AGENTS.md: plain Markdown file at repo root, "a clear, predictable place for instructions" for agents, separate from README; compatible agents listed include Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, UiPath, Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot coding agent, Ona, Windsurf, Augment Code; "60k+ examples on GitHub". — [agents.md](https://agents.md/)
- [Established] LF: AGENTS.md "adopted by more than 60,000 open source projects and agent frameworks including Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code". — [LF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [Established] Agent Skills spec: a skill is a directory with required `SKILL.md` (YAML frontmatter + Markdown) and optional `scripts/`, `references/`, `assets/`; frontmatter `name` (required, 1-64 lowercase/hyphen chars, matches dir), `description` (required, 1-1024 chars, what and when), optional `license`, `compatibility` (≤500 chars), `metadata` map, `allowed-tools` ("Experimental. Support ... may vary"); progressive disclosure. — [agentskills.io specification](https://agentskills.io/specification)
- [Established] "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products." Development on GitHub `agentskills/agentskills`. — [agentskills.io](https://agentskills.io/)
- [Established] Client showcase includes Claude Code, Claude, ChatGPT & Codex, Cursor, Gemini CLI, GitHub Copilot, VS Code, Goose, Junie, Kiro, OpenCode, OpenHands, Roo Code, Factory, Amp, Letta, Mistral AI Vibe, Snowflake Cortex Code, Databricks Genie Code, Spring AI, TRAE, Tabnine, Qodo, Pulumi Neo, and others (~45 entries). — [agentskills.io clients](https://agentskills.io/clients)
- [Established] MCP lists "Skills over MCP" as a working-group extension for discovering skills through MCP. — [MCP spec index](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/index.mdx)

### Inferences
- [Inference] CLAUDE.md, GEMINI.md and similar vendor files persist alongside AGENTS.md; I did not verify each vendor's current support for AGENTS.md vs. its own filename.
- [Inference] Agent Skills governance is not shown as an AAIF project on aaif.io's project list as read; it remains Anthropic-originated with community GitHub.

### Gaps
- No version or dated changelog for AGENTS.md or Agent Skills spec found.
- No signing/provenance mechanism for skills or AGENTS.md found (supply-chain gap).

## Other relevant: Agent Client Protocol, IBM ACP, function calling, AAIF, OWASP, NIST, ISO

### Takeaway
Zed's Agent Client Protocol fixes the editor↔agent boundary (stable protocol v1); IBM's ACP merged into A2A; AAIF (Dec 2025) is the umbrella for MCP, AGENTS.md, goose, A2A, agentgateway; OWASP provides the security taxonomy (LLM Top 10 2025, Agentic Top 10 2026); NIST AI RMF 1.0 is under revision.

### Cited Findings
- [Established] Agent Client Protocol "standardizes communication between code editors ... and coding agents"; "The current stable ACP protocol version is `1`"; wire compatibility negotiated via `protocolVersion` in `initialize`; official SDKs Kotlin, Java, Python, Rust, TypeScript; repo now under `agentclientprotocol` org. — [ACP README](https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/README.md)
- [Established] LF press release states OpenAI "has contributed ACP, Codex CLI, and the Agents SDK and Apps SDK" to the open ecosystem (which ACP is meant is ambiguous in the text). — [LF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [Established] AAIF working groups: Accuracy & Reliability, Agentic Commerce, Governance Risk & Regulatory Alignment, Identity & Trust, Observability & Traceability, Security (truncated list); events AGNTCon + MCPCon. — [aaif.io](https://aaif.io/)
- [Established] OWASP Top 10 for LLM Applications 2025: LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption. — [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
- [Established] OWASP Top 10 for Agentic Applications 2026 published 2025-12-09, >100 experts: ASI01 Agent Goal Hijack, ASI02 Tool Misuse, ASI03 Identity & Privilege Abuse, ASI04 Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution, ASI06 Memory & Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue Agents. "Securing Agentic Applications V2" published 2026-11-10. — [OWASP Agentic Top 10 page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/); [OWASP announcement](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [Established] NIST AI RMF 1.0 released 2023-01-26, voluntary; "being revised as part of the White House AI Action Plan"; NIST also developing a critical-infrastructure profile. — [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [Unreachable] ISO/IEC 42001 page (iso.org returned 403).

### Inferences
- [Inference] OWASP ASI02/ASI03/ASI07 map onto MCP (tool), identity/policy, and A2A (inter-agent) boundaries respectively; ASI06 maps onto memory, which no interface standard covers.

### Gaps
- OpenAI function-calling / JSON Schema tool-definition docs not fetched (time budget); model↔harness boundary evidence is thin. Note: MCP 2026-07-28 adopted JSON Schema 2020-12 for tool schemas (Established, see MCP section).
- NIST AI 600-1 GenAI Profile and any NIST agent-specific work not verified in this run.

## Overlaps and gaps across protocols

### Takeaway
Interfaces are now standardized for harness↔tools (MCP), agent↔agent (A2A), editor↔agent (Agent Client Protocol), harness↔telemetry (OTel GenAI, still Development), and harness↔instructions/assets (AGENTS.md, Agent Skills). The model↔harness boundary, permission/policy, and memory remain unstandardized.

### Cited Findings
- [Established] A2A leaves authorization logic "implementation-specific". — [A2A spec §7.5](https://raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md)
- [Established] MCP deprecated Sampling (model access through client) and recommends integrating directly with LLM provider APIs. — [MCP changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)
- [Established] Agent Skills `allowed-tools` is experimental and varies by implementation. — [agentskills.io specification](https://agentskills.io/specification)
- [Established] OTel has `Memory` spans (Development), i.e. memory is observed but its interface is not defined. — [client spans](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md)

### Inferences
- [Synthesized] Overlaps: MCP Prompts/Resources and Skills-over-MCP overlap with Agent Skills and AGENTS.md (instructions/assets); MCP Tasks extension overlaps A2A Tasks for long-running work; both MCP and A2A use OAuth-family auth but with different discovery (RFC 9728 metadata vs. Agent Card `securitySchemes`).
- [Inference] Gaps: (1) no standard for harness permission/policy (tool allow/deny, sandbox, approval UX) — only experimental `allowed-tools` and consent principles; (2) no memory interface standard; (3) model↔harness wire API is vendor-defined (OpenAI/Anthropic/Gemini APIs), with no neutral-body standard found; (4) no signing/provenance for skills or instruction files, unlike A2A signed Agent Cards; (5) telemetry conventions not stable.

### Gaps
- No primary source found that formally catalogues these gaps; AAIF "Identity & Trust" and "Security" working groups may address them but no outputs were found.
