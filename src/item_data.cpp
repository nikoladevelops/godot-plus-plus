// Try to keep your includes organized, so that you can easily see which ones come from your project and which ones are from Godot or other libraries
#include "item_data.hpp" // For headers that are our own, we use ""
#include <godot_cpp/classes/random_number_generator.hpp>
#include <godot_cpp/classes/resource.hpp>
#include <godot_cpp/core/class_db.hpp>

#include <godot_cpp/classes/object.hpp> // For headers coming from an external library we use <> angle brackets
#include <godot_cpp/core/print_string.hpp>

// Include things you might be using
// This line might be unnecessary if we are already including this header in the item_data.hpp file
#include <godot_cpp/classes/node.hpp>

// Note: We can include extra headers that we need in the implementation of our logic
// We are NOT required to include them in the .hpp file as well
// (as long as we don't use the class name in a function declaration - we might use forward declarations to handle that problem)

// Again having this line is important, so that you can use the classes without prefixing them with "godot::", which might be annoying
// Also doing it in a .cpp file is ALWAYS completely fine
using namespace godot;

String ItemData::get_name() const {
	return name;
}

void ItemData::set_name(const String &p_name) {
	name = p_name;
}

String ItemData::get_description() const {
	return description;
}
void ItemData::set_description(const String &p_description) {
	description = p_description;
}

int ItemData::get_price() const {
	return price;
}
void ItemData::set_price(int p_price) {
	price = p_price;
}

void ItemData::spawn_stuff() {
	Node *my_node = memnew(Node); // This is how you create a new instance of a Godot node / In GDScript you would use "var node = Node.new()"
	// Now you can attach this node to the scene tree or do whatever you want with it

	// Because my_node is a pointer to a Node, you can use the arrow operator (->) to access its methods and properties
	my_node->set_name(name); // This is how you call methods on the node, similar to "my_node.name = name" in GDScript

	// WARNING: this won't work on our Resource class, we need to inherit from Node instead and place the node in the scene tree, or we will get crashes, but it's good knowledge
	//get_local_scene()->add_child(my_node); // This is how you add a node to the current scene tree, similar to "add_child(node)" in GDScript

	// You already know how to free nodes in GDScript, so you can use the same logic here
	// my_node->queue_free(); // This will free the node after the current frame, similar to "node.queue_free()" in GDScript

	// When creating resources it's a bit different
	// You ALWAYS have to wrap them in a Ref<> smart pointer
	Ref<Resource> resource = memnew(Resource); // This is how you create a new instance of a Resource - maybe you want Textures or Materials or something else

	// You don't have to worry about memory management for Ref<> smart pointers,
	// because they automatically handle reference counting for you
	// When the last reference to the resource is gone, it will be automatically freed

	// As for the nodes, they are also managed by the scene tree unless you call queue_free() on them (just like in GDScript)

	// The only time where you might need to manually free stuff is when you use pure C++ classes
	// In modern C++ you would use smart pointers like std::unique_ptr or std::shared_ptr for that
	// Or using containers like std::vector or std::map that automatically handle memory management for you
	// C++ is not as scary as it seems, once you get used to it

	print_line("Spawned stuff!");
}

void ItemData::spawn_custom_scene(Ref<PackedScene> p_scene) {

	Node *instance = nullptr;  // Never leave default pointers to be empty, always initialize to nullptr
	// Rule: Before trying to access some argument (especially a resource)
	// be defensive about it and check if the object is actually usable
	if (p_scene.is_valid()) { // Check if live, usable object
		instance = p_scene->instantiate(); // This is how you instantiate a PackedScene
	}
	// Well look at that, when instantiating a packed scene we always get a pointer to a Node
	// but what if our scene is not actually a Node, but something else?
	// In that case we need to cast it to the type we want in order to access the functions and properties we need

	// We need to cast this pointer to the actual type that it points to
	// There are several types of casting available in Godot

	// 1. Static cast (normal C++ feature)
	// -- only use this if you FOR SURE KNOW THE ACTUAL TYPE
	// -- if someone passes something other than the type you think it is, you will get instant error
	// -- fastest cast you can do is this, because this cast is executed at compile time

	// if (instance) {
	//     Player *player = static_cast<Player *>(instance); // Safe if you know instance is a Player, it will crash if it's something else
	//     if (player) {
	//         player->some_player_method(); // Access Player-specific method
	//     }
	// }

	// 2. Dynamic cast (normal C++ feature)
	// -- use when you are not sure of the type it actually holds
	// -- handle cases for different types
	// -- slower than static cast, because this cast is executed at runtime

	// Player *player = dynamic_cast<Player *>(instance); // Safe runtime check
	// if (player) {
	// 	player->some_player_method(); // Only called if cast succeeds
	// } else {
	// 	// Handle invalid cast (e.g., instance is not a Player)
	// }

	// 3. Object::cast_to  (Godot specific runtime cast)
	// -- use when working with Godot’s Object type
	// -- still a runtime cast so slower than static_cast
	// -- useful for casting Variant to another godot specific type

	// PlayerData *data = Object::cast_to<PlayerData>(some_other_resource_class_instance);

	// How to spawn stuff to the current scene

	// If it's not nullptr, then do this..
	if (instance) {
		print_line("Valid instance was given!");
		// WARNING: This code won't work, we need to be inheriting from Node, and also it needs to be placed in the actual scene
		//get_local_scene()->add_child(instance);
	}else{
		print_line("You did NOT give a valid instance!");
	}
}

void ItemData::print_node_name(Node *just_a_node) {
	String n = just_a_node->get_name(); // Get a value and save it to a String variable (Note: if the types are not matching we need to cast)
	print_line(n); // Print the value we have saved inside the variable
}

void ItemData::print_resource_name(Ref<Resource> res) {
	String n = res->get_name();
	print_line(n);
}

void ItemData::print_all_node_names(const TypedArray<Node> &arr) {
	// Even tho we've said that our godot array only contains Node,
	// internally data is represented with the Variant data type
	// which means, in order to work with the actual type (to be able to call functions and properties specific to it)
	// we need to cast it

	for (Variant const &item : arr) { // the & means we want to use the actual object/ we don't want to make a copy of it when iterating

		// WARNING: To cast a Variant you should always use Object::cast_to
		Node *actual_node = Object::cast_to<Node>(item);

		// After the cast we can finally call the methods for our type
		print_line(actual_node->get_name());
	}

	// The loop on top can be seen as a foreach for those familiar with C#, it just goes through each item in a collection

	// Here is the normal for loop, that you are used to
	// for (int i = 0; i < 10; i++) {

	// }

	// Here is while loop
	// while (true) {

	// }
}

void ItemData::modify_all_node_names(const TypedArray<Node> &arr, const String &new_name) {
	// Warning: Even tho we see TypedArray<Node>, what we are actually storing inside these typed arrays is Variants
	// This confuses beginners a lot since they expect nodes to be found inside, but what they get is the special type Variant
	// To handle this special type and actually turn it back into a node, we need the Godot specific casting - Object::cast_to<>
	// this might be confusing for beginners, so a good tutorial might be necessary for this, if you leave a comment I might make one

	for (Variant const &item : arr) { // the & means we want to use the actual object/ we don't want to make a copy of it when iterating

		// This is where the magic happens, we are required to use const in the loop initialization, and yet we are able to use an object cast
		// and now suddenly we can call methods that modify the node that was inside the array. This is why Godot's Object::cast_to is important
		// if you use any other type of cast, it will fail. Remember, when casting Variant, always use Object::cast_to
		Node *actual_node = Object::cast_to<Node>(item); // From a const Variant, give me a pointer to the actual node I want to edit
		actual_node->set_name(new_name); // Now I am able to modify the Node

		// Rule: When casting Variant, always use Object::cast_to
	}
}

void ItemData::modify_all_node_names_wrong_way(TypedArray<Node> arr, String new_name) {
	// Our goal is to loop through an array of nodes and change each node's name, that's our purpose
	// Well we already made a mistake - our array is being copied since we didn't say we want a reference (&)
	// The string is also being copied for no reason at all..

	// If we want truly performant code, where the function will be executed many times over and over
	// It's a good practice to avoid copies always.

	// (Right now we are copying variants which actually hold pointers to our nodes, so the code doesn't really copy the actual nodes, it copies the pointers
	// but still in other situations you will get bugs because you will be working with copies instead of the original objects
	// Remember as a habit to always use const references for data structures when possible,
	// since you might be using std::vector or other pure C++ types etc.. you will only get more confused, so keep it simple)

	// Rule: Use const reference for TypedArrays always to avoid copies

	// Lets make our second mistake and not use & here, this way we will make even more copies for no reason
	// Now instead of working with the copied Variant item, we make YET ANOTHER COPY of it for no reason
	// because we didn't specify that we want a reference with (&)
	for (Variant item : arr) { // the & is missing, so copies are being made
		Node *actual_node = Object::cast_to<Node>(item);
		actual_node->set_name(new_name);
	}

	// Rule: Avoid copies in loops when you don't need them
}

TypedArray<int> ItemData::create_10k_numbers(int min, int max) {
    TypedArray<int> arr;
    arr.resize(10000); // Pre-allocate exactly 10k slots for optimal performance (avoids reallocations during insertion)

	// RandomNumberGenerator also inherits from RefCounted
	// which means we need to wrap it in Ref<>   -> Always check classes from what they inherit before using them to avoid memory leaks and weird bugs
	// A good workflow might also be finding the docs of the class inside your godot editor to check for the functions and properties you need
	// and then just fixing the syntax for C++

    Ref<RandomNumberGenerator> rng = memnew(RandomNumberGenerator); // Use a local RNG instance for better performance/isolation
    rng->randomize(); // Seed it for true randomness (optional but good practice; skips if you want reproducibility)

    for (int i = 0; i < 10000; i++) {
        arr[i] = rng->randi_range(min, max); // Generate inclusive random int between min and max
    }

    return arr;
}

void ItemData::_bind_methods() {
	// This is how you bind your methods to Godot, so they can be called from GDScript or other languages
	ClassDB::bind_method(D_METHOD("get_name"), &ItemData::get_name);

	// This is how you bind a method that takes an argument
	ClassDB::bind_method(D_METHOD("set_name", "name"), &ItemData::set_name);

	// This is how you create a property (useful instead of always calling get_name() and set_name() directly)
	ADD_PROPERTY(PropertyInfo(Variant::STRING, "name"), "set_name", "get_name");

	ClassDB::bind_method(D_METHOD("get_description"), &ItemData::get_description);
	ClassDB::bind_method(D_METHOD("set_description", "description"), &ItemData::set_description);
	ADD_PROPERTY(PropertyInfo(Variant::STRING, "description"), "set_description", "get_description");

	ClassDB::bind_method(D_METHOD("get_price"), &ItemData::get_price);
	ClassDB::bind_method(D_METHOD("set_price", "price"), &ItemData::set_price);
	ADD_PROPERTY(PropertyInfo(Variant::INT, "price"), "set_price", "get_price");

	ClassDB::bind_method(D_METHOD("spawn_stuff"), &ItemData::spawn_stuff);

	ClassDB::bind_method(D_METHOD("spawn_custom_scene", "scene_to_spawn"), &ItemData::spawn_custom_scene);

	ClassDB::bind_method(D_METHOD("print_node_name", "node"), &ItemData::print_node_name);

	ClassDB::bind_method(D_METHOD("print_resource_name", "resource"), &ItemData::print_resource_name);

	ClassDB::bind_method(D_METHOD("print_all_node_names", "arr"), &ItemData::print_all_node_names);

	ClassDB::bind_method(D_METHOD("modify_all_node_names", "arr", "new_name"), &ItemData::modify_all_node_names);

	ClassDB::bind_method(D_METHOD("modify_all_node_names_wrong_way", "arr", "new_name"), &ItemData::modify_all_node_names_wrong_way);

	ClassDB::bind_method(D_METHOD("create_10k_numbers", "min", "max"), &ItemData::create_10k_numbers);

}
