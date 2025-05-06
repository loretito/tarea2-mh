from greedy.deterministic import greedy_deterministic

def evaluate(order, airplanes, separation, num_runways=1):
    D = len(order)
    times = [None] * D
    runways = [[] for _ in range(num_runways)]

    for idx in order:
        E, P, L, C, C_ = airplanes[idx]
        best_cost = float('inf')
        best_t = None
        best_r = None

        for r, runway in enumerate(runways):
            t0 = E
            if runway:
                last = runway[-1]
                t0 = max(t0, times[last] + separation[last][idx])
            # probar todos los t posibles
            for t in range(int(t0), int(L) + 1):
                ok = True
                for prev in runway:
                    if abs(t - times[prev]) < separation[prev][idx]:
                        ok = False
                        break
                if not ok:
                    continue

                if   t < P: cost = C * (P - t)
                elif t > P: cost = C_ * (t - P)
                else:       cost = 0

                if cost < best_cost:
                    best_cost, best_t, best_r = cost, t, r
                    if cost == 0:
                        break
            if best_cost == 0:
                break

        if best_r is None:
            return float('inf')

        times[idx] = best_t
        runways[best_r].append(idx)

    total = 0.0
    for i, t in enumerate(times):
        P = airplanes[i][1]
        C = airplanes[i][3]
        C_ = airplanes[i][4]
        total += abs(t - P) * (C if t < P else C_)
    return total


def hill_climbing(order, airplanes, separation, num_runways=1):
    current = order[:]
    best_cost = evaluate(current, airplanes, separation, num_runways)

    while True:
        best_swap = None
        best_cost_after = best_cost

        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                neigh = current[:]
                neigh[i], neigh[j] = neigh[j], neigh[i]
                c = evaluate(neigh, airplanes, separation, num_runways)
                if c < best_cost_after:
                    best_cost_after = c
                    best_swap = neigh

        if best_swap is not None:
            current = best_swap
            best_cost = best_cost_after
        else:
            break

    return current, best_cost


def grasp_deterministic_hc(case, num_runways=1, max_iter=1, test=False):
    airplanes, separation = case
    best_order, best_cost = None, float('inf')

    for _ in range(max_iter):
        init_order, init_cost = greedy_deterministic(case, num_runways, test=True)
        hc_order, hc_cost   = hill_climbing(init_order, airplanes, separation, num_runways)
        if test == False:
            print(f"\n→ Tras HC: coste {init_cost:.1f} → {hc_cost:.1f}\n")
        if hc_cost < best_cost:
            best_order, best_cost = hc_order, hc_cost
    if test == False:
        print(f"✨ Mejor solución luego de GRASP con greedy determinista: {best_order} con coste {best_cost:.1f}")
    return best_order, best_cost
