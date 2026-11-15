# Customer tools

Call `account_usage` before submitting. The server exposes these 12 customer
tools and three prompts. `tldw://guide` is the live read-only connection guide.
Client-specific prefixes do not change a tool's name or required scope.

<!-- generated:tldw-tools -->
| Tool | Scope | Use |
| --- | --- | --- |
| `account_usage` | `account:read` | Read current plan, credits, rates and source/audio/concurrency/search limits before submitting. |
| `analyze_media` | `jobs:write` | Submit one authorized source with instructions and a stable idempotency key. |
| `get_job` | `jobs:read` | Read the same durable job and its polling guidance. |
| `wait_job` | `jobs:read` | Wait on the same job; a client timeout does not cancel it. |
| `list_jobs` | `jobs:read` | Find existing jobs before considering another submission. |
| `cancel_job` | `jobs:write` | Cancel only when the user asks to stop the job. |
| `search_videos` | `jobs:write` | Find X posts with video for the user's topic; each new search uses one of the plan's monthly searches. |
| `get_summary` | `summaries:read` | Read the saved answer, findings, source references and limitations. |
| `get_transcript` | `summaries:read` | Read the original saved source for a summary, following next_offset. |
| `list_transcripts` | `summaries:read` | Browse the saved-source library with unchanged filters and next_cursor. |
| `get_saved_transcript` | `summaries:read` | Read saved source metadata (mode=metadata) or bounded content pages, following next_offset. |
| `mark_transcript_read` | `summaries:read` | Change the source's read state only when requested. |
<!-- /generated:tldw-tools -->

The prompts are `youtube_brief`, `summary_and_transcript` and
`claims_and_evidence`; each accepts one `url`. They prepare instructions for the
same analysis workflow rather than creating another billing product.

`search_videos` searches X posts with video, not YouTube. Each new search uses
one of the plan's monthly searches, and the count resets each billing period;
`usage.searches_remaining` in the response and in `account_usage` shows what is
left. Check `video.over_plan_limit`, then pass a chosen result's `url` to
`analyze_media`.

`transcription` and `force_asr`: do not set; the server decides. Developers can
override these options through the SDK. A user-authorized `max_credits` bounds
spending; it does not grant a plan feature or bypass source restrictions.
Do not infer privileges from an account name, role or credential prefix.
