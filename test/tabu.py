import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from readFile import readFile
from tabuSearch import tabu_search
from time import process_time
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic

def compare_tabu_search(num_runways, case_file="1"):
    selected_file = "cases/case" + case_file + ".txt"
    
    cases = readFile(selected_file)

    results = {
        'case': [],
        'tabu_det_cost': [],
        'tabu_sto_costs': [],  
        'tabu_det_time': [],
        'tabu_sto_times': [],
        'tabu_size': []  
    }

    for idx, case in enumerate(cases, start=1):
        print(f"\n=== Caso {case_file} ===")

        print(f"Obteniendo resultados para Tabu Determinista y Estocástico con tamaño de lista {len(case[0])}")

        start_time = process_time()
        order_det, cost_det = greedy_deterministic(case, num_runways=num_runways, test=True)
        end_time = process_time()
        time_det = end_time - start_time
        print(f"Tabu Determinista: costo = {cost_det:.1f}, tiempo = {time_det:.4f} segundos")

        costs = []
        times = []
        orders = []
        
        print(f"Tabu Estocástico (10 iteraciones):")
        for run in range(1, 11):
            seed = int(time.time() * 1000) % (10**8) + run
            start_run_time = process_time()
            order_sto, cost_sto = greedy_stochastic(case, seed=seed, alpha=0.3, num_runways=num_runways, test=True)
            end_run_time = process_time()
            run_time = end_run_time - start_run_time
            costs.append(cost_sto)
            times.append(run_time)
            orders.append(order_sto)
            print(f"  Iteración {run:2d}: costo = {cost_sto:.1f}, tiempo = {run_time:.4f} segundos")
            time.sleep(0.01)

        avg_cost_sto = np.mean(costs)
        avg_time_sto = np.mean(times)
        print(f"\nPromedio Estocástico:")
        print(f"  Costo promedio  = {avg_cost_sto:.1f}, Tiempo promedio = {avg_time_sto:.4f} segundos\n")

        results['case'].append(f'Caso {case_file}')
        results['tabu_det_cost'].append(cost_det)
        results['tabu_sto_costs'].append(costs)
        results['tabu_det_time'].append(time_det)
        results['tabu_sto_times'].append(times)

        for tabu_size in [5, 15, 30, 40, 60]:  
            print(f"\n=== Probando tamaño de tabu {tabu_size} ===")

            start_time = process_time()
            order_det, cost_det, _ = tabu_search(case, initial_order=order_det, num_runways=num_runways, max_iter=100, tabu=tabu_size, config=2)
            end_time = process_time()
            time_det = end_time - start_time
            print(f"Tabu Determinista: costo = {cost_det:.1f}, tiempo = {time_det:.4f} segundos")

            costs = []
            times = []
            print(f"Tabu Estocástico (10 iteraciones):")
            for run in range(1, 11):
                seed = int(time.time() * 1000) % (10**8) + run
                start_run_time = process_time()
                order_sto, cost_sto, _ = tabu_search(case, initial_order=orders[run-1], num_runways=num_runways, max_iter=100, tabu=tabu_size, config=2)
                end_run_time = process_time()
                run_time = end_run_time - start_run_time
                costs.append(cost_sto)
                times.append(run_time)
                print(f"  Iteración {run:2d}: costo = {cost_sto:.1f}, tiempo = {run_time:.4f} segundos")
                time.sleep(0.01)

            avg_cost_sto = np.mean(costs)
            avg_time_sto = np.mean(times)
            print(f"\nPromedio Estocástico | Tamaño de tabu {tabu_size}:")
            print(f"  Costo promedio  = {avg_cost_sto:.1f}, Tiempo promedio = {avg_time_sto:.4f} segundos\n")

            results['tabu_size'].append(tabu_size)
            results['tabu_det_cost'].append(cost_det)
            results['tabu_sto_costs'].append(costs)
            results['tabu_det_time'].append(time_det)
            results['tabu_sto_times'].append(times)

            avg_cost_det = np.mean(results['tabu_det_cost'])
            avg_cpu_det = np.mean(results['tabu_det_time'])
            avg_cost_sto = np.mean([np.mean(costs) for costs in results['tabu_sto_costs']])
            avg_cpu_sto = np.mean([np.mean(times) for times in results['tabu_sto_times']])

            print(f"Tabla comparativa | Tamaño de tabu {tabu_size}:")
            print(f"Promedio Costo - Tabu Determinista: {avg_cost_det:.1f}")
            print(f"Promedio Costo - Tabu Estocástico: {avg_cost_sto:.1f}")
            print(f"Promedio Tiempo de CPU - Tabu Determinista: {avg_cpu_det:.6f} segundos")
            print(f"Promedio Tiempo de CPU - Tabu Estocástico: {avg_cpu_sto:.6f} segundos\n")

            fig, ax = plt.subplots(2, 1, figsize=(10, 10))

            ax[0].plot(range(1, 11), costs, label=f"Estocástico Tamaño {tabu_size}", marker='o', color='green')
            ax[0].plot([1, 10], [cost_det, cost_det], label="Determinista", marker='o', color='orange')

            ax[0].set_title(f'Comparación de Costos (Determinista vs Estocástico) | Tamaño tabu {tabu_size}')
            ax[0].set_xlabel('Iteraciones')
            ax[0].set_ylabel('Costo')
            ax[0].legend()

            ax[1].plot(range(1, 11), times, label=f"Estocástico Tamaño {tabu_size}", marker='o', color='green')
            ax[1].plot([1, 10], [time_det, time_det], label="Determinista", marker='o', color='orange')

            ax[1].set_title(f'Comparación de Tiempos de CPU (Determinista vs Estocástico) | Tamaño tabu {tabu_size}')
            ax[1].set_xlabel('Iteraciones')
            ax[1].set_ylabel('Tiempo de CPU (segundos)')
            ax[1].legend()

            for axis in ax:
                axis.set_xticks(range(1, 11))
                axis.set_xticklabels([f'{i}' for i in range(1, 11)])

            plt.suptitle(f'Caso {case_file}: Comparación de Algoritmos (Tamaño tabu {tabu_size})', fontsize=16)
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            plt.show()

if __name__ == "__main__":
    num_runways = int(input("Ingrese el número de pistas (1 o 2): "))
    case_file = input("Ingrese el número del archivo de caso: ")
    compare_tabu_search(num_runways, case_file)
