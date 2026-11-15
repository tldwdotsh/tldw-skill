# Source coverage

- YouTube uses available captions or eligible audio transcription.
  Private, members-only, age-restricted, removed or region-restricted media may
  be unavailable. Live streams must end before processing.
- A public X URL defaults to `scope:auto`: one attached video, the complete
  attached Article, or the post's text. Video captions keep their timestamps and
  use actual media duration. Inaccessible video speech is not replaced with
  post text. Multiple attached videos and incomplete sources fail explicitly.
- `scope:post` reads post text alone. `scope:thread` requests a bounded connected
  thread by the original author, not the entire reply discussion. An Article ID
  alone is insufficient; use its sharing post or supply complete text.
- YouTube reuses usable saved transcripts. X text and Article sources
  can be reused for up to 24 hours. `refresh_source=true` requests current source
  content; it does not grant audio permissions or change the user's budget.
- Summary instructions can request translated text. Original source text stays
  saved separately; the service does not inspect unseen visuals or produce
  dubbed audio, translated video or translated subtitle files.
- Original-source reads return normalized saved text and available timestamps.
  They do not return original subtitle-file bytes or guarantee word-perfect
  speech recognition. Quoting source requires the saved transcript, not the
  generated summary.
- Newly transcribed audio becomes readable after the job successfully settles.
  Failure or cancellation releases its hold and leaves unpaid ASR unavailable.
  Previously completed saved sources remain readable without a new charge.

Read live account limits with `account_usage`. Free uses captions, text and
saved transcripts. Audio requires an eligible plan and enabled platform.
Hobby is the paid launch offer; existing Pro accounts keep their plan eligibility.
Source-duration, concurrent-job, request-attempt, provider-budget and X video
search limits can still prevent work. Follow the returned error rather than
creating replacement accounts, rotating keys to evade limits or repeatedly
resubmitting.

## YouTube discovery metadata

Local `ytsearch5` returns up to five candidate videos, not their spoken content.
Flat results may omit title, channel, duration, upload date or other fields;
missing and `null` values are unknown. They do not establish captions, source
availability, plan eligibility or a final processing charge. Do not quote a
description as speech or invent a duration/date to fill a table.

There is no tldw-hosted YouTube search or search pagination contract. The local
JSON is dated discovery evidence, not a saved transcript. For the command, JSON
shape, presentation rules and selected-link handoff, read
[Find YouTube videos](workflows.md#find-youtube-videos). Only a successfully
processed source supplies the saved text and timestamps used for source-grounded
answers.
