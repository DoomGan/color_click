import pyautogui
from PIL import ImageGrab
import time
import keyboard
import random
import tkinter as tk

selection = (0, 0, 0, 0)
root = None
start_x, start_y = 0, 0

def on_drag(event):
    global canvas, selection_rectangle, start_x, start_y
    canvas.coords(selection_rectangle, start_x, start_y, event.x_root, event.y_root)

def on_release(event):
    global selection, root
    selection = (
        min(start_x, event.x_root),
        min(start_y, event.y_root),
        max(start_x, event.x_root),
        max(start_y, event.y_root)
    )
    print("Selection completed, area:", selection)
    try:
        root.after(100, root.quit)
        root.destroy()
    except Exception as e:
        print(f"Error occurred: {e}")

def on_activate():
    global root, canvas, selection_rectangle
    root = tk.Tk()
    root.attributes('-alpha', 0.3)
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    canvas = tk.Canvas(root, cursor='cross')
    canvas.pack(fill=tk.BOTH, expand=True)
    selection_rectangle = canvas.create_rectangle(0, 0, 0, 0, outline='red', width=2)
    
    canvas.bind('<Button-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    
    root.mainloop()

def on_press(event):
    global start_x, start_y
    start_x, start_y = event.x_root, event.y_root

def find_color_in_region(color, region):
    screenshot = ImageGrab.grab(region)
    print(f"Checking color in region {region}...")
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y)) == color:
                print("Color found!")
                return True
    print("Color not found.")
    return False

def random_delay(min_seconds, max_seconds):
    return random.uniform(min_seconds, max_seconds)

def random_click_in_region(region):
    x = random.randint(region[0], region[2])
    y = random.randint(region[1], region[3])
    pyautogui.click(x, y)

def click_if_color_found(color, region, threshold_time):
    color_found_time = None
    while True:
        if keyboard.is_pressed('esc'):
            print("User interruption: Exiting program")
            break
        if find_color_in_region(color, region):
            if color_found_time is None:
                color_found_time = time.time()
                print(f"Color detected for the first time, starting timer...")
            elif time.time() - color_found_time >= threshold_time:
                random_click_in_region(region)
                print(f"Clicked mouse at random position in region {region}")
                color_found_time = None
                delay = random_delay(0.5, 1.5)
                time.sleep(delay)
        else:
            if color_found_time is not None:
                print("Color lost, resetting timer.")
            color_found_time = None
        time.sleep(0.1)

def on_confirm():
    global root, selection
    if root:
        root.quit()
        root = None

def move_mouse_to_selection():
    if selection != (0, 0, 0, 0):
        x = random.randint(selection[0], selection[2])
        y = random.randint(selection[1], selection[3])
        pyautogui.moveTo(x, y)

keyboard.add_hotkey('alt+b', move_mouse_to_selection)
keyboard.add_hotkey('alt+n', on_activate)
keyboard.add_hotkey('enter', on_confirm)

print("Program running... Press alt+N to select screen region, hold Esc to exit.")

target_color = (255, 216, 107)
color_threshold_time = 3
try:
    while True:
        try:
            if selection != (0, 0, 0, 0):
                print("Selection detected, starting color recognition.")
                click_if_color_found(target_color, selection, color_threshold_time)
                selection = (0, 0, 0, 0)
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        if keyboard.is_pressed('esc'):
            print("Exiting program")
            break
        time.sleep(0.1)
except Exception as e:
    print(f"Error in main loop: {e}")