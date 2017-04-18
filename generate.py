'''A module for generating images containing a year to be placed on a test'''
import os
from os import path

import cv2
import numpy as np

DIR = path.abspath(path.join('.', 'generated_images/'))
if not path.exists(DIR):
    os.makedirs(DIR)

def generate(year):
    '''Creates an image containing the year given in the parameters. Returns the image path.'''
    file_path = path.join(DIR, '{}.jpg'.format(str(year)))
    if os.path.exists(file_path):
        return file_path
    width, height = cv2.getTextSize(str(year), cv2.FONT_HERSHEY_PLAIN, 2, 3)[0]
    img = np.full((height, width), 255, dtype=np.uint8)
    cv2.putText(img, str(year), (0, height), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
    cv2.imwrite(file_path, img)
    return file_path
