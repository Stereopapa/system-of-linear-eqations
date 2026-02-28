# Linear Equation Solvers - Numerical Analysis

A specialized toolset for solving large systems of linear equations (Ax = b) using both direct and iterative numerical methods. The project includes a comprehensive benchmarking suite to evaluate algorithm convergence and computational efficiency.

---

## Tech Stack
* **Language:** Python 3.x
* **Core Libraries:** NumPy (Linear Algebra operations), Matplotlib (Performance visualization)
* **Testing Framework:** Custom experiment runner for performance and convergence analysis
* **Documentation:** LaTeX-generated technical report
* **Platform:** Windows (Tested and verified)

---

## Implemented Methods
1. **LU Decomposition:** A direct solver using naive LU factorization with forward and backward substitution. Provides high precision (r ≈ 10⁻¹³) for non-singular matrices.
2. **Jacobi Method:** An iterative algorithm suitable for diagonally dominant matrices. Implements vectorized operations for enhanced performance in NumPy.
3. **Gauss-Seidel Method:** An iterative solver that utilizes updated values within the same iteration, typically offering faster convergence than Jacobi.

---

## Engineering Insights & Logic
The project focuses on the **Diagonal Dominance Condition**, which is critical for the stability of iterative methods. A matrix A is strictly diagonally dominant if:

|aᵢᵢ| > ∑_{j≠i} |aᵢⱼ|



### Key Findings from Analysis:
* **Convergence:** For a convergent case (a₁ = 8, N = 1200), Gauss-Seidel reached the 10⁻⁹ residual threshold in 17 iterations, while Jacobi required 26.
* **Performance:** While LU decomposition offers superior accuracy, its computational complexity is O(N³), making it significantly slower for large systems. 
* **Benchmark Results:** For N = 3000, LU required > 30s, whereas iterative methods finished in < 1s.
* **Stability:** The project demonstrates divergence in non-diagonally dominant cases (a₁ = 3), where the residual norm ‖r‖ increases exponentially: ‖r‖ → ∞.



---

## Project Structure
* `/core`: Core solver logic (`LinSolver`) and pentadiagonal matrix generator.
* `/experiment`: Automation tools for running convergence and performance tests.
* `/docs`: Technical charts and a detailed PDF report.

---

## Installation & Usage (Windows)
**Note:** This application was developed and tested on Windows. Cross-platform compatibility (Linux/macOS) has not been verified.
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Stereopapa/system-of-linear-eqations.git
   cd system-of-linear-eqations

2. **Set up virtual environment (Recommended)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the application:**
   ```bash
   python main.py