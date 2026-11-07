"""Build a deterministic, allowlisted skill ZIP without publication or credentials."""

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

if __package__:
    from .validate import ROOT, validate
else:
    from validate import ROOT, validate


def build(destination, root=ROOT):
    manifest, files = validate(root)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo("tldw/" + name, (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
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
