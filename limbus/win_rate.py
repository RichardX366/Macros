from threading import Thread
from time import sleep
from typing import Any

from helpers import WindowHelper

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
            wh.press("p")
            sleep(0.1)
            wh.press("enter")
            sleep(5)
        if wh.click_text(
            "Confirm",
            top=0.7,
            left=0.7,
            click=False,
            retry=False,
        ):
            wh.press("enter")
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
