extends Node2D


func _ready() -> void:
	test_plugin_functionality()

func test_plugin_functionality()->void:
	var gd_extension_class:ExampleClass = ExampleClass.new()
	
	if gd_extension_class == null:
		print("Failed to load GDExtension");
		assert(false, "ERROR: GDExtension FAILED to load")
	else:
		print("GDExtension loaded successfully")
		assert(true, "SUCCESS: GDExtension LOADED")
	
	
