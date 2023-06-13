# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt


datalist = os.listdir("IRdata/")



for file_name in datalist:
    data = np.loadtxt("IRdata/"+file_name).reshape(24,32)
    plt.title("Contour", fontsize=20)
    plt.contourf(data, cmap='plasma')
    plt.show()

