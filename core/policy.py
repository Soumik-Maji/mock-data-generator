from dataclasses import dataclass, asdict, field
from random import random, randint
from itertools import accumulate


@dataclass(frozen=True)
class ErrorRates:
    null: float = 0.05
    blank: float = 0.02
    duplicate: float = 0.01
    malformed: float = 0.01
    invalidPK: float = 0.0
    invalidFK: float = 0.0

    total: float = field(default=0.0, init=False)
    runningTotal: tuple = field(default=(), init=False)

    def __post_init__(self):
        rates = {k: v for k, v in asdict(self).items() if k not in ("total", "runningTotal")}

        total = sum(rates.values())
        if total > 1:
            raise ValueError("total percentage of all error rates went above 100")

        object.__setattr__(self, "total", total)
        object.__setattr__(self, "runningTotal", tuple(zip(rates.keys(), accumulate(rates.values()))))

    def shouldInject(self) -> bool:
        return random() < self.total

    def getErrorType(self) -> str:
        wtRand = random() * self.total
        for i in self.runningTotal:
            if wtRand < i[1]:
                return i[0]


@dataclass(frozen=True)
class Rows:
    min: int = 10
    max: int = 1000

    def __post_init__(self):
        if self.min >= self.max:
            raise ValueError("MIN rows should be less than MAX rows")

    def getInsertCount(self, currCnt: int) -> int:
        if currCnt < self.min:
            return self.min - currCnt + randint(0, int(self.min * 0.5))
        elif currCnt >= self.max:
            return 0
        else:
            return randint(1, min(3, self.max - currCnt))

    def getUpdateCount(self, currCnt: int) -> int:
        if currCnt == 0:
            return 0
        return randint(1, max(1, int(currCnt * 0.1)))

    def getDeleteCount(self, currCnt: int) -> int:
        if currCnt == 0:
            return 0
        return randint(1, max(1, int(currCnt * 0.2)))
