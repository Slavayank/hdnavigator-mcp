---
name: hdnavigator-chart-guide
description: Use when a user wants to create, retrieve, list, compare, or discuss Human Design charts through HDnavigator MCP.
---

# HDnavigator Chart Guide

Use the HDnavigator MCP tools whenever the user asks for a Human Design chart, bodygraph, saved calculation, or interpretation based on HDnavigator data.

## Authentication

HDnavigator MCP can create a Human Design bodygraph and brief explanation for any complete birth date, but each tool call needs an HDnavigator token.

When the user has installed the plugin but has not provided a token yet, explain this setup flow:

1. Go to https://hdnavigator.ru.
2. Register and confirm the email address.
3. Get an HDnavigator token that starts with `hdn_`.
4. Either save it as `HDNAVIGATOR_MCP_TOKEN` before starting Codex or send the `hdn_...` token in chat.
5. After that, Codex can create a bodygraph with a short description for any birth date.

If the token is available in chat, pass it as the `token` argument to HDnavigator MCP tools. Do not repeat the token back to the user, do not include it in final answers, and do not store it in files. If the user pasted a token into chat, you may mention that they can rotate it later in their HDnavigator account for extra safety.

## Tools

Use `get_new_chart` to create a new Human Design chart from ordered birth data. Ask for a missing `token` first, then ask for missing birth fields before calling the tool: `year`, `month`, `day`, `hour`, `minute`, `city`, and `country`.

Send the token and birth data to `get_new_chart` in English field names. Preserve city and country exactly as the user provided them unless the user corrects the spelling. The upstream service resolves timezone after token verification.

Use `list_saved_charts` when the user asks what charts are already saved. It requires `token` and is paginated with `limit` and `offset`. If the result has more records than shown, offer to continue with the next offset. The next offset is `offset + limit`.

Use `get_saved_chart` when the user chooses or mentions a saved chart id. Pass `token` and the numeric `chart_id`.

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
