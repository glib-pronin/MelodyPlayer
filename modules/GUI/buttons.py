import customtkinter as ctk

class NavigationButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="", width=60, corner_radius=40, **kwargs)

class TrackButton(ctk.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, width=250, height=30, corner_radius=40, **kwargs)