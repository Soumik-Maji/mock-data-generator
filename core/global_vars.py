import sqlite3
from faker import Faker
from core.sqlite_connection import createConnection

_GLOBAL_CONN: sqlite3.Connection = None
_GLOBAL_FAKER: Faker = None


def openSqlite(dbPath: str) -> None:
    """SINGLETON: create & store sqlite connection as global variable"""
    global _GLOBAL_CONN
    _GLOBAL_CONN = createConnection(dbPath)
    print(
        f"""Opened sqlite connection
    File: {dbPath} | check .test_store dir when testing
    Connection: {_GLOBAL_CONN}"""
    )


def getSqlite() -> sqlite3.Connection:
    """SINGLETON: call to get global sqlite connection"""
    if _GLOBAL_CONN is None:
        raise RuntimeError("Connection not initialized. Call openSqlite() first")
    return _GLOBAL_CONN


def closeSqlite() -> None:
    """SINGLETON: close global sqlite connection"""
    global _GLOBAL_CONN
    if _GLOBAL_CONN is None:
        return
    _GLOBAL_CONN.close()
    print(f"Closed sqlite connection: {_GLOBAL_CONN}")
    _GLOBAL_CONN = None


def getFaker() -> Faker:
    """SINGLETON: get global faker instance"""
    global _GLOBAL_FAKER
    if _GLOBAL_FAKER is None:
        _GLOBAL_FAKER = Faker()
    return _GLOBAL_FAKER
