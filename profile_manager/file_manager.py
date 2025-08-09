import dearpygui.dearpygui as dpg
import json
from tiny_signal import TinySignal

class FileManager():
	def __init__(self):
		self.save_signal = TinySignal()
		self.restore_signal = TinySignal()

	def attach_menu(self):
		with dpg.menu(label="File"):
			dpg.add_menu_item(label="Open", callback=self.menu_open)
			dpg.add_menu_item(label="Save", callback=self.menu_save)

	def menu_save(self):
		self.save_graph("graph.json")

	def menu_open(self):
		self.load_graph("graph.json")

	def bind_save_signal(self, _func, _from):
		self.save_signal.bind(_func, _from)

	def bind_restore_signal(self, _func, _from):
		self.restore_signal.bind(_func, _from)
	
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
		for link in list(dpg.get_item_children("editor", 0)):
			dpg.delete_item(link)
		for node in list(dpg.get_item_children("editor", 1)):
			dpg.delete_item(node)

		self.restore_signal.emit(data)
		

	