# Source coverage and failures

- YouTube/TikTok analysis uses accessible captions or transcribed speech. Local
  transcription is an operator option, not a customer credential requirement.
  On-screen text, slides and other unseen visual evidence are not analyzed.
- A normal X URL retrieves the supplied post and available attached-video captions
  or attached Article when supported. Use `scope:post` for post text alone. X video
  captions are billed by video duration and include timed source blocks; missing
  captions fail instead of silently analyzing the tweet text. Complete thread/article retrieval is
  deployment-dependent; use full supplied text when content is missing. A title,
  preview or one tweet is not a complete article or thread.
- TikTok comparison is analysis of supplied clips. It does not discover all
  current platform trends or obtain view counts, audience metrics or comments.
- Private, removed, age-restricted or platform-blocked content can fail. Do not
  bypass access controls, invent a transcript or present unavailable content as read.

Request a translated summary through `instructions`, such as `Summarize the spoken
content in Spanish.` Translation produces text in the same analysis schema;
original captions remain unchanged. It does not produce dubbed audio, translated
video or translated subtitle files. X audio transcription is not enabled, even
with `transcription=if_needed`. Do not enable it to retry an X caption failure.

Use the returned error code, reference ID and limitations to explain the failure.
For `TOKEN_SCOPE_REQUIRED`, identify the returned `required_scope`. For
`HUMAN_VERIFICATION_REQUIRED`, `SIGNUP_REQUIRED` or `TRIAL_ACTIVATION_REQUIRED`,
send the owner to their web app. For `TRIAL_EXHAUSTED` or `QUOTA_EXCEEDED`, explain
the balance/limit and wait for the owner's decision. For `RATE_LIMITED`, honor
`Retry-After` with bounded backoff and retain the original work ID.

Terminal source failures require a deliberate new attempt or caller-supplied
source text. Admission attempts and provider costs can apply even when a failed
job releases processing reservations; avoid repeated blind submissions.


Server-confirmed billing exemption: the authenticated server decides whether an account is exempt. Exempt accounts may omit a credit ceiling and do not incur customer-credit charges; explicit transcription permission and resource/provider limits still apply. Ordinary paid accounts allowing fresh transcription must supply a ceiling or receive `TRANSCRIPTION_NOT_ALLOWED` (HTTP 422); `MAX_CREDITS_EXCEEDED` (HTTP 422) means a supplied ceiling is invalid or below the required charge. Clients validate supplied values, then pass requests through without fetching extra account scopes or inferring privileges from names, roles, or key prefixes.
