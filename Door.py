import pyautogui
import time
from pynput.keyboard import Controller
from PIL import Image
import numpy as np
import pytesseract
import threading

keyboard = Controller()

# Detection

color1 = (255, 1, 0)
color2 = (65, 165, 146)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def check_color_overlap(image):
    image_array = np.array(image)
    
    mask1 = (image_array[:, :, 0] == color1[0]) & (image_array[:, :, 1] == color1[1]) & (image_array[:, :, 2] == color1[2])
    
    mask2 = (image_array[:, :, 0] == color2[0]) & (image_array[:, :, 1] == color2[1]) & (image_array[:, :, 2] == color2[2])

    overlap = np.any(mask1 & mask2)
    return overlap

def detect_letter(image):
    text = pytesseract.image_to_string(image)
    for char in text:
        if char.lower() in ['w', 'a', 's', 'd']:
            return char.lower()
        return None
    
def main_loop():
    while True:
        screenshot = pyautogui.screenshot()
        if check_color_overlap(screenshot):
            key = detect_letter(screenshot)
            if key:
                press_key(key)

def main():
    thread = threading.Thread(target=main_loop)
    thread.start()
    thread.join()

if __name__ == "__main__":
    main()
