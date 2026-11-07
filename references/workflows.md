# Workflows

Choose an existing connected transport; do not install another just to read a
result. The deployment's `/llms.txt` indexes maintained API documentation, and
`/openapi.json` contains the full schema. The CLI and SDK downloads are linked
from `/agents`; registry publication and account ownership are deployment details.

## MCP

For an authorized source call:

```json
{
  "media": "https://www.youtube.com/watch?v=VIDEO_ID",
  "instructions": "Extract the practical recommendations and flag weak evidence.",
  "idempotency_key": "research-brief-001"
}
```

Pass this to `analyze_media`, preserve the returned `job_id`, then call `get_job`.
The status response is the job itself. On `completed`, use `summary_id` with
`get_summary`. A normal failure is a result to interpret, not permission to start
unbounded replacement jobs. Poll only while nonterminal.

## CLI

The installed CLI reads `TLDW_API_URL` and `TLDW_API_TOKEN` from the environment.
Node.js 20.11 or newer is required. Save the accepted receipt written to stderr.

```sh
tldw analyze --media 'https://www.youtube.com/watch?v=VIDEO_ID' \
  --instructions 'Extract practical recommendations and flag weak evidence.' \
  --idempotency-key research-brief-001

tldw wait JOB_ID
```

For complete user-supplied text, use a UTF-8 file:

```sh
tldw analyze --file ./source.txt \
  --instructions 'Extract the argument and strongest counterarguments. Cite passages.' \
  --idempotency-key supplied-thread-001
```

These are command templates: use the actual source/job ID. Secrets do not belong
in command flags. A new key for a new task is safe; changing the body under the
same key returns an idempotency conflict. Stop waiting on timeout and preserve the
ID for later resumption; a stopped client does not cancel the server job.

## SDKs and reference workflows

The npm client is `@tldw/client`; the Python distribution is `tldw-client`, imported
as `tldw_client`. Confirm availability in the user's configured registry, or use
the deployment's versioned `.tgz` / `.whl` downloads. Both clients expose submit,
poll and retrieve methods; `analyze` combines them while retaining the receipt.

The deployment's reference-workflow ZIP includes runnable YouTube research,
TikTok comparison and complete-thread-text scripts. Their README gives the actual
file layout and arguments; use `--help` before running a new workflow.

For a TikTok comparison use the caller's links and chosen focus. The REST request
contains `urls` and `instructions`; the response wraps `comparison`. The completed
result includes cited findings and source coverage, including unusable clips.
