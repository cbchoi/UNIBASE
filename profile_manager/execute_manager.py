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
		self.link_manager = LinkManager()
		self.node_manager = NodeManager()
		self.mouse_handler = MouseHandler()
		self.file_manager = FileManager()

config = Configuration()

with BlockManager(config) as bm:
	bm.run()
