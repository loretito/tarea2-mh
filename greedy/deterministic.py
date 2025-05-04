def greedy_deterministic(case, num_runways=1):
    airplane, separation = case
    D = len(airplane)

    order = sorted(range(D), key=lambda k: airplane[k][1]) 

    print("Cantidad de Pistas:", num_runways)

    times = [None] * D
    runways = [[] for _ in range(num_runways)]

    for current in order:
        E, P, L, C, C_ = airplane[current]

        best_runway = None
        best_time = None
        best_cost = float('inf')

        for i, runway in enumerate(runways):
            t_start = E
            if runway:
                last = runway[-1]
                t_start = max(t_start, times[last] + separation[last][current])

            for t in range(int(t_start), int(L) + 1):
                conflict = False
                for prev in runway:
                    if abs(t - times[prev]) < separation[prev][current]:
                        conflict = True
                        break
                if conflict:
                    continue

                if t < P:
                    cost = C * (P - t)
                elif t > P:
                    cost = C_ * (t - P)
                else:
                    cost = 0

                if cost < best_cost:
                    best_cost = cost
                    best_time = t
                    best_runway = i

                if cost == 0:
                    break

        if best_runway is None:
            raise Exception(f"No se pudo asignar avión {current} dentro de su ventana")

        times[current] = best_time
        runways[best_runway].append(current)

    total_cost = 0.0
    
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    print(f"\n=== Aterrizajes ===\n")
    print(f"{'Avión':<11} {'Tiempo':<9} {'P':<12} {'Pista':<10} {'Penalización'}")
    print("-" * 50)

    chronological_order = sorted(range(D), key=lambda i: times[i])
    for i in chronological_order:
        E, P, L, C, C_ = airplane[i]
        t = times[i]
        delta = t - P
        runway_i = next(pi for pi, p in enumerate(runways) if i in p)
        sign = "<" if delta < 0 else ">" if delta > 0 else "="
        penalty = abs(delta) * (C if delta < 0 else C_)
        total_cost += penalty

        color = GREEN if penalty == 0 else RED
        print(f"{BLUE}Avión {i:<2}{RESET}   "
            f"{t:>6.1f}    ({sign} P={P:<5.1f})   "
            f"{YELLOW}Pista {runway_i}{RESET:<4}    "
            f"{color}{penalty:.1f}{RESET}")

    return order, total_cost
