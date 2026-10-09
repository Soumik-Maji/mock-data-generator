# NOTE: SQLite natively only recognizes five data types: NULL, INTEGER, REAL, TEXT, and BLOB.
# It doesn't know what a Python datetime/decimal/bool is, so it tries to guess or converts them into weird string formats.

import sqlite3
from datetime import date, datetime
from decimal import Decimal
import json
from pathlib import Path

# REGISTER THE ADAPTERS (Python Object -> SQLite Primitive)
sqlite3.register_adapter(bool, lambda v: 1 if v else 0)
sqlite3.register_adapter(Decimal, lambda v: str(v))
sqlite3.register_adapter(date, lambda v: v.isoformat())
sqlite3.register_adapter(datetime, lambda v: v.isoformat())
sqlite3.register_adapter(dict, lambda v: json.dumps(v))
sqlite3.register_adapter(list, lambda v: json.dumps(v))


# REGISTER THE CONVERTERS (SQLite Primitive -> Python Object)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
sqlite3.register_converter("DECIMAL", lambda v: Decimal(v.decode("utf-8")))
sqlite3.register_converter("DATE", lambda v: date.fromisoformat(v.decode("utf-8")))
sqlite3.register_converter("TIMESTAMP", lambda v: datetime.fromisoformat(v.decode("utf-8")))
sqlite3.register_converter("JSON", lambda v: json.loads(v.decode("utf-8")))


def createConnection(dbPath: str) -> sqlite3.Connection:
    # creating the storage path if not exists
    dbPath = ".test_store/" + dbPath
    path = Path(dbPath).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        database=dbPath,
        timeout=10,  # maximum time SQLite waits when encountering a locked database before throwing error
        isolation_level="IMMEDIATE",  # db locked as soon as write transaction begins
        detect_types=sqlite3.PARSE_DECLTYPES,
    )

    conn.execute("PRAGMA journal_mode=WAL;")  # can read while writing, but db still locked per write
    conn.execute("PRAGMA synchronous=NORMAL;")  # sync data at critical checkpoints instead of after every single write transaction
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row  # returns SELECT rows as objects accessible by both name and index

    return conn
