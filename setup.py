import os
import subprocess
import sys

from tools.config_manager import config

script_dir = os.path.dirname(os.path.abspath(__file__))

MENU_ITEMS = [
    ("Update godot_cpp Submodule To Latest", "update_godot_cpp.py"),
    ("Change Godot Target Version", "change_godot_target_version.py"),
    ("Select Build Profile", "select_build_profile.py"),
    ("Rename Plugin", "renaming.py"),
    ("Compile Plugin Debug Build", "compile_debug_build.py"),
    ("Compile Plugin Release Build", "compile_release_build.py"),
    ("Generate Missing XML Documentation Files", "generate_xml_docs.py"),
    ("Change LTO Mode For Release Builds", "change_lto_mode.py"),
    ("Update Editor Node Icons", "update_icons.py"),
    ("Edit Build Profile", "edit_build_profile.py"),
    ("Hot Reloading Options", "toggle_reloadable.py"),
    ("Select Godot Project Folder", "select_godot_project.py"),
    ("Toggle Editor Build Target", "toggle_editor_target.py"),
    ("Select Godot Engine Executable Path", "select_godot_path.py"),
    ("Tutorials And Help With Godot C++", "tutorials.py"),
]


def clear_screen():
    """Clear the terminal screen cross-platform using subprocess."""
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.run([cmd], check=False)


def get_active_path_version() -> str:
    """Helper to find the version tag of the currently active Godot path."""
    active_path = config.getGodotActivePath()
    if not active_path:
        return "None Set"

    saved_entries = config.getSavedGodotPaths()
    for entry in saved_entries:
        if entry.get("path") == active_path:
            return entry.get("version", "Unknown")

    return "Unknown"


def display_menu():
    """Display the main menu options dynamically from MENU_ITEMS."""
    clear_screen()

    plugin_name = config.getPluginName()
    godot_version = config.getGodotVersion()
    godot_path = config.getGodotActivePath()
    project_folder = config.getGodotProjectFolder()
    build_profile = config.getSelectedBuildProfile()
    active_version = get_active_path_version()

    print(f"Current Plugin Name: {plugin_name}")
    print(f"Current Targeted Godot Version: {godot_version}")
    print(f"Selected Godot Project Folder: {project_folder or 'NONE'}")
    print(f"Selected Build Profile: {build_profile or 'NONE'}")

    if godot_path:
        print(f"Active Godot Engine Path: {godot_path} ({active_version})\n")
    else:
        print("Active Godot Engine Path: NONE\n")

    print("Choose an option:")
    for idx, (title, _) in enumerate(MENU_ITEMS, start=1):
        print(f"{idx}. {title}")

    print("\nEnter your choice, or 'q' to quit: ")


def run_tool_script(script_filename):
    """Run a script from the tools folder and handle errors/output."""
    script_path = os.path.join(script_dir, "tools", script_filename)
    result = subprocess.run([sys.executable, script_path], check=False)

    if result.returncode != 0:
        print(result.stderr or "An error occurred.")
        input("Press Enter to continue...")


def handle_option(choice):
    """Handle the selected menu option using 1-based indexing."""
    clear_screen()

    if choice.isdigit() and 1 <= int(choice) <= len(MENU_ITEMS):
        _, script_name = MENU_ITEMS[int(choice) - 1]
        run_tool_script(script_name)
    else:
        print("Invalid choice. Please enter a valid option or 'q' to quit.")
        input("Press Enter to continue...")


def main():
    """Main loop to display menu and handle user input."""
    while True:
        config.reload()
        display_menu()
        user_input = input().strip().lower()

        if user_input == "q":
            print("Quitting...")
            sys.exit(0)

        handle_option(user_input)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit(0)
