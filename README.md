# My Python Scripts

Some do a little, some do a lot. Most scripts are documented with comments and
docstrings, and many depend on my unreleased (on pypi, anyway)
[teacher-helper](https://github.com/jdevries3133/teacher-helper)
libraries.

## Requirements

There is no requirements.txt because I usually run these scripts on globally
installed pacakges, and each script stands alone with different dependencies.
If you want to use a script, just take a quick look at the import statements;
third party libraries are always separated from built-in libraries by a newline.

For convenience of perusal, though, here is a list of some of the libraries
used:

- Optical Character Recognition (image-to-text)
  - cv2
  - pytesseract
- GUI
  - pyautogui
  - pyperclip
