import argparse
import ast
import hashlib
import json
import re
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Snapshot local Pydantic AI source documentation without summarising it."
)
parser.add_argument("repository", type=Path)
args = parser.parse_args()
source = args.repository.resolve()
dest = Path(__file__).with_name("pydantic_ai_content")
shutil.copytree(source / "docs", dest, dirs_exist_ok=True)
# Expand API directives from local source docstrings, without importing/executing upstream code.
modules = {}
for path in source.rglob("*.py"):
    parts = list(path.relative_to(source).parts)
    for i in range(len(parts) - 1, -1, -1):
        part = parts[i]
        if part in ("pydantic_ai", "pydantic_ai_harness", "pydantic_evals", "pydantic_graph"):
            mod = ".".join(parts[i:]).removesuffix(".py").removesuffix(".__init__")
            modules[mod] = path
            break


def document(node, depth=2):
    doc = ast.get_docstring(node)
    chunks = []
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        if node.name.startswith("_"):
            return ""
        if isinstance(node, ast.ClassDef):
            sig = "class " + node.name
        else:
            sig = (
                ("async " if isinstance(node, ast.AsyncFunctionDef) else "")
                + "def "
                + node.name
                + "("
                + ast.unparse(node.args)
                + ")"
                + (" -> " + ast.unparse(node.returns) if node.returns else "")
            )
        chunks.append("#" * depth + " `" + node.name + "`\n\n```python\n" + sig + "\n```\n")
    if doc:
        chunks.append(doc)
    if isinstance(node, (ast.Module, ast.ClassDef)):
        for child in node.body:
            if isinstance(
                child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ) and ast.get_docstring(child):
                chunks.append(document(child, min(depth + 1, 6)))
            elif isinstance(child, ast.AnnAssign) and isinstance(node, ast.ClassDef):
                chunks.append("```python\n" + ast.unparse(child) + "\n```")
    return "\n\n".join(chunks)


def resolve(module, member=None, seen=None):
    seen = seen or set()
    key = (module, member)
    if key in seen:
        return None
    seen.add(key)
    file = modules.get(module)
    if file is None:
        parent, _, name = module.rpartition(".")
        return resolve(parent, name, seen) if parent else None
    tree = ast.parse(file.read_text())
    if member is None:
        return tree
    for node in tree.body:
        if getattr(node, "name", None) == member:
            return node
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == member for t in targets):
                return node
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if (alias.asname or alias.name) != member:
                    continue
                if node.level:
                    parent = module if file.name == "__init__.py" else module.rpartition(".")[0]
                    levels = parent.split(".")
                    base = ".".join(levels[: len(levels) - node.level + 1])
                    target = base + ("." + node.module if node.module else "")
                else:
                    target = node.module or ""
                result = resolve(target, alias.name, seen)
                if result is not None:
                    return result
    return None


expanded = 0
unresolved = []
for path in dest.rglob("*.md"):
    text = path.read_text()
    if ":::" not in text:
        continue

    def expand(match):
        global expanded
        module = match[1]
        node = resolve(module)
        if node is None:
            symbol = module.rsplit(".", 1)[-1]
            matches = []
            for candidate, file in modules.items():
                if candidate.startswith(module.split(".")[0] + "."):
                    tree = ast.parse(file.read_text())
                    matches.extend(n for n in tree.body if getattr(n, "name", None) == symbol)
            if len(matches) == 1:
                node = matches[0]
        if node is not None:
            expanded += 1
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                return "```python\n" + ast.unparse(node) + "\n```"
            return document(node)
        unresolved.append(module)
        return f"API reference: [{module}](https://ai.pydantic.dev/api/)\n\n<!-- unresolved source directive: {module} -->"

    text = re.sub(r"^::: ([\w.]+)\n(?:[ \t]+[^\n]*\n|\n)*", expand, text, flags=re.M)
    path.write_text(text)
files = [p for p in (source / "docs").rglob("*.md") if p.name not in {"AGENTS.md", "CLAUDE.md"}]
Path(__file__).with_name("SNAPSHOT.json").write_text(
    json.dumps(
        {
            "source": str(source),
            "published_markdown_pages": len(files),
            "api_directives_expanded": expanded,
            "unresolved_api_directives": unresolved,
            "source_sha256": {
                str(p.relative_to(source / "docs")): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in files
            },
        },
        indent=2,
    )
    + "\n"
)
# Preserve upstream licence with the vendored example corpus.
for name in ("LICENSE", "LICENSE.md"):
    if (source / name).exists():
        shutil.copy2(source / name, dest / "UPSTREAM-LICENSE")
        break
print(
    len(files),
    "published pages;",
    expanded,
    "API directives expanded;",
    len(unresolved),
    "unresolved",
)
