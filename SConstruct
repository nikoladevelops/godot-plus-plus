#!/usr/bin/env python
import os
import sys
import platform

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
localEnv = Environment(tools=["default"], PLATFORM="")

# Custom configuration file
customs = ["custom.py"]
customs = [os.path.abspath(path) for path in customs]

# Define configuration options
opts = Variables(customs, ARGUMENTS)

# For source files (C++ files)
opts.Add('source_dirs', 'List of source directories (comma-separated)', 'src')
opts.Add('source_exts', 'List of source file extensions (comma-separated)', '.cpp,.c,.cc,.cxx')

# For header files
opts.Add('include_dirs', 'List of include directories (comma-separated)', 'include')

# For generated documentation source files
opts.Add('doc_output_dir', 'Directory for documentation output', 'gen')

# Build parameters with defaults
opts.Add(EnumVariable('platform', 'Target platform', platform.system().lower(), allowed_values=('linux', 'windows', 'macos', 'ios', 'android', 'web')))
opts.Add(EnumVariable('target', 'Compilation target', 'template_debug', allowed_values=('template_debug', 'template_release')))
opts.Add(EnumVariable('arch', 'Architecture', 'x86_64', allowed_values=('x86_32', 'x86_64', 'arm32', 'arm64', 'rv64', 'wasm32')))
opts.Add(EnumVariable('precision', 'Floating-point precision', 'single', allowed_values=('single', 'double')))
opts.Add(EnumVariable('threads', 'Enable WebAssembly threads', 'disabled', allowed_values=('enabled', 'disabled')))

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

# Convert threads to boolean for godot-cpp
env['threads_enabled'] = env['threads'] == 'enabled'  # Convert enabled/disabled to True/False
env['threads'] = env['threads_enabled']  # Pass boolean to godot-cpp/SConstruct

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
suffix = f".{env['target']}"
if env['platform'] in ['linux', 'android'] and env['arch'] in ['x86_32', 'x86_64', 'arm32', 'arm64', 'rv64']:
    suffix += f".{env['arch']}"
if env['platform'] == 'windows' and env['arch'] in ['x86_32', 'x86_64', 'arm64']:
    suffix += f".{env['arch']}"
if env['platform'] == 'web':
    suffix += '.wasm32'
    if env['threads'] == 'enabled':
        suffix += '.threads'
    else:
        suffix += '.nothreads'
if env['precision'] == 'double' and env['platform'] not in ['macos', 'ios']:
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
        if env['precision'] == 'double':
            arch_suffix += '.double'
        arch_lib_filename = f"{env.subst('$SHLIBPREFIX')}{libname}{arch_suffix}{env.subst('$SHLIBSUFFIX')}"
        arch_lib = arch_env.SharedLibrary(
            f"bin/{env['platform']}/{arch_lib_filename}",
            source=sources
        )
        temp_libs.append(arch_lib)
    
    # Create .framework for macOS or .xcframework for iOS
    if env['platform'] == 'macos':
        framework_name = f"lib{libname}.macos.template_{env['target']}.framework"
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
            f"bin/ios/lib{libname}.ios.template_{env['target']}.xcframework",
            temp_libs,
            "xcodebuild -create-xcframework $SOURCES -output $TARGET"
        )
else:
    # For other platforms, build a single shared library
    library = env.SharedLibrary(
        f"bin/{env['platform']}/{lib_filename}",
        source=sources
    )

# Build godot-cpp as .framework/.xcframework for macOS/iOS dependencies
if env['platform'] in ['macos', 'ios']:
    godot_cpp_libs = []
    for arch in arches:
        godot_cpp_env = env.Clone()
        godot_cpp_env['arch'] = arch
        godot_cpp_suffix = f".{env['target']}.{arch}"
        if env['precision'] == 'double':
            godot_cpp_suffix += '.double'
        godot_cpp_lib = godot_cpp_env.StaticLibrary(
            f"bin/{env['platform']}/libgodot-cpp.{env['platform']}.template_{godot_cpp_suffix}.a",
            source=Glob("godot-cpp/src/*.cpp")
        )
        godot_cpp_libs.append(godot_cpp_lib)
    
    if env['platform'] == 'macos':
        godot_cpp_framework = env.Command(
            f"bin/macos/libgodot-cpp.macos.template_{env['target']}.framework",
            godot_cpp_libs,
            """
            mkdir -p $TARGET/libgodot-cpp.macos.template_{env['target']}.framework && \
            lipo -create $SOURCES -output $TARGET/libgodot-cpp.macos.template_{env['target']}.framework/libgodot-cpp && \
            cp -r godot-cpp/misc/macos/Info.plist $TARGET/Info.plist
            """
        )
    else:  # iOS
        godot_cpp_framework = env.Command(
            f"bin/ios/libgodot-cpp.ios.template_{env['target']}.xcframework",
            godot_cpp_libs,
            "xcodebuild -create-xcframework $SOURCES -output $TARGET"
        )

# Install the library
install_dir = f"{projectdir}/{libname}/bin/{env['platform']}/"
copy = env.Install(install_dir, library)

# Set default targets
default_args = [library, copy]
Default(*default_args)