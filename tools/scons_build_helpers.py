from __future__ import annotations

import sys
from pathlib import Path

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import os
from typing import Any

from tools.paths import get_plugin_dir

from tools.config_manager import config
from tools.git_helpers import (
    check_godot_cpp_submodule_initialized,
    initialize_current_submodule_version,
)
from tools.paths import BUILD_PROFILES_DIR


def find_sources(dirs: list[str], exts: list[str]) -> list[str]:
    """Recursively searches the specified directories for source files."""
    sources: list[str] = []
    for d in dirs:
        dir_path = Path(d)
        # Keep os.walk for now - it handles symlink loops correctly on Windows
        if not dir_path.exists():
            continue
        for root, _, files in os.walk(dir_path, followlinks=False):
            root_path = Path(root)
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    sources.append(str(root_path / file))
    return sources


def verify_godot_cpp_submodule() -> None:
    """Checks if godot-cpp submodule is ready; if not, triggers initialization via git_helpers."""
    if not check_godot_cpp_submodule_initialized():
        print("godot-cpp submodule is not initialized yet.")
        initialize_current_submodule_version()


def setup_build_environment(env: Any, opts: Any) -> None:
    """Configures build profiles and updates environment options."""
    selected_profile = config.getSelectedBuildProfile()
    if selected_profile != "none":
        env["build_profile"] = str(BUILD_PROFILES_DIR / selected_profile)
        print(f"Selected build profile: {selected_profile}\n")
    else:
        print("No selected build profile\n")

    opts.Update(env)


def get_library_filename(env: Any, libname: str, precision: str) -> str:
    """Computes standard library suffix and filename conventions based on platform/target."""
    arch_suffix = f".{env['arch']}" if env.get('arch') and env['arch'] != 'universal' else ''
    threads_val = str(env.get('threads', 'no')).strip().lower()
    threads_suffix = '.threads' if env['platform'] == 'web' and threads_val in ('yes', 'true') else ''

    suffix = f".{env['platform']}.{env['target']}{arch_suffix}{threads_suffix}.{precision}"
    return f"{env.subst('$SHLIBPREFIX')}{libname}{suffix}{env.subst('$SHLIBSUFFIX')}"


def get_target_install_dir(env: Any) -> Path:
    """Resolves and ensures the active target project's installation directory exists."""
    install_dir = get_plugin_dir() / "bin" / str(env["platform"])
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Warning: could not create install dir {install_dir}: {e}", file=sys.stderr)
    return install_dir
