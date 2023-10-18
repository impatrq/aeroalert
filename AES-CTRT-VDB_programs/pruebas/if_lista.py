vuelos = {}


if 123 in vuelos:
    print("ya estaba")
else:
    print("no estaba")
    vuelos[str(123)] = []
    vuelos[str(123)][0].append([123,1234,54])
    vuelos[str(123)][0].append([56,1243546,32])


print(vuelos)