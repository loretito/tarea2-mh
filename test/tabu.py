import random
import time
import matplotlib.pyplot as plt
import numpy as np
from readFile import readFile
from tabuSearch import tabu_search
from time import process_time
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic

def compare_tabu_search(num_runways, case_file="1"):
    selected_file = f"cases/case{case_file}.txt"
    cases = readFile(selected_file)

    for idx, case in enumerate(cases, start=1):
        print(f"\n=== Caso {case_file} ===")

        start_time = process_time()
        order_det, cost_det = greedy_deterministic(case, num_runways=num_runways, test=True)
        time_det_seed = process_time() - start_time
        print(f"Semilla Determinista: costo = {cost_det:.1f}, tiempo = {time_det_seed:.4f} s")

        seed = int(time.time() * 1000) % (10**8)
        start_time = process_time()
        order_sto, cost_sto = greedy_stochastic(case, seed=seed, alpha=0.3,
                                                num_runways=num_runways, test=True)
        time_sto_seed = process_time() - start_time
        print(f"Semilla Estocástica: costo = {cost_sto:.1f}, tiempo = {time_sto_seed:.4f} s\n")

        tabu_sizes      = [5, 15, 20, 25, 30]
        det_costs       = []
        sto_costs       = []
        det_times       = []
        sto_times       = []

        for tabu_size in tabu_sizes:
            print(f"--- Tamaño de lista tabú: {tabu_size} ---")

            start_td = process_time()
            _, cost_det_tabu, _ = tabu_search(case,
                                              initial_order=order_det,
                                              num_runways=num_runways,
                                              max_iter=50,
                                              tabu=tabu_size,
                                              config=1)
            time_td = process_time() - start_td
            print(f"Tabu Determinista: costo = {cost_det_tabu:.1f}, tiempo = {time_td:.4f} s")

            start_ts = process_time()
            _, cost_sto_tabu, _ = tabu_search(case,
                                              initial_order=order_sto,
                                              num_runways=num_runways,
                                              max_iter=50,
                                              tabu=tabu_size,
                                              config=2)
            time_ts = process_time() - start_ts
            print(f"Tabu Estocástico: costo = {cost_sto_tabu:.1f}, tiempo = {time_ts:.4f} s\n")

            det_costs.append(cost_det_tabu)
            sto_costs.append(cost_sto_tabu)
            det_times.append(time_td)
            sto_times.append(time_ts)

        fig, axes = plt.subplots(2, 1, figsize=(8, 10))

        axes[0].plot(tabu_sizes, det_costs, marker='o', label='Determinista')
        axes[0].plot(tabu_sizes, sto_costs, marker='o', label='Estocástico')
        axes[0].set_title(f'Costo vs Tamaño de Lista Tabú (Caso {case_file})')
        axes[0].set_xlabel('Tamaño Tabú')
        axes[0].set_ylabel('Costo')
        axes[0].legend()

        axes[1].plot(tabu_sizes, det_times, marker='o', label='Determinista')
        axes[1].plot(tabu_sizes, sto_times, marker='o', label='Estocástico')
        axes[1].set_title(f'Tiempo de CPU vs Tamaño de Lista Tabú (Caso {case_file})')
        axes[1].set_xlabel('Tamaño Tabú')
        axes[1].set_ylabel('Tiempo (s)')
        axes[1].legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    num_runways = int(input("Ingrese el número de pistas (1 o 2): "))
    case_file  = input("Ingrese el número del archivo de caso: ")
    compare_tabu_search(num_runways, case_file)
