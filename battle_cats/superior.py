from argparse import ArgumentParser

import numpy as np

from helpers import WindowHelper, bounding_box_center
from time import sleep

wh = WindowHelper("iPhone Mirroring")


level = 1
cat_counts = [0] * 10


def click_cat(c: int):
    wh.click(
        0.33 + 0.08 * (c % 5),
        0.75 + 0.1 * (c // 5),
        relative=True,
        pre_click_delay=0.0,
        post_click_delay=0.0,
    )
    cat_counts[c] += 1


def click_upgrade():
    global level
    wh.click(0.1, 0.9, relative=True)
    level += 1


def plan(upgrade: bool, cats: list[bool]):
    if cat_counts[7] > 0 and cat_counts[9] > 0:
        if cats[7]:
            click_cat(7)
        elif cats[6]:
            click_cat(6)
        elif cats[9]:
            click_cat(9)
        elif cats[8]:
            click_cat(8)
        elif upgrade and level < 8:
            click_upgrade()
        elif cats[3]:
            click_cat(3)
        elif cats[6]:
            click_cat(6)
        elif cats[5]:
            click_cat(5)
        elif cats[4]:
            click_cat(4)
        elif cats[2]:
            click_cat(2)
        return

    if cats[7]:
        click_cat(7)
    elif cats[9]:
        click_cat(9)
    elif cats[3]:
        click_cat(3)
    elif upgrade and level < 5:
        click_upgrade()
    elif cats[2]:
        click_cat(2)


def is_superior():
    screenshot = wh.screenshot(top=0.15, left=0.55, width=0.05, height=0.1)
    color = (0xFD, 0x49, 0x31)
    return np.any(np.all(np.abs(np.array(screenshot)[:, :, :3] - color) <= 20, axis=-1))


def next_state():
    from pyautogui import position, drag, moveTo

    x, y = position()
    wh.click(0.5, 0.4, focus=False, relative=True, restore_position=False)
    drag(-100, 0, duration=0.5, button="left")
    moveTo(x, y)


def get_next_non_superior():
    wh.focus_window()
    i = 0
    while is_superior():
        next_state()
        sleep(0.5)
        i += 1
        if i > 100:
            raise Exception("Could not find non-superior level")


parser = ArgumentParser()
parser.add_argument("-i", "--infinite", action="store_true")
args = parser.parse_args()

while True:
    get_next_non_superior()
    wh.click_text("Attack", top=0.6, left=0.7, width=0.2, height=0.2, includes=True)
    sleep(1)
    if wh.click_text(
        "Yes",
        top=0.6,
        left=0.35,
        width=0.1,
        height=0.1,
        brightness=0.99,
        includes=True,
        retry=False,
    ):
        sleep(1)
        wh.click_text("Attack", top=0.6, left=0.7, width=0.2, height=0.2, includes=True)
    sleep(1)
    while not wh.click_text(
        "Victory",
        top=0.25,
        left=0.35,
        width=0.3,
        height=0.25,
        brightness=0.9,
        includes=True,
        retry=False,
        click=False,
    ):
        text = wh.read_screen(
            saturation=0.65,
            brightness=0.7,
            top=0.7,
            width=0.7,
            confidence_threshold=0.0,
        )
        boxes = [bounding_box_center(t[0]) for t in text]
        upgrade = any(b[0] / wh.width < 0.2 and 0.9 < b[1] / wh.height for b in boxes)
        cats = [
            any(
                0.32 + 0.08 * (c % 5) < b[0] / wh.width < 0.40 + 0.08 * (c % 5)
                and 0.75 + 0.1 * (c // 5) < b[1] / wh.height < 0.85 + 0.1 * (c // 5)
                for b in boxes
            )
            for c in range(10)
        ]
        plan(upgrade, cats)
        sleep(0.05)
    sleep(2)

    level = 1
    cat_counts = [0] * 10

    if wh.click_text(
        "Superior",
        top=0.65,
        left=0.3,
        width=0.4,
        height=0.15,
        brightness=0.9,
        includes=True,
        retry=False,
    ):
        if not args.infinite:
            exit()

    while not wh.click_text(
        "Star",
        top=0.25,
        left=0.1,
        width=0.2,
        height=0.15,
        brightness=0.99,
        includes=True,
        retry=False,
    ):
        wh.click(0.5, 0.9, relative=True)
        sleep(1)
    sleep(1)
