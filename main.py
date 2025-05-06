from readFile import readFile
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic
import time
from grasp.deterministic_hc import grasp_deterministic_hc
from grasp.stochastic_hc import grasp_stochastic_hc_restart

cases = readFile("cases/case1.txt")

for i, case in enumerate(cases):
    order, cost = greedy_deterministic(case, num_runways=2, test=True)
    print("\nOrden de aterrizaje:", order)
    print("Costo total:", cost)        

for i, caso in enumerate(cases):
    print(f"\n=== Greedy Estocástico ===")
    resultados = []

    for j in range(10):
        seed = int(time.time() * 1000) % (10**8) + j
        print("\nEjecución ", j+1)
        order, cost = greedy_stochastic(caso, seed=seed, alpha=0.3, num_runways=2, test=True)
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
    order, cost = grasp_deterministic_hc(case, num_runways=2, max_iter=4, test=True)
    print("Solución final:", order)
    print("Coste final:", cost)

print("=== GRASP ESTOCÁSTICO + HC (mejor mejora) + RESTART ===")
for idx, case in enumerate(cases, start=1):
    print(f"\n=== CASO {idx} ===")
    order, cost = grasp_stochastic_hc_restart(
        case,
        alpha=0.3,
        num_runways=2,
        max_iter=10,
        max_restarts=3,
        test=True
    )
    print("Solución final:", order)
    print("Coste final:", cost)
