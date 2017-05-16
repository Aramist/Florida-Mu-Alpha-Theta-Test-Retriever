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

import requests

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

    def join_tests(self, tests):
        output = PdfFileWriter()
        for test_identifier in tests:
            test_url, file_name = test_identifier
            save_path = path.join(getcwd(), 'cached_tests/{}.pdf'.format(file_name))
            if not path.exists(save_path):
                mao_request = requests.get(url)
                with open(save_path, 'wb') as context:
                	for data in mao_request.iter_content(chunk_size = 128):
                		context.write(data)
                label_test(save_path, file_name)
            with open(save_path, 'rb') as context:
            	reader = PdfFileReader(context)
            	for page in range(reader.numPages()):
            		output.addPage(reader.getPage(page))
        out_path = path.join(getcwd(), 'cached_tests/{}.pdf'.format(str(time()).replace('.', ''))
        with open(out_path, 'wb') as context:
        	output.write(context)path.join(getcwd(), 'cached_tests/{}.jpg'.format(file_name))
