import random
from typing import List, Tuple

def greedy_stochastic(case: Tuple[List[List[float]], List[List[float]]],
                      seed: int = None,
                      alpha: float = 0.3,
                      num_runways: int = 1,
                      test: bool = False
                     ) -> Tuple[List[int], float]:
    
    airplanes, separation = case
    D = len(airplanes)
    random.seed(seed)

    available = set(range(D))
    order: List[int] = []
    times: List[float] = [0.0] * D
    runways: List[List[int]] = [[] for _ in range(num_runways)]

    while available:
        candidates = sorted(available, key=lambda k: airplanes[k][1])
        lrc = candidates[:max(1, int(len(candidates)*alpha))]
        sel = random.choice(lrc)
        E, P, L, C, C_ = airplanes[sel]

        best_r = None
        best_t = None
        best_c = float('inf')

        for r_id, runway in enumerate(runways):
            for t in range(int(E), int(L)+1):
                ok = True
                for p in runway:
                    if t < times[p] + separation[p][sel]:
                        ok = False
                        break
                if not ok:
                    continue
                if t < P:
                    c = C*(P-t)
                elif t > P:
                    c = C_*(t-P)
                else:
                    c = 0
                if c < best_c:
                    best_c, best_t, best_r = c, t, r_id
                    if c == 0:
                        break
            if best_r is not None and best_c == 0:
                break

        if best_r is None:
            t0 = E
            if runways[0]:
                last = runways[0][-1]
                t0 = max(t0, times[last] + separation[last][sel])
            best_t = min(t0, L)
            best_r = 0
            best_c = C*(P-best_t) if best_t < P else C_*(best_t-P)

        times[sel] = best_t
        runways[best_r].append(sel)
        order.append(sel)
        available.remove(sel)

    if not test:
        print("Greedy stochastic → cost:", sum(
            C*(P-times[i]) if times[i]<P else C_*(times[i]-P)
            for i,(E,P,L,C,C_) in enumerate(airplanes)
        ))

    total_cost = sum(
        C*(P-times[i]) if times[i]<P else C_*(times[i]-P)
        for i,(E,P,L,C,C_) in enumerate(airplanes)
    )
    return order, total_cost