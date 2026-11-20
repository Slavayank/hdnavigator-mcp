# HDnavigator MCP — for any AI harness

<p align="center">
  <a href="#english"><img alt="In English" src="https://img.shields.io/badge/In%20English-111827?style=for-the-badge"></a>
  <a href="#russian"><img alt="На русском" src="https://img.shields.io/badge/%D0%9D%D0%B0%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC-2563eb?style=for-the-badge"></a>
</p>

<a id="english"></a>

HDnavigator MCP connects an AI agent to the HDnavigator Human Design service.

With these tools the agent can:

- create and save a bodygraph from exact birth data;
- show `image_url` first, then `page_url` and structured facts;
- list saved charts and open one by `chart_id`;
- explain type, authority, profile, centers, gates, channels, variables and descriptions in the user's language.

- Hosted MCP endpoint: `https://mcp.slavayank.com/mcp`
- Website (token, balance, usage): `https://hdnavigator.ru`
- Source: `https://github.com/Slavayank/hdnavigator-mcp`

## Quick start — choose your harness

Repository (works for every harness): **https://github.com/Slavayank/hdnavigator-mcp**
Hosted MCP server: **`https://mcp.slavayank.com/mcp`**

**Commands starting with `codex` or `npx codex-marketplace` only affect Codex.** They do not install
anything into OpenCode, Claude Code, Cursor or any other harness.

| Harness | Universal command |
| --- | --- |
| **Codex** | `npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --global` (or `--plugins --project`) |
| **OpenCode** | `opencode mcp add hdnavigator --url https://mcp.slavayank.com/mcp` — if the CLI is not installed: `npx -y @opencode/cli mcp add hdnavigator --url https://mcp.slavayank.com/mcp` |
| **Any other MCP client** | Add a remote / Streamable HTTP server with URL `https://mcp.slavayank.com/mcp` |

For a client configured by hand:

```json
{
  "mcpServers": {
    "hdnavigator": { "url": "https://mcp.slavayank.com/mcp" }
  }
}
```

## What happens after installation

The agent immediately makes a harmless tool call (`list_saved_charts`). The server answers with an
OAuth challenge (`401` + `WWW-Authenticate`), and the client starts sign-in **by itself** and prints an
authorization URL. The agent must copy that URL verbatim and give it to you. Open it in **your own
browser** on the same computer (an embedded browser may not have your HDnavigator session), log in if
asked, and click the green **Allow / Разрешить** button. The local callback receives the code and the
connection is ready — no menus and no token pasting.

If the client does not print a URL, run its sign-in command and pass the printed URL the same way:
`codex mcp login hdnavigator` (Codex) or `opencode mcp auth hdnavigator` (OpenCode).

## Fallback — no OAuth, no browser

For users who prefer the simplest path: get an `hdn_...` token at `https://hdnavigator.ru`
(register + confirm email), paste it into the chat once, and the agent saves it into the client
config automatically (Codex: `bearer_token_env_var`; OpenCode: `Authorization` header) and restarts
the connection. The token is never repeated back. See `skills/hdnavigator-chart-guide/SKILL.md`.

## Authentication: three supported flows

The server uses **dual-mode authentication**. All three flows call the same three tools.

### 1. OAuth — recommended, no token in chat

The agent signs in through OAuth 2.1 (PKCE). The access token is kept by the client and sent in the
`Authorization` header; the model never sees it.

```bash
# Codex
codex mcp login hdnavigator
# OpenCode
opencode mcp auth hdnavigator
```

The sign-in page opens in a browser. **Important:** if the harness opens its own embedded browser
with no active HDnavigator session, copy the authorization URL it prints and open it in **your own browser**,
where you are already logged in to `https://hdnavigator.ru`. Approve access there; the local
callback listener (`http://127.0.0.1/...`) receives the code even when the page is opened elsewhere.
If the harness shows a finished callback URL (`http://127.0.0.1:PORT/callback?code=...`), paste it
into the sign-in prompt.

### 2. Static token in `Authorization` — simple, no browser

Get a token at `https://hdnavigator.ru`: register, confirm your email and create a token starting with
`hdn_`. Save it once in the environment variable `HDNAVIGATOR_MCP_TOKEN` and point the MCP client at
that variable. The agent does not need to know the token value.

**Codex** — add to `~/.codex/config.toml`:

```toml
[mcp_servers.hdnavigator]
url = "https://mcp.slavayank.com/mcp"
bearer_token_env_var = "HDNAVIGATOR_MCP_TOKEN"
```

Save the variable (Windows):

```powershell
setx HDNAVIGATOR_MCP_TOKEN "hdn_your_token_here"
```

or macOS / Linux (add to `~/.zshrc`, `~/.bashrc` or `~/.profile`):

```bash
export HDNAVIGATOR_MCP_TOKEN="hdn_your_token_here"
```

Restart the agent: a variable set with `setx` or in a shell profile is read by **new** sessions.

**OpenCode** — add to `opencode.json` (project or global) or use the CLI:

```bash
opencode mcp add hdnavigator --global --url https://mcp.slavayank.com/mcp --header 'Authorization=Bearer {env:HDNAVIGATOR_MCP_TOKEN}'
```

```jsonc
{
  "mcp": {
    "servers": {
      "hdnavigator": {
        "type": "remote",
        "url": "https://mcp.slavayank.com/mcp",
        "oauth": false,
        "headers": { "Authorization": "Bearer {env:HDNAVIGATOR_MCP_TOKEN}" }
      }
    }
  }
}
```

### 3. Token in the chat / tool argument — backward-compatible fallback

Nothing has to be installed: send the `hdn_...` token to the agent in chat, and the agent passes it as
the optional `token` argument. This is the legacy path and is kept for old clients. The agent should
offer to run the one-time setup command from variant 2 so that the next session no longer needs the
token in chat. Never repeat the token back, and never write it into project files.

## Ready-made setup command from the website

`https://hdnavigator.ru` → **API / MCP** generates the exact command for your account and harness
(Codex, OpenCode or a universal prompt) with your token already inserted. Copy it into the agent once;
the agent runs it, saves `HDNAVIGATOR_MCP_TOKEN` and configures the client. Restart the agent.

## Birth data format

```json
{ "year": 1990, "month": 5, "day": 21, "hour": 14, "minute": 35, "city": "Omsk", "country": "Russia" }
```

Timezone is resolved by HDnavigator after authentication, using city and country.

## Tools

| Tool | Arguments | Notes |
| --- | --- | --- |
| `get_new_chart` | `year`, `month`, `day`, `hour`, `minute`, `city`, `country`, optional `token` | Creates and saves a chart; charged |
| `list_saved_charts` | optional `limit`, `offset`, `token` | Free; next offset = `offset + len(charts)` |
| `get_saved_chart` | `chart_id`, optional `token` | Free; ownership checked by HDnavigator |

`token` is optional now: it is only a fallback for clients that cannot send an `Authorization` header.
Tool calls without either credential return an explicit authentication error.

## Errors

- `401` — token invalid/expired; `403` — access denied; `402` — insufficient balance (top-up link is returned);
- `404` — chart not found/not owned; `422` — invalid input; `429` — rate limit, not a balance problem.

---

<a id="russian"></a>

# HDnavigator MCP для Codex / OpenCode

Плагин подключает агента к сервису HDnavigator (Design Человека): создать бодиграф, показать картинку
и ссылку, список сохранённых расчётов и объяснение параметров на языке пользователя.

- MCP-сервер: `https://mcp.slavayank.com/mcp`
- Сайт (токен, баланс, статистика): `https://hdnavigator.ru`
- Репозиторий: `https://github.com/Slavayank/hdnavigator-mcp`

## Быстрый старт — выберите харнес

Репозиторий (подходит для любого харнеса): **https://github.com/Slavayank/hdnavigator-mcp**
MCP-сервер: **`https://mcp.slavayank.com/mcp`**

**Команды, начинающиеся с `codex` или `npx codex-marketplace`, действуют только на Codex.** В OpenCode, Claude Code, Cursor и другие харнесы они ничего не устанавливают.

| Харнес | Универсальная команда |
| --- | --- |
| **Codex** | `npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --global` (или `--plugins --project`) |
| **OpenCode** | `opencode mcp add hdnavigator --url https://mcp.slavayank.com/mcp` — если CLI не установлен: `npx -y @opencode/cli mcp add hdnavigator --url https://mcp.slavayank.com/mcp` |
| **Любой другой MCP-клиент** | Добавьте удалённый сервер Streamable HTTP с URL `https://mcp.slavayank.com/mcp` |

Если клиент настраивается вручную:

```json
{
  "mcpServers": {
    "hdnavigator": { "url": "https://mcp.slavayank.com/mcp" }
  }
}
```

## Что происходит после установки

Агент сразу делает безобидный вызов (`list_saved_charts`). Сервер отвечает OAuth-челленджем (`401` + `WWW-Authenticate`), клиент **сам** начинает вход и печатает URL авторизации. Агент обязан скопировать этот URL дословно и дать его вам. Откройте его **в своём браузере на этом же компьютере** (внутренний браузер может быть без вашей сессии), при необходимости войдите и нажмите зелёную кнопку **«Разрешить»**. Локальный callback получит код — подключение готово, без меню и без вставки токена.

Если клиент не показал URL, выполните его команду входа и передайте показанный URL так же: `codex mcp login hdnavigator` (Codex) или `opencode mcp auth hdnavigator` (OpenCode).

## Запасной вариант — без OAuth и без браузера

Самый простой путь: получите токен `hdn_...` на `https://hdnavigator.ru` (регистрация + подтверждение email), пришлите его один раз в чат — агент сам сохранит его в конфиг клиента (Codex: `bearer_token_env_var`; OpenCode: заголовок `Authorization`) и переподключит сервер. Токен никогда не повторяется вслух. См. `skills/hdnavigator-chart-guide/SKILL.md`.

## Аутентификация: три варианта

Сервер работает в **dual-mode**: все три варианта вызывают одни и те же инструменты.

### 1. OAuth — рекомендуется, токен не попадает в чат

Агент входит через OAuth 2.1 (PKCE). Access-токен хранит клиент и отправляет его в заголовке
`Authorization`; модель его не видит.

```bash
# Codex
codex mcp login hdnavigator
# OpenCode
opencode mcp auth hdnavigator
```

**Важно:** если харнес открывает свой внутренний браузер без активной сессии HDnavigator, скопируйте
выведенный URL авторизации и откройте его в том браузере, где вы уже вошли на `https://hdnavigator.ru`.
Подтвердите доступ там — локальный слушатель (`http://127.0.0.1/...`) получит код, даже если страницу
открыли в другом браузере. Если харнес показывает готовый callback-URL, вставьте его в приглашение входа.

### 2. Статический токен в `Authorization` — без браузера

Получите токен на `https://hdnavigator.ru`: зарегистрируйтесь, подтвердите email, создайте токен `hdn_`.
Один раз сохраните его в переменную `HDNAVIGATOR_MCP_TOKEN` и укажите её клиенту. Агенту значение токена
не нужно.

**Codex** — в `~/.codex/config.toml`:

```toml
[mcp_servers.hdnavigator]
url = "https://mcp.slavayank.com/mcp"
bearer_token_env_var = "HDNAVIGATOR_MCP_TOKEN"
```

Windows: `setx HDNAVIGATOR_MCP_TOKEN "hdn_your_token_here"`;
macOS/Linux: `export HDNAVIGATOR_MCP_TOKEN="hdn_your_token_here"` в `~/.zshrc` / `~/.bashrc` / `~/.profile`.
Перезапустите агента: переменная читается только новыми сессиями.

**OpenCode**:

```bash
opencode mcp add hdnavigator --global --url https://mcp.slavayank.com/mcp --header 'Authorization=Bearer {env:HDNAVIGATOR_MCP_TOKEN}'
```

или в `opencode.json`: `{"mcp":{"servers":{"hdnavigator":{"type":"remote","url":"https://mcp.slavayank.com/mcp","oauth":false,"headers":{"Authorization":"Bearer {env:HDNAVIGATOR_MCP_TOKEN}"}}}}}`.

### 3. Токен в чате / аргументе — обратная совместимость

Ничего устанавливать не нужно: пришлите `hdn_...` агенту в чат, он передаст его необязательным
аргументом `token`. Это старый путь, он сохранён для прежних клиентов. Агент должен предложить выполнить
команду настройки из варианта 2, чтобы в следующей сессии токен больше не нужен был в чате. Никогда не
повторяйте токен и не записывайте его в файлы проекта.

## Готовая команда на сайте

На `https://hdnavigator.ru` → **API / MCP** для вашего аккаунта генерируется точная команда под ваш
харнес (Codex, OpenCode или универсальный промпт) с уже вставленным токеном. Скопируйте её агенту один
раз; агент сохранит `HDNAVIGATOR_MCP_TOKEN`, настроит клиент и перезапустится.

## Формат данных рождения

```json
{ "year": 1990, "month": 5, "day": 21, "hour": 14, "minute": 35, "city": "Omsk", "country": "Russia" }
```

Часовой пояс определяет HDnavigator после аутентификации по городу и стране.

## Инструменты

| Инструмент | Аргументы | Особенность |
| --- | --- | --- |
| `get_new_chart` | `year`, `month`, `day`, `hour`, `minute`, `city`, `country`, опционально `token` | Создаёт и сохраняет карту, платно |
| `list_saved_charts` | опционально `limit`, `offset`, `token` | Бесплатно; следующий offset = `offset + len(charts)` |
| `get_saved_chart` | `chart_id`, опционально `token` | Бесплатно; владельца проверяет HDnavigator |

`token` теперь необязателен — это только fallback для клиентов, которые не умеют слать `Authorization`.
Вызов без токена и без заголовка возвращает явную ошибку аутентификации.

## Ошибки

- `401` — токен неверен/истёк; `403` — нет доступа; `402` — недостаточно баланса (возвращается ссылка);
- `404` — карта не найдена или не принадлежит аккаунту; `422` — неверные данные; `429` — лимит запросов, не баланс.
