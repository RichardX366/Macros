from argparse import ArgumentParser
from time import sleep

from battle_cats.superior import (
    attempt_run,
    click_cat,
    click_upgrade,
    level,
    cat_counts,
    wh,
)
from helpers import bounding_box_center


def run(upgrade: bool, cats: list[bool]):
    if cat_counts[7] > 0:
        if cats[8]:
            click_cat(8)
        elif cats[7]:
            click_cat(7)
        elif cats[9]:
            click_cat(9)
        elif level[0] < 8 and upgrade:
            click_upgrade()
        if cats[3]:
            click_cat(3)
        if cats[4]:
            click_cat(4)
        if cats[6]:
            click_cat(6)
        if cats[5]:
            click_cat(5)
        return

    if cat_counts[8] > 0:
        if cats[7]:
            click_cat(7)
        return

    if cats[8]:
        click_cat(8)
    elif cats[3] and cat_counts[3] < 1:
        click_cat(3)
    elif cats[4] and cat_counts[4] < 1:
        click_cat(4)
    elif cats[5] and cat_counts[5] < 1:
        click_cat(5)
    elif cats[6] and cat_counts[6] < 1:
        click_cat(6)
    elif level[0] < 4 and upgrade:
        click_upgrade()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-n", "--runs", type=int, default=1, help="Number of runs to perform"
    )
    parser.add_argument(
        "-l", "--leadership", action="store_true", help="Whether to use leadership"
    )
    args = parser.parse_args()

    for _ in range(args.runs):
        attempt_run(run, use_leadership=args.leadership)
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
        sleep(2)
        start = wh.click_text(
            "Star",
            top=0.25,
            left=0.1,
            width=0.2,
            height=0.15,
            brightness=0.99,
            includes=True,
            use_cache=True,
        )
        if not start:
            raise Exception("Could not find Start button")
        coords = bounding_box_center(start[0])
        while not wh.click_text(
            "Attack",
            top=0.6,
            left=0.7,
            width=0.2,
            height=0.2,
            includes=True,
            retry=False,
            click=False,
        ):
            wh.click(*coords)
            sleep(2)
