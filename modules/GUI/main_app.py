import customtkinter as ctk
from PIL import Image
from .buttons import NavigationButton, TrackButton
from .entries import FilterEntry
from ..database import get_playlist
from ..audio_player import AudioPlayer
import os

ctk.set_default_color_theme("green")

img_path = os.path.abspath(__file__+'/../../../assets/img') # Шлях до папки з малюнками

class MelodyPlayer(ctk.CTk):
    def __init__(self, name, width, height):
        super().__init__()
        self.title(name)
        self.geometry(f'{width}x{height}')
        self.resizable(False, False) # Забороняємо змінювати розмір екрану
        # Встановлюємо службові змінні
        self.playlist = get_playlist()
        self.audio_player = AudioPlayer()
        self.track_time = 0
        self.after_id = None
        # Основна панель
        self.main_panel = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.main_panel.pack(side="left", fill='both', expand=True)
        self.main_panel.rowconfigure(0, weight=1)
        self.main_panel.columnconfigure(0, weight=1)
        # Початковий напис
        self.info_label = ctk.CTkLabel(self.main_panel, text="Виберіть пісню зі списку", font=("Arial", 18))
        self.info_label.grid(row=0, column=0)
        # Фрейм для керування піснею
        self.navigation_frame = ctk.CTkFrame(self.main_panel, fg_color="#1e1e1e")
        self.navigation_frame.grid_forget()
        # Пегулятор гучності
        self.volume_label = ctk.CTkLabel(self.navigation_frame, text="Гучність")
        self.volume_label.grid(row=0, column=1)
        self.volume_slider = ctk.CTkSlider(self.navigation_frame, from_=0, to=100, orientation="vertical", height=150, command=self.audio_player.set_volume)
        self.volume_slider.grid(row=1, column=1, pady=(0, 50))
        # Контейнер для кнопок та прогрес_бар
        self.control_container = ctk.CTkFrame(self.navigation_frame, fg_color="#1e1e1e")
        self.control_container.grid(row=1, column=0, sticky="ew", padx=20)
        # Фрейм з прогрес-баром та помітками часу
        self.progress_frame = ctk.CTkFrame(self.control_container, fg_color="#1e1e1e") 
        self.progress_frame.grid(row=0, column=0, pady=(0, 30))
        # Поточний час пісні
        self.current_time = ctk.CTkLabel(self.progress_frame, text="00:00") 
        self.current_time.grid(row=0, column=0, sticky="w")
        # Прогрес-бар
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame) 
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=10)
        self.progress_bar.set(0)
        # Загальна тривалість пісні
        self.total_time = ctk.CTkLabel(self.progress_frame, text="03:45") 
        self.total_time.grid(row=0, column=2, sticky="e")
        # Кнопки
        self.btns_frame = ctk.CTkFrame(self.control_container, fg_color="#1e1e1e")
        self.btns_frame.grid(row=1, column=0)
        # Попередня пісня
        self.prev_img = ctk.CTkImage(Image.open(f"{img_path}/previous.png"), size=(25, 25))
        self.prev_btn = NavigationButton(self.btns_frame, image=self.prev_img, command=self.turn_prev_track)
        self.prev_btn.grid(row=0, column=0, sticky="s", padx=10)
        # Пауза
        self.pause_img = ctk.CTkImage(Image.open(f"{img_path}/pause.png"), size=(25, 25))
        self.pause_btn = NavigationButton(self.btns_frame, image=self.pause_img, command=self.audio_player.pause)
        self.pause_btn.grid(row=0, column=1, sticky="s", padx=10)
        # Анпауза
        self.resume_img = ctk.CTkImage(Image.open(f"{img_path}/resume.png"), size=(25, 25))
        self.resume_btn = NavigationButton(self.btns_frame, image=self.resume_img, command=self.resume)
        self.resume_btn.grid(row=0, column=2, sticky="s", padx=10)
        # Наступна пісня
        self.next_img = ctk.CTkImage(Image.open(f"{img_path}/next.png"), size=(25, 25))
        self.next_btn = NavigationButton(self.btns_frame, image=self.next_img, command=self.turn_next_track)
        self.next_btn.grid(row=0, column=3, sticky="s", padx=10)
        # Бокова панель
        self.side_panel = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.side_panel.pack(side="right", fill="y")
        self.side_panel.columnconfigure(0, weight=1)
        self.side_panel.rowconfigure(2, weight=1)
        # Вміст бокової панелі
        self.title = ctk.CTkLabel(self.side_panel, text="Список пісень", font=("Arial", 18))
        self.title.grid(row=0, column=0, columnspan=3, pady=10)
        self.filter_entry_artist = FilterEntry(self.side_panel, placeholder_text="Виконавець") 
        self.filter_entry_artist.grid(row=1, column=0, padx=(10, 0))
        self.filter_entry_track = FilterEntry(self.side_panel, placeholder_text="Назва пісні")
        self.filter_entry_track.grid(row=1, column=1, padx=(10, 0))
        self.filter_btn = ctk.CTkButton(self.side_panel, corner_radius=40, text="Шукати", width=50, command=self.filter_tracks)
        self.filter_btn.grid(row=1, column=2, padx=10)
        # Фрейм зі скролом для спсику пісень
        self.scrollable_song_list = ctk.CTkScrollableFrame(self.side_panel, fg_color="#2b2b2b")
        self.scrollable_song_list.grid(row=2, column=0, columnspan=3, pady=(20, 0), sticky="nsew")
        # Створення масиву кнопок
        self.track_btns = []
        self.create_track_btns() # Створення самих кнопок
    # Функція, яка спрацьовує при натисканні на кнопку треку
    def choose_track(self, ind):
        # Отримуємо потрібні дані
        track = self.playlist["tracks"][ind]
        total_ind = len(self.playlist["tracks"])
        self.playlist["current_track"]=ind
        # Налаштовуємо зовнішній вигляд
        self.info_label.grid(sticky="s")
        self.info_label.configure(text=f"{track.artist} - {track.title}")
        self.navigation_frame.grid(row=1, column=0, sticky="sew", padx=(90,20))
        self.total_time.configure(text=MelodyPlayer.format_duration_long(track.duration))
        # Налаштовуємо кнопки навігації
        self.prev_btn.configure(state="normal", fg_color="#2FA572")
        self.next_btn.configure(state="normal", fg_color="#2FA572")
        if ind == total_ind: # Якщо остання пісня, блокуємо кнопку "Наступна"
            self.next_btn.configure(state="disabled", fg_color="gray")
        if ind == 1: # Якщо перша пісня, блокуємо кнопку "Попередня"
            self.prev_btn.configure(state="disabled", fg_color="gray")
        # Запускаємо трек та встановлюємо гучність
        self.audio_player.play_track(track.filepath)
        self.audio_player.set_volume(self.volume_slider.get())
        # Пепевіряємо, чи є таймер від попереднього треку, якщо є - видаляємо
        if self.after_id:
            self.after_cancel(self.after_id)
        # Налаштування прогрес_бару
        self.track_time = 0
        self.progress_bar.set(0)
        self.current_time.configure(text="00:00")
        self.set_progress_bar()

    def turn_next_track(self):
        self.playlist["current_track"] += 1
        self.choose_track(self.playlist["current_track"])

    def turn_prev_track(self):
        self.playlist["current_track"] -= 1
        self.choose_track(self.playlist["current_track"])
    # Функція для роботи з прогрес_баром
    def set_progress_bar(self):
        if self.audio_player.is_track_busy(): # Якщо трек грає
            current_track = self.playlist['current_track']
            duration = self.playlist["tracks"][current_track].duration
            ms = self.audio_player.get_track_position()  # мілісекунди
            self.track_time = ms // 1000 + 1
            self.progress_bar.set(self.track_time/duration)
            self.current_time.configure(text=MelodyPlayer.format_duration_long(self.track_time))
            self.after_id = self.after(1000, self.set_progress_bar)
    # Функція Анпаузи
    def resume(self):
        self.audio_player.resume()
        if self.after_id:
            self.after_cancel(self.after_id)
        self.set_progress_bar()

    def filter_tracks(self):
        # Налаштували дизайн
        self.navigation_frame.grid_forget()
        self.info_label.configure(text="Виберіть пісню зі списку")
        self.info_label.grid_configure(sticky="")
        self.audio_player.stop() # Зупинили пісню
        # Отримали введені значення та оновимо плейліст
        artist = self.filter_entry_artist.get()
        track = self.filter_entry_track.get()
        self.playlist = get_playlist(artist, track)
        # Оновимо список кнопок
        self.destroy_track_btns()
        self.create_track_btns()

    def create_track_btns(self):
        if not self.playlist["tracks"]:
            empty_btns_label = ctk.CTkLabel(self.scrollable_song_list, text="За вашим фільтром нічого не знайдено", font=("Arial", 16))
            empty_btns_label.pack()
            self.track_btns.append(empty_btns_label)
            return
        for ind, track in self.playlist["tracks"].items():
            btn = TrackButton(self.scrollable_song_list, text=f"{track.artist} - {track.title}", command= lambda ind =ind: self.choose_track(ind))
            btn.pack(pady=5)
            self.track_btns.append(btn)

    def destroy_track_btns(self):
        for btn in self.track_btns:
            btn.destroy()
        self.track_btns.clear()

    @staticmethod
    def format_duration_long(duration):
        total = int(duration)
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02}:{seconds:02}"

app = MelodyPlayer(name="MelodyPlayer", width=900, height=400)        


