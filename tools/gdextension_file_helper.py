import re
from pathlib import Path
from typing import Dict, List, Optional

from paths import get_gdextension_file_path


def set_editor_target_mode(mode: str, file_path: Optional[Path] = None) -> None:
    """
    Updates all `.debug` target entries in [libraries] and [dependencies] inside the
    .gdextension file to point to either 'template_debug' binaries (mode="debug")
    or 'template_release' binaries (mode="release").
    """
    target_path = get_target_gdextension_path(file_path)

    if not target_path.exists():
        raise FileNotFoundError(f"GDExtension file not found at: {target_path}")

    content = target_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    updated_lines = []

    current_section = ""
    in_debug_block = False

    for line in lines:
        stripped = line.strip()

        # Track sections
        if stripped.startswith("[") and stripped.endswith("]"):
            current_section = stripped.lower()
            in_debug_block = False
            updated_lines.append(line)
            continue

        # Only process inside [libraries] and [dependencies]
        if current_section in ["[libraries]", "[dependencies]"]:
            # Check for starting key declarations like `ios.debug = {` or `windows.debug.x86_64 = ...`
            if "=" in line and not stripped.startswith(";"):
                key_part = line.split("=", 1)[0].strip()
                in_debug_block = ".debug" in key_part

            # If we are inside a .debug key assignment or inside a multi-line .debug block
            if in_debug_block:
                if mode == "release":
                    line = line.replace("template_debug", "template_release")
                else:
                    line = line.replace("template_release", "template_debug")

            # Reset block state when multi-line dictionary closes
            if "}" in line:
                in_debug_block = False

        updated_lines.append(line)

    target_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def set_reloadable(reloadable: bool, file_path: Optional[Path] = None) -> None:
    """
    Updates or inserts the `reloadable` key under [configuration]
    in the .gdextension manifest using strict lowercase booleans (reloadable = true / false).
    """
    target_path = get_target_gdextension_path(file_path)

    if not target_path.exists():
        raise FileNotFoundError(f"GDExtension file not found at: {target_path}")

    content = target_path.read_text(encoding="utf-8")
    value_str = "true" if reloadable else "false"

    # Matches reloadable = true or reloadable = false (case-insensitive search)
    pattern = r'(reloadable\s*=\s*)(true|false|True|False)'

    if re.search(pattern, content):
        updated_content = re.sub(pattern, f'\\g<1>{value_str}', content)
    else:
        if "[configuration]" in content:
            updated_content = content.replace(
                "[configuration]\n",
                f'[configuration]\nreloadable = {value_str}\n',
                1,
            )
        else:
            updated_content = f'[configuration]\nreloadable = {value_str}\n\n' + content

    target_path.write_text(updated_content, encoding="utf-8")

def get_target_gdextension_path(custom_path: Optional[Path] = None) -> Path:
    """Utility to resolve custom_path or default to get_gdextension_file_path()."""
    return custom_path if custom_path is not None else get_gdextension_file_path()


def set_compatibility_minimum(
    min_version: str, file_path: Optional[Path] = None
) -> None:
    """
    Updates or inserts the `compatibility_minimum` key under [configuration]
    in the .gdextension manifest. Defaults to paths.get_gdextension_file_path().
    """
    target_path = get_target_gdextension_path(file_path)

    if not target_path.exists():
        raise FileNotFoundError(f"GDExtension file not found at: {target_path}")

    content = target_path.read_text(encoding="utf-8")
    pattern = r'(compatibility_minimum\s*=\s*")[^"]*(")'

    if re.search(pattern, content):
        updated_content = re.sub(pattern, f'\\g<1>{min_version}\\g<2>', content)
    else:
        if "[configuration]" in content:
            updated_content = content.replace(
                "[configuration]\n",
                f'[configuration]\ncompatibility_minimum = "{min_version}"\n',
                1,
            )
        else:
            updated_content = f'[configuration]\ncompatibility_minimum = "{min_version}"\n\n' + content

    target_path.write_text(updated_content, encoding="utf-8")


def update_section_in_gdextension(
    section_name: str, key_value_pairs: Dict[str, str], file_path: Optional[Path] = None
) -> None:
    """
    Safely replaces or appends a target section (e.g., [icons]) inside a .gdextension file.
    """
    target_path = get_target_gdextension_path(file_path)

    if not target_path.exists():
        raise FileNotFoundError(f"GDExtension file not found at: {target_path}")

    lines = target_path.read_text(encoding="utf-8").splitlines()

    new_lines: List[str] = []
    inside_target_section = False
    target_header = f"[{section_name}]"

    for line in lines:
        stripped = line.strip()
        if stripped == target_header:
            inside_target_section = True
            continue

        if inside_target_section and stripped.startswith("[") and stripped.endswith("]"):
            inside_target_section = False

        if not inside_target_section:
            new_lines.append(line)

    clean_content = "\n".join(new_lines).rstrip()

    section_entries = [
        f'{key} = "{value}"' for key, value in sorted(key_value_pairs.items())
    ]
    new_section_block = f"\n\n{target_header}\n" + "\n".join(section_entries) + "\n"

    final_content = clean_content + new_section_block
    target_path.write_text(final_content, encoding="utf-8")


def update_icons_in_gdextension(
    icon_mappings: Dict[str, str], file_path: Optional[Path] = None
) -> None:
    """
    Helper shortcut specifically for updating the [icons] section in a .gdextension file.
    """
    update_section_in_gdextension("icons", icon_mappings, file_path=file_path)
