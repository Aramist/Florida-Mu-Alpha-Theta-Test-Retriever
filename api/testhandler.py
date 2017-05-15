'''This file manages all PDFs, whether they be cached tests or created tests'''

from io import BytesIO
from os import getcwd
from os import path
from os import remove
from random import shuffle
from time import time

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas

from requests import Requests

from generate import Generator

class TestHandler(object):
    '''A class that performs operations on PDF files'''
    def __init__(self):
        #self.image_generator = Generator()
        pass

    def label_test(self, test_path, label):
        #generated_image = self.image_generator.generate(label)
        buffer = BytesIO()
        canvas = Canvas(buffer, pagesize = letter, bottomup = 0)
        canvas.drawString(280, 432, label)
        canvas.save()
        buffer.seek(0)
        mao_test_context = open(test_path, 'rb')
        mao_test = PdfFileReader(mao_test_context)
        header_text = PdfFileReader(buffer)
        output = PdfFileWriter()
        output.addPage(header_text.getPage(0))
        for page_num in range(mao_test.numPages):
            output.addPage(mao_test.getPage(page_num))
        mao_test_context.close()
        remove(test_path)
        with open(test_path, 'wb') as mao_test_context:
            output.write(mao_test_context)

    def join_tests(self, tests, output = None):
        for test_identifier in tests:
            test_url, file_name = test_identifier
            if not path.exists(path.join(getcwd(), 'cached_tests/{}.jpg'.format(file_name))):
                save_path = path.join(getcwd(), 'cached_tests/{}.jpg'.format(file_name))
                