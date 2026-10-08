from __future__ import annotations

import pytest
from pydantic import ValidationError

from pydantic_knowledge import (
    Concept,
    KnowledgeBase,
    RelationKind,
    Relationship,
    concept,
    definition,
    docs,
)


def test_concept_ids_are_unique() -> None:
    c = concept("a", "A", "A", definition("a.def", "A"))
    with pytest.raises(ValidationError):
        KnowledgeBase(title="x", concepts=(c, c))


def test_relationship_targets_must_exist() -> None:
    c = concept("a", "A", "A")
    with pytest.raises(ValidationError):
        docs(
            "x",
            concepts=[c],
            relationships=[Relationship(source="a", target="missing", kind=RelationKind.USES)],
        )


def test_with_blocks_is_immutable() -> None:
    c = Concept(id="a", title="A", summary="A")
    c2 = c.with_blocks(definition("a.def", "definition"))
    assert c.blocks == ()
    assert len(c2.blocks) == 1
