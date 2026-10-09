# from testing.error_rate_test import errorRateTest
# errorRateTest()
# from testing.row_test import randomTest
# randomTest()

from core.global_vars import openSqlite, closeSqlite

openSqlite("test.db")

from entities.customers import Customers
from core.policy import Rows
from time import sleep

try:
    customer = Customers(rows=Rows(10, 30), isCDC=True)
    while True:
        insCnt = customer.insert()
        if insCnt == 0:
            break
        sleep(2)

finally:
    closeSqlite()
