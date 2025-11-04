import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

plt.subplot(1, 3, 1)
plt.plot(x, sigmoid_y, 'b--')
