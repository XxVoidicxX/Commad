import subprocess
import sys

# Helper function to check if a package is installed, and install if not
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    'colorama', 'psutil', 'requests', 'ping3'
]

# Install missing packages
for package in required_packages:
    install_package(package)

# Import after installation check
try:
    import platform
    import colorama
    import os
    import time
    import hashlib
    import shutil
    import socket
    import traceback
    import string
    import requests
    import random
    import psutil
    from datetime import datetime
    from ping3 import ping
except Exception as e:
    print("Error:", e)

# ==================================================
# Options
color = colorama.Fore
red = color.RED
white = color.WHITE
green = color.GREEN
reset = color.RESET
blue = color.BLUE
yellow = color.YELLOW
magenta = color.MAGENTA
cyan = color.CYAN

option_00 = 'Soon'
option_01 = 'Password Hasher'
option_02 = 'Password Maker'
option_03 = 'Password Un-Hasher'
option_04 = 'Cracker Internal Test'
option_05 = 'Pinger'

# Option functionality
option_00_txt = f"{white}[{red}00{white}]{cyan} " + option_00.ljust(26)[:26] + f"{reset}".replace("-", " ")
option_01_txt = f"{white}[{green}01{white}]{cyan} " + option_01.ljust(26)[:26] + f"{reset}".replace("-", " ")
option_02_txt = f"{white}[{green}02{white}]{cyan} " + option_02.ljust(26)[:26] + f"{reset}".replace("-", " ")
option_03_txt = f"{white}[{red}03{white}]{cyan} " + option_03.ljust(26)[:26] + f"{reset}".replace("-", " ")
option_04_txt = f"{white}[{green}04{white}]{cyan} " + option_04.ljust(26)[:26] + f"{reset}".replace("-", " ")
option_05_txt = f"{white}[{green}05{white}]{cyan} " + option_05.ljust(26)[:26] + f"{reset}".replace("-", " ")

authenticated = True  # Change this to False to see the other state
state_message = "Unlocked - [L] Lock?" if authenticated else "Locked - [L] Unlock?"
Debug = False

errors = []

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            errors.append((func.__name__, e, traceback.format_exc()))
            print(f"  └─ An error occurred in function '{func.__name__}':")
            print(e)
            input(''' ┌─ This error has been logged for debugging.
   └─ Enter to Continue...''')
            ToolApp.enter()  # Return to the main menu
    return wrapper

def view_errors():
    print("  ┌─ Logged Errors:")
    if errors:
        for index, (function_name, error, tb) in enumerate(errors, 1):
            print(f"{index}. Function: {function_name}")
            print(f"   Error: {error}")
            print(f"   └─ Traceback:\n{tb}")
    else:
        print("   └─ No errors logged.")

def apply_error_handler(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, error_handler(attr_value))
    return cls

@apply_error_handler
class ToolApp:
    def __init__(self):
        self.authenticated = True
        self.VERSION = "DEV-Version: 1.0.0"
        self.stored_hashed_password = "Null"
        self.second_stored_hashed_password = "Null"
        self.pc_name = socket.gethostname()
        self.current_directory = os.getcwd()
        self.start_time = datetime.now()
        self.banner = f'''{red}.... banner content ....'''
        self.menu_locked = f'''{red}.... menu locked content ....'''
        self.menu = f'''{white}.... menu content ....'''

    def startup(self):
        print(f"{self.banner}")
        self.print_slow(f"{commad_copyright}")
        time.sleep(0.5)
        input(" └─ Enter to Continue...")
        self.enter()

    def flash_print(self, *args):
        text = ' '.join(map(str, args))
        flash_font = '\033[5m'
        normal_font = '\033[0m'
        print(f"{flash_font}{text}{normal_font}")

    def print_slow(self, text, delay=0.0015):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def center_title(self, text):
        terminal_width = shutil.get_terminal_size().columns
        splitter_length = terminal_width - 2
        spaces = (splitter_length - len(text)) // 2
        centered_text = f"{'':{spaces}}{text}"
        return centered_text

    def enter(self):
        if authenticated:
            self.tool_menu()
            if Debug:
                print("[COMMAD Debug: Calling self.tool_menu()]")
        else:
            if Debug:
                print("[COMMAD Debug: Calling self.tool_menu_locked()]")
            self.tool_menu_locked()

    def failed_auth(self):
        if Debug:
            print("[COMMAD Debug: Called self.failed_auth()]")
        while True:
            self.clear_console()
            print(f"{self.banner}")
            print(f"{self.menu_locked}")
            choice = input(f"""{reset} ┌─[ PC:        >UNKNOWN<  \n ├─[ Directory: >NO ACCESS<  \n └──$ """).lower()
            if choice == 'unlock' or choice == 'l':
                break
            else:
                continue

    def tool_menu(self):
        if not self.authenticated:
            self.failed_auth()
            return

        self.clear_console()
        if Debug:
            print("[COMMAD Debug: Called self.tool_menu()]")
        print(f"{self.banner}")
        print(f"{self.menu}")
        choice = input(f""" ┌─[ PC:        >{self.pc_name}<  \n ├─[ Directory: >{self.current_directory}<  \n └──$ """).lower()

        if choice == 'c':
            self.tool_menu_terminal()
        elif choice == 'i':
            self.info_page()
        elif choice == 'r' or choice == 'restart':
            self.enter()
        elif choice == '01' or choice == '1':
            self.password_hasher_main()
        elif choice == '02' or choice == '2':
            self.password_maker()
        elif choice == '04' or choice == '4':
            self.password_cracker_main()
        elif choice == '05' or choice == '5':
            self.tool_menu_networking_ip_pinger()
        else:
            self.error_input()

    def error_input(self):
        print(''' ┌─ COMMAD Didn't understand that input
 │
 └─ Reloading...''')
        time.sleep(3)
        self.tool_menu()

    @staticmethod
    def clear_console():
        os.system('clear')  # Clear terminal
        print("\033[3J\033[H\033[2J", end='')  # Clear scrollback buffer and move cursor to top

if __name__ == "__main__":
    ToolApp = ToolApp()
    ToolApp.startup()
