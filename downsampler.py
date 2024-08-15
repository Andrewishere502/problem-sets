import pathlib

import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread


def downsample(input_im: np.ndarray[int], target_width: int, target_height: int):
    input_im_width: int = input_im.shape[1]
    input_im_height: int = input_im.shape[0]

    # Ensure input width and height are actually larger than the
    # target's.
    assert input_im_width > target_width
    assert input_im_height > target_height

    # Create an array to down sample the original image into
    output_im: np.ndarray = np.ndarray((target_height, target_width))

    # Calculate the number of pixels in the original image per pixel
    # in the output image. Do this in the vertical and horizontal
    # directions independently.
    width_ratio: float = input_im_width / target_width
    height_ratio: float = input_im_height / target_height

    for row_i, row in enumerate(output_im):
        for col_i, pixel in enumerate(row):
            # The total columns that have been used thus far
            col_acc_dist = col_i * width_ratio
            # The number of whole columns this downsampled pixel will
            # include.
            col_whole_width = int(width_ratio)
            # The residual columns this downsampled pixel will include
            col_res_weight = width_ratio % 1  # Get decimal components
            # The portion of the column to the left that the downsampled
            # pixel will include.
            col_left_res_weight = col_res_weight * (col_i / (target_width - 1))
            # The portion of the column to the right that the downsampled
            # pixel will include.
            col_right_res_weight = col_res_weight * (1 - (col_i / (target_width - 1)))
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
            row_up_res_weight = row_res_weight * (row_i / (target_height - 1))
            # The portion of the row below that the downsampled pixel will
            # include.
            row_bot_res_weight = row_res_weight * (1 - (row_i / (target_height - 1)))
            # The index of the row to start in 
            row_start_i = int(row_acc_dist)
            # The index of the column to end in (included!)
            row_end_i = row_start_i + row_whole_height + (row_up_res_weight > 0.0) + (row_bot_res_weight > 0.0)

            # Get the values for the pixels included in this pixel
            px_value = 0
            max_px_value = 0
            # Loop over each pixel in the output image, calculating the
            # proportion of each corresponding pixel in the input image
            # that should be included in the output pixel.
            for input_row_i in range(row_start_i, row_end_i):
                for input_col_i in range(col_start_i, col_end_i):
                    # If this is the left/right most column, use residual
                    # weights.
                    col_weight = 1
                    if input_col_i == col_start_i and col_left_res_weight > 0:
                        col_weight = col_left_res_weight
                    elif input_col_i == col_end_i - 1 and col_right_res_weight > 0:
                        col_weight = col_right_res_weight

                    # If this is the up/bottom most column, use residual
                    # weights.
                    row_weight = 1
                    if input_row_i == row_start_i and row_up_res_weight > 0:
                        row_weight = row_up_res_weight
                    elif input_row_i == row_end_i - 1 and row_bot_res_weight > 0:
                        row_weight = row_bot_res_weight
                    
                    # Add the weighted pixel value to the sum for
                    # this downsampled pixel.
                    px_value += int(input_im[input_row_i][input_col_i]) * col_weight * row_weight
                    # Add the maximum weighted pixel value to another
                    # sum to normalize this pixel later.
                    max_px_value += col_weight * row_weight

            # Store the calculated downsampled pixel value
            output_im[row_i][col_i] = (px_value / max_px_value) > 0.5
    return output_im


def main():
    input_im = np.random.rand(100, 100) > 0.5

    output_im = downsample(input_im, 90, 90)

    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(input_im)
    axs[1].imshow(output_im)
    plt.show()
    return


if __name__ == '__main__':
    main()
