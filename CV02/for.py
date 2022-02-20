def find_max(in_list):

    out = in_list[0]
    for i in in_list:
        if (i > out):
            out = i

    return out

if __name__ == "__main__":
    a = find_max([15, -12, 3, 28, 9])
    print(a)