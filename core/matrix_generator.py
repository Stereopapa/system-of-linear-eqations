import numpy as np

def getMatrixA(N: int, a1: float, a2: float, a3: float) -> np.typing.NDArray[np.float64]:
    result = np.zeros((N,N), dtype=np.float64)
    for i in range(N):
        result[i][i] = a1
        if i-1>=0: result[i-1][i] = a2
        if i+1<N: result[i+1][i] = a2
        if i-2>=0: result[i-2][i] = a3
        if i+2<N: result[i+2][i] = a3
    return result

def getVectorB(N: int, f: float) -> np.typing.NDArray[np.float64]:
    result = np.zeros(N, dtype=np.float64)
    for i in range(N):
        result[i] = np.sin(i*(f+1))
    return result