import random
from typing import List, Tuple


def tabu_search(case: Tuple[List[List[float]], List[List[float]]],
                initial_order: List[int],
                max_iter: int = 100,
                tabu: int = 10,
                config: int = 1,
                num_runways: int = 2
               ) -> Tuple[List[int], float, List[Tuple[int, float]]]:
    
    airplane, separation = case
    D = len(airplane)
    
    def evaluate(order: List[int]) -> Tuple[float, List[float]]:
        times = [0.0] * D
        runways = [[] for _ in range(num_runways)]
        total_cost = 0.0
        
        for plane in order:
            E, P, L, C, C_ = airplane[plane]
            best_c = float('inf')
            best_t = None
            best_r = None

            for r_id, runway in enumerate(runways):
                t0 = E
                if runway:
                    last = runway[-1]
                    t0 = max(t0, times[last] + separation[last][plane])
                if t0 > L:
                    continue
                if t0 < P:
                    c = C * (P - t0)
                elif t0 > P:
                    c = C_ * (t0 - P)
                else:
                    c = 0
                if c < best_c or (c == best_c and (best_t is None or t0 < best_t)):
                    best_c, best_t, best_r = c, t0, r_id

            if best_r is None:
                return float('inf'), []

            times[plane] = best_t
            runways[best_r].append(plane)
            total_cost += best_c

        return total_cost, times

    current = initial_order[:]
    best = current[:]
    best_cost, _ = evaluate(best)
    tabu_list: List[Tuple] = []
    history: List[Tuple[int, float]] = []

    MAX_NEIGH = 100

    for it in range(max_iter):
        neighbors = []
        if config == 1:
            for i in range(D):
                for j in range(i+1, D):
                    n = current[:]
                    n[i], n[j] = n[j], n[i]
                    neighbors.append((n, (i, j)))
        elif config == 2:
            for i in range(D):
                for j in range(i+1, D):
                    n = current[:]
                    n.insert(j, n.pop(i))
                    neighbors.append((n, (i, j)))
        elif config == 3:
            for i in range(D-2):
                n = current[:]
                n[i:i+3] = reversed(n[i:i+3])
                neighbors.append((n, (i, i+3)))
        elif config == 4:
            for k in range(1, D):
                n = current[-k:] + current[:-k]
                neighbors.append((n, ('shift', k)))
        else:
            for i in range(D):
                for j in range(i+1, D):
                    n = current[:]
                    n[i], n[j] = n[j], n[i]
                    neighbors.append((n, ('swap', i, j)))
                if i < D-2:
                    n = current[:]
                    n[i:i+3] = reversed(n[i:i+3])
                    neighbors.append((n, ('rev', i)))

        random.shuffle(neighbors)
        neighbors = neighbors[:MAX_NEIGH]

        candidate = None
        candidate_cost = float('inf')
        candidate_move = None
        for neigh, move in neighbors:
            cost, _ = evaluate(neigh)
            if move in tabu_list and cost >= best_cost:
                continue
            if cost < candidate_cost:
                candidate, candidate_cost, candidate_move = neigh, cost, move
                if cost < best_cost:
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
