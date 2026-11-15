# tldw skill

Connect your agent to tldw.sh to analyze public video, retrieve saved summaries
and transcripts, and check usage. Start with [the setup guide](https://tldw.sh/agents).

The entry point is [SKILL.md](SKILL.md). The `references/` directory contains
tool, workflow, setup, source-limit and error guidance.

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
