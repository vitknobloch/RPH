
def value_count(data,value):
    count = 0
    for row in data:
        for i in row:
            if i == value:
                count +=1

    return count


def value_positions(data,value):
    val_coords = []
    for x, row in enumerate(data):
        for y, item in enumerate(row):
            if item == value:
                val_coords.append((x, y))
    
    return val_coords

if __name__ == '__main__':
    value = 0
    data =  [[ 0 ,-1 , 1],
            [-1 , 0 ,-1],
            [ 1 , 0 ,-1]]
    count = value_count(data, value)
    positions = value_positions(data, value)
    print(count)
    print(positions)
