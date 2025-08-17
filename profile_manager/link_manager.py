import dearpygui.dearpygui as dpg
import uuid

class LinkManager:
	def __init__(self, parent):
		self.parent_window = parent
		self.links = []
		pass

	def on_restore(self, data):
		self.links = []

		for lk in data["links"]:
			dpg.add_node_link(lk["src"], lk["dst"], parent=lk["parent"], tag=lk["tag"])
			self.links.append(lk["tag"])

	def on_save(self):
		data = []
		for link in dpg.get_item_children(self.parent_window, 0): 
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
		link_tag = f"link:{uuid.uuid4()}"
		dpg.add_node_link(dpg.get_item_alias(out_attr), dpg.get_item_alias(in_attr), parent=sender, tag=link_tag)
		self.links.append(link_tag)

	def delink_callback(self, sender, app_data):
		link_tag = app_data
		if link_tag in links:
			self.links.remove(link_tag)
		dpg.delete_item(link_tag)