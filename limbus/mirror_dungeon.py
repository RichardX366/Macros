from argparse import ArgumentParser
from time import sleep
from typing import cast

from helpers import WindowHelper, bounding_box_center

try:
    wh = WindowHelper("LimbusCompany")
except:
    wh = WindowHelper("iPhone Mirroring")

from pyautogui import press

floor_complete = False


def enter():
    wh.click_text("Drive", top=0.8, left=0.7, width=0.2)
    sleep(0.5)
    wh.click_text("Mirror", top=0.3, left=0.2, width=0.3, height=0.3, split_spaces=True)
    sleep(0.5)
    wh.click_text("Enter", top=0.6, left=0.7, pre_click_delay=0.5, post_click_delay=0.5)
    sleep(0.5)
    wh.click_text("Enter", top=0.6, left=0.5, width=0.2)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.7)
    sleep(0.5)
    wh.click_text("Cumulating Starcloud", top=0.2, left=0.1)
    sleep(0.5)
    wh.click_text("Starlight Guidance", top=0.2, left=0.1, use_cache=True)
    sleep(0.5)
    wh.click_text("Enter", top=0.2, left=0.1, use_cache=True)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Bleed", top=0.2, left=0.1, width=0.5, height=0.6)
    sleep(0.5)
    wh.click_text("Wound Cleric", top=0.3, left=0.6, width=0.4, height=0.6)
    wh.click_text("Select", top=0.3, left=0.6, width=0.4, height=0.6, use_cache=True)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.3)
    sleep(2)
    wh.click_text("SELECT", top=0.1, left=0.3, width=0.4, height=0.2, click=False)
    wh.drag(0.5, 0.4, 0.5, 0.8, relative=True)
    sleep(1)


def advantage_check():
    order = ["Very High", "High", "Norma", "Low", "Very Low"]
    text = wh.read_screen(top=0.8, confidence_threshold=0.1)
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
            y = text[0][0][1][1] + 20
            wh.click(x, y)
            sleep(0.5)
            wh.click_text("Commence", top=0.8, left=0.8)
            sleep(1.0)
            while not wh.click_text(
                "Check",
                fuzz_threshold=40,
                confidence_threshold=0.1,
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
                if wh.click_text(
                    "SKIP", top=0.8, left=0.8, use_cache=True, retry=False
                ):
                    sleep(0.1)
                wh.click(0.6, 0.6, relative=True)
                sleep(0.1)
            return


def handle_shop():
    wh.click_text("Heal", top=0.5, width=0.3, height=0.3)
    sleep(0.5)
    wh.click_text("All Sinners heal 20% HP and 15 SP", top=0.3, left=0.5, height=0.3)
    sleep(0.5)
    wh.click_text("Leave", top=0.8, left=0.8)
    sleep(0.5)

    def get_balance():
        balance_text = wh.read_screen(top=0.1, left=0.4, width=0.2, height=0.2)
        return int(balance_text[0][1].replace(",", ""))

    text = wh.read_screen(top=0.3, left=0.4, width=0.5, height=0.4)

    replace = [t for t in text if "Replace" in t[1]][0]
    x, y = bounding_box_center(replace[0])
    wh.click(x, y - 60)
    sleep(0.5)
    wh.click_text("moderate", top=0.2, left=0.1, width=0.8, height=0.2, includes=True)
    sleep(0.1)
    wh.click_text(
        "large", top=0.2, left=0.1, width=0.8, height=0.2, includes=True, use_cache=True
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
    wh.click_text("Confirm", top=0.65, left=0.5, width=0.2, height=0.2, use_cache=True)
    sleep(1)

    balance = get_balance()
    rows = []
    last_top = 0
    for t in text:
        if t[1].isnumeric():
            top = t[0][0][1]
            if abs(top - last_top) > 20:
                rows.append([])
                last_top = top
            rows[-1].append(t)
    for row in rows:
        row.sort(key=lambda t: t[0][0][0])

    items = [item for row in rows for item in row]

    def get_next():
        max_item = None
        for item in items:
            if int(item[1]) <= balance and (
                not max_item or int(item[1]) > int(max_item[1])
            ):
                max_item = item
        return max_item

    while get_next():
        next_item = get_next()
        box, cost, confidence = cast(tuple, next_item)
        x, y = bounding_box_center(box)
        wh.click(x, y - 60)
        sleep(1)
        wh.click_text("Purchase", top=0.6, left=0.5, width=0.2, height=0.3, retry=False)
        sleep(1)
        wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.3, retry=False)
        sleep(1)
        index = items.index(next_item)
        for i, item in enumerate(items[index:-1]):
            items[index + i] = (item[0], items[index + i + 1][1], item[2])
        items[-1] = (items[-1][0], "999999", items[-1][2])
        balance -= int(cost)

    wh.click_text("Leave", top=0.8, left=0.8)
    sleep(0.5)
    wh.click_text("Confirm", top=0.65, left=0.5, width=0.2, height=0.2)
    sleep(5)
    press("d")
    sleep(1.0)
    press("enter")
    sleep(1.0)
    result = fight()
    if result == "Dungeon Complete":
        global floor_complete
        floor_complete = True
        return result
    sleep(5)

    if wh.click_text(
        "Acquire E.G.O Gift", top=0.2, left=0.2, width=0.6, height=0.1, retry=False
    ):
        sleep(0.1)
        wh.click_text("Select", top=0.7, left=0.8, height=0.2)
        sleep(1)
        wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
        sleep(5)

    wh.drag(0.5, 0.4, 0.5, 0.8, relative=True)
    sleep(5)
    global floor_complete
    floor_complete = True


def question():
    sleep(1.5)
    if wh.click_text(
        "Shop", top=0.1, left=0.1, width=0.2, height=0.2, click=False, retry=False
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
            text = wh.read_screen(use_cache=True, left=0.5, height=0.8)
            text.pop(0)
            text = wh.clump_ocr(text)

            without_cursed = [t for t in text if not "Cursed" in t[1]]
            if not without_cursed:
                x, y = bounding_box_center(text[0][0])
                wh.click(x, y)
                continue

            without_battle = [t for t in without_cursed if not "Battle" in t[1]]
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

            sleep(0.5)

        if wh.click_text(
            "Advantage",
            left=0.5,
            height=0.3,
            includes=True,
            split_spaces=True,
            retry=False,
        ):
            sleep(1)
            wh.click_text(
                "Advantage",
                left=0.5,
                height=0.3,
                includes=True,
                split_spaces=True,
                use_cache=True,
                retry=False,
            )
            sleep(0.5)
            advantage_check()

        sleep(0.5)


def fight():
    wh.click_text(
        "To Battle", top=0.75, left=0.8, height=0.2, includes=True, retry=False
    )
    while True:
        if wh.click_text("Win", top=0.6, left=0.7, height=0.3, retry=False):
            sleep(0.1)
            press("enter")
            sleep(5)

        if wh.click_text("SKIP", top=0.8, left=0.8, retry=False):
            question()

        if wh.click_text(
            "Select Encounter Reward Card",
            top=0.2,
            left=0.1,
            width=0.6,
            height=0.1,
            click=False,
            retry=False,
        ):
            print("Fight Ended Due to Reward Card")
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
                sleep(0.1)
                wh.click_text(
                    "Confirm", top=0.5, left=0.1, width=0.8, height=0.3, use_cache=True
                )
                sleep(5)
                return

        if wh.click_text(
            "Acquire E.G.O Gift", top=0.2, left=0.2, width=0.6, height=0.1, retry=False
        ):
            print("Fight Ended Due to EGO Gift")
            sleep(0.1)
            wh.click_text("Select", top=0.7, left=0.8, height=0.2)
            sleep(1)
            wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
            sleep(5)

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
                sleep(0.1)
                wh.click_text(
                    "Confirm", top=0.5, left=0.1, width=0.8, height=0.3, use_cache=True
                )
                sleep(0.5)
                wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
                sleep(5)
                return

            return

        text = wh.read_screen(left=0.7, height=0.2)
        if len([t[1] for t in text if t[1].strip().isnumeric()]) >= 2:
            print("Fight Ended Due to Seeing Numbers", [t[1] for t in text])
            sleep(0.5)
            return

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

        sleep(1)


def handle_encounter():
    while wh.click_text(
        "Confirm", top=0.6, left=0.4, width=0.2, height=0.3, retry=False
    ):
        sleep(1)
    press("d")
    sleep(1)
    if not wh.click_text(
        "Clear Rewards",
        top=0.6,
        left=0.5,
        width=0.2,
        height=0.2,
        click=False,
        retry=False,
    ):
        press("enter")
        return question()
    press("a")
    sleep(1)
    press("w")
    sleep(1)
    if not wh.click_text(
        "Clear Rewards",
        top=0.6,
        left=0.5,
        width=0.2,
        height=0.2,
        click=False,
        retry=False,
    ):
        press("enter")
        return question()
    press("a")
    sleep(1)
    press("s")
    sleep(1)
    if not wh.click_text(
        "Clear Rewards",
        top=0.6,
        left=0.5,
        width=0.2,
        height=0.2,
        click=False,
        retry=False,
    ):
        press("enter")
        return question()
    press("enter")
    sleep(1)
    press("enter")
    sleep(2.0)
    return fight()


def complete_floor():
    global floor_complete
    while not floor_complete:
        result = handle_encounter()
        if result == "Dungeon Complete":
            return result
    floor_complete = False


def run():
    print("Begin Run")
    enter()
    while complete_floor() != "Dungeon Complete":
        pass
    wh.click_text("Confirm", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.8, height=0.2)
    sleep(0.5)
    wh.click_text("Claim", top=0.7, left=0.6, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
    sleep(2)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
    sleep(3)
    wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
    sleep(3)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", "--runs", type=int, default=0)
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
            run()
    else:
        for _ in range(args.runs):
            run()
