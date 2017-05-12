'''A module for generating images containing a year to be placed on a test'''
import os
from os import path

import cv2
import numpy as np


class Generator(object):
    '''
    A class that facilitates the creation of images containing text.
    The fate of the created images is getting overlayed onto a PDF.
    '''

    def __init__(self):
        self.directory = path.abspath(path.join(os.getcwd(), 'generated_images/'))
        if not path.exists(directory):
            os.makedirs(directory)

    def generate(self, string):
        '''Creates an image containing the string given in the parameters. Returns the image path.'''
        file_path = path.join(directory, '{}.jpg'.format(string))
        if os.path.exists(file_path):
            return file_path
        width, height = cv2.getTextSize(string, cv2.FONT_HERSHEY_PLAIN, 2, 3)[0]
        img = np.full((height, width), 255, dtype = np.uint8)
        cv2.putText(img, string, (0, height), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        cv2.imwrite(file_path, img)
        return file_path
