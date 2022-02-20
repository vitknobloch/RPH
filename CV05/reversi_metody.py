

def line_size(r, c, data, val):
    counter = 0

    x = c-1
    while (x >= 0 and data[r][x] == val):
        x -=1
        counter += 1
    
    x= c+1
    while (x < len(data[r]) and data[r][x] == val):
        x +=1
        counter += 1

    return counter

def column_size(r, c, data, val):
    counter = 0

    y = r-1
    while (y >= 0 and data[y][c] == val):
        y -=1
        counter += 1
    
    y= r+1
    while (y < len(data) and data[y][c] == val):
        y +=1
        counter += 1

    return counter

def diagonal_size_TL(r, c, data, val):
    counter = 0

    y = r - 1
    x = c - 1  
    while (y >= 0 and x >= 0 and data[y][x] == val):
        y -=1
        x -=1
        counter += 1
    
    y = r+1
    x = c+1
    while (y < len(data) and x < len(data[r]) and data[y][x] == val):
        y +=1
        x +=1
        counter += 1

    return counter

def diagonal_size_TR(r, c, data, val):
    val = data[r][c]
    counter = 0

    y = r-1
    x = c+1
    while (y >= 0 and x < len(data[r]) and data[y][x] == val):
        y -=1
        x +=1
        counter += 1

    y = r+1
    x = c-1
    while (y < len(data) and x >= 0 and data[y][x] == val):
        y +=1
        x -=1
        counter += 1

    return counter

def region_size(r, c, data, val):
    return line_size(r, c, data, val) + column_size(r, c, data, val) + diagonal_size_TL(r, c, data, val) + diagonal_size_TR(r, c, data, val)

if __name__ == '__main__':
    r=2
    c=6
    data = [
    [1, 0, 0, 0, 1, 1, 0, 0 ] ,
    [1, 1, 1, 0, 0, 1, 1, 1 ] ,
    [0, 1, 0, 0, 1, 1, 1, 1 ] ,
    [0, 1, 0, 1, 0, 1, 1, 1 ] ,
    [0, 1, 1, 0, 0, 0, 1, 1 ] ,
    [1, 0, 0, 0, 1, 1, 0, 0 ] ,
    [0, 0, 1, 0, 1, 1, 1, 0 ] ,
    [0, 0, 1, 0, 1, 0, 1, 0 ]]

    reg_size = region_size(r, c, data, data[r][c])
    print("Region size:", reg_size +1)
    


