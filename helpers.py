print("Loading modules...")

from json import dumps, loads

from math import exp
from os import popen
import subprocess
from time import sleep
from typing import Any, cast
from functools import wraps

import cv2
import easyocr
import numpy as np
import pygetwindow as gw
from PIL import Image, ImageChops, ImageGrab
import io
from rapidfuzz import process, fuzz

pre_click_delay_global = 0.0
post_click_delay_global = 0.2


# Decorators


def crops(func):
    @wraps(func)
    def wrapper(self, *args, top=0.0, left=0.0, width=0.0, height=0.0, **kwargs):
        if top or left or width or height:
            self.set_bounds(top, left, width, height)
        result = func(self, *args, **kwargs)
        if top or left or width or height:
            self.bounds = None
        return result

    return wrapper


def clicks(func):
    @wraps(func)
    def wrapper(self, *args, pre_click_delay=0.0, post_click_delay=0.2, **kwargs):
        global pre_click_delay_global, post_click_delay_global
        pre_set = pre_click_delay != 0.0
        post_set = post_click_delay != 0.2

        if pre_set:
            pre_click_delay_global = pre_click_delay
        if post_set:
            post_click_delay_global = post_click_delay

        result = func(
            self,
            *args,
            **kwargs,
        )

        if pre_set:
            pre_click_delay_global = 0.0
        if post_set:
            post_click_delay_global = 0.2
        return result

    return wrapper


# Helpers


def find_monitor(left, top, monitors: list[dict]):
    for monitor in monitors:
        if (
            monitor["top"] < top < monitor["top"] + monitor["height"]
            and monitor["left"] < left < monitor["left"] + monitor["width"]
        ):
            return monitor
    return monitors[0]


mac_clipboard = None


def mac_screenshot(window: int = 0):
    get_mac_clipboard()
    if window:
        subprocess.run(["screencapture", "-c", "-l", str(window)])
    else:
        subprocess.run(["screencapture", "-c"])
    img = ImageGrab.grabclipboard()
    restore_mac_clipboard()
    if not isinstance(img, Image.Image):
        return mac_screenshot(window)
    return cast(Image.Image, img)


def get_mac_clipboard():
    from AppKit import NSPasteboard  # type: ignore

    global mac_clipboard
    pasteboard = NSPasteboard.generalPasteboard()
    types = pasteboard.types()
    data = {}

    for t in types:
        content = pasteboard.dataForType_(t)
        if content:
            data[str(t)] = content

    mac_clipboard = data
    return data


def restore_mac_clipboard():
    from AppKit import NSPasteboard  # type: ignore

    global mac_clipboard
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.clearContents()
    for type_name, content in mac_clipboard.items():  # type: ignore
        pasteboard.setData_forType_(content, type_name)


def is_windows():
    return "getWindowsWithTitle" in dir(gw)


def to_json(obj):
    """
    Convert numpy types to native Python types for JSON serialization.
    """

    return loads(dumps(_to_json(obj)))


def _to_json(obj):
    if (
        isinstance(obj, np.ndarray)
        or isinstance(obj, np.integer)
        or isinstance(obj, np.floating)
    ):
        return obj.tolist()
    elif isinstance(obj, list):
        return [_to_json(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple(_to_json(x) for x in obj)
    elif isinstance(obj, dict):
        return {k: _to_json(v) for k, v in obj.items()}
    else:
        return obj


def bounding_box_center(box):
    pts = [(int(x), int(y)) for x, y in box]
    x1 = min(p[0] for p in pts)
    y1 = min(p[1] for p in pts)
    x2 = max(p[0] for p in pts)
    y2 = max(p[1] for p in pts)
    return (x1 + x2) // 2, (y1 + y2) // 2


def download_screenshot(image, filename="screenshot.png"):
    """
    Save the in-memory screenshot to a file.

    Args:
        image: PIL.Image object
        filename: Output filename (default: screenshot.png)
    """
    if image:
        image.save(filename)
    else:
        print("No image to save")


def get_screenshot_bytes(image):
    """
    Get the screenshot as bytes for further processing.

    Args:
        image: PIL.Image object

    Returns:
        bytes: Image data in PNG format
    """
    if image:
        bytes_buffer = io.BytesIO()
        image.save(bytes_buffer, format="PNG")
        return bytes_buffer.getvalue()
    return None


def sleep_windows():
    popen(
        """powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend',$false,$false)" """
    )


class WindowHelper:
    def set_window_box(self):
        if is_windows():
            self.window = gw.getWindowsWithTitle(self.title)[0]  # type: ignore

            if self.window is None:
                print(f"{self.title} window not found!")
                raise Exception(f"{self.title} window not found!")

            self.width = self.window.width
            self.height = self.window.height
            self.top = self.window.top
            self.left = self.window.left
            self.dpi = 1.0
        else:
            from pygb import getOpenedWindows

            self.window = self.title
            windows = [w for w in getOpenedWindows() if w["title"] == self.title]
            if not windows:
                raise Exception(f"{self.title} window not found!")
            window = windows[0]
            self.top = window["y"]
            self.left = window["x"]
            self.width = window["width"]
            self.height = window["height"]
            self.pid = window["pid"]
            self.windowNumber = window["windowNumber"]

    def __init__(self, title: str):
        self.title = title
        self.bounds = None
        self.ocr_cache = None
        self.old_pointer_pos = None

        self.set_window_box()

        try:
            self.ocr = easyocr.Reader(["en"], gpu=True)
        except Exception:
            self.ocr = easyocr.Reader(["en"], gpu=False)

        print("Window Helper initialized for:", self.title)

    def screenshot(self) -> Image.Image:
        """
        Capture a screenshot of the window and store it in memory.
        Handles per-monitor DPI scaling on multi-monitor setups.

        Returns:
            PIL.Image: The screenshot as a PIL Image object in memory
        """
        try:
            if is_windows():
                from windows_screenshot import windows_screenshot

                image = windows_screenshot(self.window._hWnd)  # type: ignore
            else:
                image = mac_screenshot(self.windowNumber)

            if self.bounds:
                image = image.crop(
                    (
                        self.bounds[0] * self.dpi,
                        self.bounds[1] * self.dpi,
                        self.bounds[2] * self.dpi,
                        self.bounds[3] * self.dpi,
                    )
                )

            # download_screenshot(image)

            return image

        except IndexError:
            raise Exception("Window not found!")
        except Exception as e:
            raise Exception(f"Error capturing screenshot: {e}")

    def press(self, key):
        if is_windows():
            from pyautogui import press

            press(key)
        else:
            from pygb import press

            press(key, window=self.pid)

    def set_bounds(self, top=0.0, left=0.0, width=0.0, height=0.0):
        if not width:
            width = 1 - left
        if not height:
            height = 1 - top

        self.bounds = (
            int(left * self.width),
            int(top * self.height),
            int((left + width) * self.width),
            int((top + height) * self.height),
        )

    @crops
    def get_diff_rate(self, duration=0.5, top=0.0, left=0.0, width=0.0, height=0.0):
        sc1 = self.screenshot().convert("L")
        sleep(duration)
        sc2 = self.screenshot().convert("L")

        # Find the % difference between sc1 and sc2
        diff = ImageChops.difference(sc1, sc2)
        # download_screenshot(diff, "diff.png")

        # Calculate the percentage of different pixels
        total_pixels = diff.size[0] * diff.size[1]
        histogram = diff.histogram()

        def f(x, k=0.05):
            return (1 - exp(-k * x)) / (1 - exp(-255 * k))

        for i in range(len(histogram)):
            histogram[i] = histogram[i] * f(i)  # type: ignore

        different_pixels = sum(histogram)  # Count non-zero pixels

        diff_rate = different_pixels / total_pixels

        return diff_rate

    @crops
    def diff_threshold(
        self,
        duration=0.5,
        threshold=0.01,
        num_runs=3,
        top=0.0,
        left=0.0,
        width=0.0,
        height=0.0,
    ):
        for _ in range(num_runs):
            rate = self.get_diff_rate(duration)
            if rate < threshold:
                return False
        return True

    def focus_window(self):
        if is_windows():
            self.current_window = gw.getActiveWindow()
            try:
                if self.window.isMinimized:  # type: ignore
                    self.window.restore()  # type: ignore
                self.window.activate()  # type: ignore
            except Exception as e:
                pass
        else:
            self.current_window = (
                subprocess.check_output(
                    [
                        "osascript",
                        "-e",
                        'tell application "System Events" to get name of first application process whose frontmost is true',
                    ]
                )
                .decode()
                .strip()
            )
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'tell application "{self.window}" to activate',
                ]
            )

    def restore_previous_window(self):
        if self.current_window is not None:
            if is_windows():
                try:
                    if self.current_window.isMinimized:  # type: ignore
                        self.current_window.restore()  # type: ignore
                    self.current_window.activate()  # type: ignore
                except Exception as e:
                    pass
            else:
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        f'tell application "{self.current_window}" to activate',
                    ]
                )

    def to_relative(self, x, y, relative=False):
        if relative:
            x = int(x * self.width)
            y = int(y * self.height)
        return x + self.left, y + self.top

    @clicks
    def click(self, x, y, relative=False, pre_click_delay=0.1, post_click_delay=0.2):
        from pyautogui import moveTo, position, click

        x, y = self.to_relative(x, y, relative)

        self.old_pointer_pos = position()

        global pre_click_delay_global, post_click_delay_global

        if pre_click_delay_global > 0:
            moveTo(x, y)
            sleep(pre_click_delay_global)

        click(x, y)

        if post_click_delay_global > 0:
            sleep(post_click_delay_global)

        if self.old_pointer_pos:
            moveTo(int(self.old_pointer_pos[0]), int(self.old_pointer_pos[1]))
            self.old_pointer_pos = None

    def drag(self, x1, y1, x2, y2, duration=0.5, relative=False):
        from pyautogui import moveTo, position, mouseDown, mouseUp

        x1, y1 = self.to_relative(x1, y1, relative)
        x2, y2 = self.to_relative(x2, y2, relative)

        self.old_pointer_pos = position()

        # Use pyautogui to perform a smooth drag
        moveTo(int(x1), int(y1))
        sleep(0.5)
        mouseDown()

        # dragTo will move the cursor to the target over duration
        moveTo(int(x2), int(y2), duration=duration)
        mouseUp()
        sleep(0.1)

        if self.old_pointer_pos:
            moveTo(int(self.old_pointer_pos[0]), int(self.old_pointer_pos[1]))
            self.old_pointer_pos = None

    @crops
    def read_screen(
        self,
        confidence_threshold=0.1,
        normalize_coordinates=True,
        use_cache=False,
        top=0.0,
        left=0.0,
        width=0.0,
        height=0.0,
    ):
        """
        Perform OCR on the current window's screenshot and return detected text with bounding boxes. Returns a list of tuples containing bounding box coordinates, detected text, and confidence score.
        """

        if use_cache and self.ocr_cache is not None:
            return self.ocr_cache

        img = cv2.cvtColor(np.array(self.screenshot()), cv2.COLOR_RGB2BGR)
        results = self.ocr.readtext(image=img)
        results = [
            (
                [
                    [
                        cast(int, x) / self.dpi,
                        cast(int, y) / self.dpi,
                    ]
                    for x, y in box
                ],
                detected_text,
                confidence,
            )
            for box, detected_text, confidence in results
            if cast(float, confidence) > confidence_threshold
        ]
        results.sort(key=lambda x: x[0][0][1])  # Sort by y-coordinate (top to bottom)

        if normalize_coordinates and self.bounds:
            for result in results:
                box = result[0]
                for point in box:
                    point[0] += self.bounds[0]
                    point[1] += self.bounds[1]

        self.ocr_cache = results

        return results

    @crops
    @clicks
    def click_text(
        self,
        text,
        confidence_threshold=0.2,
        fuzz_threshold=90,
        use_cache=False,
        includes=False,
        click=True,
        split_spaces=False,
        retry=True,
        top=0.0,
        left=0.0,
        width=0.0,
        height=0.0,
        pre_click_delay=0.0,
        post_click_delay=0.2,
    ):
        args = (
            text,
            confidence_threshold,
            fuzz_threshold,
            use_cache,
            includes,
            click,
            split_spaces,
            retry,
            top,
            left,
            width,
            height,
        )

        results = self.read_screen(confidence_threshold, True, use_cache)

        if not results:
            if retry and not use_cache:
                sleep(1)
                return self.click_text(*args)
            return False

        if split_spaces:
            results = [
                t for r in results for t in [(r[0], x, r[2]) for x in r[1].split(" ")]
            ]

        if includes:
            for box, detected_text, confidence in results:
                if text.lower() in detected_text.lower():
                    click_x, click_y = bounding_box_center(box)

                    if click:
                        self.click(click_x, click_y)

                    return (box, detected_text, confidence)

        match, score, index = process.extractOne(
            text.lower(),
            [detected_text.lower() for _, detected_text, _ in results],
            scorer=fuzz.WRatio,
        )

        if score > fuzz_threshold:
            box, detected_text, confidence = results[index]
            # print(detected_text, confidence, score)
            click_x, click_y = bounding_box_center(box)

            if click:
                self.click(click_x, click_y)

            return (box, detected_text, confidence)
        else:
            if retry and not use_cache:
                sleep(1)
                return self.click_text(*args)
            return False

    def clump_ocr(self, text: list, relative_distance=0.05):
        if self.bounds:
            height = self.bounds[3] - self.bounds[1]
        else:
            height = self.height

        text = to_json(text)
        new_text = []
        current_top_left = text[0][0][0]
        current_text = text[0][1]
        last_bottom = text[0][0][2][1] / height
        last_right = text[0][0][1][0]

        for box, detected_text, confidence in text[1:]:
            top = box[0][1] / height
            bottom = box[2][1] / height
            right = box[1][0]

            if top - last_bottom < relative_distance:
                current_text += " " + detected_text
                last_bottom = max(last_bottom, bottom)
                last_right = max(last_right, right)
            else:
                b = [
                    current_top_left,
                    [last_right, current_top_left[1]],
                    [last_right, last_bottom * height],
                    [current_top_left[0], last_bottom * height],
                ]
                new_text.append((b, current_text, confidence))
                current_text = detected_text
                current_top_left = box[0]
                last_bottom = bottom
                last_right = right

        new_text.append(
            (
                [
                    current_top_left,
                    [last_right, current_top_left[1]],
                    [last_right, last_bottom * height],
                    [current_top_left[0], last_bottom * height],
                ],
                current_text,
                confidence,
            )
        )

        return new_text

    def mute(self, set_mute=None):
        try:
            if "volume" not in dir(self):
                from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

                self.volume: Any = None

                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    if session.Process:
                        if self.title in session.Process.name():
                            self.volume = session._ctl.QueryInterface(
                                ISimpleAudioVolume
                            )

            if self.volume:
                if set_mute is not None:
                    self.volume.SetMute(set_mute, None)
                else:
                    self.volume.SetMute(not self.volume.GetMute(), None)
        except Exception as e:
            print(f"Error toggling mute: {e}")

    def close(self):
        if is_windows():
            self.window.close()  # type: ignore
        else:
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'tell application "{self.window}" to quit',
                ]
            )
