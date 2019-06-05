#System Imports
import os

# Third Party Imports
import video_to_frames

SAMPLE_NAME = 'sample.avi'
OUTPUT_NAME = 'result.jpg'

# Path of the main .py script
SCRIPT_PATH = os.path.dirname(__file__)
# Path to save the produced results
RESULTS_PATH = os.path.join(SCRIPT_PATH, 'results')
# Path of the sample to test
PATH_TO_SAMPLE = os.path.join(SCRIPT_PATH, f'videos/{SAMPLE_NAME}')

QUANTIZATION_LEVEL = 10

if __name__ == '__main__':

    converter = video_to_frames.VideoToFramesConverter(PATH_TO_SAMPLE,
                                                       RESULTS_PATH).create_frames()
