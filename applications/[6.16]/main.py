# System Imports
import os
import math

#     Third-party imports
import cv2

SAMPLE_NAME = 'sample.jpg'
OUTPUT_NAME = 'result.jpg'

SCRIPT_PATH = os.path.dirname(__file__)

RESULTS_DIR = os.path.join(SCRIPT_PATH, 'results')
PATH_TO_SAMPLE = os.path.join(SCRIPT_PATH, 'images/{}'.format(SAMPLE_NAME))




def image_to_array(image):
    """Return the array representation of the loaded image"""

    return cv2.imread(image, flags=cv2.IMREAD_UNCHANGED)


def quantize(array, quantization_level):
    """Quantizes the image

    Loops through the image array row by row by dividing each
    pixel's value by the quantization_level and flooring the result.

    Args:
        array: An array of cells with pixel values
        quantization_level: Divides each cell by this value


    Returns:
        An array with the quantized values for each cell/pixel.
    """

    image_height = len(array)
    image_width = len(array[0])

    for row in range(0, image_height):
        for column in range(0, image_width):
            new_pixel = image_array[row][column] / quantization_level
            array[row][column] = new_pixel

    return array

def euclidian_distance(vector_a, vector_b):
    """Calculates the euclidian distance between two vectors"""

    return math.sqrt(sum([(vector_a - vector_b) for vector_a, vector_b in zip(vector_a, vector_b)]))

def are_pixels_equal(pixel_1, pixel_2):
    """Checks if two RGB/Grayscale pixels are equal"""

    if euclidian_distance(pixel_1, pixel_2) == 0:
        return True
    return False

def next_pixel_exists(image_width, position):
    """Checks if theres a next pixel in the given row"""

    if position + 1 > image_width - 1:
        return False
    return True


def run_length_encoder(array):
    """Quantizes the image

    Run-length encoding (RLE) is a very simple form of lossless data
    compression in which runs of data (that is, sequences in which the same
    data value occurs in many consecutive data elements) are stored as a
    single data value and count, rather than as the original run.

    Args:
        array: Each cell/pixel represents a level a of gray
        quantization_level: Divides each cell by this value


    Returns:
        An array with the quantized values for each cell/pixel.
    """

    image_height = len(array)
    image_width = len(array[0])

    # Iit
    # Used for producing the encoded string
    encoded_list = []
    encoded_list.append(str(image_height))
    encoded_list.append(str(image_width))
    encoded_list.append("(0,0){}".format(array[0][0]))

    for row in range(1, image_height):
        counter = 0
        for column in range(0, image_width):
            this_pixel = array[row][column]

            if next_pixel_exists(image_width, column):
                next_pixel = array[row][column + 1]

                if are_pixels_equal(this_pixel, next_pixel):
                    counter = counter + 1
                else:
                    counter = counter + 1
                    encoded_list.append("({},{}){}".format(row, column, array[row][column]))

                if counter > image_width - 1:
                    counter = 0

    return '|'.join(encoded_list)

if __name__ == '__main__':

    image_array = image_to_array(PATH_TO_SAMPLE)
    quantized_array = quantize(image_array, 10)
    # print(image_array)
    # cv2.imwrite(PATH_TO_RESULT, quantized_array)
    encoded_string = run_length_encoder(quantized_array)

    with open(os.path.join(RESULTS_DIR, 'encoded_string.txt'), "w") as \
            text_file:
        print(encoded_string, file=text_file)
