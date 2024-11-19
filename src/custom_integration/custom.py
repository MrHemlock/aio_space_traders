from IPython.core.magic import register_line_magic
import customtkinter as ctk

class CustomTkinterEventLoop:
    def __init__(self):
        self.root = None
        self.running = False

    def start(self):
        if not self.running:
            self.root = ctk.CTk()
            # self.root.withdraw()  # Hide the main window
            self.running = True
            self._schedule_update()
            print("CustomTkinter event loop started. You can now create windows and widgets.")
        else:
            print("CustomTkinter event loop is already running.")

    def stop(self):
        if self.running:
            self.running = False
            if self.root:
                self.root.quit()
                self.root.destroy()
            print("CustomTkinter event loop stopped.")
        else:
            print("CustomTkinter event loop is not running.")

    def _schedule_update(self):
        if self.running:
            self.root.update()
            self.root.after(10, self._schedule_update)  # Schedule next update in 10ms

ctk_loop = CustomTkinterEventLoop()

@register_line_magic
def customtkinter(line):
    ctk_loop.start()

@register_line_magic
def stop_customtkinter(line):
    ctk_loop.stop()

# Use this to create and show a window
def create_window():
    if not ctk_loop.running:
        print("CustomTkinter event loop is not running. Use %customtkinter to start it.")
        return None
    window = ctk.CTkToplevel(ctk_loop.root)
    window.title("CustomTkinter Window")
    window.geometry("300x200")
    label = ctk.CTkLabel(window, text="Hello, CustomTkinter!")
    label.pack(padx=20, pady=20)
    return window

print("CustomTkinter integration loaded. Use %customtkinter to start the event loop and %stop_customtkinter to stop it.")
