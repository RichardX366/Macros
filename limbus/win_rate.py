from threading import Thread
from time import sleep
from typing import Any

from helpers import WindowHelper

try:
    wh = WindowHelper("LimbusCompany")
except:
    wh = WindowHelper("iPhone Mirroring")

from pyautogui import press


def worker():
    while True:
        if wh.click_text(
            "Win",
            top=0.6,
            left=0.5,
            height=0.3,
            click=False,
            retry=False,
            includes=True,
        ):
            wh.focus_window()
            sleep(0.2)
            press("p")
            sleep(0.1)
            press("enter")
            sleep(0.2)
            wh.restore_previous_window()
            sleep(5)
        sleep(1)


if __name__ == "__main__":
    print("Win rate ready.")

    def toggle_volume():
        pass

    try:
        from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
        import keyboard

        sessions = AudioUtilities.GetAllSessions()
        volume: Any = None

        for session in sessions:
            if session.Process:
                if session.Process.name() == "LimbusCompany.exe":
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)

        def toggle_volume():
            volume.SetMute(not volume.GetMute(), None)

        keyboard.add_hotkey("ctrl+\\", lambda: toggle_volume(), suppress=True)

        print("Press Ctrl + \\ or press enter in the terminal to toggle volume.")

    except:
        print("Audio control not available. Volume toggle will not work.")

    Thread(target=worker, daemon=True).start()

    while True:
        input()
        toggle_volume()
