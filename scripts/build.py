"""Build a deterministic, allowlisted skill ZIP without publication or credentials."""

# The docstring above is also the --help description.
# Usage: python3 scripts/build.py [--output DIR]   (default: dist/)

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

# Works both inside the ``scripts`` package (python -m scripts.build, and the
# tests) and as a plain script (python3 scripts/build.py).
if __package__:
    from .validate import ROOT, validate
else:
    from validate import ROOT, validate


def build(destination, root=ROOT):
    """Validate the skill at ``root``, then write its ZIP and release manifest.

    Writes ``tldw-skill-<version>.zip``, holding only the files listed in
    ``skill.json`` under a top-level ``tldw/`` folder, and
    ``skill-release.json`` (the ZIP's SHA-256 and size plus per-file hashes)
    into ``destination``. Entries are sorted and use a fixed timestamp and
    permissions, so the same skill always produces a byte-identical ZIP.

    Returns:
        dict: The release record written to ``skill-release.json``.

    Raises:
        ValueError: When validation fails; nothing is written then.
    """
    manifest, files = validate(root)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo("tldw/" + name, (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            # A regular file (S_IFREG) readable by everyone.
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    data = output.getvalue()
    name = "tldw-skill-" + manifest["version"] + ".zip"
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / name).write_bytes(data)
    release = {
        "schema_version": 1,
        "name": manifest["name"],
        "version": manifest["version"],
        "file": name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "files": manifest["files"],
        "credentials_included": False,
        "registry_published": False,
    }
    (destination / "skill-release.json").write_text(json.dumps(release, indent=2) + "\n")
    return release


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    print(json.dumps(build(args.output)))
