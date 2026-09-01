from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TypedDict, cast

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


class SavedPathEntry(TypedDict):
    """Typed entry for a saved Godot path."""
    path: str
    version: str


class PluginConfigData(TypedDict, total=False):
    """Typed structure for config.json contents."""
    pluginName: str
    godotVersion: str
    godotActivePath: str
    savedGodotPaths: list[SavedPathEntry]
    godotProjectFolder: str
    ltoMode: str
    selectedBuildProfile: str
    extensionApiPath: str
    reloadable: bool
    editorTargetMode: str
    debugSymbols: str


def _get_config_path() -> Path:
    """Return CONFIG_PATH without creating an import cycle."""
    # Keep tools.paths as the single source of truth for paths
    from tools.paths import CONFIG_PATH  # noqa: WPS433 - lazy to break cycle

    return CONFIG_PATH


class _PluginConfig:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path: Path = config_path if config_path is not None else _get_config_path()

        # Use cast for empty list so Pyright knows it is list[SavedPathEntry] not list[Unknown]
        self.data: PluginConfigData = {
            "pluginName": "plugin_name",
            "godotVersion": "4.7",
            "godotActivePath": "",
            "savedGodotPaths": cast(list[SavedPathEntry], []),
            "godotProjectFolder": "",
            "ltoMode": "none",
            "selectedBuildProfile": "build_profile.json",
            "extensionApiPath": "godot-cpp/gdextension/extension_api.json",
            "reloadable": True,
            "editorTargetMode": "debug",
            "debugSymbols": "no",
        }

        if self.config_path.exists():
            try:
                self._read_config()
            except (json.JSONDecodeError, OSError) as e:
                print(f"Warning: config.json exists but unreadable ({e}), recreating.", file=sys.stderr)
                self._save_config()
        else:
            self._save_config()

    def _read_config(self) -> None:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                # json.load returns Any, cast to typed dict so subsequent gets are typed
                self.data = cast(PluginConfigData, loaded)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: config.json corrupt ({e}), recreating defaults.", file=sys.stderr)
            self._save_config()

    def _save_config(self) -> None:
        # Guard: never create file with backslashes on POSIX — ensure parent exists and path is sane
        if "\\" in str(self.config_path) and not self.config_path.is_absolute():
            # Defensive: strip stray backslashes that would create weird file at project root
            print(f"Warning: refusing to write config to weird path: {self.config_path!r}", file=sys.stderr)
            return
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = self.config_path.with_suffix(".tmp")
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
                f.write("\n")
            tmp_path.replace(self.config_path)
        except OSError as e:
            print(f"Error: could not save config.json: {e}", file=sys.stderr)

    def reload(self) -> None:
        """Reload configuration from disk into memory."""
        if self.config_path.exists():
            try:
                self._read_config()
            except (json.JSONDecodeError, OSError):
                pass

    def getGodotVersion(self) -> str:
        self.reload()
        return str(self.data.get("godotVersion", "4.7"))

    def setGodotVersion(self, new_version: str) -> None:
        self.data["godotVersion"] = new_version
        self._save_config()

    def getPluginName(self) -> str:
        self.reload()
        return str(self.data.get("pluginName", "plugin_name"))

    def setPluginName(self, new_name: str) -> None:
        self.data["pluginName"] = new_name
        self._save_config()

    def getGodotProjectFolder(self) -> str:
        self.reload()
        return str(self.data.get("godotProjectFolder", "test_project"))

    def setGodotProjectFolder(self, new_folder: str) -> None:
        self.data["godotProjectFolder"] = new_folder
        self._save_config()

    def getLtoMode(self) -> str:
        self.reload()
        return str(self.data.get("ltoMode", "none"))

    def setLtoMode(self, new_lto: str) -> None:
        self.data["ltoMode"] = new_lto
        self._save_config()

    def getSelectedBuildProfile(self) -> str:
        self.reload()
        return str(self.data.get("selectedBuildProfile", ""))

    def setSelectedBuildProfile(self, new_profile: str) -> None:
        self.data["selectedBuildProfile"] = new_profile
        self._save_config()

    def getExtensionApiPath(self) -> str:
        self.reload()
        return str(self.data.get("extensionApiPath", ""))

    def setExtensionApiPath(self, new_api_path: str) -> None:
        self.data["extensionApiPath"] = str(new_api_path)
        self._save_config()

    def getReloadable(self) -> bool:
        self.reload()
        return bool(self.data.get("reloadable", True))

    def setReloadable(self, is_reloadable: bool) -> None:
        self.data["reloadable"] = is_reloadable
        self._save_config()

    def getEditorTargetMode(self) -> str:
        self.reload()
        return str(self.data.get("editorTargetMode", "debug"))

    def setEditorTargetMode(self, mode: str) -> None:
        self.data["editorTargetMode"] = mode
        self._save_config()

    def getGodotActivePath(self) -> str:
        """Returns the active Godot engine executable path."""
        self.reload()
        return str(self.data.get("godotActivePath", ""))

    def setGodotActivePath(self, new_path: str) -> None:
        """Sets the active godotActivePath in configuration."""
        self.data["godotActivePath"] = str(new_path).strip()
        self._save_config()

    def getSavedGodotPaths(self) -> list[SavedPathEntry]:
        """Returns the saved Godot path dictionaries: [{'path': '...', 'version': '...'}, ...]"""
        self.reload()
        raw: object = self.data.get("savedGodotPaths", [])
        if isinstance(raw, list):
            result: list[SavedPathEntry] = []
            for entry in raw:
                if isinstance(entry, dict):
                    # Cast to dict[str, object] so get is typed as str -> object
                    typed_entry = cast(dict[str, object], entry)
                    path_val = typed_entry.get("path")
                    ver_val = typed_entry.get("version")
                    if isinstance(path_val, str) and isinstance(ver_val, str):
                        result.append({"path": path_val, "version": ver_val})
                    elif isinstance(path_val, str):
                        ver_str = str(ver_val) if ver_val is not None else "Unknown"
                        result.append({"path": path_val, "version": ver_str})
            return result
        return []

    def addSavedGodotPath(self, new_path: str, version: str = "Unknown") -> None:
        """Adds or updates a path entry inside savedGodotPaths."""
        self.reload()
        raw_paths: object = self.data.get("savedGodotPaths", [])
        typed_paths: list[SavedPathEntry] = []
        if isinstance(raw_paths, list):
            for item in raw_paths:
                if isinstance(item, dict):
                    item_dict = cast(dict[str, object], item)
                    path_obj = item_dict.get("path")
                    ver_obj = item_dict.get("version")
                    if isinstance(path_obj, str) and isinstance(ver_obj, str):
                        typed_paths.append({"path": path_obj, "version": ver_obj})

        cleaned_path = str(new_path).strip()

        if not cleaned_path:
            return

        for entry in typed_paths:
            if entry["path"] == cleaned_path:
                entry["version"] = version
                self.data["savedGodotPaths"] = typed_paths
                self._save_config()
                return

        typed_paths.append({"path": cleaned_path, "version": version})
        self.data["savedGodotPaths"] = typed_paths
        self._save_config()

    def removeSavedGodotPath(self, path_to_remove: str) -> None:
        """
        Removes a path entry from savedGodotPaths.
        If the path being removed is currently active, clears godotActivePath to "".
        """
        self.reload()
        cleaned_remove = str(path_to_remove).strip()
        raw_paths: object = self.data.get("savedGodotPaths", [])

        if isinstance(raw_paths, list):
            new_paths: list[SavedPathEntry] = []
            for item in raw_paths:
                if isinstance(item, dict):
                    item_dict = cast(dict[str, object], item)
                    p_path = item_dict.get("path")
                    p_ver = item_dict.get("version")
                    if isinstance(p_path, str) and p_path != cleaned_remove and isinstance(p_ver, str):
                        new_paths.append({"path": p_path, "version": p_ver})
                    elif isinstance(p_path, str) and p_path != cleaned_remove:
                        # Keep entry even if version is missing, normalize it
                        ver_str = str(p_ver) if isinstance(p_ver, str) else "Unknown"
                        new_paths.append({"path": p_path, "version": ver_str})
            self.data["savedGodotPaths"] = new_paths

        if self.data.get("godotActivePath") == cleaned_remove:
            self.data["godotActivePath"] = ""

        self._save_config()

    def getDebugSymbols(self) -> str:
        self.reload()
        val: object = self.data.get("debugSymbols", "no")
        return str(val) if isinstance(val, str) else "no"

    def setDebugSymbols(self, mode: str) -> None:
        self.data["debugSymbols"] = mode.strip().lower()
        self._save_config()


config = _PluginConfig()
