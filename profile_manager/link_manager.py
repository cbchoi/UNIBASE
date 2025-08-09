import dearpygui.dearpygui as dpg

class LinkManager:
	def __init__(self):
		self.links = []
		pass

	def on_restore(self, data):
		self.links = []

		for lk in data["links"]:
			dpg.add_node_link(lk["src"], lk["dst"], parent=lk["parent"], tag=lk["tag"])

	def on_save(self):
		data = []
		for link in dpg.get_item_children("editor", 0): 
			a, b = dpg.get_item_configuration(link)["attr_1"], dpg.get_item_configuration(link)["attr_2"]
			data.append({"src": dpg.get_item_alias(a), "dst": dpg.get_item_alias(b), 
						 "parent":dpg.get_item_alias(dpg.get_item_parent(link)), 
						 "tag":dpg.get_item_alias(link)})
		return data

	def on_link_deleted(self, sel_links):
		for sl in sel_links:
			if sl in self.links:
				self.links.remove(sl)

	def link_callback(self, sender, app_data):
		out_attr, in_attr = app_data
		link_tag = f"link_{len(self.links)+1}"
		dpg.add_node_link(out_attr, in_attr, parent="editor", tag=link_tag)
		self.links.append(link_tag)

	def delink_callback(self, sender, app_data):
		link_tag = app_data
		if link_tag in links:
			self.links.remove(link_tag)
		dpg.delete_item(link_tag)