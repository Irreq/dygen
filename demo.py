def tr():
    import matplotlib.pyplot as plt

    import multibiasgen as mbg

    kg = mbg.KernelGenerator()

    kg.start()

    DISTRIBUTION = [0.5, 0.5, 0.5]

    bias = kg.fastgen(DISTRIBUTION)

    # A window will be added to bind the distribution between 0 and 0.5
    # bias = kg.setwindow(0, 0.5, bias)

    # Plot the data
    plt.subplot(211)
    plt.plot(bias)

    # Plot the bias as a histogram
    plt.subplot(212)
    plt.hist(bias)

    # Show the distribution
    plt.show()

# from multibiasgen import generate
#
# d = generate()
#
# print(d)

# tr()

from multibiasgen import BiasedDistribution
bd = BiasedDistribution()
bd.test()
bd.test2()
