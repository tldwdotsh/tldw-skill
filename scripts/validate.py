"""Validate the exported skill and all its local resources without network access.

``skill.json`` lists every skill file with its SHA-256. Validation checks
the manifest's identity (schema 1, name ``tldw``, entry ``SKILL.md``) and
that the required files are listed. Each listed file must be a regular,
non-symlink file of at most 100 KB inside the skill directory, and its
content must match its hash. Text must not contain unfinished scaffolding
or anything shaped like a tldw API key, relative Markdown links must point
to files inside the skill, and SKILL.md's front matter must start with
``name: tldw`` and declare the manifest's version.

Run ``python3 scripts/validate.py``: it prints a JSON summary, or raises
ValueError naming the first problem found.
"""

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

# The skill repository root (this file lives in scripts/).
ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    """Validate the skill at ``root``.

    Returns:
        ``(manifest, contents)``: the parsed ``skill.json`` and a dict mapping
        each listed file name to its bytes.

    Raises:
        ValueError: On the first failed check.
    """
    root = Path(root).resolve()
    manifest = json.loads((root / "skill.json").read_text())
    if (manifest.get("schema_version"), manifest.get("name"), manifest.get("entry")) != (
        1,
        "tldw",
        "SKILL.md",
    ):
        raise ValueError("Invalid skill identity")
    files = manifest.get("files", {})
    if not {"SKILL.md", "LICENSE", "agents/openai.yaml"}.issubset(files):
        raise ValueError("Missing required skill resources")
    contents = {}
    for name, expected in files.items():
        relative = PurePosixPath(name)
        path = root / name
        # Refuse absolute or parent-relative names, symlinks (the file or any
        # parent directory), files resolving outside the skill and files
        # over 100 KB.
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or path.is_symlink()
            or not path.is_file()
            or not path.resolve().is_relative_to(root)
            or any((root / parent).is_symlink() for parent in relative.parents)
            or path.stat().st_size > 100_000
        ):
            raise ValueError("Missing or unsafe skill resource")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError("Skill resource checksum mismatch")
        text = content.decode("utf-8")
        if "[TODO:" in text or re.search(r"tldw_[a-f0-9]{24}_[A-Za-z0-9_-]{43}", text):
            raise ValueError("Unfinished scaffold or credential")
        if name.endswith(".md"):
            # Relative links must resolve to files inside the skill; web links
            # and same-page anchors are skipped.
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                linked = (path.parent / target.split("#", 1)[0]).resolve()
                if not linked.is_relative_to(root) or not linked.is_file():
                    raise ValueError("Broken or escaping local Markdown reference")
        contents[name] = content
    entry = contents["SKILL.md"].decode()
    if not entry.startswith("---\nname: tldw\n") or not re.search(
        rf"^\s*version: [\"\']?{re.escape(manifest['version'])}[\"\']?$", entry, re.MULTILINE
    ):
        raise ValueError("Skill frontmatter version mismatch")
    return manifest, contents


if __name__ == "__main__":
    manifest, contents = validate()
    print(json.dumps({"valid": True, "version": manifest["version"], "files": len(contents)}))
