import os
import sys
from difflib import get_close_matches

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Prompt the user for their name, device name, and sudo password
    user_name = input(f"{Colors.OKBLUE}Enter your name: {Colors.ENDC}").strip()
    device_name = input(f"{Colors.OKBLUE}Enter your device name: {Colors.ENDC}").strip()
    sudo_password = input(f"{Colors.OKBLUE}Set your sudo password: {Colors.ENDC}").strip()

    clear_screen()
    print(f"{Colors.OKBLUE}Welcome to the Linux Terminal! Type 'exit' to quit.{Colors.ENDC}\n")
    print(f"{Colors.OKGREEN}Feel free to try commands like 'hello', 'time', 'ls', 'sudo apt', or 'rm'.{Colors.ENDC}\n")

    # Virtual file system
    virtual_fs = {
        "/": ["home"],
        "/home": ["user"],
        "/home/user": ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"],
        "/home/user/Desktop": [],
        "/home/user/Documents": [],
        "/home/user/Downloads": [],
        "/home/user/Music": [],
        "/home/user/Pictures": [],
        "/home/user/Videos": []
    }
    current_directory = "/home/user"

    # Directories that require sudo to be removed
    protected_dirs = {"Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"}

    responses = {
        "hi": f"{Colors.OKGREEN}Welcome, {user_name}!{Colors.ENDC}\n",
        "hello": f"{Colors.OKGREEN}Hello, There 👋{Colors.ENDC}\n",
        "joke": f"{Colors.OKGREEN}Why did the computer go to the doctor? Because it caught a virus! 😄{Colors.ENDC}\n",
        "do you like music": f"{Colors.OKGREEN}I love music! My favorite song is 'Code Symphony' by Debuggers. 🎵{Colors.ENDC}\n",
        "bye": f"{Colors.OKGREEN}Goodbye! Have a great day! ✨{Colors.ENDC}\n",
        "exit": f"{Colors.OKGREEN}Exiting the terminal. Bye! 👋{Colors.ENDC}\n",
        "time": "",
        "whoami": f"{Colors.OKGREEN}user{Colors.ENDC}\n",
        "clear": ""
    }

    authenticated = False  # Tracks sudo password authentication

    while True:
        user_input = input(f"{Colors.OKBLUE}{user_name}@{device_name}:{current_directory}$ {Colors.ENDC}").strip()
        print()  # Add a line gap before response output

        if user_input.startswith("sudo"):
            if not authenticated:
                pwd_input = input(f"{Colors.WARNING}[sudo] password for {user_name}: {Colors.ENDC}").strip()
                if pwd_input == sudo_password:
                    authenticated = True
                    print(f"{Colors.OKGREEN}{user_name} is now authenticated for sudo commands.{Colors.ENDC}\n")
                else:
                    print(f"{Colors.FAIL}Sorry, try again.{Colors.ENDC}\n")
                    continue

            # Handle sudo commands
            sudo_command = user_input[5:].strip()
            if not sudo_command:
                print(f"{Colors.WARNING}sudo: Command required. Usage: sudo <command>{Colors.ENDC}\n")
                continue

            if sudo_command == "apt update":
                print(f"{Colors.OKBLUE}> Executing 'sudo apt update'...{Colors.ENDC}\n")
                print(f"{Colors.OKGREEN}Reading package lists... Done\nBuilding dependency tree... Done\nReading state information... Done\n{Colors.ENDC}")
            elif sudo_command == "apt upgrade":
                print(f"{Colors.OKBLUE}> Executing 'sudo apt upgrade'...{Colors.ENDC}\n")
                print(f"{Colors.OKGREEN}Reading package lists... Done\nBuilding dependency tree... Done\nCalculating upgrade... Done\n{Colors.ENDC}")
            elif sudo_command.startswith("apt install"):
                package = sudo_command.split(maxsplit=1)[1] if len(sudo_command.split()) > 1 else None
                if package:
                    print(f"{Colors.OKBLUE}> Executing 'sudo apt install {package}'...{Colors.ENDC}\n")
                    print(f"{Colors.OKGREEN}Reading package lists... Done\nBuilding dependency tree... Done\n{package} installed successfully.\n{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}sudo: apt install: missing package name{Colors.ENDC}\n")
            elif sudo_command.startswith("rm"):
                parts = sudo_command.split()
                if len(parts) > 1:
                    target = parts[1]
                    if target in protected_dirs:
                        print(f"{Colors.OKBLUE}> Executing 'sudo rm {target}'...{Colors.ENDC}\n")
                        if target in virtual_fs.get(current_directory, []):
                            print(f"{Colors.OKGREEN}'{target}' has been removed.{Colors.ENDC}\n")
                            virtual_fs[current_directory].remove(target)
                            del virtual_fs[f"{current_directory}/{target}"]
                        else:
                            print(f"{Colors.FAIL}bash: rm: '{target}' not found{Colors.ENDC}\n")
                    else:
                        print(f"{Colors.FAIL}bash: rm: cannot remove '{target}': Operation not permitted{Colors.ENDC}\n")
                else:
                    print(f"{Colors.WARNING}sudo: rm: missing operand{Colors.ENDC}\n")
            else:
                print(f"{Colors.FAIL}bash: {sudo_command}: command not found{Colors.ENDC}\n")
                continue  # Skip the redundant command execution after sudo command

            continue  # Skip the remainder of the loop after executing a sudo command

        # Normal commands handling
        if user_input in responses:
            if user_input == "time":
                from datetime import datetime
                now = datetime.now()
                print(f"{Colors.OKBLUE}> The current time is {now.strftime('%H:%M:%S')} ⏰{Colors.ENDC}\n")
            elif user_input == "clear":
                clear_screen()
            else:
                print(f"{Colors.OKBLUE}> {responses[user_input]}")

            if user_input in ["bye", "exit"]:
                break
        elif user_input.startswith("cd"):
            parts = user_input.split()
            if len(parts) > 1:
                target_dir = parts[1]
                if target_dir == "..":
                    if current_directory != "/":
                        current_directory = "/".join(current_directory.split("/")[:-1]) or "/"
                else:
                    new_directory = f"{current_directory}/{target_dir}".replace("//", "/")
                    if new_directory in virtual_fs:
                        current_directory = new_directory
                    else:
                        print(f"{Colors.FAIL}bash: cd: {target_dir}: No such file or directory{Colors.ENDC}\n")
            else:
                current_directory = "/home/user"
        elif user_input == "ls":
            print(f"{Colors.OKBLUE}{' '.join(virtual_fs.get(current_directory, []))}{Colors.ENDC}\n")
        elif user_input == "pwd":
            print(f"{Colors.OKBLUE}{current_directory}{Colors.ENDC}\n")
        elif user_input.startswith("touch"):
            parts = user_input.split()
            if len(parts) > 1:
                file_name = parts[1]
                if file_name in virtual_fs.get(current_directory, []):
                    print(f"{Colors.FAIL}bash: touch: cannot create file '{file_name}': File exists{Colors.ENDC}\n")
                else:
                    virtual_fs[current_directory].append(file_name)
                    print(f"{Colors.OKGREEN}File '{file_name}' created.{Colors.ENDC}\n")
            else:
                print(f"{Colors.FAIL}bash: touch: missing file operand{Colors.ENDC}\n")
        elif user_input.startswith("mkdir"):
            parts = user_input.split()
            if len(parts) > 1:
                dir_name = parts[1]
                new_directory = f"{current_directory}/{dir_name}".replace("//", "/")
                if dir_name in virtual_fs.get(current_directory, []):
                    print(f"{Colors.FAIL}bash: mkdir: cannot create directory '{dir_name}': Directory exists{Colors.ENDC}\n")
                else:
                    virtual_fs[current_directory].append(dir_name)
                    virtual_fs[new_directory] = []
                    print(f"{Colors.OKGREEN}Directory '{dir_name}' created.{Colors.ENDC}\n")
            else:
                print(f"{Colors.FAIL}bash: mkdir: missing operand{Colors.ENDC}\n")
        elif user_input.startswith("rm"):
            parts = user_input.split()
            if len(parts) > 1:
                target = parts[1]
                if target in virtual_fs.get(current_directory, []):
                    if target not in protected_dirs:
                        print(f"{Colors.OKBLUE}> Executing 'rm {target}'...{Colors.ENDC}\n")
                        virtual_fs[current_directory].remove(target)
                        del virtual_fs[f"{current_directory}/{target}"]
                        print(f"{Colors.OKGREEN}'{target}' has been removed.{Colors.ENDC}\n")
                    else:
                        print(f"{Colors.FAIL}bash: rm: cannot remove '{target}': Operation not permitted{Colors.ENDC}\n")
                else:
                    print(f"{Colors.FAIL}bash: rm: cannot remove '{target}': No such file or directory{Colors.ENDC}\n")
            else:
                print(f"{Colors.FAIL}bash: rm: missing operand{Colors.ENDC}\n")
        else:
            print(f"{Colors.FAIL}bash: {user_input}: command not found{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
