from __future__ import annotations

import sys
from pathlib import Path

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import shutil

from tools.paths import PROJECT_ROOT, get_plugin_dir
from tools.scons_helpers import clear_screen, pause, run_scons_clean


def clean_bin_directories() -> None:
    """
    Cleans the root bin directory and the target project's plugin bin directory if they exist.
    """
    print("\nCleaning local bin directories...")

    # Clean root bin directory
    root_bin = PROJECT_ROOT / "bin"
    if root_bin.exists() and root_bin.is_dir():
        try:
            shutil.rmtree(root_bin)
            print(f"Removed root bin directory: {root_bin}")
        except OSError as e:
            print(f"Warning: Could not remove {root_bin}: {e}", file=sys.stderr)

    # Clean targeted project's plugin bin directory
    plugin_dir = get_plugin_dir()
    plugin_bin = plugin_dir / "bin"
    if plugin_bin.exists() and plugin_bin.is_dir():
        try:
            shutil.rmtree(plugin_bin)
            print(f"Removed project plugin bin directory: {plugin_bin}")
        except OSError as e:
            print(f"Warning: Could not remove {plugin_bin}: {e}", file=sys.stderr)


if __name__ == "__main__":
    clear_screen()
    print("GDExtension SCons Clean Tool by @realNikich\n")
    print("This tool will run 'scons -c' and clean up all compiled bin directories.")
    print("-" * 50 + "\n")

    try:
        raw_choice = input("Press Enter to proceed with cleaning, or type 'q' to quit: ")
        choice = raw_choice.strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        sys.exit(0)

    if choice == 'q':
        print("Quitting...")
        sys.exit(0)

    run_scons_clean()
    clean_bin_directories()

    pause("\nPress Enter to finish...")