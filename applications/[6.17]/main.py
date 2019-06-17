#System Imports
import os

# Third Party Imports
import video_to_frames
import cv2
import numpy as np


SAMPLE_NAME = 'sample.avi'

# Path of the main .py script
SCRIPT_PATH = os.path.dirname(__file__)

# Path to save the produced results
RESULTS_PATH = os.path.join(SCRIPT_PATH, 'results')

# Path of the sample to test
PATH_TO_SAMPLE = os.path.join(SCRIPT_PATH, f'videos/{SAMPLE_NAME}')
PATH_TO_SAMPLES = os.path.join(SCRIPT_PATH, 'videos')
PATH_TO_FRAMES = os.path.join(PATH_TO_SAMPLES, 'frames')

PATH_TO_RESULTS_FOLDER = os.path.join(SCRIPT_PATH, 'results')
PATH_TO_THE_QUANTIZED_FRAMES = os.path.join(PATH_TO_RESULTS_FOLDER, 'frames')

def erase_directyory(path):
	"""Erases the content of the given directory"""

	filelist = [f for f in os.listdir(path) if f.endswith(".jpg")]
	for f in filelist:
		os.remove(os.path.join(path, f))

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
            new_pixel = array[row][column] / quantization_level
            array[row][column] = new_pixel

    return array

def quantize_all_arrays(matrix, quantization_level):
	"""Applys the quantization algorithm for each frame"""

	return [quantize(item, quantization_level)for item in matrix]

def calculate_difference(image_1, image_2):
	"""Calculates the difference between to sequencial images"""

	return image_2 - image_1

def calculate_differences_matrix():

	differences_array = []

	PATH_TO_FRAMES = os.path.join(PATH_TO_SAMPLES, 'frames')

	frames_len = len(os.listdir(PATH_TO_FRAMES))

	for frame_number in range(1, frames_len):
		previous_image = image_to_array(os.path.join(PATH_TO_FRAMES, f'frame{frame_number - 1}.jpg'))
		new_image = image_to_array(os.path.join(PATH_TO_FRAMES, f'frame{frame_number}.jpg'))

		difference = calculate_difference(previous_image, new_image)
		differences_array.append(difference)


	all_frames = np.array(differences_array)

	return all_frames

def compression_ratio():

	size_of_original_frames = os.path.getsize(PATH_TO_FRAMES)
	size_of_the_compressed = os.path.getsize(PATH_TO_THE_QUANTIZED_FRAMES)

	print(f'Size of the original data: {size_of_original_frames}')
	print(f'Size of the compressed data: {size_of_the_compressed}')

	return size_of_original_frames / size_of_the_compressed


if __name__ == '__main__':
	erase_directyory(PATH_TO_FRAMES)
	erase_directyory(PATH_TO_THE_QUANTIZED_FRAMES)

	if (os.path.exists(PATH_TO_SAMPLE)):
		PATH_TO_SAVED_FRAMES = os.path.join(SCRIPT_PATH, 'videos/frames')
		converter = video_to_frames.VideoToFramesConverter(PATH_TO_SAMPLE,
											   PATH_TO_SAVED_FRAMES)
		converter.create_frames()
		size = converter.size
		print("Creating frames from video and save them to results folder...")
	else:
		print(
			"Place the video file named 'sample.avi' into /videos and try "
			"again...")
		enter_to_exit = input()
		exit()

	quantization_level = int(input("Please enter quantization "
										   "level..."))

	print("Creating array with all frames based on DPCM algorithm...")
	differences_matrix = calculate_differences_matrix()

	print("Quantize all encoded frames (this step may take a while)...")
	quantized_frames = quantize_all_arrays(differences_matrix, quantization_level)

	print("Saving new frames to results folder...")

	out = cv2.VideoWriter('final.avi', cv2.VideoWriter_fourcc(*'DIVX'),
						  30, (1280, 720))

	for index, frame in enumerate(quantized_frames):
		cv2.imwrite(os.path.join(PATH_TO_THE_QUANTIZED_FRAMES, f'frame{index}.jpg'),
						frame)

		out.write(frame)
	out.release()

	print(f'Compression Ratio is: {compression_ratio()}')
	input("Done")
