from __future__ import annotations

import sys
from pathlib import Path

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


from tools.config_manager import config
from tools.gdextension_file_helper import set_editor_target_mode
from tools.paths import get_gdextension_file_path
from tools.scons_helpers import clear_screen


def display_info_and_recommendations() -> None:
    print("-" * 75)
    print("ABOUT EDITOR BUILD TARGET (template_debug vs template_release):")
    print("-" * 75)
    print("• How It Works:")
    print("  By default, the Godot Editor loads binaries specified under '.debug' tags in")
    print("  your .gdextension manifest.")
    print()
    print("• Debug Target (template_debug):")
    print("  - Includes runtime safety checks, assertions, and faster compile times.")
    print("  - Best for daily feature development and C++ debugging.")
    print()
    print("• Release Target (template_release):")
    print("  - Uses maximum compiler speed optimizations (-O3 on GCC/Clang, /O2 on MSVC).")
    print("  - Combined with LTO, yields much faster execution inside the Godot Editor.")
    print("  - In-editor documentation and ClassDB bindings remain fully functional.")
    print()
    print("• Recommendations:")
    print("  1. 'debug':   Use while actively writing and debugging new C++ code.")
    print("  2. 'release': Switch before distributing your plugin or when working on")
    print("     performance-heavy editor tools (e.g., procedural generation, heavy math).")

    print("\nYou can basically force the godot editor to use the release build (fully optimized) if you are dealing with editor tools.")  # noqa: E501
    print("-" * 75 + "\n")


def toggle_editor_target() -> None:
    clear_screen()
    print("GDExtension Editor Build Target Switcher by @realNikich\n")

    display_info_and_recommendations()

    current_mode = config.getEditorTargetMode()
    manifest_path = get_gdextension_file_path()

    print(f"Target Manifest: {manifest_path.name}")
    print(f"Current Editor Target: {'DEBUG (template_debug)' if current_mode == 'debug' else 'RELEASE (template_release)'}\n")  # noqa: E501

    print("Options:")
    print("  [1] Set Editor to DEBUG mode (template_debug)")
    print("  [2] Set Editor to RELEASE mode (template_release)")
    print("  [q] Quit without changing")

    choice = input("\nSelect choice (1, 2, or q): ").strip().lower()

    if choice == "q":
        print("Operation cancelled.")
        sys.exit(0)

    if choice == "1":
        new_mode = "debug"
    elif choice == "2":
        new_mode = "release"
    else:
        print("Invalid selection.")
        sys.exit(1)

    previous_mode = config.getEditorTargetMode()
    try:
        set_editor_target_mode(new_mode)
        config.setEditorTargetMode(new_mode)
        mode_str = "DEBUG (template_debug)" if new_mode == "debug" else "RELEASE (template_release)"
        print(f"\nSuccessfully updated Editor Build Target to: {mode_str}")
        print(f"Updated tools/config.json and {manifest_path.name}.")
    except OSError as e:
        # Roll back config if file write failed to avoid desync (config says new but manifest still old)
        try:
            config.setEditorTargetMode(previous_mode)
        except OSError:
            pass
        print(f"\nError updating .gdextension file: {e}. Check the file is not locked and you have write permission.")

    _ = input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        toggle_editor_target()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
