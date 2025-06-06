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

### Para probar los casos:
Para probar el greedy ejecutar el siguiente comando:
```bash
python3 -m test.greedy
```

Se pedira ingresar el número de pistas (1 o 2) y el número de caso a probar (1-4). El código devolverá una comparación entre el greedy determinista y estocástico, mostrando el costo de cada uno y el tiempo de ejecución. Además, de graficos que muestran la evolución de los costos a lo largo de las iteraciones. 

Para probar el GRASP ejecutar el siguiente comando:
```bash
python3 -m test.grasp
```
Al igual que en el test anterior, se pedira ingresar el número de pistas (1 o 2) y el número de caso a probar (1-4). El código realizará una comparación entre GRASP con Greedy Determinista y GRASP con Greedy Estocástico (ambos con Hill Climbing, utilizando la técnica de mejor mejora). El código devolverá el costo y el tiempo de ejecución de cada uno de los métodos, además de generar gráficos que muestren la evolución de los costos a lo largo de las iteraciones.

Para probar el Tabu Search ejecutar el siguiente comando:
```bash
python3 -m test.tabu
```

Al igual que en los test anteriores, se pedira ingresar el número de pistas (1 o 2) y el número de caso a probar (1-4). El código realizará una comparación entre Tabu Search con Greedy Determinista y Tabu Search con Greedy Estocástico. El código devolverá el costo y el tiempo de ejecución de cada uno de los métodos utilizando 5 configuraciones diferentes (tamaño de la tabla tabú), además de generar gráficos que muestren la evolución de los costos vs el tamaño de la tabla.