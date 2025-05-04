import random

def greedy_stochastic(case, seed=None, alpha=0.3, num_runways=1):
    airplanes, separation = case
    D = len(airplanes)
    random.seed(seed)

    available = set(range(D))
    order = []
    times = [None] * D
    runways = [[] for _ in range(num_runways)]

    while available:
        candidates = sorted(available, key=lambda k: airplanes[k][1])  
        lrc_size = max(1, int(len(candidates) * alpha))
        lrc = candidates[:lrc_size]
        selected = random.choice(lrc)

        E, P, L, C, C_ = airplanes[selected]

        best_runway = None
        best_time = None
        best_cost = float('inf')

        for i, runway in enumerate(runways):
            t_start = E
            if runway:
                last = runway[-1]
                t_start = max(t_start, times[last] + separation[last][selected])

            for t in range(int(t_start), int(L) + 1):
                conflict = False
                for prev in runway:
                    if abs(t - times[prev]) < separation[prev][selected]:
                        conflict = True
                        break
                if conflict:
                    continue

                cost = C * (P - t) if t < P else C_ * (t - P) if t > P else 0

                if cost < best_cost:
                    best_cost = cost
                    best_time = t
                    best_runway = i

                if cost == 0:
                    break  

        if best_runway is None:
            raise Exception(f"No se pudo asignar avión {selected} dentro de su ventana")

        times[selected] = best_time
        runways[best_runway].append(selected)
        order.append(selected)
        available.remove(selected)

    total_cost = 0.0
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    print(f"=== Aterrizajes Estocásticos ===\n")
    print(f"{'Avión':<11} {'Tiempo':<9} {'P':<12} {'Pista':<10} {'Penalización'}")
    print("-" * 50)

    chronological_order = sorted(range(D), key=lambda i: times[i])
    for i in chronological_order:
        E, P, L, C, C_ = airplanes[i]
        t = times[i]
        delta = t - P
        sign = "<" if delta < 0 else ">" if delta > 0 else "="
        penalty = abs(delta) * (C if delta < 0 else C_)
        total_cost += penalty
        runway_i = next(pi for pi, p in enumerate(runways) if i in p)
        color = GREEN if penalty == 0 else RED
        print(f"{BLUE}Avión {i:<2}{RESET}   "
              f"{t:>6.1f}    ({sign} P={P:<5.1f})   "
              f"{YELLOW}Pista {runway_i}{RESET:<4}    "
              f"{color}{penalty:.1f}{RESET}")
        
    return order, total_cost
