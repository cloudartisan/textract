#!/usr/bin/env python

"""
Extracts text from an image.

Supports extracting text from the screen or from a file.

The size of the image affects accuracy, the user may wish to enlarge
the image to improve accuracy. However, too much enlargement can cause
excessive demands on resources.
"""

import argparse
import sys
import time

import pyautogui
from PIL import Image
from pytesseract import *


SCREEN = 'screen'
IMAGE  = 'image'


def countdown(delay, callback=None):
    """
    Countdown until calling callback(). If the delay is 0 there is no
    countdown and callback() will be called immediately.
    """
    while delay:
        mins, secs = divmod(delay, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        delay -= 1
    if callback:
        return callback()


def parse_args():
    """
    Parse command-line arguments, allow the user to specify an enlargement
    multiplier, an input file, an output file, etc.
    """
    parser = argparse.ArgumentParser(description='Extract text from image data')
    parser.add_argument('--enlarge', metavar='X', type=int, default=1,
            help='enlargement multiplier (enlarge by X, 1 is no change)')
    parser.add_argument('--save', metavar='FILENAME', type=str,
            help='file to save the image, including transformations')
    parser.add_argument('--outfile', type=argparse.FileType('w'), default=sys.stdout,
            help='write extracted text to the named file')

    # Use a subparser to specify the source as screen or image
    subparsers = parser.add_subparsers(dest='source', title='sources',
            help='source')
    subparsers.required = True

    # The user can specify a delay when using the screen source
    subparser_screen = subparsers.add_parser(SCREEN, help='extract from the screen')
    subparser_screen.add_argument('--delay', type=int, default=0,
            help='delay in seconds before capturing the screen')
    subparser_screen.add_argument('--region', metavar=('X1','Y1','X2','Y2'), type=int, nargs=4,
            help='region of the screen (x1 y1 x2 y2)')

    # Require that the user specify either stdin or an input file as the image source
    subparser_image = subparsers.add_parser(IMAGE, help='extract from an image')
    subparser_image.add_argument('--infile', type=argparse.FileType('rb'), default=sys.stdin.buffer,
            help='input file, otherwise assumes stdin')

    # TODO add WINDOW subparser

    return parser.parse_args()


def find_tesseract():
    """
    Auto-detect the tesseract binary location.
    Return the path to the tesseract binary or None if not found.
    """
    import subprocess
    import os
    
    # Common paths to check
    possible_paths = [
        '/usr/local/bin/tesseract',
        '/opt/homebrew/bin/tesseract',
        '/usr/bin/tesseract'
    ]
    
    # First try to get it from PATH
    try:
        result = subprocess.run(['which', 'tesseract'], 
                                capture_output=True, text=True, check=False)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    # Check common locations
    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
    return None


def main():
    # Auto-detect tesseract binary path
    tesseract_path = find_tesseract()
    if not tesseract_path:
        print("Error: Tesseract not found. Please install tesseract-ocr package.", file=sys.stderr)
        sys.exit(1)
    
    pytesseract.tesseract_cmd = tesseract_path

    # Failsafes for pyautogui (move the mouse to the top-left to abort, use a
    # 0.1 second pause after each pyautogui call)
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    args = parse_args()
    if args.source == SCREEN:
        countdown(args.delay)
        image = pyautogui.screenshot(region=args.region)
    elif args.source == IMAGE:
        image = Image.open(args.infile)

    # The size of the image affects accuracy, the user may wish to enlarge the
    # image to improve accuracy; too much enlargement can cause excessive
    # demands on resources
    if args.enlarge > 1:
        new_size = tuple(args.enlarge * x for x in image.size)
        image = image.resize(new_size, Image.ANTIALIAS)

    # Save the transformed image; we do not save the raw, untransformed image
    # because that is not what we processed and, presumably, we will always
    # have access to that
    if args.save:
        image.save(args.save, 'png')

    output = pytesseract.image_to_string(image)
    args.outfile.write(output)


if __name__ == '__main__':
    main()
