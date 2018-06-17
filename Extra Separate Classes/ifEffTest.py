from time import time

def func():
    return True

for i in range(10):
    print("==========")
    x = time()
    for j in range(1):
        if func():
            pass

    print(time() - x)

    y = time()
    for j in range(1):
        if func() == True:
            pass

    print(time() - y)
