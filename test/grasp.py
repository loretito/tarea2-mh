import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple
from readFile import readFile
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def test_grasp_deterministic(case, num_runways=1, max_iter=10, test=False):
    best_order, best_cost = None, float('inf')

    for _ in range(max_iter):
        init_order, init_cost = greedy_deterministic(case, num_runways, test=True) 

        if test == False:
            print(f"\n→ Costo de la solución determinista: {init_cost:.1f}")

        if init_cost < best_cost:
            best_order, best_cost = init_order, init_cost

    if test == False:
        print(f"✨ Mejor solución luego de GRASP con greedy determinista: {best_order} con coste {best_cost:.1f}")

    return best_order, best_cost

def test_grasp_stochastic(case: Tuple[List[List[float]], List[List[float]]],
                          alpha: float = 0.3,
                          num_runways: int = 1,
                          max_iter: int = 10,
                          test=False) -> Tuple[List[int], float]:
    best_order: List[int] = []
    best_cost = float('inf')

    for it in range(1, max_iter + 1):
        if test == False:
            print(f"\nIteración {it}/{max_iter}")

        init_order, init_cost = greedy_stochastic(
            case,
            alpha=alpha,
            num_runways=num_runways,
            test=test
        )

        if test == False:
            print(f"→ Costo inicial: {init_cost:.1f}")

        if init_cost < best_cost:
            best_cost = init_cost
            best_order = init_order

    if test == False:
        print(f"✨ Mejor solución con GRASP estocástico: {best_order} con coste {best_cost:.1f}\n")

    return best_order, best_cost

def compare_grasp_algorithms(num_runways, case_file="1"):
    selected_file = "cases/case" + case_file + ".txt"
    cases = readFile(selected_file)

    results = {
        'case': [],
        'grasp_det_cost': [],
        'grasp_sto_costs': [],
        'grasp_det_time': [],
        'grasp_sto_times': [],
        'grasp_det_order': [],
        'grasp_sto_best_order': [],
        'grasp_sto_best_iter': []
    }

    for idx, case in enumerate(cases, start=1):
        print(f"\n{GREEN}=== Caso {case_file} ==={RESET}")

        start_time = time.process_time()
        order_det, cost_det = test_grasp_deterministic(case, num_runways=num_runways, max_iter=10, test=False)
        end_time = time.process_time()
        time_det = end_time - start_time
        print(f"{YELLOW}GRASP Determinista:{RESET}")
        print(f"  Costo = {cost_det:.1f}, Tiempo = {time_det:.4f} segundos")
        print(f"  Orden determinista: {order_det}")

        costs = []
        times = []
        orders = []

        best_sto_order = None
        best_sto_iter = None
        min_cost_sto = float('inf')

        print(f"\n{YELLOW}GRASP Estocástico:{RESET}")
        for run in range(1, 11):
            seed = int(time.time() * 1000) % (10**8) + run
            start_run_time = time.process_time()
            order_sto, cost_sto = test_grasp_stochastic(case, alpha=0.3, num_runways=num_runways, max_iter=10, test=False)
            end_run_time = time.process_time()
            run_time = end_run_time - start_run_time
            costs.append(cost_sto)
            times.append(run_time)
            orders.append(order_sto)
            print(f"  Iteración {run:2d}: costo = {cost_sto:.1f}, tiempo = {run_time:.4f} segundos")
            time.sleep(0.01)

            if cost_sto < min_cost_sto:
                min_cost_sto = cost_sto
                best_sto_order = order_sto
                best_sto_iter = run

        avg_cost_sto = np.mean(costs)
        avg_time_sto = np.mean(times)

        print(f"\nPromedio estocástico:")
        print(f"  Costo promedio  = {avg_cost_sto:.1f}, Tiempo promedio = {avg_time_sto:.4f} segundos\n")
        print(f"  Mejor orden estocástico (Iteración {best_sto_iter}): {best_sto_order}")

        results['case'].append(f'Caso {case_file}')
        results['grasp_det_cost'].append(cost_det)
        results['grasp_sto_costs'].append(costs)
        results['grasp_det_time'].append(time_det)
        results['grasp_sto_times'].append(times)
        results['grasp_det_order'].append(order_det)
        results['grasp_sto_best_order'].append(best_sto_order)
        results['grasp_sto_best_iter'].append(best_sto_iter)

    df = pd.DataFrame(results)

    avg_cost_det = np.mean(df['grasp_det_cost'])
    avg_cpu_det = np.mean(df['grasp_det_time'])

    avg_cost_sto = np.mean([np.mean(costs) for costs in df['grasp_sto_costs']])
    avg_cpu_sto = np.mean([np.mean(times) for times in df['grasp_sto_times']])

    print(f"\n{BLUE}Tabla comparativa:{RESET}")
    print(f"{MAGENTA}Promedio Costo - GRASP Determinista:{RESET} {avg_cost_det:.1f}")
    print(f"{MAGENTA}Promedio Costo - GRASP Estocástico:{RESET} {avg_cost_sto:.1f}")
    print(f"{CYAN}Promedio Tiempo de CPU - GRASP Determinista:{RESET} {avg_cpu_det:.6f} segundos")
    print(f"{CYAN}Promedio Tiempo de CPU - GRASP Estocástico:{RESET} {avg_cpu_sto:.6f} segundos\n\n")

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    for idx, case in enumerate(df['case']):
        ax[0].plot(range(1, 11), df['grasp_sto_costs'][idx], label="GRASP Estocástico", marker='o', color='green')
        ax[0].plot([1, 10], [df['grasp_det_cost'][idx], df['grasp_det_cost'][idx]], label="GRASP Determinista", marker='o', color='orange')

    ax[0].set_title(f'Comparación de Costos (Determinista vs Estocástico)')
    ax[0].set_xlabel('Iteraciones')
    ax[0].set_ylabel('Costo')
    ax[0].legend()

    for idx, case in enumerate(df['case']):
        ax[1].plot(range(1, 11), df['grasp_sto_times'][idx], label="GRASP Estocástico", marker='o', color='green')
        ax[1].plot([1, 10], [df['grasp_det_time'][idx], df['grasp_det_time'][idx]], label="GRASP Determinista", marker='o', color='orange')

    ax[1].set_title(f'Comparación de Tiempos de CPU (Determinista vs Estocástico)')
    ax[1].set_xlabel('Iteraciones')
    ax[1].set_ylabel('Tiempo de CPU (segundos)')
    ax[1].legend()

    for axis in ax:
        axis.set_xticks(range(1, 11))
        axis.set_xticklabels([f'{i}' for i in range(1, 11)])

    plt.suptitle(f'Caso {case_file}: Comparación de Algoritmos GRASP (Determinista vs Estocástico)', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

if __name__ == "__main__":
    num_runways = int(input("Ingrese el número de pistas (1 o 2): "))
    case_file = input("Ingrese el número del archivo de caso: ")
    compare_grasp_algorithms(num_runways, case_file)
