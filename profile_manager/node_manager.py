import dearpygui.dearpygui as dpg
import uuid
from alter_controls import add_input_text

class NodeManager:
	def __init__(self, parent):
		self.parent_window = parent
		self.node_tags = {}

	def attach_menu(self):
		dpg.add_button(label="Add Node (+)", callback=self.on_add_node)

	def on_restore(self, data):
		self.node_tags = {}

		for nd in data["nodes"]:
			if nd["label"] == "Head":
				self.add_node(label=nd["label"], pos=tuple(nd["pos"]), tag=nd["tag"], is_head = True)
			else:
				self.add_node(label=nd["label"], pos=tuple(nd["pos"]), tag=nd["tag"],
							  name=nd["fields"][0], type=nd["fields"][1], value=nd["fields"][2])

	def on_save(self):
		data = []
		for node in dpg.get_item_children(self.parent_window, 1):  
			pos = dpg.get_item_pos(node)
			label = dpg.get_item_label(node)
			field_data = []

			tag = dpg.get_item_alias(node)
			
			for second_key in self.node_tags[tag]:
				field_data.append(dpg.get_value(second_key)) 

			data.append({
				"tag": tag,
				"label": label,
				"pos": pos, 
				"fields":field_data,
			})
		
		return data

	def on_node_deleted(self, sel_nodes):
		for sn in sel_nodes:
			if sn in self.node_tags:
				self.node_tags.remove(sl)

	def on_add_node(self, sender, app_data):
		mx, my = dpg.get_mouse_pos()
		self.add_node(label=f"Field", pos=(int(mx), int(my)))
	
	def add_node(self, label, pos, name="필드", type="TEXT", value="", tag="", is_head=False):
		if not tag:
			node_tag = f"node:{uuid.uuid4()}"
		else:
			node_tag = tag

		with dpg.font_registry():
			with dpg.font(r"C:\Windows\Fonts\malgun.ttf", 20) as font1:
				# add the default font range
				dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
				dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
		
			dpg.bind_font(font1)
		

		self.node_tags[node_tag] = {}
		with dpg.node(label=label, tag=node_tag, parent=self.parent_window, pos=pos):
			if not is_head:
				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=f"{node_tag}in"):
					field_name_tag = add_input_text(label="Field Name:", contents=value, width=150)
					self.node_tags[node_tag][field_name_tag] = name

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_text("Type:")
					field_type_tag = dpg.add_combo(("TEXT", "BOOLEAN", "INT", "FLOAT"),
									default_value="TEXT", width=200, tag=f"{node_tag}FieldType")
					dpg.set_value(field_type_tag, type)
					self.node_tags[node_tag][field_type_tag] = type

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}out"):
					field_value_tag = add_input_text(label="Value:", contents=value, width=150)
					self.node_tags[node_tag][field_value_tag] = value
			else:
				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}out"):
					 dpg.add_text("Start")
		return node_tag