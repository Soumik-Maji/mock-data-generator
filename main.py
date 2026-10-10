# from testing.error_rate_test import errorRateTest
# errorRateTest()
# from testing.row_test import randomTest
# randomTest()

from time import time

start = time()

from random import random
from time import sleep
from datetime import timedelta

from core.global_vars import openSqlite, closeSqlite

openSqlite("test.db")

from entities.customers import Customers
from core.policy import Rows

try:
    customer = Customers(rows=Rows(3, 5), isCDC=True)
    sleep(3)
    n = 100
    print(f"-- running all I/U/D together for {n} times --")
    for _ in range(n):
        customer.iud()
        sleep(0.1)

finally:
    closeSqlite()

elapsed = time() - start
print(f"\n\nTime taken to run: {str(timedelta(seconds=int(elapsed)))}")
