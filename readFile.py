def readFile(filePath):
    allCases = []

    with open(filePath, "r", encoding="utf-8") as file:
        content = file.read()

    lines = content.splitlines()

    cases = int(lines[0].split()[0])

    i = 1
    cont = False
    while i < len(lines):
        if cont == False:    
            forEachPlane = list(map(float, lines[i].split()))
            i+= 1
            if i >= len(lines):
                break
            timeApart = list(map(int,lines[i].split()))
            i+= 1
        
        if len(timeApart) < cases: 
            tmp = list(map(int, lines[i].split()))
            
            for j in range(len(tmp)):
                timeApart.append(tmp[j])    
            i+= 1
            
            if len(timeApart) == cases:
                cont = False 
            else:
                cont = True    

        if cont == False:
            allCases.append([forEachPlane, timeApart])


    aviones = [c[0] for c in allCases]
    separacion = [c[1] for c in allCases]
    cases = [[aviones, separacion]]  
    
    return cases