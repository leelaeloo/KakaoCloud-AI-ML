import pytesseract
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

class TesseractOCR:
    def __init__(self):
        pass

    def get_available_languages(self):
        langs = pytesseract.get_languages()
        return langs
    
    def orc_with_bbox(self, image, lang='eng'):
        data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)

        result_image = image.copy()

        for i in range(len[data['text']]):
            if int(data['conf'][i]) > 60:
                