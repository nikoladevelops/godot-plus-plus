// WARNING: All this code is tested on Godot 4.4.1, on each godot-cpp branch release there might be changes to the API

// WARNING: In every .hpp file that you make, always include "#pragma once" at the top of the file (or use the old way with include guards)
// This will prevent multiple inclusions of the same header file (without it, you would get errors when compiling)
#pragma once

// A single .hpp file should contain class declarations and method signatures
// For each .hpp file you should have a corresponding .cpp file where you place the method definitions (implementing the actual logic of the methods)

// More advanced devs might use the templates C++ feature (like Generics in C# but more powerful)
// or want to forcefully inline methods,
// only then you would put the method definitions in the .hpp file

// Include necessary Godot headers. If you ever want to use a Godot class, you need to include its header file here
// By holding CTRL and clicking on it, you will see the class declaration and all the functions that it has
// If you want to see implementations you can always check godot's source code on GitHub
#include <godot_cpp/variant/typed_array.hpp> // Added for Godot arrays
#include <godot_cpp/classes/node.hpp> // Added for Node
#include <godot_cpp/classes/packed_scene.hpp> // Added for PackedScene
#include <godot_cpp/classes/resource.hpp> // Added for Resource
// If you are using the Clangd language server and using my setup script to compile,
// it will automatically suggest the correct headers to include when you type a class name (because of the generated compile_commands.json file)

// The actual VS Code extensions you need for smooth development
// "llvm-vs-code-extensions.vscode-clangd",  -> clangd, it will also prompt you to download the language server automatically
// "ms-python.python", -> just a python extension if you need to edit the SConstruct someday
// "amiralizadeh9480.cpp-helper" -> allows you to right click on a method declaration in the .hpp and create implementations in the .cpp file fast
// You might also want to install github actions extension if you plan on editing the build-plugin.yml file

//
// Microsoft's extension for C++ is not that great, if you have that, disable it and install Clangd along with its language server
// If you still insist on using something other than Clangd (which reads the compile_commands.json),
// then you might need to setup the include paths correctly

// ${workspaceFolder}/godot-cpp/gdextension/
// ${workspaceFolder}/godot-cpp/gen/**
// ${workspaceFolder}/godot-cpp/include/**
// ${workspaceFolder}/godot-cpp/src/**
// ${workspaceFolder}/src   -> usually where you write all your code, but you might separate it into src/ and include/ dirs (check Sconstruct file)
//

// If you are inexperienced with C++
// A good workflow might be writing your logic in GDScript first and ensuring it works as expected,
// and then writing the C++ equivalent of it (or using AI to help you with that)

// If you run into linking issues when making custom classes, make sure you don't have a situation where
// header file A includes B, and B includes A, because that will cause a circular dependency
// Use forward declarations inside the header if necessary and combine that with pointers
// (avoid references since Godot constructors are weird and they have limitations, for constructors use your own setup functions)

// For header files that are completely yours use double quotes, like this: #include "my_header.hpp"
// For header files that are from Godot or other libraries use angle brackets, like this: #include <godot_cpp/classes/resource.hpp>
// Clangd sometimes might suggest you to use double quotes for Godot headers, but you should always use angle brackets, be consistent

// It is usually a VERY BAD practice to use "using namespace;" in header files (.hpp)
// because it can cause name conflicts, but since we are not working with other libraries, we will not have any issues with it
// WARNING: Always include this code in both your .hpp and .cpp files, so that you can use the classes without prefixing them with "godot::"
using namespace godot;

// class ExampleClass;
// this is a forward declaration, we just tell C++
// "Hey, we have a class that we are going to be using and it's called ExampleClass
// I'll supply the implementation later, by including the header inside the .cpp file only, that way I avoid circular dependencies"

// You can inherit from other classes, like Node, Node2D, Node3D, even MultiMeshInsance2D etc...
// That would actually allow you to place your custom class inside the scene tree, so you can use it like any other node
// and you will have functions like _ready(), _process(), _physics_process() etc...
class ItemData : public Resource { // Right now inheriting from Resource, just as a simple example
	// WARNING: Always have this GDCLASS macro when making custom classes that you want visible in your Godot project
	// and as a second argument always pass the class you are inheriting from
	GDCLASS(ItemData, Resource)

// WARNING: Always have this when making custom classes that you want visible in your Godot project
// In this _bind_methods() function you will bind your methods to Godot, so they can be called from GDScript or other languages
protected:
	static void _bind_methods();

// For methods and properties that never get accessed by other C++ classes, write them under private, otherwise write them under public
private:
	// Always set default values to avoid hard to track bugs. Especially when dealing with custom resource classes.
	// If you do not set default values to a Resource, and then try to use the ResourceSaver/ ResourceLoaded you will get undefined behavior
	// it's especially interesting when you have a boolean variable that you do not set to a default value
	// each time your ResourceSaver will save it with a completely different value on a random... avoid bugs like these..

	String name = "Default Item";
	String description = "This is a default item description.";
	int price = 0;

	String get_name() const; // const here means that the function is never making changes to the class / never assigning new values to anything
	void set_name(const String &p_name); // const here means that we are never editing the string that we are passing ,  & means that this is a reference, so we are never copying the string, we are passing the actual string itself

	String get_description() const;
	void set_description(const String &p_description);

	int get_price() const;
	void set_price(int p_price);

	// Just a simple void method that is supposed to spawn things
	// (Usually you will NEVER have such methods inside a class that inherits from Resource, so this is just an example)
	void spawn_stuff();

	// If you are accepting an argument that inherits from RefCounted, like PackedScene or Resource, you should use the Ref<> smart pointer
	// If you don't do this you will get errors when trying to pass the argument from GDScript
	// Again, remember any type of resources like Texture, Material, PackedScene stuff like that should be wrapped in Ref<>
	void spawn_custom_scene(Ref<PackedScene> p_scene);

	// When dealing with nodes you use (*) which means a simple pointer (valid for everything that inherits from Node)
	void print_node_name(Node *just_a_node);

	// When dealing with resources or objects that inherit from RefCounted ALWAYS USE Ref<> to wrap the resource or you will get compile time errors
	void print_resource_name(Ref<Resource> res);

	// When working with arrays it's best to use & (which means it's a reference and you avoid copying the whole array)
	// WARNING: When using references with Godot objects, ALWAYS add a const keyword or you will get an error
	// Godot tries to protect you from undefined behavior and weird bugs,
	// so it discourages you from overwriting the actual object that can be in use inside GDScript
	// memory is handled by the engine, Godot tells you to keep it that way and don't overwrite my arrays!
	void print_all_node_names(const TypedArray<Node> &arr); // having const infront means that you can NEVER edit the actual TypedArray

	// This is how you can get an array of godot classes and modify them in some sort of way
	void modify_all_node_names(const TypedArray<Node> &arr, const String &new_name); // using const reference for String always (we never want to copy strings)

	// This is also valid code, but the difference is that because we don't use &, we always make a copy of the whole array
	// And because we are working with a copy and not the real godot object, we are free to avoid using const infront of it
	void modify_all_node_names_wrong_way(TypedArray<Node> arr, String new_name); // Also the String is now being copied as well...

	// WARNING: For simple types like int, float etc..  never pass by reference. String is the only exception to this rule.

	// Create 10 thousand random numbers in the range from min to max and return an array that is compatible with GDScript (TypedArray)
	// A good exercise would be to modify this function so that it also includes the amount of random numbers to generate as amount argument
	TypedArray<int> create_10k_numbers(int min, int max);

	// Understanding the difference between pointers, references and the const keyword is valuable knowledge
	// I might make a tutorial on the topic if people are interested

};  // Classes end with ";"

// WARNING: Each time you make a change, you should always recompile the project
// You can always use my setup script for that or just run "scons compiledb=yes" in the terminal
// The compiledb=yes flag will generate a compile_commands.json file that you can use with Clangd for better autocompletion and error checking
// If you rely on include directories, you can just run the "scons" command

// WARNING: When you make a class that you want to use in Godot, you have to also register it in the `register_types.cpp` file

// Node: If you are tired of using print statements to debug and you want an actual debugger
// you can compile your code using the "scons debug_symbols=yes compiledb=yes" command
// (this command might change depending on godot-cpp version and also prevents optimized builds)
// and after that run your game and attach the debugger to the Godot process (the correct one, since you have an editor process and game process)
// As long as you don't inline functions forcefully, you will be able to set breakpoints and step through your code

// Note: You are also free to make PURE C++ classes, that you can use internally (won't be exposed in GDScript),
// but then you should handle memory management yourself

// Note: if you prefer working with 2 separate directories for .hpp and .cpp files, you can do that as well
// Just edit the SConstruct file - search for "# Directory for headers"/ "includes" to see the code there and change "src" to "include"

// Expect tutorials and more examples on my YouTube channel: https://www.youtube.com/@realNikich
// Follow me on X: https://x.com/realNikich
// Bluesky: https://bsky.app/profile/realnikich.bsky.social

// Consider supporting my work on Ko-fi: https://ko-fi.com/realnikich
// Or on Patreon: https://patreon.com/realnikich

// If you found this template useful, please leave a star on GitHub: https://github.com/nikoladevelops/godot-plus-plus
// You should also star the official godot-cpp repository: https://github.com/godotengine/godot-cpp

// This godot-plus-plus template is based on https://github.com/godotengine/godot-cpp-template,
// and it removes a lot of the struggle that beginners might face and does an insane amount of changes to simplify everything
