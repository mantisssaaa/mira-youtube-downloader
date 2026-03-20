import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os
import sys
import subprocess

LANGUAGES = {
    "Русский": {
        "title": "SEQUOIA DOWNLOADER",
        "url_placeholder": "Вставьте ссылку (Ctrl+V)...",
        "btn_analyze": "АНАЛИЗИРОВАТЬ",
        "label_res": "Выберите разрешение:",
        "label_fmt": "Итоговый формат:",
        "btn_path": "ВЫБРАТЬ ПАПКУ",
        "path_none": "Папка не выбрана",
        "btn_download": "СКАЧАТЬ",
        "btn_open": "Открыть папку",
        "status_ready": "Готов к работе",
        "status_loading": "Загрузка:",
        "status_fin": "Конвертация звука (AAC)...",
        "status_done": "ЗАВЕРШЕНО!",
        "error_link": "Ошибка в ссылке или сети"
    },
    "English": {
        "title": "SEQUOIA DOWNLOADER",
        "url_placeholder": "Paste link here (Ctrl+V)...",
        "btn_analyze": "ANALYZE VIDEO",
        "label_res": "Select resolution:",
        "label_fmt": "Output format:",
        "btn_path": "SELECT FOLDER",
        "path_none": "No folder selected",
        "btn_download": "DOWNLOAD",
        "btn_open": "Open Folder",
        "status_ready": "Ready",
        "status_loading": "Downloading:",
        "status_fin": "Finalizing (AAC Audio)...",
        "status_done": "FINISHED!",
        "error_link": "Link or network error"
    },
    "Español": {
        "title": "SEQUOIA DOWNLOADER",
        "url_placeholder": "Pegar enlace (Ctrl+V)...",
        "btn_analyze": "ANALIZAR",
        "label_res": "Seleccionar resolución:",
        "label_fmt": "Formato final:",
        "btn_path": "SELECCIONAR CARPETA",
        "path_none": "Carpeta no seleccionada",
        "btn_download": "DESCARGAR",
        "btn_open": "Abrir carpeta",
        "status_ready": "Listo",
        "status_loading": "Descargando:",
        "status_fin": "Finalizando (Audio AAC)...",
        "status_done": "¡COMPLETADO!",
        "error_link": "Error de enlace or red"
    }
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "Русский"
        self.title("MiraYouTubeDownloader")
        self.geometry("620x660")

        try:
            icon_p = resource_path("icon.ico")
            self.after(200, lambda: self.iconbitmap(icon_p))
        except: pass

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.lang_menu = ctk.CTkOptionMenu(self.main_frame, values=list(LANGUAGES.keys()), 
                                           command=self.change_language, width=120)
        self.lang_menu.pack(pady=10, padx=20, anchor="ne")

        self.label_title = ctk.CTkLabel(self.main_frame, text="", font=("Impact", 28), text_color="#3b8ed0")
        self.label_title.pack(pady=(10, 15))
        
        self.entry_url = ctk.CTkEntry(self.main_frame, width=480, height=40)
        self.entry_url.pack(pady=10)
        self.entry_url.bind("<Control-v>", self.handle_clipboard)
        self.entry_url.bind("<Control-V>", self.handle_clipboard)
        self.entry_url.bind("<Control-KeyPress>", self.handle_clipboard)

        self.btn_fetch = ctk.CTkButton(self.main_frame, command=self.fetch_formats, fg_color="#34495e")
        self.btn_fetch.pack(pady=10)

        self.label_q = ctk.CTkLabel(self.main_frame, text="")
        self.label_q.pack()
        self.option_quality = ctk.CTkOptionMenu(self.main_frame, values=["..."], width=300)
        self.option_quality.pack(pady=5)

        self.label_f = ctk.CTkLabel(self.main_frame, text="")
        self.label_f.pack()
        self.option_ext = ctk.CTkOptionMenu(self.main_frame, values=["mp4", "webm"], width=150)
        self.option_ext.pack(pady=5)
        
        self.btn_path = ctk.CTkButton(self.main_frame, command=self.choose_path, fg_color="transparent", border_width=1)
        self.btn_path.pack(pady=10)
        
        self.label_path_text = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 10), text_color="gray")
        self.label_path_text.pack()

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=480, progress_color="#2ecc71")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12))
        self.info_label.pack()

        self.btn_download = ctk.CTkButton(self.main_frame, command=self.start_download, height=50, width=250,
                                         fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 16, "bold"))
        self.btn_download.pack(pady=20)

        self.btn_open = ctk.CTkButton(self.main_frame, text="", command=self.open_folder, state="disabled")
        self.btn_open.pack()

        self.save_path = ""
        self.formats_dict = {}
        self.update_ui_text()

    def handle_clipboard(self, event):
        if event.keycode == 86 or event.keysym.lower() == 'v':
            try:
                self.entry_url.insert('insert', self.clipboard_get())
                return "break"
            except: pass

    def change_language(self, new_lang):
        self.current_lang = new_lang
        self.update_ui_text()

    def update_ui_text(self):
        ln = LANGUAGES[self.current_lang]
        self.label_title.configure(text=ln["title"])
        self.entry_url.configure(placeholder_text=ln["url_placeholder"])
        self.btn_fetch.configure(text=ln["btn_analyze"])
        self.label_q.configure(text=ln["label_res"])
        self.label_f.configure(text=ln["label_fmt"])
        self.btn_path.configure(text=ln["btn_path"])
        if not self.save_path:
            self.label_path_text.configure(text=ln["path_none"])
        else:
            self.label_path_text.configure(text=f"{self.save_path}")
        self.btn_download.configure(text=ln["btn_download"])
        self.btn_open.configure(text=ln["btn_open"])
        self.info_label.configure(text=ln["status_ready"])

    def choose_path(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.label_path_text.configure(text=f"{self.save_path}", text_color="white")

    def open_folder(self):
        if self.save_path:
            subprocess.Popen(f'explorer "{os.path.normpath(self.save_path)}"')

    def fetch_formats(self):
        url = self.entry_url.get().strip()
        if not url: return
        self.btn_fetch.configure(state="disabled")
        
        def task():
            try:
                with yt_dlp.YoutubeDL() as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    unique_res = {}
                    for f in formats:
                        h = f.get('height')
                        if h and f.get('vcodec') != 'none':
                            res_key = f"{h}p"
                            unique_res[res_key] = f['format_id']
                    
                    sorted_res = sorted(unique_res.keys(), key=lambda x: int(x[:-1]), reverse=True)
                    self.formats_dict = unique_res
                    self.option_quality.configure(values=sorted_res)
                    if sorted_res: self.option_quality.set(sorted_res[0])
                self.btn_fetch.configure(state="normal")
            except:
                self.btn_fetch.configure(state="normal")
        
        threading.Thread(target=task, daemon=True).start()

    def progress_hook(self, d):
        ln = LANGUAGES[self.current_lang]
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                self.progress_bar.set(float(p) / 100)
                self.info_label.configure(text=f"{ln['status_loading']} {d.get('_percent_str', '0%')}")
            except: pass
        if d['status'] == 'finished':
            self.info_label.configure(text=ln["status_fin"])

    def start_download(self):
        url = self.entry_url.get().strip()
        res = self.option_quality.get()
        target_ext = self.option_ext.get()
        ln = LANGUAGES[self.current_lang]
        
        if not url or not self.save_path or res == "...":
            return

        self.btn_download.configure(state="disabled")
        
        def download_task():
            opts = {
                'format': f'{self.formats_dict[res]}+bestaudio/best',
                'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'ffmpeg_location': resource_path("ffmpeg.exe"),
                'merge_output_format': target_ext,
                'postprocessor_args': ['-c:a', 'aac', '-b:a', '192k'],
            }
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                self.info_label.configure(text=ln["status_done"])
                self.btn_open.configure(state="normal", fg_color="#3b8ed0")
                messagebox.showinfo("Done", ln["status_done"])
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.btn_download.configure(state="normal")

        threading.Thread(target=download_task, daemon=True).start()

if __name__ == "__main__":
    app = YTDownloader()
    app.mainloop()