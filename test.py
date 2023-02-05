import time
import sys

sys.setrecursionlimit(200000)

def factorial(n):
    if n ==1:
        return 1
    else:
        fact = n * factorial(n-1)
        return fact

start_time = time.time()
factorial(150000)
end_time = time.time()

print("Processing time:", end_time - start_time, "seconds")