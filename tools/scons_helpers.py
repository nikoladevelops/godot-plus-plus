from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

# Bootstrap so absolute imports work whether run as `python tools/foo.py` or `python -m tools.foo`
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.config_manager import config
from tools.paths import PROJECT_ROOT, TOOLS_DIR

BuildTarget = Literal["template_debug", "template_release"]


def _resolve_scons_command() -> list[str]:
    """Find the scons binary, or fall back to python -m scons if it's not on PATH."""
    scons_exe = shutil.which("scons")
    if scons_exe:
        # Windows pip creates scons.bat which needs a shell, so use -m instead
        if scons_exe.lower().endswith(".bat"):
            return [sys.executable, "-m", "scons"]
        return [scons_exe]
    return [sys.executable, "-m", "scons"]


def pause(msg: str = "Press Enter to continue...") -> None:
    """Pause until the user hits Enter. Handles pipes and Ctrl+C quietly."""
    try:
        _ = input(msg)
    except (EOFError, KeyboardInterrupt):
        pass


def clear_screen() -> None:
    """Clear the screen. Does nothing if it fails, so the menu never crashes."""
    try:
        if os.name == "nt":
            import platform as _platform

            # Tests sometimes fake os.name on Linux, skip the actual cls call there
            if _platform.system() != "Windows":
                return
            _ = subprocess.run("cls", shell=True, check=False)  # noqa: S602
        else:
            if shutil.which("clear"):
                _ = subprocess.run(["clear"], check=False)
            else:
                # No clear command, use ANSI sequence
                _ = sys.stdout.write("\033[2J\033[H")
                _ = sys.stdout.flush()
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        _ = exc
        pass


def _stream_popen(args: list[str], cwd: str) -> tuple[int, str, str]:
    """Run a command, print its output live, and return the result."""
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd,
    )
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    if process.stdout is not None:
        while True:
            output: str = process.stdout.readline()
            if output:
                print(output, end="")
                stdout_lines.append(output)
            elif process.poll() is not None:
                break
    remaining_out: str | None
    remaining_err: str | None
    remaining_out, remaining_err = process.communicate()
    if remaining_out:
        print(remaining_out, end="")
        stdout_lines.append(remaining_out)
    if remaining_err:
        stderr_lines.append(remaining_err)
    return process.returncode or 0, "".join(stdout_lines), "".join(stderr_lines)


def run_tool_script(script_filename: str) -> None:
    """Run one of the tool scripts in tools/."""
    script_path = TOOLS_DIR / script_filename
    result = subprocess.run([sys.executable, str(script_path)], check=False)

    if result.returncode != 0:
        print(f"Tool '{script_filename}' exited with code {result.returncode}.")
        pause()


def run_scons_build(target: BuildTarget) -> None:
    """Build the GDExtension with SCons for the given target."""
    godot_version = config.getGodotVersion()
    debug_symbols = config.getDebugSymbols()

    # Only apply LTO for template_release builds.
    # Debug builds MUST use lto=none for fast compilation and debugging.
    if target == "template_debug":
        lto_mode = "none"
    else:
        lto_mode = config.getLtoMode()

    if not godot_version:
        print("Error: No Godot version set in config.json.")
        print("Please set a target version via Godot Engine & Version Settings.")
        pause("\nPress Enter to continue...")
        sys.exit(1)

    scons_base = _resolve_scons_command()
    scons_args = scons_base + [
        f"target={target}",
        "compiledb=yes",
        f"api_version={godot_version}",
        f"lto={lto_mode}",
        f"debug_symbols={debug_symbols}",
    ]

    mode_label = "Debug" if target == "template_debug" else "Release"

    print(f"Starting {mode_label} compilation targeting Godot API version {godot_version}...")
    print(f"Debug Symbols: {debug_symbols.upper()}")
    if target == "template_debug" and config.getLtoMode() != "none":
        print("Note: LTO is automatically disabled for Debug builds to ensure fast compilation.")
    else:
        print(f"LTO Optimization Mode: {lto_mode}")

    print(f"Executing: {' '.join(scons_args)}\n" + "-" * 50 + "\n")

    try:
        returncode, _, stderr = _stream_popen(scons_args, str(PROJECT_ROOT))
        if returncode == 0:
            print("\n" + "=" * 50)
            print(f"Compilation finished successfully ({mode_label} Build).")
            print(f"Target API: Godot {godot_version} | LTO: {lto_mode} | Debug Symbols: {debug_symbols}")
            print(f"A {mode_label.lower()} build was added to the bin/ folder.")
            print("The compile_commands.json file was also updated for IDE IntelliSense support.")
        else:
            print("\n" + "=" * 50)
            print(f"Compilation FAILED ({mode_label} Build):")
            print(stderr.strip() or "Unknown error occurred. Check output above for compiler messages.")
    except FileNotFoundError:
        print("Error: 'scons' command not found. Make sure SCons is installed and available in your PATH.")
        print("Try: python -m pip install scons")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"An unexpected execution error occurred: {e}")

    pause("\nPress Enter to continue...")


def run_scons_clean() -> None:
    """Run scons -c to clean build files."""

    scons_args = _resolve_scons_command() + [
        "-c",
    ]

    print("Starting SCons clean process")
    print(f"Executing: {' '.join(scons_args)}\n" + "-" * 50 + "\n")

    try:
        returncode, _, stderr = _stream_popen(scons_args, str(PROJECT_ROOT))
        if returncode == 0:
            print("\n" + "=" * 50)
            print("SCons clean finished successfully.")
            print("All built targets and generated artifacts mapped by SCons have been cleared.")
        else:
            print("\n" + "=" * 50)
            print("SCons clean FAILED:")
            print(stderr.strip() or "Unknown error occurred.")
    except FileNotFoundError:
        print("Error: 'scons' command not found. Make sure SCons is installed and available in your PATH.")
        print("Try: python -m pip install scons")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"An unexpected execution error occurred: {e}")
