from math import ceil, sqrt


def dif1():
    sum = 0
    for i in range(-100, 3000, 1): 
        sum += i
    print("SUMA 1:", sum)

def dif2():
    sum = 0
    for i in range(0, 3000, 3):
        sum += i
    for i in range(0, 3000, 7):
        if i % 3 != 0:
            sum += i
    print("SUMA 2:", sum)

def dif3():
    primes = []
    for i in range(2, 3000):
        is_prime = True
        for p in primes[0:int(ceil(sqrt(i)))]:
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)

    sum = 0
    for i in range(1, 3000):
        num = i
        num_factors = 0
        for p in primes:
            while(num % p == 0):
                num = num // p
                num_factors += 1
            if num == 1:
                break
            if(num_factors > 3):
                break

        if num_factors == 3:
            sum += i           

    print("SUMA 3:", sum)

if __name__ == "__main__":
    dif1()
    dif2()
    dif3()
