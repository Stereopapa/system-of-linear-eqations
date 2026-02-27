from dataclasses import dataclass
from typing import List

@dataclass
class ExperimentParams:
    name: str
    N: List[int] | int
    a1: float
    a2: float
    a3: float
    f: int
    DEFAULT_CONVERGENT: 'ExperimentParams' = None
    DEFAULT_NON_CONVERGENT: 'ExperimentParams' = None
    DEFAULT_PERFORMANCE: 'ExperimentParams' = None

ExperimentParams.DEFAULT_CONVERGENT = ExperimentParams(
    name="Convergence", N=1200, a1=8, a2=-1, a3=-1, f=1
)

ExperimentParams.DEFAULT_NON_CONVERGENT = ExperimentParams(
    name="Non Convergence", N=1200, a1=3, a2=-1, a3=-1, f=1
)

ExperimentParams.DEFAULT_PERFORMANCE = ExperimentParams(
    name="Performance", N=[100, 300 , 500, 1000, 2000, 3000], a1=8, a2=-1, a3=-1, f=1
)
