import numpy as np

noise = np.random.normal(0,1,100)

class Noise(object):

    def __init__(self, data):

        self.data = data

    def addnoise(self, *snr):

        """ snr being signal to noise ratio, if nothing has been added, the ratio will be 20%/80% """

        if len(snr) > 0:
            snr = snr[0]

        else:
            snr = 0.2

        noise = np.random.normal(0,1,len(data)) * snr

        added_noise = np.concatenate((self.data, noise))

        return added_noise

    def getnoise(self):
        return self.data

    def delnoise(self):
        return self.data
