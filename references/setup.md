# Connect to tldw.sh

The production MCP endpoint is **https://api.tldw.sh/mcp**. Reuse an existing
authenticated connection; avoid configuring duplicate servers. The account
owner signs in through the client's browser flow, reviews scopes and the
callback, and explicitly approves consent. Never automate consent or one-time
human verification.

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
