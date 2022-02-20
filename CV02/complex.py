class ComplexNumber:
    def __init__(self, re, im):
        self.re = re
        self.im = im


    def __str__(self):
        if (self.im == 0):
            return str(self.re)
        elif(self.im < 0):
            return f"{self.re} - {-self.im}i"
        else:
            return f"{self.re} + {self.im}i"
    
    def __abs__(self):
        return (self.re**2 + self.im**2)**(1/2)

    def __add__(self, other):
        return ComplexNumber(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return ComplexNumber(self.re - other.re, self.im - other.im)
    
    def __mul__(self, other):
        re = self.re * other.re - self.im * other.im
        im = self.im * other.re + self.re * other.im
        return ComplexNumber(re, im)

    def complexConjugate(self): #komplexně sdružené číslo
        return ComplexNumber(self.re, -self.im)

    def __truediv__(self, other):
        nominator = self * other.complexConjugate()
        denominator = other.re**2 - other.im**2
        if denominator == 0:
            raise Exception("Error: Zero division (complex truediv function)")

        return ComplexNumber(nominator.re / denominator, nominator.im)


if __name__ == "__main__":
    c1 = ComplexNumber(3,3)
    c2 = ComplexNumber(7, -3)
    print(c1)
    print(c2)
    print(c2 - c1)
    print(c1 * c2)
    print(c1 / c2)