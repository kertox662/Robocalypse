mapA = []
mapA.append([2]*50)
mapA.append([2]*50)
mapA.append([2]*50)
for i in range(44):
    mapA.append([2]*3 + [1]*44 + [2]*3)
mapA.append([2]*50)
mapA.append([2]*50)
mapA.append([2]*50)

for i in mapA:
    print(i)