#System Imports
import os

# Third Party Imports
import video_to_frames
import cv2
import numpy as np
np.seterr(over='ignore')

SAMPLE_NAME = 'sample.avi'
OUTPUT_NAME = 'result.jpg'

# Path of the main .py script
SCRIPT_PATH = os.path.dirname(__file__)
# Path to save the produced results
RESULTS_PATH = os.path.join(SCRIPT_PATH, 'results')
# Path of the sample to test
PATH_TO_SAMPLE = os.path.join(SCRIPT_PATH, f'videos/{SAMPLE_NAME}')

PATH_TO_FIRST_FRAME = os.path.join(SCRIPT_PATH,'results/frame0.jpg')

PATH_TO_FINAL_RESULT = os.path.join(SCRIPT_PATH, 'final_results')

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

def quantize_all_arrays(super_array, quantization_level):
	array = [quantize(super_array[0],quantization_level)]
	count=1
	try:
		while True:
			array.append(quantize(super_array[count],quantization_level))
			
			count+=1
	except:
		array = np.array(array)
		return array

def calculate_difference(image2, image1):
	return image2-image1

def calculate_all_arrays(first_image_array):
	all_frames=[first_image_array]
	count=0
	try:
		while True:
			
			prev_image=image_to_array(os.path.join(SCRIPT_PATH,'results/frame{}.jpg'.format(count)))
			new_image=image_to_array(os.path.join(SCRIPT_PATH,'results/frame{}.jpg'.format(count+1)))
			difference_array=calculate_difference(new_image,prev_image)
			all_frames.append(difference_array)
			count+=1
	except:
		all_frames = np.array(all_frames)
		return all_frames

def compression_ratio():
	count = 0
	size_of_frames=0
	size_of_encoded=0
	try:
		while True:
			size_of_frames = size_of_frames + os.path.getsize('results/frame{}.jpg'.format(count))
			size_of_encoded = size_of_encoded + os.path.getsize('final_results/frame{}.jpg'.format(count))
			count+=1
	except:
		return size_of_frames/size_of_encoded
    

if __name__ == '__main__':
	print("Please place the video file into videos folder with name 'sample.avi'...")
	try:
		print("Creating frames from video and save them to results folder...")
		video_to_frames.VideoToFramesConverter(PATH_TO_SAMPLE,RESULTS_PATH).create_frames()
	except:
		print("Error with the video file")
		exit()

	while True:
		try:
			quantization_level = input("Please enter quantization level... ")
			quantization_level = int(quantization_level)
			break
		except:
			print("Error with the input. You must select a number. Please try again...")
	print("Creating array with all frames based on DPCM algorithm...")
	all_frames = calculate_all_arrays(image_to_array(PATH_TO_FIRST_FRAME))
	print("Quantilize all encoded frames (this step may take a while)...")
	quantized_frames = quantize_all_arrays(all_frames, quantization_level)
	print("Saving new frames to final_results folder...")
	try:
		count=0
		while True:
			cv2.imwrite(os.path.join(PATH_TO_FINAL_RESULT, f'frame{count}.jpg'),quantized_frames[count])
			count+=1
	except:
		print("Compression Ratio is: ",compression_ratio())
	input("Done")
