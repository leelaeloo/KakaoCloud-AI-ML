
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

image = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
])

plt.figure(figsize=(8, 4))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray', vmin=0, vmax=1)
plt.title('origin')

brightened = image + 0.5
plt.subplot(1, 3, 2)
plt.imshow(brightened, cmap='gray', vmin=0, vmax=1)
plt.title('brightened')

inverted = 1 - image
plt.subplot(1, 3, 1)
plt.imshow(inverted, cmap='gray', vmin=0, vmax=1)
plt.title('inverted')

plt.tight_layout()
plt.savefig('image_example.png')
plt.show()

