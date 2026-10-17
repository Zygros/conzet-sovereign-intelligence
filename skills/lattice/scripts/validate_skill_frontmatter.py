"""Small dependency-free validator for portable Agent Skills Markdown files."""
from __future__ import annotations
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def validate_skill_text(text: str, path: str = "SKILL.md") -> list[str]:
    errors = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [f"{path}: missing opening YAML frontmatter delimiter"]
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return [f"{path}: missing closing YAML frontmatter delimiter"]
    front = lines[1:end]
    fields = {}
    for line in front:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            errors.append(f"{path}: unsupported frontmatter line: {line!r}")
            continue
        key, value = match.groups()
        if key in fields:
            errors.append(f"{path}: duplicate frontmatter field {key}")
        fields[key] = value.strip().strip("\\\"").strip("\\'")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        errors.append(f"{path}: missing name field")
    elif not NAME_RE.fullmatch(name):
        errors.append(f"{path}: name must be lowercase hyphen-separated alphanumeric")
    if not description:
        errors.append(f"{path}: missing description field")
    elif len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    body = "\\n".join(lines[end + 1:]).strip()
    if not body:
        errors.append(f"{path}: missing skill instructions after frontmatter")
    return errors

def validate_tree(root: Path) -> tuple[int, list[str]]:
    paths = sorted(root.rglob("SKILL.md"))
    errors = []
    for path in paths:
        try:
            errors.extend(validate_skill_text(path.read_text(encoding="utf-8"), str(path)))
        except UnicodeDecodeError:
            errors.append(f"{path}: file is not valid UTF-8")
    return len(paths), errors

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    count, errors = validate_tree(args.root)
    print(json.dumps({"skills_checked": count, "error_count": len(errors), "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)