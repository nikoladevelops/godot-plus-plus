import json

from paths import CONFIG_PATH

class _PluginConfig:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path

        self.data = {
            "pluginName": "plugin_name",
            "godotVersion": "4.7",
            "godotPath": "GODOT_ENGINE_PATH_GOES_HERE"
        }

        if self.config_path.exists():
            self._read_config()
        else:
            self._save_config()

    def reload(self) -> None:
        """Reload the configuration from disk into memory."""
        if self.config_path.exists():
            self._read_config()

    def _read_config(self):
        """Internal helper to read the JSON file into memory."""
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def _save_config(self):
        """Internal helper to write the memory dictionary back to JSON."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def getPluginName(self) -> str:
        return self.data.get("pluginName", "")

    def setPluginName(self, new_name: str) -> None:
        self.data["pluginName"] = new_name
        self._save_config()

    def getGodotVersion(self) -> str:
        return self.data.get("godotVersion", "")

    def setGodotVersion(self, new_version: str) -> None:
        self.data["godotVersion"] = new_version
        self._save_config()

    def getGodotPath(self) -> str:
        return self.data.get("godotPath", "")

    def setGodotPath(self, new_path: str) -> None:
        self.data["godotPath"] = new_path
        self._save_config()

config = _PluginConfig()
