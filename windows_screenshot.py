import ctypes
import win32gui
import win32ui
from PIL import Image

PW_RENDERFULLCONTENT = 0x00000002

user32 = ctypes.windll.user32
user32.PrintWindow.argtypes = [
    ctypes.c_void_p,  # HWND
    ctypes.c_void_p,  # HDC
    ctypes.c_uint,  # flags
]
user32.PrintWindow.restype = ctypes.c_bool


def windows_screenshot(hwnd: int):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        raise RuntimeError(f"Invalid window size: {width} x {height}")

    window_dc = win32gui.GetWindowDC(hwnd)

    if window_dc == 0:
        raise RuntimeError("Could not get the window device context.")

    source_dc = win32ui.CreateDCFromHandle(window_dc)
    memory_dc = source_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(source_dc, width, height)

    previous_bitmap = memory_dc.SelectObject(bitmap)

    try:
        success = user32.PrintWindow(
            ctypes.c_void_p(hwnd),
            ctypes.c_void_p(memory_dc.GetSafeHdc()),
            PW_RENDERFULLCONTENT,
        )

        if not success:
            raise RuntimeError("PrintWindow failed.")

        bitmap_info = bitmap.GetInfo()
        bitmap_data = bitmap.GetBitmapBits(True)

        image = Image.frombuffer(
            "RGB",
            (bitmap_info["bmWidth"], bitmap_info["bmHeight"]),
            bitmap_data,
            "raw",
            "BGRX",
            0,
            1,
        )

        return image

    finally:
        memory_dc.SelectObject(previous_bitmap)
        win32gui.DeleteObject(bitmap.GetHandle())
        memory_dc.DeleteDC()
        source_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, window_dc)
