import os
import sys
import re

# Paths relative to script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
TEST_PROJECT_DIR = os.path.join(PARENT_DIR, "test_project")
SRC_DIR = os.path.join(PARENT_DIR, "src")

# Global state for rollback
renamed_paths = []  # tuples of (new_path, old_path)
file_backups = {}   # path -> original content


def sanitize_and_validate_filename(name: str) -> str | None:
    """
    Sanitizes and validates a string to be used as a cross-platform filename/folder name
    and a valid C++ function name. Returns the cleaned name, or None if invalid.
    """

    # Remove leading/trailing whitespace and replace internal whitespace with underscores
    cleaned = re.sub(r"\s+", "_", name.strip())

    # Remove invalid characters (cross-platform unsafe and not allowed in C++ identifiers)
    # Allowed: a-zA-Z0-9_
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "", cleaned)

    # Must not start with a digit
    if not cleaned or cleaned[0].isdigit():
        return None

    # Reserved device names in Windows (case-insensitive)
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    if cleaned.upper() in reserved_names:
        return None

    # Avoid names ending with dot or space (invalid in Windows)
    if cleaned.endswith(".") or cleaned.endswith(" "):
        return None

    return cleaned


def get_old_plugin_name():
    """
    Reads the old plugin name from the first line of dont_touch.txt.
    """
    file_path = os.path.join(PARENT_DIR, "dont_touch.txt")
    with open(file_path, "r") as f:
        lines = f.readlines()
    if not lines:
        raise ValueError("dont_touch.txt is empty.")
    return lines[0].strip()


def verify_paths_exist(paths):
    """
    Verifies that all provided paths exist.
    Exits program if any missing.
    """
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        for path in missing:
            print(f"Error: Required path does not exist: {path}", file=sys.stderr)
        sys.exit(1)


def backup_file(path):
    """
    Saves content of a file for possible rollback.
    """
    with open(path, "r", encoding="utf-8") as f:
        file_backups[path] = f.read()


def restore_file_contents():
    """
    Restores the contents of all backed-up files.
    """
    for path, content in file_backups.items():
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Warning: Could not restore file {path}: {e}", file=sys.stderr)


def rename_path(old_path, new_path):
    """
    Renames a file or directory and tracks it for rollback.
    """
    os.rename(old_path, new_path)
    renamed_paths.append((new_path, old_path))


def rollback_renames():
    """
    Rolls back all renames in reverse order.
    """
    for new_path, old_path in reversed(renamed_paths):
        try:
            os.rename(new_path, old_path)
        except Exception as e:
            print(f"Warning: Could not rollback rename {new_path} -> {old_path}: {e}", file=sys.stderr)


def rename_and_track_paths(old_name, new_name):
    """
    Rename the plugin directory and gdextension file step by step,
    updating and returning the new paths immediately after each rename.
    """
    # Rename plugin directory
    old_plugin_dir = os.path.join(TEST_PROJECT_DIR, old_name)
    new_plugin_dir = os.path.join(TEST_PROJECT_DIR, new_name)
    rename_path(old_plugin_dir, new_plugin_dir)

    # Rename .gdextension file inside the renamed directory
    old_gdextension = os.path.join(new_plugin_dir, f"{old_name}.gdextension")
    new_gdextension = os.path.join(new_plugin_dir, f"{new_name}.gdextension")
    rename_path(old_gdextension, new_gdextension)

    # Paths that do not change:
    register_types_path = os.path.join(SRC_DIR, "register_types.cpp")
    sconstruct_path = os.path.join(PARENT_DIR, "SConstruct")

    return {
        "plugin_dir": new_plugin_dir,
        "gdextension": new_gdextension,
        "register_types": register_types_path,
        "sconstruct": sconstruct_path
    }


def edit_gdextension(path, old_name, new_name):
    backup_file(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace entry_symbol line
    content = re.sub(
        r'entry_symbol\s*=\s*"[^"]*_init"',
        f'entry_symbol = "{new_name}_init"',
        content,
        flags=re.IGNORECASE
    )

    lines = content.splitlines(keepends=True)
    in_libraries = False
    updated_lines = []

    old_name_pattern = re.escape(old_name)
    lib_old_name_pattern = re.compile(rf'lib{old_name_pattern}\.', flags=re.IGNORECASE)
    path_old_name_pattern = re.compile(rf'/{old_name_pattern}\.', flags=re.IGNORECASE)

    for line in lines:
        if line.strip().startswith("[libraries]"):
            in_libraries = True
        if in_libraries:
            # Replace libOldName. with libnewname_lowercase.
            line = lib_old_name_pattern.sub(f'lib{new_name.lower()}.', line)
            # Replace /OldName. with /new_name.
            line = path_old_name_pattern.sub(f'/{new_name}.', line)
        updated_lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)


def edit_register_types(path, new_name):
    backup_file(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match any init function and replace with lowercase new_name + _init
    content = re.sub(
        r'(GDExtensionBool GDE_EXPORT )\w+(_init\s*\()',
        r'\1' + new_name.lower() + r'\2',
        content,
        flags=re.IGNORECASE
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def edit_sconstruct(path, new_name):
    backup_file(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'libname\s*=\s*"[^"]+"',
        f'libname = "{new_name}"',
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def update_dont_touch(new_name):
    path = os.path.join(PARENT_DIR, "dont_touch.txt")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines[0] = new_name + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def recursively_rename_bin_files(bin_path, old_name, new_name):
    if not os.path.exists(bin_path):
        return

    # Case-insensitive patterns
    pattern_lib = re.compile(rf'^lib{re.escape(old_name)}\.', flags=re.IGNORECASE)
    pattern_plain = re.compile(rf'^{re.escape(old_name)}\.', flags=re.IGNORECASE)

    for root, _, files in os.walk(bin_path):
        for filename in files:
            old_file_path = os.path.join(root, filename)
            new_filename = filename

            if pattern_lib.match(new_filename):
                # Replace libOldName. -> libnewname_lowercase.
                new_filename = pattern_lib.sub(f'lib{new_name.lower()}.', new_filename)
            elif pattern_plain.match(new_filename):
                # Replace OldName. -> new_name (keep new_name casing)
                new_filename = pattern_plain.sub(f'{new_name}.', new_filename)

            if new_filename != filename:
                new_file_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_file_path, new_file_path)
                    renamed_paths.append((new_file_path, old_file_path))
                except Exception as e:
                    print(f"Warning: Could not rename file {old_file_path} to {new_file_path}: {e}", file=sys.stderr)


def update_plugin_name(new_name):
    old_name = get_old_plugin_name()

    old_plugin_dir = os.path.join(TEST_PROJECT_DIR, old_name)
    old_gdextension = os.path.join(old_plugin_dir, f"{old_name}.gdextension")
    register_types_path = os.path.join(SRC_DIR, "register_types.cpp")
    sconstruct_path = os.path.join(PARENT_DIR, "SConstruct")

    verify_paths_exist([
        old_plugin_dir,
        old_gdextension,
        register_types_path,
        sconstruct_path
    ])

    try:
        paths = rename_and_track_paths(old_name, new_name)

        bin1_path = os.path.join(PARENT_DIR, "bin")
        bin2_path = os.path.join(paths["plugin_dir"], "bin")

        recursively_rename_bin_files(bin1_path, old_name, new_name)
        recursively_rename_bin_files(bin2_path, old_name, new_name)

        edit_gdextension(paths["gdextension"], old_name, new_name)
        edit_register_types(paths["register_types"], new_name)
        edit_sconstruct(paths["sconstruct"], new_name)

        update_dont_touch(new_name)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Rolling back changes...", file=sys.stderr)
        restore_file_contents()
        rollback_renames()
        print("Rollback complete.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python renaming.py <new_plugin_name>", file=sys.stderr)
        sys.exit(1)

    # Join everything after sys.argv[0] to get the full plugin name
    raw_input_name = " ".join(sys.argv[1:])
    sanitized = sanitize_and_validate_filename(raw_input_name)

    update_plugin_name(sanitized)
