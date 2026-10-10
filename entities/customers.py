import sqlite3
from datetime import date
from random import randint, random
from core.base import BaseEntity
from core.fields import Field
from core.policy import Rows, ErrorRates


class Customers(BaseEntity):

    def __init__(self, isCDC: bool = False, rows: Rows = None, errorRates: ErrorRates = None):
        super().__init__("customers", isCDC, rows, errorRates)
        # self.showTable()

    def getFields(self) -> list[Field]:
        return [
            Field("customer_id", "INTEGER", pk=True),
            Field("first_name", "TEXT", self.fake.first_name),
            Field("last_name", "TEXT", self.fake.last_name),
            Field("country", "TEXT", self.fake.country),
            Field("value", "INTEGER", lambda: randint(10, 100)),
            Field("growth_per", "INTEGER", lambda: round(random(), 4)),
            Field("signup_date", "DATE", lambda: self.fake.date_between("-10y")),
        ]
