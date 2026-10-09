from entities.helper.errors_rates import ErrorRates


def _run(msg, er):
    print("msg")
    # print(er)
    for _ in range(20):
        s = er.shouldInject()
        t = er.getErrorType() if s else None
        print(f"{s}\t{t}")
    print("-" * 20)


def errorRateTest():
    _run("Normal rates", ErrorRates())
    _run("Increased rates", ErrorRates(0.01, 0.1, 0.2, 0.2, 0.05, 0.05))
    _run("Increased rates for db keys only", ErrorRates(invalidFK=0.3, invalidPK=0.2))
