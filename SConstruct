#!/usr/bin/env python
import os
import sys

from methods import print_error

# Function to recursively find all .cpp files in the given directories
def find_sources(dirs, exts):
    """
    Recursively searches the specified directories for .cpp files.
    
    Args:
        dirs (list): List of directory paths to search.
        exts (list): List of file extensions that are acceptable and should contain c++ code.
    Returns:
        list: List of full paths to .cpp files found.
    """
    sources = []
    for dir in dirs:
        for root, _, files in os.walk(dir):
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    sources.append(os.path.join(root, file))
    return sources

# Configuration
libname = "PLUGIN_NAME_GOES_HERE"  # Replace with your plugin name
projectdir = "test_project"      # Directory where the built library will be installed

# Set up the environment
localEnv = Environment(tools=["default"], PLATFORM="")

# Custom configuration file
customs = ["custom.py"]
customs = [os.path.abspath(path) for path in customs]

# Define configuration options
opts = Variables(customs, ARGUMENTS)

# For source files (c++ files)
opts.Add('source_dirs', 'List of source directories (comma-separated)', 'src')
opts.Add('source_exts', 'List of source file extensions (comma-separated)', '.cpp,.c,.cc,.cxx')

# For header files
opts.Add('include_dirs', 'List of include directories (comma-separated)', 'include')

# For generated documentation source files
opts.Add('doc_output_dir', 'Directory for documentation output', 'gen')

# Update the environment with the options
opts.Update(localEnv)

# Generate help text for the options
Help(opts.GenerateHelpText(localEnv))

# Clone the environment for further modifications
env = localEnv.Clone()

# Process the configuration options
source_dirs = env['source_dirs'].split(',')   # Convert comma-separated string to list
source_exts = env['source_exts'].split(',')   # Convert comma-separated string to list

include_dirs = env['include_dirs'].split(',') # Convert comma-separated string to list

doc_output_dir = env['doc_output_dir']        # Directory for documentation output

# Check for godot-cpp submodule
if not (os.path.isdir("godot-cpp") and os.listdir("godot-cpp")):
    print_error("""godot-cpp is not available within this folder, as Git submodules haven't been initialized.
Run the following command to download godot-cpp:

    git submodule update --init --recursive""")
    sys.exit(1)

# Include godot-cpp SConstruct
env = SConscript("godot-cpp/SConstruct", {"env": env, "customs": customs})

# Append include directories to CPPPATH
env.Append(CPPPATH=include_dirs)

# Find all .cpp files recursively in the specified source directories
sources = find_sources(source_dirs, source_exts)

# Handle documentation generation if applicable
if env["target"] in ["editor", "template_debug"]:
    try:
        doc_output_file = os.path.join(doc_output_dir, 'doc_data.gen.cpp')
        doc_data = env.GodotCPPDocData(doc_output_file, source=Glob("doc_classes/*.xml"))
        sources.append(doc_data)
    except AttributeError:
        print("Not including class reference as we're targeting a pre-4.3 baseline.")

# Determine the library filename
suffix = env['suffix'].replace(".dev", "").replace(".universal", "")
lib_filename = "{}{}{}{}".format(env.subst('$SHLIBPREFIX'), libname, suffix, env.subst('$SHLIBSUFFIX'))

# Build the shared library
library = env.SharedLibrary(
    "bin/{}/{}".format(env['platform'], lib_filename),
    source=sources,
)

# Install the library
copy = env.Install("{}/{}/bin/{}/".format(projectdir, libname, env["platform"]), library)

# Set default targets
default_args = [library, copy]
Default(*default_args)