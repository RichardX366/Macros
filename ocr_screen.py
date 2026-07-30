from argparse import ArgumentParser
import os
import sys
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

from helpers import WindowHelper


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

    try:
        reader = easyocr.Reader(["en"], gpu=True)
    except Exception:
        reader = easyocr.Reader(["en"], gpu=False)

    while True:
        img = np.array(wh.screenshot())

        results = reader.readtext(image=img)
        # results = wh.clump_ocr(results)

        for box, text, confidence in results:
            # box is 4 points: top-left, top-right, bottom-right, bottom-left
            pts = [(int(x), int(y)) for x, y in box]
            x1 = min(p[0] for p in pts)
            y1 = min(p[1] for p in pts)
            x2 = max(p[0] for p in pts)
            y2 = max(p[1] for p in pts)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img,
                text,
                (x1, max(y1 - 5, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
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
        plt.show()


if __name__ == "__main__":
    main()
