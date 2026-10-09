from random import randint
from entities.helper.rows import Rows


def randomTest():
    row = Rows()
    print(f"min rows: {row.min}\tmax rows: {row.max}\n")
    currCnts = [randint(row.min, row.max) for _ in range(7)] + [0, 1, row.min, row.max]
    for r in range(10):
        print(f"Run: {r}")
        print("Current\tinsert\tupdate\tdelete")
        for i in currCnts:
            s = str(i)
            s += "\t" + str(row.getInsertCount(i))
            s += "\t" + str(row.getUpdateCount(i))
            s += "\t" + str(row.getDeleteCount(i))
            print(s)
        print("-" * 20)
