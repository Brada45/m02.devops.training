def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Denominator cannot be zero")
    return a / b


def power(base, exponent):
    return base ** exponent


def square_root(n):
    if n < 0:
        raise ValueError("Input must be a non-negative number")
    return n ** 0.5


def modulo(a, b):
    if b == 0:
        raise ValueError("Denominator cannot be zero")
    return a % b


def is_even(n):
    return n % 2 == 0


def is_positive(n):
    return n > 0


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
