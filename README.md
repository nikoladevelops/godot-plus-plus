### THIS TEMPLATE IS STILL BEING UPDATED AND TESTED, DO NOT USE IT YET, MIGHT HAVE BUGS. 
### CHECK IT IN A FEW DAYS TIME, MEANWHILE IF YOU WANT THE OLD VERSION - AFTER CLONING THE REPO, CHECKOUT TO THIS COMMIT #2f854ce  (https://github.com/nikoladevelops/godot-plus-plus/commit/2f854ce391b049666cfde2f0386a7a136ad78f52)

# Godot++
This repository provides a user-friendly template for developing [GDExtensions](https://docs.godotengine.org/en/stable/classes/class_gdextension.html) in C++ for [Godot Engine](https://godotengine.org/).  Unlike traditional setups that require manual configuration, file editing, and command-line tinkering, [Godot++](https://github.com/nikoladevelops/godot-plus-plus) simplifies the entire process with a single <b>`setup.py`</b> script that automates everything - from initializing submodules to configuring your library name and entry points. This makes it perfect for beginners and experienced developers alike, enabling a fast workflow to write, compile, and test C++ plugins in Godot with minimal hassle.

* **Proven in Production:** See this template in action with [BlastBullets2D](https://github.com/nikoladevelops/godot-blast-bullets-2d) - a fully finished 2D C++ bullets plugin. Download the `test_project.zip` to test its performance, or fork the repository to start building your own features.

---
## Who Is This For?

* **All Skill Levels:** Whether you are a beginner or an advanced developer looking for a frictionless C++ setup.
* **Godot Developers:** Anyone wanting to build **cross-platform C++ plugins or games** for Godot Engine.
* **Legacy Updaters:** Developers looking to update older GDExtension plugins to support modern cross-platform workflows.
* **Performance Seekers:** Anyone aiming to make their games **significantly faster and more optimized**.
* **Solo Developers:** Perfect if you don't own multiple operating system devices, yet want guaranteed cross-platform compatibility across architectures (`x86_64`, `arm64`, etc.).

---

## Key Features

* **Built-In GitHub Actions:** Automatically compiles your code for **Windows, macOS, Linux, Android, iOS, and Web**.
* **Flexible Build Profiles:** Generates both **debug** and **release** builds out of the box, ready for distribution on the [Godot Asset Library](https://godotengine.org/asset-library/asset), [Itch.io](https://itch.io/), or elsewhere.
* **Web Target Support:** Compiles both **threaded** and **non-threaded Web** builds effortlessly.
* **Maximized Performance:** Automatically applies **Link-Time Optimization (LTO)** for final release builds to squeeze out every drop of performance.
* **Zero Configuration Hassle:** No complex terminal commands to memorize-just run `setup.py` and start writing C++ GDExtension code immediately.
* **Plug-and-Play End User Experience:** End users simply unzip your plugin and it works instantly-zero setup required on their end.

---

## Requirements
- [GitHub](https://github.com/) account because we are going to be using GitHub Actions for cross platform compilation
- [Git](https://git-scm.com/downloads) installed on your machine and configured correctly so you can push changes to remote
- [Python](https://www.python.org/) latest version and ensure it's available in <b>system environment PATH</b>
- [Scons](https://scons.org/) latest version and ensure it's available in <b>system environment PATH</b>
    - Windows command: `pip install scons`
    - macOS command: `python3 -m pip install scons`
    - Linux command `python3 -m pip install scons`
- C++ compiler
    - Windows: MSVC (Microsoft Visual C++) via Visual Studio or Build Tools.
    - macOS: Clang (included with Xcode or Xcode Command Line Tools).
    - Linux: GCC or Clang (available via package managers).
- [Visual Studio Code](https://code.visualstudio.com/) or any other editor that supports C++ and the `compile_commands.json`

Here are some include directories, if for some reason your editor needs them (Visual Studio Code will NOT need them as long as we use the Clangd extension)
```
${workspaceFolder}/godot-cpp/gdextension/
${workspaceFolder}/godot-cpp/gen/**
${workspaceFolder}/godot-cpp/include/**
${workspaceFolder}/godot-cpp/src/**

${workspaceFolder}/src   -> usually where you write all your code
```

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

## Python Helper Tool Scripts

**It is also worth exploring all other menus, since there are lots of helpful tool scripts!**

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

## Some advice
1. Don't modify the godot-cpp classes, always make your own - you can choose to inherit from theirs or use pure C++ classes (pure classes won't be exposed to Godot)
2. If you need source code of some classes, check [Godot Engine's source code](https://github.com/godotengine/godot)
3. Godot uses C++ 17 currently, so keep it that way for compatibility
4. When making brand new classes ensure you use `GDCLASS`, and `bind_methods()` and finally ensure you register the actual class inside `register_types.cpp` or else it won't be visible inside the editor
5. Usually when you are writing C++ code, the selected Godot project should be open - you write some C++ code, then compile and you repeat that over and over. You might not see some of the changes immediately, so you need to restart the Godot project <b>(Project -> Reload Current Project)</b>
6. You can edit the ```.github/workflows/build-plugin.yml``` file and add or remove operating systems and architectures for which you want to compile your plugin

---

## Does My Plugin Work On Other Operating Systems?
Right now every time you compile your code, it is being compiled for your own operating system and your own architecture, but since you want your plugin to be used by other people that might be on a different operating system (whether they are using the editor or trying to export their game with your plugin) we need to use GitHub Actions to test if everything is working correctly


Every time you've added features to your plugin and you are wondering if it works for other operating systems you do this:

1. Commit and Push your code to remote
2. Go to the GitHub Actions tab on your repository
3. Run the <b>"Build GDExtension Cross Platform Plugin"</b> workflow by selecting that you want a `debug` build only - again first time compiling will be slow, but GitHub Actions also uses cache for Scons that lasts around 7 days, so it's fine. After everything is completed you will see a `finished_unzip_me` that contains a zip of your plugin. If everything is green, congrats your plugin works on all operating systems, if however you see red, it means that some of the builds failed and you need to play around and see why and fix your issues, then push to remote and try again.. repeat..

<b>Warning:</b> You should not use these builds as a plugin release.. they only test if everything is compiling correctly instead of wasting more resources for optimizations

---

## My C++ GDExtension Plugin Is Ready, I Want To Publish It
If you compiled a debug build first, and you saw that everything is working and all your features are truly done, then you can go ahead and do your full plugin compilation that compiles `debug` builds used by the editor as well as `release` builds that are meant to be used by the exported game of the user.

To do this, go inside your repository, then go to Actions tab, and then again run the <b>"Build GDExtension Cross Platform Plugin"</b> workflow, but this time from the dropdown instead of `debug`, you should choose `full_plugin_compilation`.

Again a `finished_unzip_me` that contains a zip of your plugin will be generated.

1. Unzip it to get the actual zip for publishing
2. Publish your plugin zip file as a release on your GitHub Repository / [Godot Asset Store](https://store.godotengine.org/) / [Itch.io](https://itch.io/) or give it to someone to test

---

## How Does Someone Download And Install The Plugin?

1. Download the zip (comes with an addons folder already)
2. Unzip it inside a Godot project

Make sure that users keep your plugin in the `addons` folder, since that's where plugins should live. The Godot Asset Store also expects the same.

---

## Support
If you wish to support me you can do so here - https://ko-fi.com/realnikich or https://patreon.com/realnikich

If you find this template useful:
- <b>Leave a Star on the repository</b>
- Expect <b>GDExtension Tutorials</b> on my YouTube channel - https://www.youtube.com/@realnikich
- [Follow me on X (Twitter)](https://x.com/realNikich)
- [Follow me on Bluesky](https://bsky.app/profile/realnikich.bsky.social)

This template wouldn't be possible without the offical [godot-cpp](https://github.com/godotengine/godot-cpp) repository as well as the [godot-cpp-template](https://github.com/godotengine/godot-cpp-template), so you can star them as well
