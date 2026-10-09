from dataclasses import dataclass
from typing import Callable, Any


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

        if self.name in ("", "rowid"):
            raise ValueError("Column name cannot be empty or 'rowid' (sqlite internal use only).")

        validTypes = ["NULL", "INTEGER", "REAL", "TEXT", "BLOB", "BOOLEAN", "DECIMAL", "DATE", "TIMESTAMP", "JSON"]
        if self.datatype not in validTypes:
            raise ValueError(
                f"{self.datatype} datatype is invalid in sqlite & custom declared types.\nUse one of these {",".join(validTypes)}"
            )

    def ddl(self) -> str:
        sql = f"{self.name} {self.datatype}"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql
