from argparse import ArgumentParser
from typing import Callable

import numpy as np

from helpers import WindowHelper, bounding_box_center
from time import sleep

wh = WindowHelper("iPhone Mirroring")


level = [1]
cat_counts = [0] * 10


def click_cat(c: int):
    wh.click(
        0.33 + 0.08 * (c % 5),
        0.75 + 0.1 * (c // 5),
        relative=True,
        pre_click_delay=0.0,
        post_click_delay=0.0,
        restore_position=False,
    )
    cat_counts[c] += 1


def click_upgrade():
    global level
    wh.click(
        0.1,
        0.9,
        relative=True,
        pre_click_delay=0.0,
        post_click_delay=0.0,
        restore_position=False,
    )
    level[0] += 1


def run(upgrade: bool, cats: list[bool]):
    if cat_counts[7] > 0 and cat_counts[9] > 0:
        if cats[7]:
            click_cat(7)
        elif cats[6]:
            click_cat(6)
        elif cats[9]:
            click_cat(9)
        elif cats[8]:
            click_cat(8)
        elif upgrade and level[0] < 8:
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
    elif upgrade and level[0] < 5:
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


def attempt_run(plan: Callable[[bool, list[bool]], None], use_leadership=False):
    global level, cat_counts
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
        click=False,
    ):
        if use_leadership:
            wh.click_text(
                "Yes",
                top=0.6,
                left=0.35,
                width=0.1,
                height=0.1,
                brightness=0.99,
                includes=True,
                use_cache=True,
            )
        else:
            print("Leadership available, but not used. Exiting.")
            exit()
        sleep(1)
        wh.click_text("Attack", top=0.6, left=0.7, width=0.2, height=0.2, includes=True)
    sleep(1)

    while True:
        img = np.array(wh.screenshot(top=0.75))

        fire_color = (0xFB, 0xDC, 0x4C)
        fire_mask = np.all(
            np.abs(img[:, :, :3].astype(np.int16) - fire_color) <= 50, axis=-1
        )
        fire_height, fire_width = fire_mask.shape
        fire_y = int(0.81 * fire_height)
        fire_left, fire_right = int(0.85 * fire_width), int(0.91 * fire_width)

        fire = bool(np.any(fire_mask[fire_y, fire_left:fire_right]))

        buy_color = (0xF9, 0xF0, 0x50)
        buy_mask = np.all(
            np.abs(img[:, :, :3].astype(np.int16) - buy_color) <= 20, axis=-1
        )

        height, width = buy_mask.shape
        x_boundaries = np.linspace(0.3, 0.73, 6)
        x_pixels = (x_boundaries * width).astype(int)
        y_lines = (0.15, 0.67)
        upgrade_y = 0.88

        cats = [
            bool(np.any(buy_mask[int(y * height), left:right]))
            for y in y_lines
            for left, right in zip(x_pixels[:-1], x_pixels[1:])
        ]

        upgrade = bool(
            np.any(
                buy_mask[int(upgrade_y * height), int(0.07 * width) : int(0.13 * width)]
            )
        )

        if fire:
            wh.click(
                0.9,
                0.9,
                relative=True,
                pre_click_delay=0.0,
                post_click_delay=0.0,
                restore_position=False,
            )

        plan(upgrade, cats)

        if (
            not any(cats)
            and not upgrade
            and wh.click_text(
                "Victory",
                top=0.25,
                left=0.35,
                width=0.3,
                height=0.25,
                brightness=0.9,
                includes=True,
                retry=False,
                click=False,
            )
        ):
            break
    sleep(2)

    level[0] = 1
    for i in range(10):
        cat_counts[i] = 0


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--infinite", action="store_true")
    args = parser.parse_args()

    while True:
        get_next_non_superior()

        attempt_run(run)

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
