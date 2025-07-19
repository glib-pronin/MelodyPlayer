import customtkinter as ctk
from tkinter import filedialog
from mutagen.mp3 import MP3
import shutil, os
from ..database import add_track_to_db

class AddTrackWindow(ctk.CTkToplevel):
    def __init__(self, fg_color, refresh_func, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        # Налаштовуємо вікно
        self.title("Додати пісню")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width-500)//2
        y = (screen_height - 200)//2
        self.geometry(f"500x200+{x}+{y}")
        self.grab_set()

        self.refresh_func=refresh_func

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((1, 2, 3), weight=1)
        # Поле для введення виконавця
        self.artist_entry = ctk.CTkEntry(self, placeholder_text="Виконавець")
        self.artist_entry.grid(row=1, column=0, pady=10, padx=10)
        # Поле для введення назви
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Назва пісні")
        self.title_entry.grid(row=1, column=1, pady=10, padx=10)
        # Кнопка для вибору файлу
        self.select_button = ctk.CTkButton(self, text="Вибрати файл", command=self.select_file)
        self.select_button.grid(row=2, column=0, pady=10, padx=10)
        # Відображення назви пісні
        self.select_label = ctk.CTkLabel(self, text="Обраний файл: ще не вибрали")
        self.select_label.grid(row=2, column=1, pady=10, padx=10)
        # Кнопка додавання
        self.add_button = ctk.CTkButton(self, text="Додати", command=self.add_track)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.selected_file = None
    # Функція вибору файлу
    def select_file(self):
        self.selected_file = filedialog.askopenfilename(title="Виберіть аудіофайл", filetypes=(("Audio", "*.mp3"),))
        if self.selected_file:
            path_items = self.selected_file.split("/")
            self.select_label.configure(text=path_items[-1])
    # Функція додавання файлу
    def add_track(self):
        # Отримуємо значення з полів
        artist = self.artist_entry.get()
        track = self.title_entry.get()
        # Перевіряємо, чи надав користувач всю потрібну інформацію
        if not artist or not track or not self.selected_file:
            warn_label = ctk.CTkLabel(self, text="Ви не заповнили усі поля або не вибрали файл", text_color="red", font=("Arial", 16))
            warn_label.grid(row=0, column=0, columnspan=2, pady=10)
            return
        # Отримали тривалість пісні
        audio = MP3(self.selected_file)
        duration = round(audio.info.length)
        try:
            # Копіюємо файл файл
            destination = os.path.abspath(__file__+"/../../../assets/music")
            os.makedirs(destination, exist_ok=True)
            shutil.copy(src=self.selected_file, dst=destination)
            # Додаємо в БД
            add_track_to_db(track, artist, self.select_label.cget("text"), duration)
        except Exception as e:
            warn_label = ctk.CTkLabel(self, text="Сталася помилка при додаванні файлу", text_color="red", font=("Arial", 16))
            warn_label.grid(row=0, column=0, columnspan=2, pady=10)
            return
        # Оновлюємо застосунок та закриваємо модальне вікно
        self.refresh_func()
        self.destroy()


