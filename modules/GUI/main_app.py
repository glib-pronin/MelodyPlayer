import customtkinter as ctk
from PIL import Image
from .buttons import NavigationButton
import os

ctk.set_default_color_theme("green")

img_path = os.path.abspath(__file__+'/../../../img') 

class MelodyPlayer(ctk.CTk):
    def __init__(self, name, width, height):
        super().__init__()
        self.title(name)
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        # Основна панель
        self.main_panel = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.main_panel.pack(side="left", fill='both', expand=True)
        self.main_panel.rowconfigure(0, weight=1)
        self.main_panel.columnconfigure(0, weight=1)
        # Початковий напис
        self.info_label = ctk.CTkLabel(self.main_panel, text="Виберіть пісню зі списку", font=("Arial", 18))
        self.info_label.grid(row=0, column=0)

        self.navigation_frame = ctk.CTkFrame(self.main_panel, fg_color="#1e1e1e")
        self.navigation_frame.grid_forget()

        self.volume_label = ctk.CTkLabel(self.navigation_frame, text="Гучність")
        self.volume_label.grid(row=0, column=1)
        self.volume_slider = ctk.CTkSlider(self.navigation_frame, from_=0, to=100, orientation="vertical", height=150)
        self.volume_slider.grid(row=1, column=1, pady=(0, 50))

        self.control_container = ctk.CTkFrame(self.navigation_frame, fg_color="#1e1e1e")
        self.control_container.grid(row=1, column=0, sticky="ew", padx=20)

        # Прогрес-бар
        self.progress_frame = ctk.CTkFrame(self.control_container, fg_color="#1e1e1e")
        self.progress_frame.grid(row=0, column=0, pady=(0, 20))

        self.current_time = ctk.CTkLabel(self.progress_frame, text="00:00")
        self.current_time.grid(row=0, column=0, sticky="w")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=10)

        self.total_time = ctk.CTkLabel(self.progress_frame, text="03:45")
        self.total_time.grid(row=0, column=2, sticky="e")

        # Кнопки
        self.btns_frame = ctk.CTkFrame(self.control_container, fg_color="#1e1e1e")
        self.btns_frame.grid(row=1, column=0)

        self.prev_img = ctk.CTkImage(Image.open(f"{img_path}/previous.png"), size=(25, 25))
        self.prev_btn = NavigationButton(self.btns_frame, text="", image=self.prev_img)
        self.prev_btn.grid(row=0, column=0, sticky="s", padx=10)

        self.pause_img = ctk.CTkImage(Image.open(f"{img_path}/pause.png"), size=(25, 25))
        self.pause_btn = NavigationButton(self.btns_frame, text="", image=self.pause_img)
        self.pause_btn.grid(row=0, column=1, sticky="s", padx=10)

        self.resume_img = ctk.CTkImage(Image.open(f"{img_path}/resume.png"), size=(25, 25))
        self.resume_btn = NavigationButton(self.btns_frame, text="", image=self.resume_img)
        self.resume_btn.grid(row=0, column=2, sticky="s", padx=10)
        
        self.next_img = ctk.CTkImage(Image.open(f"{img_path}/next.png"), size=(25, 25))
        self.next_btn = NavigationButton(self.btns_frame, text="", image=self.next_img)
        self.next_btn.grid(row=0, column=3, sticky="s", padx=10)

        self.side_panel = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.side_panel.pack(side="right", fill="y")
        self.side_panel.columnconfigure(0, weight=1)
        self.side_panel.rowconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self.side_panel, text="Список пісень", font=("Arial", 18))
        self.title.grid(row=0, column=0, columnspan=2, pady=10)
        self.filter_entry = ctk.CTkEntry(self.side_panel, text_color="white", fg_color="#2a2a2a",
                                         placeholder_text="Введіть назву або виконавця пісні", corner_radius=40, width=250)
        self.filter_entry.grid(row=1, column=0, padx=(10, 0))
        self.filter_btn = ctk.CTkButton(self.side_panel, corner_radius=40, text="Шукати", width=50)
        self.filter_btn.grid(row=1, column=1, padx=10)

        self.scrollable_song_list = ctk.CTkScrollableFrame(self.side_panel, fg_color="#2b2b2b")
        self.scrollable_song_list.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky="nsew")

        for i in range(10):
            self.btn = ctk.CTkButton(self.scrollable_song_list, text="Beatles Yesterday", hover_color="#55d88c", command=self.show_navigation_frame)
            self.btn.pack(pady=10)

    def show_navigation_frame(self):
        self.info_label.grid_configure(sticky="s")
        self.navigation_frame.grid(row=1, column=0, sticky="sew", padx=(90,20))



app = MelodyPlayer(name="MelodyPlayer", width=900, height=400)        


