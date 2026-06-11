from time import sleep

from pyautogui import press
from helpers import WindowHelper

if __name__ == "__main__":
    wh = WindowHelper("LimbusCompany", 1.5)

    while True:
        if wh.click_text("Win", top=0.7, left=0.7, height=0.2):
            wh.focus_window()
            sleep(0.1)
            press("enter")
            sleep(0.2)
            wh.restore_previous_window()
            sleep(5)
        sleep(1)
