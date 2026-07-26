# HDnavigator MCP Plugin

HDnavigator MCP connects Codex to the public HDnavigator Human Design MCP server at:

`https://mcp.slavayank.com/mcp`

The MCP server exposes three tools:

- `get_new_chart`: create and save a new Human Design bodygraph from birth data.
- `list_saved_charts`: list saved charts with `limit` and `offset` pagination.
- `get_saved_chart`: retrieve a saved chart by numeric `chart_id`.

Each chart response can include a bodygraph `image_url`, a permanent `page_url`, structured chart parameters, and HDnavigator descriptions. Codex should show the bodygraph image first, summarize the chart in human-readable language, and translate HDnavigator's English response into the user's language when appropriate.

## Authentication

Users can get an HDnavigator token at https://hdnavigator.ru after registration and email confirmation. Tokens should start with `hdn_`.

There are two ways to use the token:

- Save it as `HDNAVIGATOR_MCP_TOKEN` before starting Codex.
- Or send it in chat when Codex asks for the HDnavigator token.

Codex will pass the token to MCP tool calls as the `token` argument. Do not commit real tokens to this repository.

## Install From GitHub

After this repository is published, users can add its marketplace to Codex:

```bash
codex plugin marketplace add <github-owner>/<github-repo>
```

Then install `HDnavigator MCP` from the Codex plugin list. Codex should explain that the user needs an `hdn_...` token from https://hdnavigator.ru and can either save it in `HDNAVIGATOR_MCP_TOKEN` or send it in chat.

For local testing before publication:

```bash
codex plugin marketplace add .
codex plugin add hdnavigator-mcp@hdnavigator
```

## Starter Prompts

- Create my Human Design chart.
- Show my saved HDnavigator charts.
- Explain this Human Design bodygraph.

## Notes For Codex

Ask for the user's HDnavigator `hdn_...` token before calling tools if one is not already available. Do not repeat the token back to the user. Ask for `year`, `month`, `day`, `hour`, `minute`, `city`, and `country` before creating a new chart. Send those fields using English JSON keys along with the `token` field. HDnavigator resolves timezone upstream after token verification.

When `image_url` is present, render it as:

```markdown
![Human Design bodygraph](https://hdnavigator.ru/images/bodygraphs/1.png)
```

Then summarize chart parameters and descriptions. Avoid raw JSON unless the user explicitly requests it.
