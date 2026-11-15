# tldw skill

Connect your agent to tldw.sh to analyze public video, retrieve saved summaries
and transcripts, and check usage. Start with [the setup guide](https://tldw.sh/agents).

The entry point is [SKILL.md](SKILL.md). The `references/` directory contains
tool, workflow, setup, source-limit and error guidance.

Hosted video search finds X videos. For YouTube discovery, the skill explains
how to install yt-dlp with an isolated tool environment, run a bounded metadata
search, read its JSON and present candidate links before submitting a selection
to the same analysis API/MCP tool. See [setup](references/setup.md#youtube-discovery-tool)
and [the YouTube workflow](references/workflows.md#find-youtube-videos).

With filesystem access, the agent saves search results, durable job receipts,
summaries and bounded transcript pages in private workspace `.tldw/` files.
It reuses saved results for follow-ups and resumes accepted jobs by ID. The
SDK and MCP transport do not automatically write these files.

One analysis saves generated output and original source. Reading saved source is
free of processing charges; starting an analysis uses normal credits. Saved
transcripts contain normalized captions, recognized speech or supplied text,
with source timestamps where available. Accuracy follows that source rather than
a word-perfect transcription guarantee.

Validate and build locally, without credentials or network requests:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests
python3 scripts/build.py
```

The build writes a deterministic ZIP and release manifest to `dist/`.
Versioned downloads are listed on https://tldw.sh/agents.
