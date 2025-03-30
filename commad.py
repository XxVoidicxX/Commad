commad_copyright = '''
© COMMAD™. All rights reserved.

This code is the property of COMMAD™. Unauthorized copying, distribution, or modification of this code,
in whole or in part, without express written permission from the owner, is strictly prohibited.

This code is provided "as is," without warranty of any kind, express or implied, including but not limited to
the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall
the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action
of contract, tort, or otherwise, arising from, out of, or in connection with the code or the use or other
dealings in the code.

This program is intended solely for authorized personnel. Unauthorized access, distribution, or use of this
program is strictly prohibited. Illegally obtaining or attempting to access this program is a violation of
copyright and will result in the program being locked to unauthorized users.
'''

try:
    import platform
    import colorama
    import os
    import time
    import subprocess
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
    print(" Error:", e)

# ==================================================
# Options

#Colours
color = colorama.Fore
red = color.RED
white = color.WHITE
green = color.GREEN
reset = color.RESET
blue = color.BLUE
yellow = color.YELLOW
magenta = color.MAGENTA
cyan = color.CYAN

# Options
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

# Define the global boolean variable
authenticated = True  # Change this to False to see the other state

# Output the state
state_message = "Unlocked - [L] Lock?" if authenticated else "Locked - [L] Unlock?"

Debug = False

# ==================================================
# Error Catcher

errors = []

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            errors.append((func.__name__, e, traceback.format_exc()))
            print("  └─ An error occurred in function '{}':".format(func.__name__))
            print(e)
            input('''
   ┌─ This error has been logged for debugging.
   └─ Enter to Continue...''')
            ToolApp.enter()  # Return to the main menu
    return wrapper


def view_errors():
    print("  ┌─ Logged Errors:")
    if errors:
        for index, (function_name, error, tb) in enumerate(errors, 1):
            print("{}. Function: {}".format(index, function_name))
            print("   Error: {}".format(error))
            print("   └─ Traceback:\n{}".format(traceback))
            pass
    else:
        print("   └─ No errors logged.")

def apply_error_handler(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, error_handler(attr_value))
    return cls

# ==================================================

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

        self.banner = f'''{red}


                                                         ▄████▄   ▒█████   ███▄ ▄███▓ ███▄ ▄███▓ ▄▄▄      ▓█████▄
                                                        ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▒████▄    ▒██▀ ██▌
                                                        ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▓██    ▓██░▒██  ▀█▄  ░██   █▌
                                                        ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██    ▒██ ░██▄▄▄▄██ ░▓█▄   ▌
                                                        ▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒▒██▒   ░██▒ ▓█   ▓██▒░▒████▓
                                                        ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒▒▓  ▒
                                                          ░  ▒     ░ ▒ ▒░ ░  ░      ░░  ░      ░  ▒   ▒▒ ░ ░ ▒  ▒
                                                        ░        ░ ░ ░ ▒  ░      ░   ░      ░     ░   ▒    ░ ░  ░
                                                {green}
                                                COMMAD - Centralized Operations Management and Command Application Dashboard{white}'''
        self.menu_locked = f'''{red}
     ┌─ >COMMAD MENU<
     │
     ├─ State: {state_message}
     ├─ Version: DENIED                                                                                                                      [X] NO ACCESS ─┐
     ├─ [X] Null                                                                                                                             [X] NO ACCESS ─┤
     └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    '''
        self.menu = f'''{white}
     ┌─ >COMMAD MENU<
     │
     ├─ State: {state_message}
     ├─ Version: DEV-Version-1.0.0                                                                                                     [C] Console ─┐
     ├─ [I] Info ┌───────────┐                     ┌────────────┐                    ┌───────────────────┐             ┌───────┐       [R] Restart ─┤
     └──────────┬┤ Utilities ├────────────────────┬┤ Networking ├───────────────────┬┤ System Management ├────────────┬┤ Other ├────────────────────┘
                │└───────────┘                    │└────────────┘                   │└───────────────────┘            │└───────┘
                ├─ {option_01_txt                }├─ {option_05_txt                }├─ {option_00_txt                }├─ {option_00_txt                }
                ├─ {option_02_txt                }├─ {option_00_txt                }├─ {option_00_txt                }├─ {option_00_txt                }
                ├─ {option_03_txt                }└─ {option_00_txt                }└─ {option_00_txt                }└─ {option_00_txt                }
                └─ {option_04_txt                }
    '''

    def startup(self):
        print(f"{self.banner}")
        self.print_slow(f"{commad_copyright}")
        time.sleep(.5)
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

    #self.terminal_title = " -- == { U-T Terminal } == -- "
    #splitter_length = shutil.get_terminal_size().columns - 2
    #splitters = "=" * splitter_length

    #print(f" {splitters}")
    #print(f" {self.center_title(self.title)}")
    #print(f" {self.center_title(self.VERSION)}")
    #print(f" {splitters}")


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

        clear_console()
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
        elif choice== 'update':
            print(' Update feature removed...')
            time.sleep(2)
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
        print('''
 ┌─ COMMAD Didn't understand that input
 │
 └─ Reloading...
        ''')
        time.sleep(3)
        self.tool_menu()


# ==================================================
# Terminal

    def tool_menu_terminal(self):
        clear_console()
        print(f"{self.banner}")
        print('''
     ┌─ >COMMAD COMMAND CONSOLE<
     │
     ├─ Version: DEV-Version-1.0.0
     │                                                                                                                                              [Exit] ─┐
     │  [Help]                                                                                                                                              │
     └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ''')
        print()
        while True:
            try:
                print()
                command = input(f""" ┌─[ PC:        >{self.pc_name}<  \n ├─[ Directory: >{self.current_directory}< \n └──$ """)
                if command.lower() == "exit":
                    self.enter()
                elif command.lower() == "help":
                    print(" ┌─ This is a simple terminal built within COMMAD: you can execute commands, NOTE: no security measures attached... ")
                    print(" ├─ Custom commands include: 'help', 'help (command)'(doesn't work), 'restart terminal', 'clear screen'")
                    print(" ├─ Use 'help_list' for command lists")
                    print(" └─ And 'exit' to leave.")
                elif command.lower() == "all_commands":
                    print(dir(os))
                elif command.lower().startswith("help "):
                    command_name = command.split(" ")[1]
                    if hasattr(os, command_name):
                        help(getattr("   >", os, command_name))
                elif command.lower() == "restart terminal":
                    self.tool_menu_terminal()
                elif command.lower() == "clear screen":
                    os.system("clear")
                    print(f"{self.banner}")
                    print('''
     ┌─ >COMMAD COMMAND CONSOLE<
     │
     ├─ Version: DEV-Version-1.0.0
     │                                                                                                                                              [Exit] ─┐
     │  [Help]                                                                                                                                              │
     └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ''')
                    print()
                elif command.lower().startswith("abilities "):
                    directory_path = command.split(" ")[1]
                    if os.path.isdir(directory_path):
                        file_commands = [cmd for cmd in dir(os) if callable(getattr(os, cmd)) and not cmd.startswith("_")]
                        print("   {Available file commands to run on target: ")
                        for cmd in file_commands:
                            print(f"   - {cmd}")
                        else:
                            print("   { Invalid Directory Path...")
                elif command.lower() == "help_list":
                    print("   { Command list to use: ")
                    print("    ")
                    print("   { 'all_commands' - Prints all available commands from the os ")
                    print("   { 'sys_commands' - Prints popular commands related to system")
                    print("   { 'text_commands' - Prints popular commands related to text manipulation")
                    print("   { 'file_commands' - Prints popular commands more related to files themselves")
                    print("   { 'process_commands' - Prints commands related to process management")
                    print("   { 'network_commands' - Prints commands related to networking")
                elif command.lower() == "file_commands":
                    print("   { File Commands: ")
                    print("    ")
                    print("   { 'ls' (list everything in directory) ")
                    print("   { 'cd' (Change Directory) ")
                    print("   { 'mkdir' (Make Directory) ")
                    print("   { 'rm' (Remove Directory) ")
                    print("   { 'cp' (Copy) ")
                    print("   { 'mv' (Move) ")
                    print("   { 'pwd' (Print working directory) ")
                    print("   { 'touch' (Create empty file or update access and mod times of a file) ")
                    print("   { 'chmod' (Change mode) ")
                    print("   { 'chown' (Change Owner) ")
                elif command.lower() == "text_commands":
                    print("   { Text Commands: ")
                    print("    ")
                    print("   { 'cat' (concatenate - display contents of a file) ")
                    print("   { 'grep' (Global regular expression print - search for patterns in files) ")
                    print("   { 'sed' (Stream Editor - for transforming text) ")
                    print("   { 'awk' (Text processing tool for pattern scanning and processing) ")
                elif command.lower() == "sys_commands":
                    print("   { System Commands: ")
                    print("    ")
                    print("   { 'shutdown' (Shutdown the system) ")
                    print("   { 'reboot' (Reboot the system) ")
                    print("   { 'poweroff' (Power off the system) ")
                    print("   { 'date' (Display or set the system date and time) ")
                    print("   { 'uptime' (Show how long the system has been running) ")
                    print("   { 'hostname' (Display or set the system's hostname) ")
                    print("   { 'who' (Display info about currently logged-in users) ")
                    print("   { 'w' (Show who's logged on & what they're doing) ")
                    print("   { 'last' Show a list of last logged-in users ")
                    print("   { 'uname' (Print system, kernel, hardware, processer info) ")
                    print("   { 'dmesg' (Display kernel ring buffer messages) ")
                    print("   { 'free' (Display amount of free and used memory in system) ")
                    print("   { 'df' (Display disk space usage for filesystems) ")
                    print("   { 'mount' (Mount a filesystem) ")
                    print("   { 'unmount' (Unmount a filesystem) ")
                    print("   { 'ps' (Display info about active processes) ")
                    print("   { 'kill' (Terminate processes by process ID (PID) or name) ")
                    print("   { 'top' (Display system summary info and list of processes) ")
                    print("   { 'nice' (Run a command with modified scheduling priority) ")
                    print("   { 'renice' (Alter the priority of running processes) ")
                elif command.lower() == "process_commands":
                    print("   { Process Commands: ")
                    print("    ")
                    print("   { 'ps' (Display info about active processes) ")
                    print("   { 'top' (Display system summary info and list of processes) ")
                    print("   { 'kill' (Terminate processes by process ID (PID) or name) ")
                    print("   { 'killall' (Terminate processes by name) ")
                    print("   { 'pgrep' (List processes based on name or other attributes) ")
                    print("   { 'pkill' (Send signals to processes based on name or other attributes) ")
                    print("   { 'nice' (Run a command with modified scheduling priority) ")
                    print("   { 'jobs' (Display status of jobs in the background) ")
                    print("   { 'bg' (Put a job in the background) ")
                    print("   { 'fg' (Bring a job to the foreground) ")
                elif command.lower() == "network_commands":
                    print("   { Network Commands: ")
                    print("    ")
                    print("   { 'ping' (Send ICMP echo requests to a host to test network connectivity) ")
                    print("   { 'traceroute' (DIsplay the rought packets take to reach a destination host, or 'tracert' for windows) ")
                    print("   { 'netstat' (Display network connections, routing tables, interface stats, masquerade connections, and multicast memberships) ")
                    print("   { 'ifconfig' (or 'ipconfig' on Windows - Configure network interfaces and display network interface configuration) ")
                    print("   { 'iwconfig' (Display wireless network interface configuration) ")
                    print("   { 'route' (Display or manipulate the IP routing table) ")
                    print("   { 'arp' (Display or manipulate the ARP cache) ")
                    print("   { 'host' (DNS lookup utility to query DNS servers for information about hosts and domains) ")
                    print("   { 'dig' (DNS lookup utility for querying DNS servers for DNS information) ")
                    print("   { 'nslookup' (DNS lookup utility to query DNS servers for domain name resolution) ")
                else:
                    result = os.system(command)
                    if result == 0:
                        print("   { Command ran succesfully")
                    elif result != 0:
                        print("   { Command not found. ")
                    else:
                        print("   { Command Error:", result)
            except Exception as e:
                print("   { An error occurred:", e)
                time.sleep(5)

    def get_system_stats(self):
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Memory usage
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.used // (1024 * 1024)  # Convert to MB
        total_memory = memory_info.total // (1024 * 1024)  # Convert to MB

        # Disk usage
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent

        # Uptime
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds

        # Active connections
        active_connections = len(psutil.net_connections())

        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "total_memory": total_memory,
            "disk_usage": disk_usage,
            "uptime": uptime_str,
            "active_connections": active_connections
        }

# ==================================================
# Secton: Info Page

    def info_page(self):
        clear_console()
        stats = self.get_system_stats()
        info_page = f'''
     ┌─ >COMMAD INFO CONSOLE<
     │
     ├─ State: {state_message}
     ├─ Version: DEV-Version-1.0.0                                                                                                                      [Exit] ─┐
     │           ┌─────────────┐                                                                                                                                │
     └──────────┬┤ SYSTEM Info ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                │└─────────────┘
                ├─ CPU Usage: {stats['cpu_usage']}%
                ├─ Memory Usage: {stats['memory_usage']}MB used / {stats['total_memory']}MB total
                ├─ GPU Usage: ERROR
                ├─ Disk Usage: {stats['disk_usage']}%

     ┌─ >COMMAD CONSOLE<
     │
     ├─ System Information
     ├─ Version: DEV-Version-1.0.0

     ├─ Console Uptime: {stats['uptime']}
     ├─ Active Connections: {stats['active_connections']}
    '''
        print(info_page)
        choice = input(''' ''')
        if choice == 'back' or choice == 'b':
            self.enter()

# ==================================================
# Secton: Pinger

    def tool_menu_networking_ip_pinger(self):
        if not self.authenticated:
            self.failed_auth()
            return

        print()
        time.sleep(0.5)
        print(" [ COMMAND PINGER: Enter an IP address or domain name to ping ")
        print(" [ COMMAND: This checks if an IP network or domain is running")
        host = input(" IP or Domain { ")

        # Use ping_host method to check if host is reachable and get packet loss
        is_up, packet_loss = self.ping_host(host)

        if is_up:
            print(f'''
 ┌─ [ COMMAND: {host} has been pinged!
 │
 └─ [ Packet loss: {packet_loss:.2f}%
            ''')
        else:
            print(f'''
 ┌─ [ COMMAND: {host} not pinged!
 └─ [ Host is not running, online, or just undetected
            ''')

        time.sleep(1)
        print(" [ COMMAND PINGER: Again? (y/n)")
        choice = input('''
  ┌─ COMMAND Pinger
  │
  └─ $ ''').lower()

        # Re-run the menu or exit based on user input
        if choice == "y" or choice == "yes":
            self.tool_menu_networking_ip_pinger()
        elif choice == "n" or choice == "no":
            self.enter()
        else:
            self.tool_menu_networking_ip_pinger()

    def ping_host(self, host, count=4):
        try:
            # Resolve the host to an IP address
            ip_address = socket.gethostbyname(host)

            # Try pinging with ping3 first
            successful_pings = 0
            for _ in range(count):
                response_time = ping(ip_address)
                if response_time is not None:
                    successful_pings += 1
                time.sleep(0.5)  # Brief delay between pings

            # Calculate packet loss if ping3 worked
            if successful_pings > 0:
                packet_loss = ((count - successful_pings) / count) * 100
                return True, packet_loss

            # If ping3 fails, try using system ping as fallback
            else:
                if platform.system().lower() == "windows":
                    command = ["ping", "-n", str(count), ip_address]
                else:
                    command = ["ping", "-c", str(count), ip_address]

                output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if output.returncode == 0:
                    # On success, calculate packet loss by parsing output
                    output_text = output.stdout.decode()
                    loss_str = "Lost = " if platform.system().lower() == "windows" else "received,"
                    lost_packets = int(output_text.split(loss_str)[-1].split(",")[0].strip().split(" ")[0])
                    packet_loss = (lost_packets / count) * 100
                    return True, packet_loss
                else:
                    return False, 100.0

        except (socket.gaierror, Exception) as e:
            print("    Error:", e)
            # Handle exceptions for invalid hosts or other errors
            return False, 100.0  # Assume 100% packet loss if the host cannot be reached


# ==================================================
# Secton: Password Cracker

    # Global variable to store the password
    password = ""

    def set_password(self):
        """
        Function to set the password dynamically.
        """
        global password
        password = input("Set the password: ")
        print("Password set successfully!")

    def check_password(self, user_input):
        """
        Function to check if the user input matches the password.
        """
        if user_input == password:
            return True
        else:
            return False

    def automated_guess(self):
        """
        Function to automate the password guessing process using a password list.
        """
        password_list = []

        # Read passwords from a file
        with open("passwords.txt", "r") as file:
            password_list = file.readlines()

        crack_attempt_count = 0
        for password_attempt in password_list:
            crack_attempt_count += 1
            password_attempt = password_attempt.strip()
            if self.check_password(password_attempt):
                print(f" └─ Cracking successful! Password is: {password_attempt}")
                return crack_attempt_count
            print(f" └─ Cracking, Attempted: {password_attempt}")
        print(" └─ Cracking failed...")
        return crack_attempt_count

    def password_cracker_main(self):
        """
        Main function to handle user input and start the password checking or cracking process.
        """
        global password
        # Prompt user to set the password
        self.set_password()

        while True:
            user_input = input(" └─ Password: ")
            if user_input.lower() == "crack_password":
                print(" Initiating cracking process...")
                time.sleep(2)
                attempts = self.automated_guess()
                print(f" Total cracking attempts: {attempts}")
                break
            if self.check_password(user_input):
                print(" Correct!")
                break
            else:
                print(" Incorrect! Try again...")
                time.sleep(1)

# ==================================================
# Secton: Passwork Maker Functionality

    def get_random_word(self):
        response = requests.get("https://random-word-api.herokuapp.com/word")
        word = response.json()[0]
        return word

    def replace_with_number(self, word):
        replaced_word = ""
        for char in word:
            if char.lower() == 'o':
                replaced_word += '0'
            elif char.lower() == 'l':
                replaced_word += '1'
            elif char.lower() == 'e':
                replaced_word += '3'
            elif char.lower() == 'a':
                replaced_word += '4'
            elif char.lower() == 's':
                replaced_word += '$'
            else:
                replaced_word += char
        return replaced_word

    def capitalize_random(self, word):
        for _ in range(len(word) // 2):
            index_to_capitalize = random.randint(0, len(word) - 1)
            word = word[:index_to_capitalize] + word[index_to_capitalize].upper() + word[index_to_capitalize + 1:]
        return word

    def generate_customizable_password(self, length, use_keywords=True, include_numbers=True, random_capitalization=True):
        keyword = ""
        while len(keyword) < length:
            keyword += self.get_random_word()
        keyword = keyword[:length]

        if include_numbers:
            keyword = self.replace_with_number(keyword)

        random_word = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        password = self.replace_with_number(random_word)

        if random_capitalization:
            password = self.capitalize_random(password)

        password = password.replace(password[:len(keyword)], keyword)

        if random_capitalization:
            password = self.capitalize_random(password)

        if include_numbers:
            password += ''.join(random.choice(string.digits) for _ in range(4))

        self.last_passwords.append(password)

        return password

    def generate_impossible_password(self):
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation.replace('!', '')) for _ in range(30))
        self.last_passwords.append(password)
        return password

    def generate_ultimate_password(self):
        password_length = random.randint(30, 50)
        keywords_count = random.randint(1, 3)
        password = ""
        for _ in range(keywords_count):
            password += self.generate_customizable_password(password_length // keywords_count, use_keywords=True, include_numbers=True, random_capitalization=True)
        self.last_passwords.append(password)
        return password

# ==================================================
# Secton: Password Maker

    def password_maker(self):
        global changes_made
        self.unlocked_ultimate = False
        self.last_passwords = []
        while True:
            clear_console()
            print(f"{self.banner}")
            print('''
    ┌─ COMMAD Password Maker
    │
    ├─ Choose an option below
    │
    └─ [Back]

     ┌─ [01] Customizable Password
     └─ [02] Impossible Password
     ''')
            if self.last_passwords:
                print("   └─ [03] Show Last Password")
            if self.unlocked_ultimate:
                print("   └─ [04] Ultimate Password Generator")
            option = input(''' ┌─ [ Directory: >COMMAD\PASSWORD_MAKER< \n │ \n └─ $ ''').lower()

            if option == '1':
                while True:
                    print()
                    length_input = input(" └─ How many digits would you like your password to be? ")
                    if length_input.lower() == "back":
                        break
                    try:
                        length = int(length_input)
                        break
                    except ValueError:
                        print(" └─ Please enter a valid number.")

                if length_input.lower() == "back":
                    continue

                while True:
                    print()
                    use_keywords = input("  └─ Would you like keywords? (y/n): ").lower()
                    if use_keywords in ['y', 'n']:
                        use_keywords = use_keywords == 'y'
                        break
                    else:
                        print("  └─ Please answer the question with 'y' or 'n'.")

                while True:
                    print()
                    include_numbers = input("  └─ Would you like numbers? (y/n): ").lower()
                    if include_numbers in ['y', 'n']:
                        include_numbers = include_numbers == 'y'
                        break
                    else:
                        print(" └─ Please answer the question with 'y' or 'n'.")

                while True:
                    print()
                    random_capitalization = input("  └─ Would you like random capitalization? (y/n): ").lower()
                    if random_capitalization in ['y', 'n']:
                        random_capitalization = random_capitalization == 'y'
                        break
                    else:
                        print("  └─ Please answer the question with 'y' or 'n'.")

                self.password = self.generate_customizable_password(length, use_keywords, include_numbers, random_capitalization)
                print()
                print("   └─ Your generated password is:", self.password)
                print()
                input("   └─ Press Enter to continue...")

            elif option == '2':
                self.password = self.generate_impossible_password()
                print()
                print("  └─ Your generated password is:", self.password)
                print()
                input("  └─ Press Enter to continue...")

            elif option == '3' and self.last_passwords:
                print()
                print("  └─ Last password generated:", self.last_passwords[-1])
                print()
                input("  └─ Press Enter to continue...")

            elif option == '4' and self.unlocked_ultimate:
                self.password = self.generate_ultimate_password()
                print()
                print("  └─ Your generated ultimate password is:", self.password)
                print()
                input("  └─ Press Enter to continue...")

            elif option == 'back':
                print()
                print(" └─ Exiting...")
                time.sleep(3)
                self.enter()
                break

            elif option.lower() == 'password':
                self.unlocked_ultimate = True
                print("   └─ Congratulations! You've unlocked the Ultimate Password Generator!")
                input("   └─ Press Enter to continue...")


            else:
                print(" └─ Invalid option. Please choose a valid option.")
                input(" └─ Press Enter to continue...")

# ==================================================
# Secton: Password Hasher

    # Define hashing functions
    def hash_md5(self, input_string):
        """Hash using MD5."""
        return hashlib.md5(input_string.encode()).hexdigest()

    def hash_sha1(self, input_string):
        """Hash using SHA-1."""
        return hashlib.sha1(input_string.encode()).hexdigest()

    def hash_sha256(self, input_string):
        """Hash using SHA-256."""
        return hashlib.sha256(input_string.encode()).hexdigest()

    def hash_sha512(self, input_string):
        """Hash using SHA-512."""
        return hashlib.sha512(input_string.encode()).hexdigest()

    def hash_blake2b(self, input_string):
        """Hash using BLAKE2b."""
        return hashlib.blake2b(input_string.encode()).hexdigest()

    def hash_blake2s(self, input_string):
        """Hash using BLAKE2s."""
        return hashlib.blake2s(input_string.encode()).hexdigest()

    def get_salted_password_hash(self, password, salt):
        """Hash the password with a salt."""
        salted_password = password + salt
        return {
            'MD5': self.hash_md5(salted_password),
            'SHA-1': self.hash_sha1(salted_password),
            'SHA-256': self.hash_sha256(salted_password),
            'SHA-512': self.hash_sha512(salted_password),
            'BLAKE2b': self.hash_blake2b(salted_password),
            'BLAKE2s': self.hash_blake2s(salted_password)
        }

    def display_menu(self):
        """Display the password hasher menu."""
        clear_console()
        print(f"{self.banner}")
        print(f"{self.menu_password_hasher}")

    def handle_user_choice(self, choice, password):
        """Handle the user's choice and display hashed results."""
        salt = os.urandom(16).hex()  # Generate a random salt
        hashes = None

        if choice == '01' or choice == '1':
            hashes = {'MD5': self.hash_md5(password)}
        elif choice == '02' or choice == '2':
            hashes = {'SHA-1': self.hash_sha1(password)}
        elif choice == '03' or choice == '3':
            hashes = {'SHA-256': self.hash_sha256(password)}
        elif choice == '04' or choice == '4':
            hashes = {'SHA-512': self.hash_sha512(password)}
        elif choice == '05' or choice == '5':
            hashes = {'BLAKE2b': self.hash_blake2b(password)}
        elif choice == '06' or choice == '6':
            hashes = {'BLAKE2s': self.hash_blake2s(password)}
        elif choice == '07' or choice == '7':
            hashes = self.get_salted_password_hash(password, salt)
            print(f"\n └─ Salt: {salt}")
        else:
            print(" └─ Invalid choice. Please select a valid option.")
            return

        print("\n └─ Password Hashes: ")
        for algo, hashed in hashes.items():
            print(f"{algo}: {hashed}")

    menu_password_hasher = '''
 ┌─ >COMMAD MENU\PASSWORD HASHER<
 │
 │                                                                                                                                              [Back] ─┐
 │              ┌─────────────────┐                                                                                                          [Refresh]  │
 └─────────────┬┤ Hashing Options ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
               │└─────────────────┘
               ├─ [01] MD5
               ├─ [02] SHA-1
               ├─ [03] SHA-256
               ├─ [04] SHA-512
               ├─ [05] BLAKE2b
               ├─ [06] BLAKE2s
               └─ [07] All (with Salt)
'''

# Main function to handle user interaction
    def password_hasher_main(self):
        self.display_menu()
        while True:
            choice = input(" ┌─ Select an option \n │ \n └──$ ").strip()
            if choice == 'Back':  # Implement how to handle the back option if needed
                self.enter()
                break
            elif choice == 'refresh':
                self.display_menu()
            password = input(" ┌─ Enter your password \n │ \n └──$ ")
            self.handle_user_choice(choice, password)

# ==================================================
# Secton: Class Start

@staticmethod
def clear_console():
    os.system('clear')  # Clear terminal
    print("\033[3J\033[H\033[2J", end='')  # Clear scrollback buffer and move cursor to top

if __name__ == "__main__":
    ToolApp = ToolApp()
    ToolApp.startup()
