#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: multibias.py
# Author : Irreq

"""
DOCUMENTATION:          Generate a synthetic distribution.
"""

from importlib.metadata import distribution
from more_itertools import distribute
import numpy as np

def add_noise(data, snr):
    """Add noise to data"""
    noise = np.random.normal(0, 1, len(data)) * snr
    added_noise = np.concatenate((data, noise))
    return added_noise

def closest(lst, n):
    """Return `n` if `lst` is empty"""
    aux = []
    if not any(lst):
        return n
    for valor in lst:
        aux.append(abs(n-valor))
    return lst[aux.index(min(aux))]

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(np.random.choice(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def constrained_sum_sample_nonneg(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]


class DistributionGenerator(object):
    """Main class for distribution generation."""

    bias = {
        "normal_distribution": [[0.5, 0.2], ],  # median, standard deviation
    }

    def __init__(self, size=1000, window=[0.0, 1.0], kernel="gaussian"):
        self.size = size
        self.window = window
        self.kernel = kernel

    def setwindow(self, window: list()):
        """Apply window."""
        self.window = window

    def setsize(self, size: int()):
        """Apply size."""
        self.size = size

    def setkernel(self, kernel: str()):
        """Apply kernel."""
        self.kernel = kernel


    def kernel_normal_dist(self, mean, std, size=None, window=[0, 1]):
        """ Returns normal distribution """

        if size == None:
            size = self.size

        s = np.random.normal(mean, std, size)
        min_val, max_val = window[0], window[1]

        return [i for i in s if min_val <= i <= max_val]

    def addbias(self, id, kernel):
        """Adds distribution from a dictionary."""
        if id in self.bias.keys():  # Already here
            return
        
        self.bias[id] = kernel

    def kernel_density(self):

        pre_data = self.data

        start = np.array(pre_data)

        start_len = len(start)

        resolution = np.linspace(0, 1, num=10).tolist()

        pre_data = np.histogram(pre_data, bins=resolution)[0]

        pre_data = pre_data / max(pre_data)

        pre_data = np.array([int(i*100) for i in pre_data.tolist()])

        # 2 is an arbitary good number to use
        initial_length = int(len(pre_data) * 2)

        a = pre_data.reshape(-1, 1)

        kde = KernelDensity(kernel='gaussian', bandwidth=2).fit(a)
        s = np.linspace(0, initial_length)
        e = kde.score_samples(s.reshape(-1, 1))

        lower_boundaries = argrelextrema(e, np.less)[0]

        minima = s[lower_boundaries]

        demodulated_index = [int((i/initial_length)*start_len) for i in minima]

        return start[np.array(demodulated_index)]

    def kernel_generator(self, localkernel):

        normal_distributions = [self.kernel_normal_dist(
            localkernel[k][0], localkernel[k][1], self.size) for k in range(len(localkernel))]

        normal_distributions.sort()

        self.data = normal_distributions[::int(
            round(len(normal_distributions)/self.size))]

        if len(self.data) > self.size:

            for i in range(len(self.data)-self.size):

                del self.data[np.random.randint(len(self.data))]

        elif len(self.data) < self.size:

            local_average = np.mean(np.array(self.data))

            values = self.kernel_density()[0]

            values = self.kernel_normal_dist(
                values, 0.1, size=self.size-len(self.data))

            values = [(i+local_average)/2 for i in values]

            self.data.extend(values)

            self.data.sort()

        return self.data

    def generate(self, id, distribution):

        resolution = self.size

        window = len(distribution) ** -1

    def generate_bias(self, bias: dict()):
        """Load and generate bias.
        >>> generate_bias([1, 43, 22])
        """

        return self.kernel_generator(bias)


class DoctorDataset:
    """Generic patient structure."""

    patient_structure = {
        # Social

        # 1 is equivalent of 113 years CIA World Factbook (2018 est.)
        "age": [0.1754, 0.1106, 0.3937, 0.1167],

        # location

        # 1 is equivalent to > 30 minutes based on data from https://www.regionfakta.com/Skane-lan/Samhallets-service/Avstand-till-vardcentral/ -- 2014
        "travel_difficulty": [0.66, 0.206, 0.128, 0.005],

        # General population (SCB, 2017)
        "socio_economic_vulnerability": [0.041, 0.169, 0.327, 0.235, 0.228],

        # medical treatment

        "medical_conditions": [0.9, 0.09, 0.01],  # fictional

        "severity": [0.9, 0.09, 0.01],

        "treatment_time": [0.9, 0.09, 0.01],

        "treatment_frequency": [0.9, 0.09, 0.01],

        # how bad the patient is with the doctor fictional
        "burden_quality": [0.9, 0.09, 0.01],
    }

    patients = []

    _invoked = False

    def __init__(self, id=None):
        if self.id is None:
            self.id = 0
        else:
            self.id = id

    def invoke(self):
        if self.invoked:
            return
        else:
            kg = KernelGenerator()

            kg.start()

            for i in self.patient_structure.keys():
                self.patient_structure[i] = kg.fastgen(self.patient_structure[i])

            self.invoked = True


def test():
    doctors = 16
    patients = 23000


    # doctors = doctorgeneration(doctors, patients).tolist()


    res = constrained_sum_sample_nonneg(doctors, patients)

    print(res)

# test()

bias = {
    "travel_difficulty": [0.66, 0.206, 0.128, 0.005]
}


bs = bias["travel_difficulty"]

bs = [0.1, 2, 3, 0.2]

normal_dist = np.random.normal(0.5, 0.2, 1000)

distribution = bs
upper = len(distribution) ** -1
lower = 0

resolution = 100

c_n_dist = [i*(upper-lower)+lower for i in normal_dist]

final_distribution = []

for i, value in enumerate(distribution):
    data = [i*upper+np.random.choice(c_n_dist)
            for _ in range(int(value*resolution))]

    final_distribution.extend(data)




# dg = DistributionGenerator()

# compiled_bias = dg.generate_bias(bias["travel_difficulty"])


# print(final_distribution)

import matplotlib.pyplot as plt

plt.plot(final_distribution)
plt.show()

# dg.generate(bias, size, window)