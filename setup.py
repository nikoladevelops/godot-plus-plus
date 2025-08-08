import os
import sys
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))

def clear_screen():
    """Clear the terminal screen cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_dont_touch():
    """Read the first and second lines from dont_touch.txt."""
    try:
        with open(os.path.join(script_dir, "dont_touch.txt"), "r") as file:
            lines = file.readlines()
            if len(lines) < 2:
                raise ValueError("dont_touch.txt does not have at least two lines")
            return lines[0].strip(), lines[1].strip()
    except (FileNotFoundError, IOError, ValueError):
        print("Someone deleted or touched the dont_touch.txt file used for storing important data,")
        print("you can't use the functionality anymore sorry, you'll have to edit the appropriate")
        print("files yourself, check out the scripts inside the tools folder for more info")
        sys.exit(1)


def display_start_screen():
    print("\n")
    print("=== Godot C++ GDExtension Setup Tool By @realNikich ===")
    print("\n")
    print("Official GitHub Repository: https://github.com/nikoladevelops/godot-plus-plus")
    print("Find Godot GDExtension Tutorials Here: https://youtube.com/@realNikich")
    
    print("\n")
    input("Press any key to continue...")
    clear_screen()


def display_menu():
    """Display the main menu options."""
    clear_screen()
    

    # Read dont_touch.txt before proceeding
    first_line, second_line = read_dont_touch()
    
    print(f"Current Plugin Name: {first_line}")
    print(f"Current Targeted Godot Version: {second_line}")

    print("\n")

    print("Choose an option")

    print("1. Change Godot Target Version")
    print("2. Rename Plugin")
    print("3. Prepare For Export")
    print("Enter your choice (1-3), 'q' to quit: ")

def handle_option(choice):
    """Handle the selected option and wait for 'b' input."""
    clear_screen()
    
    if choice == '1':  # Change Godot Target Version
        change_version_path = os.path.join(script_dir, "tools", "change_version.py")
        result = subprocess.run([sys.executable, change_version_path])
        if result.returncode != 0:
            print(result.stderr)
            input("Press Enter to continue...")
            return
    elif choice == '2':  # Rename Plugin
        while True:
                renaming_path = os.path.join(script_dir, "tools", "renaming.py")
                result = subprocess.run([sys.executable, renaming_path])
                if result.returncode != 0:
                    print(result.stderr)
                    input("Press Enter to continue...")
                    return
                break
    elif choice == '3':  # Prepare For Export
        prepare_export_path = os.path.join(script_dir, "tools", "prepare_export.py")
        result = subprocess.run([sys.executable, prepare_export_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            input("Press Enter to continue...")
            return
    
        # TODO
        print("NOT IMPLEMENTED YET")
        input("Press Enter to return...")
        

def main():
    """Main loop to display menu and handle user input."""

    display_start_screen()
    while True:
        display_menu()
        user_input = input().lower()
        if user_input == 'q':
            print("Quitting...")
            sys.exit(0)
        if user_input not in ['1', '2', '3']:
            print("Invalid choice. Please enter a valid option or 'q' to quit.")
            input("Press Enter to continue...")
            continue

        handle_option(user_input)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(0)