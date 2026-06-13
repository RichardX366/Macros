from argparse import ArgumentParser

from helpers import WindowHelper, download_screenshot


def main():
    wh = WindowHelper("LimbusCompany")
    parser = ArgumentParser()
    parser.add_argument("-t", "--top", type=float, default=0.0)
    parser.add_argument("-l", "--left", type=float, default=0.0)
    parser.add_argument("-w", "--width", type=float, default=0.0)
    parser.add_argument("-y", "--height", type=float, default=0.0)
    args = parser.parse_args()
    wh.set_bounds(
        top=args.top,
        left=args.left,
        width=args.width,
        height=args.height,
    )
    download_screenshot(wh.screenshot(), "screenshot.png")


if __name__ == "__main__":
    main()
