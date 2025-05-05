import random
from typing import List, Tuple

def greedy_stochastic(case: Tuple[List[List[float]], List[List[float]]],
                      seed: int = None,
                      alpha: float = 0.3,
                      num_runways: int = 1
                     ) -> Tuple[List[int], float]:
    airplanes, separation = case
    D = len(airplanes)
    random.seed(seed)

    available = set(range(D))
    order: List[int] = []
    times: List[float] = [None] * D
    runways: List[List[int]] = [[] for _ in range(num_runways)]

    while available:
        candidates = sorted(available, key=lambda k: airplanes[k][1])
        lrc = candidates[:max(1, int(len(candidates)*alpha))]
        selected = random.choice(lrc)

        E, P, L, C, C_ = airplanes[selected]
        best_runway = None
        best_time = None
        best_cost = float('inf')

        for r_id, runway in enumerate(runways):
            t0 = E
            if runway:
                last = runway[-1]
                t0 = max(t0, times[last] + separation[last][selected])

            for t in range(int(t0), int(L) + 1):
                # separación mínima
                if any(abs(t - times[p]) < separation[p][selected] for p in runway):
                    continue
                cost = C*(P - t) if t < P else C_*(t - P) if t > P else 0
                if cost < best_cost:
                    best_cost, best_time, best_runway = cost, t, r_id
                if best_cost == 0:
                    break

        if best_runway is None:
            fallback_t, fallback_r = float('inf'), None
            for r_id, runway in enumerate(runways):
                t0 = E
                if runway:
                    last = runway[-1]
                    t0 = max(t0, times[last] + separation[last][selected])
                t_clamped = min(t0, L)
                if t_clamped < fallback_t:
                    fallback_t, fallback_r = t_clamped, r_id
            best_time = fallback_t
            best_runway = fallback_r
            best_cost = C*(P - best_time) if best_time < P else C_*(best_time - P)

        times[selected] = best_time
        runways[best_runway].append(selected)
        order.append(selected)
        available.remove(selected)

    total_cost = 0.0
    GREEN = "\033[92m"
    RED   = "\033[91m"
    YELLOW= "\033[93m"
    BLUE  = "\033[94m"
    RESET = "\033[0m"

    print(f"\n=== Aterrizajes Estocásticos ===\n")
    print(f"{'Avión':<11} {'Tiempo':<9} {'P':<12} {'Pista':<10} {'Penalización'}")
    print("-" * 56)

    chronological = sorted(range(D), key=lambda i: times[i])
    for i in chronological:
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

    print(f"\n Orden de aterrizaje: {order}")
    print(f"Costo total: {total_cost:.1f}\n")

    return order, total_cost
