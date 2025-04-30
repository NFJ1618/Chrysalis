import ast

import pytest

from chrysalis._internal import _invariants as invariants
from chrysalis._internal._relation import KnowledgeBase, Relation


@pytest.fixture
def sample_expression_1() -> ast.Expression:
    return ast.parse("3 - 2 + 4 / 2 + 1", mode="eval")


@pytest.fixture
def sample_expression_2() -> ast.Expression:
    return ast.parse("6 / 3 + 2 - 1", mode="eval")


class _MultiplyConstantsBy2(ast.NodeTransformer):
    def visit_Num(self, node: ast.Constant) -> ast.Constant:  # NOQA: N802
        return ast.Constant(value=node.value * 2)


class _DivideConstantsBy2(ast.NodeTransformer):
    def visit_Num(self, node: ast.Constant) -> ast.Constant:  # NOQA: N802
        return ast.Constant(value=node.value / 2)


def identity(expr: ast.Expression) -> ast.Expression:
    return expr


def inverse(expr: ast.Expression) -> ast.Expression:
    return ast.Expression(
        body=ast.BinOp(
            left=ast.UnaryOp(op=ast.USub(), operand=ast.Constant(value=1)),
            op=ast.Mult(),
            right=expr.body,
        )
    )


def multiply_constant_by_2(expr: ast.Expression) -> ast.Expression:
    return _MultiplyConstantsBy2().visit(expr)


def divide_constant_by_2(expr: ast.Expression) -> ast.Expression:
    return _DivideConstantsBy2().visit(expr)


def add_1_to_expression(expr: ast.Expression) -> ast.Expression:
    return ast.Expression(
        body=ast.BinOp(
            left=expr.body,
            op=ast.Add(),
            right=ast.Constant(value=1),
        ),
    )


def subtract_1_from_expression(expr: ast.Expression) -> ast.Expression:
    return ast.Expression(
        body=ast.BinOp(
            left=expr.body,
            op=ast.Sub(),
            right=ast.Constant(value=1),
        ),
    )


@pytest.fixture
def mock_knowledge_base() -> KnowledgeBase:
    knowledge_base: KnowledgeBase[ast.Expression, float] = KnowledgeBase()

    # Correct relations
    knowledge_base.register(
        transformation=identity,
        invariant=invariants.equals,
    )
    knowledge_base.register(
        transformation=inverse,
        invariant=invariants.not_same_sign,
    )
    knowledge_base.register(
        transformation=add_1_to_expression,
        invariant=invariants.greater_than,
    )

    # Inorrect relations, (invariant `equals` will fail).
    knowledge_base.register(
        transformation=subtract_1_from_expression,
        invariant=invariants.less_than,
    )
    knowledge_base.register(
        transformation=subtract_1_from_expression,
        invariant=invariants.equals,
    )
    return knowledge_base


@pytest.fixture
def correct_relation_1(mock_knowledge_base: KnowledgeBase) -> Relation:
    return mock_knowledge_base.relations[
        mock_knowledge_base.transformation_ids["identity"]
    ]


@pytest.fixture
def correct_relation_2(mock_knowledge_base: KnowledgeBase) -> Relation:
    return mock_knowledge_base.relations[
        mock_knowledge_base.transformation_ids["inverse"]
    ]


@pytest.fixture
def correct_relation_3(mock_knowledge_base: KnowledgeBase) -> Relation:
    return mock_knowledge_base.relations[
        mock_knowledge_base.transformation_ids["add_1_to_expression"]
    ]


@pytest.fixture
def incorrect_relation_1(mock_knowledge_base: KnowledgeBase) -> Relation:
    return mock_knowledge_base.relations[
        mock_knowledge_base.transformation_ids["subtract_1_from_expression"]
    ]


@pytest.fixture
def correct_relation_chain(
    correct_relation_1: Relation,
    correct_relation_2: Relation,
    correct_relation_3: Relation,
) -> list[Relation]:
    return [correct_relation_1, correct_relation_2, correct_relation_3]


@pytest.fixture
def incorrect_relation_chain(
    correct_relation_1: Relation,
    correct_relation_2: Relation,
    incorrect_relation_1: Relation,
) -> list[Relation]:
    return [correct_relation_1, correct_relation_2, incorrect_relation_1]


def eval_expr(a: ast.Expression) -> float:
    expr = compile(ast.fix_missing_locations(a), filename="<ast>", mode="eval")
    return eval(expr)  # NOQA: S307
