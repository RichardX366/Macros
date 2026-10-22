from argparse import ArgumentParser

import numpy as np

from helpers import WindowHelper, bounding_box_center
from time import sleep

wh = WindowHelper("iPhone Mirroring")


level = 1


def click_cat(c: int):
    wh.click(0.33 + 0.08 * (c % 5), 0.75 + 0.1 * (c // 5), relative=True)


def click_upgrade():
    global level
    wh.click(0.1, 0.9, relative=True, pre_click_delay=0.05, post_click_delay=0.05)
    level += 1


def plan(upgrade: bool, cats: list[bool]):
    if cats[7]:
        click_cat(7)
    elif cats[9]:
        click_cat(9)
    elif cats[5]:
        click_cat(5)
    elif cats[4]:
        click_cat(4)
    elif level < 5 and upgrade:
        click_upgrade()


wh.click_text("Attack", top=0.6, left=0.7, width=0.2, height=0.2, includes=True)
sleep(2)
while not wh.click_text(
    "Victory",
    top=0.3,
    left=0.35,
    width=0.3,
    height=0.2,
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
