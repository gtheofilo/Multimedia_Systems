# System Imports
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
PATH_TO_SAMPLES = os.path.join(SCRIPT_PATH, 'videos')
PATH_TO_FRAMES = os.path.join(PATH_TO_SAMPLES, 'frames')

PATH_TO_RESULTS_FOLDER = os.path.join(SCRIPT_PATH, 'results')
PATH_TO_THE_QUANTIZED_FRAMES = os.path.join(PATH_TO_RESULTS_FOLDER, 'frames')

PATH_TO_FIRST_FRAME = os.path.join(PATH_TO_FRAMES, 'frame0.jpg')

PATH_TO_FIRST_BULLET = os.path.join(SCRIPT_PATH, 'first_bullet')


def image_to_array(image):
    """Return the array representation of the loaded image"""

    return cv2.imread(image, flags=cv2.IMREAD_UNCHANGED)


def calculate_difference(image2, image1):
    """Calculates the error """

    return image2 - image1

def frame_to_macroblock(frame):
    """Converts a frame to 16x16 macroblocks"""

    image = frame

    block = np.zeros(frame.shape)

    image_height, image_width = frame.shape[:2]

    block_height = 16

    block_width = 16

    for row in np.arange(image_height - block_height + 1, step=block_width):

        for column in np.arange(image_width - block_width + 1, step=block_width):

            block[row:row + block_height, column:column + block_width] = image[
                                                                     row:row + block_height, column:column + block_width]
    return block



def calculate_all_arrays(first_image_array):
    """Calculates the difference"""

    all_frames = [first_image_array]
    count = 0
    try:
        while True:
            prev_image = image_to_array(
                os.path.join(PATH_TO_FRAMES, 'frame{}.jpg'.format(count)))
            new_image = image_to_array(os.path.join(PATH_TO_FRAMES,
                                                    'frame{}.jpg'.format(
                                                        count + 1)))
            difference_array = calculate_difference(new_image, prev_image)
            all_frames.append(difference_array)
            count += 1
    except:
        all_frames = np.array(all_frames)

        return all_frames


def save_video(frames):
    """Saves the DPCM encoded video"""

    height, width, layers = frames[0].shape
    video = cv2.VideoWriter(os.path.join(PATH_TO_FIRST_BULLET, 'result.avi'),
                            cv2.VideoWriter_fourcc(*'XVID'),
                            30,
                            (width, height))

    for i in range(1, len(frames) - 1):
        video.write(frames[i])

    video.release()
    cv2.destroyAllWindows()


def bullet_1():
    print("Creating the array with all the error frames...")
    all_frames = calculate_all_arrays(image_to_array(PATH_TO_FIRST_FRAME))
    print("Saving new frames to final_results folder...")
    try:
        count = 0
        while True:
            cv2.imwrite(os.path.join(PATH_TO_FIRST_BULLET, f'frames/frame{count}.jpg'),all_frames[count + 1])
            count += 1
    except:
        print("Creating video of error frames...")
        save_video(all_frames)


if __name__ == '__main__':
    video = video_to_frames.VideoToFramesConverter(PATH_TO_SAMPLE,
                                                   PATH_TO_FRAMES)
    video.create_frames()

    bullet_1()



