import customtkinter as ctk

ctk.set_default_color_theme("green")

class MelodyPlayer(ctk.CTk):
    def __init__(self, name, width, height):
        super().__init__()
        self.title(name)
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        # Основна панель
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.pack(side="left", fill='y')
        # Початковий напис
        self.info_label = ctk.CTkLabel(self.main_panel, text="Виберіть пісню зі списку", font=("Arial", 18))
        self.info_label.pack()
        print(self.info_label.cget("font"))

        self.navigation_frame = ctk.CTkFrame(self.main_panel)
        self.navigation_frame.pack()

app = MelodyPlayer(name="MelodyPlayer", width=600, height=400)        