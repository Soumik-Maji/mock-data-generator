from abc import ABC, abstractmethod
from random import randint, choice, random
from datetime import datetime, timezone
from typing import Callable, Any, final
from core.global_vars import getSqlite, getFaker
from core.fields import Field
from core.policy import Rows, ErrorRates


class BaseEntity(ABC):
    getSqlite().execute(  # static code, runs once when BaseEntity loaded
        """create table if not exists cdc (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TIMESTAMP, oper TEXT,
            tbl TEXT, col TEXT, pk INTEGER,
            before TEXT, after TEXT
        )"""
    )

    def __init__(self, tableName: str, isCDC: bool = False, rowsConf: Rows = None, errorsConf: ErrorRates = None):
        self.conn = getSqlite()
        self.fake = getFaker()

        self.tableName = tableName.strip().lower()
        if self.tableName in ("", "cdc"):
            raise ValueError("Table name cannot be empty or 'cdc' (sqlite internal use only).")

        self.rowsConf = Rows() if rowsConf is None else rowsConf
        self.errorsConf = ErrorRates() if errorsConf is None else errorsConf
        self.isCDC = isCDC

        self.fields = self.getFields()
        pks = [c for c in self.fields if c.pk]
        if len(pks) > 1:
            raise ValueError(f"{self.tableName} must have <= 1 pk field, found {len(pks)}.")
        self.pk = pks[0].name

        self.createTable()

    @final
    def insertIntoCDC(self, ts, oper, col, pk, before, after) -> None:
        values = [ts, oper, self.tableName, col, pk, before, after]
        self.conn.execute("insert into cdc (ts,oper,tbl,col,pk,before,after) values(?,?,?,?,?,?,?)", values)

    @final
    def makeRow(self) -> dict[str, Callable[[], Any]]:
        return {f.name: f.generator() for f in self.fields if f.generator}

    def insert(self) -> int:
        insCnt = self.rowsConf.getInsertCount(self.getRowCount())
        if insCnt < 1:
            print(f"'{self.tableName}' table is full. cannot insert anything else.")
            return insCnt

        print(f"inserting {insCnt} rows into '{self.tableName}'")
        validCols = tuple(f.name for f in self.fields if not f.pk)
        validVals = ",".join("?" * len(validCols))
        query = f"insert into {self.tableName} ({",".join(validCols)}) values({validVals})"
        currTs = datetime.now(timezone.utc)
        with self.conn:
            for _ in range(insCnt):
                row = self.makeRow()
                self.conn.execute(query, list(row.values()))
                pk = self.conn.execute("select last_insert_rowid()").lastrowid
                if self.isCDC:
                    for k, v in row.items():
                        self.insertIntoCDC(currTs, "I", k, pk, None, v)
        return insCnt

    def delete(self) -> int:
        delCnt = self.rowsConf.getDeleteCount(self.getRowCount())
        if delCnt < 1:
            print(f"'{self.tableName}' table is empty. no row to delete.")
            return delCnt

        print(f"deleting {delCnt} rows in '{self.tableName}'")
        currTs = datetime.now(timezone.utc)
        query = f"delete from {self.tableName} where {self.pk} = ?"
        with self.conn:
            for _ in range(delCnt):
                row = self.getRandomRow()
                pkid = row[self.pk]
                self.conn.execute(query, [pkid])
                if self.isCDC:
                    self.insertIntoCDC(currTs, "D", None, pkid, None, None)
        return delCnt

    def update(self) -> int:
        updtCnt = self.rowsConf.getUpdateCount(self.getRowCount())
        if updtCnt < 1:
            print(f"'{self.tableName}' table is empty. no row to update.")
            return updtCnt

        print(f"updating {updtCnt} rows in '{self.tableName}'")
        currTs = datetime.now(timezone.utc)
        with self.conn:
            for _ in range(updtCnt):
                row = self.getRandomRow()
                col = self.getRandomColumnName()
                pkid = row[self.pk]
                oldVal = row[col.name]
                newVal = col.generator()

                query = f"update {self.tableName} set {col.name} = ? where {self.pk} = ?"
                self.conn.execute(query, [newVal, pkid])
                if self.isCDC:
                    self.insertIntoCDC(currTs, "U", col.name, pkid, str(oldVal), str(newVal))
        return updtCnt

    @final
    def iud(self) -> None:
        """Call insert/update/delete based on the row counts they return so as to not waste cycles"""
        chance = round(random(), 2)
        if chance < 0.33:
            inscnt = self.insert()
            if inscnt == 0:
                if chance < 0.5:
                    self.update()
                else:
                    self.delete()
        elif chance < 0.66:
            updtCnt = self.update()
            if updtCnt == 0:
                self.insert()
        else:
            delCnt = self.delete()
            if delCnt == 0:
                self.insert()

    @final
    def getRandomColumnName(self) -> Field:
        return choice(list(filter(lambda x: not x.pk, self.fields)))

    @abstractmethod
    def getFields(self) -> list[Field]:
        pass

    @final
    def createTable(self) -> None:
        schema = ",".join(f.ddl() for f in self.fields)
        with self.conn:
            self.conn.execute(f"create table if not exists {self.tableName} ({schema});")

    @final
    def showTable(self) -> None:
        create_sql = self.conn.execute("select sql from sqlite_schema where name = ? collate nocase;", [self.tableName]).fetchone()
        if create_sql:
            print(f"Raw SQL definition:\n{create_sql[0]}")
        else:
            print(f"No table name found with name: {self.tableName}")

    @final
    def getRowCount(self) -> int:
        return self.conn.execute(f"select count(1) from {self.tableName}").fetchone()[0]

    @final
    def getRandomRow(self) -> dict[str, any] | None:
        currCnt = self.getRowCount()
        if currCnt == 0:
            return None
        randOffset = randint(0, currCnt - 1)
        return dict(
            self.conn.execute(
                f"select * from {self.tableName} where rowid = (select rowid from {self.tableName} limit 1 offset {randOffset});"
            ).fetchone()
        )
