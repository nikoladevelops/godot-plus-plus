from pathlib import Path

# Absolute path to the directory containing this script
TOOLS_DIR = Path(__file__).resolve().parent

# Absolute path to the project root (one directory up from tools)
PROJECT_ROOT = TOOLS_DIR.parent

# This is where the config json lives
CONFIG_PATH = TOOLS_DIR / "config.json"

# This is where godot-cpp submodule is
SUBMODULE_PATH = PROJECT_ROOT / "godot-cpp"

# This is where all extension_api json files are located
GDEXTENSION_APIS_PATH = SUBMODULE_PATH / "gdextension"

# This is where you put icons for your nodes and they automatically get transferred to your godot project
ICONS_SOURCE_DIR = PROJECT_ROOT / "icons"

# This is where the build profiles are stored
BUILD_PROFILES_DIR = PROJECT_ROOT / "build_profiles"

# This is where the SConstruct file for scons is
SCONSTRUCT_PATH = PROJECT_ROOT / "SConstruct"


def get_godot_project_dir() -> Path:
    """Returns the absolute Path to the Godot project directory."""
    from config_manager import config
    return PROJECT_ROOT / config.getGodotProjectFolder()


def get_plugin_dir() -> Path:
    """Returns the absolute Path to the plugin folder inside the Godot project."""
    from config_manager import config
    return get_godot_project_dir() / config.getPluginName()


def get_gdextension_file_path() -> Path:
    """Returns the absolute Path to the target .gdextension manifest file."""
    from config_manager import config
    plugin_name = config.getPluginName()
    return get_plugin_dir() / f"{plugin_name}.gdextension"

def get_selected_extension_api_path() -> Path:
    """
    Returns the absolute Path to the active extension_api JSON file by combining
    PROJECT_ROOT with the relative path stored in config.
    """
    from config_manager import config
    rel_path_str = config.getExtensionApiPath()
    if rel_path_str:
        return PROJECT_ROOT / rel_path_str

    # Fallback default if no path is stored in config yet
    return GDEXTENSION_APIS_PATH / "extension_api.json"
