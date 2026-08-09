from argparse import ArgumentParser
import re
from time import sleep
import time
from typing import cast

from PIL import Image
import cv2
import numpy as np

from helpers import (
    WindowHelper,
    bounding_box_center,
    kill_keybind,
    pause_keybind,
    download_screenshot,
)

try:
    wh = WindowHelper("LimbusCompany")
except:
    wh = WindowHelper("iPhone Mirroring")


floor_complete = False
last_floor = 0

easy = False

packs = [
    ["Chicke"],
    ["Hatred"],
    ["Line 2"],
    ["Line 4", "Line 1", "Line 3", "District"],
]
difficulties = [True, True, True, True]

easy_packs = [
    ["Chicke"],
    ["Hatred"],
    ["Line 2"],
    ["Line 4", "Line 1", "Line 3", "District"],
]
easy_difficulties = [False, False, True, True]

poise_gifts = [
    "spiderweb",
    "clear",
    "tomb",
    "commemorative",
    "ragged bamboo",
    "lucky",
    "cask",
    "finifugality",
    "endorphin",
    "clover",
    "reminiscence",
    "broken blade",
    "ebulizer",
    "old wooden",
    "cigarette",
    "recollection",
    "angel",
    "emerald",
    "sack",
    "share",
    "pom",
    "ornamental",
    "pendant",
]
enhance_costs = (0, 150, 180, 225, 300)
enhanceable = ["clear", "tomb", "ebulizer", "emerald"]
currently_enhanced = set()
recipes = [
    [3, 3, 2],  # 4
    [4, 2, 2],  # 4
    [4, 3, 1],  # 4
    [4, 3, 2],  # 4
    [2, 2, 2],  # 3
    [2, 1, 1],  # 2
]
unit_distance = 0.0
killed_teammates = False
ego_gifts = []
require_gift_calibration = False

# Helpers


def in_room_selection():
    text = wh.read_screen(left=0.7, height=0.2, width=0.2, brightness=0.3)
    if len([t[1] for t in text if re.sub(r"\D", "", t[1]).isnumeric()]) >= 2:
        text = wh.read_screen(
            left=0.3, height=0.2, width=0.4, confidence_threshold=0.0, brightness=0.3
        )
        flat = []
        for t in text:
            flat += t[1].split(" ")
        if len([t for t in flat if re.sub(r"\D", "", t).isnumeric()]) >= 4:
            return True
    return False


def handle_gift():
    if wh.click_text(
        "Select Encounter Reward Card",
        top=0.1,
        left=0.1,
        width=0.6,
        height=0.2,
        click=False,
        retry=False,
    ):
        print("Reward Card")
        sleep(0.5)
        if wh.click_text(
            "Gain",
            top=0.5,
            left=0.1,
            width=0.8,
            height=0.2,
            includes=True,
            retry=False,
        ) or wh.click_text(
            "Resource",
            top=0.5,
            left=0.1,
            width=0.8,
            height=0.2,
            includes=True,
            use_cache=True,
            retry=False,
        ):
            confirm()
            sleep(1)
            accept_gift(True)
            sleep(5)

    text = wh.read_screen(top=0.2, left=0.1, width=0.8, height=0.1)
    acquires = [t for t in text if "Acquire" in t[1] and "Gift" in t[1]]
    if acquires:
        gifts = []
        current_gift = {"owned": False, "name": "", "box": ()}
        for t in sorted(text, key=lambda x: x[0][1][0]):
            if "Owned" in t[1]:
                current_gift["owned"] = True
            elif "Acquire" in t[1] and "Gift" in t[1]:
                current_gift["box"] = t[0]
                gifts.append(current_gift)
                current_gift = {"owned": False, "name": "", "box": ()}
            else:
                current_gift["name"] = t[1] + " "
        gift_levels = get_gift_levels(height=0.5)

        def get_level(gift: dict):
            return get_gift_level(
                gift["box"][3],
                [l for l in gift_levels if l["x"] < gift["box"][0][0]],
                up=False,
            )

        gifts.sort(
            key=lambda x: (
                9999 - get_level(x)
                if x["owned"]
                else (
                    min(
                        (
                            i
                            for i, gift in enumerate(poise_gifts)
                            if gift in x["name"].lower()
                        ),
                        default=999 - get_level(x),
                    )
                )
            )
        )
        print([g["name"] for g in gifts])
        sleep(0.5)
        wh.click(*bounding_box_center(gifts[0]["box"]))
        sleep(0.5)
        if len(acquires) > 3:
            wh.click(*bounding_box_center(gifts[1]["box"]))
            sleep(0.5)
        wh.click_text("Select", top=0.7, left=0.8, height=0.2, includes=True)
        accept_gift()
        if len(acquires) > 3:
            accept_gift()
        sleep(3)

    if wh.click_text(
        "Victory",
        top=0.1,
        left=0.7,
        height=0.2,
        click=False,
        retry=False,
    ):
        print("Dungeon Complete")
        return "Dungeon Complete"


def roll_for_pack(packs: list[str], hard: bool = False):
    wh.click_text(
        "NORMAL" if hard else "HARD", left=0.6, height=0.2, width=0.2, retry=False
    )

    print("Rolling for packs:", packs)

    sleep(3)
    for _ in range(4):
        read_packs = wh.read_screen(top=0.5, left=0.1, width=0.8, height=0.2)
        print("Found packs:", [t[1] for t in read_packs])
        if any(pack in t[1] for t in read_packs for pack in packs):
            break
        if _ == 3:
            from pyautogui import mouseUp, position, moveTo

            wh.click(0.15, 0.1, relative=True)
            wh.click(0.21, 0.3, relative=True)
            sleep(1)
            wh.read_screen(top=0.4, left=0.45, height=0.2)
            while not any(
                wh.click_text(
                    pack,
                    top=0.4,
                    left=0.45,
                    height=0.2,
                    includes=True,
                    retry=False,
                    use_cache=True,
                )
                for pack in packs
            ):
                print("Found packs:", [t[1] for t in cast(list, wh.ocr_cache)])
                x, y = position()
                wh.drag(0.5, 0.7, 0.5, 0.35, relative=True, release=False)
                sleep(0.2)
                mouseUp()
                moveTo(x, y)
                wh.read_screen(top=0.45, left=0.45, height=0.2)
            sleep(0.5)
            wh.click(0.6, 0.8, relative=True)
            sleep(0.5)
            confirm()
        else:
            wh.click(0.85, 0.1, relative=True)
        sleep(3)

    box = [[0]]
    wh.read_screen(top=0.5, left=0.1, width=0.8, height=0.2)
    for pack in packs:
        result = wh.click_text(
            pack,
            top=0.5,
            left=0.1,
            width=0.8,
            height=0.2,
            includes=True,
            click=False,
            use_cache=True,
            retry=False,
        )
        if result:
            box, _, _ = result
            break
    x, y = bounding_box_center(box)
    wh.drag(x, 0.4 * wh.height, x, 0.8 * wh.height)
    sleep(1)


def kill_teammates():
    text = wh.read_screen(top=0.93, height=0.05)
    text = [t for t in text if len(re.sub(r"\D", "", t[1])) > 2]
    while len(text) == 0:
        text = wh.read_screen(top=0.93, height=0.05)
        text = [t for t in text if len(re.sub(r"\D", "", t[1])) > 2]
        sleep(1)

    while len(text) != 1:
        defense()
        sleep(3)
        text = wh.read_screen(top=0.93, height=0.05)
        text = [t for t in text if len(re.sub(r"\D", "", t[1])) > 2]
        while len(text) == 0:
            text = wh.read_screen(top=0.93, height=0.05)
            text = [t for t in text if len(re.sub(r"\D", "", t[1])) > 2]
            if in_room_selection():
                return
            sleep(1)
    print("Everyone dead")
    global killed_teammates
    killed_teammates = True


def defense():
    text = wh.read_screen(top=0.93, height=0.05)
    text = [t for t in text if len(re.sub(r"\D", "", t[1])) > 2]
    text.sort(key=lambda t: t[0][0][0])

    global unit_distance
    if unit_distance == 0.0:
        unit_distance = text[1][0][0][0] - text[0][0][0][0]

    damage = wh.click_text("Damage", top=0.75, left=0.5, height=0.1, click=False)
    if not damage:
        return
    end_x = damage[0][3][0] - 0.04 * wh.width
    end_y = damage[0][3][1] + 0.03 * wh.height

    last_unit = damage[0][0][0] - 0.1 * wh.width

    units = (last_unit - text[0][0][0][0]) / unit_distance + 1
    for i in range(round(units)):
        wh.click(
            last_unit - i * unit_distance,
            text[0][0][0][1],
            pre_click_delay=0.0,
            post_click_delay=0.0,
        )

    combat_x = text[0][0][2][0] - 0.05 * wh.width
    combat_y = text[0][0][2][1] - 0.2 * wh.height

    from pyautogui import position, moveTo

    x, y = position()

    wh.drag(
        combat_x,
        combat_y,
        text[0][0][2][0],
        text[0][0][2][1],
        release=False,
        duration=0.1,
    )
    wh.drag(
        text[0][0][2][0],
        text[0][0][2][1],
        last_unit + 0.02 * wh.width,
        text[0][0][2][1],
        release=False,
        duration=0.2,
    )
    wh.drag(last_unit + 0.02 * wh.width, text[0][0][2][1], end_x, end_y, duration=0.1)

    moveTo(x, y)

    return text


def bounding_distance(box1, box2):
    p1 = bounding_box_center(box1)
    p2 = bounding_box_center(box2)
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def index_to_gift_coord(index: int):
    x_diff = 0.08
    y_diff = 0.14
    row = index // 5
    col = index % 5
    x = 0.52 + col * x_diff
    y = 0.4 + row * y_diff
    return x, y


def get_gift_levels(color=(0xF7, 0xC1, 0x00), top=0.0, left=0.0, width=0.0, height=0.0):
    arr = np.array(
        wh.screenshot(top=top, left=left, width=width, height=height).convert("RGB")
    )
    binary = (np.all(abs(arr - color) < 20, axis=2) * 255).astype(np.uint8)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blobs = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        if area < 20:
            continue

        crop = binary[y : y + h, x : x + w]
        white = np.count_nonzero(crop)
        white_ratio = white / crop.size
        if white_ratio < 0.3:
            continue

        if h / w < 1.5:
            continue

        blobs.append(
            {
                "x": int(x + left * wh.width),
                "y": int(y + top * wh.height),
                "width": w,
                "height": h,
                "text": "i" if h / w > 5 else "v",
                "center": (
                    int(x + left * wh.width + w / 2),
                    int(y + top * wh.height + h / 2),
                ),
            }
        )

    def merge_blobs(blobs):
        blobs = sorted(blobs, key=lambda b: b["center"][0])
        while True:
            merged = False
            for i, blob in enumerate(blobs):
                for other_blob in blobs[i + 1 :]:
                    w = max(blob["width"], other_blob["width"])
                    h = max(blob["height"], other_blob["height"])
                    dx = abs(blob["center"][0] - other_blob["center"][0])
                    dy = abs(blob["center"][1] - other_blob["center"][1])
                    if dx < 3 * w and dy < 2 * h:
                        merged = True
                        blob["x"] = min(blob["x"], other_blob["x"])
                        blob["y"] = min(blob["y"], other_blob["y"])
                        blob["width"] = int(
                            max(
                                blob["x"] + blob["width"],
                                other_blob["x"] + other_blob["width"],
                            )
                            - blob["x"]
                        )
                        blob["height"] = int(
                            max(
                                blob["y"] + blob["height"],
                                other_blob["y"] + other_blob["height"],
                            )
                            - blob["y"]
                        )
                        blob["center"] = (
                            int(blob["x"] + blob["width"] / 2),
                            int(blob["y"] + blob["height"] / 2),
                        )
                        blob["text"] += other_blob["text"]
                        blobs.remove(other_blob)
                        break
                if merged:
                    break
            if not merged:
                break

        return blobs

    merged = merge_blobs(blobs)

    numbers = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8}
    for blob in merged:
        blob["text"] = numbers.get(blob["text"], 0)

    # output = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    # for blob in merged:
    #     cv2.rectangle(
    #         output,
    #         (blob["x"] - int(left * wh.width), blob["y"] - int(top * wh.height)),
    #         (
    #             blob["x"] - int(left * wh.width) + blob["width"],
    #             blob["y"] - int(top * wh.height) + blob["height"],
    #         ),
    #         (0, 0, 255),
    #         1,
    #     )
    # download_screenshot(Image.fromarray(output))

    return merged


def get_gift_level(
    index: int | tuple[float, float], blobs: list[dict], up=True, left=True
):
    if isinstance(index, int):
        coords = index_to_gift_coord(index)
        x = coords[0] * wh.width
        y = coords[1] * wh.height
    else:
        x, y = index
    fit = [
        b
        for b in blobs
        if (b["x"] < x if left else b["x"] > x) and (b["y"] < y if up else b["y"] > y)
    ]
    fit.sort(key=lambda b: abs(x - b["x"]) + abs(y - b["y"]))
    return fit[0]["text"] if fit else 0


def scroll_gift(gift_index: int = 5, down=True):
    if gift_index < 5:
        return
    from pyautogui import mouseUp, position, moveTo

    i = gift_index // 5

    x, y = position()
    scroll_from = index_to_gift_coord(10) if down else index_to_gift_coord(0)
    scroll_to = index_to_gift_coord(10 - 5 * i) if down else index_to_gift_coord(5 * i)
    wh.drag(
        *scroll_from,
        *scroll_to,
        relative=True,
        release=False,
    )
    sleep(0.2)
    mouseUp()
    moveTo(x, y)


def click_gift(index: int, scroll_back=True):
    diff = 0
    if index >= 15:
        diff = (index - 10) // 5 * 5
        scroll_gift(diff)
    wh.click(*index_to_gift_coord(index - diff), relative=True)
    if index >= 15 and scroll_back:
        scroll_gift(diff, down=False)
    return diff


def update_gift_list():
    global ego_gifts
    wh.click_text("Enhance", top=0.5, left=0.1, width=0.1, height=0.1)
    sleep(0.5)
    wh.click_text("By Tier", top=0.15, left=0.75, width=0.15, height=0.15)
    wh.click_text("Recent", top=0.3, left=0.8, width=0.1, height=0.1)
    blobs = get_gift_levels(top=0.3, left=0.5)
    ego_gifts = []

    def scroll_signature():
        nonlocal blobs
        blobs = get_gift_levels(top=0.3, left=0.5)
        return " ".join([str(get_gift_level(i, blobs)) for i in range(len(blobs))])

    def is_more():
        if len(blobs) % 5 != 0 or len(blobs) < 15:
            return False
        old = " ".join([str(get_gift_level(i, blobs)) for i in range(len(blobs))])
        scroll_gift()
        return scroll_signature() != old

    def add_gift(i):
        wh.click(
            *index_to_gift_coord(i),
            relative=True,
            pre_click_delay=0.0,
            post_click_delay=0.0,
        )
        text = wh.read_screen(
            top=0.2, left=0.2, width=0.25, height=0.2, brightness=0.7, saturation=-0.5
        )
        name = " ".join([t[1] for t in text])
        gift = {
            "name": name,
            "level": get_gift_level(i, blobs),
        }
        ego_gifts.append(gift)

    for i in range(len(blobs)):
        add_gift(i)

    scrolls = 0

    while is_more():
        scrolls += 5
        extras = len(blobs) - 10
        for i in range(extras):
            add_gift(i + 10)
        if extras < 5:
            break

    scroll_gift(scrolls, False)

    wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)


def power_up_gift(index: int):
    wh.click_text("Enhance", top=0.5, left=0.1, width=0.1, height=0.1)
    sleep(0.5)
    wh.click_text("By Tier", top=0.15, left=0.75, width=0.15, height=0.15)
    wh.click_text("Recent", top=0.3, left=0.8, width=0.1, height=0.1)
    wh.click(*index_to_gift_coord(index), relative=True)
    wh.click_text("Power", top=0.7, left=0.5, width=0.2, height=0.2, includes=True)
    sleep(0.5)
    wh.click(0.8, 0.72, relative=True)
    confirm()
    wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)


def accept_gift(optional=False):
    hit = confirm(optional, mode="center", click=False)
    if not hit:
        return False
    box, text, confidence = hit

    def read_name():
        text = wh.read_screen(
            top=0.55,
            left=0.25,
            width=0.15,
            height=0.15,
            brightness=0.7,
            saturation=-0.5,
        )
        name = " ".join([t[1] for t in text])
        return name

    name = read_name()
    if not name:
        print("No gift name found")
        return False
    blobs = get_gift_levels(top=0.3, left=0.25, width=0.1, height=0.2)
    ego_gifts.append({"name": name, "level": blobs[0]["text"] if blobs else 1})
    if len(name) < 5:
        print("Short name", name)
    wh.click(*bounding_box_center(box))
    if read_name() == name:
        wh.click(*bounding_box_center(box))
    print("Accepting gift:", f"{name} ({ego_gifts[-1]["level"]})")
    return True


def confirm(optional=False, use_cache=False, click=True, mode=""):
    return wh.click_text(
        "Confirm",
        top=0.6,
        left=0.5 if mode == "right" else 0.4,
        width=0.2 if mode == "right" or mode == "center" else 0.3,
        height=0.3,
        retry=not optional,
        use_cache=use_cache,
        click=click,
    )


question_room_icon = cast(
    np.ndarray, cv2.imread("limbus/fast_mirror/question.png", cv2.IMREAD_GRAYSCALE)
)


# Overarching functions


def enter():
    wh.click_text("Drive", top=0.8, left=0.7, width=0.2)
    wh.click_text("Mirror", top=0.3, left=0.2, width=0.3, height=0.3, split_spaces=True)
    sleep(0.5)
    while not wh.click_text("Enter", top=0.6, left=0.5, width=0.2, retry=False):
        wh.click_text("Enter", top=0.6, left=0.7)
    wh.click_text("Confirm", top=0.6, left=0.7)
    wh.click_text(
        "Beginning",
        top=0.2,
        left=0.1,
        width=0.2,
        height=0.1,
        includes=True,
        click=False,
    )
    sleep(1)
    wh.click_text(
        "Beginning",
        top=0.2,
        left=0.1,
        width=0.2,
        height=0.1,
        includes=True,
    )
    wh.click(0.5, 0.3, relative=True)  # Interstellar Travel
    wh.click(0.9, 0.9, relative=True)  # Enter
    confirm()
    wh.click_text("Poise", top=0.5, left=0.25, width=0.1, height=0.1)
    wh.click_text("Stone Tomb", top=0.4, left=0.6, width=0.2, height=0.2)
    wh.click(0.8, 0.8, relative=True)
    accept_gift()
    wh.click_text("Keyword", top=0.2, left=0.45, width=0.1, height=0.1, includes=True)
    sleep(0.5)
    wh.click(0.55, 0.8, relative=True)
    wh.click(0.85, 0.8, relative=True)
    confirm()
    accept_gift()
    wh.click_text(
        "SELECT", top=0.1, left=0.3, width=0.4, height=0.2, click=False, includes=True
    )
    roll_for_pack(["Gamblers"], not easy)


def advantage_check():
    from pyautogui import position, moveTo

    order = ["Very High", "High", "Norma", "Low", "Very Low", "select"]
    text = wh.read_screen(top=0.8, width=0.8, height=0.1)
    text.sort(key=lambda t: t[0][0][0])
    text = [t for t in text if any(o in t[1] for o in order)]
    left = text[0][0][0][0]
    right = text[-1][0][1][0]
    advantages = []
    for _, t, _ in text:
        indices = [(t.find(o) if t.find(o) >= 0 else 999) for o in order]
        min_index = indices.index(min(indices))
        while min(indices) < 999:
            advantages.append(order[min_index])
            t = t.replace(order[min_index], "", 1)
            indices = [(t.find(o) if t.find(o) >= 0 else 999) for o in order]
            min_index = indices.index(min(indices))
    step = (right - left) / (len(advantages))
    left += step / 2

    for o in order:
        if o in advantages:
            x = left + step * advantages.index(o)
            y = text[0][0][1][1] + 0.02 * wh.height
            wh.click(x, y)
            sleep(0.5)
            while not wh.click_text("Commence", top=0.8, left=0.8, retry=False):
                wh.click(x, y)
                sleep(0.5)

            wh.click_text(
                "Check",
                fuzz_threshold=40,
                top=0.6,
                left=0.6,
                width=0.3,
                height=0.2,
                split_spaces=True,
            )
            while not wh.click_text(
                "Continue", top=0.8, left=0.8, click=False, retry=False
            ) and not wh.click_text(
                "Proceed", top=0.8, left=0.8, click=False, retry=False, use_cache=True
            ):
                wh.click_text(
                    "SKIP",
                    top=0.8,
                    left=0.8,
                    use_cache=True,
                    retry=False,
                    pre_click_delay=0.0,
                    post_click_delay=0.0,
                )
                x, y = position()
                for _ in range(5):
                    wh.click(
                        0.1,
                        0.5,
                        relative=True,
                        restore_position=False,
                        pre_click_delay=0.0,
                        post_click_delay=0.01,
                    )
                moveTo(x, y)

            sleep(1)
            return


def handle_shop():
    global last_floor, killed_teammates

    def get_balance(iter=0):
        balance_text = wh.read_screen(top=0.1, left=0.4, width=0.2, height=0.2)
        balance = [
            t[1].replace(",", "").replace("G", "6")
            for t in balance_text
            if t[1].replace(",", "").replace("G", "6").isnumeric()
        ]
        if not balance and iter < 3:
            sleep(0.5)
            return get_balance(iter + 1)
        return int(balance[0]) if balance else 0

    if get_balance() >= 100:
        wh.click_text("Heal", top=0.5, width=0.3, height=0.3)
        wh.click_text(
            "All Sinners heal 20% HP and 15 SP",
            top=0.3,
            left=0.6,
            height=0.3,
            width=0.3,
        )
        sleep(0.5)
        wh.click_text("Leave", top=0.8, left=0.8, retry=False)
        wh.click_text("Return", top=0.8, left=0.8, retry=False, use_cache=True)

    text = wh.read_screen(top=0.3, left=0.4, width=0.5, height=0.5)

    def is_purchased(t):
        x, y = bounding_box_center(t[0])
        purchased = [
            t
            for t in text
            if t[0][0][0] > x - 0.1 * wh.width
            and t[0][1][0] < x + 0.1 * wh.width
            and t[0][0][1] > y - 0.2 * wh.height
            and t[0][2][1] < y - 0.1 * wh.height
            and "Purchased" in t[1]
        ]
        return bool(purchased)

    def replace_skill(balance: int):
        replace_skills = [t for t in text if "Ryoshu" in t[1] or "Skill Search" in t[1]]
        print(f"Replacements: {[t[1] for t in text if "Replace" in t[1]]}")
        for replace in replace_skills:
            if is_purchased(replace) or balance < 45:
                continue

            x, y = bounding_box_center(replace[0])
            wh.click(x, y - 0.06 * wh.height)
            sleep(0.5)

            if "Skill Search" in replace[1]:
                wh.click(0.25, 0.9, relative=True)
                sleep(0.5)

            wh.click_text(
                "moderate",
                top=0.2,
                left=0.1,
                width=0.8,
                height=0.2,
                includes=True,
                pre_click_delay=0.0,
                post_click_delay=0.0,
            )
            wh.click_text(
                "large",
                top=0.2,
                left=0.1,
                width=0.8,
                height=0.2,
                includes=True,
                use_cache=True,
                pre_click_delay=0.0,
                post_click_delay=0.0,
            )
            wh.click_text(
                "tremendous",
                top=0.2,
                left=0.1,
                width=0.8,
                height=0.2,
                includes=True,
                use_cache=True,
                pre_click_delay=0.0,
                post_click_delay=0.0,
            )
            confirm()
            confirm(use_cache=True)
            sleep(0.5)
        return balance

    def get_items():
        nonlocal text
        text = wh.read_screen(top=0.3, left=0.4, width=0.5, height=0.5)
        blobs = get_gift_levels(top=0.3, left=0.4, width=0.5, height=0.5)
        items = []
        for t in text:
            if t[1].isnumeric():
                if is_purchased(t):
                    continue
                label = sorted(text, key=lambda x: bounding_distance(t[0], x[0]))[1][1]
                if not any(g in label.lower() for g in poise_gifts):
                    continue
                item = {
                    "box": t[0],
                    "cost": t[1],
                    "name": label,
                    "level": get_gift_level(t[0][0], blobs),
                }
                items.append(item)
        items.sort(key=lambda x: x["box"][0][1])
        rows = [[]]
        for item in items:
            if (
                rows[-1]
                and rows[-1][-1]["box"][0][1] + 0.1 * wh.height < item["box"][0][1]
            ):
                rows.append([])
            rows[-1].append(item)
        for row in rows:
            row.sort(key=lambda x: x["box"][0][0])
        return [item for row in rows for item in row]

    def purchase(item):
        x, y = bounding_box_center(item["box"])
        wh.click(x, y - 0.06 * wh.height)
        sleep(1)
        wh.click_text("Purchase", top=0.6, left=0.5, width=0.2, height=0.3, retry=False)
        sleep(1)
        accept_gift(True)
        sleep(0.5)

    def enhance(balance: int):
        to_enhance = [
            g
            for g in ego_gifts
            if any(
                e in g["name"].lower() and e not in currently_enhanced
                for e in enhanceable
            )
        ]
        if to_enhance:
            costs = [enhance_costs[g["level"]] for g in to_enhance]
            for cost, gift in zip(costs, to_enhance):
                if cost <= balance:
                    print(
                        "Enhancing:",
                        gift["name"],
                        "Level:",
                        gift["level"],
                        "Cost:",
                        cost,
                    )
                    sorted_gifts = [
                        g for g in ego_gifts if " Vestige" not in g["name"]
                    ] + [g for g in ego_gifts if " Vestige" in g["name"]]
                    power_up_gift(sorted_gifts.index(gift))
                    currently_enhanced.add(
                        [name for name in enhanceable if name in gift["name"].lower()][
                            0
                        ]
                    )
                    balance -= cost
        return balance

    def buy_items():
        sleep(0.5)
        items = get_items()
        balance = get_balance()

        balance = replace_skill(balance)
        balance = enhance(balance)

        order = sorted(
            items,
            key=lambda x: [
                i for i, g in enumerate(poise_gifts) if g in x["name"].lower()
            ][0],
        )
        for item in order:
            if int(item["cost"]) <= balance:
                purchase(item)
                last_box = items[-1]["box"]
                index = items.index(item)
                for i in range(len(items) - 1, index, -1):
                    items[i]["box"] = items[i - 1]["box"]
                item["box"] = last_box
                items.remove(item)
                items.append(item)
                balance = get_balance()

    global require_gift_calibration
    if require_gift_calibration:
        update_gift_list()
        require_gift_calibration = False

    def fusion_menu(type="POISE"):
        wh.click_text("Fuse", top=0.5, left=0.2, width=0.1, height=0.1)
        sleep(0.5)
        wh.click_text("By Tier", top=0.15, left=0.75, width=0.15, height=0.15)
        wh.click_text("Recent", top=0.3, left=0.8, width=0.1, height=0.1)
        wh.click(0.5, 0.3, relative=True)
        wh.click_text(type, top=0.6, left=0.2, width=0.1, height=0.1)
        confirm()
        sleep(0.5)

    def fuse(gifts: list[dict]):
        sorted_gifts = [g for g in ego_gifts if " Vestige" in g["name"]] + [
            g for g in ego_gifts if " Vestige" not in g["name"]
        ]
        gifts.sort(key=lambda g: sorted_gifts.index(g))
        diff = 0
        for gift in gifts:
            diff += click_gift(sorted_gifts.index(gift) - diff, scroll_back=False)
            ego_gifts.remove(gift)
        scroll_gift(diff, down=False)
        wh.click(0.1, 0.5, relative=True)
        wh.click_text("Fuse", top=0.8, left=0.6, width=0.1, height=0.1)
        sleep(0.5)
        wh.click_text("Fuse", top=0.8, left=0.6, width=0.1, height=0.1, use_cache=True)
        sleep(0.5)
        print(
            "Fusing gifts:",
            [f"{g["name"]} ({g["level"]})" for g in gifts],
        )
        accept_gift()
        sleep(0.5)
        fuse_specials()

    def to_fuse():
        excess_gifts = [
            g for g in ego_gifts if not any(p in g["name"].lower() for p in poise_gifts)
        ]
        # Remove level 4 reforging if we already have Clear
        if any("clear" in g["name"].lower() for g in ego_gifts):
            excess_gifts = [g for g in excess_gifts if g["level"] < 4]

        breakdown = [[], [], [], [], [], []]
        for g in excess_gifts:
            breakdown[g["level"]].append(g)

        for recipe in recipes:
            counts = [len(count) for count in breakdown]
            for level in recipe:
                counts[level] -= 1
            if any(c < 0 for c in counts):
                continue
            return [breakdown[level].pop() for level in recipe]
        return []

    def fuse_specials():
        def fusion_available():
            text = wh.read_screen(
                top=0.25,
                left=0.45,
                width=0.2,
                height=0.1,
                brightness=0.7,
                saturation=-0.5,
            )
            return any("Fusion" in t[1] for t in text)

        fused = False

        while fusion_available():
            for i in range(5):
                wh.click(
                    *index_to_gift_coord(i),
                    relative=True,
                    pre_click_delay=0.0,
                    post_click_delay=0.0,
                )
            wh.click_text("Fuse", top=0.8, left=0.6, width=0.1, height=0.1)
            sleep(0.5)
            wh.click_text(
                "Fuse", top=0.8, left=0.6, width=0.1, height=0.1, use_cache=True
            )
            sleep(0.5)
            accept_gift()
            sleep(0.5)
            fused = True

        if fused:
            wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)
            sleep(0.5)
            update_gift_list()
            fusion_menu()

    if to_fuse():
        fusion_menu()
        fuse_specials()
        while gifts := to_fuse():
            fuse(gifts)
        wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)

    buy_items()
    if get_balance() >= 45:
        wh.click_text("Refresh", top=0.1, left=0.75, width=0.1, height=0.1)
        buy_items()

        while get_balance() >= 400:
            wh.click_text("Keyword", top=0.1, left=0.85, width=0.1, height=0.1)
            wh.click_text("POISE", top=0.6, left=0.2, width=0.1, height=0.1)
            wh.click_text("Refresh", top=0.75, left=0.5, width=0.2, height=0.1)
            buy_items()

    wh.click_text("Leave", top=0.8, left=0.8)
    confirm()
    sleep(1)
    while not wh.click_text(
        "Enter", top=0.65, left=0.8, height=0.2, retry=False, click=False
    ):
        wh.press("d")
        sleep(1)
    wh.press("enter")
    sleep(1.0)
    if last_floor == 3 or last_floor == 4:
        wh.click(0.4, 0.3, relative=True)
    result = fight()
    if result == "Dungeon Complete":
        global floor_complete
        floor_complete = True
        return result

    if easy:
        roll_for_pack(easy_packs[last_floor], easy_difficulties[last_floor])
    else:
        roll_for_pack(packs[last_floor], difficulties[last_floor])
    last_floor += 1
    sleep(3)
    floor_complete = True


def question():
    from pyautogui import position, moveTo

    sleep(1.5)
    if wh.click_text(
        "Shop",
        top=0.1,
        left=0.1,
        width=0.2,
        height=0.2,
        click=False,
        retry=False,
        includes=True,
    ):
        return handle_shop()
    if wh.click_text(
        "To Battle",
        top=0.75,
        left=0.8,
        height=0.2,
        click=False,
        retry=False,
        includes=True,
    ):
        return fight()

    battle_flag = False
    while True:
        wh.click_text(
            "Skip",
            top=0.8,
            left=0.8,
            retry=False,
            pre_click_delay=0.0,
            post_click_delay=0.0,
        )
        wh.click_text(
            "Proceed",
            top=0.8,
            left=0.8,
            use_cache=True,
            retry=False,
            pre_click_delay=0.0,
            post_click_delay=0.0,
        )
        x, y = position()
        for _ in range(5):
            wh.click(
                0.1,
                0.5,
                relative=True,
                restore_position=False,
                pre_click_delay=0.0,
                post_click_delay=0.01,
            )
        moveTo(x, y)
        if wh.click_text("Continue", top=0.8, left=0.8, use_cache=True, retry=False):
            sleep(2)
            if battle_flag:
                fight()
                sleep(0.5)
            sleep(0.5)
            return

        if wh.click_text("Choices", click=False, left=0.5, height=0.8, retry=False):
            text = wh.read_screen(left=0.5, height=0.8, use_cache=True)
            text.pop(0)
            text = wh.clump_ocr(text)

            without_cursed = [t for t in text if not "cursed" in t[1].lower()]
            if not without_cursed:
                x, y = bounding_box_center(text[0][0])
                wh.click(x, y)
                continue

            without_battle = [t for t in without_cursed if not "battle" in t[1].lower()]
            if not without_battle:
                x, y = bounding_box_center(without_cursed[0][0])
                wh.click(x, y)
                battle_flag = True
                continue

            wh.ocr_cache = without_battle

            if not wh.click_text(
                "level up",
                use_cache=True,
                includes=True,
                left=0.5,
                height=0.8,
                retry=False,
            ):
                if not wh.click_text(
                    "gain a",
                    use_cache=True,
                    includes=True,
                    left=0.5,
                    height=0.8,
                    retry=False,
                ):
                    x, y = bounding_box_center(without_battle[0][0])
                    wh.click(x, y)
            # sleep(0.1)

        if wh.click_text(
            "Advantage",
            top=0.1,
            left=0.7,
            height=0.2,
            width=0.2,
            split_spaces=True,
            retry=False,
            fuzz_threshold=80,
        ):
            while not wh.read_screen(top=0.8, width=0.8, height=0.1):
                wh.click(
                    0.5, 0.5, relative=True, pre_click_delay=0.0, post_click_delay=0.0
                )
            advantage_check()
        if in_room_selection():
            return


def fight():
    wh.click_text(
        "To Battle", top=0.75, left=0.8, height=0.2, includes=True, retry=False
    )
    global killed_teammates
    if not killed_teammates:
        kill_teammates()

    while True:
        if wh.click_text(
            "Win", top=0.6, left=0.5, height=0.3, retry=False, click=False
        ):
            wh.press("p")
            sleep(0.1)
            wh.press("enter")
            sleep(5)

        if wh.click_text("SKIP", top=0.8, left=0.8, retry=False):
            question()

        if handle_gift() == "Dungeon Complete":
            return "Dungeon Complete"

        if in_room_selection():
            print("Fight Ended Due to Seeing Numbers")
            sleep(0.5)
            return

        if wh.click_text(
            "SELECT",
            top=0.1,
            left=0.3,
            width=0.4,
            height=0.2,
            click=False,
            includes=True,
            retry=False,
        ):
            print("Fight Ended Due to Seeing Select")
            return

        sleep(0.5)


def handle_encounter():
    while accept_gift(True):
        sleep(0.5)
    while not in_room_selection():
        sleep(0.5)

    room = wh.match_template(
        question_room_icon,
        brightness=0.25,
        saturation=0.5,
        top=0.05,
        left=0.5,
        width=0.15,
        height=0.85,
        confidence_threshold=0.0,
    )
    if room:
        wh.click(*room)
        wh.press("d")
        sleep(0.5)
    if not wh.click_text(
        "Clear Rewards",
        top=0.6,
        left=0.5,
        width=0.2,
        height=0.2,
        click=False,
        retry=False,
    ):
        wh.press("enter")
        return question()
    wh.press("enter")
    sleep(1)
    wh.press("enter")
    sleep(2.0)
    return fight()


def complete_floor():
    global floor_complete
    while not floor_complete:
        result = handle_encounter()
        if result == "Dungeon Complete":
            return result
    floor_complete = False


def run(floor=0):
    print("Begin Run")
    global killed_teammates, last_floor, currently_enhanced, ego_gifts, require_gift_calibration
    killed_teammates = floor > 0
    last_floor = floor
    currently_enhanced = set()
    ego_gifts = []
    if not in_room_selection():
        enter()
    else:
        require_gift_calibration = True
    while complete_floor() != "Dungeon Complete":
        pass
    wh.click_text("Confirm", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.6, width=0.2, height=0.2)
    sleep(1)
    confirm(True)
    sleep(2)
    confirm(True)
    sleep(3)
    confirm(True)
    sleep(3)


if __name__ == "__main__":
    kill_keybind()
    pause_keybind()
    parser = ArgumentParser()
    parser.add_argument("-n", "--runs", type=int, default=0)
    parser.add_argument("-f", "--floor", type=int, default=1)
    parser.add_argument("-i", "--infinite", type=bool, default=False)
    parser.add_argument("-e", "--easy", type=bool, default=False)
    args = parser.parse_args()

    if args.runs == 0 and not args.infinite:
        print("Which would you like to do?")
        print("1. Run infinitely (just type nothing and press enter)")
        print("2. Run a specific number of times (type the number and press enter)")
        choice = input()
        if choice.strip() == "":
            args.infinite = True
        else:
            args.runs = int(choice)
        print(
            "Would you like easy or hard mode? (type 'e' for easy and anything else for hard)"
        )
        choice = input()
        if choice.strip().lower() == "e":
            args.easy = True

    easy = args.easy

    if args.infinite:
        while True:
            t = time.time()
            run()
            print("Run completed in", round((time.time() - t) / 60, 2), "minutes")
    else:
        for _ in range(args.runs):
            t = time.time()
            run(args.floor - 1)
            print("Run completed in", round((time.time() - t) / 60, 2), "minutes")
