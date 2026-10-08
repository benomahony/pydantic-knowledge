from __future__ import annotations

from pydantic_knowledge import (
    AudienceProfile,
    Depth,
    DocsContext,
    Experience,
    Intent,
    Preference,
    compose,
    concept,
    definition,
    example,
    failure,
)


def test_fix_context_prefers_failure_blocks() -> None:
    c = concept(
        "output",
        "Output",
        "Output",
        definition("def", "definition", weight=2),
        failure("fail", "failure", intents=[Intent.FIX], weight=5),
        example("build", "x = 1", intents=[Intent.BUILD]),
    )
    blocks = compose(c, DocsContext(intent=Intent.FIX))
    ids = [b.id for b in blocks]
    assert "fail" in ids
    assert "build" not in ids


def test_quick_context_limits_blocks() -> None:
    c = concept("x", "X", "X", *(definition(str(i), str(i)) for i in range(10)))
    ctx = DocsContext(
        audience=AudienceProfile(
            pydantic_ai=Experience.EXPERT,
            ai_engineering=Experience.EXPERT,
            preference=Preference.REFERENCE,
            depth=Depth.QUICK,
        )
    )
    assert len(compose(c, ctx)) == 3
