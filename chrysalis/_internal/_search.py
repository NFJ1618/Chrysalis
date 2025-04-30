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
        chain_length: int = 10,
    ):
        self._knowledge_base = knowledge_base
        self._strategy = strategy
        self._chain_length = chain_length

    def generate_chains(self, num_chains: int) -> list[list[Relation]]:
        """Generate metamorphic chains based on search strategy."""
        match self._strategy:
            case SearchStrategy.RANDOM:
                orderings = [
                    random.choices(
                        list(self._knowledge_base.relations.values()),
                        k=self._chain_length,
                    )
                    for _ in range(num_chains)
                ]
            case SearchStrategy.EXHAUSTIVE:
                raise NotImplementedError
            case SearchStrategy.DYNAMIC:
                raise NotImplementedError

        return orderings
