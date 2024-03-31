"""
Functions for question #12
================================================

Contents:
---------
Contains the code for the question #12 and the following bonus question labelled 
question #12.5 of the project. 

- Question #12:
    In question #12, we wished to estimate the mean of P_heavy (computed with 
    the function of question #8) for a circuit with 10 qubits and 5 layers of 
    circuit. 

- Question #12.5:
    In question #12.5, we wished to caracterise the mean of P_heavy for circuits 
    with different numbers of qubits and layers.
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_unitary as qiskit_rand_unitary
import tools_for_questions.question8 as q8
from rich import print


def qtm_circ_single_layer(
        nbr_qubits: int
    ) -> QuantumCircuit:
    """DOCS
    """
    quantCirc = QuantumCircuit(nbr_qubits)
    all_rand_unitaries = [
        qiskit_rand_unitary(4) for _ in range((nbr_qubits - 1))
    ]
    qubit_idxs = get_qubit_idx_qtm_circ(nbr_qubits)
    for u, qidx in zip(all_rand_unitaries, qubit_idxs):
        quantCirc.append(u, list(qidx))
    return quantCirc


def multiply_layers_qtm_circ(
        nbr_layers: int, 
        qtm_circ_single_layer: QuantumCircuit
    ) -> QuantumCircuit:
    """DOCS
    """
    init_qtm_circ = qtm_circ_single_layer
    qtm_circ_to_update = qtm_circ_single_layer
    for _ in range(nbr_layers - 1):
        qtm_circ_to_update = qtm_circ_to_update.compose(init_qtm_circ)
    return  qtm_circ_to_update


def get_qubit_idx_qtm_circ(nbr_qubits: int) -> list:
    """DOCS
    """
    qubit_idx = np.arange(nbr_qubits)
    if nbr_qubits % 2 == 0:
        first_col = np.array_split(
            qubit_idx, 
            nbr_qubits // 2
        )
        sec_col = np.array_split(
            qubit_idx[1:len(qubit_idx) - 1], 
            nbr_qubits // 2 - 1
        )
        return first_col + sec_col
    else:
        first_col = np.array_split(
            qubit_idx[:len(qubit_idx) - 1], 
            nbr_qubits // 2
        )
        sec_col = np.array_split(
            qubit_idx[1:], 
            nbr_qubits // 2
        )
        return first_col + sec_col


def compute_mean_P_heavy(
        nbr_sim: int,
        nbr_qubits: int,
        nbr_layers: int,
        print_bool: bool = True
    ) -> float:
    """DOCS
    """
    p_heavys = []
    for _ in range(nbr_sim):
        qtm_circ = qtm_circ_single_layer(nbr_qubits)
        mult_layers_qtm_circ = multiply_layers_qtm_circ(nbr_layers, qtm_circ)
        pjs = q8.compute_pjs_one_rand_circ(mult_layers_qtm_circ)[0]
        p_heavys.append(q8.compute_P_heavy(pjs, False))
        if (_ % 5000 == 0) & (_ != 0):
            print(f"Simulation number {_} done.")
    
    mean_p_heavy = np.mean(p_heavys)
    if print_bool == True:
        print(
            f"The mean of all P_heavy over {nbr_sim} simulations is " +
            f"{mean_p_heavy:.3f} with standard deviation " +
            f"{np.std(p_heavys):.3f}. Simulations where with " +
            f"{int(nbr_qubits)} qubits and {int(nbr_layers)} layers."
        )
    return mean_p_heavy


def caracterise_bar_P_heavy(
        nbr_sim: int,
        max_nbr_qubits: int,
        max_nbr_layers: int
    ) -> np.ndarray:
    """DOCS
    """
    all_bar_P_heavy = []
    for nq in range(3, max_nbr_qubits + 1):
        for nl in range(1, max_nbr_layers + 1):
            all_bar_P_heavy.append(
                compute_mean_P_heavy(nbr_sim, nq, nl, True)
            )
    return np.array(all_bar_P_heavy)


def color_plot(
        all_bar_P_heavy: np.ndarray,
        max_nbr_qubits: int,
        max_nbr_layers: int
    ) -> None:
    """DOCS
    """
    mat_all_bar_P_heavy = np.array(
        np.array_split(all_bar_P_heavy, max_nbr_qubits - 2)
    )
    nq, nl = range(3, max_nbr_qubits + 1), range(1, max_nbr_layers + 1)
    qubit_grid, layer_grid = np.meshgrid(nq, nl)

    figure, axes = plt.subplots()
    color_map = axes.pcolormesh(
        qubit_grid.T, 
        layer_grid.T, 
        mat_all_bar_P_heavy, 
        cmap = 'Reds',
        vmax = 1,
        vmin = 0.8
    )
    figure.colorbar(color_map, ax = axes, label = r"$\bar{P}_{heavy}$")
    axes.axis(
        [qubit_grid.min(), qubit_grid.max(), layer_grid.min(), layer_grid.max()]
    )
    axes.set_xlabel("Number of qubits")
    axes.set_ylabel("Number of circuit layers")    
    figure.tight_layout()
    plt.savefig(
        f"{os.path.abspath(os.getcwd())}/figures/question12_figs/" + 
        "question12_5_bonus_colorplot.png"
    )
    return


def run_q12(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #12: \n")
    bar_P_heavy = compute_mean_P_heavy(
        params["N_q12"], 
        params["n_q12"],
        params["c_q12"]
    )
    print("\n Question #12 done. \n")
    return


def run_q12_5_bonus(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #12.5: \n")
    bar_P_heavys_coords = caracterise_bar_P_heavy(
        params["N_q12_5_bonus"], 
        params["max_n_q12_5_bonus"], 
        params["max_c_q12_5_bonus"]
    )
    color_plot(
        bar_P_heavys_coords, 
        params["max_n_q12_5_bonus"], 
        params["max_c_q12_5_bonus"]
    )
    print("\n Question #12.5 done. \n")
    return


if __name__ == "__main__":
    pass