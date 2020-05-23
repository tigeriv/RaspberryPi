import numpy as np

cat_to_color = {0: (0, 0, 0), 1: (0, 0, 255)}

def cat_to_im(image):
    new_image = np.zeros((len(image), len(image[0]), 3), dtype=np.int32)
    for row_num in range(len(image)):
        for ind_num in range(len(image[row_num])):
            category = image[row_num][ind_num]
            new_image[row_num, ind_num] = cat_to_color[category]
    return new_image
