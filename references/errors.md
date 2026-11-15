# Recover from an error

Keep the accepted job ID and inspect its final state. A source error does not
authorize a new job or a higher budget. An uncertain initial POST can be retried
with the exact same body and idempotency key. Respect `Retry-After` on throttled
reads and the job's polling hints.

These codes and HTTP statuses are validated against the API source. Live
machine-readable guidance is at https://tldw.sh/docs/errors.json.

<!-- generated:tldw-errors -->
| Error | HTTP | Recovery |
| --- | --- | --- |
| `UNAUTHENTICATED` | 401 | Check token expiry or revocation. Reconnect through the client; never print credentials. |
| `SESSION_REQUIRED` | 403 | This action requires the account owner's browser session. Direct them to the signed-in web app. |
| `TOKEN_SCOPE_REQUIRED` | 403 | Show details.required_scope to the owner. Do not broaden permissions automatically. |
| `SIGNUP_REQUIRED` | 403 | The owner must finish account enrollment in the web app. |
| `HUMAN_VERIFICATION_REQUIRED` | 403 | The owner must complete one-time human verification in the web app. Never automate or bypass it. |
| `TRIAL_ACTIVATION_REQUIRED` | 403 | Activate the account allowance once in the web app. |
| `TRIAL_PAUSED` | 403 | The free offer is paused. Show the available plans to the owner without changing plans. |
| `QUOTA_EXCEEDED` | 402 | Check account usage and reserved credits. Show details.upgrade.billing_url or wait for the reset; do not purchase anything. |
| `SEARCH_QUOTA_EXCEEDED` | 402 | The plan's monthly X video searches are used up; the count resets when the next billing period starts. Show details.upgrade.billing_url to the owner when present; do not retry or purchase anything. |
| `VIDEO_TOO_LONG` | 422 | Compare details.duration_minutes with details.limit_minutes. Show the available upgrade; do not resubmit the same source. |
| `PLAN_FEATURE_REQUIRED` | 403 | Show the plan requirement and details.upgrade.billing_url to the account owner. |
| `ASR_REQUIRES_UPGRADE` | 403 | The account cannot transcribe this source. Show the plan requirement or accept complete source text from the user. |
| `TRANSCRIPTION_NOT_ALLOWED` | 422 | Read details.reason and the account's enabled platforms. Explain the limitation; do not change transcription options or resubmit automatically. |
| `MAX_CREDITS_EXCEEDED` | 402, 422 | The ceiling is invalid or below the required charge. Ask the owner before increasing it; preserve the original job or request. |
| `DUPLICATE_ACTIVE_JOB` | 409 | Find and follow the existing job rather than submitting another copy. |
| `RATE_LIMITED` | 429 | Honor Retry-After and the existing job's polling hint. Retry an uncertain POST only with the exact original body and idempotency key. |
| `IDEMPOTENCY_CONFLICT` | 409 | The key belongs to another request body. Recover the original job or use a new key only for newly authorized work. |
| `SOURCE_UNAVAILABLE` | 422 | Explain the unavailable or incomplete source. Accept complete source text if the user supplies it; never pretend missing content was read. |
| `UNSUPPORTED_CONTENT` | 422 | Explain the unsupported source type and request a supported source or complete text. |
| `VIDEO_PRIVATE` | 422 | The source requires access the service does not have. Do not request passwords or private cookies. |
| `VIDEO_MEMBERS_ONLY` | 422 | Members-only video is unavailable. Request authorized source text instead. |
| `VIDEO_AGE_RESTRICTED` | 422 | Age-restricted video is unavailable. Request authorized source text instead. |
| `VIDEO_UNAVAILABLE` | 422 | The source may be removed or region restricted. Do not repeatedly resubmit. |
| `LIVE_NOT_SUPPORTED` | 422 | Wait until the live stream has ended before requesting a new analysis. |
| `NO_SPEECH_DETECTED` | 422 | Explain that usable speech was not detected. Do not invent a transcript. |
| `FEATURE_DISABLED` | 422, 503 | This feature is off on this deployment. Explain that it is unavailable; do not retry automatically. |
| `PLATFORM_BLOCKED` | 503 | The source platform is blocking retrieval. Try later only when the user authorizes a new attempt. |
| `SUBTITLE_PARSE_ERROR` | 422 | The captions could not be read. Explain the source failure; do not invent missing text or automatically start another job. |
| `TRANSCRIPT_TOO_LONG` | 422 | The available transcript exceeds the supported limit. Ask the user to select a shorter source or supply a bounded excerpt. |
| `INVALID_URL` | 400 | Ask for a supported YouTube or public X link, or complete supplied text. Do not guess the source. |
| `UNSUPPORTED_PLATFORM` | 400 | Use a supported source or complete text provided by the user. Do not substitute an unrelated link. |
| `VALIDATION_ERROR` | 409, 422 | Correct the rejected fields using the documented schema; do not raise a spending ceiling without user authorization. |
| `NOT_FOUND` | 404 | Check the existing job and its own source IDs. New audio transcripts require successful completion; do not guess other IDs. |
| `ACCOUNT_UNAVAILABLE` | 403 | Stop and direct the account owner to support. Rotating credentials or creating another account does not resolve account suspension. |
| `SPEND_LIMIT_REACHED` | 503 | The service or account provider budget refused this call. Stop automatic retries; preserve the job/key and wait for capacity or owner support guidance. |
| `SOURCE_FETCH_FAILED` | 503 | The source provider could not complete retrieval. Preserve the request/key and explain the failure; do not start new analyses automatically. |
| `BILLING_UNAVAILABLE` | 503 | Billing reconciliation is temporarily unavailable. Use bounded retries for the same read or stable-key request; do not buy credits or resubmit another job. |
| `BILLING_CONFIGURATION_ERROR` | 503 | Stop retries and direct the account owner to support for billing configuration review. |
<!-- /generated:tldw-errors -->
