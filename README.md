## Getting Started

### Install pyenv & pipenv

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
pipenv run ./pincidents.py [...]
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
