'''This file manages all PDFs, whether they be cached tests or created tests'''

from os import getcwd
from os import path
from os import remove
from random import shuffle
from time import time

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas

from generate import Generator

TEMP = path.join(getcwd(), 'temp/')

class TestHandler(object):
    ''''''
    def __init__(self):
        #self.image_generator = Generator()
        pass
    
    def label_test(self, test_path, label):
        #generated_image = self.image_generator.generate(label)
        temp_file_name = '{}'.format(time()).replace('.', '').split()
        shuffle(temp_file_name)
        temp_file_name = ''.join(temp_file_name)
        temp_pdf_path = path.join(TEMP, '{}.pdf'.format(temp_file_name))
        canvas = Canvas(temp_pdf_path, pagesize = letter, bottomup = 0)
        canvas.drawString(72, 36, label)
        canvas.save()
        mao_test_context = open(test_path, 'rb')
        with open(temp_pdf_path, 'rb') as header_text_context:
            mao_test = PdfFileReader(mao_test_context)
            header_text = PdfFileReader(header_text_context)
            output = PdfFileWriter()
            first_page = mao_test.getPage(0)
            first_page.mergePage(header_text.getPage(0))
            output.addPage(first_page)
            for page_num in range(1, mao_test.numPages):
                output.addPage(mao_test.getPage(page_num))
            mao_test_context.close()
            remove(test_path)
            with open(test_path, 'wb') as mao_test_context:
                output.write(mao_test_context)
        remove(temp_pdf_path)
