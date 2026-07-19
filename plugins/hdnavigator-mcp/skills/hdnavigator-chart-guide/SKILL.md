---
name: hdnavigator-chart-guide
description: Use when a user wants to create, retrieve, list, compare, or discuss Human Design charts through HDnavigator MCP.
---

# HDnavigator Chart Guide

Use the HDnavigator MCP tools whenever the user asks for a Human Design chart, bodygraph, saved calculation, or interpretation based on HDnavigator data.

## Authentication

The MCP server uses Bearer authentication. Users can get a token at https://hdnavigator.ru after registration and email confirmation. The plugin expects the token in `HDNAVIGATOR_MCP_TOKEN`.

Do not ask the user to paste the token into a chat message if the client can store it as plugin authentication or an environment variable.

## Tools

Use `get_new_chart` to create a new Human Design chart from ordered birth data. Ask for missing required fields before calling the tool: `year`, `month`, `day`, `hour`, `minute`, `city`, and `country`.

Send birth data to `get_new_chart` in English field names. Preserve city and country exactly as the user provided them unless the user corrects the spelling. The upstream service resolves timezone after token verification.

Use `list_saved_charts` when the user asks what charts are already saved. It is paginated with `limit` and `offset`. If the result has more records than shown, offer to continue with the next offset. The next offset is `offset + limit`.

Use `get_saved_chart` when the user chooses or mentions a saved chart id. Pass only the numeric `chart_id`.

## Response Style

When a chart response contains `image_url`, show the bodygraph image first:

```markdown
![Human Design bodygraph](https://example.com/images/bodygraphs/1.png)
```

Then show the permanent page link from `page_url` when present.

Summarize the main parameters in a human-readable order: type, strategy, authority, profile, definition, centers, gates, channels, incarnation cross, variables, and any descriptions supplied by HDnavigator.

Treat descriptions returned by HDnavigator as authoritative. Do not invent missing Human Design descriptions. If the response is in English and the user is speaking another language, translate and explain it in the user's language.

Do not dump raw JSON unless the user explicitly asks for raw data. Do not infer meaning from bodygraph pixels; rely on the structured response fields.

## Errors

If the MCP reports `401` or `403`, tell the user that the token was rejected or lacks access.

If the MCP reports `402`, explain that HDnavigator says payment or balance is required. If a top-up link is returned, include it.

If the MCP reports `404`, say that the saved chart was not found or is unavailable for this account.

If the MCP reports `422`, ask the user to correct the birth data or chart id.

If the MCP reports `429`, say that the request limit was reached and suggest trying again later. Do not describe `429` as an empty balance condition; balance/payment is `402`.
