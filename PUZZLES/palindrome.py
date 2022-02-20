from numpy.lib.twodim_base import mask_indices


def is_palindrome(word):
    for i in range(int(len(word)/2)):
        if(word[i] != word[-(i+1)]):
            return False

    return True

def dif1():
    words = []
    with open("1-3.txt") as f:
        for line in f:
            words += line.lower().strip().split()

    count = 0
    for w in words:
        if(is_palindrome(w)):
            count += 1

    print(count)

def dif2():
    largest = 0
    for i in range(0, 1000000, 51):
        w = str(i)
        if(is_palindrome(w)):
            largest = i

    print(largest)

def dif3():
    largest = 0
    for i in range(100, 1000):
        for j in range(100, 1000):
            w = str(i*j)
            if(is_palindrome(w)):
                if(i*j > largest):
                    largest = i*j

    print(largest)

if __name__ == "__main__":
    dif1()
    dif2()
    dif3()

