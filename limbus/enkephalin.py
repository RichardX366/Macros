from time import sleep

from helpers import WindowHelper, bounding_box_center
from limbus.open_limbus import launch_limbus


def main(wh: WindowHelper):
    wh.mute(True)

    print("Loading game...")
    wh.click_text(
        "FACE THE SIN, SAVE THE E.G.O",
        top=0.6,
        left=0.3,
        height=0.2,
        width=0.4,
        click=False,
    )
    sleep(1)
    wh.click(0.5, 0.5, relative=True)

    print("Waiting for game to load and opening Enkephalin screen...")
    wh.click_text("LUNACY", top=0.8, left=0.35, width=0.2, click=False)
    wh.click(0.3, 0.9, relative=True)
    sleep(0.5)

    print("Clicking >> button...")
    text = wh.read_screen(top=0.3, left=0.3, height=0.5, width=0.4)
    confirm_box = [t for t in text if "Confirm" in t[1]][0][0]
    owned_box = [t for t in text if "Owned" in t[1]][0][0]
    recovered_box = [t for t in text if "recovered" in t[1]][0][0]
    x = confirm_box[1][0]
    y = (owned_box[2][1] + recovered_box[0][1]) / 2
    wh.click(x, y, pre_click_delay=0.2)

    print("Confirming...")
    confirm_center = bounding_box_center(confirm_box)
    wh.click(
        confirm_center[0],
        confirm_center[1],
    )

    sleep(1)


if __name__ == "__main__":
    try:
        launch_limbus()
        wh = WindowHelper("LimbusCompany")
        main(wh)
    except KeyboardInterrupt:
        pass
    finally:
        wh.mute(False)
        wh.close()
