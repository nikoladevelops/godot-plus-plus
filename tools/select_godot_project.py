import sys
from pathlib import Path
from typing import List

from config_manager import config
from paths import PROJECT_ROOT
from scons_helpers import clear_screen


def display_info():
    print("-" * 75)
    print("ABOUT TARGET GODOT PROJECT SWITCHER:")
    print("-" * 75)
    print("• Switch Target Projects Easily:")
    print("  Choose which Godot project folder receives the compiled binaries.")
    print("  You can quickly switch between different Godot projects in your workspace")
    print("  for testing purposes (e.g., 'test_project_2d', 'demo_game', etc.).")
    print()
    print("• Auto-Discovery:")
    print("  Scans your workspace for folders that contain a Godot project.")
    print("-" * 75 + "\n")


def discover_godot_projects() -> List[Path]:
    """
    Scans immediate subdirectories of PROJECT_ROOT for Godot projects.
    A directory is considered a Godot project if it contains a 'project.godot'
    file or a '.godot' directory.
    """
    godot_projects = []

    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and ((item / "project.godot").exists() or (item / ".godot").exists()):
            godot_projects.append(item)

    return sorted(godot_projects, key=lambda p: p.name.lower())


def select_godot_project():
    clear_screen()
    print("Select Godot Project Folder Tool by @realNikich\n")

    display_info()

    current_project = config.getGodotProjectFolder()
    print(f"Currently Active Target Project Folder: '{current_project}'\n")

    discovered_projects = discover_godot_projects()

    if not discovered_projects:
        print(f"Error: No Godot projects found in {PROJECT_ROOT}.")
        print("Ensure your project subfolder contains a 'project.godot' file or '.godot' directory.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print("Discovered Godot Projects in workspace:")
    for idx, proj_path in enumerate(discovered_projects, start=1):
        is_current = " (Active)" if proj_path.name == current_project else ""
        print(f"  [{idx}] {proj_path.name}{is_current}")

    print("  [q] Quit without changing\n")

    while True:
        choice = input("Select a Godot project folder or 'q': ").strip().lower()

        if choice == "q":
            print("Operation cancelled.")
            sys.exit(0)

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(discovered_projects):
                selected_dir = discovered_projects[idx - 1]
                config.setGodotProjectFolder(selected_dir.name)

                print(f"\nSuccessfully set active Godot project folder to: '{selected_dir.name}'")
                print("SCons will now copy compiled binaries directly into this project folder.")
                input("\nPress Enter to continue...")
                return

        print(f"Invalid selection! Enter a number between 1 and {len(discovered_projects)}, or 'q'.")


if __name__ == "__main__":
    try:
        select_godot_project()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
