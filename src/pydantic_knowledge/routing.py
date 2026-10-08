from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .compose import compose
from .models import DocsContext, KnowledgeBase

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _ngrams(text: str, n: int = 3) -> set[str]:
    clean = " ".join(_tokens(text))
    if len(clean) < n:
        return {clean} if clean else set()
    return {clean[i : i + n] for i in range(len(clean) - n + 1)}


def _concept_text(kb: KnowledgeBase, concept_id: str) -> str:
    concept = kb.concept(concept_id)
    route_hints = [r.route_when or "" for r in kb.relationships if r.target == concept_id]
    return " ".join([concept.title, concept.summary, *sorted(concept.aliases), *route_hints])


def _candidates(kb: KnowledgeBase, current_concept: str | None) -> tuple[str, ...]:
    if current_concept is None:
        return tuple(c.id for c in kb.concepts if not c.show_ontology)
    neighbours: list[str] = []
    for relation in kb.relationships:
        if relation.source == current_concept:
            neighbours.append(relation.target)
        elif relation.target == current_concept:
            neighbours.append(relation.source)
    return tuple(dict.fromkeys(neighbours)) or tuple(
        c.id for c in kb.concepts if not c.show_ontology
    )


def token_overlap(query: str, candidate: str) -> float:
    q = Counter(_tokens(query))
    c = Counter(_tokens(candidate))
    if not q or not c:
        return 0.0
    overlap = sum((q & c).values())
    return overlap / math.sqrt(sum(q.values()) * sum(c.values()))


def char_ngram(query: str, candidate: str) -> float:
    q, c = _ngrams(query), _ngrams(candidate)
    if not q or not c:
        return 0.0
    return len(q & c) / len(q | c)


def hybrid_score(query: str, candidate: str) -> float:
    return 0.7 * token_overlap(query, candidate) + 0.3 * char_ngram(query, candidate)


Scorer = Callable[[str, str], float]
SCORERS: dict[str, Scorer] = {
    "token": token_overlap,
    "char_ngram": char_ngram,
    "hybrid": hybrid_score,
}


@dataclass(frozen=True)
class Suggestion:
    concept_id: str
    score: float


def suggest_docs(
    kb: KnowledgeBase,
    phrase: str,
    *,
    current_concept: str | None = None,
    scorer: str | Scorer = "hybrid",
    limit: int = 3,
) -> tuple[Suggestion, ...]:
    score_fn = SCORERS[scorer] if isinstance(scorer, str) else scorer
    ranked = [
        Suggestion(concept_id=concept_id, score=score_fn(phrase, _concept_text(kb, concept_id)))
        for concept_id in _candidates(kb, current_concept)
    ]
    ranked.sort(key=lambda x: (-x.score, x.concept_id))
    return tuple(ranked[: max(1, limit)])


def authored_answer(
    kb: KnowledgeBase,
    concept_ids: Iterable[str],
    *,
    context: DocsContext | None = None,
    max_blocks_per_concept: int = 3,
) -> str:
    context = context or DocsContext()
    parts: list[str] = []
    for concept_id in concept_ids:
        concept = kb.concept(concept_id)
        parts.append(concept.summary)
        for block in compose(concept, context)[:max_blocks_per_concept]:
            parts.append(block.body)
    return "\n\n".join(dict.fromkeys(parts))
