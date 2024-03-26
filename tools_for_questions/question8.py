"""
Functions for question #8
================================================

Contents:
---------
Contains the code for the question #8 of the project. In this question, we
wished to create an algorithm to compute a quantity called P_heavy.
"""


import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import random_unitary as qiskit_rand_unitary
import tools_for_questions.question7 as q7
from rich import print


def compute_pjs_one_rand_circ(
        number_qubits: int, 
        rand_qtm_circuit: QuantumCircuit
    ) -> np.ndarray:
    """DOCS
    """
    state_before_circuit = Statevector.from_int(0, 2**number_qubits)
    state_after_circuit = state_before_circuit.evolve(rand_qtm_circuit)
    return list(state_after_circuit.probabilities_dict().values())


def compute_P_heavy(list_pj: list, print_bool: bool = True) -> float:
    """DOCS
    """
    p_med = np.median(list_pj)
    list_pj_bigger_or_eq_pmed = [pj for pj in list_pj if pj >= p_med]
    P_heavy = sum(list_pj_bigger_or_eq_pmed)
    if print_bool == True:
        print(f"The value computed for P_heavy is {P_heavy:.3f}.")
    return P_heavy


def run_q8(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #8: \n")
    rand_n_qubit_qtm_circ = q7.qtm_circ_n_qubit_unitary(
        qiskit_rand_unitary(2**params["n_q8"]), 
        params["n_q8"]
    )
    P_heavy = compute_P_heavy(
        compute_pjs_one_rand_circ(params["n_q8"], rand_n_qubit_qtm_circ),
        True
    )
    print("\n Question #8 done. \n")
    return


if __name__ == "__main__":
    pass