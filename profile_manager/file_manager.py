import dearpygui.dearpygui as dpg
import json
from tiny_signal import TinySignal

from enum import Enum

class MenuState(Enum):
	NONE = 0
	NEW = 1
	OPEN = 2
	SAVE = 3

class FileManager():
	def __init__(self, parent):
		self.parent_window = parent
		self.save_signal = TinySignal()
		self.restore_signal = TinySignal()
		self.file_path = None
		self.menu_state = MenuState.NONE

	def attach_menu(self):
		with dpg.menu(label="File"):
			dpg.add_menu_item(label="New", callback=self.menu_new)
			dpg.add_menu_item(label="Open", callback=self.menu_open)
			dpg.add_menu_item(label="Save", callback=self.menu_save)
			dpg.add_menu_item(label="Save As", callback=self.menu_save_as)

		with dpg.file_dialog(
			directory_selector=False, show=False, 
			default_path=".", default_filename="graph.json",
			callback=self.callback, tag="file_dialog_id",
			cancel_callback=self.cancel_callback, width=700 ,height=400):
			dpg.add_file_extension(".json", color=(0,255,0,255), custom_text="JSON (*.json)")
			dpg.add_file_extension(".*", color=(180,180,180,255), custom_text="All Files (*.*)")

	
	def callback(self, sender, app_data):
		dpg.set_value("status_file_path", app_data['file_path_name'])
		self.file_path = app_data["file_path_name"]
		
		if self.menu_state == MenuState.OPEN:
			self.load_graph(self.file_path)
		elif self.menu_state == MenuState.New:
			self.new_graph(self.file_path)
		else:
			self.save_graph(self.file_path)

	def cancel_callback(self, sender, app_data):
		pass

	def menu_new(self, sender, app_data):
		self.menu_state = MenuState.NEW
		dpg.show_item("file_dialog_id")		

	def menu_save(self, sender, app_data):
		if self.file_path:
			self.save_graph(self.file_path)
		else:
			print("Save File Not Selected")

	def menu_save_as(self, sender, app_data):
		self.menu_state = MenuState.SAVE
		dpg.show_item("file_dialog_id")
			
	def menu_open(self):
		self.menu_state = MenuState.OPEN
		dpg.show_item("file_dialog_id")		

	def bind_save_signal(self, _func, _from):
		self.save_signal.bind(_func, _from)

	def bind_restore_signal(self, _func, _from):
		self.restore_signal.bind(_func, _from)
	
	def new_graph(self, filename):
		for link in list(dpg.get_item_children(self.parent_window, 0)):
			dpg.delete_item(link)
		for node in list(dpg.get_item_children(self.parent_window, 1)):
			dpg.delete_item(node)

		self.restore_signal.emit({})

	def save_graph(self, filename):
		data = {"nodes": [], "links": []}
		res = self.save_signal.emit()
		
		data["nodes"] = res["node"]
		data["links"] = res["link"]
		
		with open(filename, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2)
			print(f"Saved to {filename}")

	def load_graph(self, filename):
		with open(filename, "r", encoding="utf-8") as f:
			data = json.load(f)

		# 기존 노드/링크 삭제
		for link in list(dpg.get_item_children(self.parent_window, 0)):
			dpg.delete_item(link)
		for node in list(dpg.get_item_children(self.parent_window, 1)):
			dpg.delete_item(node)

		self.restore_signal.emit(data)
		

	