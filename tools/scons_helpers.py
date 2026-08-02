import os
import subprocess
import sys
from typing import Literal

from config_manager import config
from paths import PROJECT_ROOT

BuildTarget = Literal["template_debug", "template_release"]


def clear_screen() -> None:
    """Clear the terminal screen cross-platform using subprocess."""
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.run([cmd], check=False)


def run_scons_build(target: BuildTarget) -> None:
    """
    Executes SCons build targeting a specific build profile (template_debug or template_release)
    and streams output in real-time.
    """
    godot_version = config.getGodotVersion()

    if not godot_version:
        print("Error: No Godot version set in config.json.")
        input("\nPress Enter to continue...")
        sys.exit(1)

    scons_args = [
        "scons",
        f"target={target}",
        "compiledb=yes",
        f"api_version={godot_version}"
    ]

    mode_label = "Debug" if target == "template_debug" else "Release"

    print(f"Starting {mode_label} compilation targeting Godot API version {godot_version}...")
    print(f"Executing: {' '.join(scons_args)}\n" + "-" * 50 + "\n")

    try:
        process = subprocess.Popen(
            scons_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        stdout_lines = []
        stderr_lines = []

        # Type guard for linters: guarantees process.stdout is not None
        if process.stdout is not None:
            while True:
                output = process.stdout.readline()
                if output:
                    print(output, end="")
                    stdout_lines.append(output)
                elif process.poll() is not None:
                    break

        remaining_out, remaining_err = process.communicate()
        if remaining_out:
            print(remaining_out, end="")
            stdout_lines.append(remaining_out)
        if remaining_err:
            stderr_lines.append(remaining_err)

        if process.returncode == 0:
            print("\n" + "=" * 50)
            print(f"Compilation finished successfully ({mode_label} Build).")
            print(f"Target API: Godot {godot_version}")
            print(f"A {mode_label.lower()} build for your current OS and architecture was added to your Godot project's folder.")
            print("The compile_commands.json file was also updated for IDE IntelliSense support.")
        else:
            print("\n" + "=" * 50)
            print(f"Compilation FAILED ({mode_label} Build):")
            print("".join(stderr_lines).strip() or "Unknown error occurred.")

    except FileNotFoundError:
        print("Error: 'scons' command not found. Make sure SCons is installed and available in your PATH.")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"An unexpected execution error occurred: {e}")

    input("\nPress Enter to continue...")
