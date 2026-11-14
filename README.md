# tldw.sh portable agent skill

A portable instruction package for source-grounded media analysis through the
user's existing tldw REST, MCP or CLI connection. It does not contain an API key,
run a local video processor, create a service account or establish a connection
by itself. The reviewed entry point is [SKILL.md](SKILL.md), with workflow and
source-coverage references beside it.

This private repository is an exported snapshot of
[`tldwdotsh/tldw`](https://github.com/tldwdotsh/tldw), directory
`packages/agent-skill/tldw`. The monorepo remains canonical until an independent
release/synchronization workflow is approved and documented. Private clones
require GitHub organization access through your credential manager or authorized
SSH key. Never embed tokens in clone URLs or repository files.

## Validate and build offline

Use Python 3.10 or newer from this repository's root:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output dist
```

No external dependencies, monorepo checkout, model key or network request is
required. The validator checks the identity/version, the five-resource allowlist,
SHA-256 hashes, local Markdown links, JSON examples, and agent-interface metadata.
Tests cover deterministic packaging and reject changed, missing and symlinked
resources. The builder writes `dist/tldw-skill-0.2.5.zip` and its checksum manifest.
CI performs only these validations, with read-only repository permissions and no
registry credentials, publication, deployment or inference.

## Install the reviewed skill

After obtaining organization access, inspect the files before placing this repo
at a skill directory recognized by your host. For example, a project-local Codex
installation can use `.agents/skills/tldw/`, with `SKILL.md` directly inside it.
The built ZIP has a single `tldw/` root for the same layout. Other hosts have their
own discovery and trust rules; a portable format does not prove universal support
or store approval. The package's `agents/openai.yaml` supplies optional interface
metadata; the Markdown entry remains the instruction source.

Use one existing authenticated connection. The service's `/agents` page provides
its current key/OAuth onboarding and client downloads. Keep customer credentials
in the host's secret store or private environment. Never automate human
verification, paste tokens into chat, or give an agent operator credentials.

The skill preserves custom instructions, durable job receipts and exact
idempotent retries. Default caption/text processing uses 1 credit/minute; fresh
transcription costs 3 and needs server-authorized access and explicit permission.
Ordinary paid accounts must supply a ceiling; authenticated server-confirmed
exempt accounts may omit it. Resource and provider safety limits still apply. Free monthly credits do not enable fresh transcription, and
purchased credits never silently authorize it. Read the live service policy and
account usage before processing.

## Provenance and synchronization

`skill.json` identifies the reviewed resources and their hashes.
`EXPORT_MANIFEST.json` records the canonical source snapshot and repository
export. Review changes in the canonical monorepo, refresh the copied skill and
its manifest together, then rerun validation and tests. Do not silently diverge
or overwrite independent edits. This private GitHub repository is not a public
skill-directory listing or an npm/PyPI release.

Maintainer note: the skill deliberately contains no registry installation
instructions and no "check the registry" step, because the npm scope and PyPI
project names for the clients are not yet verified as owned by this project.
Agents install the CLI/SDKs only from the operator's download URL after a SHA-256
check. `scripts/validate.py` rejects registry wording. Registry instructions may
return only after both names are claimed and a first release is published by
this project.
