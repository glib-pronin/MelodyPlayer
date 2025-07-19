import customtkinter as ctk
from .entries import FilterEntry
from .frames import NavigationButtonsFrame, ScrollableTrackListFrame, ProgressFrame
from .toplevels import AddTrackWindow
from ..database import get_playlist
from ..audio_player import AudioPlayer

ctk.set_default_color_theme("green")

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
        self.progress_frame = ProgressFrame(self.control_container, fg_color="#1e1e1e", audio_player=self.audio_player, get_playlist=lambda: self.playlist, format_duration=MelodyPlayer.format_duration_long) 
        self.progress_frame.grid(row=0, column=0, pady=(0, 30))
        # Фрейм з навігаціними кнопками
        self.btns_frame = NavigationButtonsFrame(
            self.control_container, prev_command=self.turn_prev_track, pause_command=self.audio_player.pause, 
            resume_command=self.resume, next_command=self.turn_next_track, fg_color="#1e1e1e")
        self.btns_frame.grid(row=1, column=0)
        # Бокова панель
        self.side_panel = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.side_panel.pack(side="right", fill="y")
        self.side_panel.columnconfigure(0, weight=1)
        self.side_panel.rowconfigure(3, weight=1)
        # Вміст бокової панелі
        self.track_lst_title = ctk.CTkLabel(self.side_panel, text="Список пісень", font=("Arial", 18))
        self.track_lst_title.grid(row=0, column=0, pady=10)
        # Службова панель
        self.service_panel = ctk.CTkFrame(self.side_panel, fg_color="#2b2b2b", border_color="#747171", border_width=2)
        self.service_panel.grid(row=1, column=0, padx=10)
        self.filter_entry_artist = FilterEntry(self.service_panel, placeholder_text="Виконавець")
        self.filter_entry_artist.grid(row=0, column=0, padx=(10, 0), pady=10)
        self.filter_entry_track = FilterEntry(self.service_panel, placeholder_text="Назва пісні")
        self.filter_entry_track.grid(row=0, column=1, padx=(10, 0), pady=10)
        self.filter_btn = ctk.CTkButton(self.service_panel, corner_radius=40, text="Шукати", width=50, command=self.filter_tracks)
        self.filter_btn.grid(row=0, column=2, padx=10, pady=10)
        self.add_track_btn = ctk.CTkButton(self.service_panel, corner_radius=40, text="Додати пісню", command=self.show_add_track_window)
        self.add_track_btn.grid(row=1, column=0, columnspan=3, pady=10)
        # Фрейм зі скролом для спсику пісень
        self.scrollable_song_list = ScrollableTrackListFrame(self.side_panel, fg_color="#2b2b2b", track_btn_command=self.choose_track)
        self.scrollable_song_list.grid(row=3, column=0, pady=(10, 0), sticky="nsew")
        self.scrollable_song_list.create_track_btns(playlist=self.playlist)
        
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
        self.progress_frame.set_time(total_time=MelodyPlayer.format_duration_long(track.duration), current_time="00:00", progress_value=0)
        # Налаштовуємо кнопки навігації
        self.btns_frame.enable_prev_or_next_btns(index=ind, total=total_ind)
        # Запускаємо трек та встановлюємо гучність
        self.audio_player.play_track(track.filepath)
        self.audio_player.set_volume(self.volume_slider.get())
        # Пепевіряємо, чи є таймер від попереднього треку, якщо є - видаляємо
        if self.after_id:
            self.after_cancel(self.after_id)
        # Налаштування прогрес_бару
        self.progress_frame.track_time = 0
        self.create_after()

    def turn_next_track(self):
        self.playlist["current_track"] += 1
        self.choose_track(self.playlist["current_track"])

    def turn_prev_track(self):
        self.playlist["current_track"] -= 1
        self.choose_track(self.playlist["current_track"])
    
    # Функція Анпаузи
    def resume(self):
        self.audio_player.resume()
        if self.after_id:
            self.after_cancel(self.after_id)
        self.create_after()

    def create_after(self):
        self.progress_frame.update_progress_bar()
        self.after_id = self.after(1000, self.create_after)

    def filter_tracks(self):
        # Отримали введені значення та оновимо плейліст
        artist = self.filter_entry_artist.get()
        track = self.filter_entry_track.get()
        self.refresh_playlist_ui(artist=artist, track=track)


    def refresh_playlist_ui(self, artist="", track=""):
        # Налаштували дизайн
        self.navigation_frame.grid_forget()
        self.info_label.configure(text="Виберіть пісню зі списку")
        self.info_label.grid_configure(sticky="")
        self.audio_player.stop() # Зупинили пісню
        # Оновимо список кнопок
        self.playlist = get_playlist(artist, track)
        print(self.playlist)
        self.scrollable_song_list.destroy_track_btns()
        self.scrollable_song_list.create_track_btns(playlist=self.playlist)

    def show_add_track_window(self):
        self.add_track_window = AddTrackWindow(fg_color="#2b2b2b", refresh_func=self.refresh_playlist_ui)

    @staticmethod
    def format_duration_long(duration):
        total = int(duration)
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02}:{seconds:02}"

app = MelodyPlayer(name="MelodyPlayer", width=900, height=400)        