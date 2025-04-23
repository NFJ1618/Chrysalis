from collections.abc import Callable

_LAMBDA_FUNCTION_NAME = "<lambda>"


class Relation[T, R]:
    """
    A relationship between input change and output change.

    Metamorphic relations are the fundamental building blocks of metamorphic testing.
    Each metamorphic relation consists of a transformation and invariants. The
    transformation is a function that transforms the input data. An invariant is a
    conditional between the outputs of execution on the base input and transformed
    input.
    """

    def __init__(
        self,
        transformation: Callable[[T], T],
    ):
        self._transformation = transformation
        self._invariants: set[Callable[[R, R], bool]] = set()

    def add_invariant(self, invariant: Callable[[R, R], bool]) -> None:
        """Add an invariant to a transformation to create a new relation pair."""
        self._invariants.add(invariant)

    def apply_transform(self, data: T) -> T:
        """Apply a relation's transformation."""
        return self._transformation(data)

    @property
    def transformation_name(self) -> str:
        return self._transformation.__name__

    @property
    def invariants(self) -> list[Callable[[R, R], bool]]:
        return list(self._invariants)


class KnowledgeBase[T, R]:
    """
    A collection of metamorphic relations.

    Relations are registered in (transformation, invariant) pairs. Under the hood, a
    relation stores single transformation and a list of invariants.

    Is it important to note that lambda functions cannot be used for transformations or
    invariants.
    """

    def __init__(self) -> None:
        self._relations: dict[str, Relation[T, R]] = {}

    def register(
        self,
        transformation: Callable[[T], T],
        invariant: Callable[[R, R], bool],
    ):
        """Register a relation into the knowledge base, ensuring the name is unique."""
        transform_name = transformation.__name__
        if _LAMBDA_FUNCTION_NAME in {transform_name, invariant.__name__}:
            raise ValueError(
                "Lambda functions cannot be used as transformation or invariants."
            )

        if transform_name not in self._relations:
            self._relations[transform_name] = Relation[T, R](transformation)
        self._relations[transform_name].add_invariant(invariant)

    @property
    def relations(self) -> list[Relation[T, R]]:
        """Return a list of all registered relations."""
        return list(self._relations.values())
