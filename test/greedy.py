import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from readFile import readFile
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic
from time import process_time

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def compare_algorithms(num_runways, case_file="1"):
    selected_file = "cases/case" + case_file + ".txt"
    
    cases = readFile(selected_file)

    results = {
        'case': [],
        'greedy_det_cost': [],
        'greedy_sto_costs': [],  
        'greedy_det_time': [],
        'greedy_sto_times': [],  
    }

    for idx, case in enumerate(cases, start=1):
        print(f"\n{GREEN}=== Caso {case_file} ==={RESET}")

        start_time = process_time()
        order_det, cost_det = greedy_deterministic(case, num_runways=num_runways, test=True)
        end_time = process_time()
        time_det = end_time - start_time
        print(f"{YELLOW}Greedy determinista:{RESET}")
        print(f"  Costo = {cost_det:.1f}, Tiempo = {time_det:.4f} segundos")

        costs = []
        times = []
        orders = []
        
        print(f"\n{YELLOW}Greedy estocástico:{RESET}")
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

        print(f"\nPromedio estocástico:")
        print(f"  Costo promedio  = {avg_cost_sto:.1f}, Tiempo promedio = {avg_time_sto:.4f} segundos\n")

        results['case'].append(f'Caso {case_file}')
        results['greedy_det_cost'].append(cost_det)
        results['greedy_sto_costs'].append(costs)  
        results['greedy_det_time'].append(time_det)
        results['greedy_sto_times'].append(times)  

    df = pd.DataFrame(results)

    avg_cost_det = np.mean(df['greedy_det_cost'])
    avg_cpu_det = np.mean(df['greedy_det_time'])

    avg_cost_sto = np.mean([np.mean(costs) for costs in df['greedy_sto_costs']])
    avg_cpu_sto = np.mean([np.mean(times) for times in df['greedy_sto_times']])

    print(f"\n{BLUE}Tabla comparativa:{RESET}")
    print(f"{MAGENTA}Promedio Costo - Greedy Determinista:{RESET} {avg_cost_det:.1f}")
    print(f"{MAGENTA}Promedio Costo - Greedy Estocástico:{RESET} {avg_cost_sto:.1f}")
    print(f"{CYAN}Promedio Tiempo de CPU - Greedy Determinista:{RESET} {avg_cpu_det:.6f} segundos")
    print(f"{CYAN}Promedio Tiempo de CPU - Greedy Estocástico:{RESET} {avg_cpu_sto:.6f} segundos\n\n")

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    for idx, case in enumerate(df['case']):
        ax[0].plot(range(1, 11), df['greedy_sto_costs'][idx], label="Greedy Estocástico", marker='o', color='green')
        ax[0].plot([1, 10], [df['greedy_det_cost'][idx], df['greedy_det_cost'][idx]], label="Greedy Determinista", marker='o', color='orange')

    ax[0].set_title(f'Comparación de Costos (Determinista vs Estocástico)')
    ax[0].set_xlabel('Iteraciones')
    ax[0].set_ylabel('Costo')
    ax[0].legend()

    for idx, case in enumerate(df['case']):
        ax[1].plot(range(1, 11), df['greedy_sto_times'][idx], label="Greedy Estocástico", marker='o', color='green')
        ax[1].plot([1, 10], [df['greedy_det_time'][idx], df['greedy_det_time'][idx]], label="Greedy Determinista", marker='o', color='orange')

    ax[1].set_title(f'Comparación de Tiempos de CPU (Determinista vs Estocástico)')
    ax[1].set_xlabel('Iteraciones')
    ax[1].set_ylabel('Tiempo de CPU (segundos)')
    ax[1].legend()

    for axis in ax:
        axis.set_xticks(range(1, 11))
        axis.set_xticklabels([f'{i}' for i in range(1, 11)])

    plt.suptitle(f'Caso {case_file}: Comparación de Algoritmos (Greedy Determinista vs Estocástico)', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

if __name__ == "__main__":
    num_runways = int(input("Ingrese el número de pistas (1 o 2): "))
    case_file = input("Ingrese el número del archivo de caso: ")
    compare_algorithms(num_runways, case_file)
