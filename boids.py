import numpy as np

EULER = 2.718281828459045235360287471352662497757

M = 0.01 # mass in kg



def sigmoid(x):
    return 1.0 / (1.0 + EULER**-x)


def sqrt_einsum_T(data):
    a, b = data[1]
    a_min_b = a - b
    return numpy.sqrt(numpy.einsum("ij,ij->j", a_min_b, a_min_b))

def newton_gravity(m1, m2, r):
    return G * (m1*m2) / r**2

def chaos(x):
    return 3.9 * x * (1-x)

def euclidian_distance_2d(a1, a2):
    return ((abs(a1[0]) + abs(a2[0]))**2+(abs(a1[1]) + abs(a2[1]))**2)**0.5

z = euclidian_distance_2d((2.0,1.4),(34,-4.5))
print(z)
print(sigmoid(-2))

if __name__ == '__main__':
    a1, a2 = setup(3)
    print(a1, a2)
