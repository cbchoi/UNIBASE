import dearpygui.dearpygui as dpg

class NodeManager:
	def __init__(self):
		self.node_idx = 0
		self.node_tags = {}

	def on_restore(self, data):
		self.node_idx = 0
		self.node_tags = {}
		# 노드 복원
		for nd in data["nodes"]:
			if nd["label"] == "Head":
				self.add_node(label=nd["label"], pos=tuple(nd["pos"]), tag=nd["tag"], is_head = True)
			else:
				self.add_node(label=nd["label"], pos=tuple(nd["pos"]), tag=nd["tag"],
							  name=nd["fields"][0], type=nd["fields"][1], value=nd["fields"][2])

	def on_save(self):
		data = []
		for node in dpg.get_item_children("editor", 1):  # slot=1은 노드들
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

	def on_add_node(self):
		mx, my = dpg.get_mouse_pos()
		self.add_node(label=f"Field {self.node_idx}", pos=(int(mx), int(my)))
	
	def add_node(self, label, pos, name="", type="TEXT", value="", tag="", is_head=False):
		self.node_idx += 1

		if not tag:
			node_tag = f"NODE:{self.node_idx}"
			
		else:
			node_tag = tag

		self.node_tags[node_tag] = {}
		with dpg.node(label=label, tag=node_tag, parent="editor", pos=pos):
			if not is_head:
				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=f"{node_tag}in"):
					 dpg.add_text("In")

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_text("Field Name:")
					field_name_tag = dpg.add_input_text(label="", width=150, user_data="Field Name", tag=f"{node_tag}FieldName")
					dpg.set_value(field_name_tag, name)
					self.node_tags[node_tag][field_name_tag] = name

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_text("Type:")
					field_type_tag = dpg.add_combo(("TEXT", "BOOLEAN", "INT", "FLOAT"),
									default_value="TEXT", width=200, tag=f"{node_tag}FieldType")
					dpg.set_value(field_type_tag, type)
					self.node_tags[node_tag][field_type_tag] = type

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_text("Value:")
					field_value_tag = dpg.add_input_text(label="", width=150, user_data="Field Name", tag=f"{node_tag}FieldValue")
					dpg.set_value(field_value_tag, value)
					self.node_tags[node_tag][field_value_tag] = value

			with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}out"):
				 dpg.add_text("Out")
		return node_tag