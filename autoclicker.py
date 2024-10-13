import threading
import time
import tkinter as tk
import json
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode
from tkinter import messagebox

# Initialize mouse controller
mouse = MouseController()

# Global variables for keybinds and state
left_clicking = False
right_clicking = False
left_click_key = KeyCode(char='a')
right_click_key = KeyCode(char='s')
sleep_time = 0.1;
settings_file = 'autoclicker_settings.json'  # JSON file to store settings

# Autoclicker functions
def left_clicker():
    while left_clicking:
        mouse.click(Button.left, 1)
        time.sleep(sleep_time)

def right_clicker():
    while right_clicking:
        mouse.click(Button.right, 1)
        time.sleep(sleep_time)

# Listener for keyboard events
def on_press(key):
    global left_clicking, right_clicking
    
    if key == left_click_key:
        left_clicking = not left_clicking
        if left_clicking:
            threading.Thread(target=left_clicker).start()

    elif key == right_click_key:
        right_clicking = not right_clicking
        if right_clicking:
            threading.Thread(target=right_clicker).start()

# Function to save settings to a JSON file
def save_settings():
    settings = {
        'left_click_key': left_click_key.char,
        'right_click_key': right_click_key.char,
        'sleep_time': sleep_time
    }
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

# Function to load settings from the JSON file
def load_settings():
    global left_click_key, right_click_key, sleep_time
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            left_click_key = KeyCode(char=settings['left_click_key'])
            right_click_key = KeyCode(char=settings['right_click_key'])
            sleep_time = float(settings['sleep_time'])
    except FileNotFoundError:
        print("Settings file not found, using default settings.")

# GUI for setting keybinds and sleep time
class AutoclickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker Settings")
        
        # Load settings from file
        load_settings()
        self.listener = Listener(on_press=on_press)
        self.listener.start()
        # Keybind settings
        tk.Label(root, text="Left Click Key:").grid(row=0, column=0, padx=10, pady=10)
        self.left_click_entry = tk.Entry(root)
        self.left_click_entry.grid(row=0, column=1, padx=10, pady=10)
        self.left_click_entry.insert(0, left_click_key.char)  # Load from settings
        
        tk.Label(root, text="Right Click Key:").grid(row=1, column=0, padx=10, pady=10)
        self.right_click_entry = tk.Entry(root)
        self.right_click_entry.grid(row=1, column=1, padx=10, pady=10)
        self.right_click_entry.insert(0, right_click_key.char)  # Load from settings
        
        # Sleep time setting
        tk.Label(root, text="Click Interval (seconds):").grid(row=3, column=0, padx=10, pady=10)
        self.sleep_time_entry = tk.Entry(root)
        self.sleep_time_entry.grid(row=3, column=1, padx=10, pady=10)
        self.sleep_time_entry.insert(0, str(sleep_time))  # Load from settings
        
        # Control buttons
        self.apply_button = tk.Button(root, text="Apply Settings", command=self.apply_settings)
        self.apply_button.grid(row=4, column=0, padx=10, pady=10)

    def apply_settings(self):
        global left_click_key, right_click_key, sleep_time
        
        left_key = self.left_click_entry.get()
        right_key = self.right_click_entry.get()
        interval = self.sleep_time_entry.get()

        if len(left_key) != 1 or len(right_key) != 1:
            messagebox.showerror("Error", "Keybinds must be a single character.")
            return

        try:
            sleep_time = float(interval)
        except ValueError:
            messagebox.showerror("Error", "Interval must be a valid number.")
            return

        left_click_key = KeyCode(char=left_key)
        right_click_key = KeyCode(char=right_key)
        save_settings()  # Save settings after applying
        messagebox.showinfo("Info", "Settings applied successfully.")


# Start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = AutoclickerGUI(root)
    root.mainloop()
