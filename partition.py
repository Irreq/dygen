import numpy as np

EULER = 2.718281828459045235360287471352662497757

def sigmoid(x):
    return 1.0 / (1.0 + EULER**-x)

def constrained_sum_sample_pos(total, n):

    """
    Integer partitioning of 'same' size.

    NOTE:                   Return a randomly chosen list of n positive
                            integers summing to total. Each such list is
                            equally likely to occur.
    ARGUMENTS:
        - n:                int() The total of groups of integer that
                            together sums up to 'n'. Eg, 3
        - total:            int() An integer which will be partitioned of
                            random size. Eg, 17
    RETURNS:
                            list() A partition of size 'n' that sums up
                            to 'total'. Eg, [6, 6, 5]

    TODO:                   None
    """

    dividers = sorted(np.random.choice(range(1, total), n - 1))

    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def constrained_sum_sample_nonneg(total, n):

    """
    Integer partitioning of random similar size.

    NOTE:                   Return a randomly chosen list of n nonnegative
                            integers summing to total. Each such list is
                            equally likely to occur.
    ARGUMENTS:
        - n:                int() The total of groups of integer that
                            together sums up to 'n'. Eg, 3
        - total:            int() An integer which will be partitioned of
                            random size. Eg, 17
    RETURNS:
                            list() A partition of size 'n' that sums up
                            to 'total'. Eg, [7, 4, 6]

    TODO:                   None
    """

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]

def partion_n_times(total, n):

    """
    Integer partitioning of same size.

    NOTE:                   If mod(total, n) != 0, then some partions will
                            be of larger size, but together sum up to total.
                            Zeros will be appended since you are trying to
                            partition an integer more times than it consists of.
    ARGUMENTS:
        - total:            int() An integer which will be partitioned of
                            random size. Eg, 17
        - n:                int() The total of groups of integer that
                            together sums up to 'n'. Eg, 3

    RETURNS:
                            list() A partition of size 'n' that sums up
                            to 'total'. Eg, [6, 5, 6]

    TODO:                   Fix float partition. At the moment, the total
                            will be lower as the function tries to convert
                            the value to integer.
    """

    chunk = total // n

    return [chunk + 1 if i < total%n else chunk for i in range(n)]


def prime_factors(n):

    """
    Prime factorization

    NOTE:                   None

    ARGUMENTS:
        - n                 int() An integer to factorize into prime
                            numbers. Eg, 48

    Returns:
        - factor            list() An array of prime numbers.
                            Eg, [2, 3]
    """

    n = int(n) # make sure the number is an integer

    factor = []

    for i in range(2, n + 1):
        if n % i == 0:
            prime = True
            for j in range(2, (i // 2 + 1)):
                if i % j == 0:
                    prime = False
                    break

            if prime:
                factor.append(i)
    return factor

def consecutive_constrained_sum(total, n):
    return total

if __name__ == '__main__':

    def main():
        print ("This program illustrates a chaotic function")
        x = float(input("Enter a number between 0 and 1: "))

        if not 0<x<1:
            x = sigmoid(abs(x / (x/0.9*x)))

        for i in range(10):
            x = 3.9 * x * (1-x)
        print(x)


    main()
    total = 56
    n = 6

    # value = consecutive_constrained_sum(total, n)
    value = prime_factors(48)

    print(value)
