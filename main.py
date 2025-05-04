from readFile import readFile
from greedy.deterministic import greedy_deterministic

cases = readFile("cases/case1.txt")

for i, case in enumerate(cases):
    orden, costo = greedy_deterministic(case, num_runways=2)
    print("\nOrden de aterrizaje:", orden)
    print("Costo total:", costo)