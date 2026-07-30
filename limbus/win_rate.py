from threading import Thread
from time import sleep
from typing import Any

import keyboard

from helpers import WindowHelper, is_windows

try:
    wh = WindowHelper("LimbusCompany")
except:
    wh = WindowHelper("iPhone Mirroring")


def worker():
    while True:
        if wh.click_text(
            "Win",
            top=0.6,
            left=0.5,
            height=0.3,
            click=False,
            retry=False,
        ):
            if is_windows():
                wh.focus_window()
            wh.press("p")
            sleep(0.1)
            wh.press("enter")
            if is_windows():
                wh.restore_previous_window()
            sleep(5)
        if wh.click_text(
            "Confirm",
            top=0.7,
            left=0.7,
            click=False,
            retry=False,
        ):
            if is_windows():
                wh.focus_window()
            wh.press("enter")
            if is_windows():
                wh.restore_previous_window()
            sleep(5)
        sleep(1)


if __name__ == "__main__":
    print("Win rate ready.")

    keyboard.add_hotkey("ctrl+\\", lambda: wh.mute(), suppress=True)

    print("Press Ctrl + \\ or press enter in the terminal to toggle volume.")

    Thread(target=worker, daemon=True).start()

    while True:
        input()
        wh.mute()
