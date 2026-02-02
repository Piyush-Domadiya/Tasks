# Fibonacci series using memoization
memo = {}

def fib(n):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]

n = int(input("Enter number of terms: "))
series = [fib(i) for i in range(n)]
print(series)
