#!/usr/bin/env python

import pyautogui
from PIL import Image
from pytesseract import *

# Note: change the path below to point to the tesseract binary
pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

image = Image.open('terraform_text.png')
output = pytesseract.image_to_string(image)
print(output)
