import customtkinter as ctk
from .buttons import NavigationButton, TrackButton
from PIL import Image
import os

img_path = os.path.abspath(__file__+'/../../../assets/img') # Шлях до папки з малюнками

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color, audio_player, playlist, format_duration, **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)
        self.audio_player=audio_player
        self.playlist=playlist
        self.format_duration=format_duration
        self.track_time = 0
        # Поточний час пісні
        self.current_time = ctk.CTkLabel(self, text="00:00") 
        self.current_time.grid(row=0, column=0, sticky="w")
        # Прогрес-бар
        self.progress_bar = ctk.CTkProgressBar(self) 
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=10)
        self.progress_bar.set(0)
        # Загальна тривалість пісні
        self.total_time = ctk.CTkLabel(self, text="03:45") 
        self.total_time.grid(row=0, column=2, sticky="e")

    def set_time(self, total_time=None, current_time=None, progress_value=None):
        if total_time is not None and self.total_time.winfo_exists():
            self.total_time.configure(text=total_time)
        if current_time is not None and self.current_time.winfo_exists():
            self.current_time.configure(text=current_time)
        if progress_value is not None and self.progress_bar.winfo_exists():
            self.progress_bar.set(progress_value)


    # Функція для роботи з прогрес_баром
    def update_progress_bar(self):
        if self.audio_player.is_track_busy(): # Якщо трек грає
            current_track = self.playlist['current_track']
            duration = self.playlist["tracks"][current_track].duration
            ms = self.audio_player.get_track_position()  # мілісекунди
            self.track_time = ms // 1000 + 1
            self.set_time(current_time=self.format_duration(self.track_time), progress_value=self.track_time/duration)
            after_id = self.after(1000, self.update_progress_bar)
            return after_id

class NavigationButtonsFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color, prev_command, pause_command, resume_command, next_command, **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)
         # Попередня пісня
        self.prev_img = ctk.CTkImage(Image.open(f"{img_path}/previous.png"), size=(25, 25))
        self.prev_btn = NavigationButton(self, image=self.prev_img, command=prev_command)
        self.prev_btn.grid(row=0, column=0, sticky="s", padx=10)
        # Пауза
        self.pause_img = ctk.CTkImage(Image.open(f"{img_path}/pause.png"), size=(25, 25))
        self.pause_btn = NavigationButton(self, image=self.pause_img, command=pause_command)
        self.pause_btn.grid(row=0, column=1, sticky="s", padx=10)
        # Анпауза
        self.resume_img = ctk.CTkImage(Image.open(f"{img_path}/resume.png"), size=(25, 25))
        self.resume_btn = NavigationButton(self, image=self.resume_img, command=resume_command)
        self.resume_btn.grid(row=0, column=2, sticky="s", padx=10)
        # Наступна пісня
        self.next_img = ctk.CTkImage(Image.open(f"{img_path}/next.png"), size=(25, 25))
        self.next_btn = NavigationButton(self, image=self.next_img, command=next_command)
        self.next_btn.grid(row=0, column=3, sticky="s", padx=10)

    def enable_prev_or_next_btns(self, index, total):
        self.prev_btn.configure(state="normal", fg_color="#2FA572")
        self.next_btn.configure(state="normal", fg_color="#2FA572")
        if index == total: # Якщо остання пісня, блокуємо кнопку "Наступна"
            self.next_btn.configure(state="disabled", fg_color="gray")
        if index == 1: # Якщо перша пісня, блокуємо кнопку "Попередня"
            self.prev_btn.configure(state="disabled", fg_color="gray")

class ScrollableTrackListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, fg_color, track_btn_command, **kwargs):
        super().__init__(master,  fg_color=fg_color, **kwargs)
        self.track_btn_command = track_btn_command
        self.track_btns = []

    def create_track_btns(self, playlist):
        if not playlist["tracks"]:
            empty_btns_label = ctk.CTkLabel(self, text="За вашим фільтром нічого не знайдено", font=("Arial", 16))
            empty_btns_label.pack()
            self.track_btns.append(empty_btns_label)
            return
        for ind, track in playlist["tracks"].items():
            btn = TrackButton(self, text=f"{track.artist} - {track.title}", command= lambda ind=ind: self.track_btn_command(ind))
            btn.pack(pady=5)
            self.track_btns.append(btn)

    def destroy_track_btns(self):
        for btn in self.track_btns:
            btn.destroy()
        self.track_btns.clear()