import json

from paths import CONFIG_PATH


class _PluginConfig:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path

        self.data = {
            "pluginName": "plugin_name",
            "godotVersion": "4.7",
            "godotPath": "GODOT_ENGINE_PATH_GOES_HERE",
            "godotProjectFolder": "test_project",
            "ltoMode": "none",
            "selectedBuildProfile": "none",
            "extensionApiPath": "godot-cpp/gdextension/extension_api.json"
        }

        if self.config_path.exists():
            self._read_config()
        else:
            self._save_config()

    def _read_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def _save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def reload(self) -> None:
        """Reload configuration from disk into memory."""
        if self.config_path.exists():
            self._read_config()

    def getGodotVersion(self) -> str:
        self.reload()
        return self.data.get("godotVersion", "4.7")

    def setGodotVersion(self, new_version: str) -> None:
        self.data["godotVersion"] = new_version
        self._save_config()

    def getPluginName(self) -> str:
        self.reload()
        return self.data.get("pluginName", "plugin_name")

    def setPluginName(self, new_name: str) -> None:
        self.data["pluginName"] = new_name
        self._save_config()

    def getGodotProjectFolder(self) -> str:
        self.reload()
        return self.data.get("godotProjectFolder", "test_project")

    def setGodotProjectFolder(self, new_folder: str) -> None:
        self.data["godotProjectFolder"] = new_folder
        self._save_config()

    def getLtoMode(self) -> str:
        self.reload()
        return self.data.get("ltoMode", "none")

    def setLtoMode(self, new_lto: str) -> None:
        self.data["ltoMode"] = new_lto
        self._save_config()

    def getSelectedBuildProfile(self) -> str:
        self.reload()
        return self.data.get("selectedBuildProfile", "none")

    def setSelectedBuildProfile(self, new_profile: str) -> None:
        self.data["selectedBuildProfile"] = new_profile
        self._save_config()

    def getExtensionApiPath(self) -> str:
        self.reload()
        return self.data.get("extensionApiPath", "")

    def setExtensionApiPath(self, new_api_path: str) -> None:
        self.data["extensionApiPath"] = str(new_api_path)
        self._save_config()


config = _PluginConfig()
