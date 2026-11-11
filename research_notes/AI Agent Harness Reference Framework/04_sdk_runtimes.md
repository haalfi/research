# SDK runtimes mapped to harness responsibilities: OpenAI Agents SDK, Claude Agent SDK, LangGraph

Method: shallow `git clone` of each repo into the scratchpad on 2026-11-11, then grep and read of the source and of the in-repo docs. No cloned code was run. Live docs were fetched as `.md` from code.claude.com and docs.langchain.com on 2026-11-11. Source links are pinned to the cloned commit. Evidence tier: vendor docs and source are implementation evidence (tier 3). Anything a vendor says about capability or reliability counts as a vendor claim, not a verified result.

Labels: **[E]** Established means read directly in source or docs. **[S]** Synthesized means combined from several sources. **[P]** Proposed is a framework suggestion. **[Inf]** marks inference. **[U]** marks a source that could not be reached or was not checked.

Short base URLs used below:
- OAI = https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775
- OAI-docs = https://openai.github.io/openai-agents-python (the same Markdown lives in `OAI/docs/*.md`)
- CAS = https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946
- CC = https://code.claude.com/docs/en/agent-sdk
- LG = https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec
- DA = https://github.com/langchain-ai/deepagents/blob/f2a6e02dc8e2dcb05885c5133b94102ccc79b794
- LC = https://docs.langchain.com

## Q0. Versions and the dates of what was checked

### Takeaway
All three code bases are being changed almost daily. The cloned versions are openai-agents 0.24.0, claude-agent-sdk 0.2.180 (which bundles Claude Code CLI 2.1.318 or later), langgraph 1.2.20 with prebuilt 1.1.1 and checkpoint 4.3.1, and deepagents 0.7.35. Docs were checked on 2026-11-11.

### Cited Findings
- [E] OpenAI Agents SDK `version = "0.24.0"`, head commit dated 2026-11-11 — [pyproject.toml](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/pyproject.toml)
- [E] Claude Agent SDK (Python) `__version__ = "0.2.180"`, head commit dated 2026-11-10. The CHANGELOG entry for 0.2.178 says "Updated bundled Claude CLI to version 2.1.318" — [_version.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/_version.py), [CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/CHANGELOG.md)
- [E] LangGraph versions in the monorepo: langgraph 1.2.20, langgraph-prebuilt 1.1.1, langgraph-checkpoint 4.3.1, checkpoint-postgres 3.2.0, checkpoint-sqlite 3.1.3. Head commit dated 2026-11-10 — [libs/langgraph/pyproject.toml](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/pyproject.toml)
- [E] deepagents `version = "0.7.35"`, head commit dated 2026-11-11 — [libs/deepagents/pyproject.toml](https://github.com/langchain-ai/deepagents/blob/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/pyproject.toml)

### Inferences
- [Inf] The Python package version of the Claude Agent SDK says little about its capabilities. Behaviour belongs to the bundled CLI, and the docs gate features on CLI versions such as "requires Claude Code v2.1.217". A reference framework should record the CLI version alongside the SDK version.

### Gaps
- [U] The LangChain `langchain` package that provides `create_agent` and its middleware was not cloned. Statements about it rest on docs.langchain.com and on how deepagents imports it, so no version number is recorded for it.
- I did not check the TypeScript SDK versions (openai-agents-js, @anthropic-ai/claude-agent-sdk, langgraphjs).

## Q1. OpenAI Agents SDK (Python): the loop, tools, context, memory, control, durability, tracing and multi-agent support

### Takeaway
One library owns the loop. `Runner.run`, `run_sync` and `run_streamed` drive a turn loop. Each model response is sorted into one of four next steps: final output, handoff, run again or interruption. The loop stops on final output, raises `MaxTurnsExceeded` after 10 turns by default, or pauses at an interruption that can be serialized as a `RunState`. Control is spread across guardrails (input, output and tool), approvals (`needs_approval` together with `RunState` approve or reject), and lifecycle hooks (`RunHooks` and `AgentHooks`). Durable execution is not built in. The SDK points to Temporal, Dapr, Restate and DBOS integrations.

### Cited Findings
**Loop**
- [E] There are three entry points. `Runner.run()` is async, `run_sync()` wraps it, and `run_streamed()` returns `RunResultStreaming` with `.stream_events()`. The input can be a string, a list of Responses-API items, or a `RunState` when resuming — [OAI/docs/running_agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/running_agents.md)
- [E] The loop works like this. The model is called. If the output counts as final output, the run returns. If the model asks for a handoff, the current agent and input are replaced and the loop runs again. Tool calls are executed, their results appended, and the loop runs again. Going past `max_turns` raises `MaxTurnsExceeded`, and `max_turns=None` disables the limit. Output is "final" when it is text of the desired type and contains no tool calls — same doc.
- [E] The default is `DEFAULT_MAX_TURNS = 10` — [src/agents/run_config.py L45](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/run_config.py#L45)
- [E] The internal step types are `NextStepFinalOutput`, `NextStepHandoff`, `NextStepRunAgain` and `NextStepInterruption`. `Runner.run` also accepts `error_handlers` keyed by error kind, so a max-turns error can be handled — [src/agents/run.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/run.py). The loop logic lives in the `src/agents/run_internal/` package (approvals.py, guardrails.py, error_handlers.py, model_retry.py and others) — [run_internal/](https://github.com/openai/openai-agents-python/tree/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/run_internal)
- [E] `Agent.tool_use_behavior` sets whether tool results go back to the model or end the run, for example `"stop_on_first_tool"` — [OAI/docs/agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/agents.md)
- [E] A run can also be stopped with `cancel(mode="after_turn")` and resumed from a `RunState` — running_agents.md (above).

**Tools**
- [E] The classes in `tool.py` are `FunctionTool`, `FileSearchTool`, `WebSearchTool`, `ComputerTool`, `HostedMCPTool`, `CodeInterpreterTool`, `ImageGenerationTool`, `LocalShellTool`, `ShellTool`, `ApplyPatchTool`, `CustomTool`, `ToolSearchTool` and `ProgrammaticToolCallingTool` — [src/agents/tool.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/tool.py)
- [S] Hosted tools run on OpenAI's side through the Responses API. These include file search, web search, code interpreter, image generation and hosted MCP. Function, shell and apply_patch tools run locally. The split is inferred from the class names together with the docs' "hosted vs local MCP" distinction — [OAI/docs/mcp.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/mcp.md)
- [E] MCP has five integration modes: hosted MCP (`HostedMCPTool`), Streamable HTTP, SSE, stdio and an MCP server manager. Tool filtering can be static or dynamic, and the docs also cover prompts, caching and tracing for MCP. Local MCP servers accept `require_approval` — [OAI/docs/mcp.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/mcp.md)
- [E] Sandbox Agents give the model "a persistent workspace" with a `Manifest`, sandbox capabilities and `SandboxRunConfig`. `UnixLocalSandboxClient` adds no OS-level confinement on Linux. Provider extensions exist for blaxel, cloudflare, daytona, e2b, modal and vercel, and a Docker extra is available — [OAI/docs/sandbox_agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/sandbox_agents.md), [src/agents/extensions/sandbox/](https://github.com/openai/openai-agents-python/tree/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/extensions/sandbox)
- [E] `RunConfig.tool_execution` (`ToolExecutionConfig(max_function_tool_concurrency=...)`), `tool_not_found_behavior` and `tool_name_collision_policy` configure how tools are executed — running_agents.md.

**Context**
- [E] Instructions can be static, dynamic (a function) or a prompt template. `RunConfig.call_model_input_filter` can edit "the fully prepared model input (instructions and input items) immediately before the model call" — [agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/agents.md), running_agents.md
- [E] Local context (`RunContextWrapper`, `ToolContext`) is kept separate from the context the LLM sees — [OAI/docs/context.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/context.md)
- [E] Compaction comes from `OpenAIResponsesCompactionSession`, which wraps another session and calls `responses.compact`. It can compact automatically after each turn based on `should_trigger_compaction` — context.md. Separately, `ToolOutputTrimmer` lives in extensions — [src/agents/extensions/tool_output_trimmer.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/extensions/tool_output_trimmer.py)
- [E] The context passed in a handoff can be shaped with `Handoff.input_filter` and the global `RunConfig.handoff_input_filter`. There is also an opt-in beta, `nest_handoff_history`, which "compacts summarizable history into ordered assistant summary segments", and a `handoff_history_mapper` — running_agents.md

**Memory/state**
- [E] The `Session` protocol is implemented by `SQLiteSession` (built in), `AsyncSQLiteSession`, `RedisSession`, `SQLAlchemySession`, `MongoDBSession`, `DaprSession`, an encrypted session, `AdvancedSQLiteSession`, `OpenAIConversationsSession` (server-side) and `OpenAIResponsesCompactionSession`. History is merged with new input through `session_input_callback` and limited with `SessionSettings(limit=...)` — [OAI/docs/sessions/index.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/sessions/index.md), [src/agents/memory/](https://github.com/openai/openai-agents-python/tree/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/memory), [src/agents/extensions/memory/](https://github.com/openai/openai-agents-python/tree/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/extensions/memory)
- [E] Long-term memory for sandbox agents is a `Memory()` capability that "distills lessons from prior runs into files in the sandbox workspace". The docs describe it as separate from conversational `Session` memory — [OAI/docs/sandbox/memory.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/sandbox/memory.md)
- [E] Paused-run state is a `RunState` that can be serialized with `to_string()`/`from_string()` or `to_json()`/`from_json()` — [OAI/docs/human_in_the_loop.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/human_in_the_loop.md)

**Control**
- [E] Guardrails. Input guardrails run only for the first agent, and output guardrails only for the last. Tool guardrails (`ToolInputGuardrail` and `ToolOutputGuardrail`) run on every guarded function-tool call, including local MCP tools. Input guardrails run in parallel with the agent by default (`run_in_parallel=True`), so tokens and tools can be spent before a tripwire fires. Blocking mode is `run_in_parallel=False`. A tripwire raises `InputGuardrailTripwireTriggered` or `OutputGuardrailTripwireTriggered` — [OAI/docs/guardrails.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/guardrails.md), [src/agents/guardrail.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/guardrail.py), [src/agents/tool_guardrails.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/tool_guardrails.py)
- [E] Approvals and human-in-the-loop. `needs_approval` (a bool or a callable) is available on `function_tool`, `Agent.as_tool`, `ShellTool` and `ApplyPatchTool`. MCP has `require_approval`. A pending approval appears as a `ToolApprovalItem` in `RunResult.interruptions`. The caller runs `result.to_state()`, then `state.approve()` or `state.reject()`, then `Runner.run(agent, state)`. Approvals are run-wide, so they also cover handoffs and nested `as_tool` runs. Sticky decisions are set with `always_approve` or `always_reject`. Callable rules fail closed on malformed arguments. A documented caveat: sticky shell and apply_patch decisions are not scoped to an agent — human_in_the_loop.md
- [E] Hooks. `RunHooks` cover the whole run and `AgentHooks` are attached per agent. They observe agent start and end, LLM calls, tool calls and handoffs — [agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/agents.md), [src/agents/lifecycle.py](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/lifecycle.py)

**Durable execution**
- [E] The section "Durable execution integrations and human-in-the-loop" lists four third-party integrations. Dapr (through Diagrid) offers "durable, long-running agents that automatically recover from failures". Temporal (`temporalio.contrib.openai_agents`) offers durable long-running workflows including HITL. Restate offers durable agents with approval, handoffs and session management. DBOS preserves progress across failures and needs only SQLite or Postgres — [running_agents.md §Durable execution](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/running_agents.md) (the reliability wording is a vendor claim)

**Tracing**
- [E] Tracing is on by default. A `TraceProvider` with a `BatchTraceProcessor` sends traces through a `BackendSpanExporter` to OpenAI. `add_trace_processor()` adds a destination and `set_trace_processors()` replaces the default ones. Tracing can be turned off with `OPENAI_AGENTS_DISABLE_TRACING=1` or `RunConfig.tracing_disabled`, and `trace_include_sensitive_data` controls payload capture. The docs list external processors in an ecosystem section — [OAI/docs/tracing.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/tracing.md)

**Multi-agent**
- [E] Two patterns are documented. In a handoff, the LLM chooses and control passes to another agent. In the manager pattern, agents are called as tools with `Agent.as_tool()`. Code-driven orchestration is also documented — [agents.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/agents.md), [multi_agent.md](https://github.com/openai/openai-agents-python/blob/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/docs/multi_agent.md)
- [E] Experimental extensions `codex` and `hosted_multi_agent` exist — [src/agents/extensions/experimental/](https://github.com/openai/openai-agents-python/tree/64fbde5d02b42ae5f9db668eb0184cdb3fc9d775/src/agents/extensions/experimental)

**Extensibility**
- [E] The documented extension points are model providers (`MultiProvider`, LiteLLM and any-llm extensions), custom session backends, sandbox providers, trace processors, `call_model_input_filter`, handoff filters, error handlers and lifecycle hooks — sources above.

### Inferences
- [Inf] "Control" is split across four mechanisms: guardrails, approvals, hooks and error handlers. Approvals are tied into state, since an approval pauses the run as a `RunState`. That makes human-in-the-loop part Control and part Memory/state.
- [Inf] With input guardrails running in parallel by default, a guardrail here is a detector rather than a gate unless the caller opts into blocking mode.

### Gaps
- I did not read the contents of `hosted_multi_agent` or the Temporal contrib module, so their semantics are unknown.
- I did not trace the realtime and voice runners (`src/agents/realtime/runner.py`), which run a separate loop.

## Q2. Claude Agent SDK: how it relates to Claude Code, the query loop, tools, permissions, hooks, subagents, skills, settings, compaction, MCP and sessions

### Takeaway
The Claude Agent SDK is a thin client around the Claude Code harness. The Python package launches the bundled Claude Code CLI as a subprocess and speaks a JSON control protocol over stdio. The loop, tools, compaction, permissions, subagents and telemetry all run inside the CLI. The SDK adds programmatic options and callbacks on top: `can_use_tool`, hook callbacks, in-process MCP tools and `SessionStore`. It is the only one of the three systems that ships a full built-in toolset and a layered permission model by default.

### Cited Findings
**Relationship to Claude Code**
- [E] The overview says "Build production AI agents with Claude Code as a library". The SDK gives "the same tools, agent loop, and context management that power Claude Code". It is "A library that runs the Claude Code binary". The overview contrasts it with Managed Agents, "A hosted agent harness that runs the agent loop" — [CC/overview](https://code.claude.com/docs/en/agent-sdk/overview.md)
- [E] The README says "The Claude Code CLI is automatically bundled with the package", and `cli_path` can override it. The transport is `subprocess_cli.py` — [README.md](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/README.md), [_internal/transport/subprocess_cli.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/_internal/transport/subprocess_cli.py)
- [E] The control-protocol request subtypes in `types.py` include `interrupt`, `can_use_tool`, `initialize`, `set_permission_mode`, `hook_callback`, `mcp_message`, `rewind_files`, `mcp_reconnect`, `mcp_toggle` and `stop_task` — [types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py)

**Loop**
- [E] There are two entry points. `query()` is a one-shot async iterator. `ClaudeSDKClient` keeps a conversation going across calls — README; [CC/sessions](https://code.claude.com/docs/en/agent-sdk/sessions.md)
- [E] The loop goes: prompt received, `SystemMessage(init)` emitted, then Claude evaluates, calls tools and repeats. It ends with a text-only `AssistantMessage` followed by a `ResultMessage` carrying the result, usage, cost and session_id. `max_turns` counts each turn that calls tools plus one for the final turn, and has no default limit. `max_budget_usd` also exists. The result subtypes are `success`, `error_max_turns`, `error_max_budget_usd`, `error_max_structured_output_retries` and others. Streaming partial messages are enabled with `include_partial_messages`. Read-only tools run in parallel and state-changing tools run in sequence. Custom tools run in parallel only if they set `readOnlyHint` — [CC/agent-loop](https://code.claude.com/docs/en/agent-sdk/agent-loop.md), [types.py ClaudeAgentOptions](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py)
- [E] Other loop-related options on `ClaudeAgentOptions` include `effort`, `thinking`, `fallback_model`, `output_format` (structured output), `task_budget` and `forward_subagent_text` — types.py

**Tools**
- [E] Built-in tools are `Read`, `Edit` and `Write` for files, `Glob` and `Grep` for search, `Bash` for execution, `WebSearch` and `WebFetch` for the web, `ToolSearch` for discovery, and `Agent`, `Skill`, `AskUserQuestion`, `TaskCreate` and `TaskUpdate` for orchestration — [CC/agent-loop §Built-in tools](https://code.claude.com/docs/en/agent-sdk/agent-loop.md)
- [E] Custom tools are written with the `@tool` decorator and `create_sdk_mcp_server()`, which runs an MCP server inside the Python process. External MCP servers are configured as `McpServerConfig`, which can be stdio, SSE, HTTP or SDK. `strict_mcp_config` is also available — [__init__.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/__init__.py), [types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py), [CC/custom-tools](https://code.claude.com/docs/en/agent-sdk/custom-tools.md) [listing only]
- [E] Sandboxing comes from `SandboxSettings`, which "controls how Claude Code sandboxes bash commands for filesystem and network isolation". Its docstring says tool-level file and network restrictions belong in permission rules instead. There are no hosted, server-side tools. Everything runs on the host or inside the sandbox — types.py `SandboxSettings`

**Context**
- [E] Instructions are assembled from `system_prompt`, which is either a string or the `claude_code` preset with `append`, plus CLAUDE.md files and `.claude/rules/*.md` loaded through `setting_sources`. All levels are additive with "no hard precedence rule". Leaving `setting_sources` out is the same as `["user","project","local"]`. Managed policy and `~/.claude.json` are read no matter what `setting_sources` says. For multi-tenant isolation the docs advise `settingSources: []` together with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — [CC/claude-code-features](https://code.claude.com/docs/en/agent-sdk/claude-code-features.md)
- [E] Compaction is automatic. When the context is close to its limit, older history is summarized and a `SystemMessage` with subtype `compact_boundary` is emitted. It can be customized in three ways: summarization guidance in CLAUDE.md, a `PreCompact` hook (trigger `manual` or `auto`), and a manual `/compact` prompt. Stable prefixes are prompt-cached — [CC/agent-loop §Automatic compaction](https://code.claude.com/docs/en/agent-sdk/agent-loop.md)
- [E] Subagent context starts fresh, except for forks. Only the Agent tool's prompt string is passed down. The subagent gets its own `AgentDefinition.prompt`, the project CLAUDE.md (unless `omitClaudeMd` is set) and its tool subset. It does not get the parent's history or system prompt. Only the subagent's final message goes back to the parent, and that message is scanned for instruction-shaped patterns from v2.1.210 — [CC/subagents](https://code.claude.com/docs/en/agent-sdk/subagents.md)

**Memory/state**
- [E] Sessions are JSONL transcripts stored under `~/.claude/projects/<encoded-cwd>/`. The options `continue_conversation`, `resume`, `fork_session`, `resume_session_at` and `session_id` control continuation. A `SessionStore` adapter mirrors transcripts to external storage so that other hosts can resume them. Forking branches the conversation but not the filesystem. File changes are handled separately by `enable_file_checkpointing` and `rewind_files` — [CC/sessions](https://code.claude.com/docs/en/agent-sdk/sessions.md), [types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py), [_internal/session_store.py](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/_internal/session_store.py)
- [E] Long-term memory is file-based. It consists of CLAUDE.md files at user, project and local levels, plus "auto memory", which can be disabled with `CLAUDE_CODE_DISABLE_AUTO_MEMORY`. `AgentDefinition.memory` takes `"user" | "project" | "local"` — claude-code-features; types.py `AgentDefinition`

**Control**
- [E] Permission modes are `default`, `acceptEdits`, `plan`, `bypassPermissions`, `dontAsk` and `auto`. In `auto`, "a model classifier reviews actions" — [types.py L25](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py#L25), [CC/permissions](https://code.claude.com/docs/en/agent-sdk/permissions.md)
- [E] Permissions are evaluated in six steps: hooks, then deny rules, then ask rules, then the permission mode, then allow rules, then the `canUseTool` callback. A hook that returns `allow` does not skip the deny or ask steps. In `dontAsk` the callback step turns into a denial — [CC/permissions §How permissions are evaluated](https://code.claude.com/docs/en/agent-sdk/permissions.md)
- [E] The hook events are `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `Notification`, `SubagentStart` and `PermissionRequest`. Hooks are registered with `HookMatcher`. `on_failure="block"` was added in 0.2.177 — [types.py L286](https://github.com/anthropics/claude-agent-sdk-python/blob/3cf3446b0fa6c97042e85b245bba07459f22f946/src/claude_agent_sdk/types.py#L286), CHANGELOG
- [E] Human-in-the-loop works through `can_use_tool` callbacks and the `AskUserQuestion` tool. The process is never suspended to durable storage. The callback is awaited while the subprocess stays alive — [CC/permissions](https://code.claude.com/docs/en/agent-sdk/permissions.md); the docs link to [CC/user-input](https://code.claude.com/docs/en/agent-sdk/user-input) [U: not fetched]

**Multi-agent**
- [E] Subagents can be defined in code with `agents: dict[str, AgentDefinition]` (description, prompt, tools, disallowedTools, model, skills, memory, MCP servers, effort). They can also be defined as `.claude/agents/*.md` files. A built-in `general-purpose` agent exists. Subagents run in the background by default (`async_launched`). Forks use `subagent_type: "fork"`. `SendMessage` lets agents address each other by name. The budget cap includes subagent spend — [CC/subagents](https://code.claude.com/docs/en/agent-sdk/subagents.md), [CC/agent-loop](https://code.claude.com/docs/en/agent-sdk/agent-loop.md)

**Skills, plugins and extensibility**
- [E] Skills are discovered from `.claude/skills` through `setting_sources`. `skills="all"`, a list, or `[]` controls them, and setting `skills` adds the `Skill` tool automatically. Plugins (`SdkPluginConfig`) bundle skills, agents, hooks and MCP servers — [CC/claude-code-features](https://code.claude.com/docs/en/agent-sdk/claude-code-features.md), [CC/skills](https://code.claude.com/docs/en/agent-sdk/skills.md), [CC/plugins](https://code.claude.com/docs/en/agent-sdk/plugins.md) [listing only]

**Tracing and durable execution**
- [E] OpenTelemetry. "The SDK does not produce telemetry of its own". The CLI emits OTLP traces (spans around model requests and tool runs), metrics (tokens, cost, tool decisions) and log events — [CC/observability](https://code.claude.com/docs/en/agent-sdk/observability.md)
- [S] No durable-execution engine is documented. Durability is approximated by persisting transcripts (`SessionStore`) and resuming them. The hosting guide covers "subprocess architecture, session persistence, scaling" — [CC/hosting](https://code.claude.com/docs/en/agent-sdk/hosting.md) [listing only, page not fetched]

### Inferences
- [Inf] Each harness responsibility here has two layers: the CLI, which provides the mechanism, and the SDK, which provides configuration and callbacks. A framework should record "where it executes" separately from "where it is configured".
- [Inf] Context and Memory overlap here. CLAUDE.md is both instructions that get assembled into context and long-term memory, and compaction guidance is itself written in CLAUDE.md.

### Gaps
- [U] I did not fetch the hosting, session-storage, user-input or custom-tools pages, so their details come from the llms.txt descriptions only.
- I did not look at any built-in durable "resume after crash" for a run in progress. Resuming from a JSONL transcript restores the conversation, not a tool call that was mid-flight. [Inf]

## Q3. LangGraph: graph and state model, checkpointers and durability, interrupts, Store, prebuilt agents and create_agent middleware, deep agents, and Agent Server

### Takeaway
LangGraph is the low-level runtime. It runs a Pregel/BSP superstep engine over a typed state graph, with checkpointing after each step. That makes durable execution, human-in-the-loop interrupts and time travel part of the core rather than add-ons. The agent loop is not built into LangGraph. It comes from the layers on top: LangChain `create_agent` with middleware, which replaces `langgraph.prebuilt.create_react_agent`, and Deep Agents, an opinionated harness of middleware for planning, filesystem, subagents, summarization, skills, memory and HITL. Deployment uses LangSmith Agent Server, which supplies the checkpointer and store, PostgreSQL, a task queue and cron.

### Cited Findings
**Loop and graph model**
- [E] The Pregel engine is implemented in `langgraph/pregel/` (`_loop.py`, `_runner.py`, `_algo.py`, `_checkpoint.py`, `_retry.py` and others) — [libs/langgraph/langgraph/pregel/](https://github.com/langchain-ai/langgraph/tree/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/langgraph/pregel)
- [E] The termination guard is the recursion limit. `DEFAULT_RECURSION_LIMIT` reads env `LANGGRAPH_DEFAULT_RECURSION_LIMIT` and defaults to "10007" supersteps — [_internal/_config.py L42](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/langgraph/_internal/_config.py#L42). deepagents sets `"recursion_limit": 9_999` — [deepagents/graph.py L1039](https://github.com/langchain-ai/deepagents/blob/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/deepagents/graph.py#L1039)
- [E] Streaming modes are `StreamMode = "values" | "updates" | "checkpoints" | "tasks" | "debug" | "messages" | "custom"`. The control primitives are `Send` (fan-out), `Command` (goto, update and resume), `RetryPolicy` and `CachePolicy` — [types.py](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/langgraph/types.py)
- [E] The Functional API (`@task`, `@entrypoint`) is an alternative to `StateGraph` — [func/__init__.py](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/langgraph/func/__init__.py)
- [E] `create_agent` is "a model calling tools in a loop until a task is complete, shaped by a harness of prompt, tools, and middleware". "Middleware is the primitive for customization". The node-style hooks include `before_model` and `after_model` — [LC/oss/python/langchain/agents](https://docs.langchain.com/oss/python/langchain/agents.md)
- [E] The prebuilt package points to `create_agent`. For example, `ValidationNode is deprecated. Please use create_agent from langchain.agents`, and `AgentStatePydantic` is deprecated "in favor of AgentState in langchain.agents" — [prebuilt/tool_validator.py](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/prebuilt/langgraph/prebuilt/tool_validator.py), [prebuilt/chat_agent_executor.py](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py)

**Memory/state and durability**
- [E] Checkpointers persist each thread's graph state, keyed by `thread_id`, and are used "for … conversation continuity, human-in-the-loop workflows, time travel, and fault tolerance". Stores hold application-defined key-value data that lives across threads and serves as long-term memory. Compile with `builder.compile(checkpointer=..., store=...)`. Implementations include `InMemorySaver`, `PostgresSaver` and SQLite — [LC/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence.md) (the durable-execution URL returned this same page), [LC short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory.md), [libs/checkpoint-postgres](https://github.com/langchain-ai/langgraph/tree/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/checkpoint-postgres)
- [E] Durability modes are `Durability = "sync" | "async" | "exit"`. They control when checkpoint writes are persisted: before the next step, concurrently with it, or only at exit — [types.py L99](https://github.com/langchain-ai/langgraph/blob/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec/libs/langgraph/langgraph/types.py#L99)
- [E] A checkpoint-conformance test package exists (0.0.2) — libs/checkpoint-conformance

**Control and human-in-the-loop**
- [E] Calling `interrupt(value)` inside a node saves the state through the checkpointer and "waits indefinitely". The run resumes with `Command(resume=...)`, and the resume value becomes the return value of `interrupt()`. This requires a checkpointer and a `thread_id`. "Reusing it resumes the same checkpoint" — [LC/oss/python/langgraph/interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts.md)
- [E] At the agent layer, approvals use `HumanInTheLoopMiddleware` and `InterruptOnConfig`, imported from `langchain.agents.middleware` by deepagents. deepagents also builds `interrupt_on` from `FilesystemPermission` rules — [deepagents/graph.py](https://github.com/langchain-ai/deepagents/blob/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/deepagents/graph.py)
- [S] Guardrails have no dedicated LangGraph primitive. They are implemented as middleware or nodes, for example deepagents' `ModelRefusalMiddleware` and `_ToolExclusionMiddleware` — deepagents/graph.py imports. [Inf for "no dedicated primitive"; I did not check LangChain's guardrails docs]

**Context**
- [E] Summarization is done by LangChain's `SummarizationMiddleware`. deepagents builds its own via `create_summarization_middleware` and adds message eviction, overflow clipping, blob offload and prompt-caching middleware — [LC short-term-memory §Summarize messages](https://docs.langchain.com/oss/python/langchain/short-term-memory.md), [deepagents/middleware/](https://github.com/langchain-ai/deepagents/tree/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/deepagents/middleware)

**Deep Agents harness**
- [E] Deep Agents describes itself as "the agent harness for complex, multi-step work. It adds planning, a virtual filesystem for context, subagent spawning, and long-term memory on top of LangChain and LangGraph". It is "the same core tool calling loop as other agent frameworks". It is offered both as Managed Deep Agents and as an open-source SDK — [LC/oss/python/deepagents/overview](https://docs.langchain.com/oss/python/deepagents/overview.md)
- [E] `create_deep_agent` assembles a middleware stack from `FilesystemMiddleware`, `SubAgentMiddleware`, `AsyncSubAgentMiddleware`, `SkillsMiddleware`, `MemoryMiddleware`, `PatchToolCallsMiddleware`, summarization, `HumanInTheLoopMiddleware`, `ModelRefusalMiddleware` and others. Custom middleware is merged by name. The pluggable backends are state, store, filesystem, local_shell, sandbox, composite, langsmith and context_hub — [deepagents/graph.py](https://github.com/langchain-ai/deepagents/blob/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/deepagents/graph.py), [backends/](https://github.com/langchain-ai/deepagents/tree/f2a6e02dc8e2dcb05885c5133b94102ccc79b794/libs/deepagents/deepagents/backends)

**Deployment, tracing and multi-agent**
- [E] Agent Server is part of LangSmith Deployment. It is built around assistants, threads, runs and cron jobs. Deploying it means deploying the graphs, "a database for persistence, and a task queue". "The server automatically injects the checkpointer and memory store … Do not configure these in your graph code". Persistence uses PostgreSQL by default — [LC/langsmith/agent-server](https://docs.langchain.com/langsmith/agent-server.md)
- [E] Tracing and evaluation go through LangSmith: "Trace each step of this loop, debug tool calls, and evaluate agent outputs with LangSmith" — [LC agents](https://docs.langchain.com/oss/python/langchain/agents.md)
- [S] Multi-agent support comes from several pieces. Graph primitives (`Send`, `Command`, subgraphs) handle routing and fan-out. Deep Agents adds subagents (sync and async) with isolated context — types.py; deepagents overview ("Delegate to general or specialized subagents running in isolated context windows").

### Inferences
- [Inf] LangGraph alone covers Memory/state, durability and part of Control, namely interrupts. Loop, Tools and Context only appear in `create_agent` and Deep Agents. That makes LangGraph a runtime rather than a harness, which is how LangChain itself presents it: the agents doc defines "harness" as "the prompt, the tools, and any middleware".
- [Inf] With middleware, one mechanism is used for several responsibilities. Context (summarization), Control (HITL, refusal), Tools (filesystem) and Multi-agent (subagents) are all middleware, so the boundary is set by the framework's own conventions rather than by its types.

### Gaps
- [U] I did not read the `create_agent` source or the full middleware hook list. `wrap_model_call` and `wrap_tool_call` could not be confirmed from what I fetched. The exact deprecation status and version of `create_react_agent` were not confirmed beyond the deprecated helpers.
- [U] I did not verify the langgraph-supervisor and langgraph-swarm packages.

## Q4. Matrix of responsibility against SDK, and which responsibilities map cleanly

### Takeaway
Loop, Tools and Control map cleanly onto all three systems. Context and Memory blur together in all three: compaction sessions in OpenAI, CLAUDE.md in Claude, checkpointers versus summarization middleware in LangChain. Durable execution, tracing, evaluation and multi-agent need their own rows. Durable execution is external in OpenAI, absent in Claude (resume only) and native in LangGraph. Tracing is a cross-cutting sink in all three. Evaluation is absent from all three SDKs and is supplied by platforms such as the OpenAI dashboard [U] and LangSmith.

### Cited Findings (matrix; each cell cites the sources from Q1–Q3)

| Responsibility | OpenAI Agents SDK 0.24.0 | Claude Agent SDK 0.2.180 (CLI 2.1.318+) | LangGraph 1.2.20 + LangChain create_agent + deepagents 0.7.35 |
|---|---|---|---|
| **Loop**: run, turns, termination | `Runner.run/run_sync/run_streamed`; `NextStep*` classification; final = typed text with no tool calls; `tool_use_behavior` [E] | Runs in the CLI. `query()` / `ClaudeSDKClient`; ends with `ResultMessage` with a subtype [E] | Pregel supersteps in LangGraph. The agent loop itself lives in `create_agent` [E] |
| Max turns | `max_turns`, default 10, raises `MaxTurnsExceeded`; `error_handlers` [E] | `max_turns` (no default), `max_budget_usd`, `task_budget` → `error_max_*` [E] | `recursion_limit`, default 10007 (deepagents uses 9999) [E] |
| Streaming | `run_streamed().stream_events()` [E] | Async message iterator; `include_partial_messages` [E] | 7 `StreamMode`s [E] |
| **Tools**: function | `FunctionTool` / `@function_tool` [E] | `@tool` with `create_sdk_mcp_server` (in-process MCP) [E] | LangChain tools / `ToolNode` [Inf: not opened] |
| Hosted | Web/file search, code interpreter, image gen, hosted MCP, `ToolSearchTool` [E] | None hosted; built-ins run locally: Read/Edit/Write/Glob/Grep/Bash/Web*/ToolSearch/Agent/Skill [E] | None in the core [Inf] |
| MCP | Hosted plus stdio/SSE/HTTP plus manager, filtering, approvals [E] | stdio/SSE/HTTP/SDK `McpServerConfig` [E] | Via langchain-mcp-adapters [U: not checked] |
| Sandbox / code exec | Sandbox Agents (`Manifest`, `SandboxRunConfig`, 6+ providers), `ShellTool`, `ApplyPatchTool` [E] | `SandboxSettings` for Bash file/network isolation [E] | deepagents `sandbox` / `local_shell` backends; REPL [E] |
| **Context**: instructions | `instructions` (static, dynamic, prompt), `call_model_input_filter` [E] | `system_prompt` preset + `append` + CLAUDE.md/rules via `setting_sources` [E] | `system_prompt=` + middleware [E] |
| Compaction | `OpenAIResponsesCompactionSession`; `nest_handoff_history` (beta); `ToolOutputTrimmer` [E] | Automatic, `compact_boundary`, `PreCompact` hook, `/compact` [E] | `SummarizationMiddleware`; deepagents eviction/offload [E] |
| Sub-agent context | Handoff `input_filter` / history mapper; `as_tool` gets a fresh input [E/Inf] | Fresh context (forks excepted), prompt-only handoff, final message returned [E] | Subagents in "isolated context windows" (deepagents) [E] |
| **Memory**: sessions / short-term | `Session` protocol with about 10 backends [E] | JSONL transcripts; resume/continue/fork; `SessionStore` [E] | Checkpointers keyed by `thread_id` [E] |
| Run-state persistence | `RunState` serialize/resume [E] | Transcript resume; file checkpointing for the filesystem [E] | Checkpoint on every superstep; `Durability` modes [E] |
| Long-term store | Sandbox `Memory()` capability (files) [E] | CLAUDE.md + auto memory; `AgentDefinition.memory` [E] | `BaseStore` (`InMemoryStore`, Postgres); deepagents `MemoryMiddleware` [E] |
| **Control**: guardrails | Input/output/tool guardrails with tripwires; input guardrails run in parallel by default [E] | No guardrail type; done through hooks and permission rules [S] | No primitive; done through middleware [S/Inf] |
| Permissions | `needs_approval` per tool; MCP `require_approval` [E] | 6 modes plus a 6-step evaluation (hooks, deny, ask, mode, allow, `can_use_tool`) [E] | deepagents `FilesystemPermission` → `interrupt_on` [E] |
| Hooks | `RunHooks`, `AgentHooks` (observe) [E] | 10 hook events that can block or modify [E] | Middleware hooks (`before_model`, `after_model` …) [E] |
| HITL / interrupts | `interruptions` → `RunState.approve/reject` → re-run [E] | `can_use_tool` callback, `AskUserQuestion` (process stays alive) [E] | `interrupt()` + `Command(resume=)`, durable, waits indefinitely [E] |
| **Durable execution** | Not built in. Temporal, Dapr, Restate and DBOS integrations [E] | Not built in. Session persistence and resume [S] | Native: checkpointers, Durability, RetryPolicy; Agent Server task queue [E] |
| **Tracing** | Built-in traces/spans → OpenAI; custom processors [E] | OTel exported by the CLI (traces, metrics, logs) [E] | LangSmith [E] |
| **Multi-agent** | Handoffs; agents-as-tools; experimental hosted multi-agent [E] | `agents` / `AgentDefinition`, `.claude/agents`, forks, background subagents, `SendMessage` [E] | Graph composition, `Send`/`Command`; deepagents sync and async subagents [E/S] |
| **Extensibility** | Model providers, session backends, sandbox providers, trace processors, filters, hooks [E] | MCP, hooks, plugins, skills, settings sources, custom CLI path [E] | Custom nodes/graphs, middleware, checkpointer/store/backends [E] |
| **Deployment** | Library (+ realtime/voice) [E] | Library that runs a subprocess; Managed Agents is the hosted option [E] | Agent Server (assistants/threads/runs/cron, Postgres, queue) [E] |
| **Evaluation** | Not in the SDK [Inf] | Not in the SDK [Inf] | LangSmith (platform, not the library) [E] |

### Inferences
- [S] **Clean mappings.** Loop maps cleanly in all three. Tools maps cleanly, though "hosted versus local" is a real axis only for OpenAI. Control maps cleanly but has sub-parts: guardrails versus permissions versus hooks versus HITL.
- [S] **Combined responsibilities.** Context and Memory are combined in OpenAI (the compaction session is a Session), in Claude (CLAUDE.md is both instruction and memory) and in deepagents (the filesystem is both context offload and memory). Control and Memory are combined in LangGraph and OpenAI because HITL relies on persisted state (checkpoint or `RunState`). Durability and Memory are one mechanism in LangGraph, the checkpointer.
- [S] **Split across modules.** Claude separates mechanism (CLI) from configuration (SDK). LangGraph spreads the harness across runtime (langgraph), harness (langchain `create_agent`), opinionated harness (deepagents) and platform (Agent Server or LangSmith).
- [P] **What does not fit the five categories.** (a) Durable execution should be its own axis with the values native, integration or absent. (b) Observability should be a cross-cutting sink rather than a responsibility of the loop. (c) Evaluation sits outside all three SDKs and belongs at the platform layer. (d) Multi-agent and Deployment are better as separate dimensions than folded into Loop or Context. (e) Budget and cost limits (`max_budget_usd`, `task_budget`) are a Control-on-Loop concern, and only Claude has them first-class.

### Gaps
- Evaluation tooling on OpenAI's side (dashboard evals) was not checked [U].
- I only checked the Python implementations. The TypeScript SDKs may differ, and Claude's docs already show TypeScript-only features such as `permission_policy: always_ask`.
