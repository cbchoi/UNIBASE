import dearpygui.dearpygui as dpg

class BlockManager():
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		dpg.destroy_context()
		return False

	def __init__(self, config):
		dpg.create_context()
		
		with dpg.font_registry():
			with dpg.font(r"C:\Windows\Fonts\malgun.ttf", 20) as font1:
				# add the default font range
				dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
				dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
		
			dpg.bind_font(font1)

		self.node_manager = config.node_manager
		self.link_manager = config.link_manager
		self.mouse_handler = config.mouse_handler
		self.file_manager = config.file_manager

		self.mouse_handler.bind_link_signal(self.link_manager.on_link_deleted, "link")
		self.mouse_handler.bind_node_signal(self.node_manager.on_node_deleted, "node")

		self.file_manager.bind_save_signal(self.node_manager.on_save, "node")
		self.file_manager.bind_save_signal(self.link_manager.on_save, "link")

		self.file_manager.bind_restore_signal(self.node_manager.on_restore, "node")
		self.file_manager.bind_restore_signal(self.link_manager.on_restore, "link")

		with dpg.window(label="Node Editor", width=900, height=600, no_scrollbar=False):		
			with dpg.menu_bar():
				self.file_manager.attach_menu()
				dpg.add_button(label="Add Node (+)", callback=self.node_manager.on_add_node)
			
			with dpg.child_window(tag="work_area", width=-1, height=500, border=False):
				with dpg.node_editor(tag="editor", callback=self.link_manager.link_callback, delink_callback=self.link_manager.delink_callback):
					self.head_node = self.node_manager.add_node("Head", pos=(40, 100), is_head=True)
			with dpg.child_window(height=40, autosize_x=True, no_scrollbar=True, border=True):
				with dpg.group(horizontal=True):
					dpg.add_text("Current File:")
					dpg.add_text("", tag="status_file_path")

		with dpg.handler_registry():
			dpg.add_mouse_down_handler(callback=self.mouse_handler.get_mouse_down_handler())
	
		dpg.create_viewport(title=config.title, width=config.width, height=config.height)


	def run(self):
		dpg.show_font_manager()
		dpg.setup_dearpygui()
		dpg.show_viewport()
		dpg.start_dearpygui()
