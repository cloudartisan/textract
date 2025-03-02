#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="textract",
    version="0.1.0",
    description="A tool for extracting text from images using OCR",
    author="CloudArtisan",
    author_email="david@cloudartisan.com",
    url="https://github.com/cloudartisan/textract",
    py_modules=["textract"],
    entry_points={
        "console_scripts": [
            "textract=textract:cli",
        ],
    },
    install_requires=[
        "pytesseract",
        "Pillow",
        "pyautogui",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)