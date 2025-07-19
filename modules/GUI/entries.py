import customtkinter as ctk

class FilterEntry(ctk.CTkEntry):
    def __init__(self, master, placeholder_text, **kwargs):
        super().__init__(
            master, placeholder_text = placeholder_text, text_color="white", 
            fg_color="#2a2a2a", corner_radius=40, width=110, **kwargs)