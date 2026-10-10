from dataclasses import dataclass
from typing import Callable, Any
import re

# 1. Base format validation (Letter/underscore first, no special characters, no $)
COLUMN_NAME_PATTERN = r"^[A-Za-z_][A-Za-z0-9_]*$"

# 2. Main SQLite reserved keywords to avoid
SQLITE_KEYWORDS = {
    "ABORT",
    "ACTION",
    "ADD",
    "AFTER",
    "ALL",
    "ALTER",
    "ANALYZE",
    "AND",
    "AS",
    "ASC",
    "ATTACH",
    "AUTOINCREMENT",
    "BEFORE",
    "BEGIN",
    "BETWEEN",
    "BY",
    "CASCADE",
    "CASE",
    "CAST",
    "CHECK",
    "COLLATE",
    "COLUMN",
    "COMMIT",
    "CONFLICT",
    "CONSTRAINT",
    "CREATE",
    "CROSS",
    "CURRENT_DATE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "DATABASE",
    "DEFAULT",
    "DEFERRABLE",
    "DEFERRED",
    "DELETE",
    "DESC",
    "DETACH",
    "DISTINCT",
    "DROP",
    "EACH",
    "ELSE",
    "END",
    "ESCAPE",
    "EXCEPT",
    "EXCLUSIVE",
    "EXISTS",
    "EXPLAIN",
    "FAIL",
    "FOR",
    "FOREIGN",
    "FROM",
    "FULL",
    "GLOB",
    "GROUP",
    "HAVING",
    "IF",
    "IGNORE",
    "IMMEDIATE",
    "IN",
    "INDEX",
    "INDEXED",
    "INITIALLY",
    "INNER",
    "INSERT",
    "INSTEAD",
    "INTERSECT",
    "INTO",
    "IS",
    "ISNULL",
    "JOIN",
    "KEY",
    "LEFT",
    "LIKE",
    "LIMIT",
    "MATCH",
    "NATURAL",
    "NO",
    "NOT",
    "NOTNULL",
    "NULL",
    "OF",
    "OFFSET",
    "ON",
    "OR",
    "ORDER",
    "OUTER",
    "PLAN",
    "PRAGMA",
    "PRIMARY",
    "QUERY",
    "RAISE",
    "RECURSIVE",
    "REFERENCES",
    "REGEXP",
    "REINDEX",
    "RELEASE",
    "RENAME",
    "REPLACE",
    "RESTRICT",
    "RIGHT",
    "ROLLBACK",
    "ROW",
    "SAVEPOINT",
    "SELECT",
    "SET",
    "TABLE",
    "TEMP",
    "TEMPORARY",
    "THEN",
    "TO",
    "TRANSACTION",
    "TRIGGER",
    "UNION",
    "UNIQUE",
    "UPDATE",
    "USING",
    "VACUUM",
    "VALUES",
    "VIEW",
    "VIRTUAL",
    "WHEN",
    "WHERE",
    "WITH",
    "WITHOUT",
}


@dataclass(frozen=True)
class Field:
    name: str = ""
    datatype: str = "TEXT"
    generator: Callable[[], Any] | None = None
    pk: bool = False
    fk: str | None = None  # "table.column", metadata only

    def __post_init__(self):
        object.__setattr__(self, "name", self.name.strip().lower())
        object.__setattr__(self, "datatype", self.datatype.strip().upper())
        if self.fk:
            object.__setattr__(self, "fk", self.fk.strip().lower())

        Field._isValidColumnName(self.name)

        validTypes = ["NULL", "INTEGER", "REAL", "TEXT", "BLOB", "BOOLEAN", "DECIMAL", "DATE", "TIMESTAMP", "JSON"]
        if self.datatype not in validTypes:
            raise ValueError(
                f"{self.datatype} datatype is invalid in sqlite & custom declared types.\nUse one of these {",".join(validTypes)}"
            )

    @staticmethod
    def _isValidColumnName(name) -> None:
        # Step 1: Check against empty & rowid
        if name in ("", "rowid"):
            raise ValueError("Column name cannot be empty or 'rowid' (sqlite internal use only).")

        # Step 2: Check against the basic character rules
        if not re.match(COLUMN_NAME_PATTERN, name):
            raise ValueError("Column name has to follow sqlite column naming convention, exclude '$' too.")

        # Step 3: Check if it conflicts with a forbidden keyword (case-insensitive)
        if name.upper() in SQLITE_KEYWORDS:
            raise ValueError("Column name cannot have sqlite reserved keywords.")

    def ddl(self) -> str:
        sql = f"{self.name} {self.datatype}"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql
