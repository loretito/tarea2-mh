# Tarea 2 de Algoritmos Exactos y Metaheurísticas
Autoras: Sofía Belmar y Loreto Ñancucheo

## Problema: "Control Aéreo"
Para la gestión de tráfico aéreo en un aeropuerto, se requiere coordinar los aterrizajes de manera segura y eficiente. Se tiene como objetivo planificar la secuencia de un conjunto de aviones, asignándolos a una o dos pistas de aterrizaje, de modo que se minimizar los costos operativos asociados a desviaciones del tiempo de aterrizaje preferente de cada avión.

Cada avión tiene definido un intervalo de tiempo para aterrizar (tiempo más temprano, tiempo preferente y tiempo más tardío). Si un avión aterriza antes o después de su tiempo preferente, se incurre en un costo proporcional a la desvación. Además, deben cumplirse restricciones de seguridad: entre cada par de aviones existe un tiempo mínimo de separación entre aterrizajes.

## Soluciones Implementadas

1. Greedy determinista y estocástico (10 iteraciones)
2. GRASP con HC mejor-mejora
3. Tabu Search

## Funcionamiento del código

