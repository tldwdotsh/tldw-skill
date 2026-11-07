# Source coverage and failures

- YouTube/TikTok analysis uses accessible captions or transcribed speech. Local
  transcription is an operator option, not a customer credential requirement.
  On-screen text, slides and other unseen visual evidence are not analyzed.
- A normal X URL retrieves one public post. Complete thread/article retrieval is
  deployment-dependent; use full supplied text when content is missing. A title,
  preview or one tweet is not a complete article or thread.
- TikTok comparison is analysis of supplied clips. It does not discover all
  current platform trends or obtain view counts, audience metrics or comments.
- Private, removed, age-restricted or platform-blocked content can fail. Do not
  bypass access controls, invent a transcript or present unavailable content as read.

Use the returned error code, reference ID and limitations to explain the failure.
For `TOKEN_SCOPE_REQUIRED`, identify the returned `required_scope`. For
`HUMAN_VERIFICATION_REQUIRED`, `SIGNUP_REQUIRED` or `TRIAL_ACTIVATION_REQUIRED`,
send the owner to their web app. For `TRIAL_EXHAUSTED` or `QUOTA_EXCEEDED`, explain
the balance/limit and wait for the owner's decision. For `RATE_LIMITED`, honor
`Retry-After` with bounded backoff and retain the original work ID.

Terminal source failures require a deliberate new attempt or caller-supplied
source text. Admission attempts and provider costs can apply even when a failed
job releases processing reservations; avoid repeated blind submissions.
