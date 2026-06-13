from json import dumps, loads

from math import exp
from time import sleep
from typing import cast
from functools import wraps

import cv2
import easyocr
import numpy as np
import pygetwindow as gw
import mss
from PIL import Image, ImageChops
import io
from rapidfuzz import process, fuzz

pre_click_delay_global = 0.0
post_click_delay_global = 0.2


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


def get_dpi(x, y):
    import ctypes

    if not hasattr(ctypes, "windll"):
        return 1.0  # Assume 96 DPI (100% scaling) on non-Windows platforms

    from ctypes import WINFUNCTYPE, byref, c_uint, wintypes, windll, c_int, POINTER

    windll.shcore.SetProcessDpiAwareness(2)

    MONITORENUMPROC = WINFUNCTYPE(
        c_int,
        wintypes.HMONITOR,
        wintypes.HDC,
        POINTER(wintypes.RECT),
        wintypes.LPARAM,
    )

    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        dpi_x = c_uint()
        dpi_y = c_uint()

        windll.shcore.GetDpiForMonitor(
            hMonitor,
            0,
            byref(dpi_x),
            byref(dpi_y),
        )

        rect = lprcMonitor.contents

        monitors.append(
            {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom,
                "dpi": dpi_x.value,
                "scale_percent": dpi_x.value / 96,
            }
        )

        return 1

    def point_in_rect(x, y, rect):
        return rect["left"] <= x < rect["right"] and rect["top"] <= y < rect["bottom"]

    windll.user32.EnumDisplayMonitors(0, 0, MONITORENUMPROC(callback), 0)

    for m in monitors:
        if point_in_rect(x, y, m):
            return m["scale_percent"]

    return 1.0


class WindowHelper:
    def __init__(self, title: str, dpi=0.0):
        self.sct = mss.MSS()

        if dpi == 0.0:
            dpi = get_dpi(self.window.center.x, self.window.center.y)

        self.bounds = None
        self.ocr_cache = None
        self.old_pointer_pos = None
        self.dpi = dpi

        if "getWindowsWithTitle" in dir(gw):
            self.window = gw.getWindowsWithTitle(title)[0]  # type: ignore

            if self.window is None:
                print(f"{title} window not found!")
                raise Exception(f"{title} window not found!")

            self.width = self.window.width * dpi
            self.height = self.window.height * dpi
            self.top = self.window.top
            self.left = self.window.left
        else:
            top, left, width, height = gw.getWindowsGeometry(title)  # type: ignore
            self.width = width * dpi
            self.height = height * dpi
            self.top = top
            self.left = left

        _ = self.screenshot()
        del _

        try:
            self.ocr = easyocr.Reader(["en"], gpu=True)
        except Exception:
            self.ocr = easyocr.Reader(["en"], gpu=False)

    def screenshot(self) -> Image.Image:
        """
        Capture a screenshot of the window and store it in memory.
        Handles per-monitor DPI scaling on multi-monitor setups.

        Returns:
            PIL.Image: The screenshot as a PIL Image object in memory
        """
        try:
            # Get window coordinates and account for DPI scaling
            left = int(self.left)
            top = int(self.top)
            width = int(self.width)
            height = int(self.height)

            # Capture screenshot using mss (efficient method)
            with mss.MSS() as sct:
                monitor = {"top": top, "left": left, "width": width, "height": height}
                sc = sct.grab(monitor)

                # Convert to PIL Image and keep in memory
                image = Image.frombytes("RGB", sc.size, sc.rgb)

                if self.bounds:
                    image = image.crop(self.bounds)

                # download_screenshot(image)

                return image

        except IndexError:
            raise Exception("LimbusCompany window not found!")
        except Exception as e:
            raise Exception(f"Error capturing screenshot: {e}")

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
        self.current_window = gw.getActiveWindow()
        try:
            _focus_window(self.window)
        except Exception as e:
            print(f"Error focusing window: {e}")
            raise

    def restore_previous_window(self):
        if self.current_window is not None:
            try:
                if self.current_window.isMinimized:
                    self.current_window.restore()
                self.current_window.activate()
            except Exception as e:
                print(f"Error restoring previous window: {e}")
                raise

    def to_relative(self, x, y, relative=False):
        if self.bounds:
            if relative:
                x = self.bounds[0] + x * (self.bounds[2] - self.bounds[0]) // self.dpi
                y = self.bounds[1] + y * (self.bounds[3] - self.bounds[1]) // self.dpi
            else:
                x = (self.bounds[0] // self.dpi) + x
                y = (self.bounds[1] // self.dpi) + y
        elif relative:
            x = int(x * self.width / self.dpi)
            y = int(y * self.height / self.dpi)
        return x + self.left, y + self.top

    @clicks
    def click(self, x, y, relative=False, pre_click_delay=0.0, post_click_delay=0.2):
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
        from pyautogui import moveTo, position

        x1, y1 = self.to_relative(x1, y1, relative)
        x2, y2 = self.to_relative(x2, y2, relative)

        self.old_pointer_pos = position()

        drag(
            x1,
            y1,
            x2,
            y2,
            duration,
        )

        if self.old_pointer_pos:
            moveTo(int(self.old_pointer_pos[0]), int(self.old_pointer_pos[1]))
            self.old_pointer_pos = None

    @crops
    def read_screen(
        self,
        confidence_threshold=0.2,
        use_cache=False,
        top=0.0,
        left=0.0,
        width=0.0,
        height=0.0,
    ):
        if use_cache and self.ocr_cache is not None:
            return self.ocr_cache

        img = cv2.cvtColor(np.array(self.screenshot()), cv2.COLOR_RGB2BGR)
        results = self.ocr.readtext(image=img)
        results = [
            (
                [[cast(int, x) // self.dpi, cast(int, y) // self.dpi] for x, y in box],
                detected_text,
                confidence,
            )
            for box, detected_text, confidence in results
            if cast(float, confidence) > confidence_threshold
        ]
        results.sort(key=lambda x: x[0][0][1])  # Sort by y-coordinate (top to bottom)

        self.ocr_cache = results

        return results

    @crops
    @clicks
    def click_text(
        self,
        text,
        confidence_threshold=0.2,
        fuzz_threshold=80,
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

        results = self.read_screen(confidence_threshold, use_cache)

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
            height = self.height // self.dpi

        text = loads(dumps(convert(text)))
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


def convert(obj):
    if (
        isinstance(obj, np.ndarray)
        or isinstance(obj, np.integer)
        or isinstance(obj, np.floating)
    ):
        return obj.tolist()
    elif isinstance(obj, list):
        return [convert(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple(convert(x) for x in obj)
    elif isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
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


def _focus_window(window):
    # Attempt to bring the window to front using pygetwindow APIs.
    try:
        if window.isMinimized:
            window.restore()
        # activate should bring to foreground on most systems
        window.activate()
    except Exception:
        # best-effort; ignore failures
        pass


def drag(x1, y1, x2, y2, duration=0.5):
    from pyautogui import moveTo, mouseDown, mouseUp

    # Use pyautogui to perform a smooth drag
    moveTo(int(x1), int(y1))
    sleep(0.5)
    mouseDown()
    # dragTo will move the cursor to the target over duration
    moveTo(int(x2), int(y2), duration=duration)
    mouseUp()
    sleep(0.1)
