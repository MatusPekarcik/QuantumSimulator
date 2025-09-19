import numpy as np

# Basic single-qubit gates
X = np.array([[0, 1],
              [1, 0]], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                 [1, -1]], dtype=complex)

# helper to create controlled-X etc could be added later