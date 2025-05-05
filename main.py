from readFile import readFile
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic
from grasp.stochastic_hc_restart import grasp_hc_restart
import time
from grasp.deterministic_hc import grasp_deterministic_hc

cases = readFile("cases/case1.txt")

for i, case in enumerate(cases):
    order, cost = greedy_deterministic(case, num_runways=2)
    print("\nOrden de aterrizaje:", order)
    print("Costo total:", cost)        

for i, caso in enumerate(cases):
    print(f"\n=== Greedy Estocástico ===")
    resultados = []

    for j in range(10):
        seed = int(time.time() * 1000) % (10**8) + j
        print("\nEjecución ", j+1)
        order, cost = greedy_stochastic(caso, seed=seed, alpha=0.3, num_runways=2)
        resultados.append((j + 1, order, cost))
        time.sleep(0.01)

    for run_id, order, cost in resultados:
        print(f"\nEjecución {run_id}:")
        print(f"  Orden de aterrizaje: {order}")
        print(f"  Costo total: {cost:.1f}")

    mejor_run = min(resultados, key=lambda x: x[2])
    print(f"\nMejor Caso: Ejecución {mejor_run[0]} con costo = {mejor_run[2]:.1f}")

for case in cases:
    print("=== GRASP DETERMINISTA ===")
    order, cost = grasp_deterministic_hc(case, num_runways=2, max_iter=1)
    print("Solución final:", order)
    print("Coste final:", cost)
