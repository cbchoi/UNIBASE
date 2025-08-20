import dearpygui.dearpygui as dpg

import pprint

class GenerateManager():
	def __init__(self, parent):
		self.parent_window = parent
		self.node_editor_id = None
		pass

	def set_node_editor_id(self, _id):
		self.node_editor_id = _id

	def attach_menu(self):
		dpg.add_button(label="Generate", callback=self.on_generate)

	def find_by_label(self, container_id, target_label) -> list:
		"""
			Find a Node with given target label from Node Editor

			Args:
				container_id: target container
				target_label: target label
		
			Returns:
				list: Found nodes
		"""
		nodes = dpg.get_item_children(container_id, slot=1)
		node_info = []
		for node_id in nodes:
			if dpg.get_item_label(node_id) == target_label:
				node_info.append(node_id)	
		return node_info

	def find_connected_nodes(self, container_id, start_node_id):
		links = dpg.get_item_children(container_id, slot=0) 
    
		# 연결 정보를 저장할 딕셔너리
		connections = {}
		visited_nodes = set()
		node_info = {}
	    
		# 링크 정보 파싱
		for link_id in links:
			link_info = dpg.get_item_configuration(link_id)
			attr1 = link_info.get('attr_1')
			attr2 = link_info.get('attr_2')

			if attr1 and attr2:
				# attribute의 부모 노드 찾기
				node1 = dpg.get_item_parent(attr1)
				node2 = dpg.get_item_parent(attr2)

				# 연결 정보 저장 (양방향)
				if node1 not in connections:
					connections[node1] = []
				if node2 not in connections:
					connections[node2] = []
		            
				connections[node1].append({
				'connected_node': node2,
				'link_id': link_id,
				'output_attr': attr1,
				'input_attr': attr2
				})

				connections[node2].append({
				'connected_node': node1,
				'link_id': link_id,
				'output_attr': attr2,
				'input_attr': attr1
				})

		def traverse_node(node_id, depth=0):
			print(">"* depth, node_id)
			if node_id in visited_nodes:
				return

			visited_nodes.add(node_id)

			# 현재 노드의 정보 수집
			node_config = dpg.get_item_configuration(node_id)
			node_children = dpg.get_item_children(node_id)

			# attribute 정보 수집
			attributes = []
			if node_children:
				for child_id in node_children[1]:  # slot 1에 attribute들이 있음
					attr_config = dpg.get_item_configuration(child_id)
					attr_type = dpg.get_item_type(child_id)

					for grand_id in dpg.get_item_children(child_id)[1]:
						pprint.pprint(dpg.get_item_configuration(grand_id))

					attributes.append({
					    'id': child_id,
					    'type': attr_type,
					    'label': attr_config.get('label', ''),
					    'shape': attr_config.get('shape', ''),
					    'category': attr_config.get('category', '')
					})

			node_info[node_id] = {
				'label': node_config.get('label', f'Node {node_id}'),
				'pos': dpg.get_item_pos(node_id),
				'attributes': attributes,
				'connections': connections.get(node_id, []),
				'depth': depth
				}

			# 연결된 노드들 탐색
			if node_id in connections:
				for connection in connections[node_id]:
					traverse_node(connection['connected_node'], depth + 1)
	    
		# 시작 노드부터 탐색 시작
		traverse_node(start_node_id)
		
		return node_info

	def on_generate(self):
		head_id = self.find_by_label("editor", "Head")
		self.find_connected_nodes("editor", head_id[0])
