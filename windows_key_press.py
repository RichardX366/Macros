import time
import win32gui
import win32con
import win32api
from typing import Union


def press(key: Union[str, int], window: Union[int, str], release_delay: float = 0.05):
    """
    Send a key press to a background window.

    Args:
        key: Either a character (str) or virtual key code (int)
        window: Either window handle (int) or window title (str)
        release_delay: Time in seconds between key down and key up (default 0.05)

    Returns:
        bool: True if successful, False otherwise
    """
    # Convert window title to handle if string provided
    if isinstance(window, str):
        hwnd = win32gui.FindWindow(None, window)
        if not hwnd:
            print(f"Window not found: '{window}'")
            return False
    else:
        hwnd = window

    # Convert character to virtual key code if string provided
    if isinstance(key, str):
        # Handle special keys
        special_keys = {
            "enter": win32con.VK_RETURN,
            "return": win32con.VK_RETURN,
            "tab": win32con.VK_TAB,
            "esc": win32con.VK_ESCAPE,
            "escape": win32con.VK_ESCAPE,
            "space": win32con.VK_SPACE,
            "backspace": win32con.VK_BACK,
            "delete": win32con.VK_DELETE,
            "up": win32con.VK_UP,
            "down": win32con.VK_DOWN,
            "left": win32con.VK_LEFT,
            "right": win32con.VK_RIGHT,
            "home": win32con.VK_HOME,
            "end": win32con.VK_END,
            "pageup": win32con.VK_PRIOR,
            "pagedown": win32con.VK_NEXT,
            "f1": win32con.VK_F1,
            "f2": win32con.VK_F2,
            "f3": win32con.VK_F3,
            "f4": win32con.VK_F4,
            "f5": win32con.VK_F5,
            "f6": win32con.VK_F6,
            "f7": win32con.VK_F7,
            "f8": win32con.VK_F8,
            "f9": win32con.VK_F9,
            "f10": win32con.VK_F10,
            "f11": win32con.VK_F11,
            "f12": win32con.VK_F12,
        }

        if len(key) == 1 and key.isalpha():
            # For letters, use uppercase virtual key code
            vk_code = ord(key.upper())
        elif len(key) == 1 and key.isdigit():
            # For digits, use the digit's virtual key code
            vk_code = ord(key)
        elif key.lower() in special_keys:
            vk_code = special_keys[key.lower()]
        else:
            print(f"Unsupported key: '{key}'")
            return False
    else:
        vk_code = key

    # Get the foreground window to restore later
    foreground_hwnd = win32gui.GetForegroundWindow()

    try:
        # Find the child window that can receive keyboard input
        # This is important for applications with multiple child controls
        child_hwnd = hwnd
        if win32gui.GetClassName(hwnd) not in ["Edit", "RichEdit20W", "Scintilla"]:
            # Try to find a child window that can receive keyboard input
            def enum_child_callback(child, children):
                class_name = win32gui.GetClassName(child)
                if class_name in [
                    "Edit",
                    "RichEdit20W",
                    "Scintilla",
                    "Static",
                    "Button",
                ]:
                    children.append(child)
                return True

            children = []
            win32gui.EnumChildWindows(hwnd, enum_child_callback, children)
            if children:
                # Use the first suitable child window
                child_hwnd = children[0]

        # Post key down message
        win32api.PostMessage(child_hwnd, win32con.WM_KEYDOWN, vk_code, 0)

        # If it's a character, also send WM_CHAR (for text input)
        if isinstance(key, str) and len(key) == 1 and key.isprintable():
            char_code = ord(key)
            win32api.PostMessage(child_hwnd, win32con.WM_CHAR, char_code, 0)

        # Small delay between key down and key up
        time.sleep(release_delay)

        # Post key up message
        win32api.PostMessage(child_hwnd, win32con.WM_KEYUP, vk_code, 0)

        # Restore focus to previous window
        if foreground_hwnd and foreground_hwnd != hwnd:
            win32gui.SetForegroundWindow(foreground_hwnd)

        return True

    except Exception as e:
        print(f"Error sending key press: {e}")
        # Restore focus if something went wrong
        if foreground_hwnd and foreground_hwnd != hwnd:
            win32gui.SetForegroundWindow(foreground_hwnd)
        return False


def press_combination(keys: list, window: Union[int, str], release_delay: float = 0.05):
    """
    Send a key combination (e.g., Ctrl+C) to a background window.

    Args:
        keys: List of keys to press simultaneously (e.g., ['ctrl', 'c'])
        window: Either window handle (int) or window title (str)
        release_delay: Time in seconds between key down and key up
    """
    # Virtual key codes for modifier keys
    modifiers = {
        "ctrl": win32con.VK_CONTROL,
        "control": win32con.VK_CONTROL,
        "shift": win32con.VK_SHIFT,
        "alt": win32con.VK_MENU,
        "win": win32con.VK_LWIN,
        "windows": win32con.VK_LWIN,
    }

    # Convert window title to handle if string provided
    if isinstance(window, str):
        hwnd = win32gui.FindWindow(None, window)
        if not hwnd:
            print(f"Window not found: '{window}'")
            return False
    else:
        hwnd = window

    # Get the foreground window to restore later
    foreground_hwnd = win32gui.GetForegroundWindow()

    try:
        # Find child window for keyboard input
        child_hwnd = hwnd
        if win32gui.GetClassName(hwnd) not in ["Edit", "RichEdit20W", "Scintilla"]:

            def enum_child_callback(child, children):
                class_name = win32gui.GetClassName(child)
                if class_name in ["Edit", "RichEdit20W", "Scintilla"]:
                    children.append(child)
                return True

            children = []
            win32gui.EnumChildWindows(hwnd, enum_child_callback, children)
            if children:
                child_hwnd = children[0]

        # Convert keys to virtual codes
        vk_codes = []
        for key in keys:
            key_lower = key.lower()
            if key_lower in modifiers:
                vk_codes.append(modifiers[key_lower])
            elif len(key) == 1 and key.isalpha():
                vk_codes.append(ord(key.upper()))
            elif len(key) == 1 and key.isdigit():
                vk_codes.append(ord(key))
            else:
                print(f"Unsupported key in combination: '{key}'")
                return False

        # Press all keys down
        for vk_code in vk_codes:
            win32api.PostMessage(child_hwnd, win32con.WM_KEYDOWN, vk_code, 0)

        # Small delay
        time.sleep(release_delay)

        # Release all keys in reverse order
        for vk_code in reversed(vk_codes):
            win32api.PostMessage(child_hwnd, win32con.WM_KEYUP, vk_code, 0)

        # Restore focus
        if foreground_hwnd and foreground_hwnd != hwnd:
            win32gui.SetForegroundWindow(foreground_hwnd)

        return True

    except Exception as e:
        print(f"Error sending key combination: {e}")
        if foreground_hwnd and foreground_hwnd != hwnd:
            win32gui.SetForegroundWindow(foreground_hwnd)
        return False


# Example usage
if __name__ == "__main__":
    # Example 1: Send a single character to Notepad
    # First, make sure Notepad is open
    hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
    if hwnd:
        print("Sending 'Hello' to Notepad...")
        for char in "Hello":
            press(char, hwnd, release_delay=0.02)

    # Example 2: Send using window title
    press("enter", "Untitled - Notepad")

    # Example 3: Send a key combination (Ctrl+A to select all)
    press_combination(["ctrl", "a"], "Untitled - Notepad")

    # Example 4: Send special keys
    press("f5", "MyWindow")  # Refresh (F5)
    press("tab", "MyWindow")  # Tab key
