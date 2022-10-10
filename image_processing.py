import cv2
import numpy as np


def remove_bg(file):
    src = cv2.imread(f'uploaded/{file}', 1)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    mask = 255 - mask
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=1, sigmaY=1, borderType = cv2.BORDER_DEFAULT)
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)

    result = src.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    name = file.split('.')[0]
    cv2.imwrite(f"converted/bg_{name}.png", result)
