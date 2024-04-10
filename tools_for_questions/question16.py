"""
Functions for question #16
================================================

Contents:
---------
Contains the code for the question #16 and the following bonus question labelled 
question #16.5 of the project. 

- Question #16:
    In question #16, we wished to estimate the mean of P_heavy computed with a
    quantum computer and compare it to the classical estimation we did at
    question #12.

- Question #16.5:
    In question #16.5, we wished to caracterise the mean of P_heavy for circuits
    running on real quantum computer with different numbers of layers.
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2, SamplerOptions, Sampler, Options
from qiskit.providers.backend import BackendV2
from qiskit_aer.noise import NoiseModel
import tools_for_questions.question8 as q8
import tools_for_questions.question12 as q12
from rich import print

import warnings
warnings.filterwarnings("ignore", category = RuntimeWarning) 


def run_job(
        token: str, 
        qtm_computer: str, 
        nbr_tirages: int, 
        all_qtm_circs: list,
        generated_noise: bool
    ) -> tuple:
    """DOCS
    """
    service = QiskitRuntimeService(
        channel = "ibm_quantum", 
        token = token
    )
    backend = service.backend(qtm_computer)
    backend_noise_reference = service.backend("ibm_brisbane")


    if generated_noise == True:
        print("Running with noise model from ibm_brisbane quantum computer.")
        noise_model = NoiseModel.from_backend(backend_noise_reference)
        options = Options()
        options.simulator = {
            "noise_model": noise_model,
            "basis_gates": backend_noise_reference.configuration().basis_gates
        }
        options.execution.shots = nbr_tirages
        options.optimization_level = 1

        print(f"Quantum computer {backend.name} ready!\n")
        sampler = Sampler(
            backend,
            options = options
        )
        job = sampler.run(all_qtm_circs)
        quasi_job_results = [
            i.nearest_probability_distribution().binary_probabilities() 
            for i in job.result().quasi_dists
        ]
        job_results = []
        for res_dict in quasi_job_results:
            res_dict.update(
                (state, int(prob * nbr_tirages)) # Approximately good enough
                for state, prob in res_dict.items()
            )
            job_results.append(res_dict)

    else:
        print(f"Quantum computer {backend.name} ready!\n")
        sampler = SamplerV2(
            backend,
            options = SamplerOptions(default_shots = nbr_tirages)
        )
        job = sampler.run(transpile_all_qtm_circ(all_qtm_circs, backend))
        job_results = [
            pub_result.data.meas.get_counts() for pub_result in job.result()
        ]

    classic_pjs = [
        q8.compute_pjs_one_rand_circ(
            circ.remove_final_measurements(inplace = False)
        )
        for circ in all_qtm_circs
    ]
    p_meds = [np.median(j) for j in [i[0] for i in classic_pjs]]
    prob_dicts = [i[1] for i in classic_pjs]
    return p_meds, prob_dicts, job_results


def generate_all_qtm_circ(
        nbr_circ: int,
        nbr_qubits: int, 
        nbr_layers: int
    ) -> list:
    """DOCS
    """
    all_qtm_circs = []
    for _ in range(nbr_circ):
        temp_single_layer_qtm_circ = q12.qtm_circ_single_layer(nbr_qubits)
        temp_mult_layers_qtm_circ = q12.multiply_layers_qtm_circ(
            nbr_layers, 
            temp_single_layer_qtm_circ
        )
        temp_mult_layers_qtm_circ.measure_all()
        all_qtm_circs.append(temp_mult_layers_qtm_circ)
    return all_qtm_circs


def transpile_all_qtm_circ(all_qtm_circs: list, backend: BackendV2) -> list:
    """DOCS
    """
    all_transpiled_qtm_circ = [
        transpile(circ, backend, optimization_level = 1) 
        for circ in all_qtm_circs
    ] 
    return all_transpiled_qtm_circ


def single_qtm_circ_shot(
        curr_p_med: list, 
        curr_prob_dict: list, 
        curr_job_res: list
    ) -> tuple:
    """DOCS
    """
    class_P_heavy = q8.compute_P_heavy(
                list(curr_prob_dict.values()), 
                print_bool = False
            )
    count = 0
    for states, prob in curr_prob_dict.items():
            if (states in curr_job_res) & (prob >= curr_p_med):
                count += curr_job_res[states]
    return class_P_heavy, count


def estimate_mean_P_heavy(
        token: str,
        qtm_computer: str,
        nbr_circ: int, 
        nbr_tirages: int, 
        nbr_qubits: int, 
        nbr_layers: int,
        generated_noise: bool
    ) -> float:
    """DOCS
    """
    all_qtm_circ = generate_all_qtm_circ(nbr_circ, nbr_qubits, nbr_layers)
    print(f"All {nbr_circ} quantum circuits generated!")
    p_meds, prob_dicts, job_results = run_job(
        token, 
        qtm_computer, 
        nbr_tirages, 
        all_qtm_circ,
        generated_noise
    )
    print("Job done!")

    all_class_P_heavy = []
    final_count = 0
    for circ_idx in range(nbr_circ):
        class_P_heavy, count = single_qtm_circ_shot(
            p_meds[circ_idx], 
            prob_dicts[circ_idx], 
            job_results[circ_idx]
        )
        all_class_P_heavy.append(class_P_heavy)
        final_count += count

    class_mean_P_heavy = np.mean(all_class_P_heavy)
    class_var_P_heavy = np.var(all_class_P_heavy)
    qtm_mean_P_heavy = final_count / (nbr_circ * nbr_tirages)

    print(
        f"The classical estimation for the mean of P_heavy is " + 
        f"{class_mean_P_heavy:.5f} with variance {class_var_P_heavy:.5f} " + 
        f"and the quantum estimation is {qtm_mean_P_heavy:.5f} with quantum " + 
        f"computer {qtm_computer}. \n"
    )

    return class_mean_P_heavy, class_var_P_heavy, qtm_mean_P_heavy


def caracterise_mean_P_heavy(
        max_circ_layers: int, 
        token: str,
        qtm_computer: str,
        nbr_circ: int, 
        nbr_tirages: int, 
        nbr_qubits: int,
        generated_noise: bool
    ) -> list:
    """DOCS
    """
    all_mean_qtm_P_heavys, all_mean_class_P_heavys = [], []
    for nbr_layers in range(1, max_circ_layers + 1):
        print(f"Now running circuit with {nbr_layers} layers.")
        temp_mean_P_heavy = estimate_mean_P_heavy(
            token, 
            qtm_computer, 
            nbr_circ, 
            nbr_tirages, 
            nbr_qubits, 
            nbr_layers,
            generated_noise
        )
        all_mean_qtm_P_heavys.append(temp_mean_P_heavy[2])
        all_mean_class_P_heavys.append(temp_mean_P_heavy[0])
    return all_mean_qtm_P_heavys, all_mean_class_P_heavys


def plot_caract_mean_P_heavy(
        max_circ_layers: int, 
        all_mean_qtm_P_heavys: list,
        all_mean_class_P_heavys: list
    ) -> None:
    """DOCS
    """
    plt.plot(
        range(1, max_circ_layers + 1), 
        all_mean_qtm_P_heavys, 
        ".-",
        markersize = 8,
        color = "#7e374e",
        label = r"Machine réelle"
    )
    plt.plot(
        range(1, max_circ_layers + 1), 
        all_mean_class_P_heavys, 
        ".-",
        markersize = 8,
        color = "#e3024d",
        label = r"Sachant les $\{p_j\}$"
    )
    plt.yticks(
        [0.5, 0.6, 2 / 3, 0.7, 0.8, 0.9, 1], 
        ["0.5", "0.6", "2/3", "0.7", "0.8", "0.9", "1"]
    )
    plt.hlines(2 / 3, 0, max_circ_layers + 1, color = "k", ls = "--")
    plt.xlabel(r"Nombre de couches pour le circuit $c$")
    plt.ylabel(r"$\bar{P}_{heavy}$")
    plt.xlim(0.95, max_circ_layers + 0.05)
    plt.ylim(0.5, 1)
    plt.legend()
    plt.savefig(
        f"{os.path.abspath(os.getcwd())}/figures/question16_figs/" + 
        "question16_caract.png"
    )
    return


def run_q16(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #16: \n")

    if params["quantum_computer"] == "ibmq_qasm_simulator":
        params["with_noise_or_not"] = True
    else:
        params["with_noise_or_not"] = False

    mean_P_heavy_quantities = estimate_mean_P_heavy(
        params["personnal_token"], 
        params["quantum_computer"],
        params["N_circuits_q16"],
        params["N_tirages_q16"],
        params["n_q16"],
        params["c_q16"],
        params["with_noise_or_not"]
    )
    print("\n Question #16 done. \n")
    return


def run_q16_5_bonus(params: dict) -> None:
    """DOCS
    """
    print("\n Currently running question #16.5: \n")

    if params["quantum_computer"] == "ibmq_qasm_simulator":
        params["with_noise_or_not"] = True
    else:
        params["with_noise_or_not"] = False

    all_mean_qtm_P_heavys, all_mean_class_P_heavys = caracterise_mean_P_heavy(
        params["max_c_q16_5_bonus"],
        params["personnal_token"], 
        params["quantum_computer"],
        params["N_circuits_q16_5_bonus"],
        params["N_tirages_q16_5_bonus"],
        params["n_q16_5_bonus"],
        params["with_noise_or_not"]
    )
    plot_caract_mean_P_heavy(
        params["max_c_q16_5_bonus"], 
        all_mean_qtm_P_heavys, 
        all_mean_class_P_heavys
    )
    print("\n Question #16.5 done. \n")
    return


if __name__ == "__main__":
    pass