from subprocess import Popen
from time import sleep
import pygetwindow as gw
import mss

from helpers import is_windows


def launch_limbus():
    if not is_windows():
        raise EnvironmentError("This function is only supported on Windows.")

    if gw.getWindowsWithTitle("LimbusCompany"):
        exit()

    process = Popen(
        [
            "%appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Steam\\Limbus Company.url"
        ],
        shell=True,
    )

    while not gw.getWindowsWithTitle("LimbusCompany"):  # type: ignore
        sleep(0.5)

    windows = gw.getWindowsWithTitle("LimbusCompany")  # type: ignore

    window = windows[0]  # Get the first matching window

    with mss.MSS() as sct:
        monitors = sct.monitors[1:]
        leftmost_monitor = min(monitors, key=lambda m: m["left"])

    window.moveTo(leftmost_monitor["left"], leftmost_monitor["top"])
    sleep(0.1)
    window.resizeTo(leftmost_monitor["width"], leftmost_monitor["height"])
    sleep(0.1)
    window.maximize()
    sleep(0.1)

    return process
