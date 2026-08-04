import os
import subprocess
import sys

from tools.config_manager import config

script_dir = os.path.dirname(os.path.abspath(__file__))


def clear_screen():
    """Clear the terminal screen cross-platform using subprocess."""
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.run([cmd], check=False)


def display_menu():
    """Display the main menu options."""
    clear_screen()


    plugin_name = config.getPluginName()
    godot_version = config.getGodotVersion()


    print(f"Current Plugin Name: {plugin_name}")
    print(f"Current Targeted Godot Version: {godot_version}\n")

    print("Choose an option:")
    print("1. Update godot_cpp Submodule To Latest")
    print("2. Change Godot Target Version")
    print("3. Select Build Profile")
    print("4. Rename Plugin")
    print("5. Compile Plugin Debug Build")
    print("6. Compile Plugin Release Build")
    print("7. Generate Missing XML Documentation Files")
    print("8. Change LTO Mode For Release Builds")
    print("9. Update Editor Node Icons")
    print("10. Edit Build Profile")
    print("11. Hot Reloading Options")
    print("12. Select Godot Project Folder")
    print("13. Toggle Editor Build Target")

    print("15. Tutorials And Help With Godot C++")

    print("Enter your choice (0-9), or 'q' to quit: ")


def run_tool_script(script_filename):
    """Run a script from the tools folder and handle errors/output."""
    script_path = os.path.join(script_dir, "tools", script_filename)
    result = subprocess.run([sys.executable, script_path], check=False)

    if result.returncode != 0:
        print(result.stderr or "An error occurred.")
        input("Press Enter to continue...")


def handle_option(choice):
    """Handle the selected menu option."""
    clear_screen()

    valid_choices = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "15"}

    if choice not in valid_choices:
        print("Invalid choice. Please enter a valid option or 'q' to quit.")
        input("Press Enter to continue...")
        return

    script_map = {
        "1": "update_godot_cpp.py",
        "2": "change_godot_target_version.py",
        "3": "select_build_profile.py",
        "4": "renaming.py",
        "5": "compile_debug_build.py",
        "6": "compile_release_build.py",
        "7": "generate_xml_docs.py",
        "8": "change_lto_mode.py",
        "9": "update_icons.py",
        "10": "edit_build_profile.py",
        "11": "toggle_reloadable.py",
        "12": "select_godot_project.py",
        "13": "toggle_editor_target.py",
        "15": "tutorials.py"
    }

    script_name = script_map.get(choice)
    if script_name:
        run_tool_script(script_name)
    else:
        print("Invalid option.")
        input("Press Enter to continue...")


def main():
    """Main loop to display menu and handle user input."""

    while True:
        display_menu()
        user_input = input().strip().lower()

        if user_input == "q":
            print("Quitting...")
            sys.exit(0)


        handle_option(user_input)
        config.reload()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit(0)
