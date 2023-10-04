p = 3
q = 11

n = p * q

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def phi():
    return (p-1)*(q-1)

