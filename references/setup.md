# Connect to tldw.sh

The production MCP endpoint is **https://api.tldw.sh/mcp**. Reuse an existing
authenticated connection; avoid configuring duplicate servers. The account
owner signs in through the client's browser flow, reviews scopes and the
callback, and explicitly approves consent. Never automate consent or one-time
human verification.

When setup needs service identity, activation-policy or catalog facts, the
connected MCP tools `public_config`, `public_security` and `billing_catalog`
provide read-only metadata without additional scopes. The same REST routes
`/v1/public/config`, `/v1/public/security` and `/v1/billing/catalog` can be read
without a key, including through SDK 0.2.14's explicit public-only client. A
public-only client cannot submit jobs or read private account/source data.

For clients with a remote-MCP command:

```sh
claude mcp add --transport http tldw https://api.tldw.sh/mcp
codex mcp add tldw --url https://api.tldw.sh/mcp
```

For other clients, add that URL as a remote Streamable HTTP MCP server and
choose Connect. Client configuration differs; https://tldw.sh/agents provides
the current client-specific setup. OAuth metadata is available at
https://api.tldw.sh/.well-known/oauth-protected-resource/mcp.

If the client needs an API-key fallback, the owner creates a scoped key at
https://tldw.sh/developers after enrollment and one-time verification. Standard
scopes are `account:read`, `jobs:write`, `jobs:read` and `summaries:read`. Store
the key privately as `TLDW_API_TOKEN` or in the client's supported secret store.
Never request provider keys, paste OAuth tokens into chat or send a refresh
token as an API key. Refresh and revocation belong to the client.
Manage or revoke connected apps at https://tldw.sh/settings#connected-apps.

## When an SDK is needed

Use the reviewed version and install method listed on https://tldw.sh/agents.
The owned package names are npm `@tldw/client` and PyPI `tldw-client`; do not
assume a registry's latest version contains the current API contract. Reusing
an existing MCP connection requires no SDK installation.

Set `TLDW_API_URL` explicitly to https://api.tldw.sh for SDK or CLI setup, or to
an explicitly configured HTTPS deployment. Preserve unrelated client configuration. Run
`tldw doctor` for a read-only connection check; it submits no processing work
and does not establish media coverage or billing readiness.

## YouTube discovery tool

YouTube search is a local yt-dlp operation, separate from tldw's hosted X search.
First check the existing executable without making a media request:

```sh
yt-dlp --version
```

Reuse a working installation. If it is missing, ask before installing, then
choose one method that fits the user's existing tools. Do not install several
copies or a new package manager just to follow this table.

| Existing tool or platform | Install command or source |
| --- | --- |
| uv, macOS/Linux/Windows | `uv tool install "yt-dlp[default]"` |
| pipx, macOS/Linux/Windows | `pipx install "yt-dlp[default]"` |
| Homebrew, macOS/Linux | `brew install yt-dlp` |
| winget, Windows | `winget install --source winget --id yt-dlp.yt-dlp` |
| No suitable manager | Choose the matching OS/CPU asset from the [official releases](https://github.com/yt-dlp/yt-dlp/releases/latest). |

The Python distribution currently requires Python 3.11 or newer; uv/pipx keep
the application in its own environment. Use a compatible existing interpreter
or an appropriate standalone release. Do not use `sudo pip`,
`--break-system-packages` or remove an `EXTERNALLY-MANAGED` marker. If installation
requires another runtime or a PATH change, explain that step before changing it.
Check `yt-dlp --version` again from the shell that will run discovery.

Use the same installation method for an authorized update, for example
`uv tool upgrade yt-dlp`, `pipx upgrade yt-dlp` or `brew upgrade yt-dlp`.
Package-manager releases can lag upstream. Full YouTube downloading may require
additional upstream dependencies; the discovery workflow requests flat metadata
and does not download or process audio/video. A working version check alone does
not prove search will succeed. On an error, report it without automatically
installing more tools, importing browser cookies or retrying indefinitely.

Installation and option details: [yt-dlp installation](https://github.com/yt-dlp/yt-dlp/wiki/Installation),
[yt-dlp usage and dependencies](https://github.com/yt-dlp/yt-dlp#readme),
[uv tools](https://docs.astral.sh/uv/guides/tools/) and
[pipx](https://pipx.pypa.io/latest/). Check these primary sources and the installed
`yt-dlp --help` when options or platform requirements change. Continue with
[Find YouTube videos](workflows.md#find-youtube-videos).
