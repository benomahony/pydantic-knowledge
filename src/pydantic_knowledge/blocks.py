from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from .models import BlockKind, Depth, Experience, Intent, KnowledgeBlock, Preference

T = TypeVar("T")


def _set(value: Iterable[T] | None) -> frozenset[T]:
    return frozenset(value or ())


def block(
    id: str,
    body: str,
    *,
    kind: BlockKind,
    title: str | None = None,
    language: str | None = None,
    intents: Iterable[Intent] | None = None,
    experiences: Iterable[Experience] | None = None,
    preferences: Iterable[Preference] | None = None,
    depths: Iterable[Depth] | None = None,
    weight: int = 0,
) -> KnowledgeBlock:
    return KnowledgeBlock(
        id=id,
        kind=kind,
        title=title,
        body=body.strip(),
        language=language,
        intents=_set(intents),
        experiences=_set(experiences),
        preferences=_set(preferences),
        depths=_set(depths),
        weight=weight,
    )


def definition(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.DEFINITION, **kwargs)  # type: ignore[arg-type]


def mental_model(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.MENTAL_MODEL, **kwargs)  # type: ignore[arg-type]


def example(id: str, body: str, *, language: str = "python", **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.EXAMPLE, language=language, **kwargs)  # type: ignore[arg-type]


def procedure(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.PROCEDURE, **kwargs)  # type: ignore[arg-type]


def failure(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.FAILURE, **kwargs)  # type: ignore[arg-type]


def tradeoff(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.TRADEOFF, **kwargs)  # type: ignore[arg-type]


def reference(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.REFERENCE, **kwargs)  # type: ignore[arg-type]


def note(id: str, body: str, **kwargs: object) -> KnowledgeBlock:
    return block(id, body, kind=BlockKind.NOTE, **kwargs)  # type: ignore[arg-type]
