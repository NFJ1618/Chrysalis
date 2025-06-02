# analyze_failures.py

import duckdb

# Use an absolute path to avoid file not found errors
DB_PATH = "C:/Users/jaipa/CS/Chrysalis/examples/randomllm/chrys.db"

db = duckdb.connect()
db.execute("INSTALL sqlite;")
db.execute("LOAD sqlite;")

print("\n=== TOTAL TRANSFORMATION APPLICATIONS ===")
print(db.execute("""
SELECT
    name AS transformation,
    COUNT(*) AS total_applications
FROM sqlite_scan(?, 'applied_transformation')
GROUP BY name;
""", [DB_PATH]).fetchdf())

print("\n=== TOTAL INVARIANT FAILURES BY TRANSFORMATION ===")
print(db.execute("""
SELECT
    at.name AS transformation,
    fi.name AS invariant,
    COUNT(*) AS failures
FROM sqlite_scan(?, 'failed_invariant') fi
JOIN sqlite_scan(?, 'applied_transformation') at ON fi.applied_transformation = at.id
GROUP BY at.name, fi.name
ORDER BY failures DESC;
""", [DB_PATH, DB_PATH]).fetchdf())

print("\n=== FAILURE RATE (%) BY TRANSFORMATION AND INVARIANT ===")
print(db.execute("""
WITH total_pairs AS (
    SELECT
        at.name AS transformation,
        COUNT(*) AS total_pairs
    FROM sqlite_scan(?, 'applied_transformation') at
    JOIN sqlite_scan(?, 'input_data') id ON 1=1
    GROUP BY at.name
),
failures AS (
    SELECT
        at.name AS transformation,
        fi.name AS invariant,
        COUNT(*) AS failures
    FROM sqlite_scan(?, 'failed_invariant') fi
    JOIN sqlite_scan(?, 'applied_transformation') at ON fi.applied_transformation = at.id
    GROUP BY at.name, fi.name
)
SELECT
    failures.transformation,
    failures.invariant,
    failures.failures,
    total_pairs.total_pairs,
    ROUND(100.0 * failures.failures / total_pairs.total_pairs, 2) AS failure_rate_percent
FROM failures
JOIN total_pairs ON failures.transformation = total_pairs.transformation
ORDER BY failure_rate_percent DESC;
""", [DB_PATH, DB_PATH, DB_PATH, DB_PATH]).fetchdf())

print("\n=== ALL FAILED CASES (for debugging) ===")
print(db.execute("""
SELECT
    at.name AS transformation,
    fi.name AS invariant,
    fi.input_data,
    at.link_index,
    at.created_at
FROM sqlite_scan(?, 'failed_invariant') fi
JOIN sqlite_scan(?, 'applied_transformation') at ON fi.applied_transformation = at.id
ORDER BY at.link_index;
""", [DB_PATH, DB_PATH]).fetchdf())

print("\n=== TOTAL FAILURES PER INVARIANT ===")
print(db.execute("""
SELECT
    name AS invariant,
    COUNT(*) AS total_failures
FROM sqlite_scan(?, 'failed_invariant')
GROUP BY name
ORDER BY total_failures DESC;
""", [DB_PATH]).fetchdf())