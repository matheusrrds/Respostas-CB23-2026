import random
import time
import sys
from AulasPraticas.AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort

sys.setrecursionlimit(max(10000, 6000))

def randomlist(size) :

    return [random.randint(1, 100) for _ in range(size)]

def worst_case_quick_sort(size) :

    return [x for x in range(1, size+1)]

def benchmark(algorithm, n, test, k = 1) :

    # caso medio
    accumulator = 0

    if test == "medium" :

        for _ in range(k) :

            array = randomlist(n)

            begin = time.perf_counter()
            algorithm(array)

            end = time.perf_counter()
            accumulator += (end - begin)

        timeav = (accumulator / k)
        return timeav

    elif test == "worst" :

        # piores casos

        if algorithm == quick_sort :

            for _ in range(k) :

                array = worst_case_quick_sort(n)
                
                begin = time.perf_counter()
                algorithm(array)
    
                end = time.perf_counter()
                accumulator += (end - begin)
            
            timeav = (accumulator / k)
            return timeav

        else :

            for _ in range(k) :

                array = randomlist(n)
            
                begin = time.perf_counter()
                algorithm(array)
    
                end = time.perf_counter()
                accumulator += (end - begin)
    
            timeav = (accumulator / k)
            return timeav

print(f"{'Algoritmo':<25} {'Caso':<10} {'N':<8} {'Tempo médio (s)':>18}")
print("-" * 65)

for algorithm, name in [
    (selection_sort, "Selection Sort"),
    (divide_and_conquer_sort, "Merge Sort"),
    (quick_sort, "Quick Sort")
]:
    
    for test in ["medium", "worst"]:
        
        for n in [100, 500, 1000, 5000]:
            
            time_average = benchmark(algorithm, n, test, 50)
            
            print(f"{name:<25} {test:<10} {n:<8} {time_average:>18.8f}")


