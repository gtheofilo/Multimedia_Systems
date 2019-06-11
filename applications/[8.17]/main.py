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
def save_video(frames):
	height, width, layers = frames[0].shape
	video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width,height))

	for i in range(1, len(frames)-1):
		video.write(frames[i])

	
	video.release()
	cv2.destroyAllWindows()
    

if __name__ == '__main__':
	print("Please place the video file into videos folder with name 'sample.avi'...")
	try:
		print("Creating frames from video and save them to results folder...")
		video_to_frames.VideoToFramesConverter(PATH_TO_SAMPLE,RESULTS_PATH).create_frames()
	except:
		print("Error with the video file")
		exit()

	print("Creating array with all error frames...")
	all_frames = calculate_all_arrays(image_to_array(PATH_TO_FIRST_FRAME))
	print("Saving new frames to final_results folder...")
	try:
		count=0
		while True:
			cv2.imwrite(os.path.join(PATH_TO_FINAL_RESULT, f'frame{count}.jpg'),all_frames[count+1])
			count+=1
	except:
		print("Creating video of error frames...")
		save_video(all_frames)
	
