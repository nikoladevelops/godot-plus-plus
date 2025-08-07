import os
import sys
import subprocess
import re

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
SUBMODULE_PATH = os.path.join(PARENT_DIR, "godot-cpp")
GITMODULES_PATH = os.path.join(PARENT_DIR, ".gitmodules")
DONT_TOUCH_PATH = os.path.join(PARENT_DIR, "dont_touch.txt")

def run_git_command(args, cwd=None):
    """Run a Git command and return (success, output)."""
    result = subprocess.run([
        "git"] + args,
        cwd=cwd,
        text=True,
        capture_output=True
    )
    return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

def fetch_remote_branches():
    """Fetch and return all supported remote branches from godot-cpp."""
    success, _ = run_git_command(["fetch", "--all"], cwd=SUBMODULE_PATH)
    if not success:
        print("Failed to fetch remote branches.")
        sys.exit(1)

    success, output = run_git_command(["branch", "-r"], cwd=SUBMODULE_PATH)
    if not success:
        print("Failed to list remote branches.")
        sys.exit(1)

    raw_branches = [line.strip() for line in output.splitlines() if "->" not in line]
    cleaned = sorted(set(b.replace("origin/", "") for b in raw_branches))

    versioned = sorted([b for b in cleaned if is_supported_version(b)], key=version_sort_key)
    if "master" in cleaned and "master" not in versioned:
        versioned.append("master")

    return versioned

def version_sort_key(version):
    try:
        return tuple(map(int, version.split(".")))
    except:
        return (999, 999)

def is_supported_version(branch):
    """Return True if branch is 4.0+ or master."""
    if branch == "master":
        return True
    try:
        major, minor = map(int, branch.split("."))
        return major >= 4
    except Exception:
        return False

def compute_next_version(versioned_branches):
    """Compute the next semantic version after the highest supported branch."""
    numeric_versions = [v for v in versioned_branches if v != "master"]
    if not numeric_versions:
        return "4.0"
    last = numeric_versions[-1]
    major, minor = map(int, last.split("."))
    return f"{major}.{minor + 1}"

def read_dont_touch_file():
    """Return (plugin_name, version) from dont_touch.txt."""
    try:
        with open(DONT_TOUCH_PATH, "r") as file:
            lines = file.readlines()
            if len(lines) < 2:
                raise ValueError
            plugin_name = lines[0].strip()
            version = lines[1].strip()
            return plugin_name, version
    except Exception:
        print("Could not read dont_touch.txt or file is malformed.")
        sys.exit(1)

def validate_dont_touch_version(branches):
    """Check if current dont_touch.txt version is valid or derived from master."""
    _, version = read_dont_touch_file()
    if version in branches:
        print(f"Currently selected version: {version}")
    else:
        expected_master_version = compute_next_version(branches)
        if version == expected_master_version:
            print(f"Currently selected version: {version} (derived from master)")
        else:
            print(f"Warning: Your dont_touch.txt version '{version}' is not a valid godot-cpp branch.")

def prompt_branch_selection(branches):
    """Prompt user to select a branch by index or name."""
    print("Available branches:")
    for i, branch in enumerate(branches, 1):
        print(f"{i}. {branch}")
    print(f"{len(branches) + 1}. Exit")

    user_input = input("Enter branch number or name: ").strip()

    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(branches):
            return branches[index]
        elif index == len(branches):
            print("Returning to setup.py...")
            sys.exit(0)
        else:
            print("Invalid branch number selected.")
            sys.exit(1)

    if user_input in branches:
        return user_input

    print("Invalid branch name selected.")
    sys.exit(1)

def checkout_branch(branch):
    """Create a local tracking branch and pull latest changes."""
    success, output = run_git_command(["checkout", "-B", branch, f"origin/{branch}"], cwd=SUBMODULE_PATH)
    if not success:
        print(f"Failed to checkout branch: {output}")
        sys.exit(1)

    success, output = run_git_command(["pull"], cwd=SUBMODULE_PATH)
    if not success:
        print("Warning: Pull may have failed or was unnecessary.")
        print(output)

def update_gitmodules_branch(branch):
    """Update the branch field in .gitmodules."""
    try:
        with open(GITMODULES_PATH, "r") as f:
            lines = f.readlines()
    except Exception:
        print("Could not read .gitmodules.")
        sys.exit(1)

    updated_lines = []
    for line in lines:
        if line.strip().startswith("branch ="):
            updated_lines.append(f"\tbranch = {branch}\n")
        else:
            updated_lines.append(line)

    with open(GITMODULES_PATH, "w") as f:
        f.writelines(updated_lines)

def sync_submodule():
    """Run git submodule sync to apply updated config."""
    success, _ = run_git_command(["submodule", "sync"], cwd=PARENT_DIR)
    if not success:
        print("Failed to sync submodule configuration.")
        sys.exit(1)

def update_dont_touch_file(selected_branch, all_branches):
    """Update the second line of dont_touch.txt with the proper version."""
    try:
        with open(DONT_TOUCH_PATH, "r") as f:
            lines = f.readlines()

        if len(lines) < 2:
            raise ValueError

        if selected_branch == "master":
            version = compute_next_version(all_branches)
        else:
            version = selected_branch

        lines[1] = version + "\n"

        with open(DONT_TOUCH_PATH, "w") as f:
            f.writelines(lines)
    except Exception:
        print("Failed to update dont_touch.txt.")
        sys.exit(1)

def update_gdextension_file(plugin_name, version):
    """Update compatibility_minimum in the plugin's .gdextension file."""
    gdextension_path = os.path.join(PARENT_DIR, "test_project", plugin_name, f"{plugin_name}.gdextension")
    if not os.path.isfile(gdextension_path):
        print(f"Error: .gdextension file not found at {gdextension_path}")
        sys.exit(1)

    try:
        with open(gdextension_path, "r") as f:
            content = f.read()

        updated_content = re.sub(
            r'compatibility_minimum\s*=\s*"[^"]*"',
            f'compatibility_minimum = "{version}"',
            content
        )

        with open(gdextension_path, "w") as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Failed to update .gdextension file: {e}")
        sys.exit(1)

def main():
    print("Godot C++ Version Switch Tool\n")

    # Ensure the godot-cpp submodule is initialized
    git_path = os.path.join(SUBMODULE_PATH, ".git")
    if not (os.path.isdir(git_path) or os.path.isfile(git_path)):
        print("godot-cpp submodule not initialized. Initializing now...\n")
        success, output = run_git_command(["submodule", "update", "--init", "--recursive"], cwd=PARENT_DIR)
        if not success:
            print("Failed to initialize godot-cpp submodule:")
            print(output)
            sys.exit(1)

    branches = fetch_remote_branches()

    if not branches:
        print("No supported branches found.")
        sys.exit(1)

    validate_dont_touch_version(branches)
    print()

    selected_branch = prompt_branch_selection(branches)

    print(f"\nSwitching to branch: {selected_branch}\n")
    checkout_branch(selected_branch)
    update_gitmodules_branch(selected_branch)
    sync_submodule()
    update_dont_touch_file(selected_branch, branches)

    plugin_name, version = read_dont_touch_file()
    update_gdextension_file(plugin_name, version)

    print(f"\nSuccessfully switched to godot-cpp branch: {selected_branch}")
    print("You can now commit the submodule update with:")
    print("    git add godot-cpp .gitmodules")
    print(f"    git commit -m \"Update godot-cpp to {selected_branch}\"")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
