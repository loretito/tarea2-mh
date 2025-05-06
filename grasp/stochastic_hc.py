import time
from typing import List, Tuple
from greedy.stochastic import greedy_stochastic

def evaluate(order: List[int],
             airplanes: List[List[float]],
             separation: List[List[float]],
             num_runways: int = 1
            ) -> float:
    
    D = len(order)
    times = [None] * D
    runways = [[] for _ in range(num_runways)]

    for idx in order:
        E, P, L, C, C_ = airplanes[idx]
        best_cost = float('inf')
        best_t = None
        best_r = None

        for r_id, runway in enumerate(runways):
            t0 = E
            if runway:
                last = runway[-1]
                t0 = max(t0, times[last] + separation[last][idx])

            for t in range(int(t0), int(L) + 1):
                # verificar separación mínima
                if any(abs(t - times[p]) < separation[p][idx] for p in runway):
                    continue

                cost = C*(P - t) if t < P else (C_*(t - P) if t > P else 0)
                if cost < best_cost:
                    best_cost, best_t, best_r = cost, t, r_id
                    if cost == 0:
                        break
            if best_cost == 0:
                break

        if best_r is None:
            best_r = 0
            best_t = min(L, max(E, times[runways[0][-1]] + separation[runways[0][-1]][idx]) if runways[0] else E)
            best_cost = C*(P - best_t) if best_t < P else C_*(best_t - P)

        times[idx] = best_t
        runways[best_r].append(idx)

    total = 0.0
    for i, t in enumerate(times):
        _, P, _, C, C_ = airplanes[i]
        delta = t - P
        total += abs(delta) * (C if delta < 0 else C_)
    return total


def hill_climbing_best(order: List[int],
                       airplanes: List[List[float]],
                       separation: List[List[float]],
                       num_runways: int = 1
                      ) -> Tuple[List[int], float]:

    current = order[:]
    best_cost = evaluate(current, airplanes, separation, num_runways)

    improved = True
    while improved:
        improved = False
        best_swap = None

        for i in range(len(current)):
            for j in range(i+1, len(current)):
                neigh = current[:]
                neigh[i], neigh[j] = neigh[j], neigh[i]
                c = evaluate(neigh, airplanes, separation, num_runways)
                if c < best_cost:
                    best_cost = c
                    best_swap = neigh

        if best_swap is not None:
            current = best_swap
            improved = True

    return current, best_cost


def grasp_stochastic_hc_restart(case: Tuple[List[List[float]], List[List[float]]],
                                alpha: float = 0.3,
                                num_runways: int = 1,
                                max_iter: int = 10,
                                max_restarts: int = 3,
                                test = False
                               ) -> Tuple[List[int], float]:
    airplanes, separation = case
    best_order: List[int] = []
    best_cost = float('inf')

    for rr in range(1, max_restarts + 1):
        if test == False:
            print(f"\n--- Restart {rr}/{max_restarts} ---")
        base_seed = int(time.time() * 1000) % (10**8)

        for it in range(1, max_iter + 1):
            if test == False:
                print(f"\nIteración {it}/{max_iter}")
            init_order, init_cost = greedy_stochastic(
                case,
                seed=base_seed + it,
                alpha=alpha,
                num_runways=num_runways,
                test=test
            )

            hc_order, hc_cost = hill_climbing_best(
                init_order, airplanes, separation, num_runways
            )
            if test == False:
                print(f"→ Tras HC: coste {init_cost:.1f} → {hc_cost:.1f}")

            if hc_cost >= init_cost:
                if test == False:
                    print("⚠️  HC no mejoró la solución estocástica, forzando restart.")
                break

            if hc_cost < best_cost:
                best_cost = hc_cost
                best_order = hc_order[:]

    if test == False:
        print(f"\n✨ Mejor solución con GRASP estocastico HC con restart: {best_order} con coste {best_cost:.1f}\n")
    return best_order, best_cost
