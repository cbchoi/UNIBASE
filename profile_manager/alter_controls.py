import dearpygui.dearpygui as dpg

import uuid

def add_input_text(label="", contents="", width=100):
	com_id = str(uuid.uuid4())
	print(type(com_id))
	with dpg.group(horizontal=True):
		def open_input_dialog():
			import tkinter as tk
			from tkinter import simpledialog
			
			root = tk.Tk()
			root.withdraw()
			user_input = simpledialog.askstring("Input Dialog", "Contents:")
			root.destroy()
			
			if user_input:
				dpg.set_value(com_id, user_input)

		dpg.add_text(label)
		dpg.add_text(contents, tag=com_id)
		dpg.add_button(label="Input", callback=open_input_dialog)
	return com_id