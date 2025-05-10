import random
from typing import List, Tuple

def tabu_search(case: Tuple[List[List[float]], List[List[float]]],
                initial_order: List[int],
                max_iter: int = 100,
                tabu: int = 10,
                config: int = 2,
                num_runways: int = 2
               ) -> Tuple[List[int], float, List[Tuple[int, float]]]:

    airplanes, separation = case
    D = len(airplanes)

    def evaluate(order: List[int]) -> Tuple[float, List[float]]:
        times = [0.0] * D
        runways = [[] for _ in range(num_runways)]
        total = 0.0

        for plane in order:
            E, P, L, C, C_ = airplanes[plane]
            best_c = float('inf')
            best_t = None
            best_r = None

            for r_id, runway in enumerate(runways):
                for t in range(int(E), int(L) + 1):
                    if any(t < times[p] + separation[p][plane] for p in runway):
                        continue
                    c = C * (P - t) if t < P else C_ * (t - P) if t > P else 0
                    if c < best_c or (c == best_c and (best_t is None or t < best_t)):
                        best_c, best_t, best_r = c, t, r_id
                if best_c == 0:
                    break

            if best_r is None:
                min_earliest = float('inf')
                for r_id, runway in enumerate(runways):
                    if runway:
                        last = runway[-1]
                        earliest = max(times[last] + separation[last][plane], E)
                    else:
                        earliest = E
                    t_clamped = min(earliest, L)
                    if t_clamped < min_earliest:
                        min_earliest = t_clamped
                        best_r = r_id
                        best_t = t_clamped
                best_c = C * (P - best_t) if best_t < P else C_ * (best_t - P)

            times[plane] = best_t
            runways[best_r].append(plane)
            total += best_c

        return total, times

    current = initial_order[:]
    cost0, _ = evaluate(current)
    if cost0 == float('inf'):
        raise ValueError("La solución inicial NO es factible para el scheduling.")

    best, best_cost = current[:], cost0
    tabu_list: List[Tuple] = []
    history: List[Tuple[int, float]] = []

    MAX_NEIGH = 10
    
    for it in range(max_iter):
        neighs: List[Tuple[List[int], Tuple]] = []
        if config == 1:
            for i in range(D):
                for j in range(i + 1, D):
                    n = current[:]; n[i], n[j] = n[j], n[i]
                    neighs.append((n, (i, j)))
        elif config == 2:
            for i in range(D):
                for j in range(i + 1, D):
                    n = current[:]; n.insert(j, n.pop(i))
                    neighs.append((n, (i, j)))
        elif config == 3:
            for i in range(D - 2):
                n = current[:]; n[i:i+3] = reversed(n[i:i+3])
                neighs.append((n, (i, i+3)))
        elif config == 4:
            for k in range(1, D):
                n = current[-k:] + current[:-k]
                neighs.append((n, ('shift', k)))
        else:
            for i in range(D):
                for j in range(i + 1, D):
                    n = current[:]; n[i], n[j] = n[j], n[i]
                    neighs.append((n, ('swap', i, j)))
                if i < D - 2:
                    n = current[:]; n[i:i+3] = reversed(n[i:i+3])
                    neighs.append((n, ('rev', i)))

        random.shuffle(neighs)
        neighs = neighs[:MAX_NEIGH]

        candidate = None
        candidate_cost = float('inf')
        candidate_move = None
        for n, move in neighs:
            c, _ = evaluate(n)
            if move in tabu_list and c >= best_cost:
                continue
            if c < candidate_cost:
                candidate, candidate_cost, candidate_move = n, c, move
                if c < best_cost:
                    break

        if candidate is None:
            break

        current = candidate
        if candidate_cost < best_cost:
            best, best_cost = current[:], candidate_cost

        tabu_list.append(candidate_move)
        if len(tabu_list) > tabu:
            tabu_list.pop(0)

        history.append((it, best_cost))

    return best, best_cost, history
