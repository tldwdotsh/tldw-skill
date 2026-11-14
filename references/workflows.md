# Workflows

Choose an existing connected transport; do not install another just to read a
result. The deployment's `/llms.txt` indexes maintained API documentation, and
`/openapi.json` contains the full schema. Install the SDKs as npm `@tldw/client`
or PyPI `tldw-client`. As a fallback, `/agents` links versioned downloads with a
SHA-256 checksum for each file; install those only after the checksum matches.
Never install a similarly named package.

## Summary and original transcript

Submit one link through MCP `analyze_media` or REST `POST /v1/analyses`.
Save the accepted `job_id` and poll `get_job` / `wait_job` until completed.
The same job saves a summary and its original transcript. Read them using
`get_summary` and `get_transcript` with the same `summary_id`, or REST
`GET /v1/summaries/{summary_id}` and `GET /v1/summaries/{summary_id}/transcript`.
Reading saved results creates no job, model call or processing charge.
Use `list_transcripts` and `get_saved_transcript` for saved-source pagination.

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

## Captioned X video

For a captioned X video, pass the post URL to `analyze_media`:

```json
{
  "media": "https://x.com/hamptonism/status/2071631335836225751",
  "instructions": "Summarize the spoken content in Spanish. Keep it concise and avoid repetition.",
  "transcription": "never",
  "idempotency_key": "x-video-spanish-001"
}
```

Default `scope:auto` detects the attachment. `scope:post` is explicitly text-only.
Retain `job_id`, poll `get_job` and call `get_summary` after completion. The
translated summary is generated text; the saved source captions remain original.
Missing captions fail explicitly; X audio transcription is not enabled.

## CLI

Run the CLI with `npx tldw` from a project where the client is installed. It reads `TLDW_API_URL` and `TLDW_API_TOKEN` from the environment.
Node.js 20.11 or newer is required. Save the accepted receipt written to stderr.

```sh
npx tldw analyze --media 'https://www.youtube.com/watch?v=VIDEO_ID' \
  --instructions 'Extract practical recommendations and flag weak evidence.' \
  --idempotency-key research-brief-001

npx tldw wait JOB_ID
```

For complete user-supplied text, use a UTF-8 file:

```sh
npx tldw analyze --file ./source.txt \
  --instructions 'Extract the argument and strongest counterarguments. Cite passages.' \
  --idempotency-key supplied-thread-001
```

These are command templates: use the actual source/job ID. Secrets do not belong
in command flags. A new key for a new task is safe; changing the body under the
same key returns an idempotency conflict. Stop waiting on timeout and preserve the
ID for later resumption; a stopped client does not cancel the server job.

## SDKs and reference workflows

Install the clients with `npm install @tldw/client` or
`python -m pip install tldw-client`. The fallback is the deployment's versioned
`.tgz` / `.whl` download listed on its `/agents` page: verify its SHA-256 shown
there (for example `shasum -a 256 -c -`), then install the verified local file.
Never install a similarly named package. Once installed, JavaScript imports `TldwClient` from the installed
package and Python imports `tldw_client`. Both clients expose submit,
poll and retrieve methods; `analyze` combines them while retaining the receipt.
Generated output and original source use separate reads: JavaScript `getSummary`
and `getTranscript`, Python `get_summary` and `get_transcript`. Both use the
completed job's `summary_id` and require `summaries:read`. They do not start
another analysis or consume processing credits. REST reads saved source at
`GET /v1/summaries/{summary_id}/transcript`; MCP uses paginated `get_transcript`.

The deployment's reference-workflow ZIP includes runnable YouTube research and
complete-thread-text scripts. Their README gives the actual file layout and
arguments; use `--help` before running a new workflow.
