# HDnavigator MCP for Codex

<p align="center">
  <a href="#english"><img alt="In English" src="https://img.shields.io/badge/In%20English-111827?style=for-the-badge"></a>
  <a href="#russian"><img alt="На русском" src="https://img.shields.io/badge/%D0%9D%D0%B0%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC-2563eb?style=for-the-badge"></a>
</p>

<a id="english"></a>

HDnavigator MCP connects Codex to the HDnavigator Human Design service.

With this plugin, Codex can:

- create and save a new Human Design bodygraph from exact birth data;
- show the bodygraph image first when `image_url` is returned;
- list saved charts from the user's HDnavigator account;
- open one saved chart by `chart_id`;
- explain chart parameters, gates, channels, centers, profile, type, authority, and returned descriptions in the user's language.

The hosted MCP server is:

```text
https://mcp.slavayank.com/mcp
```

The HDnavigator website is:

```text
https://hdnavigator.ru
```

## Install

In AI Harness / Codex plugin installation flow, install this GitHub repository:

```bash
npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --global
```

If you want to install it only for the current project instead of globally:

```bash
npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --project
```

If your Codex environment uses the Codex CLI plugin commands directly, use:

```bash
codex plugin marketplace add Slavayank/hdnavigator-mcp
codex plugin add hdnavigator-mcp@hdnavigator
```

After installation, restart Codex or open a new task so the MCP tools can load.

## First prompt after installation

Send this first message to Codex:

```text
Create my Human Design chart with HDnavigator.
```

Codex should then ask for an HDnavigator token and exact birth data.

## Token

Get your HDnavigator token at:

```text
https://hdnavigator.ru
```

You need to register and confirm your email. Tokens should look like:

```text
hdn_...
```

You can use the token in either of two ways:

1. Save it before starting Codex:

```bash
export HDNAVIGATOR_MCP_TOKEN="hdn_your_token_here"
```

2. Or send it in chat when Codex asks for it.

If you send the token in chat, Codex should not repeat it back to you. You can rotate the token later on HDnavigator if needed.

## Birth data format

For a new chart, Codex needs:

```json
{
  "year": 1990,
  "month": 5,
  "day": 21,
  "hour": 14,
  "minute": 35,
  "city": "Omsk",
  "country": "Russia"
}
```

Timezone is resolved by HDnavigator after token verification, using the city and country.

## Available tools

The plugin exposes these MCP tools:

- `get_new_chart` — creates and saves a new Human Design chart.
- `list_saved_charts` — lists saved charts with `limit` and `offset` pagination.
- `get_saved_chart` — loads one saved chart by numeric `chart_id`.

Every tool call requires the user's HDnavigator token as the `token` argument.

## Expected chart response

HDnavigator may return:

- `image_url` — direct bodygraph image URL;
- `page_url` — permanent chart page, for example `https://hdnavigator.ru/bodygraph/1`;
- structured chart facts: type, profile, authority, centers, gates, channels, variables, cross, etc.;
- descriptions for type, profile, authority, gates, channels, centers, and other parameters.

Codex should show the image first:

```markdown
![Human Design bodygraph](https://hdnavigator.ru/images/bodygraphs/1.png)
```

Then Codex should show the permanent page URL, important structured facts, and translated descriptions. Raw JSON should be hidden unless the user explicitly asks for it.

## Example conversation

User:

```text
Create my Human Design chart with HDnavigator.
```

Codex:

```text
Please send your HDnavigator token. You can get it at https://hdnavigator.ru after registration and email confirmation.
```

User:

```text
hdn_your_token_here
1990-05-21, 14:35, Omsk, Russia
```

Codex then calls `get_new_chart` and explains the result.

## Troubleshooting

If Codex only shows the guide but does not see the tools, open a new task after installing the plugin.

If the token is invalid or expired, HDnavigator may return `401`.

If the account balance is not enough, HDnavigator may return `402`.

If too many requests are sent, HDnavigator may return `429`. This means rate limit, not insufficient balance.

If `image_url` is present but the image is not rendered by the client, Codex should still show the direct image link.

---

<a id="russian"></a>

# HDnavigator MCP для Codex

HDnavigator MCP подключает Codex к сервису HDnavigator для расчёта Дизайна Человека.

С этим плагином Codex может:

- создать и сохранить новый бодиграф по точным данным рождения;
- показать изображение бодиграфа первым, если в ответе есть `image_url`;
- показать список сохранённых расчётов пользователя;
- открыть один сохранённый расчёт по `chart_id`;
- объяснить тип, профиль, авторитет, центры, ворота, каналы, переменные и описания на языке пользователя.

Адрес MCP-сервера:

```text
https://mcp.slavayank.com/mcp
```

Сайт HDnavigator:

```text
https://hdnavigator.ru
```

## Установка

В AI Harness / установщике плагинов Codex установите этот GitHub-репозиторий:

```bash
npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --global
```

Если нужно установить только для текущего проекта:

```bash
npx codex-marketplace add Slavayank/hdnavigator-mcp --plugins --project
```

Если в вашей среде Codex используются прямые команды Codex CLI:

```bash
codex plugin marketplace add Slavayank/hdnavigator-mcp
codex plugin add hdnavigator-mcp@hdnavigator
```

После установки перезапустите Codex или откройте новый task, чтобы MCP-инструменты загрузились.

## Первый запрос после установки

Отправьте Codex первый запрос:

```text
Create my Human Design chart with HDnavigator.
```

Можно по-русски:

```text
Создай мой бодиграф через HDnavigator.
```

После этого Codex должен попросить HDnavigator token и точные данные рождения.

## Токен

Получите HDnavigator token на сайте:

```text
https://hdnavigator.ru
```

Для этого нужно зарегистрироваться и подтвердить email. Токен должен выглядеть примерно так:

```text
hdn_...
```

Токен можно использовать двумя способами:

1. Сохранить перед запуском Codex:

```bash
export HDNAVIGATOR_MCP_TOKEN="hdn_your_token_here"
```

2. Или отправить прямо в чат, когда Codex попросит токен.

Если токен отправлен в чат, Codex не должен повторять его обратно пользователю. При необходимости токен можно позже перевыпустить на HDnavigator.

## Формат данных рождения

Для нового расчёта Codex должен получить:

```json
{
  "year": 1990,
  "month": 5,
  "day": 21,
  "hour": 14,
  "minute": 35,
  "city": "Omsk",
  "country": "Russia"
}
```

Timezone определяется на стороне HDnavigator после проверки токена, по городу и стране.

## Доступные инструменты

Плагин подключает MCP-инструменты:

- `get_new_chart` — создать и сохранить новый бодиграф.
- `list_saved_charts` — получить список сохранённых расчётов с пагинацией `limit` и `offset`.
- `get_saved_chart` — получить один сохранённый расчёт по числовому `chart_id`.

Каждый вызов инструмента требует HDnavigator token в аргументе `token`.

## Ожидаемый ответ расчёта

HDnavigator может вернуть:

- `image_url` — прямую ссылку на изображение бодиграфа;
- `page_url` — постоянную ссылку на страницу расчёта, например `https://hdnavigator.ru/bodygraph/1`;
- структурированные параметры: тип, профиль, авторитет, центры, ворота, каналы, переменные, крест и т.д.;
- описания типа, профиля, авторитета, ворот, каналов, центров и других параметров.

Codex должен показать изображение первым:

```markdown
![Human Design bodygraph](https://hdnavigator.ru/images/bodygraphs/1.png)
```

Затем Codex должен показать постоянную ссылку, ключевые параметры и переведённые описания. Сырой JSON не нужно показывать, если пользователь явно не попросил.

## Пример диалога

Пользователь:

```text
Создай мой бодиграф через HDnavigator.
```

Codex:

```text
Для расчёта нужен HDnavigator token. Получите его на https://hdnavigator.ru после регистрации и подтверждения email.
```

Пользователь:

```text
hdn_your_token_here
1990-05-21, 14:35, Omsk, Russia
```

После этого Codex вызывает `get_new_chart` и объясняет результат.

## Частые проблемы

Если Codex видит только инструкцию, но не видит инструменты, откройте новый task после установки плагина.

Если токен неверный или истёк, HDnavigator может вернуть `401`.

Если на балансе недостаточно средств, HDnavigator может вернуть `402`.

Если отправлено слишком много запросов, HDnavigator может вернуть `429`. Это rate limit, а не нехватка баланса.

Если есть `image_url`, но клиент Codex не отрисовал картинку, Codex должен показать прямую ссылку на изображение.
