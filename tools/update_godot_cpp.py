from __future__ import annotations

import sys
from pathlib import Path

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


from tools.git_helpers import (
    check_godot_cpp_has_updates,
    check_godot_cpp_submodule_initialized,
    initialize_current_submodule_version,
    update_submodule_to_latest_master_commit,
)


def update_godot_cpp_version() -> None:
    print("Tool For Updating godot_cpp Version By @realNikich\n")

    print("By updating the submodule version, bug fixes will be applied and new target versions of Godot could become available.\n")  # noqa: E501

    if not check_godot_cpp_submodule_initialized():
        initialize_current_submodule_version()

    if check_godot_cpp_has_updates():
        while True:
            user_input = (
                input(
                    "There is a new version of godot_cpp available. "
                    "Do you want to update to latest? [y/n/q]: "
                )
                .strip()
                .lower()
            )

            if user_input in ("q", "n"):
                print("Skipping update. Quitting...")
                sys.exit(0)
            elif user_input == "y":
                break
            else:
                print("Invalid choice! Please enter 'y' for Yes, 'n' for No, or 'q' to Quit.\n")

        update_submodule_to_latest_master_commit()

        print("Submodule successfully updated!")
        _ = input("\nPress Enter to continue...")
    else:
        print("You are already running the latest godot_cpp version. No updates available.")
        _ = input("\nPress Enter to continue...")
        sys.exit(0)


if __name__ == "__main__":
    try:
        update_godot_cpp_version()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
