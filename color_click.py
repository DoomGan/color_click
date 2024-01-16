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
    # 确保区域坐标按左上和右下的顺序
    selection = (
        min(start_x, event.x_root),
        min(start_y, event.y_root),
        max(start_x, event.x_root),
        max(start_y, event.y_root)
    )
    print("框选完成，区域：", selection)  # 输出框选区域
    try:
        root.after(100, root.quit)  # 在100毫秒后安排root.quit
        root.destroy()  # 销毁窗口
    except Exception as e:
        print(f"发生错误: {e}")

def on_activate():
    global root, canvas, selection_rectangle
    root = tk.Tk()
    root.attributes('-alpha', 0.3)  # 设置窗口透明度
    root.attributes('-fullscreen', True)  # 全屏
    root.attributes('-topmost', True)  # 置于顶层
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
    print(f"正在检查区域 {region} 中的颜色...")
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y)) == color:
                print("找到指定颜色！")
                return True
    print("未找到指定颜色。")
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
        if keyboard.is_pressed('esc'):  # 如果按下Esc键，则退出程序
            print("用户中断: 退出程序")
            break
        if find_color_in_region(color, region):
            if color_found_time is None:
                color_found_time = time.time()
                print(f"颜色首次被检测到，开始计时...")
            elif time.time() - color_found_time >= threshold_time:
                random_click_in_region(region)
                print(f"在区域 {region} 内的随机位置点击了鼠标")
                color_found_time = None
                delay = random_delay(0.5, 1.5)
                time.sleep(delay)
        else:
            if color_found_time is not None:
                print("颜色丢失，重置计时器。")
            color_found_time = None
        time.sleep(0.1)
def on_confirm():
    global root, selection
    if root:
        # 确认选择区域
        root.quit()
        root = None

def move_mouse_to_selection():
    if selection != (0, 0, 0, 0):
        # 计算框选区域内的随机点
        x = random.randint(selection[0], selection[2])
        y = random.randint(selection[1], selection[3])
        # 将鼠标移动到随机点
        pyautogui.moveTo(x, y)
keyboard.add_hotkey('alt+b', move_mouse_to_selection)
keyboard.add_hotkey('alt+n', on_activate)
keyboard.add_hotkey('enter', on_confirm)

print("程序运行中...按下 alt+N 来选择屏幕区域，按住 Esc 退出程序。")

# 设定要寻找的颜色
target_color = (255,216,107)  # 颜色值
color_threshold_time = 3  # 颜色连续存在的阈值时间（秒）
try:
    while True:
        try:
            if selection != (0, 0, 0, 0):
                print("检测到框选区域，开始进行颜色识别。")  # 确认框选区域后的输出
                # 使用selection变量进行颜色检测和点击操作
                click_if_color_found(target_color, selection, color_threshold_time)
                selection = (0, 0, 0, 0)  # 重置selection以等待下次激活
        except Exception as e:
            print(f"主循环中发生错误: {e}")
        
        if keyboard.is_pressed('esc'):
            print("退出程序")
            break
        time.sleep(0.1)
except Exception as e:
    print(f"主循环中发生错误: {e}")