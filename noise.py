import numpy as np

noise = np.random.normal(0,1,100)

class Noise(object):

    def __init__(self, *data):

        self.data = data

    def addnoise(self, *snr):

        """ snr being signal to noise ratio, if nothing has been added, the ratio will be 20%/80% """

        if len(snr) > 0:
            snr = snr[0]

        else:
            # snr = 0.1
            snr = 10

        noise = np.random.normal(-1,1,len(self.data)) * snr

        # noise = np.array([1-i for i in noise])

        # added_noise = np.concatenate((self.data, noise))

        # added_noise = np.addition(self.data, noise)
        added_noise = self.data + noise

        self.data = added_noise

        return added_noise

    def getnoise(self):
        return self.data

    def delnoise(self):
        return self.data

    def loaddata(self, sig):
        self.data = sig


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    binary = np.linspace(0, 50)
    print(binary)

    N = Noise()

    N.loaddata(binary)

    N.addnoise(1)

    binary2 = N.getnoise()

    print(binary2)

    plt.subplot(211)
    plt.plot(binary)

    plt.subplot(212)
    plt.plot(binary2)

    plt.show()
