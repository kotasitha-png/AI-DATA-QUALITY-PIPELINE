import time
from typing import Any, Callable, Dict


def measure_operation(
    operation: Callable,
) -> tuple[Any, float]:
    """
    Execute an operation and return
    its result and elapsed seconds.
    """

    start = time.perf_counter()

    result = operation()

    elapsed = (
        time.perf_counter()
        - start
    )

    return (
        result,
        round(elapsed, 3),
    )


def build_benchmark_record(
    dataset: str,
    rows: int,
    timings: Dict[str, float],
) -> Dict[str, Any]:

    return {
        "dataset": dataset,
        "rows": rows,
        **timings,
    }