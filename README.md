# Godot++: The Ultimate C++ GDExtension Template

The easiest way to develop, compile, and distribute C++ plugins for Godot Engine.

Godot++ is a user-friendly Godot GDExtension template designed to streamline C++ development for the Godot Engine. Unlike complex manual configurations, this template uses a powerful `setup.py` automation script, making it the perfect choice for any developer.

Stop fighting with build systems and start building high-performance plugins today.

---

## Why Choose Godot++?

- **Zero Configuration:** Use the automated `setup.py` to initialize submodules, set library names, and configure entry points instantly.

- **Cross-Platform Automation:** Built-in GitHub Actions compile your code for `Windows`, `macOS`, `Linux`, `Android`, `iOS`, and `Web` automatically.

- **Performance Optimized:** Automatically applies Link-Time Optimization (LTO) for high-performance release builds.

- **Professional Workflow:** Full support for `compile_commands.json` to enable high-quality IntelliSense via Clangd.

- **Production Ready:** End-users get a simple, plug-and-play experience. See this template in action with [BlastBullets2D](https://github.com/nikoladevelops/godot-blast-bullets-2d).

---

## Built-In Tooling

Beyond simple compilation, Godot++ includes a comprehensive suite of helper scripts:

- **Build Management:** Debug/Release profiles, LTO toggling, and clean-up tools.

- **Plugin Maintenance:** Rename plugins, update icons, and generate documentation.

- **Distribution:** Automatically package your plugin for the Godot Asset Library.

Run `python setup.py` in your terminal (inside the workspace directory/root where SConstruct file is located) to see this menu:

```
Main Menu Categories:
  [0] Run Quick Setup Wizard (First-Time Users)
  [1] Godot Engine & Version Settings
  [2] Plugin Configuration & Assets
  [3] Compilation & Build Settings
  [4] Advanced & Workflow Options
```

Type a number `0` or `1` and so on (from the displayed ones).. and press `Enter` to access the sub-menus. You can always cancel/go back by typing `q` and pressing `Enter`.

```
Submenu: Godot Engine & Version Settings
--------------------------------------------------
  1. Change Godot Target Version
  2. Select Godot Engine Executable Path
  3. Update godot_cpp Submodule To Latest
  4. Select Godot Project Folder
  q. Back to Main Menu
--------------------------------------------------
```

```
Submenu: Plugin Configuration & Assets
--------------------------------------------------
  1. Rename Plugin
  2. Update Editor Node Icons
  3. Generate Missing XML Documentation Files
  q. Back to Main Menu
--------------------------------------------------
```

```
Submenu: Compilation & Build Settings
--------------------------------------------------
  1. Compile Plugin Debug Build
  2. Compile Plugin Release Build
  3. Select Build Profile
  4. Edit Build Profile
  5. Change LTO Mode For Release Builds
  6. Toggle Editor Build Target
  7. Toggle Debug Symbols (Allows Attaching Debugger)
  8. Clean Compiled SCons Build Artifacts
  q. Back to Main Menu
--------------------------------------------------
```

```
Submenu: Advanced & Workflow Options
--------------------------------------------------
  1. Hot Reloading Options
  2. Export Local Plugin Zip Release (Ready For Godot Asset Store)
  3. Tutorials And Help With Godot C++
  q. Back to Main Menu
--------------------------------------------------
```

---

## Requirements

To use Godot++, make sure you have the following tools installed and configured on your system.

### 1. GitHub Account & Git

* [GitHub Account](https://github.com/): Required if you plan to use GitHub Actions for automated cross-platform compilation.
* [Git](https://git-scm.com/downloads) latest version, available in your **system environment PATH**: Installed on your machine and configured with your credentials so you can push changes to your remote repository.

### 2. Python & SCons (Build System)

- [Python](https://www.python.org/) latest version, available in your **system environment PATH**.

	- **Windows**: During the Python installer setup, make sure to check the box that says "Add Python to PATH" at the very bottom of the installer window. If you missed this, re-run the installer, choose "Modify", and check it.
	- **macOS**: `brew install python` (via Homebrew) or download from python.org.
	- **Arch Linux** / **CachyOS**: `sudo pacman -S python`
	- **Ubuntu** / **Linux Mint** / **Pop!_OS** / **Debian**: `sudo apt install python3 python3-pip`
	- **Fedora** / **RHEL** / **CentOS**: `sudo dnf install python3 python3-pip`

- [Scons](https://scons.org/) latest version, available in your **system environment PATH**.

	- **Windows**: `python -m pip install scons`
	- **macOS**: `python3 -m pip install --user scons` (or via Homebrew: `brew install scons`)
	- **Arch Linux** / **CachyOS**: `sudo pacman -S scons`
	- **Ubuntu** / **Linux Mint** / **Pop!_OS** / **Debian**: `sudo apt install scons`
	- **Fedora** / **RHEL** / **CentOS**: `sudo dnf install scons`
	- **Other Linux / Fallback**: `python3 -m pip install --user scons`

### 3. C++ Compiler
Make sure your compiler is installed and available in your **system environment PATH**.

* **Windows:** MSVC (Microsoft Visual C++) via Visual Studio or Build Tools.
> ⚠️ **Important Windows Warning:** You must use **MSVC** if you want Link-Time Optimization (LTO) for release builds. LTO is broken or unsupported when using MinGW on Windows.


- **macOS**: Clang (included with Xcode Command Line Tools: `xcode-select --install`).

- **Linux**: GCC or Clang (install your distro's standard development group):

	- **Arch Linux** / **CachyOS**: `sudo pacman -S base-devel`
	- **Ubuntu** / **Linux Mint** / **Pop!_OS** / **Debian**: `sudo apt install build-essential`
	- **Fedora** / **RHEL** / **CentOS**: `sudo dnf groupinstall "Development Tools"`

### 4. Code Editor

* **[Visual Studio Code](https://code.visualstudio.com/)** (with Clangd extension, I don't recommend the Microsoft one it's not as smart)
* **[Zed](https://zed.dev/)** (works with Clangd by default)
* Any other editor that supports C++ and `compile_commands.json` 


If your editor ever fails to find header files automatically, here are the paths you can manually point it to. *(Visual Studio Code **will not** need these as long as you use the recommended Clangd extension).*

```text
${workspaceFolder}/godot-cpp/gdextension/
${workspaceFolder}/godot-cpp/gen/**
${workspaceFolder}/godot-cpp/include/**
${workspaceFolder}/godot-cpp/src/**

${workspaceFolder}/src   -> usually where you write all your code

```

---

## How to Test If Everything Is Set Up Correctly

Before moving on, open your terminal (Command Prompt, PowerShell, or Bash) and run the following check commands. **If every command returns a version number or success message without errors, you are golden!**

* **Check Git:**
```bash
git --version

```


*(Expected: prints something like `git version 2.4x.x`)*
* **Check Python:**
```bash
python --version

```


*(Expected: prints your Python version)*
* **Check SCons:**
```bash
scons --version

```


*(Expected: prints the SCons version and path)*
* **Check C++ Compiler:**
* *Windows (MSVC):* Open the **Developer Command Prompt for VS** (not regular cmd) and type:
```cmd
cl

```


*(Expected: prints Microsoft C/C++ optimizing compiler info)*
* *macOS / Linux (Clang/GCC):*
```bash
clang --version
```
or
```
gcc --version

```


*(Expected: prints compiler version details)*



---


## How to use

You can choose to watch this tutorial for beginners - https://www.youtube.com/watch?v=I79u5KNl34o
##

1. To use this template, log in to GitHub and click the green <b>"Use this template"</b> button at the top of the repository page (not the clone button).
This will let you create a copy of this repository with a clean git history. Please ensure you set it to public if you want to use GitHub Actions for cross platform compilation **FOR FREE**, without facing any problems.

- There is no need for you to upload the actual Godot Project inside the repository and leak all your code, it can totally be an external project that you link to using the tool script helper called `Select Godot Project Folder` and pasting a valid path there, this way only performance critical C++ code is made public. [More information on GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions). Choosing a build profile will really speed up compilation and it will also avoid wasting resources on your local machine as well as on GitHub's machines.

- You could choose to avoid GitHub Actions completely and just use the tool script helper `Export Local Plugin Zip Release (Ready For Godot Asset Store)`, but this will only pack the current compiled binaries. It is totally possible to compile from Windows to Linux using WSL, to web using Emscripten as well as to Android, however for macOS and iOS you will most likely struggle unless you own a device.

2. From now on you will work <b>in your own repository</b> - open it inside your browser, we are gonna make some slight changes

3. Modify the <b>`README.md`</b> file by clearing it and writing something useful about the code you're about to write

4. <b>REPLACE THE `LICENSE` CONTENT</b> with the correct license

5. Clone <b>your own repository</b> that you just made

6. Open <b>`Visual Studio Code`</b> inside the directory you just cloned (where <b>`setup.py`</b> is located)

7. If you have the Microsoft C/C++ extension <b>DELETE IT OR DISABLE IT</b>

8. The extensions that we are going to use for VS Code are the following:

File is called <b>`extensions.json`</b>
```
"recommendations": [
        "llvm-vs-code-extensions.vscode-clangd",
        "ms-python.python",
        "amiralizadeh9480.cpp-helper"
    ]
```

Basically instead of Microsoft's extension for C++, we are going to use the `Clangd` extension which is far superior for intelisense, when you install it, it will offer to install the language server as well, click yes you need that as well


9. Run the <b>`setup.py`</b> script
    - Open your command line terminal where <b>`setup.py`</b> is located (You can use the VS Code terminal too)
    - Run `python setup.py` command inside the terminal to run the script

10. Type `0` and press `Enter` to run the first option `Run Quick Setup Wizard (First-Time Users)`
#
```
Main Menu Categories:
  [0] Run Quick Setup Wizard (First-Time Users)
  [1] Godot Engine & Version Settings
  [2] Plugin Configuration & Assets
  [3] Compilation & Build Settings
  [4] Advanced & Workflow Options
```

Warning: The first time you compile and the VS Code project is open, the Clangd extension will try to read and cache a lot of the information about your classes that were generated inside compile_commands.json by beginning to index them (you will actually notice that at the bottom left of your Visual Studio Code window). So before beginning to write code, please wait for everything to finish.

If everything went well, then every time you type a godot class (example : `Sprite2D`), you should get intelisense as well as auto header includes.
Usually header includes that come from an external library should be with angle brackets, but even if you leave the godot-cpp headers with double quotes, it's still fine so don't worry about it


Note: I've excluded a lot of the files from the explorer that are unnecessary, but you can always unhide some of them by going inside `.vscode/settings.json` and modifying the values there from true to false


Warning: If you are on Linux or macOS and see <b>any weird errors that don't make sense (like seeing detected errors on comments)</b>, but your code compiles perfectly fine, then ensure you have a `.clangd` file inside your VS Code directory and paste this inside if it's not already there:

```
CompileFlags:
  Add: -Wno-unknown-warning-option
  Remove: [-m*, -f*]
```

Instead of VS Code, you could try using [Zed](https://zed.dev/), it is insanely fast and it works with Clangd by default.


After the initial setup is done, you can select option `3` and see code compilation options. Every time you make a change in your code, you have to save your file and then re-compile.

---

## WARNING
1. Don't modify the godot-cpp classes, always make your own - you can choose to inherit from theirs or use pure C++ classes (pure classes won't be exposed to Godot)
2. If you need source code of some classes, check [Godot Engine's source code](https://github.com/godotengine/godot)
3. Godot uses C++ 17 currently, so keep it that way for compatibility
4. When making brand new classes ensure you use `GDCLASS`, and `bind_methods()` and finally ensure you register the actual class inside `register_types.cpp` or else it won't be visible inside the editor
5. Usually when you are writing C++ code, the selected Godot project should be open - you write some C++ code, then compile and you repeat that over and over. You might not see some of the changes immediately, so you need to restart the Godot project <b>(Project -> Reload Current Project)</b>
6. You can edit the `.github/workflows/build-plugin.yml` file and add or remove operating systems and architectures for which you want to compile your plugin. You can also modify the `.gdextension` file which is responsible for loading the binaries.
7. After you are fully done with all your features it is absolutely worth to switch to a custom build profile, this will eliminate classes that your project does not need and will speed up compilation locally and inside GitHub actions workflow. Be warned that if you try to access classes that were stripped away while coding, you will get errors, so you will need to switch back to another profile 2D/3D and only then switch to a newly generated custom build profile.
8. Linker issues and undefined behavior are horrible in C++, so regularly make commits and work on different branches with Git or you will lose valuable time investigating magical bugs
9. To avoid undefined behavior always set your variables to an initial value, pointers should be `null` and when deleting objects you should set all pointers that point to them again back to `null`.
10. When generating documentation if you have NOT compiled your C++ project, it will delete all XML files, which is a big headache and another reason to use Git and being aware of how to restore files (Visual Studo Code makes this easy).
11. If you have no idea how to expose certain things to the engine you can always look at other project's source code as inspiration - [BlastBullets2D](https://github.com/nikoladevelops/godot-blast-bullets-2d)
12. Some compilers are more strict than others, it's entirely possible for some builds to work while others fail, research the issue and what you are doing wrong and resolve it.
13. For objects that inherit `RefCounted` always use `Ref<>` smart pointer to store them or you will get errors.
14. There is no need for you to expose all your source code to a public GitHub repository, instead you can use the helper script and change the Godot Project from `test_project` to an external one that is not inside the repository.
15. If you download someone's GDExtension source code and he uses Godot++, just run option `0` from the template and you have everything configured and ready to run - that's why Godot++ is so easy.

---
## How To Update An Old GDExtension Plugin To Use This Template

If you've already used GDExtension or you have found a plugin that does not use the latest version of this template you can follow these instructions to port it:

1. Download or clone the source code of the plugin you are trying to port along with the new version of Godot++

- `old_plugin_folder` - this refers to the folder of the plugin you are trying to port

- `new_template_folder` - this refers to the folder of the latest Godot++ template version


2. Make sure that your file explorer can see hidden files and folders (there is a setting in Windows File Explorer that you need to check)
3. Move the hidden `.git` folder FROM `old_plugin_folder` TO `new_template_folder`
- This will keep your original plugin git history 
4. If `doc_classes` folder exists, then move it FROM `old_plugin_folder` TO `new_template_folder`
- This will keep the old documentation XML files of the plugin
5. Move `LICENSE` and `README` files FROM `old_plugin_folder` TO `new_template_folder`
6. If there is a godot project that the plugin has inside `old_plugin_folder`, then copy all files and move them inside `new_template_folder`'s `test_project` folder
- Optional, you can now externally link your godot project without the need of it being in the same directory as your github repository, so this depends on your preference
7. If there are any icons that the plugin uses from `old_plugin_folder` then move them all inside `new_template_folder`'s icons root folder. It's important to rename them so that each icon's name matches the C++ custom class that it belongs to.
- After initial setup you will have to run the icons python script helper later, so that the folder gets scanned and those icons loaded properly.
8. Move all source code files (`.cpp` and `.hpp` files) from `old_plugin_folder` TO `new_plugin_folder`.
9. Now that you have moved all those source files TO `new_plugin_folder`, open up the `register_types.cpp` and search for a function that looks like this 

```
GDExtensionBool GDE_EXPORT  someName_init...
```

replace it with

```
// Initialization
	GDExtensionBool GDE_EXPORT plugin_name_init(GDExtensionInterfaceGetProcAddress p_get_proc_address, GDExtensionClassLibraryPtr p_library, GDExtensionInitialization *r_initialization)
	{
		GDExtensionBinding::InitObject init_obj(p_get_proc_address, p_library, r_initialization);
		init_obj.register_initializer(initialize_gdextension_types);
		init_obj.register_terminator(uninitialize_gdextension_types);
		init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

		return init_obj.init();
	}
```
- It's very important that the function's name is renamed to `plugin_name_init`
- Rename the function inside the `register_types.h` header file or you can straight up delete the file


10. Open command terminal in `new_template_folder` directory.

**De-initialize and clear out the broken submodule tracking:**

```
git submodule deinit -f godot-cpp
rm -rf .git/modules/godot-cpp
rm -rf godot-cpp
```

**Re-add/re-initialize the `godot-cpp` submodule** so Git recreates the correct references inside your copied `.git` history:

```
git submodule add https://github.com/godotengine/godot-cpp.git godot-cpp
git submodule update --init --recursive
```

9. Run `git status` and if it manages to recognize your template as your plugin repository then you've done your job

You can also verify whether it points to the right remote repository by running 

```
git remote -v
```


10. Open your terminal and run `setup.py` and choose option `0` to run the setup wizard.

If you get any errors when you reach the compilation step, it means that there were breaking changes in the latest `godot_cpp` and you have to resolve them in your code


Here are some examples:

- Legacy macro-style constants (`Math_PI`, `Math_TAU`) have been phased out or cleaned up in favor of proper class-scoped static constants (`Math::PI` and `Math::TAU`). You should **avoid** using `M_PI` because it is strictly a `double`. Godot uses `real_t`, which can compile as either `float` or `double` depending on your build configuration, making Godot's native `Math` constants the correct choice

- Now godot_cpp is stricter and forces you to use Ref<> instead of plain simple pointers when dealing with ref counted objects (anything that inherits RefCounted class) - you will get a bunch of errors when doing `memnew` and storing a RefCounted object in a plain pointer instead of a Ref<> pointer. This is a very good change by the Godot team that enforces correct behavior

There are many more possible errors that you might get depending on how old the plugin you're porting is.


---

## My C++ GDExtension Plugin Is Ready, I Want To Publish It

1. Commit and Push your code to remote (It's a good idea to switch to a custom generated build profile to speed up compilation before this)
2. Go to the GitHub Actions tab on your repository
3. Run the <b>"Build GDExtension Cross Platform Plugin"</b> workflow and leave LTO(Link-Time Optimization) as `auto` for best results. If LTO fails switch to using `none` for the platform.
4. When everything is in green color it means success, if it's red then you need to resolve your errors and push again.
5. Refresh the page and click on `Summary`.
6. Download the `finished_unzip_me`, unzip it somewhere.
7. You will receive another zip (named after your plugin) that you can upload to [Godot Asset Store](https://store.godotengine.org/) / [Itch.io](https://itch.io/) or GitHub as release.
- The zip includes an `addons` folder and that's recommended for the Godot Asset Store so no need to make changes.
- The zip includes the README and LICENSE files copied from your repository, so ensure they are correct before publishing.

If the user is downloading your plugin zip straight from your repository (instead of using the Godot Asset Store), he should unzip your zip, open the plugin folder, copy the `addons` folder and paste it inside his Godot project root directory.

---

## Support
If you wish to support me you can do so here - https://ko-fi.com/realnikich or https://patreon.com/realnikich

If you find this template useful:
- <b>Leave a Star on the repository</b>
- Expect <b>GDExtension Tutorials</b> on my YouTube channel - https://www.youtube.com/@realnikich
- [Follow me on X (Twitter)](https://x.com/realNikich)
- [Follow me on Bluesky](https://bsky.app/profile/realnikich.bsky.social)

This template wouldn't be possible without the offical [godot-cpp](https://github.com/godotengine/godot-cpp) repository as well as the [godot-cpp-template](https://github.com/godotengine/godot-cpp-template), so you can star them as well
