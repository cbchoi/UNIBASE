import dearpygui.dearpygui as dpg

class GenerateManager():
	def __init__(self, parent):
		self.parent_window = parent
		self.node_editor_id = None
		pass

	def set_node_editor_id(self, _id):
		self.node_editor_id = _id

	def attach_menu(self):
		dpg.add_button(label="Generate", callback=self.on_generate)

	def find_by_label(self, target_label):
		print(self.node_editor_id)
		node_editor_children = dpg.get_item_children(self.node_editor_id)
		print(node_editor_children)
		nodes = node_editor_children[1] 
		for node_id in nodes:
			node_config = dpg.get_item_configuration(node_id)
			node_label = node_config.get('label', '')
			print(node_label)
			if node_label == target_label:
				return node_id

	def on_generate(self):
		print(self.find_by_label("Head"))
