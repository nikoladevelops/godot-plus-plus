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
