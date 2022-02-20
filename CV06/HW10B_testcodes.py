import random
from math import log, log2

def prinf_regions(min, max, count):
    range_size = ( log2(max - min) ) / (count - 1)

    print(min)
    for i in range(count - 1):
        print(min + round(pow(2, i * range_size)))
    



if __name__ == "__main__":
    max = random.randint(1, 100000)

    min = random.randint(0, max)

    count = random.randint(2, 10)
    print("max:  ", max)
    print("min:  ", min)
    print("count:", count)
    prinf_regions(min, max, count)
