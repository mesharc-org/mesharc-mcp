# MeshArc MCP Server

MeshArc turns any website into clean markdown your assistant can read, and keeps a record of what changed on it. It gives Claude, Cursor and any MCP client 19 tools to read pages, map and crawl sites, watch a site over time and ask what changed, all in plain English. Add it by URL, with nothing to install.

The **free plan includes 1,000 credits with no card**, and a plain fetch costs 1 credit.

```text
https://mcp.mesharc.dev/mcp
```

[![Glama score](https://glama.ai/mcp/connectors/dev.mesharc/mesharc/badges/score.svg)](https://glama.ai/mcp/connectors/dev.mesharc/mesharc) ![MCP remote, streamable HTTP](https://img.shields.io/badge/MCP-remote%20%7C%20streamable%20HTTP-6366f1?style=flat-square) ![tools 19](https://img.shields.io/badge/tools-19-10b981?style=flat-square) [![PyPI](https://img.shields.io/pypi/v/mesharc?style=flat-square&logo=pypi&logoColor=white&label=PyPI&color=3775a9)](https://pypi.org/project/mesharc/) ![license MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

## Contents

- [What can you do with it?](#what-can-you-do-with-it)
- [What you need](#what-you-need)
- [Quick start](#quick-start)
- [Example prompts](#example-prompts)
- [Tools](#tools)
- [Errors and failure paths](#errors-and-failure-paths)
- [Pricing, free tier and limits](#pricing-free-tier-and-limits)
- [Tool selection](#tool-selection)
- [How it compares](#how-it-compares)
- [FAQ](#faq)
- [Source](#source)
- [Links](#links)
- [License](#license)

## What can you do with it?

- **Read any page as clean markdown.** Pass one URL or up to 500. Navigation, cookie banners and boilerplate are stripped. PDF, Word and spreadsheet links are read as text.
- **Get past walled sites.** Each page climbs a fetch ladder: a plain request first, then a real browser, then stealth and residential exits only when the page needs them. You pay for the rung that worked. A page the site refuses comes back marked as blocked, and costs nothing.
- **Map a site before you fetch it.** Every URL a site declares in its sitemaps, with its sections, without fetching a single page.
- **Crawl a whole site or one section.** Use path globs such as `/blog/*`, with a page limit and a depth. You get an index of every page plus readable excerpts, sized to fit a chat turn.
- **Watch a site over time.** Make it a project, put it on a schedule, and ask "what changed?". You get pages added, modified and removed, and field-level changes. Removals are held back when a run reached too little of the site, so a blocked crawl never reports a site as gone.
- **Run browser steps.** Click "Load more" until it disappears, type into a search box, pick an option, then read the page.
- **Extract structured fields.** Give a JSON schema and get the same fields from every page.

## What you need

- An MCP client that speaks remote MCP (Claude.ai, Claude Desktop, Claude Code, Cursor, VS Code, Windsurf…), or Python 3.10+ to run the server locally.
- A MeshArc account. You sign in when you first connect, and the free plan needs no card.

## Quick start

**Hosted (recommended).** Nothing to install, and no key to copy: you sign in to mesharc.dev and approve once. The connection is read-only unless you tick write access.

| Field | Value |
|---|---|
| URL | `https://mcp.mesharc.dev/mcp` |
| Transport | HTTP, streamable |
| Auth | OAuth: sign in and approve in the browser |

Claude.ai: Settings → Connectors → Add custom connector → paste the URL and sign in.

Claude Code:

```bash
claude mcp add --transport http mesharc https://mcp.mesharc.dev/mcp
```

Cursor, Windsurf and other clients (`mcp.json`):

```json
{
  "mcpServers": {
    "mesharc": { "url": "https://mcp.mesharc.dev/mcp" }
  }
}
```

**Local (stdio), with your own API key.** Make a key under Settings → API keys on mesharc.dev.

```bash
pip install "mesharc[mcp]"
claude mcp add mesharc -e MESHARC_API_KEY=mesharc_... -- mesharc-mcp
```

Claude Desktop (`claude_desktop_config.json`) or Cursor:

```json
{
  "mcpServers": {
    "mesharc": {
      "command": "mesharc-mcp",
      "env": { "MESHARC_API_KEY": "mesharc_..." }
    }
  }
}
```

## Example prompts

These conversations were run against real sites; the results are the real ones.

- "Get Linear's pricing page and list every tier and price." The assistant used `scrape_urls`: 1 credit and 4 seconds for the four tiers.
- "How many pages does the FastAPI docs site have, and which are about security?" The assistant used `map_site`: 151 URLs declared, 9 under /tutorial/security/, with no page fetched.
- "Set up a project for hotspotseo.com that only scrapes the blog, weekly." The assistant used `describe_project_config`, `map_site` and `create_project`. It found the blog under /blogs/, not /blog/, and the first run read only blog pages.
- "Make it daily instead, and skip the tag and author pages." The assistant used `update_project`; the include setting stayed as it was.
- "Re-check the home page and page 2 now. What changed?" The assistant used `recrawl_pages`, then `get_changes`.
- "Read this arXiv paper (a PDF) and summarise the method." The assistant used `scrape_urls`: 6,036 words of text for 2 credits.
- "Which of these pages mention GDPR?" The assistant used `search_pages` on the stored crawl, at no credit cost.

## Tools

**Read the web**

| Tool | What it does | Credits |
|---|---|---|
| `scrape_urls` | Content of 1 to 500 known URLs. PDF, Word and spreadsheet files are read as text. | per page |
| `extract_url` | One URL with every format: raw html, head and extracted fields, images. Browser steps run first. | per page |
| `map_site` | Every URL a site declares in its sitemaps, with its sections, without fetching a page. | 1 per sitemap file |
| `crawl_site` | Crawl a site or a section once, with page limit, depth and path globs. You get an index plus excerpts. | per page |

**Watch a site over time**

| Tool | What it does | Credits |
|---|---|---|
| `keep_crawl_as_project` | Turn a `crawl_site` crawl into a watched project, with nothing fetched again. | none |
| `create_project` | A watched project from a URL, with any settings: one section, a schedule, a format. | none |
| `describe_project_config` | Every setting an assistant can set, with its meaning and default. | none |
| `list_projects` | The workspace's projects, with status and last run. | none |
| `get_project` | One project's settings and state. | none |
| `update_project` | Change the name, schedule or settings. Only the keys you give change. | none |
| `start_run` | Crawl a project now. You can wait for it to finish. | per page |
| `recrawl_pages` | Fetch listed pages of a project again now, compared with the last full run. | per page |
| `list_runs` | A project's runs, newest first. | none |
| `list_pages` | A run's pages: url, status, depth, words, when changed. | none |
| `get_page` | One stored page in full, with its versions across runs. | none |
| `search_pages` | Search a run's pages: words, a quoted phrase, or a CSS selector. | none |
| `get_changes` | Pages added, modified and removed since the run before, with field changes. | none |

**Long jobs**

| Tool | What it does | Credits |
|---|---|---|
| `get_job` | Follow a crawl, run or batch that came back as a job, and get its result. | none |
| `cancel_job` | Stop a crawl, run or batch that is still going. Pages already read stay. | none |

Read-only tools are marked read-only, and the two that overwrite or stop work are marked destructive.

## Errors and failure paths

- **Blocked is not missing.** A page the site refuses is reported as `blocked` (or `captcha`, `timeout`, `missing` for a 404 or 410), never as an empty page, and none of them is charged.
- **Read-only connections:** any tool that fetches or changes something answers `code: read_only`, with how to reconnect with write access.
- **Long work:** a crawl, run or batch that outlasts the connection's time limit comes back as a job. `get_job` picks it up, and calling the original tool again returns the same job rather than starting a second one.
- **Out of credits:** `402`. A run that uses up the budget stops and keeps what it read.
- **A run already going:** `start_run` and `recrawl_pages` answer `409`; `list_runs` shows it and `cancel_job` stops it.
- **Plan limits:** `create_project` answers `plan_limit` when the plan's project count is full; values above a plan's caps are lowered to them.
- **Settings:** an unknown config key is refused by name, never silently dropped.
- **Size:** a many-page answer is an index plus excerpts inside 60,000 characters; any one page comes back whole (each body up to 12,000 characters) on request.

## Pricing, free tier and limits

- **Free:** 1,000 credits once, with no card. 2 projects, 500 pages per run, and 7-day retention.
- **Paid plans:** Starter $29/mo (100,000 credits), Growth $99/mo (500,000 credits, stealth tier), Scale $349/mo (2,500,000 credits), and Enterprise.
- **A credit:** a plain fetch costs 1, a fetch with a site's session 2, a real Chrome 4, a residential address 16, a solved widget 22.
- **Free of charge:** a refused page, a 404 or 410, a cached page, change detection, search, and listing and reading what is stored.
- The MCP server itself costs nothing extra. A tool call is an ordinary request through your account, with the same credits, limits and rate.

## Tool selection

- You have the URLs → `scrape_urls`. You need to find them → `map_site` (cheap, declared URLs only) or `crawl_site` (follows links).
- One page with clicks, structured fields or every format → `extract_url`.
- You want to know what changes over time → `create_project`, then `start_run` and `get_changes`.
- You want to read what was already crawled, at no cost → `list_pages`, `get_page`, `search_pages`, `get_changes`.

## How it compares

| | Firecrawl | MeshArc |
|---|---|---|
| Blocked or error response billed | Yes | No |
| 404 billed | Yes | No |
| Cheaper repeat reads of protected sites | No | Yes, session reuse at 2 credits |
| Website change monitoring | Yes (Monitor) | Yes, with sitemap sections and held-back removals |
| Web search API | Yes | No |
| Autonomous agent / browser interaction | Yes | Browser steps only |
| Open source | Yes | No |

Checked against public documentation and pricing pages. If you need web search or an autonomous research agent, Firecrawl is the stronger fit.

## FAQ

### Does the assistant see my API key?

No. Hosted, you approve the app and MeshArc issues it a key of its own, which you can see and revoke under Settings → API keys. Run locally, the key stays in the server's environment on your machine.

### Can it read pages behind a login?

No. It reads what a visitor can see. A login wall comes back as blocked, at no cost.

### Does it respect robots.txt?

Yes, by default (`respect_robots`).

### Can it change my projects?

Only if you allowed write access when you connected it.

### Which clients work?

Any client that speaks remote MCP over streamable HTTP, or any client that runs a stdio server (`mesharc-mcp`).

## Source

This repository is the MCP server's home page. The server itself is `mesharc/mcp.py` in [mesharc-org/mesharc-python](https://github.com/mesharc-org/mesharc-python), published on PyPI as [`mesharc`](https://pypi.org/project/mesharc/), and the hosted one runs at `https://mcp.mesharc.dev/mcp`. Report issues with the server in this repository or in mesharc-python.

## Links

- Website: https://mesharc.dev
- MCP page and setup per client: https://mesharc.dev/mcp
- Documentation: https://mesharc.dev/docs
- Python SDK and MCP server: https://github.com/mesharc-org/mesharc-python · https://pypi.org/project/mesharc/
- Node SDK: https://github.com/mesharc-org/mesharc-node
- Privacy: https://mesharc.dev/legal/privacy
- Support: hello@mesharc.dev

## License

MIT. The SDK and the MCP server are MIT licensed too.
