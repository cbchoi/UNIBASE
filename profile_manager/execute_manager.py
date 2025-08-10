from block_manager import BlockManager
from node_manager import NodeManager
from link_manager import LinkManager
from mouse_handler import MouseHandler
from file_manager import FileManager

class Configuration():
	def __init__(self):
		self.title  = "Example"
		self.width  = 1000
		self.height = 900
		self.parent_window = "editor"
		self.link_manager = LinkManager(self.parent_window)
		self.node_manager = NodeManager(self.parent_window)
		self.mouse_handler = MouseHandler(self.parent_window)
		self.file_manager = FileManager(self.parent_window)

config = Configuration()

with BlockManager(config) as bm:
	bm.run()
