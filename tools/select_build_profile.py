import subprocess
import sys

from config_manager import config
from paths import BUILD_PROFILES_DIR, PROJECT_ROOT
from scons_helpers import clear_screen


def clean_build_files() -> None:
    """Executes 'scons -c' to clean previous build artifacts."""
    print("Cleaning old build files...")
    try:
        subprocess.run(["scons", "-c"], check=True, cwd=PROJECT_ROOT)
        print("Build artifacts cleaned successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: Could not run 'scons -c' clean: {e}. Continuing anyway...")


def select_build_profile():
    clear_screen()
    print("Select Build Profile Tool by @realNikich\n")

    if not BUILD_PROFILES_DIR.exists():
        BUILD_PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    current_profile = config.getSelectedBuildProfile()
    print(f"Currently Active Build Profile: {current_profile}\n")

    profiles = sorted(BUILD_PROFILES_DIR.glob("*.json"))

    print("Available Build Profiles:")
    print("  [0] None (Include all Godot classes - no profile)")

    for idx, prof in enumerate(profiles, start=1):
        is_current = " (Active)" if prof.name == current_profile else ""
        print(f"  [{idx}] {prof.name}{is_current}")

    print("  [q] Quit without changing\n")

    while True:
        user_input = input("Select a build profile or 'q': ").strip().lower()

        if user_input == "q":
            print("Operation cancelled.")
            sys.exit(0)

        if user_input == "0":
            config.setSelectedBuildProfile("none")
            print("\nBuild Profile set to: None (all classes enabled).")
            clean_build_files()
            input("\nPress Enter to continue...")
            return

        if user_input.isdigit():
            choice_num = int(user_input)
            if 1 <= choice_num <= len(profiles):
                selected_file = profiles[choice_num - 1]
                config.setSelectedBuildProfile(selected_file.name)

                print(f"\nSuccessfully selected Build Profile: {selected_file.name}")
                clean_build_files()
                print("Please recompile your project for the profile changes to take effect.")
                input("\nPress Enter to continue...")
                return

        print(f"Invalid selection! Enter a number between 0 and {len(profiles)}, or 'q'.")


if __name__ == "__main__":
    try:
        select_build_profile()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
