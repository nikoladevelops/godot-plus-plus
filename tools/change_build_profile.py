import os
import re
import json
import subprocess
from pathlib import Path
from typing import List, Set, Tuple, Dict

# Paths relative to script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
TEST_PROJECT_DIR = os.path.join(PARENT_DIR, "test_project")
SRC_DIR = os.path.join(PARENT_DIR, "src")
SCONSTRUCT_PATH = os.path.join(PARENT_DIR, "SConstruct")
API_JSON_PATH = os.path.join(PARENT_DIR, "godot-cpp", "gdextension", "extension_api.json")

def read_file(file_path: str) -> str:
    """Read the contents of a file.

    Args:
        file_path: Path to the file.

    Returns:
        File contents.

    Raises:
        SystemExit: If the file is not found.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)

def write_file(file_path: str, content: str) -> None:
    """Write content to a file, overwriting if it exists.

    Args:
        file_path: Path to the file.
        content: Content to write.

    Raises:
        SystemExit: If writing fails.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError:
        print(f"Error: Could not write to {file_path}.")
        exit(1)

def extract_2d_3d_xr_classes() -> Tuple[Set[str], Set[str], Set[str]]:
    """Extract 2D, 3D, and XR classes from extension_api.json.

    Returns:
        Sets of 2D, 3D, and XR class names.

    Raises:
        SystemExit: If extension_api.json is not found.
    """
    content = read_file(API_JSON_PATH)
    api_data = json.loads(content)

    two_d_classes = set()
    three_d_classes = set()
    xr_classes = set()

    for cls in api_data["classes"]:
        class_name = cls["name"]
        if class_name.lower().endswith("2d"):
            two_d_classes.add(class_name)
        elif class_name.lower().endswith("3d"):
            three_d_classes.add(class_name)
        if class_name.startswith("XR") or class_name == "WebXRInterface":
            xr_classes.add(class_name)

    return two_d_classes, three_d_classes, xr_classes

def read_sconstruct_vars() -> Dict[str, str]:
    """Read boolean variables from SConstruct.

    Returns:
        Dictionary mapping variable names to their boolean values ('true' or 'false').

    Raises:
        SystemExit: If SConstruct is missing, a variable is not found, or a variable has an invalid value.
    """
    content = read_file(SCONSTRUCT_PATH)
    vars = {}
    required_vars = ["is_2d_profile_used", "is_3d_profile_used", "is_custom_profile_used"]

    for var in required_vars:
        match = re.search(rf'^{var}\s*=\s*"([^"]+)"\s*$', content, re.MULTILINE)
        if not match:
            print(f"Error: Variable '{var}' not found in {SCONSTRUCT_PATH}. Ensure it is defined as '{var} = \"true\"' or '{var} = \"false\"'.")
            exit(1)
        value = match.group(1).lower()
        if value not in {"true", "false"}:
            print(f"Error: Variable '{var}' has invalid value '{value}' in {SCONSTRUCT_PATH}. Must be 'true' or 'false'.")
            exit(1)
        vars[var] = value

    return vars

def update_sconstruct_vars(vars_to_set: Dict[str, str]) -> None:
    """Update boolean variables in SConstruct.

    Args:
        vars_to_set: Dictionary of variable names and their new boolean values ('true' or 'false').

    Raises:
        SystemExit: If SConstruct cannot be read or written, or a variable is not found.
    """
    content = read_file(SCONSTRUCT_PATH)
    new_content = content

    for var, value in vars_to_set.items():
        pattern = rf'^{var}\s*=\s*"[^"]+"\s*$'
        replacement = f'{var} = "{value}"'
        if not re.search(pattern, new_content, re.MULTILINE):
            print(f"Error: Variable '{var}' not found in {SCONSTRUCT_PATH} for updating.")
            exit(1)
        new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)

    write_file(SCONSTRUCT_PATH, new_content)

def clean_build_files() -> None:
    """Run 'scons -c' to clean old build files.

    Raises:
        SystemExit: If the scons -c command fails.
    """
    try:
        subprocess.run(["scons", "-c"], check=True, cwd=PARENT_DIR)
        print("Old build files cleaned successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to run 'scons -c' to clean old build files.")
        exit(1)

def display_current_profile(vars: Dict[str, str]) -> None:
    """Display the current build profile based on SConstruct variables.

    Args:
        vars: Dictionary of SConstruct variables and their values.
    """
    is_profile_used = any(vars[var] == "true" for var in vars)
    print(f"Build Profile Being Used: {str(is_profile_used).lower()}")
    print("Current Profile:")
    if not is_profile_used:
        print("  None (all classes included)")
    elif vars["is_2d_profile_used"] == "true":
        print("  2D Profile")
    elif vars["is_3d_profile_used"] == "true":
        print("  3D Profile")
    elif vars["is_custom_profile_used"] == "true":
        print("  Custom User Profile")

def get_user_choice() -> Tuple[str, bool]:
    """Prompt the user for a build profile choice and XR exclusion preference.

    Returns:
        Selected choice ('1', '2', '3', or '4') and whether to exclude XR classes.
        Returns ('q', False) if the user chooses to quit.

    Raises:
        SystemExit: If the choice is invalid (not '1', '2', '3', '4', or 'q').
    """
    print("\nSelect Build Profile:")
    print("  1. None (use all classes)")
    print("  2. 2D Profile (disable 3D classes)")
    print("  3. 3D Profile (disable 2D classes)")
    print("  4. Custom User Profile (edit build_profile.json manually)")
    print("  Press 'q' to exit")
    choice = input("Enter choice (1-4 or q): ").strip().lower()

    if choice == "q":
        return "q", False
    if choice not in {"1", "2", "3", "4"}:
        print("Invalid choice. Please enter 1, 2, 3, 4, or q.")
        exit(1)

    exclude_xr = False
    if choice in {"2", "3"}:
        exclude_xr_input = input("\nDo you want to also disable XR classes (e.g., XRInterface, XRCamera3D)? (y/n): ").strip().lower()
        exclude_xr = exclude_xr_input == "y"

    return choice, exclude_xr

def generate_profile_json(file_name: str, disabled_classes: List[str]) -> None:
    """Generate a build profile JSON file with disabled classes, overwriting any existing file.

    Args:
        file_name: Name of the profile file (e.g., '2d_build_profile.json').
        disabled_classes: List of classes to disable.

    Raises:
        SystemExit: If writing the file fails.
    """
    profile = {
        "_": "Auto-generated build profile. For Custom Profile, edit build_profile.json to add 'enabled_classes' or 'disabled_classes'.",
        "type": "feature_profile",
        "disabled_classes": sorted(disabled_classes)
    }
    write_file(os.path.join(PARENT_DIR, file_name), json.dumps(profile, indent=4))

def handle_profile_choice(choice: str, exclude_xr: bool, two_d_classes: Set[str], three_d_classes: Set[str], xr_classes: Set[str]) -> Dict[str, str]:
    """Handle the user's profile choice by setting SConstruct variables and generating profile files.

    Args:
        choice: User's profile choice ('1', '2', '3', or '4').
        exclude_xr: Whether to exclude XR classes for 2D/3D profiles.
        two_d_classes: Set of 2D class names.
        three_d_classes: Set of 3D class names.
        xr_classes: Set of XR class names.

    Returns:
        Dictionary of SConstruct variables to update.

    Raises:
        SystemExit: If build_profile.json is missing for Custom Profile or file operations fail.
    """
    new_vars = {
        "is_2d_profile_used": "false",
        "is_3d_profile_used": "false",
        "is_custom_profile_used": "false"
    }

    if choice == "1":
        print("Profile set to None (all classes included).")
    elif choice == "2":
        new_vars["is_2d_profile_used"] = "true"
        disabled_classes = list(three_d_classes)
        if exclude_xr:
            disabled_classes.extend(xr_classes)
        generate_profile_json("2d_build_profile.json", disabled_classes)
        print(f"2D Profile enabled: {len(disabled_classes)} classes disabled (3D{' and XR' if exclude_xr else ''}).")
    elif choice == "3":
        new_vars["is_3d_profile_used"] = "true"
        disabled_classes = list(two_d_classes)
        if exclude_xr:
            disabled_classes.extend(xr_classes)
        generate_profile_json("3d_build_profile.json", disabled_classes)
        print(f"3D Profile enabled: {len(disabled_classes)} classes disabled (2D{' and XR' if exclude_xr else ''}).")
    elif choice == "4":
        new_vars["is_custom_profile_used"] = "true"
        profile_path = os.path.join(PARENT_DIR, "build_profile.json")
        if not os.path.exists(profile_path):
            print(f"Error: {profile_path} not found. Please create it with 'enabled_classes' or 'disabled_classes'.")
            exit(1)
        print("Custom User Profile enabled: Edit build_profile.json to specify 'enabled_classes' or 'disabled_classes'.")

    
    return new_vars

def main():
    """Configure the build profile for a GDExtension project."""
    print("Configure Custom Build Profile Tool by @realNikich")

    # Read and display current SConstruct variables
    vars = read_sconstruct_vars()
    display_current_profile(vars)

    # Extract 2D/3D/XR classes
    two_d_classes, three_d_classes, xr_classes = extract_2d_3d_xr_classes()

    # Get user input
    choice, exclude_xr = get_user_choice()
    if choice == "q":
        print("Exiting without changes.")
        exit(0)

    # Handle profile choice and update SConstruct
    new_vars = handle_profile_choice(choice, exclude_xr, two_d_classes, three_d_classes, xr_classes)
    update_sconstruct_vars(new_vars)

    
    # Clean old build files
    print("\nAll old object files will now be cleaned up, so you will have to recompile everything when this finishes.")
    clean_build_files()
    print("\n")

    # Print final messages after cleaning
    if choice == "1":
        print("Profile set to None (all classes included).")
    elif choice == "2":
        print(f"2D Profile enabled: {len(list(three_d_classes) + (list(xr_classes) if exclude_xr else []))} classes disabled (3D{' and XR' if exclude_xr else ''}).")
        print("Warning: If you need some of the 3D classes that were disabled, you can always edit the 2d_build_profile.json and save your changes.")
    elif choice == "3":
        print(f"3D Profile enabled: {len(list(two_d_classes) + (list(xr_classes) if exclude_xr else []))} classes disabled (2D{' and XR' if exclude_xr else ''}).")
        print("Warning: If you need some of the 2D classes that were disabled, you can always edit the 3d_build_profile.json and save your changes.")
    elif choice == "4":
        print("Custom User Profile enabled: Edit build_profile.json to specify 'enabled_classes' or 'disabled_classes'.")
    print("SConstruct updated with new profile settings.")

    
    print("\nPlease recompile your project to apply the new build profile.")

    input("Press any key to continue...")

if __name__ == "__main__":
    main()