from __future__ import annotations

from .models import BlockKind, Concept, DocsContext, KnowledgeBlock

_KIND_ORDER = {
    BlockKind.DEFINITION: 0,
    BlockKind.MENTAL_MODEL: 1,
    BlockKind.PROCEDURE: 2,
    BlockKind.EXAMPLE: 3,
    BlockKind.FAILURE: 4,
    BlockKind.TRADEOFF: 5,
    BlockKind.NOTE: 6,
    BlockKind.REFERENCE: 7,
}


def compose(concept: Concept, context: DocsContext) -> tuple[KnowledgeBlock, ...]:
    scored = [(block.score(context), block) for block in concept.blocks]
    eligible = [(score, block) for score, block in scored if score >= -2]
    eligible.sort(key=lambda pair: (-pair[0], _KIND_ORDER[pair[1].kind], pair[1].id))

    limit = {"quick": 3, "normal": 6, "deep": 100}[context.audience.depth.value]
    chosen = eligible[:limit]

    # Preserve a coherent reading order after relevance has selected the blocks.
    chosen.sort(key=lambda pair: (_KIND_ORDER[pair[1].kind], -pair[0], pair[1].id))
    return tuple(block for _, block in chosen)
