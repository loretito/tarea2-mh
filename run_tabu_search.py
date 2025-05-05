#!/usr/bin/env python3
import glob
import time
from readFile import readFile
from greedy.deterministic import greedy_deterministic
from greedy.stochastic import greedy_stochastic
from tabuSearch.tabuSearch import tabu_search


def main():
    case_files = ['cases/case1.txt']
    all_cases = []
    for f in case_files:
        cases = readFile(f)
        all_cases.extend(cases)

    tabu_configs = [
        {'config': 1, 'max_iter': 100, 'tabu': 5},
        {'config': 2, 'max_iter': 100, 'tabu': 5},
        {'config': 3, 'max_iter': 100, 'tabu': 10},
        {'config': 4, 'max_iter': 100, 'tabu': 10},
        {'config': 5, 'max_iter': 100, 'tabu': 15},
    ]

    for idx, case in enumerate(all_cases, start=1):
        print(f"\n=== Caso {idx} ===")

        det_order, det_cost = greedy_deterministic(case, num_runways=2)
        print(f"Greedy Determinista: Orden={det_order}, Costo={det_cost:.1f}\n")

        best_sto_order = None
        best_sto_cost = float('inf')
        print("Greedy Estocástico:")
        for run in range(1, 11):
            seed = int(time.time() * 1000) % (10**8) + run
            sto_order, sto_cost = greedy_stochastic(case,
                                                    seed=seed,
                                                    alpha=0.3,
                                                    num_runways=2)
            print(f"  Run {run:2d}: Costo={sto_cost:.1f} | Orden={sto_order}")
            if sto_cost < best_sto_cost:
                best_sto_cost = sto_cost
                best_sto_order = sto_order
        print(f"Mejor Estocástico: Costo={best_sto_cost:.1f}, Orden={best_sto_order}\n")

        print("Tabu Search (5 configuraciones):")
        for cfg in tabu_configs:
            print(f"-- Conf. vecindario={cfg['config']}, iter={cfg['max_iter']}, tam. lista={cfg['tabu']}")

            _, bc_det, _ = tabu_search(case,
                                       initial_order=det_order,
                                       max_iter=cfg['max_iter'],
                                       tabu=cfg['tabu'],
                                       config=cfg['config'],
                                       num_runways=2)
            print(f"   Det -> Costo Tabu: {bc_det:.1f}")

            _, bc_sto, _ = tabu_search(case,
                                       initial_order=best_sto_order,
                                       max_iter=cfg['max_iter'],
                                       tabu=cfg['tabu'],
                                       config=cfg['config'],
                                       num_runways=2)
            print(f"   Sto -> Costo Tabu: {bc_sto:.1f}\n")

if __name__ == "__main__":
    main()
