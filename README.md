# Introduction
`color_click.py` is a Python script designed to detect the presence of a specific color within a user-defined screen area. When the specified color is continuously present in the area for a certain duration, the program executes a random click operation within that area. This script can be utilized in various scenarios, such as automation testing, gaming assistance, and more.

## Installation Guide
To use this script, you need to install the following Python libraries:
- `pyautogui`
- `PIL` (Python Imaging Library)
- `keyboard`
- `tkinter` (usually installed with Python)

## Usage
1. **Start the Script**: 
   ```sh
   python color_click.py
2. Select Area: Press `alt+n` to activate the area selection mode, then drag the mouse to select an area on the screen.
3. Confirm Selection: After selecting the area, press enter to confirm.
4. Detection and Clicking: The program will monitor the selected area and detect the specified color. If the color is continuously present for more than the preset time, the program will randomly click within the area.
5. Exit the Program: You can exit the program at any time by pressing the `esc` key.
