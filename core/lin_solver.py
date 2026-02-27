from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray
from typing import List, Literal
import time

class SolvingMethod(str, Enum):
    JACOBI = "jacobi"
    GAUSS_SEIDLER = "gauss_seidler"
    LU_DECOMPOSITION = "lu_decomposition"

class LinSolver:
    A: NDArray[np.float64]
    b: NDArray[np.float64]
    N: int

    x: np.ndarray
    iters: int
    time_to_solve: float
    residual_norm_archive: List[float]

    def __init__(self):
        pass

    def load_data(self, A: NDArray[np.float64], b: NDArray[np.float64], N: int):
        self.A: NDArray[np.float64] = A
        self.b: NDArray[np.float64] = b
        self.N: int = N
        self._reset_results()

    def normE1(self) -> float:
        r = (np.matmul(self.A, self.x) - self.b)
        return np.sum(np.abs(r))

    def normE2(self) -> float:
        r = (np.matmul(self.A, self.x) - self.b)
        return np.sum(r ** 2) ** 0.5

    def _reset_results(self):
        self.x = np.zeros(self.N)
        self.iters = 0
        self.time_to_solve = 0
        self.residual_norm_archive = []

    def solve(self, mode: SolvingMethod):
        if self.A is None or self.b is None or self.N is None:
            raise ValueError("Solver components (A, b, N) must be initialized by load data before solving.")
        match mode:
            case SolvingMethod.JACOBI:
                self._solve_jacobi()

            case SolvingMethod.GAUSS_SEIDLER:
                self._solve_gauss_seidler()

            case SolvingMethod.LU_DECOMPOSITION:
                self._solve_lu()

    def _solve_jacobi(self):
        self.time_to_solve = time.perf_counter_ns()
        D = np.diag(self.A)
        R = self.A - np.diag(D)

        currNorm = self.normE1()
        while 1e-9 < currNorm < 1e+9:
            self.x = (self.b- np.matmul(R,self.x)) / D
            self.iters += 1
            currNorm = self.normE1()
            self.residual_norm_archive.append(currNorm)

        self.time_to_solve = (time.perf_counter_ns() - self.time_to_solve) / 1e9
        return self.x

    def _solve_gauss_seidler(self):
        self.time_to_solve = time.perf_counter_ns()
        currNorm = self.normE1()

        while 1e-9 < currNorm < 1e9:
            for i in range(self.N):
                sum_ = np.dot(self.A[i, :i], self.x[:i])
                sum_ += np.dot(self.A[i, i + 1:], self.x[i + 1:])
                self.x[i] = (self.b[i] - sum_) / self.A[i][i]

            self.iters += 1
            currNorm = self.normE1()
            self.residual_norm_archive.append(currNorm)

        self.time_to_solve = (time.perf_counter_ns() - self.time_to_solve) / 1e9
        return self.x

    def _lu_decomposition_naive(self):
        U = self.A.copy()
        L = np.eye(self.N)
        for i in range(2, self.N + 1):
            for j in range(1, i):
                L[i - 1, j - 1] = U[i - 1, j - 1] / U[j - 1, j - 1]
                U[i - 1, :] = U[i - 1, :] - L[i - 1, j - 1] * U[j - 1, :]
        return L, U

    def _solve_lu(self):
        self.time_to_solve = time.perf_counter_ns()

        L, U = self._lu_decomposition_naive()
        y = np.zeros(self.N)

        # Forward substitution to solve L * y = b
        for i in range(self.N):
            sum_ = np.dot(L[i, :i], y[:i])
            y[i] = (self.b[i] - sum_) / L[i, i]

        # Backward substitution to solve U * x = y
        for i in reversed(range(self.N)):
            sum_ = np.dot(U[i, i + 1:], self.x[i + 1:])
            self.x[i] = (y[i] - sum_) / U[i, i]

        self.time_to_solve = (time.perf_counter_ns() - self.time_to_solve) / 10e8
        return self.x
