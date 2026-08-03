import shutil
import sys
from pathlib import Path

from config_manager import config
from gdextension_file_helper import update_icons_in_gdextension
from paths import PROJECT_ROOT
from scons_helpers import clear_screen

ICONS_SOURCE_DIR = PROJECT_ROOT / "icons"


def print_instructions_and_prompt(project_folder: str, plugin_name: str) -> bool:
    """Displays Godot icon creation guidelines and asks for confirmation."""
    clear_screen()
    print("Update GDExtension Node Icons Tool\n")

    print(f"Target Project Folder : {project_folder}")
    print(f"Target Plugin File    : {plugin_name}/{plugin_name}.gdextension\n")

    print("HOW IT WORKS:")
    print("  1. Place your SVG icon files in the root 'icons/' folder.")
    print("  2. Name each icon EXACTLY like its C++ Node class (e.g., 'ItemData.svg').")
    print("  3. Cleans destination icon directory and wipes stale Godot .import files.")
    print("  4. Copies new SVGs and updates the [icons] block in .gdextension.\n")

    print("GODOT ICON GUIDELINES & COLOR PALETTE:")
    print("  • Recommended Size : 16 x 16 pixels (SVG format)")
    print("  • 2D Nodes (#8da5f3): Soft Light Blue")
    print("  • 3D Nodes (#fc7f7f): Soft Red / Salmon")
    print("  • GUI Nodes (#8eef97): Soft Green")
    print("  • General Nodes (#e0e0e0) / Dark Theme Accent (#41b0f6)\n")

    print("-" * 50)

    while True:
        user_input = input("Are you sure you want to update node icons now? (y/q): ").strip().lower()
        if user_input == "y":
            return True
        elif user_input == "q":
            print("\nOperation cancelled.")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'y' to proceed or 'q' to quit.")


def clean_destination_directory(project_icons_dest: Path, godot_imported_dir: Path):
    """
    Completely wipes the destination icons directory (including old .import files)
    and removes matching imported cache files in .godot/imported/.
    """
    if project_icons_dest.exists():
        print("Cleaning old icons and stale .import files...")
        shutil.rmtree(project_icons_dest)

    # Re-create fresh destination directory
    project_icons_dest.mkdir(parents=True, exist_ok=True)

    # Clean .godot/imported cache for icon files to prevent stale import loops
    if godot_imported_dir.exists():
        for imported_file in godot_imported_dir.glob("*.md5"):
            if "icons" in imported_file.name or "svg" in imported_file.name:
                try:
                    imported_file.unlink(missing_ok=True)
                    stex_file = imported_file.with_suffix(".stex")
                    ctex_file = imported_file.with_suffix(".ctex")
                    stex_file.unlink(missing_ok=True)
                    ctex_file.unlink(missing_ok=True)
                except OSError:
                    pass


def update_gdextension_icons():
    plugin_name = config.getPluginName()
    project_folder = config.getGodotProjectFolder()

    if not print_instructions_and_prompt(project_folder, plugin_name):
        return

    # Base paths
    project_path = PROJECT_ROOT / project_folder
    plugin_dir = project_path / plugin_name
    gdextension_file = plugin_dir / f"{plugin_name}.gdextension"
    project_icons_dest = plugin_dir / "icons"
    godot_imported_dir = project_path / ".godot" / "imported"

    if not ICONS_SOURCE_DIR.exists():
        ICONS_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\nCreated source directory: {ICONS_SOURCE_DIR}")
        print("Place your 16x16 .svg node icons there and run this script again.")
        input("\nPress Enter to continue...")
        return

    svg_files = list(ICONS_SOURCE_DIR.glob("*.svg"))
    if not svg_files:
        print(f"\nNo .svg icons found in: {ICONS_SOURCE_DIR}")
        print("Please place your node SVG files inside the folder and try again.")
        input("\nPress Enter to continue...")
        return

    if not gdextension_file.exists():
        print(f"\nError: Could not locate GDExtension file at:")
        print(f"  {gdextension_file}")
        print("Check your 'pluginName' and 'godotProjectFolder' settings in config.json.")
        input("\nPress Enter to continue...")
        return

    # Wipe destination icons folder & import cache
    clean_destination_directory(project_icons_dest, godot_imported_dir)

    # Copy fresh SVGs and build mapping dictionary
    icon_mappings = {}
    print("\nCopying Fresh Icons:")
    for svg_file in svg_files:
        node_name = svg_file.stem  # e.g., 'ItemData'

        dest_file = project_icons_dest / svg_file.name
        shutil.copy2(svg_file, dest_file)

        res_path = f"res://{plugin_name}/icons/{svg_file.name}"
        icon_mappings[node_name] = res_path
        print(f"Copied & Mapped: {node_name} -> {res_path}")

    update_icons_in_gdextension(gdextension_file, icon_mappings)
    print(f"\nSuccessfully updated {len(icon_mappings)} icon(s) in '{gdextension_file.name}'!")


if __name__ == "__main__":
    try:
        update_gdextension_icons()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

    input("\nPress Enter to continue...")
