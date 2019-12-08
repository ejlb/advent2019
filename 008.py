import numpy as np

# part 1
array = np.array(list(open('008.txt').read().strip())).reshape(-1, 25*6).astype(np.uint8)
min_index = np.argmin(np.count_nonzero(array==0, axis=1))
print(np.count_nonzero(array[min_index, :]==1) * np.count_nonzero(array[min_index, :]==2))


# part 2 - lazy way
image = []
for pixel_n in range(array.shape[1]):
    for layer_n in range(array.shape[0]):
        if array[layer_n, pixel_n] != 2:
            image.append(array[layer_n, pixel_n])
            break

from PIL import Image
i = Image.fromarray(np.array(image).astype(np.uint8).reshape(6, 25)*255)
i.show()
