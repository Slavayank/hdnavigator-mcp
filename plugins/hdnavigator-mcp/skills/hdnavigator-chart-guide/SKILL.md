---
name: hdnavigator-chart-guide
description: Use when a user wants to create, retrieve, list, compare, or discuss Human Design charts through HDnavigator MCP.
---

# HDnavigator Chart Guide

Use the HDnavigator MCP tools whenever the user asks for a Human Design chart, bodygraph, saved
calculation, or interpretation based on HDnavigator data.

## After installation

When the plugin has just been installed (or the user asks how to start), say this once, in the user's
language:

> HDnavigator MCP is installed. Restart your agent so the tools load, then choose one way to sign in:
> **1. OAuth (recommended)** — use your harness's MCP sign-in: Codex `codex mcp login hdnavigator`,
> OpenCode `/mcps` → hdnavigator → sign in. If your agent opens an embedded browser without your
> HDnavigator session, copy the printed URL and open it in your own browser where you are logged in
> to https://hdnavigator.ru, and approve there.
> **2. Token** — get an `hdn_...` token at https://hdnavigator.ru (register and confirm your email)
> and paste it here once. I will save it in the environment and configure the connection.
> After that, say "Create my Human Design chart" or "Show my saved charts".

Do not ask for a token if OAuth sign-in is available and succeeds. Never repeat a token back to the
user. This greeting is about setup only — do not call any chart tool until the user asks for a chart.

## Authentication

The MCP server is `https://mcp.slavayank.com/mcp` for every harness. The `codex ...` and
`opencode ...` commands below are examples for those two clients only; any other MCP client should
be configured with the server URL and its own OAuth sign-in (or an Authorization header with an
`hdn_` token if the client cannot do OAuth). Choose the first available method and do not ask the
user for a token if one is already configured.

### 1. OAuth (preferred)

If the harness supports MCP OAuth, ask it to sign in (`codex mcp login hdnavigator` or
`opencode mcp auth hdnavigator`) and call the tools without any token. The client keeps the access
token in the Authorization header; the model never sees it.

If the harness opens an embedded browser without an active HDnavigator session, tell the user to open
the printed authorization URL in **their own browser**, where they are logged in to
`https://hdnavigator.ru`, and approve there. The loopback callback still works. If a finished
callback URL is printed, paste it into the sign-in prompt.

### 2. Token from the environment

Check `HDNAVIGATOR_MCP_TOKEN` first. If it is set, the client sends it in the Authorization header,
so call the tools **without** the `token` argument. Do not ask the user again.

If the user pasted an `hdn_...` token in chat and it is not saved yet, run the one-time setup command
from the website (or the equivalent for this harness) so future sessions do not need the token:

- Codex: add `[mcp_servers.hdnavigator]` with `url = "https://mcp.slavayank.com/mcp"` and
  `bearer_token_env_var = "HDNAVIGATOR_MCP_TOKEN"` to `~/.codex/config.toml`;
- save it into the `HDNAVIGATOR_MCP_TOKEN` environment variable:
- Windows: `setx HDNAVIGATOR_MCP_TOKEN "hdn_..."`;
- macOS/Linux: append `export HDNAVIGATOR_MCP_TOKEN="hdn_..."` to `~/.zshrc` (or `~/.bashrc` / `~/.profile`);
- OpenCode: `opencode mcp add hdnavigator --global --url https://mcp.slavayank.com/mcp --header 'Authorization=Bearer {env:HDNAVIGATOR_MCP_TOKEN}'` and set `oauth: false` in the server config.

Then tell the user to restart the agent: a newly saved variable is only read by new sessions. For the
current session, use the token they sent in chat as the `token` argument.

### 3. Token argument (fallback)

If no Authorization header is configured, pass the `hdn_...` token as the optional `token` argument.
This is backward-compatible and works immediately, including the first session when the user just
pasted the token. After using it, offer to run the setup command from section 2.

Never repeat the token back to the user, never include it in final answers, and never write it into
project files, logs, or commits. If the user pasted a token into chat, you may mention that they can
rotate it later in their HDnavigator account.

## Tools

Use `get_new_chart` to create a new Human Design chart from exact birth data. Ask for missing birth
fields before calling: `year`, `month`, `day`, `hour`, `minute`, `city`, `country`. Add `token` only
when using fallback section 3.

Send birth data in English field names. Preserve city and country exactly as provided. The upstream
service resolves timezone after authentication.

Use `list_saved_charts` for the user's library. It is paginated with `limit` and `offset`; the next
offset is `offset + limit`. Use `get_saved_chart` with a numeric `chart_id` when the user selects a
saved chart. Both are free; `get_new_chart` consumes balance.

## Response Style

When a chart response contains `image_url`, show the bodygraph image first:

```markdown
![Human Design bodygraph](https://example.com/images/bodygraphs/1.png)
```

Then show `page_url`, summarize type, strategy, authority, profile, definition, centers, gates,
channels, incarnation cross and variables. Treat returned descriptions as authoritative; translate
them into the user's language without changing meaning. Do not dump raw JSON unless explicitly asked.

## Errors

- `401`/`403` — token rejected; if using fallback, offer to configure the Authorization header;
- `402` — insufficient balance; include the top-up link if returned;
- `404` — chart not found or not owned; `422` — correct birth data or chart id;
- `429` — rate limit; suggest retrying later. It never means insufficient balance.
