from time import sleep
from typing import Any

from pyautogui import press
from helpers import WindowHelper
import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

sessions = AudioUtilities.GetAllSessions()
volume: Any = None

for session in sessions:
    if session.Process:
        if session.Process.name() == "LimbusCompany.exe":
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)


if __name__ == "__main__":
    keyboard.add_hotkey(
        "ctrl+\\", lambda: volume.SetMute(not volume.GetMute(), None), suppress=True
    )

    wh = WindowHelper("LimbusCompany", 1.5)

    print("Win rate ready. Press Ctrl + \\ to toggle volume.")

    while True:
        if wh.click_text("Win", top=0.7, left=0.7, height=0.2, click=False):
            wh.focus_window()
            sleep(0.2)
            press("p")
            sleep(0.1)
            press("enter")
            sleep(0.2)
            wh.restore_previous_window()
            sleep(5)
        sleep(1)
