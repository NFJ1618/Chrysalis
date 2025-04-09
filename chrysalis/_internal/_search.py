import random
from enum import Enum

from chrysalis._internal._relation import KnowledgeBase, Relation


class SearchStrategy(Enum):
    """Possible search strategies when creating metamorphic relation chains."""

    RANDOM = 1
    EXHAUSTIVE = 2
    DYNAMIC = 3


class SearchSpace:
    """A handle to interact with the search space for a knowledge base."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        strategy: SearchStrategy = SearchStrategy.RANDOM,
        num_links: int = 10,
    ):
        self._knowledge_base = knowledge_base
        self._strategy = strategy
        self._num_links = num_links

    def generate_chains(self, num_tests: int) -> list[list[Relation]]:
        """Generate metamorphic chains based on search strategy."""
        match self._strategy:
            case SearchStrategy.RANDOM:
                orderings = [
                    random.choices(self._knowledge_base.relations, k=self._num_links)
                    for _ in range(num_tests)
                ]
            case SearchStrategy.EXHAUSTIVE:
                raise NotImplementedError
            case SearchStrategy.DYNAMIC:
                raise NotImplementedError

        return orderings
