from time import sleep

from helpers import WindowHelper, bounding_box_center
from limbus.enkephalin import redeem_enkephalin
from limbus.open_limbus import launch_limbus

wh: WindowHelper = None  # type: ignore


def battle():
    while True:
        if wh.click_text(
            "Win",
            top=0.6,
            left=0.5,
            height=0.3,
            click=False,
            retry=False,
        ):
            wh.focus_window()
            wh.press("p")
            sleep(0.1)
            wh.press("enter")
            wh.restore_previous_window()
            sleep(5)
        if wh.click_text(
            "Confirm",
            top=0.7,
            left=0.7,
            retry=False,
        ):
            return
        sleep(1)


def main():
    redeem_enkephalin()

    wh.click(0.1, 0.1, relative=True)  # Click outside to close the Enkephalin screen

    print("Opening Luxcavation screen...")
    wh.click_text("Drive", top=0.8, left=0.7, width=0.2)
    sleep(0.5)
    wh.click_text("Luxcavation", top=0.2, left=0.25, width=0.2, height=0.15)
    sleep(0.5)

    print("Handling XP Luxcavation...")
    wh.click_text("Enter", top=0.6, left=0.75, width=0.2, height=0.15)
    sleep(0.5)
    wh.click_text("To Battle", top=0.75, left=0.8, height=0.2, includes=True)
    sleep(0.5)
    battle()
    sleep(0.5)

    print("Handling Thread Luxcavation...")
    wh.click_text("Thread", top=0.4, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Skip Battle", top=0.65, left=0.2, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Skip Battle", top=0.55, left=0.5, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Confirm", top=0.6, left=0.5, width=0.2, height=0.2)
    sleep(0.5)
    wh.click_text("Confirm", top=0.7, left=0.7)
    sleep(1)
    wh.focus_window()
    wh.press("esc")
    wh.restore_previous_window()
    sleep(0.5)

    print("Opening Limbus Pass...")
    wh.click_text("Window", top=0.5, left=0.6, width=0.2)
    sleep(0.5)
    wh.click_text("UNTIL SEASON 8 UPDATE", top=0.3, left=0.7, width=0.2, height=0.2)
    sleep(0.5)

    print("Claiming Limbus Pass missions...")
    wh.click_text("Pass Missions", left=0.2, width=0.2, height=0.2)
    sleep(0.5)
    text = wh.read_screen(top=0.2, left=0.3, height=0.7, width=0.2)
    for t in text:
        wh.click(*bounding_box_center(t[0]), post_click_delay=0.0)
    sleep(0.5)

    print("Claiming Limbus Pass Rewards...")
    wh.click_text("Battle Pass", left=0.1, width=0.2, height=0.2)
    sleep(0.5)
    for _ in range(10):
        if wh.click_text(
            "Claim",
            top=0.75,
            left=0.55,
            width=0.2,
            height=0.2,
            includes=True,
            retry=False,
        ):
            sleep(0.5)
            wh.click_text("Confirm", top=0.6, left=0.4, width=0.2, height=0.2)
            sleep(1)
            return
        sleep(1)


if __name__ == "__main__":
    try:
        launch_limbus()
        wh = WindowHelper("LimbusCompany")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        wh.mute(False)
        wh.close()
