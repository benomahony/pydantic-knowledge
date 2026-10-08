"""Import complete Markdown pages without summarising or dropping source content."""

from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path
from urllib.parse import urljoin

import yaml

from .models import BlockKind, Concept, KnowledgeBlock


def chunk_markdown(text: str, *, heading_level: int = 2) -> tuple[tuple[str, str], ...]:
    """Split at headings outside fenced code, preserving every source character.

    A chunk consists of its heading and all subsections until the next heading
    at this level. Introductory content is kept as its own chunk.
    """
    if not 1 <= heading_level <= 6:
        raise ValueError("heading_level must be between 1 and 6")
    sections = []
    lines = []
    title = "Introduction"
    fence = None
    heading = re.compile(r"^ {0,3}" + "#" * heading_level + r"(?!#)\s+(.+?)(?:\s+\{#.*?\})?\s*$")
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
        match = heading.match(line) if fence is None else None
        if match and lines:
            sections.append((title, "".join(lines)))
            lines = []
        if match:
            title = match[1].strip("` ")
        lines.append(line)
    if lines:
        sections.append((title, "".join(lines)))
    return tuple(sections)


def _outside_fences(text: str, transform) -> str:
    """Apply a prose transform everywhere except inside fenced code blocks."""
    out, prose, fence = [], [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence is None and marker:
            out.append(transform("".join(prose)))
            prose, fence = [], marker[1]
            out.append(line)
        elif fence is not None:
            out.append(line)
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
        else:
            prose.append(line)
    out.append(transform("".join(prose)))
    return "".join(out)


def import_markdown_directory(
    directory: str | Path,
    *,
    base_url: str,
    ids: dict[str, str] | None = None,
    titles: dict[str, str] | None = None,
    routes: dict[str, str] | None = None,
) -> tuple[Concept, ...]:
    """Read every published Markdown page; AGENTS.md is repository guidance, not a page."""
    root = Path(directory)
    paths = sorted(p for p in root.rglob("*.md") if p.name not in {"AGENTS.md", "CLAUDE.md"})
    mapping = {
        p.relative_to(root).as_posix(): "reference-"
        + re.sub(r"[^a-zA-Z0-9_-]", "-", p.relative_to(root).with_suffix("").as_posix())
        for p in paths
    }
    mapping.update(ids or {})
    api_modules = {}
    for page in paths:
        header = re.search(r"^#\s+`?([a-zA-Z_]+[\w.]*)`?\s*$", page.read_text(), re.MULTILINE)
        if header and "." in header[1]:
            api_modules[header[1]] = mapping[page.relative_to(root).as_posix()]

    def api_link(match: re.Match) -> str:
        label, symbol = match[1], match[2]
        module = next(
            (
                name
                for name in sorted(api_modules, key=len, reverse=True)
                if symbol == name or symbol.startswith(name + ".")
            ),
            None,
        )
        if module:
            return f"[{label}](knowledge:{api_modules[module]})"
        if symbol.startswith("pydantic_ai."):
            return f"[{label}](knowledge:{mapping.get('api/agent.md', '')})"
        # References to other projects' API docs cannot be resolved locally; keep the label.
        return label

    titles, routes = titles or {}, routes or {}
    concepts = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        original = path.read_text(encoding="utf-8")
        text = original
        meta = {}
        if text.startswith("---\n"):
            pieces = text.split("---", 2)
            if len(pieces) == 3:
                meta = yaml.safe_load(pieces[1]) or {}
                text = pieces[2].lstrip()
        heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = titles.get(relative) or (
            heading[1].strip("`") if heading else path.stem.replace("-", " ").title()
        )
        summary = meta.get("description", "")
        if heading:
            text = text[: heading.start()] + text[heading.end() :].lstrip("\n")

        def link(match: re.Match, path: Path = path) -> str:
            target = match[2]
            if ":" in target or target.startswith(("#", "//")):
                return match[0]
            filename, _, fragment = target.partition("#")
            resolved = (path.parent / filename).resolve()
            try:
                key = resolved.relative_to(root.resolve()).as_posix()
            except ValueError:
                return f"[{match[1]}]({urljoin(base_url, target)})"
            if key in mapping:
                return (
                    f"[{match[1]}](knowledge:{mapping[key]}"
                    + (f"#{fragment}" if fragment else "")
                    + ")"
                )
            return f"[{match[1]}]({urljoin(base_url, key)})"

        def local_media(target: str, path: Path = path) -> str:
            if ":" in target or target.startswith("//"):
                return target
            file = (path.parent / target).resolve()
            if not file.is_relative_to(root.resolve()) or not file.is_file():
                return target
            mime = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
            return "data:" + mime + ";base64," + base64.b64encode(file.read_bytes()).decode()

        text = re.sub(
            r"!\[([^\]]*)\]\(([^\s)]+)\)", lambda m: f"![{m[1]}]({local_media(m[2])})", text
        )
        text = re.sub(
            r'(<(?:img|video|audio|source)\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])',
            lambda m: m[1] + local_media(m[2]) + m[3],
            text,
        )
        text = _outside_fences(
            text,
            lambda prose: re.sub(
                r"\[([^\]]+)\]\[([\w.]+)\]",
                api_link,
                re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", link, prose),
            ),
        )
        concepts.append(
            Concept(
                id=mapping[relative],
                title=title,
                summary=str(summary),
                hide_title=bool(meta.get("hideTitle", False)),
                source_url=urljoin(
                    base_url, routes.get(relative, relative.removesuffix(".md")) + "/"
                ),
                domain=(path.relative_to(root).parent.as_posix() or "Overview").replace(
                    ".", "Overview"
                ),
                blocks=tuple(
                    KnowledgeBlock(
                        id=f"{mapping[relative]}.section.{index}",
                        kind=BlockKind.REFERENCE,
                        title=section_title,
                        body=body,
                        format="markdown",
                    )
                    for index, (section_title, body) in enumerate(chunk_markdown(text))
                ),
            )
        )
    return tuple(concepts)
