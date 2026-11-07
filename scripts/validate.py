"""Validate this skill's identity, resource hashes and local references offline."""

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = {
    "SKILL.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/workflows.md",
    "references/source-limits.md",
}
SECRET = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{24,}|tldw_[a-f0-9]{24}_[A-Za-z0-9_-]{43}|-----BEGIN .*PRIVATE KEY-----)"
)


def validate(root=ROOT):
    root = Path(root)
    manifest = json.loads((root / "skill.json").read_text())
    if (
        manifest.get("schema_version"),
        manifest.get("name"),
        manifest.get("version"),
        manifest.get("entry"),
        manifest.get("license"),
    ) != (1, "tldw", "0.2.0", "SKILL.md", "MIT"):
        raise ValueError("Skill manifest identity/version mismatch")
    if set(manifest.get("files", {})) != RESOURCES:
        raise ValueError("Skill resource allowlist mismatch")
    contents = {}
    for name, expected in manifest["files"].items():
        relative = PurePosixPath(name)
        path = root / name
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or path.is_symlink()
            or not path.is_file()
            or path.stat().st_size > 100_000
        ):
            raise ValueError("Missing or unsafe skill resource")
        if any((root / parent).is_symlink() for parent in relative.parents if str(parent) != "."):
            raise ValueError("Symlinked skill directory")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError("Skill resource checksum mismatch")
        text = content.decode("utf-8")
        if "[TODO:" in text or SECRET.search(text):
            raise ValueError("Unfinished scaffold or likely credential")
        contents[name] = content
        if name.endswith(".md"):
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                target = target.split("#", 1)[0]
                linked = (path.parent / target).resolve()
                if not linked.is_relative_to(root.resolve()) or not linked.is_file():
                    raise ValueError("Broken or escaping local Markdown reference")
            for block in re.findall(r"```json\n([\s\S]*?)```", text):
                json.loads(block)
    entry = contents["SKILL.md"].decode()
    if not entry.startswith("---\nname: tldw\n") or 'version: "0.2.0"' not in entry:
        raise ValueError("Skill frontmatter identity/version mismatch")
    description = re.search(r"^description: (.+)$", entry, re.MULTILINE)
    if not description or not 1 <= len(description[1]) <= 1024:
        raise ValueError("Missing or oversized skill description")
    agent = contents["agents/openai.yaml"].decode()
    if not agent.startswith("interface:\n") or "$tldw" not in agent:
        raise ValueError("Invalid agent interface metadata")
    return manifest, contents


if __name__ == "__main__":
    manifest, contents = validate()
    print(
        json.dumps(
            {
                "valid": True,
                "name": manifest["name"],
                "version": manifest["version"],
                "files": len(contents),
                "network_requests": 0,
            }
        )
    )
