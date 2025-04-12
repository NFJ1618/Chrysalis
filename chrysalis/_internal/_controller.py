from collections.abc import Callable

from chrysalis._internal._relation import KnowledgeBase
from chrysalis._internal._search import SearchSpace, SearchStrategy

_CURRENT_KNOWLEDGE_BASE: KnowledgeBase | None = None
"""
The current knowledge space for the module.

It is possible to "hack" the module to create a single source of truth knowledge base.
This allows repeated calls to `register` to add relations the same knowledge base
and for the knowledge base to be reset. It is important that this global variable start
uninitialized so that its generic can be specified at run time.
"""


def new_knowledge_base() -> None:
    """Initialize a new knowledge base for the module."""
    global _CURRENT_KNOWLEDGE_BASE  # NOQA: PLW0603
    _CURRENT_KNOWLEDGE_BASE = KnowledgeBase()


def register[T, R](
    transformation: Callable[[T], T],
    invariant: Callable[[R, R], bool],
) -> None:
    """Register a metamorphic relation into the current knowledge base."""
    global _CURRENT_KNOWLEDGE_BASE  # NOQA: PLW0603
    if _CURRENT_KNOWLEDGE_BASE is None:
        _CURRENT_KNOWLEDGE_BASE = KnowledgeBase()

    _CURRENT_KNOWLEDGE_BASE.register(
        transformation=transformation,
        invariant=invariant,
    )


def run[T, R](
    sut: Callable[[T], R],  # NOQA: ARG001
    dataset: list[R],  # NOQA: ARG001
    search_strategy: SearchStrategy = SearchStrategy.RANDOM,
    chain_length: int = 10,
    num_chains: int = 10,
) -> None:
    """
    Run metamorphic testing on the SUT using previously registered relations.

    Parameter
    ---------
    sut : Callable[[T], R]
        The 'system under test' that is currenting being tested.
    dataset : Callable[[T], R]
        The input data to be transformed and used as input into the SUT.
    search_strategy : SearchStrategy, optional
        The search strategy to use when generating metamorphic relation chains. The
        serach strategy defaults to `SearchStrategy.RANDDOM`.
    chain_length : int, optional
        The number of relations in each generated metamorphic relation chain. The chain
        length defaults to 10.
    num_chains : int, optional
        The number of metamorphic chains to generate. The number of chains defaults to
        10.
    """
    if _CURRENT_KNOWLEDGE_BASE is None:
        raise RuntimeError(
            "No metamorphic relations have been registered in the current session, exiting."
        )
    search_space = SearchSpace(
        knowledge_base=_CURRENT_KNOWLEDGE_BASE,
        strategy=search_strategy,
        chain_length=chain_length,
    )
    search_space.generate_chains(num_chains=num_chains)
