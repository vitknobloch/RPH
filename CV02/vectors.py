
class MyVector:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def get_vector(self):
        return self.coordinates
    
    def __mul__(self, other):
        result = 0
        #cycle through every coordinate of the vectors
        for i in range(min([len(self.coordinates), len(other.coordinates)])):
            #add result of mulitplication between coordinates to the result
            result += (self.coordinates[i] * other.coordinates[i])
        return result

    def __add__(self, other):
        resultField = []
        #cycle through every coordinate of the vectors
        for i in range(max([len(self.coordinates), len(other.coordinates)])):
            coordinate_result = 0
            if i < len(self.coordinates):
                coordinate_result += self.coordinates[i]

            if i < len(other.coordinates):
                coordinate_result += other.coordinates[i]

            resultField.append(coordinate_result)

        return MyVector(resultField)

    def norm(self):
        norm = 0
        for i in self.coordinates:
            norm += i**2
        
        norm = (norm ** 0.5)
        return norm

if __name__ == '__main__':
    vec1 = MyVector([1,2,3,0,-2])
    vec2 = MyVector([4,5,6,8,10])
    
    print("input:")
    print(vec1.get_vector())
    print(vec2.get_vector())

    print("result:")
    print(vec1*vec2)

    print((vec1 + vec2).get_vector())
    print(MyVector([1]).norm())
    print(MyVector([3,4]).norm())
    print(MyVector([1,1,2**0.5]).norm())
