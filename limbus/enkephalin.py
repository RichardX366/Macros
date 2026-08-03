from time import sleep

from helpers import WindowHelper, bounding_box_center
from limbus.open_limbus import launch_limbus

wh: WindowHelper = None  # type: ignore


def redeem_enkephalin():
    wh.mute(True)

    print("Loading game...")
    while not wh.click_text(
        "LUNACY", top=0.8, left=0.35, width=0.2, click=False, retry=False
    ):
        print(
            "Instead of LUNACY, found:",
            [
                t[1]
                for t in wh.read_screen(top=0.8, left=0.35, width=0.2, use_cache=True)
            ],
        )
        wh.click_text(
            "FACE", top=0.6, left=0.3, height=0.2, width=0.4, includes=True, retry=False
        )
        sleep(5)

    print("Opening Enkephalin screen...")
    wh.click(0.3, 0.9, relative=True)
    sleep(1.0)

    print("Clicking >> button...")
    text = wh.read_screen(top=0.2, left=0.3, height=0.6, width=0.4)
    confirm_box = [t for t in text if "Confirm" in t[1]][0][0]
    owned_box = [t for t in text if "Owned" in t[1]][0][0]
    use_boxes_box = [t for t in text if "Boxes" in t[1]][0][0]
    x = confirm_box[2][0]
    y = bounding_box_center(owned_box)[1] + owned_box[0][1] - use_boxes_box[0][1]
    wh.click(x, y, pre_click_delay=0.2)

    print("Confirming...")
    confirm_center = bounding_box_center(confirm_box)
    wh.click(
        confirm_center[0],
        confirm_center[1],
    )

    sleep(1)


def main():
    redeem_enkephalin()


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
