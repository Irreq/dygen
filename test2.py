#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: multibias.py
# Author : Irreq

from fileinput import filename
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KernelDensity
from scipy.signal import argrelextrema

class MultiBiasGen:
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

    def addbias(self, name, distribution):
        pass

    def removebias(self, name):
        pass

    def compilebias(self):
        pass

    def loadbias(self, name):
        if name not in self.bias.keys():
            return


def compilebias(distribution, size=1000, window=[0.0, 1.0], kernel="gaussian"):
    n_diff = len(distribution) ** -1

    lower, upper = window
    upper = n_diff
    ref_bias = [i*(upper-lower) +
                lower for i in np.random.normal(0.5, 0.2, size)]

    compiled_bias = []

    for i, value in enumerate(distribution):

        data = [i*n_diff+np.random.choice(ref_bias)
                for _ in range(int(value*size))]
            
        compiled_bias.extend(data)

    return np.array(compiled_bias)


def get_args() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draw", action="store_true")
    parser.add_argument("--load", help="Path to bias file")

    return parser.parse_args()

if __name__ == "__main__":
    import argparse
    args = get_args()

    if args.draw:
        from mpl_point_clicker import clicker
        lower, upper = 0, 1

        fig, ax = plt.subplots(constrained_layout=True)
        ax.set_xlim([0, 1])
        ax.set_ylim([lower, upper])
        plt.title("Draw a representation of the distribution:")
        plt.axis('off')
        klicker = clicker(ax, ["PoI"], markers=["x"], linestyle="--") # **{"linestyle": "--"})

        plt.show()

        bias = [i for _, i in klicker.get_positions()["PoI"]]

        compiled_bias = compilebias(bias)

        plt.hist(compiled_bias, bins=np.linspace(0, 1, 10))
        plt.title("Result Histogram")
        plt.show()

        import csv

        filename = input("Save your file as: ")

        with open("compiled/"+filename, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(compiled_bias)
    else:
        print("Usage: --draw")

