from readFile import readFile


cases = readFile("cases/case1.txt")


for i in range(len(cases)):
        print("\nCaso ", i+1)
        print("Para cada Avión: ", cases[i][0])
        print("Tiempo de Separación: ", cases[i][1])        