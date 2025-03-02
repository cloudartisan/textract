# Textract

A Python tool for extracting text from images using OCR (Optical Character Recognition).

## Features

- Extract text from screen captures with optional delay
- Extract text from image files
- Specify screen regions for targeted extraction
- Resize images to improve OCR accuracy
- Save processed images
- Output text to stdout or files

## Getting Started

### Install dependencies

For MacOS:

```
brew install tesseract tesseract-lang
brew install pyenv
pip install --user pipenv
```

### Create the virtual environment

```
pipenv install
```

### Using the virtual environment

Drop into the shell:

```
pipenv shell
```

Or run commands in the shell:

```
pipenv run python textract.py [arguments]
```

### Examples

Extract text from screen with a 3-second delay:
```
pipenv run python textract.py screen --delay 3
```

Extract text from a specific screen region:
```
pipenv run python textract.py screen --region 100 100 500 300
```

Extract text from an image file:
```
pipenv run python textract.py image --infile test/terraform_text.png
```

Save the processed image:
```
pipenv run python textract.py image --infile test/terraform_text.png --save output.png
```

Enlarge the image by 2x for better OCR accuracy:
```
pipenv run python textract.py image --infile test/terraform_text.png --enlarge 2
```

## TODO

- Add automated tests
- Test for and handle image size limits 
  - `DecompressionBombWarning ... exceeds limit of 89478485 pixels, could be decompression bomb DOS attack` from `PIL`
  - `TesseractError ... Image too large` from `pytesseract`
- Verify that `--region` does not exceed the screen coordinates
- Support using `--region` on image source as well as screen source
- Add support for mouse drag and select
- Add a window source with selection by mouse click
- Add support for countdown as a graphical overlay
