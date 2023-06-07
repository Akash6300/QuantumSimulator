import numpy as np
def pauli_x()->np.array:
    x_gate=np.array([[0,1],
                    [1,0]])
    return x_gate

def pauli_y()->np.array:
    y_gate=np.array([[0,-1j],
                      [1j,0]])
    return y_gate

def pauli_z()->np.array:
    return np.array([[1,0],
                    [0,-1]])

def hadamard()->np.array:
    return np.array([[1,1],
                    [1,-1]])*(np.sqrt(2))

def identity()->np.array:
    return np.identity(2)

def s_gate() -> np.array:
    return np.array([[1, 0],
                     [0, 1j]])

def t_gate() -> np.array:
    return np.array([[1, 0],
                     [0, np.exp(1j * np.pi / 4)]])

def sdg_gate() -> np.array:
    return np.conjugate(s_gate())

def tdg_gate() -> np.array:
    return np.conjugate(t_gate())

def rx_gate(angle: float) -> np.array:
    cos = np.cos(angle / 2)
    sin = np.sin(angle / 2)
    return np.array([[cos, -1j * sin],
                     [-1j * sin, cos]])

def ry_gate(angle: float) -> np.array:
    cos = np.cos(angle / 2)
    sin = np.sin(angle / 2)
    return np.array([[cos, -sin],
                     [sin, cos]])

def rz_gate(angle: float) -> np.array:
    cos = np.cos(angle / 2)
    sin = np.sin(angle / 2)
    return np.array([[np.exp(-1j * angle / 2), 0],
                     [0, np.exp(1j * angle / 2)]])


def gate(id: str,angle:float=0) -> np.array:
    gate_dict = {
        'x': pauli_x(),
        'y': pauli_y(),
        'z': pauli_z(),
        'h': hadamard(),
        'i': identity(),
        's': s_gate(),
        't': t_gate(),
        'sdg': sdg_gate(),
        'tdg': tdg_gate()
    }
    return gate_dict.get(id, lambda: None)

    
def cnot(control, target, num_qubits):
    M = np.zeros((2 ** num_qubits, 2 ** num_qubits), dtype=np.complex128)
    for i in range(2 ** num_qubits):
        binary_i = format(i, f'0{num_qubits}b')[::-1]  # Reverse the binary representation
        binary_i_list = list(binary_i)
        if binary_i_list[control] == '1':
            binary_i_list[target] = str(1 - int(binary_i_list[target]))
        binary_j = ''.join(binary_i_list)[::-1]  # Reverse back the modified binary representation
        j = int(binary_j, 2)
        M[i, j] = 1
        M[j, i] = 1
    return M
