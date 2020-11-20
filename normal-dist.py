#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
    Documentation

    A class for generating multi biased
    distributions using Kernel Density Estimation (KDE)

"""

"""

    TODO

"""

__author__ = "Isac Bruce"
__copyright__ = "Copyright 2020, Irreq"
__credits__ = ["Isac Bruce"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Isac Bruce"
__email__ = "irreq@protonmail.com"
__status__ = "Production"


import numpy as np

from sklearn.neighbors.kde import KernelDensity

from scipy.signal import argrelextrema


class KernelGenerator(object):

    def __init__(self, size=200, debug=False):

        self.size = size

        self.debug = debug

        self.bias = {

            "normal_distribution" : [[0.5, 0.2],], # median, standard deviation

        }

    def kernel_normal_dist(self, mean, std, size=None, window=[0, 1]):

        """ Returns normal distribution """

        if size == None:
            size = self.size

        s = np.random.normal(mean, std, size)

        min_val, max_val = window[0], window[1]

        return [i for i in s if min_val <= i <= max_val]

    def kernel_density(self, x):

        x = np.array(x)

        start = x

        gg = np.linspace(0,1, num=10).tolist()

        x, _ = np.histogram(x, bins=gg)

        x = x / max(x)

        pp = x

        x = np.array([int(x*100) for x in x.tolist()])

        ll = int(len(x)*2)

        a = x.reshape(-1, 1)

        kde = KernelDensity(kernel='gaussian', bandwidth=2).fit(a)
        s = np.linspace(0,ll)
        e = kde.score_samples(s.reshape(-1,1))


        mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]

        minima = s[mi]

        minima.tolist()

        start = np.array(start)

        gt = np.array([int((i/ll)*len(start)) for i in minima])

        # print(gt)

        result = start[gt]

        if self.debug:

            import matplotlib.pyplot as plt

            print(result)

            plt.subplot(221)
            plt.plot(pp)


            plt.subplot(222)
            plt.plot(s, e)
            plt.plot(s[mi], e[mi], 'ro')

            plt.subplot(223)
            plt.hist(start)

            plt.subplot(224)
            plt.plot(start)



            plt.show()

        return result

    def kernel_generator(self, localkernel):

        # print(localkernel)

        normal_distributions = []

        for k in range(len(localkernel)):

            distribution = self.kernel_normal_dist(localkernel[k][0], localkernel[k][1], self.size)

            normal_distributions.extend(distribution)


        normal_distributions.sort()

        final_distribution = normal_distributions[::int(round(len(normal_distributions)/self.size))]

        if len(final_distribution) > self.size:

            for i in range(len(final_distribution)-self.size):

                del final_distribution[np.random.randint(len(final_distribution))]


        elif len(final_distribution) < self.size:

            norm = np.mean(np.array(final_distribution))

            values = self.kernel_density(final_distribution)

            values = self.kernel_normal_dist(values[0], 0.1, size=self.size-len(final_distribution))

            values = [(i+norm)/2 for i in values]

            final_distribution.extend(values)

            final_distribution.sort()



        if self.debug:

            import matplotlib.pyplot as plt

            print('elements : {}\nmean : {}\nmax : {}\nmin : {}'.format(len(final_distribution),np.mean(np.array(final_distribution)), max(final_distribution), min(final_distribution)))

            plt.hist(np.array(final_distribution), bins=np.linspace(0,1, num=100).tolist())
            plt.show()

        return final_distribution

    def kernel_error_catcher(self, kernel_seed):

        ErrorCount = 0

        while True:



            try:

                distribution = self.kernel_generator(kernel_seed)
                return distribution

                break

            except Exception as e:
                ErrorCount += 1

                if ErrorCount > 100:
                    print('Error overflow')
                    print(e)
                    print("error found in kernel density estimation last row")

                    break




    def random_kernels(self, n_kernels):

        # if self.bias[id][0] == list():

        self.bias['normal_distribution'] = self.kernel_error_catcher(self.bias['normal_distribution'])

        def dub(n):

            return [0.2, 0.3], [0.8, 0.7]

        for i in range(n_kernels):

            x = np.random.choice(self.bias['normal_distribution'])

            print("normal_distribution")

            print(x)

            self.bias[i] = [dub(x)]

    def start(self):

        for id in self.bias:

            # print(type(self.bias[id][0]).__name__)

            if type(self.bias[id][0]).__name__ == list:
                continue

            self.bias[id] = self.kernel_error_catcher(self.bias[id])

    def addbias(self, *kernel):

        """
        Adds distributions from a dictionary


        kernel = eg, {'tag':[[0.4]]}

        returns = dict() # distribution

        """

        if len(kernel) == 0:
            return

        else:
            kernel = kernel[0]

        for id in kernel.keys():
            self.bias[id] = self.kernel_error_catcher(kernel[id])

        return {id:self.bias[id] for id in kernel.keys()}

    def getbias(self):

        return self.bias

    def setwindow(self, lower, upper, kernel_id):

        data = self.bias[kernel_id]

        data = [i*(upper-lower)+lower for i in data]

        self.bias[kernel_id] = data

        return data

def test():

    """ Example showing a biased distribution """

    import matplotlib.pyplot as plt

    # I have chosen two distributions
    # her, but you could use whatever
    # you wan't

    generic_bias_instructions = {

        "medical_conditions" : [[0.0, 0.1],
                                [0.72, 0.06],
                                [1.0, 0.4],
                                [0.35, 0.1],],

        "random_distribution" : [[0.0, 0.1],
                                 [0.72, 0.1],
                                 [1.0, 0.4],
                                 [0.35, 0.1],]
    }

    resolution = 5000

    kg = KernelGenerator(size=resolution)

    kg.start()

    bias = kg.addbias(generic_bias_instructions)

    nomdist = kg.setwindow(0,4,"normal_distribution")

    nomdist = np.array(nomdist)

    print('elements : {}\nmean : {}\nmax : {}\nmin : {}'.format(len(nomdist),np.mean(np.array(nomdist)), max(nomdist), min(nomdist)))



    # To get all stored biases :

    # bias = kg.getbias()

    # plt.hist(np.array(bias["normal_distribution"]), bins=np.linspace(0,resolution)/resolution)
    plt.hist(nomdist, bins=np.linspace(0,resolution)/resolution)

    plt.show()

if __name__ == '__main__':

    test()
