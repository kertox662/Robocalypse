class Tester:
    def __init__(self, value):
        self.val = value


l1 = []
for i in range(10):
    l1.append(Tester(i))

l2 = l1.copy()

for i in range(10):
    l1[i].val *= 3

print(l1, l2)
print()
for i in range(10):
    print(l1[i].val, l2[i].val)