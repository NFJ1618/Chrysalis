from collections import Counter
from collections.abc import Callable


class Relation[T]:
    """
    A relationship between input change and output change.

    Metamorphic relations are the fundamental building blocks of metamorphic testing.
    Each metamorphic relation consists of a transformation and an invariant. The
    transformation is a function that transforms the input data. The invariant is a
    conditional between the outputs of execution on the base input and transformed
    input.
    """

    def __init__(
        self,
        name: str,
        transformation: Callable[[T], T],
        invariant: Callable[[T, T], bool],
    ):
        self._name = name
        self._transformation = transformation
        self._invariant = invariant

    def apply(self, data: T) -> T:
        """Apply a relation's transformation."""
        return self._transformation(data)

    @property
    def name(self) -> str:
        return self._name


class KnowledgeBase[T]:
    """
    A collection of metamorphic relations.

    For unique naming purposes, a counter of unique relation names is kept. When a new
    relation is created, the name of the relation is stored in the `_names` counter.
    Subsequent relations registered with a duplicate name will have their corresponding
    count appended (the first relation counts as the zeroth relation).
    """

    def __init__(self) -> None:
        self._names = Counter[str]()
        self._relations: list[Relation[T]] = []

    def register(
        self,
        transformation: Callable[[T], T],
        invariant: Callable[[T, T], bool],
        name: str | None = None,
    ):
        """Register a relation into the knowledge base, ensuring the name is unique."""
        if name is None:
            name = transformation.__name__

        unique_name = f"{name}_{self._names[name]}" if name in self._names else name
        self._names[name] += 1

        self._relations.append(
            Relation(
                transformation=transformation,
                invariant=invariant,
                name=unique_name,
            )
        )

    @property
    def relations(self) -> list[Relation[T]]:
        """Return a list of all registered relations."""
        return self._relations
