from pathlib import Path

from experiment.params import ExperimentParams
from experiment.runner import ExperimentRunner
from core.lin_solver import LinSolver
from core.lin_solver import SolvingMethod
from experiment.visualizer import ExperimentVisualizer

if __name__ == "__main__":
    solver = LinSolver()
    visualizer = ExperimentVisualizer(
        save=True, show=True, outdir=Path("docs/charts")
    )
    exp_runner = ExperimentRunner(solver=solver,visualizer=visualizer)

    all_methods = [SolvingMethod.JACOBI, SolvingMethod.GAUSS_SEIDLER, SolvingMethod.LU_DECOMPOSITION]

    exp_runner.run_convergence(params=ExperimentParams.DEFAULT_CONVERGENT,
             methods=[SolvingMethod.JACOBI, SolvingMethod.GAUSS_SEIDLER])
    exp_runner.run_convergence(params=ExperimentParams.DEFAULT_NON_CONVERGENT,
            methods=[SolvingMethod.JACOBI, SolvingMethod.GAUSS_SEIDLER])

    visualizer.show = False
    visualizer.save = False
    exp_runner.run_convergence(params=ExperimentParams.DEFAULT_NON_CONVERGENT,
            methods=[SolvingMethod.LU_DECOMPOSITION])
    visualizer.show = True
    visualizer.save = True

    exp_runner.run_performance(params=ExperimentParams.DEFAULT_PERFORMANCE,methods=all_methods)

