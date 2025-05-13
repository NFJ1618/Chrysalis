from pathlib import Path
from functools import cache

import chrysalis as chry
import duckdb
import polars as pl

import sql.transformations as transformations
import sql.invariants as invariants


@cache
def _test_connection() -> duckdb.DuckDBPyConnection:
    input_data_path = Path("./sql/player_stats.parquet")
    if not input_data_path.exists():
        raise RuntimeError("Input dataset does not exist, exiting.")

    conn = duckdb.connect()
    conn.register(
        "player_stats",
        pl.read_parquet(input_data_path).cast({"round": pl.Int8}),
    )
    return conn


def evaluate_query(query: str) -> pl.DataFrame:
    conn = _test_connection()
    return conn.query(query).pl()


_TEST_QUERY = "SELECT name, position, college, team, round, draft FROM player_stats;"

if __name__ == "__main__":
    chry.register(transformations.add_college_column, invariants.length_equals)
    chry.register(transformations.add_team_column, invariants.length_equals)
    chry.register(transformations.add_round_column, invariants.length_equals)
    chry.register(transformations.add_draft_column, invariants.length_equals)
    chry.register(transformations.remove_college_column, invariants.length_equals)
    chry.register(transformations.remove_team_column, invariants.length_equals)
    chry.register(transformations.remove_round_column, invariants.length_equals)
    chry.register(transformations.remove_draft_column, invariants.length_equals)

    # TODO: WHERE clause

    chry.register(transformations.add_order_by_asc, invariants.length_equals)
    chry.register(transformations.add_order_by_desc, invariants.length_equals)
    chry.register(transformations.remove_order_by, invariants.length_equals)

    # Intentional bug, it is possible that adding `LIMIT 400` will remove `LIMIT 200`
    # and cause the invariant to fail.
    chry.register(transformations.add_limit_400, invariants.length_less_than_equals)
    chry.register(transformations.add_limit_200, invariants.length_less_than_equals)
    chry.register(transformations.remove_limit, invariants.length_equals)

    chry.run(evaluate_query, [_TEST_QUERY], chain_length=50, num_chains=10)
