from __future__ import annotations

import sys
from pathlib import Path

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


from tools.config_manager import config
from tools.paths import PROJECT_ROOT, normalize_user_path
from tools.scons_helpers import clear_screen


def display_info() -> None:
    print("-" * 75)
    print("ABOUT TARGET GODOT PROJECT SWITCHER:")
    print("-" * 75)
    print("• Switch Target Projects Easily:")
    print("  Choose which Godot project folder receives the compiled binaries.")
    print("  You can target projects inside your workspace or completely anywhere")
    print("  else on your filesystem using full/custom paths (no copy-pasting needed).")
    print()
    print("• Auto-Discovery & Custom Paths:")
    print("  - Automatically scans your workspace root for local projects.")
    print("  - Allows pasting or inputting an absolute/custom path to any external project.")
    print("-" * 75 + "\n")


def is_valid_godot_project(path: Path) -> bool:
    """Verifies if a given path points to a valid Godot project folder."""
    if not path.is_dir():
        return False
    return (path / "project.godot").is_file() or (path / ".godot").is_dir()


def normalize_path(user_input: str) -> Path | None:
    """Backward-compat wrapper — delegates to paths.normalize_user_path (single source)."""
    return normalize_user_path(user_input)


def discover_godot_projects() -> list[Path]:
    """
    Scans immediate subdirectories of PROJECT_ROOT for Godot projects.
    """
    godot_projects = []
    try:
        for item in PROJECT_ROOT.iterdir():
            if is_valid_godot_project(item):
                godot_projects.append(item)
    except (PermissionError, OSError):
        pass

    return sorted(godot_projects, key=lambda p: p.name.lower())


def select_godot_project() -> None:
    clear_screen()
    print("Select Godot Project Folder Tool by @realNikich\n")

    display_info()

    current_project = config.getGodotProjectFolder()
    print(f"Currently Active Target Project Path/Folder: '{current_project}'\n")

    discovered_projects = discover_godot_projects()

    print("Discovered Godot Projects in Workspace:")
    if not discovered_projects:
        print("  (No projects automatically found in workspace root)")
    else:
        for idx, proj_path in enumerate(discovered_projects, start=1):
            is_current = " (Active)" if str(proj_path) == current_project or proj_path.name == current_project else ""
            print(f"  [{idx}] {proj_path} {is_current}")

    print("\nOptions:")
    print("  [p] Provide a custom folder path (absolute or external to workspace)")
    print("  [q] Quit without changing\n")

    while True:
        choice = input("Select workspace project number, 'p' for custom path, or 'q': ").strip().lower()

        if choice == "q":
            print("Operation cancelled.")
            sys.exit(0)

        if choice == "p":
            print("\nEnter the absolute or relative path to the external Godot project folder:")
            user_input = input("> ").strip()
            custom_path = normalize_path(user_input)

            if not custom_path or not is_valid_godot_project(custom_path):
                print("\nError: The provided path is either invalid or does not contain a 'project.godot' file!")
                _ = input("Press Enter to try again...")
                clear_screen()
                display_info()
                continue

            # Save full absolute path string for ultimate flexibility across systems
            final_path_str = str(custom_path)
            config.setGodotProjectFolder(final_path_str)

            print(f"\nSuccessfully set active Godot project path to: '{final_path_str}'")
            print("SCons will now copy compiled binaries directly into this external project folder.")
            _ = input("\nPress Enter to continue...")
            return

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(discovered_projects):
                selected_dir = discovered_projects[idx - 1]
                # Save either full path or name depending on standard usage; storing full absolute path here for robust support  # noqa: E501
                final_path_str = str(selected_dir)
                config.setGodotProjectFolder(final_path_str)

                print(f"\nSuccessfully set active Godot project folder to: '{final_path_str}'")
                print("SCons will now copy compiled binaries directly into this project folder.")
                _ = input("\nPress Enter to continue...")
                return

        print("Invalid selection! Enter a valid number, 'p', or 'q'.")


if __name__ == "__main__":
    try:
        select_godot_project()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
