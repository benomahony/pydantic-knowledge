from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from .models import KnowledgeBase
from .renderer import BuildTarget, build
from .reports import write_eval_artifacts


def load_knowledge_base(path: Path) -> KnowledgeBase:
    spec = importlib.util.spec_from_file_location("pydantic_knowledge_user_docs", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    value = getattr(module, "DOCS", None)
    if not isinstance(value, KnowledgeBase):
        raise ValueError(f"{path} must define DOCS: KnowledgeBase")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(prog="pydantic-knowledge")
    sub = parser.add_subparsers(dest="command", required=True)
    build_cmd = sub.add_parser("build", help="Build static docs from Python-authored knowledge")
    build_cmd.add_argument("source", type=Path)
    build_cmd.add_argument(
        "--target",
        choices=[target.value for target in BuildTarget],
        default=BuildTarget.SITE.value,
        help="site (default), offline multi-page, or single-file export",
    )
    build_cmd.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory for site/offline or HTML path for single",
    )
    eval_cmd = sub.add_parser("eval", help="Build routing eval artifacts from JTBD examples")
    eval_cmd.add_argument("source", type=Path)
    eval_cmd.add_argument("--out", type=Path, default=Path("eval-results"))

    args = parser.parse_args()

    if args.command == "build":
        kb = load_knowledge_base(args.source)
        target = BuildTarget(args.target)
        output = args.out or (
            Path("site") if target is not BuildTarget.SINGLE else Path("docs.html")
        )
        result = build(kb, output, target=target)
        print(result)
    elif args.command == "eval":
        kb = load_knowledge_base(args.source)
        print(write_eval_artifacts(kb, args.out))


if __name__ == "__main__":
    main()
