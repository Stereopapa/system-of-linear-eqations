import dataclasses
from typing import List, Dict, Tuple

from core.lin_solver import LinSolver
from core.lin_solver import SolvingMethod
from core.matrix_generator import getMatrixA, getVectorB
from experiment.params import ExperimentParams
from experiment.visualizer import ExperimentVisualizer
import matplotlib as plt
import numpy as np



class ExperimentRunner:
    _lin_solver: LinSolver
    _visualizer: ExperimentVisualizer

    def __init__(self, solver: LinSolver, visualizer: ExperimentVisualizer):
        self._visualizer = visualizer
        self._lin_solver = solver

    def _print_solving_info(self, method: str):
        name = method[0].upper() + method[1:]
        print(f"{name} Time: {self._lin_solver.time_to_solve}, {name} residium: {self._lin_solver.normE1()}")

    def run_convergence(self, methods: List[SolvingMethod],  params: ExperimentParams):
        A = getMatrixA(params.N, params.a1, params.a2, params.a3)
        b = getVectorB(params.N, params.f)
        N = params.N

        results: Dict[str, Tuple[List[int], List[float]]] = {}
        print(f"\n{"="*20} Genereated data for Experiment {params.name} {"="*20}")
        print(f"Matrix A:\n{A}\nvector b\n{b}")
        print(f"\n{"="*20} Experiment {params.name} Stated {"="*20}")
        for method in methods:
            self._lin_solver.load_data(A=A.copy(), b=b.copy(), N=N)
            self._lin_solver.solve(method)
            self._print_solving_info(method)
            y = self._lin_solver.residual_norm_archive.copy()
            x = np.arange(1, len(y) + 1).tolist()
            results[method] = x, y
        self._visualizer.plot_methods_comparison(
            experiments=results, title=f"{params.name} Experiment",
            x_label="Iteration", y_label="Residual Norm", x_log=False, y_log=True
            )

    def run_performance(self, methods: List[SolvingMethod], params: ExperimentParams):

        time_results: Dict[str, List[float]] = {method: [] for method in methods}
        print(f"\n{"="*20} Experiment {params.name} Stated {"="*20}")
        for N in params.N:
            A = getMatrixA(N, params.a1, params.a2, params.a3)
            b = getVectorB(N, params.f)

            print(f"Testing performance for matrix size N={N}...")
            for method in methods:
                self._lin_solver.load_data(A=A.copy(), b=b.copy(), N=N)
                self._lin_solver.solve(method)
                self._print_solving_info(method)
                time_results[method].append(self._lin_solver.time_to_solve)
            print()

        results: Dict[str, Tuple[List[int], List[float]]] = {}
        for method in methods:
            results[method] = (params.N, time_results[method])

        # 1. Generate Linear Time Comparison Chart
        self._visualizer.plot_methods_comparison(
            experiments=results, title="Algorithms Time Comparison", filename="algorithms_time_comparison",
            x_label="Matrix Size N", y_label="Time to Solve [s]", x_log=False, y_log=False
        )

        # 2. Generate Logarithmic Time Comparison Chart
        self._visualizer.plot_methods_comparison(
            experiments=results, title=f"{params.name} Experiment",
            filename="algorithms_log_time_comparison",
            x_label="Matrix Size N", y_label="Time to Solve [s]", x_log=False, y_log=True
        )



