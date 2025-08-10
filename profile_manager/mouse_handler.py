import dearpygui.dearpygui as dpg
from tiny_signal import TinySignal

class MouseHandler():
	def __init__(self, parent):
		self.parent_window = parent
		self.link_signal = TinySignal()
		self.node_signal = TinySignal()

	def bind_link_signal(self, _func, _from):
		self.link_signal.bind(_func, _from)

	def bind_node_signal(self, _func, _from):
		self.node_signal.bind(_func, _from)

	def on_mouse_right_down(self, sender, app_data):
		# 현재 선택된 항목 조회
		sel_links = dpg.get_selected_links("editor") or []
		sel_nodes = dpg.get_selected_nodes("editor") or []

		# 링크 우선 삭제 (여러 개면 전부)
		if sel_links:
			self.link_signal.emit(list(sel_links))
			for lt in list(sel_links):
				if dpg.does_item_exist(lt):
					dpg.delete_item(lt)
			return

		# 링크가 없으면 노드 삭제 (여러 개면 전부)
		if sel_nodes:
			self.node_signal.emit(list(sel_nodes))
			for nt in list(sel_nodes):
				if dpg.does_item_exist(nt):
					dpg.delete_item(nt)

	def on_mouse_down(self, sender, app_data):
		if app_data[0] == 1:
			self.on_mouse_right_down(sender, app_data)

	def get_mouse_down_handler(self):
		return self.on_mouse_down
