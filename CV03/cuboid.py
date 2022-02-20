class Cuboid:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def compute_surface(self):
        return 2 * (self.a * self.b + self.b * self.c + self.a * self.c)

    def make_enlarged_copy(self, a1, b1, c1):
        return Cuboid(self.a + a1, self.b + b1, self.c + c1)

if __name__ == '__main__':
    c = Cuboid(1, 2, 3)
    print(c.compute_surface())
    c2 = c.make_enlarged_copy(1,2,1)
    print(c2.compute_surface())