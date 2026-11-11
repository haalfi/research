# Enterprise governance and operations controls of agent harnesses (controls x systems)

Method note: All docs were retrieved 2026-11-11 as live pages. GitHub Docs came through the docs.github.com article-body API (markdown). Claude Code docs came from code.claude.com `.md` pages and Codex docs from developers.openai.com `.md` pages, which now redirect to learn.chatgpt.com content. OpenCode pages are HTML from opencode.ai/docs (V2 "latest", plus the V1 Enterprise page). None of these pages shows a visible "last updated" date, so "doc date" below means the retrieval date (2026-11-11). Where a page names a client version, that version is quoted.
Labels:
- **[E] Established**: read in the full text of a primary doc.
- **[S] Synthesized**: combined from several [E] facts.
- **[P] Proposed**: a recommendation.
- **[Inference]**: my reasoning, not stated in a source.
- **[Unreachable]**: the source could not be fetched.

## 1. Policy hierarchy, inheritance/override, and managed-settings delivery

### Takeaway
All four systems now have an admin-enforced "managed settings" layer that sits above user and project settings. GitHub Copilot has adopted a `managed-settings.json` model that closely mirrors Claude Code's, with the same key names: `permissions.deny/ask/allow`, `disableBypassPermissionsMode`, `sandbox` and `allowedMcpServers`. Copilot's distinctive advantage is its native enterprise → organization → repository policy tree on GitHub, plus per-enterprise-team overrides. Claude Code (Enterprise) and Codex (Agent Security) also offer per-group configurations. OpenCode has machine/MDM-managed config and Console workspace policies.

### Cited Findings
**GitHub Copilot (Business/Enterprise)**
- [E] Policies are set at the enterprise level first. For most policies, enterprise admins can enable, disable, or "let organizations decide". A separate "Policies for enterprise-assigned users" setting covers users licensed directly by the enterprise. — [Copilot policies for enterprises and organizations](https://docs.github.com/en/copilot/concepts/enterprise/policies)
- [E] Conflict rule: if a user is licensed by several orgs in one enterprise, the **least restrictive** policy usually applies. Across enterprises, the **most restrictive** policy almost always applies. — [same](https://docs.github.com/en/copilot/concepts/enterprise/policies)
- [E] Policies apply only to users licensed by that enterprise/org. A few policies govern everyone, e.g. "Block Copilot cloud agent in all repositories owned by ENTERPRISE" and "Block Copilot code review in all enterprise repositories". Those blocks also cover users with personal or other-enterprise licenses. — [Blocking agentic features](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/block-agentic-features)
- [E] Policy admins are enterprise owners or holders of the "Manage enterprise AI controls" custom role. At org level, admins are org owners or holders of granular custom permissions. The audit log is the recommended tool for detecting policy drift. — [Copilot policies](https://docs.github.com/en/copilot/concepts/enterprise/policies)
- [E] Enterprise-managed settings are a `copilot/managed-settings.json` file in a `.github-private` repo ("server-managed"). Supported clients: Copilot CLI, VS Code, the GitHub Copilot app, Copilot in the cloud, and JetBrains. Clients pick up changes within about 1 hour. GitHub validates the file and shows errors under AI controls > Agents. — [Getting started with enterprise-managed settings](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/get-started)
- [E] Delivery methods are server-managed (GitHub repo), MDM, and file-based:
  - MDM: Windows `HKLM\SOFTWARE\Policies\GitHubCopilot` or the macOS `com.github.copilot` domain, checked hourly. There is no native MDM on Linux.
  - File-based: `/etc/github-copilot/managed-settings.json` and the macOS/Windows equivalents. Copilot CLI requires the file to be root-owned and not writable by others.
  - Precedence is MDM > server-managed > file > user. `sandbox` and `permissions.deny/ask/allow` compose in the most restrictive direction across methods.
  - `forceRemoteSettingsRefresh` can require fresh server settings at startup.
  - If a server fetch fails with no cache, the server-managed policy is unavailable for that CLI session.
  — [Choosing how to deploy enterprise-managed settings](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/deploy-managed-settings)
- [E] Per-team overrides work only with server-managed delivery:
  - Mark a key `{ "overridable": VALUE }`, then map enterprise teams to files under `copilot/teams/` via `team-mappings.json`.
  - Overridable keys: `model`, `autoTier`, `fusionTier`, `permissions.*` (deny/ask/allow, disableBypassPermissionsMode), `allowedMcpServers`, `deniedMcpServers`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, `sandbox`. `enabledPlugins` is additive.
  - For users in several teams, team files combine using the **least restrictive** value per key, beneath the enterprise settings.
  — [Overriding enterprise-managed settings for enterprise teams](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/override-settings-for-teams)
- [E] The managed-settings reference lists these keys: `features.computerUse`, `enabledPlugins`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, `model`, `fusionTier`, `autoTier`, `forceRemoteSettingsRefresh`, `permissions` (deny/ask/allow, disableBypassPermissionsMode, disableAssistedPermissionsMode, defaultMode), `telemetry` (capture controls), `remoteControl`, `allowedMcpServers`, `deniedMcpServers`, and `sandbox` (learningMode, userPolicy.filesystem/network/seatbelt). — [Enterprise managed settings reference](https://docs.github.com/en/copilot/reference/enterprise-administrators/enterprise-managed-settings) (headings read; body not fully read)

**Claude Code (Team/Enterprise)**
- [E] Precedence: managed settings > command line `--settings` > project local (`.claude/settings.local.json`) > shared project (`.claude/settings.json`) > user (`~/.claude/settings.json`). — [Settings files and precedence](https://code.claude.com/docs/en/settings)
  - Nothing overrides a managed key, and `--model` picks only from allowed models.
  - Some security keys honor a *stricter* value from a lower scope, e.g. `permissions.blockReadsOutsideWorkingDirectories` (v2.1.257+) and `maxEffortLevel` lower cap (v2.1.267+).
- [E] Managed delivery options:
  - server-managed (claude.ai admin console, or a self-hosted Claude apps gateway), fetched at startup and polled hourly;
  - MDM/OS policy (macOS `com.anthropic.claudecode`, Windows `HKLM\SOFTWARE\Policies\ClaudeCode`), checked every 30 min;
  - file-based (`/etc/claude-code/managed-settings.json`, plus a `managed-settings.d/*.json` drop-in directory merged alphabetically so several teams can own parts of one policy, plus `managed-mcp.json`);
  - HKCU registry (user-writable, used only when no admin document is present).
  - By default the first source with a policy key wins. `managedSourcesBehavior: "merge"` (v2.1.242+) composes sources: lists union, locks take the strictest value.
  — [Managed settings](https://code.claude.com/docs/en/managed-settings)
- [E] Server-managed settings need a Claude for Teams or Enterprise plan, the Owner/Primary Owner role, and network access to `api.anthropic.com`. All settings.json keys are supported except a short OS-only list. Hooks delivered this way trigger a user security-approval dialog. `/status` and `claude doctor` (v2.1.248+) show the delivery state. — [Configure server-managed settings](https://code.claude.com/docs/en/server-managed-settings)
- [E] Per-group configurations (Enterprise only):
  - Each group is SCIM-synced or a custom admin-console group. A member gets at most one config: the highest-ranked among their groups, or else a catch-all.
  - Configurations **don't merge** with each other or with the org-wide config.
  - Admins can check any member's effective settings in the console.
  - Not available yet for HIPAA-enabled orgs.
  — [same](https://code.claude.com/docs/en/server-managed-settings)
- [E] Endpoint (MDM) settings give stronger guarantees on managed devices but don't reach Anthropic-hosted cloud sessions. Only server-managed settings reach cloud sessions. — [same](https://code.claude.com/docs/en/server-managed-settings); [Settings](https://code.claude.com/docs/en/settings)

**OpenAI Codex (ChatGPT Business/Enterprise)**
- [E] Codex governance is split into separate boundaries: workspace access (seats, roles, RBAC, groups); local runtime policy (desktop app, CLI, IDE extension); Codex cloud; Platform API (API-key org/project); plugins/connectors; and permissions in connected systems. — [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup)
- [E] Managed configuration has two layers:
  - **Requirements** (`requirements.toml`, admin-enforced, users can't override): approval policy, approvals reviewer, Auto-review policy, sandbox mode/permission profiles, web search mode, managed hooks, which MCP servers users can enable, plugin marketplace sources, and `[features]` pins.
  - **Defaults** (`config.toml`, users can override).
  - Legacy `managed_config.toml` only sets launch defaults.
  — [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- [E] The Admin Console **Agent security** page has a **Workspace default** and **Overrides** for specific users, groups, or roles. A policy has a Global baseline (orchestrator controls such as approvals and web search) plus Local and Codex Cloud environment overrides for execution controls (sandbox, filesystem, managed networking). Environment overrides cannot override orchestrator controls. A policy API with Terraform workflows manages Global settings. — [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration); [Agent Security](https://developers.openai.com/codex/enterprise/agent-security)
- [E] For local execution, MDM and legacy managed-device requirements rank above Agent Security. Cloud environments don't inherit local device policy, MDM settings, or local network access. — [Configuration reference](https://developers.openai.com/codex/config-reference); [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup)
- [E] Repository configuration (`.codex`/`.agents`) supplies defaults, rules, and skills. It cannot grant workspace, model, Platform API, or connected-system access. — [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup)

**OpenCode (open source, plus Console)**
- [E] Config precedence: project `opencode.json(c)` files merge from the repo root down to the closest file. Project config overrides global (user) config. The system (managed, machine-wide) config overrides all of them. On macOS, MDM-deployed managed preferences in the `ai.opencode.managed` domain have the highest precedence, so users and projects cannot override them. — [OpenCode Config](https://opencode.ai/docs/config/)
- [E] `policies` statements (actions `provider.use`, `tool.use`, `integration.connect/use`, `mcp.use`, `skill.use`, `plugin.use`, `websearch.use`; effect allow/deny):
  - Policies "only ever tighten" what permissions and providers allow, and never prompt.
  - When several statements match, the last one wins (no specificity rule).
  - Statements that fail validation are **dropped with a warning** and the rest still apply.
  - Console-managed policy exists.
  — [OpenCode Policies](https://opencode.ai/docs/policies/)
- [E] OpenCode Console offers workspaces for teams, provider connections through a Console gateway, usage tracking and budget controls, and team-wide policies. Those policies are delivered as statements that outrank members' user and project config. — [OpenCode Console](https://opencode.ai/docs/console/)

### Inferences
- [Inference] Copilot's client-governance key set (`permissions.*`, `sandbox`, `allowedMcpServers`, `enabledPlugins`, `strictKnownMarketplaces`, `disableBypassPermissionsMode`) is close to Claude Code's managed-settings schema. On *client* policy the two are now at near feature parity. Copilot's lead is the surrounding GitHub org/repo/team structure and audit trail.
- [Inference] Merge semantics differ in ways that matter at scale:
  - Copilot team overrides merge to the *least* restrictive value across a user's teams.
  - Claude Code group configs don't merge at all (first-ranked wins).
  - Codex uses ordered policy assignments.
  - OpenCode uses last-match-wins.
  Each design needs different hygiene. Copilot multi-team users can be loosened by accident. Claude Code admins must duplicate every baseline restriction into every group config.
- [Inference] OpenCode silently drops invalid statements, while Copilot treats a malformed MCP allowlist as an empty list. Copilot fails closed and OpenCode partially fails open.

### Gaps
- Copilot "Supported surfaces for policies" and the policy-conflicts reference were not read in full, so per-surface coverage is not fully verified.
- OpenCode V2 has no "Enterprise" page under docs/enterprise (it returned the V1 page). Whether Console policy can target sub-groups/teams was not confirmed.

## 2. Model allowlists, MCP allowlists/registries, tool/permission policies, sandbox/network

### Takeaway
Copilot, Claude Code and Codex all have enforceable model, MCP and permission controls. Copilot and Claude Code use near-identical MCP allowlist semantics (match by name, URL or command, deny wins). Claude Code additionally offers an *exclusive* `managed-mcp.json`. Copilot's cloud agent firewall has the richest built-in org → repo network delegation. OpenCode enforces provider/MCP/tool policies, but I found no built-in OS sandbox.

### Cited Findings
**GitHub Copilot**
- [E] Models: users can only access models enabled at enterprise level. Enterprise/org owners can add custom models via BYOK (public preview) from Anthropic, AWS Bedrock, Google AI Studio, Microsoft Foundry, OpenAI, OpenAI-compatible providers and xAI, and can enable them for all orgs or per org. Separately, user-local BYOK keys in Copilot CLI are **not** controlled by enterprise policy. — [Enabling custom models](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/enable-custom-models); [Administering Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise)
- [E] A "Restrict Copilot to FedRAMP models" policy (GHE.com US data residency only) limits users to FedRAMP Moderate models. It adds 10% to AI-credit consumption. — [FedRAMP-compliant models](https://docs.github.com/en/copilot/concepts/enterprise/fedramp-models)
- [E] MCP: the "MCP servers in Copilot" policy turns MCP on/off.
  - The recommended (GA) allowlist is `allowedMcpServers`/`deniedMcpServers` in managed settings. Matching is by name, URL or stdio command. Deny wins.
  - Built-in default servers are always allowed. Unresolved variables block a server.
  - With multiple sources, a server must match the allowlist at every layer. A malformed list blocks all non-built-in servers. A retrieval error retains the previous policy.
  - These lists don't apply to MCP servers defined in repository custom agent profiles; use the firewall instead.
  — [Configuring an MCP server allowlist](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist)
- [E] Custom MCP registry restriction is public preview, "not prioritized for development". It matches by name/ID only, and users can bypass it by editing config files. — [MCP server usage in your company](https://docs.github.com/en/copilot/concepts/enterprise/mcp-management); [Configure an MCP registry](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry)
- [E] Cloud agent / code review firewall:
  - Organization settings: Enable firewall (Enabled / Disabled / Let repositories decide), Recommended allowlist (same three options), "Allow repository custom rules", and an org custom allowlist that repos can't delete.
  - Rules are domains (including subdomains) or URL path prefixes.
  - Limitations: it applies only to processes the agent starts via Bash (not MCP server processes or setup steps), only inside the runner/sandbox, and "sophisticated attacks may bypass the firewall".
  — [Customizing or disabling the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall)
- [E] Cloud agent guardrails: it pushes only to one `copilot/` branch, cannot run `git push` directly, opens draft PRs that a human must merge, and doesn't trigger Actions workflows until approved. The requesting user cannot approve the PR. — [Cloud agent risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)
- [E] Subscription-based network routing lets you allow `*.business.githubcopilot.com` / `*.enterprise.githubcopilot.com` and block `*.individual.githubcopilot.com` to stop personal Copilot plans on corporate networks. — [Managing Copilot access to your network](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-access/manage-network-access)

**Claude Code**
- [E] MCP control patterns:
  - Disable MCP: `managed-mcp.json` with an empty map.
  - Fixed deployment: `managed-mcp.json` (exclusive; file-based only, not via server-managed).
  - Approved catalog: `allowedMcpServers` + `allowManagedMcpServersOnly: true`.
  - Soft allowlist: `allowedMcpServers` without the lock, which users can broaden.
  - Denylist only: `deniedMcpServers`.
  - `managedMcpServers` (v2.1.259+) provides servers through managed settings.
  — [Control MCP server access](https://code.claude.com/docs/en/managed-mcp)
- [E] Models: `availableModels` restricts selection. `enforceAvailableModels` applies the allowlist to the default model. Organization model restrictions also exist. — [Model configuration](https://code.claude.com/docs/en/model-config)
- [E] Permissions:
  - Managed `permissions.deny` plus `disableBypassPermissionsMode` / `disableAutoMode: "disable"`.
  - `allowManagedPermissionRulesOnly: true` restricts rules to managed ones.
  - `Bash(curl *)` deny rules match the command text only. Docs recommend the sandbox for network enforcement.
  - PreToolUse hook decisions don't bypass deny/ask rules.
  — [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings); [Permissions](https://code.claude.com/docs/en/permissions)
- [E] The OS-enforced Bash sandbox (Seatbelt on macOS; bubblewrap + socat on Linux/WSL2):
  - Network goes via a local proxy against `network.allowedDomains` (empty by default).
  - `sandbox.failIfUnavailable` makes startup fail if no sandbox is available. By default Claude Code runs unsandboxed when the sandbox is unavailable.
  - Built-in Read/Edit/WebFetch tools follow permission rules, not the sandbox.
  — [Sandboxing](https://code.claude.com/docs/en/sandboxing)

**Codex**
- [E] `requirements.toml` constrains approval policy, sandbox modes/permission profiles (e.g. `allowed_permission_profiles` omitting `:danger-full-access`), web search modes (`allowed_web_search_modes = ["cached"]` prevents live search even in danger-full-access), managed hooks, the MCP servers users can enable, plugin marketplaces, feature pins (e.g. `computer_use = false`), and command rules. Network use controls are "not a workspace-wide internet switch". — [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration); [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup)
- [E] Codex cloud: agent internet access is off by default during the agent phase (setup scripts have internet). It is configured per environment with a domain allowlist (presets None / Common dependencies / All) and optional GET/HEAD/OPTIONS-only. — [Codex Cloud (Legacy): internet access](https://developers.openai.com/codex/cloud/internet-access)
- [E] `model_provider`/`model_providers` are not supported in managed Work Cloud local-access requirements. — [Configuration reference](https://developers.openai.com/codex/config-reference)

**OpenCode**
- [E] Permission rules are `{action, resource, effect}`, with actions such as shell, read, edit and subagent and effects allow/ask/deny. If no rule matches, OpenCode asks. Any deny denies, otherwise any ask asks. — [OpenCode Permissions](https://opencode.ai/docs/permissions/)
- [E] Provider policy: `provider.use` deny removes a provider from the catalog and model selection. This acts as a model/provider allowlist. — [OpenCode Policies](https://opencode.ai/docs/policies/)

### Inferences
- [Inference] The "Copilot MCP registry policy" named in the brief is now explicitly the weaker, deprecated-in-practice mechanism. Copilot's GA MCP control is the same allowlist pattern Claude Code uses.
- [Inference] A Copilot gap: user-local BYOK models in the CLI bypass enterprise model policy, and custom-agent-profile MCP servers bypass the MCP allowlist. Claude Code's `availableModels`/`enforceAvailableModels` covers local model selection, but third-party base-URL routing affects server-managed fetch (see section 8).

### Gaps
- No OS sandbox found for OpenCode in the pages read. Its network page covers only proxies and certificates. Treat as **absent unless shown otherwise** [Inference].
- The Codex `requirements.toml` MCP identity fields (name/URL/command matching) were not read in detail.

## 3. Identity / SSO / SCIM / seats

### Takeaway
Copilot inherits GitHub Enterprise Cloud identity (SAML/OIDC, SCIM, Enterprise Managed Users) and assigns seats to users, enterprise teams or orgs. Claude Enterprise and ChatGPT Enterprise both offer SSO and SCIM, with SSO also on Teams/Business. OpenCode's SSO comes via its Enterprise offering or your own gateway.

### Cited Findings
- [E] GHEC: SCIM provisioning plus SAML or OIDC. GHE.com (data residency) requires Enterprise Managed Users. — [About GHEC with data residency](https://docs.github.com/en/enterprise-cloud@latest/admin/data-residency/about-github-enterprise-cloud-with-data-residency)
- [E] Copilot seats can be assigned to individuals, enterprise teams or whole orgs. A SCIM/team-sync-driven seat event is attributed to whoever granted the team access. — [Seat assignment](https://docs.github.com/en/copilot/reference/copilot-billing/seat-assignment); [Reviewing audit logs](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/review-audit-logs)
- [E] Claude for Teams includes SSO, admin tools and server-managed settings. Claude for Enterprise adds domain capture, role-based permissions and the compliance API. Console roles include "Claude Code" (can only create Claude Code keys) and "Developer". `forceLoginOrgUUID` / `forceLoginMethod` in managed settings restrict which org can be logged into. — [Identity and access management](https://code.claude.com/docs/en/iam)
- [E] Claude apps gateway (self-hosted):
  - Supports OIDC IdPs (Okta, Entra ID, Google Workspace, Keycloak, Dex, PingFederate); SAML and LDAP aren't supported.
  - IdP groups map to model allowlists, managed-settings policies and upstreams.
  - Short-lived tokens mean a deprovisioned user loses access within the session lifetime (default 1 hour).
  - The gateway is an alternative to claude.ai login and doesn't fetch claude.ai server-managed settings.
  — [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway)
- [E] ChatGPT Business includes SAML SSO. Enterprise adds SCIM, EKM and more. — [Codex pricing](https://developers.openai.com/codex/pricing). Codex access follows ChatGPT workspace membership, seats, groups and RBAC; the rollout guide links group provisioning and user lifecycle docs. — [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup); [Codex auth](https://developers.openai.com/codex/auth)
- [E] The OpenCode Enterprise (V1) page lists "Central Config", "SSO integration", "Internal AI gateway" and "Self-hosting" sections, and per-seat pricing. If you use your own LLM gateway, OpenCode doesn't charge for tokens. — [OpenCode Enterprise](https://opencode.ai/docs/enterprise/)

### Gaps
- The body text of the OpenCode Enterprise SSO section was not captured (only headings). Whether OpenCode supports SCIM is unknown.
- Help Center pages (help.openai.com, support.claude.com) for SCIM details were not fetched.

## 4. Audit logs

### Takeaway
Copilot has the most mature audit trail: GitHub enterprise audit log with Copilot and agent events, 180-day retention, SIEM streaming, and (preview) streaming of agent session and Copilot API usage records including request/response bodies. However, it explicitly does **not** log local client session data. Claude (compliance API on Enterprise; OTel for local) and Codex (Compliance API with `codex_log`; OTel for local) depend on API exports plus client telemetry. OpenCode has no vendor audit log.

### Cited Findings
- [E] Copilot audit log:
  - It records plan/settings/policy changes, license changes, and agent activity on the GitHub website.
  - It does **not** include client session data such as local prompts. Companies use custom hooks (e.g. Copilot CLI hooks) to send events to their own logging.
  - It retains 180 days, with streaming to a SIEM recommended.
  — [Reviewing audit logs for Copilot](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/review-audit-logs)
- [E] Agentic events can be filtered with `actor:Copilot` and carry `actor_is_agent`, `agent_session_id` and `user` (the initiator). Public preview, for EMU and data-residency enterprises: streamed Copilot API usage records contain `user_id`, `endpoint`, and request/response `body` (truncated at 1 MB). — [Audit log events for agents](https://docs.github.com/en/copilot/reference/enterprise-administrators/agentic-audit-log-events); [Monitoring agentic activity](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/monitor-agentic-activity)
- [E] Audit log streaming: a paused stream keeps a 7-day buffer. Output is compressed JSON. A health check runs every 24h, and a misconfigured stream must be fixed within 6 days. — [Streaming the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise)
- [E] Claude Code: cloud sessions run in isolated VMs, and "all operations in cloud sessions are logged for compliance and audit purposes". Enterprise adds the compliance API. Local sessions can be audited via managed hooks (example: a PostToolUse audit script) and OTel events. — [Security](https://code.claude.com/docs/en/security); [IAM](https://code.claude.com/docs/en/iam); [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings)
- [E] Claude apps gateway spend limits store durable spend and audit state in Postgres. The gateway sends no telemetry, audit logs or identity to Anthropic. — [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway)
- [E] Codex: the Compliance API covers audit and investigation. Work/local records appear under `conversation_message` and `codex_log`. Local execution emits separate OTel events. Admin-defined MCP hooks on the cloud orchestrator can audit tool events. Docs warn that "conversation visibility alone does not establish a complete record of local actions". — [Governance](https://developers.openai.com/codex/enterprise/governance); [Compliance API](https://developers.openai.com/codex/enterprise/compliance-api)

### Gaps
- Retention windows for the Anthropic compliance API and the OpenAI Compliance API were not stated in the pages read. Both defer to API references or Help Center pages that require authentication [Unreachable/not fetched].
- Whether Claude/Anthropic offers an admin-action audit log (settings changes) comparable to GitHub's was not verified in a full text.

## 5. Content exclusion, data residency, retention/ZDR, training

### Takeaway
Only Copilot has a named "content exclusion" feature with repo/org/enterprise scopes, and the docs say outright it is not a security boundary. Claude Code and Codex achieve the equivalent through managed deny rules and sandbox filesystem policy. On residency: GitHub offers GHE.com regions (EU, AU, US, JP); Claude routes via Bedrock, Vertex or Foundry, or at a 1.1x data-residency rate; Codex offers data/inference residency for eligible content. Claude documents standard 30-day commercial retention and ZDR for qualified Enterprise orgs.

### Cited Findings
- [E] Copilot content exclusion:
  - Configured by repo admins (their repos), org owners (their seat holders) and enterprise owners.
  - Covered agents in IDE/CLI/app block excluded files via Copilot tools and check file paths in commands, "but might not detect indirect file access".
  - Not a filesystem security boundary. Not guaranteed for third-party MCP servers or clients. Doesn't apply to symlinks or remote filesystems.
  - Copilot CLI honors exclusions.
  — [Content exclusion](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion); [Administering Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise)
- [E] GHE.com data residency regions are the EU (incl. Norway and Switzerland Azure regions), Australia, the US and Japan. Some Copilot features are unavailable on GHE.com. — [About GHEC with data residency](https://docs.github.com/en/enterprise-cloud@latest/admin/data-residency/about-github-enterprise-cloud-with-data-residency)
- [E] Claude commercial terms:
  - No training on Claude Code prompts or code unless the customer opts in (e.g. the Development Partner Program).
  - Standard 30-day retention.
  - ZDR is available to qualified Claude for Enterprise accounts, enabled per organization by the account team. It is not in the standard plan and applies only to Anthropic's direct platform; on Bedrock, Vertex or Foundry the provider's policy applies.
  - Local transcripts are kept 30 days by default (`cleanupPeriodDays`).
  - `/feedback` transcripts are retained 5 years.
  — [Data usage](https://code.claude.com/docs/en/data-usage); [Zero data retention](https://code.claude.com/docs/en/zero-data-retention)
- [E] Claude BAA coverage: the HIPAA configuration (Enterprise) or ZDR. Cloud sessions, Remote Control, and Claude Code routed via third-party clouds or a gateway are not covered under the HIPAA configuration. — [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- [E] Claude data-residency responses are billed at 1.1x. — [Costs](https://code.claude.com/docs/en/costs)
- [E] Codex/ChatGPT:
  - Business has "No training on your business data by default". — [Codex pricing](https://developers.openai.com/codex/pricing)
  - With an API key, usage follows the API organization's retention. — [Codex auth](https://developers.openai.com/codex/auth)
  - "Local computer access with Work Cloud does not provide strict zero data retention". Data/inference residency covers only eligible content/workloads/regions. EKM covers supported stored content. — [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup)
- [E] OpenCode "does not store your code or context data". Processing is local or direct to your provider. — [OpenCode Enterprise](https://opencode.ai/docs/enterprise/)

### Gaps
- **Copilot prompt/suggestion retention and training-use terms were not verified in full text this run.** The docs.github.com retention page path guessed returned 404, and no Trust Center page was fetched. The commonly cited "Business/Enterprise data not used for training" claim is [Unverified, from prior knowledge]. The writer should treat it as a gap.
- openai.com/enterprise-privacy returned **403 (site, Cloudflare)** [Unreachable]. OpenAI retention days and ZDR for Codex were not verified.

## 6. Cost controls

### Takeaway
Copilot is clearly strongest. It has hard-stop user-level budgets (universal, cost-center and individual, with expiry), cost-center, org and enterprise budgets, included-usage caps per cost center, and budget-request workflows. Claude Code relies on org usage settings, per-user spend reports, `modelPricing` and (self-hosted gateway) per-user/group/org spend caps. Codex shares ChatGPT workspace credit controls, which "don't set a universal Codex limit". OpenCode Console offers usage tracking and budgets.

### Cited Findings
- [E] Copilot budgets, user-level:
  - User-level budgets (ULBs) are always a hard stop. Types are universal, cost-center ULB (e.g. $20/user engineering vs $5/user marketing) and individual (overrides, optional expiry). The most specific wins.
  — [Budgets for usage-based billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/budgets)
- [E] Copilot budgets, group and enterprise level:
  - Cost-center, org and enterprise budgets cap metered charges. They hard-stop only if "Stop usage when budget limit is reached" is enabled, which is **off by default**.
  - Included-usage caps per cost center are 1,900 AI credits per Business license and 3,900 per Enterprise license.
  - Cost-center exclusion from the enterprise cap is available.
  - The rule is "lowest remaining headroom wins".
  - Users licensed by several orgs are billed to a random org each cycle, which makes org budgets unpredictable.
  — [same](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/budgets)
- [E] Copilot usage metrics: dashboards (usage, code generation, impact) and REST APIs/NDJSON exports with repository- and user-level detail. Data lands within two full UTC days. Org totals overlap and should not be summed. — [Copilot usage metrics](https://docs.github.com/en/copilot/concepts/billing-and-usage/copilot-usage-metrics/copilot-metrics)
- [E] Claude Code:
  - Average about $13 per developer per active day and $150–250 per month, with 90% of users below $30 per active day.
  - Admins can set `modelPricing` to show contracted rates.
  - Team/Enterprise members without billing access can request more usage from admins.
  - The Team/Enterprise analytics dashboard shows usage and contribution metrics with CSV export. The spend report lists per-user token usage and estimated spend. Per-user cost is also available via OTel.
  — [Costs](https://code.claude.com/docs/en/costs); [Analytics](https://code.claude.com/docs/en/analytics)
- [E] Claude apps gateway spend limits: an Admin API (`/v1/organizations/spend_limits`) sets daily, weekly or monthly caps per `user` (OIDC sub), `rbac_group` or `organization`, enforced live with 429 responses. Bedrock supports per-developer AWS cost attribution. — [Gateway spend limits](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)
- [E] Codex: workspace analytics, the Codex Analytics API (aggregated) and "ChatGPT usage limits and spend controls". Eligible Codex activity consumes workspace credits, and exhausted limits pause access. These controls "don't set a universal Codex limit or govern Platform API billing". — [Governance](https://developers.openai.com/codex/enterprise/governance)
- [E] OpenCode Console: "Usage tracking and budget controls". — [OpenCode Console](https://opencode.ai/docs/console/)

### Gaps
- Details of the Claude for Enterprise admin-console per-user spend caps (outside the gateway) were not read in full; that content lives in the Help Center.
- The granularity of Codex workspace credit limits (per user or group?) was not verified.

## 7. Telemetry / observability

### Takeaway
All three vendor harnesses support OpenTelemetry export that admins can enforce. Copilot adds fine-grained capture classes. Claude Code locks the OTLP destination when it is set in managed settings and ignores OTel variables in repo settings. Codex exposes `otel.*` config including prompt logging. Usage-metric APIs exist for Copilot (REST/NDJSON) and Codex (Analytics API). Claude offers a dashboard with CSV export plus OTel.

### Cited Findings
- [E] Copilot OTel:
  - Exports traces, metrics and events. By default no identity, prompts, responses, tool args/results or raw policy detail are included.
  - Admins enable capture classes independently via the managed-settings `telemetry` key: identity, prompts, responses, tool arguments, tool output, policy detail. All default to false.
  - Fine-grained classes are supported in Copilot CLI, the Copilot app and VS Code Agent Host. VS Code's local harness has only all-or-nothing capture.
  - Managed values override local settings and env vars.
  — [OpenTelemetry for agent monitoring](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)
- [E] Claude Code OTel:
  - Exports metrics, events/logs and beta traces, configurable in managed settings `env`.
  - When managed settings set the endpoint, protocol or headers, developer-set per-signal variables are removed (since v2.1.217).
  - Exporter selectors follow normal precedence unless also set in managed settings.
  - Repo `.claude/settings.json` cannot enable or redirect telemetry.
  — [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage)
- [E] Codex config keys include `otel.exporter`, `otel.trace_exporter`, `otel.metrics_exporter`, `otel.log_user_prompt`, `otel.log_agent_responses` and `otel.tool_result.max_bytes`. `analytics.enabled=false` disables the built-in Statsig exporter. — [Configuration reference](https://developers.openai.com/codex/config-reference)
- [E] OpenAI Agents SDK: tracing is on by default. It can be disabled via `OPENAI_AGENTS_DISABLE_TRACING=1` and is unavailable under ZDR. Custom trace processors can send traces elsewhere. — [Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/)

### Gaps
- OpenCode OTel support was not found in the pages read.

## 8. Deployment options and LLM gateway support

### Takeaway
Copilot is SaaS-only (github.com or GHE.com). It can route through enterprise BYOK keys (Bedrock, Foundry, OpenAI-compatible) but has no self-hosted or air-gapped harness. Claude Code has the broadest routes: Anthropic SaaS, Bedrock, Google Cloud Agent Platform/Vertex, Microsoft Foundry, any compatible LLM gateway, and a first-party self-hosted Claude apps gateway. Codex supports ChatGPT SaaS plus a gateway rollout and custom `model_providers`. OpenCode is provider-agnostic open source, self-hostable with any gateway.

### Cited Findings
- [E] Copilot custom models via enterprise BYOK cover Bedrock, Foundry, OpenAI-compatible and others (public preview). Data residency is via GHE.com. — [Enabling custom models](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/enable-custom-models); [Data residency](https://docs.github.com/en/enterprise-cloud@latest/admin/data-residency/about-github-enterprise-cloud-with-data-residency)
- [E] Claude Code team auth options: Teams/Enterprise, Console, Claude apps gateway, Amazon Bedrock, Google Cloud's Agent Platform and Microsoft Foundry. — [IAM](https://code.claude.com/docs/en/iam)
- [E] Any gateway with a supported API format works. Anthropic doesn't support routing Claude Code to non-Claude models. — [LLM gateway](https://code.claude.com/docs/en/llm-gateway)
- [E] Caveat: gateway sessions don't fetch claude.ai server-managed settings, so policy must come from the gateway's `managed` block. A custom `ANTHROPIC_BASE_URL` or third-party provider variable causes the server-managed fetch to be skipped. — [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway); [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings)
- [E] Codex: an enterprise "Roll out a gateway" path for local clients (with or without ChatGPT sign-in), and `model_providers.<id>.base_url` in config. — [Admin rollout guide](https://developers.openai.com/codex/enterprise/admin-setup); [Configuration reference](https://developers.openai.com/codex/config-reference)
- [E] OpenCode providers include Azure, Bedrock, Vertex, Ollama and "Gateways" (`baseURL` override, custom headers such as tenant). The Enterprise page describes keeping code and data in your infrastructure via central config, SSO and an internal AI gateway. — [OpenCode Providers](https://opencode.ai/docs/providers/); [OpenCode Enterprise](https://opencode.ai/docs/enterprise/)
- [E] SDK route: LangSmith (LangGraph Platform) has deployment pages for "Deploy to Cloud" and "Deploy to Self-hosted". Its admin API includes org roles/access policies, SSO settings, SCIM tokens, audit logs, usage limits, TTL settings and data planes. — [LangChain docs index (llms.txt)](https://docs.langchain.com/llms.txt) (endpoint list only; deployment page body 404 [Unreachable])

### Inferences
- [Inference] For air-gapped or sovereign needs, Copilot cannot run the harness off GitHub's cloud. Claude Code through Bedrock/Vertex/Foundry plus the self-hosted gateway, or OpenCode with a local model, are the viable routes. Fully air-gapped operation of Claude Code still needs a reachable model endpoint; it was not documented as an offline mode.
- [Inference] SDK-based harnesses (OpenAI Agents SDK, Claude Agent SDK, LangGraph) put every control in this matrix on the operator. The only built-ins are tracing (Agents SDK, on by default, disabled under ZDR) and platform admin features (LangSmith RBAC/SSO/SCIM/audit). The Claude Agent SDK inherits Claude Code's settings and MCP machinery, e.g. claude.ai connectors and managed MCP apply to Agent SDK sessions per [Claude Code MCP](https://code.claude.com/docs/en/mcp).

### Gaps
- The full text of the Claude Agent SDK governance specifics, OpenAI Agents SDK guardrails, and the LangGraph self-hosted / air-gapped modes was not read [partially Unreachable].

## 9. Scaling: how controls hold up as teams and use cases are added; hypothesis verdict

### Takeaway
The hypothesis "Copilot is stronger in enterprise policy and governance than Claude Code, Codex and OpenCode" is **partly supported**:
- **Copilot clearly leads** on cost controls, the admin-action audit log/SIEM streaming, org → repo delegation (firewall, content exclusion, policy tree), and seat management tied to GitHub teams.
- **It is at parity** with Claude Code (and roughly with Codex) on client policy (managed settings, MCP allowlists, permissions, sandbox, OTel), because Copilot adopted essentially the same managed-settings model.
- **It is weaker** on deployment flexibility (no cloud-provider or self-hosted harness routes), on local session audit (explicitly not logged), and in some enforcement gaps (local BYOK models, custom-agent MCP, firewall bypass caveats).
- OpenCode trails on vendor-managed governance but gives the operator full control.

### Verdict per control area [S]
| Control area | Verdict | Basis |
|---|---|---|
| Policy hierarchy / delegation | **Copilot stronger** (enterprise → org → repo, plus enterprise-team overrides). Claude Enterprise (group configs) and Codex (user/group/role overrides) are close on client policy. OpenCode is weakest (machine/MDM plus Console). | Sec. 1 |
| Managed settings delivery | **Parity, Copilot ≈ Claude Code** (server + MDM + file for both). Codex is comparable (cloud + MDM + system). OpenCode has system/MDM (macOS) + Console. | Sec. 1 |
| Model allowlist | **Parity.** Copilot has enterprise/org enablement and FedRAMP mode, but local BYOK escapes policy. Claude has `availableModels`/`enforceAvailableModels`. OpenCode has `provider.use` deny. | Sec. 2 |
| MCP allowlist / registry | **Parity, with Claude Code slightly stronger** (exclusive `managed-mcp.json`). Copilot's registry mode is weak; its allowlist doesn't cover custom agent profiles. | Sec. 2 |
| Tool / permission policy | **Parity** (Copilot `permissions.*` mirrors Claude Code; Codex `requirements.toml`; OpenCode rules + policies). | Sec. 2 |
| Sandbox / network | **Mixed.** Copilot leads on *cloud agent* firewall delegation. Claude Code and Codex lead on documented *local* OS sandboxes. OpenCode has none documented. | Sec. 2 |
| Identity / SSO / SCIM | **Parity among SaaS vendors** (GHEC/EMU; Claude Enterprise SCIM; ChatGPT Enterprise SCIM). Copilot benefits from existing GitHub identity. | Sec. 3 |
| Audit logs | **Copilot stronger** for admin and cloud-agent events (180d, streaming, agent fields). No vendor offers complete local session audit by default; all rely on hooks/OTel. | Sec. 4 |
| Content exclusion | **Copilot has the only named feature**, but it is self-described as not a security boundary. Equivalent deny rules exist in Claude Code and Codex. | Sec. 5 |
| Data residency / ZDR / training | **Not decidable for Copilot this run** (retention/training pages not verified). Claude documents ZDR and 30-day retention. Copilot offers GHE.com regions and FedRAMP models. | Sec. 5 |
| Cost controls | **Copilot clearly stronger** (multi-level hard-stop budgets, cost centers). | Sec. 6 |
| Telemetry / OTel | **Parity.** Copilot has the richer capture classes; Claude Code has stronger destination locking. | Sec. 7 |
| Deployment / gateways | **Claude Code and OpenCode stronger.** Copilot is SaaS only. | Sec. 8 |

### Cited Findings (scaling-relevant)
- [E] Copilot team overrides combine across multiple teams using the **least restrictive** value. Overrides work only with server-managed delivery; MDM and file delivery need separate device-group deployments. — [Override settings for teams](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/override-settings-for-teams)
- [E] Claude Code group configs don't merge. Each must restate every restriction, and multi-group members get only the top-ranked config. Not available yet for HIPAA orgs. — [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings)
- [E] Claude `managed-settings.d/` lets several teams own separate policy fragments merged in alphabetical order. — [Managed settings](https://code.claude.com/docs/en/managed-settings)
- [E] Copilot cost-center ULBs apply one per-user amount to all current and future members, "without creating thousands of individual budgets". The universal ULB list populates lazily on first use. — [Budgets](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/budgets)
- [E] Codex Agent Security uses ordered policy assignments with overrides by users, groups or roles, managed via a policy API/Terraform. — [Agent Security](https://developers.openai.com/codex/enterprise/agent-security)

### Inferences
- [P] For large multi-team estates:
  - Copilot: keep restrictive keys non-overridable and rely on enterprise-level denies, because least-restrictive team merging erodes them.
  - Claude Code: generate per-group configs from a template (policy-as-code) so baseline denies aren't dropped.
  - Codex: manage Agent Security via the policy API/Terraform.
  - OpenCode: validate policies in CI, since invalid statements are dropped.
- [Inference] The decisive differentiator is less the client policy (now converging) than the **surrounding platform**. GitHub's org/repo/team/cost-center objects give Copilot finer delegation and cost attribution. Anthropic and OpenAI rely on IdP groups and workspace groups.

### Gaps
- No independent (non-vendor) evaluations of enforcement robustness were collected. All findings are vendor documentation.
- Scale limits (max teams, max group configs, rate limits on policy APIs) were not found in any doc read.
