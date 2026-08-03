from pathlib import Path
from typing import Dict, List


def update_section_in_gdextension(
    file_path: Path, section_name: str, key_value_pairs: Dict[str, str]
) -> None:
    """
    Safely replaces or appends a target section (e.g., [icons]) inside a .gdextension INI file.

    :param file_path: Path object pointing to the .gdextension file.
    :param section_name: Name of the INI section without brackets (e.g., 'icons').
    :param key_value_pairs: Dictionary of keys and formatted values to write under the section.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"GDExtension file not found at: {file_path}")

    lines = file_path.read_text(encoding="utf-8").splitlines()

    new_lines: List[str] = []
    inside_target_section = False
    target_header = f"[{section_name}]"

    # Line-by-line parsing state machine to strip existing section
    for line in lines:
        stripped = line.strip()
        if stripped == target_header:
            inside_target_section = True
            continue

        # If we encounter another section header while inside the target section, exit strip mode
        if inside_target_section and stripped.startswith("[") and stripped.endswith("]"):
            inside_target_section = False

        if not inside_target_section:
            new_lines.append(line)

    clean_content = "\n".join(new_lines).rstrip()

    # Build the fresh section block
    section_entries = [
        f'{key} = "{value}"' for key, value in sorted(key_value_pairs.items())
    ]
    new_section_block = f"\n\n{target_header}\n" + "\n".join(section_entries) + "\n"

    final_content = clean_content + new_section_block
    file_path.write_text(final_content, encoding="utf-8")


def update_icons_in_gdextension(
    file_path: Path, icon_mappings: Dict[str, str]
) -> None:
    """
    Helper shortcut specifically for updating the [icons] section in a .gdextension file.

    :param file_path: Path object to the target .gdextension manifest.
    :param icon_mappings: Dict where keys are C++ Node Class Names and values are res:// paths.
                          Example: {'ItemData': 'res://plugin_name/icons/ItemData.svg'}
    """
    update_section_in_gdextension(file_path, "icons", icon_mappings)
