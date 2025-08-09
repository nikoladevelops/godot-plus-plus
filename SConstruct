#!/usr/bin/env python
import os
import sys

from methods import print_error

# Function to recursively find .cpp files in the given directories
def find_sources(dirs, exts):
    """
    Recursively searches the specified directories for .cpp files.
    
    Args:
        dirs (list): List of directory paths to search.
        exts (list): List of file extensions that are acceptable and should contain C++ code.
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
libname = "plugin_name_goes_here"  # Replace with your plugin name
projectdir = "test_project"        # Directory where the built library will be installed

# Set up the environment
env = Environment(tools=["default"], PLATFORM="")

# Custom configuration file
customs = ["custom.py"]
customs = [os.path.abspath(path) for path in customs]

# Define GDExtension-specific options
opts = Variables(customs, ARGUMENTS)
opts.Add('source_dirs', 'List of source directories (comma-separated)', 'src')
opts.Add('source_exts', 'List of source file extensions (comma-separated)', '.cpp,.c,.cc,.cxx')
opts.Add('include_dirs', 'List of include directories (comma-separated)', 'include')
opts.Add('doc_output_dir', 'Directory for documentation output', 'gen')

# Update the environment with the options
opts.Update(env)

# Generate help text for the options
Help(opts.GenerateHelpText(env))

# Check for godot-cpp submodule
if not (os.path.isdir("godot-cpp") and os.listdir("godot-cpp")):
    print_error("""godot-cpp is not available within this folder, as Git submodules haven't been initialized.
Run the following command to download godot-cpp:

    git submodule update --init --recursive""")
    sys.exit(1)

# Include godot-cpp SConstruct, passing all command-line arguments
env = SConscript("godot-cpp/SConstruct", {"env": env, "customs": customs})

# Process GDExtension-specific options
source_dirs = env['source_dirs'].split(',')   # Convert comma-separated string to list
source_exts = env['source_exts'].split(',')   # Convert comma-separated string to list
include_dirs = env['include_dirs'].split(',') # Convert comma-separated string to list
doc_output_dir = env['doc_output_dir']        # Directory for documentation output

# Append include directories to CPPPATH
env.Append(CPPPATH=include_dirs)

# Find all .cpp files recursively in the specified source directories
sources = find_sources(source_dirs, source_exts)

# Handle documentation generation if applicable
if env.get("target") in ["editor", "template_debug"]:
    try:
        doc_output_file = os.path.join(doc_output_dir, 'doc_data.gen.cpp')
        doc_data = env.GodotCPPDocData(doc_output_file, source=Glob("doc_classes/*.xml"))
        sources.append(doc_data)
    except AttributeError:
        print("Not including class reference as we're targeting a pre-4.3 baseline.")

# Determine the library filename using godot-cpp naming
suffix = f".{env['target']}"
if env['platform'] in ['linux', 'android'] and env['arch'] in ['x86_32', 'x86_64', 'arm32', 'arm64', 'rv64']:
    suffix += f".{env['arch']}"
if env['platform'] == 'windows' and env['arch'] in ['x86_32', 'x86_64', 'arm64']:
    suffix += f".{env['arch']}"
if env['platform'] == 'web':
    suffix += f".wasm32{env['suffix']}"  # Use godot-cpp's suffix (.threads/.nothreads)
if env['platform'] not in ['macos', 'ios'] and env.get('precision') == 'double':
    suffix += '.double'

lib_filename = f"{env.subst('$SHLIBPREFIX')}{libname}{suffix}{env.subst('$SHLIBSUFFIX')}"

# Build the shared library
library = None
if env['platform'] in ['macos', 'ios']:
    # For macOS and iOS, build for multiple architectures and create framework/xcframework
    arches = ['x86_64', 'arm64'] if env['platform'] == 'macos' else ['arm64', 'x86_64']
    temp_libs = []
    for arch in arches:
        arch_env = env.Clone()
        arch_env['arch'] = arch
        arch_suffix = f".{env['target']}.{arch}"
        if env.get('precision') == 'double':
            arch_suffix += '.double'
        arch_lib_filename = f"{env.subst('$SHLIBPREFIX')}{libname}{arch_suffix}{env.subst('$SHLIBSUFFIX')}"
        arch_lib = arch_env.SharedLibrary(
            f"bin/{env['platform']}/{arch_lib_filename}",
            source=sources
        )
        temp_libs.append(arch_lib)
    
    # Create .framework for macOS or .xcframework for iOS
    if env['platform'] == 'macos':
        framework_name = f"lib{libname}.macos.{env['target']}.framework"
        library = env.Command(
            f"bin/macos/{framework_name}",
            temp_libs,
            """
            mkdir -p $TARGET/$framework_name && \
            lipo -create $SOURCES -output $TARGET/$framework_name/$libname && \
            cp -r godot-cpp/misc/macos/Info.plist $TARGET/Info.plist
            """
        )
    else:  # iOS
        library = env.Command(
            f"bin/ios/lib{libname}.ios.{env['target']}.xcframework",
            temp_libs,
            "xcodebuild -create-xcframework $SOURCES -output $TARGET"
        )
else:
    # For other platforms, build a single shared library
    library = env.SharedLibrary(
        f"bin/{env['platform']}/{lib_filename}",
        source=sources
    )

# Install the library
install_dir = f"{projectdir}/{libname}/bin/{env['platform']}/"
copy = env.Install(install_dir, library)

# Set default targets
default_args = [library, copy]
Default(*default_args)