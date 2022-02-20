from fractions import Fraction
import math

def get_all_real_roots(coefficients):
    roots = []
    if not (type(coefficients[0]) == int or coefficients[0].is_integer()) or not (type(coefficients[-1]) == int or coefficients[-1].is_integer()):
        denominator_first_member  = Fraction(coefficients[0]).denominator
        denominator_last_member = Fraction(coefficients[-1]).denominator
        lcm = denominator_first_member * denominator_last_member / math.gcd(denominator_first_member, denominator_last_member)
        print("LCM: ", lcm)
        for i in range(len(coefficients)):
            coefficients[i] = coefficients[i] * lcm
        print(coefficients)
        

    r, c = get_root(coefficients)
    while r != "end":
        roots.append(r)
        r, c = get_root(c)
    return roots, c


def get_root(coefficients):
    if coefficients[-1] == 0:
        coefficients.pop()
        return 0, coefficients
    
    possible_roots = generate_possible_roots(coefficients)

    for r in possible_roots:
        coef_r = calculate_scheme(r, coefficients)
        if(coef_r[-1] == 0):
            coef_r.pop()
            print(r, coef_r)
            return r, coef_r
    
    return "end", coefficients

def generate_possible_roots(coefficients):
    possible_roots = []

    for a in get_divisors(coefficients[-1]):
        for b in get_divisors(coefficients[0]):
            if not (a/b) in possible_roots:
                possible_roots.append(a/b)
                possible_roots.append(-a/b)

    return possible_roots

def get_divisors(number):
    divisors = [number, -number]
    for i in range((int)((number**2)**(1/4))):
        if(number % (i+1) == 0):
            divisors.append(i+1)
    return divisors

def calculate_scheme(root, coefficients):
    result = []
    result.append(coefficients[0])
    for i in range(len(coefficients) - 1):
        result.append(root * result[i] + coefficients[i+1])
    
    return result

def try_root(root, coefficients):
    if(calculate_scheme(root, coefficients)[-1] == 0):
        return True
    
    return False

if __name__ == '__main__':
    c =  [4, -12, 5, 8, -3, -2]
    print(get_all_real_roots(c))

    c = [1.0, -3, 1.25, 2, -0.75, -0.5]
    print(get_all_real_roots(c))