from functools import partial

import sqlglot
from sqlglot.expressions import Column, Select


def _remove_column_transformer(
    node: sqlglot.Expression, name: str
) -> sqlglot.Expression | None:
    if (
        isinstance(node, Column)
        and isinstance(node.parent, Select)
        and node.name == name
    ):
        return None
    return node


def add_college_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    expr_tree = expr_tree.transform(partial(_remove_column_transformer), name="college")

    assert isinstance(expr_tree, Select)
    return expr_tree.select("college").sql()


def add_team_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    expr_tree = expr_tree.transform(partial(_remove_column_transformer), name="team")

    assert isinstance(expr_tree, Select)
    return expr_tree.select("team").sql()


def add_round_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    expr_tree = expr_tree.transform(partial(_remove_column_transformer), name="round")

    assert isinstance(expr_tree, Select)
    return expr_tree.select("round").sql()


def add_draft_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    expr_tree = expr_tree.transform(partial(_remove_column_transformer), name="draft")

    assert isinstance(expr_tree, Select)
    return expr_tree.select("draft").sql()


def remove_college_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    return expr_tree.transform(
        partial(_remove_column_transformer), name="college"
    ).sql()


def remove_team_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    return expr_tree.transform(partial(_remove_column_transformer), name="team").sql()


def remove_round_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    return expr_tree.transform(partial(_remove_column_transformer), name="round").sql()


def remove_draft_column(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    return expr_tree.transform(partial(_remove_column_transformer), name="draft").sql()


def add_order_by_asc(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if "order" in expr_tree.args:
        expr_tree.args["order"].pop()
    return expr_tree.order_by("draft ASC, round ASC").sql()


def add_order_by_desc(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if "order" in expr_tree.args:
        expr_tree.args["order"].pop()
    return expr_tree.order_by("draft DESC, round DESC").sql()


def remove_order_by(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if "order" in expr_tree.args:
        expr_tree.args["order"].pop()
    return expr_tree.sql()


def add_limit_400(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if expr_tree.args["limit"] is not None:
        expr_tree.args["limit"].pop()
    return expr_tree.limit(400).sql()


def add_limit_200(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if expr_tree.args["limit"] is not None:
        expr_tree.args["limit"].pop()
    return expr_tree.limit(200).sql()


def remove_limit(query: str) -> str:
    expr_tree = sqlglot.parse_one(query)
    assert isinstance(expr_tree, Select)

    if expr_tree.args["limit"] is not None:
        expr_tree.args["limit"].pop()
    return expr_tree.sql()
