#include "item_data.hpp"
#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/variant/utility_functions.hpp> // Required for UtilityFunctions::print

using namespace godot;

// Setters and Getters
String ItemData::get_name() const { return name; }
void ItemData::set_name(const String &p_name) { name = p_name; }

String ItemData::get_description() const { return description; }
void ItemData::set_description(const String &p_description) { description = p_description; }

int ItemData::get_price() const { return price; }
void ItemData::set_price(int p_price) { price = p_price; }

void ItemData::spawn_stuff() {
    // memnew() creates an object. If not added to the scene tree via add_child(),
    // it MUST be manually freed to avoid memory leaks.
    Node *my_node = memnew(Node);
    my_node->set_name(name);

    UtilityFunctions::print("Spawned temporary node: ", my_node->get_name());

    // Clean up manually since it was never added to the SceneTree
    memdelete(my_node);
}

void ItemData::spawn_custom_scene(Ref<PackedScene> p_scene) {
    if (p_scene.is_valid()) {
        Node *instance = p_scene->instantiate();
        if (instance) {
            UtilityFunctions::print("Valid instance created!");
            // Remember: If you add this to the tree, you don't call memdelete.
            // If you DON'T add it to the tree, call instance->queue_free() or memdelete(instance).
            instance->queue_free();
        }
    } else {
        UtilityFunctions::print("Invalid PackedScene provided!");
    }
}

void ItemData::print_node_name(Node *p_node) {
    if (p_node) {
        UtilityFunctions::print(p_node->get_name());
    }
}

void ItemData::print_resource_name(Ref<Resource> p_res) {
    if (p_res.is_valid()) {
        UtilityFunctions::print(p_res->get_name());
    }
}

void ItemData::print_all_node_names(const TypedArray<Node> &p_arr) {
    for (const Variant &item : p_arr) {
        Node *actual_node = Object::cast_to<Node>(item);
        if (actual_node) {
            UtilityFunctions::print(actual_node->get_name());
        }
    }
}

void ItemData::modify_all_node_names(const TypedArray<Node> &p_arr, const String &p_new_name) {
    for (const Variant &item : p_arr) {
        Node *actual_node = Object::cast_to<Node>(item);
        if (actual_node) {
            actual_node->set_name(p_new_name);
        }
    }
}

void ItemData::modify_all_node_names_wrong_way(TypedArray<Node> p_arr, String p_new_name) {
    // Note: passing by value makes unnecessary copies of the TypedArray (which contains Variants).
    for (Variant item : p_arr) {
        Node *actual_node = Object::cast_to<Node>(item);
        if (actual_node) {
            actual_node->set_name(p_new_name);
        }
    }
}

TypedArray<int> ItemData::create_10k_numbers(int p_min, int p_max) {
    TypedArray<int> arr;
    arr.resize(10000);

    Ref<RandomNumberGenerator> rng = memnew(RandomNumberGenerator);
    rng->randomize();

    for (int i = 0; i < 10000; i++) {
        arr[i] = rng->randi_range(p_min, p_max);
    }
    return arr;
}

void ItemData::_bind_methods() {
    ClassDB::bind_method(D_METHOD("get_name"), &ItemData::get_name);
    ClassDB::bind_method(D_METHOD("set_name", "name"), &ItemData::set_name);
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
