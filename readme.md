# About

This is a collection of my macros.

## Python

Run child programs with `python -m <filename>` to avoid issues with imports.
The Python should work on Mac and Windows, but you can't focus/restore windows on Mac.
When using WindowHelper, be sure to initialize it before importing pyautogui since the import messes up the DPI.

## Installation

For any of the NodeJS macros, just install with yarn.
Just run `pip install -r requirements.txt` to install the dependencies for Python (I use 3.13.14).

## Shortcuts

To make shortcuts, just do `python.exe -m limbus.mirror_dungeon` in Target and the path to the Macros repository in the Start in field. You can also add keyboard shortcuts to launch this way.
