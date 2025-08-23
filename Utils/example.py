import dearpygui.dearpygui as dpg

def open_input_dialog():
    import tkinter as tk
    from tkinter import simpledialog
    
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("입력", "한글을 입력하세요:")
    root.destroy()
    
    if user_input:
        dpg.set_value("text_display", user_input)

dpg.create_context()

# 한글 폰트 추가
with dpg.font_registry():
    # Windows의 경우
    #korean_font = dpg.add_font(r"C:/Windows/Fonts/malgun.ttf", 16)
    with dpg.font(r"C:\Windows\Fonts\malgun.ttf", 20) as korean_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
    # 또는 NotoSans 등 다른 한글 폰트 사용
    dpg.bind_font(korean_font)

dpg.create_viewport()
dpg.setup_dearpygui()


# 폰트 적용
with dpg.window(label="대안"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="한글 입력", callback=open_input_dialog)
        dpg.add_text("", tag="text_display")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()