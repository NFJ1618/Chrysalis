from collections.abc import Callable

from chrysalis._internal import _tables as tables

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
        transformation_id: str,
    ):
        self._transformation = transformation
        self._transformation_id = transformation_id
        self._invariants: dict[str, Callable[[R, R], bool]] = {}

    def add_invariant(
        self,
        invariant: Callable[[R, R], bool],
        invariant_id: str,
    ) -> None:
        """Add an invariant to a transformation to create a new relation pair."""
        self._invariants[invariant_id] = invariant

    def apply_transform(self, data: T) -> T:
        """Apply a relation's transformation."""
        return self._transformation(data)

    @property
    def transformation_id(self) -> str:
        return self._transformation_id

    @property
    def transformation_name(self) -> str:
        return self._transformation.__name__

    @property
    def invariants(self) -> dict[str, Callable[[R, R], bool]]:
        return self._invariants

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"transformation={self._transformation.__name__}, "
            f"invariants={[invariant.__name__ for invariant in self._invariants.values()]})"
        )


class KnowledgeBase[T, R]:
    """
    A collection of metamorphic relations.

    Relations are registered in (transformation, invariant) pairs. Under the hood, a
    relation stores single transformation and a list of invariants.

    Is it important to note that lambda functions cannot be used for transformations or
    invariants.
    """

    def __init__(self) -> None:
        self._transformations: dict[str, str] = {}
        self._invariants: dict[str, str] = {}
        self._relations: dict[str, Relation[T, R]] = {}

    def register(
        self,
        transformation: Callable[[T], T],
        invariant: Callable[[R, R], bool],
    ):
        """Register a relation into the knowledge base, ensuring the name is unique."""
        transformation_name = transformation.__name__
        invariant_name = invariant.__name__
        if _LAMBDA_FUNCTION_NAME in {transformation_name, invariant_name}:
            raise ValueError(
                "Lambda functions cannot be used as transformation or invariants."
            )

        if transformation_name not in self._transformations:
            self._transformations[transformation_name] = tables.generate_uuid()
        if invariant_name not in self._invariants:
            self._invariants[invariant_name] = tables.generate_uuid()
        transformation_id = self._transformations[transformation_name]
        invariant_id = self._invariants[invariant_name]

        if transformation_id not in self._relations:
            self._relations[transformation_id] = Relation[T, R](
                transformation,
                transformation_id,
            )
        self._relations[transformation_id].add_invariant(invariant, invariant_id)

    @property
    def transformation_ids(self) -> dict[str, str]:
        """Return mappings from transformation name to transformation id."""
        return self._transformations

    @property
    def invariant_ids(self) -> dict[str, str]:
        """Return mappings from invariant name to invariant id."""
        return self._invariants

    @property
    def relations(self) -> dict[str, Relation[T, R]]:
        """Return a mapping of all registered relations."""
        return self._relations

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"relations={list(self._transformations.keys())}"
        )
