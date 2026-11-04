from argparse import ArgumentParser
import os
import sys
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

from helpers import WindowHelper


def main():
    try:
        wh = WindowHelper("LimbusCompany")
    except Exception:
        wh = WindowHelper("iPhone Mirroring")

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

    try:
        reader = easyocr.Reader(["en"], gpu=True)
    except Exception:
        reader = easyocr.Reader(["en"], gpu=False)

    while True:
        img = np.array(wh.screenshot())

        results = reader.readtext(image=cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        # results = wh.clump_ocr(results)

        for box, text, confidence in results:
            # box is 4 points: top-left, top-right, bottom-right, bottom-left
            pts = [(int(x), int(y)) for x, y in box]
            x1 = min(p[0] for p in pts)
            y1 = min(p[1] for p in pts)
            x2 = max(p[0] for p in pts)
            y2 = max(p[1] for p in pts)

            color = (
                255
                if len(img.shape) == 2
                else (0, 255, 0, 255) if img.shape[2] == 4 else (0, 255, 0)
            )

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                img,
                text,
                (x1, max(y1 - 5, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

        h, w = img.shape[:2]
        plt.imshow(img)
        plt.xticks(
            np.linspace(0, w, 11),
            ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
        )
        plt.yticks(
            np.linspace(0, h, 11),
            ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
        )
        ax = plt.gca()
        ax.set_xticks(np.linspace(0, w, 51), minor=True)
        ax.set_yticks(np.linspace(0, h, 51), minor=True)
        plt.grid(
            True, which="major", color="white", linestyle="--", linewidth=0.8, alpha=0.6
        )
        plt.grid(
            True, which="minor", color="white", linestyle=":", linewidth=0.4, alpha=0.3
        )
        plt.show()
        wh.set_window_box()
        wh.set_bounds(
            top=args.top,
            left=args.left,
            width=args.width,
            height=args.height,
        )


if __name__ == "__main__":
    main()
