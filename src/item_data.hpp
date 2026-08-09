// WARNING: All this code is tested on Godot 4.7.
// On each godot-cpp release, there might be slight changes to the API, but GDExtension ABI is stable.

#pragma once

#include <godot_cpp/variant/typed_array.hpp>
#include <godot_cpp/classes/node.hpp>
#include <godot_cpp/classes/packed_scene.hpp>
#include <godot_cpp/classes/resource.hpp>
#include <godot_cpp/classes/random_number_generator.hpp>

// Note: Using "using namespace" in headers is generally discouraged in professional C++
// to avoid name collisions. However, for a template focused on simplicity, it is acceptable.
using namespace godot;

class ItemData : public Resource {
    GDCLASS(ItemData, Resource)

protected:
    static void _bind_methods();

private:
    String name = "Default Item";
    String description = "This is a default item description.";
    int price = 0;

    // Getters and Setters
    String get_name() const;
    void set_name(const String &p_name);

    String get_description() const;
    void set_description(const String &p_description);

    int get_price() const;
    void set_price(int p_price);

    // Demonstration methods
    void spawn_stuff();
    void spawn_custom_scene(Ref<PackedScene> p_scene);
    void print_node_name(Node *p_node);
    void print_resource_name(Ref<Resource> p_res);

    // Array handling
    void print_all_node_names(const TypedArray<Node> &p_arr);
    void modify_all_node_names(const TypedArray<Node> &p_arr, const String &p_new_name);
    void modify_all_node_names_wrong_way(TypedArray<Node> p_arr, String p_new_name);

    TypedArray<int> create_10k_numbers(int p_min, int p_max);
};
