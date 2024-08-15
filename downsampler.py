import numpy as np

import matplotlib.pyplot as plt


im1_width = 100
im1_height = 100

im2_width = 80
im2_height = 80

# Ensure image 1 is bigger than image 2
assert im1_width > im2_width
assert im1_height > im2_height

data_im = np.random.rand(im1_height, im1_width) > 0.5
# data_im = [
#     [1, 1, 0, 0, 0],
#     [1, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1],
#     [0, 0, 0, 1, 1],
# ]
# data_im = [
#     [0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
# ]
# print(data_im)
down_sampled_im = np.zeros((im2_height, im2_width))
# print(down_sampled_im)

width_ratio = im1_width / im2_width
height_ratio = im1_height / im2_height
for row_i, row in enumerate(down_sampled_im):
    for col_i, pixel in enumerate(row):
        print(row_i, col_i)
        # The total columns that have been used thus far
        col_acc_dist = col_i * width_ratio
        # The number of whole columns this downsampled pixel will
        # include.
        col_whole_width = int(width_ratio)
        # The residual columns this downsampled pixel will include
        col_res_weight = width_ratio % 1  # Get decimal components
        # The portion of the column to the left that the downsampled
        # pixel will include.
        col_left_res_weight = col_res_weight * (col_i / (im2_width - 1))
        # The portion of the column to the right that the downsampled
        # pixel will include.
        col_right_res_weight = col_res_weight * (1 - (col_i / (im2_width - 1)))
        # The index of the column to start in
        col_start_i = int(col_acc_dist)
        # The index of the column to end in (included!)
        col_end_i = col_start_i + col_whole_width + (col_left_res_weight > 0.0) + (col_right_res_weight > 0.0)

        # The total rows that have been used thus far
        row_acc_dist = row_i * height_ratio
        # The number of whole rows this downsampled pixel will include.
        row_whole_height = int(height_ratio)
        # The residual columns this downsampled pixel will include
        row_res_weight = height_ratio % 1  # Get decimal components
        # The portion of the row above that the downsampled pixel will
        # include.
        row_up_res_weight = row_res_weight * (row_i / (im2_height - 1))
        # The portion of the row below that the downsampled pixel will
        # include.
        row_bot_res_weight = row_res_weight * (1 - (row_i / (im2_height - 1)))
        # The index of the row to start in 
        row_start_i = int(row_acc_dist)
        # The index of the column to end in (included!)
        row_end_i = row_start_i + row_whole_height + (row_up_res_weight > 0.0) + (row_bot_res_weight > 0.0)

        # print('\tCol', col_left_res_weight, col_whole_width, col_right_res_weight)
        # print('\tRow', row_up_res_weight, row_whole_height, row_bot_res_weight)

        # Get the values for the pixels included in this pixel
        px_value = 0
        max_px_value = 0
        for data_row_i in range(row_start_i, row_end_i):
            for data_col_i in range(col_start_i, col_end_i):
                # If this is the left/right most column, use residual
                # weights
                col_weight = 1
                if data_col_i == col_start_i and col_left_res_weight > 0:
                    col_weight = col_left_res_weight
                elif data_col_i == col_end_i - 1 and col_right_res_weight > 0:
                    col_weight = col_right_res_weight

                # If this is the up/bottom most column, use residual
                # weights
                row_weight = 1
                if data_row_i == row_start_i and row_up_res_weight > 0:
                    row_weight = row_up_res_weight
                elif data_row_i == row_end_i - 1 and row_bot_res_weight > 0:
                    row_weight = row_bot_res_weight
                
                # print(data_im[data_row_i][data_col_i], col_weight, row_weight)
                # print('\t', data_col_i, data_row_i, col_weight, row_weight, end=' = ')
                # print(int(data_im[data_row_i][data_col_i]) * col_weight * row_weight)
                print('\t', data_col_i, data_row_i, col_weight * row_weight)
                px_value += int(data_im[data_row_i][data_col_i]) * col_weight * row_weight
                max_px_value += col_weight * row_weight
        print('\t=', px_value)
        down_sampled_im[row_i][col_i] = px_value / max_px_value > 0.5
        # print(px_value)

fig, axs = plt.subplots(1, 2)
axs[0].imshow(data_im)
axs[1].imshow(down_sampled_im)
plt.show()

