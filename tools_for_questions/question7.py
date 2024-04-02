"""
Functions for question #7
================================================

Contents:
---------
Contains the code for the question #7 of the project. In this question, we 
wished to show that our Haar measurement is uniform with a histogram plot. We
also wanted to compute the mean of the z variable and it's variance.
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate 
from qiskit.quantum_info import Statevector, Pauli
from scipy.stats import rv_continuous
from rich import print


def prob_distrib_phi(range_of_phi: tuple):
    """DOCS
    """
    class phi_distrib(rv_continuous):
        """DOCS
        """
        def _pdf(self, phi):
            """DOCS
            """
            return 1 / 2 * np.sin(phi)
    return phi_distrib(a = range_of_phi[0], b = range_of_phi[1]).rvs()


def generate_rand_params(range_of_params: tuple) -> tuple:
    """DOCS
    """
    rhos = np.random.uniform(
        low = range_of_params[0][0], 
        high = range_of_params[0][1]
    )
    phis = prob_distrib_phi(range_of_params[1])
    thetas = np.random.uniform(
        low = range_of_params[2][0], 
        high = range_of_params[2][1]
    )
    return (rhos, phis, thetas)


def generate_haar_unitary(params: tuple) -> UnitaryGate:
    """DOCS
    """
    unitary = [
        [np.exp(-1j * (params[0] + params[2]) / 2) * np.cos(params[1] / 2),
         -np.exp(1j * (params[0] - params[2]) / 2) * np.sin(params[1] / 2)],
        [np.exp(-1j * (params[0] - params[2]) / 2) * np.sin(params[1] / 2),
         np.exp(1j * (params[0] + params[2]) / 2) * np.cos(params[1] / 2)]
    ]
    return UnitaryGate(unitary)


def qtm_circ_n_qubit_unitary(
        unitary_to_apply: UnitaryGate, 
        number_qubits: int
    ) -> QuantumCircuit:
    """DOCS
    """
    quantCirc = QuantumCircuit(number_qubits)
    quantCirc.append(unitary_to_apply, range(number_qubits))
    return quantCirc


def compute_z_value(qtm_circ: QuantumCircuit) -> float:
    """DOCS
    """
    sigma_z = Pauli("Z")
    state_after_circuit = Statevector.from_label("0").evolve(qtm_circ)
    return state_after_circuit.expectation_value(sigma_z)


def compute_mean_z_value(
        sim_number: int, 
        number_qubits: int, 
        range_of_params: tuple
    ) -> tuple:
    """DOCS
    """
    all_z_values = []
    for _ in range(0, sim_number):
        rand_unitary = generate_haar_unitary(
            generate_rand_params(range_of_params)
        )
        rand_qtm_circuit = qtm_circ_n_qubit_unitary(rand_unitary, number_qubits)
        all_z_values.append(compute_z_value(rand_qtm_circuit))
        if (_ % 5000 == 0) & (_ != 0):
            print(f"Simulation number {_} done.")
    
    mean_all_z_values = np.abs(np.mean(all_z_values))
    var_all_z_values = np.var(all_z_values)
    print(f"The mean value of z is: {mean_all_z_values:.3f}" 
          + f" and it's variance is: {var_all_z_values:.3f}")
    return (all_z_values, mean_all_z_values, var_all_z_values)


def histo_plot(all_z_values: list) -> None:
    """DOCS
    """
    plt.hist(all_z_values, bins = 20, color = "#7e374e")
    plt.xlabel(r"$z = \langle Z \rangle$")
    plt.ylabel("Comptes")
    plt.savefig(
        f"{os.path.abspath(os.getcwd())}/figures/question7_figs/" + 
        "question7_histo.png"
    )
    return


def run_q7(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #7: \n")
    all_z_values = compute_mean_z_value(
        params["N_q7"], 
        params["n_q7"], 
        (
            params["rho_range_q7"], 
            params["phi_range_q7"], 
            params["theta_range_q7"]
        )
    )
    histo_plot(all_z_values[0])
    print("\n Question #7 done. \n")
    return


if __name__ == "__main__":
    pass