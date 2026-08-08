from argparse import ArgumentParser
import re
from time import sleep
import time
from typing import cast

from PIL import Image
import cv2
import numpy as np

from helpers import WindowHelper, bounding_box_center, download_screenshot, kill_keybind

try:
    wh = WindowHelper("LimbusCompany")
except:
    wh = WindowHelper("iPhone Mirroring")


floor_complete = False
last_floor = 0
packs = [
    ["Chicken"],
    ["Unconfronting", "Gloom"],
    ["Addicting", "Certain", "Yield", "Degraded"],
    ["Line 4", "Line 1", "Line 3", "District"],
]
difficulties = [True, True, True, True]
poise_gifts = [
    "Spiderweb",
    "Clear",
    "Tomb",
    "Reminiscence",
    "Conceit",
    "Lucky",
    "Cask",
    "Finifugality",
    "Clover",
    "Pendant",
    "Nebulizer",
    "Endorphin",
    "Ornamental",
    "Share",
    "Emerald",
    "Old Wooden",
    "Cigarette",
    "Recollection",
    "Angel",
    "pom",
    "sack",
    "Broken Blade",
    "Ragged Bamboo",
    "Commemorative",
]
enhance_costs = (0, 100, 120, 150, 200)
enhanceable = ["Clear", "Tomb", "Nebulizer"]
currently_enhanced = set()

# Helpers


def in_room_selection():
    text = wh.read_screen(left=0.7, height=0.2, width=0.2)
    if len([t[1] for t in text if re.sub(r"\D", "", t[1]).isnumeric()]) >= 2:
        text = wh.read_screen(
            left=0.3, height=0.2, width=0.4, confidence_threshold=0.05
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
            height=0.3,
            includes=True,
            retry=False,
        ) or wh.click_text(
            "Resource",
            top=0.5,
            left=0.1,
            width=0.8,
            height=0.3,
            includes=True,
            use_cache=True,
            retry=False,
        ):
            sleep(0.5)
            wh.click_text(
                "Confirm", top=0.5, left=0.1, width=0.8, height=0.3, use_cache=True
            )
            sleep(1)
            wh.click_text(
                "Confirm", top=0.6, left=0.4, width=0.2, height=0.2, retry=False
            )
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
        gifts.sort(
            key=lambda x: (
                9999
                if x["owned"]
                else (
                    min(
                        (i for i, gift in enumerate(poise_gifts) if gift in x["name"]),
                        default=999,
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
        sleep(1)
        wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
        sleep(0.5)
        wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2, retry=False)
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

    sleep(1.5)
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
                sleep(0.5)
                mouseUp()
                moveTo(x, y)
                wh.read_screen(top=0.45, left=0.45, height=0.2)
            sleep(0.5)
            wh.click(0.6, 0.8, relative=True)
            sleep(0.5)
            wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
        else:
            wh.click(0.85, 0.1, relative=True)
        sleep(1.5)

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


unit_distance = 0.0
killed_teammates = False


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
        wh.click(last_unit - i * unit_distance, text[0][0][0][1])

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
    y_diff = 0.12
    row = index // 5
    col = index % 5
    x = 0.52 + col * x_diff
    y = 0.4 + row * y_diff
    return x, y


def get_gift_levels():
    arr = np.array(wh.screenshot().convert("RGB"))
    binary = (np.all(arr == (0xF7, 0xC1, 0x00), axis=2) * 255).astype(np.uint8)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blobs = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        if area < 5:
            continue

        crop = binary[y : y + h, x : x + w]
        white = np.count_nonzero(crop)
        white_ratio = white / crop.size
        if white_ratio < 0.3:
            continue

        blobs.append(
            {
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "text": "i" if h / w > 5 else "v",
                "center": (x + w / 2, y + h / 2),
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
                            blob["x"] + blob["width"] / 2,
                            blob["y"] + blob["height"] / 2,
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
    #         (blob["x"], blob["y"]),
    #         (blob["x"] + blob["width"], blob["y"] + blob["height"]),
    #         (0, 0, 255),
    #         1,
    #     )
    # download_screenshot(Image.fromarray(output))

    return merged


def get_gift_level(index: int, blobs: list[dict]):
    coords = index_to_gift_coord(index)
    x = coords[0] * wh.width
    y = coords[1] * wh.height
    fit = [b for b in blobs if b["x"] < x and b["y"] < y]
    fit.sort(key=lambda b: x - b["x"] + y - b["y"])
    return fit[0]["text"] if fit else 0


def get_gift_list(shift_vestiges=False):
    wh.click_text("Enhance", top=0.5, left=0.1, width=0.1, height=0.1)
    sleep(0.5)
    blobs = get_gift_levels()
    blobs = [b for b in blobs if b["x"] > 0.5 * wh.width and b["y"] > 0.3 * wh.height]
    gifts = []
    for i in range(len(blobs)):
        wh.click(
            *index_to_gift_coord(i),
            relative=True,
            pre_click_delay=0.0,
            post_click_delay=0.0,
        )
        wh.set_bounds(0.2, 0.2, 0.25, 0.2)
        bw = cv2.threshold(
            cv2.cvtColor(
                cv2.cvtColor(np.array(wh.screenshot()), cv2.COLOR_RGB2BGR),
                cv2.COLOR_BGR2GRAY,
            ),
            200,
            255.0,
            cv2.THRESH_BINARY,
        )[1]
        text = wh.read_screen(image=bw, top=0.2, left=0.2, width=0.25, height=0.2)
        name = " ".join([t[1] for t in text])
        gift = {
            "name": name,
            "level": get_gift_level(i, blobs),
        }
        gifts.append(gift)
    wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)
    if shift_vestiges:
        return [g for g in gifts if " Vestige" in g["name"]] + [
            g for g in gifts if " Vestige" not in g["name"]
        ]
    return gifts


def power_up_gift(index: int):
    wh.click_text("Enhance", top=0.5, left=0.1, width=0.1, height=0.1)
    sleep(0.5)
    wh.click(*index_to_gift_coord(index), relative=True)
    wh.click_text("Power", top=0.7, left=0.5, width=0.2, height=0.2, includes=True)
    sleep(0.5)
    wh.click(0.8, 0.72, relative=True)
    wh.click_text("Confirm", top=0.8, left=0.5, width=0.2, height=0.1)
    wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)


question_room_icon = cast(
    np.ndarray, cv2.imread("limbus/fast_mirror/question.png", cv2.IMREAD_GRAYSCALE)
)


# Overarching functions


def enter():
    wh.click_text("Drive", top=0.8, left=0.7, width=0.2)
    wh.click_text("Mirror", top=0.3, left=0.2, width=0.3, height=0.3, split_spaces=True)
    sleep(0.5)
    while not wh.click_text("Enter", top=0.6, left=0.5, width=0.2, retry=False):
        wh.click_text(
            "Enter", top=0.6, left=0.7, pre_click_delay=0.5, post_click_delay=0.5
        )
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
    wh.click(0.5, 0.3, relative=True)
    wh.click(0.9, 0.9, relative=True)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
    wh.click_text("Poise", top=0.5, left=0.25, width=0.1, height=0.1)
    wh.click_text("Stone Tomb", top=0.4, left=0.6, width=0.2, height=0.2)
    wh.click(0.8, 0.8, relative=True)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.3)
    wh.click_text("Keyword", top=0.2, left=0.45, width=0.1, height=0.1, includes=True)
    sleep(0.5)
    wh.click(0.55, 0.8, relative=True)
    wh.click(0.85, 0.8, relative=True)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.3)
    wh.click_text(
        "SELECT", top=0.1, left=0.3, width=0.4, height=0.2, click=False, includes=True
    )
    roll_for_pack(["Gamblers"], True)


def advantage_check():
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
            if not wh.click_text("Commence", top=0.8, left=0.8, retry=False):
                wh.click(x, y)
                sleep(0.5)
                wh.click_text("Commence", top=0.8, left=0.8)

            sleep(1.0)
            while not wh.click_text(
                "Check",
                fuzz_threshold=40,
                top=0.6,
                left=0.6,
                width=0.3,
                height=0.2,
                retry=False,
                split_spaces=True,
            ):
                sleep(1)
            while not wh.click_text(
                "Continue", top=0.8, left=0.8, click=False, retry=False
            ) and not wh.click_text(
                "Proceed", top=0.8, left=0.8, click=False, retry=False, use_cache=True
            ):
                wh.click_text("SKIP", top=0.8, left=0.8, use_cache=True, retry=False)
                wh.click(0.6, 0.6, relative=True)
                sleep(0.1)
            return


def handle_shop():
    def get_balance(iter=0):
        balance_text = wh.read_screen(top=0.1, left=0.4, width=0.2, height=0.2)
        balance = [
            t[1].replace(",", "")
            for t in balance_text
            if t[1].replace(",", "").isnumeric()
        ]
        if not balance and iter < 3:
            sleep(0.5)
            return get_balance(iter + 1)
        return int(balance[0]) if balance else 0

    if get_balance() >= 100:
        wh.click_text("Heal", top=0.5, width=0.3, height=0.3)
        sleep(0.5)
        wh.click_text(
            "All Sinners heal 20% HP and 15 SP", top=0.3, left=0.5, height=0.3
        )
        sleep(1)
        wh.click_text("Leave", top=0.8, left=0.8, retry=False)
        wh.click_text("Return", top=0.8, left=0.8, retry=False)
        sleep(0.5)

    text = wh.read_screen(top=0.3, left=0.4, width=0.5, height=0.5)

    gift_list = get_gift_list(True)

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

    def replace_skill():
        replace_skills = [t for t in text if "Ryoshu" in t[1]]
        print(f"Replacements: {[t[1] for t in text if "Replace" in t[1]]}")
        for replace in replace_skills:
            if is_purchased(replace):
                continue

            x, y = bounding_box_center(replace[0])
            wh.click(x, y - 0.06 * wh.height)
            sleep(0.5)
            wh.click_text(
                "moderate", top=0.2, left=0.1, width=0.8, height=0.2, includes=True
            )
            sleep(0.1)
            wh.click_text(
                "large",
                top=0.2,
                left=0.1,
                width=0.8,
                height=0.2,
                includes=True,
                use_cache=True,
            )
            sleep(0.1)
            wh.click_text(
                "tremendous",
                top=0.2,
                left=0.1,
                width=0.8,
                height=0.2,
                includes=True,
                use_cache=True,
            )
            sleep(0.5)
            wh.click_text("Confirm", top=0.65, left=0.5, width=0.2, height=0.2)
            sleep(1)
            wh.click_text(
                "Confirm", top=0.65, left=0.5, width=0.2, height=0.2, use_cache=True
            )
            sleep(1)

    def get_items():
        nonlocal text
        text = wh.read_screen(top=0.3, left=0.4, width=0.5, height=0.5)
        items = []
        for t in text:
            if t[1].isnumeric():
                if is_purchased(t):
                    continue
                label = sorted(text, key=lambda x: bounding_distance(t[0], x[0]))[1][1]
                poise = False
                for gift in poise_gifts:
                    if gift in label:
                        poise = True
                        break
                if not poise:
                    continue
                item = {"box": t[0], "cost": t[1], "name": label}
                items.append(item)
        items.sort(key=lambda x: int(x["cost"]))
        return items

    def purchase(item):
        x, y = bounding_box_center(item["box"])
        wh.click(x, y - 0.06 * wh.height)
        sleep(1)
        wh.click_text("Purchase", top=0.6, left=0.5, width=0.2, height=0.3, retry=False)
        sleep(1)
        wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.3, retry=False)
        sleep(1)

    def buy_items():
        sleep(0.5)
        items = get_items()
        balance = get_balance()
        if balance >= 120:
            replace_skill()
            balance = get_balance()
        gift_names = [g["name"] for g in gift_list]
        for item in items:
            if int(item["cost"]) <= balance:
                purchase(item)
                gift_names.append(item["name"])
                balance -= int(item["cost"])
            else:
                break
        if any(
            any(e in g and e not in currently_enhanced for e in enhanceable)
            for g in gift_names
        ):
            gl = get_gift_list()
            to_enhance = [
                g
                for g in gl
                if any(
                    e in g["name"] and e not in currently_enhanced for e in enhanceable
                )
            ]
            costs = [enhance_costs[g["level"]] for g in to_enhance]
            balance = get_balance()
            for cost, gift in zip(costs, to_enhance):
                if cost <= balance:
                    power_up_gift(gl.index(gift))
                    currently_enhanced.add(
                        [name for name in enhanceable if name in gift["name"]][0]
                    )
                    balance -= cost

    buy_items()
    if get_balance() >= 120:
        wh.click_text("Refresh", top=0.1, left=0.75, width=0.1, height=0.1)
        buy_items()

        while get_balance() >= 400:
            wh.click_text("Keyword", top=0.1, left=0.85, width=0.1, height=0.1)
            wh.click_text("POISE", top=0.6, left=0.2, width=0.1, height=0.1)
            wh.click_text("Refresh", top=0.75, left=0.5, width=0.2, height=0.1)
            buy_items()

    def fuse(gifts: list[int]):
        wh.click_text("Fuse", top=0.5, left=0.2, width=0.1, height=0.1)
        sleep(0.5)
        wh.click(0.5, 0.3, relative=True)
        wh.click_text("POISE", top=0.6, left=0.2, width=0.1, height=0.1)
        wh.click_text("Confirm", top=0.75, left=0.5, width=0.2, height=0.1)
        sleep(0.5)
        for i in range(3):
            wh.click(*index_to_gift_coord(gifts[i]), relative=True)
        wh.click_text("Fuse", top=0.8, left=0.6, width=0.1, height=0.1)
        sleep(0.5)
        wh.click_text("Fuse", top=0.8, left=0.6, width=0.1, height=0.1, use_cache=True)
        wh.click_text("Confirm", top=0.7, left=0.4, width=0.2, height=0.1)
        wh.click_text("Close", top=0.8, left=0.35, width=0.1, height=0.1)

    def remove_preserved(gifts: list[dict]):
        excess_gifts = [
            (i, g)
            for i, g in enumerate(gifts)
            if g["level"] < 4 and not any(p in g["name"] for p in poise_gifts)
        ]
        removed = []
        l3 = [g[0] for g in excess_gifts if g[1]["level"] == 3]
        if l3:
            excess_gifts.remove((l3[0], gifts[l3[0]]))
            removed.append(l3[0])
            l3.remove(l3[0])
        if l3:
            excess_gifts.remove((l3[0], gifts[l3[0]]))
            removed.append(l3[0])
        l2 = [g[0] for g in excess_gifts if g[1]["level"] == 2]
        if l2:
            excess_gifts.remove((l2[0], gifts[l2[0]]))
            removed.append(l2[0])
        return removed, [g[0] for g in excess_gifts]

    removed, gifts = remove_preserved(gift_list)
    while len(removed) > 2:
        fuse(removed)
        removed, gifts = remove_preserved(get_gift_list(True))

    while len(gifts) > 2:
        fuse(gifts[:3])
        if len(gifts) < 5:
            break
        removed, gifts = remove_preserved(get_gift_list(True))

    wh.click_text("Leave", top=0.8, left=0.8)
    sleep(0.5)
    wh.click_text("Confirm", top=0.65, left=0.5, width=0.2, height=0.2)
    sleep(1)
    while not wh.click_text(
        "Enter", top=0.65, left=0.8, height=0.2, retry=False, click=False
    ):
        wh.press("d")
        sleep(1)
    wh.press("enter")
    sleep(1.0)
    result = fight()
    if result == "Dungeon Complete":
        global floor_complete
        floor_complete = True
        return result

    global last_floor
    roll_for_pack(packs[last_floor], difficulties[last_floor])
    last_floor += 1
    sleep(3)
    floor_complete = True


def question():
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
        wh.click_text("Skip", top=0.8, left=0.8, retry=False)
        wh.click_text("Proceed", top=0.8, left=0.8, use_cache=True, retry=False)
        if wh.click_text("Continue", top=0.8, left=0.8, use_cache=True, retry=False):
            sleep(2)
            if battle_flag:
                fight()
                sleep(0.5)
            wh.click_text(
                "Confirm", top=0.6, left=0.4, width=0.2, height=0.2, retry=False
            )
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

            sleep(0.1)

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
            sleep(0.1)
            while not wh.read_screen(top=0.8, width=0.8, height=0.1):
                wh.click(0.5, 0.5, relative=True)
                sleep(0.1)
            advantage_check()
        if in_room_selection():
            return

        sleep(0.1)


def fight():
    wh.click_text(
        "To Battle", top=0.75, left=0.8, height=0.2, includes=True, retry=False
    )
    global killed_teammates
    if not killed_teammates:
        kill_teammates()
    while True:
        if wh.click_text("Win", top=0.6, left=0.5, height=0.3, retry=False):
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
            sleep(0.5)
            return

        sleep(1)


def handle_encounter():
    while wh.click_text(
        "Confirm", top=0.6, left=0.4, width=0.2, height=0.3, retry=False
    ):
        sleep(0.5)
    while not in_room_selection():
        sleep(0.5)

    wh.drag(0.1, 0.5, 0.1, 0.55, relative=True)
    sleep(0.5)
    room = wh.match_template(
        question_room_icon,
        threshold=0.27,
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
    global killed_teammates, last_floor, currently_enhanced
    killed_teammates = floor > 0
    last_floor = floor
    currently_enhanced = set()
    if not in_room_selection():
        enter()
    while complete_floor() != "Dungeon Complete":
        pass
    wh.click_text("Confirm", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.6, width=0.2, height=0.2)
    sleep(1)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2, retry=False)
    sleep(2)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2, retry=False)
    sleep(3)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2, retry=False)
    sleep(3)


if __name__ == "__main__":
    kill_keybind()
    parser = ArgumentParser()
    parser.add_argument("-n", "--runs", type=int, default=0)
    parser.add_argument("-f", "--floor", type=int, default=1)
    parser.add_argument("-i", "--infinite", type=bool, default=False)
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

    if args.infinite:
        while True:
            t = time.time()
            run()
            print("Run completed in", round(time.time() - t, 2), "seconds")
    else:
        for _ in range(args.runs):
            t = time.time()
            run(args.floor - 1)
            print("Run completed in", round(time.time() - t, 2), "seconds")
