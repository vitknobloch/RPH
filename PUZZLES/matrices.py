import numpy as np

def dif1():
    matrix = []
    with open('1-2.csv') as f:
        for line in f:
            matrix.append(line.split(','))

    index = 0
    final_str = ""
    while(index < len(matrix) and index < len(matrix[index])):
        final_str += matrix[index][index]
        index += 1

    print(final_str)

def dif2():
    matrix = []
    with open('2-2.csv') as f:
        for line in f:
            line_split = line.split(',')
            nums = []
            for l in line_split:
                nums.append(int(l))
            matrix.append(nums)


    result = 1

    for i in range(len(matrix)):
        row = i
        column = 0
        diag_sum = 0
        while(row < len(matrix) and column < len(matrix[row])):
            diag_sum += matrix[row][column]
            row += 1
            column += 1
        result *= diag_sum

    for i in range(1, len(matrix)):
        row = 0
        column = i
        diag_sum = 0
        while(row < len(matrix) and column < len(matrix[row])):
            diag_sum += matrix[row][column]
            row += 1
            column += 1
        result *= diag_sum

    print(result)

def dif3():
    matrix = []
    with open('3-2.csv') as f:
        for line in f:
            line_split = line.split(',')
            nums = []
            for l in line_split:
                nums.append(int(l))
            matrix.append(nums)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (i + j) % 2 == 0:
                matrix[i][j] *= 2

    arr = np.array(matrix)

    det = np.linalg.det(arr)
    print(int(round(det)))

if __name__ == "__main__":
    dif1()
    dif2()
    dif3()