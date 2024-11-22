import threading
import customtkinter as ctk
from yt_dlp import YoutubeDL

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_percentage = float(d.get('_percent_str', '0.0%').replace('%', '').strip()) / 100
        progress_bar.set(progress_percentage)
        status_label.configure(text=f"Downloading... {d['_percent_str']}", text_color="blue")

        if 'eta' in d and d['eta'] is not None:
            eta_formatted = format_time(d['eta'])
            estimated_time_label.configure(text=f"Estimated download time: {eta_formatted}")
        else:
            estimated_time_label.configure(text="Estimated download time: Calculating...")

    elif d['status'] == 'finished':
        status_label.configure(text="Download finished!", text_color="green")
        progress_bar.set(1.0)
        estimated_time_label.configure(text="Estimated download time: -")

def format_time(seconds):
    if seconds is None:
        return "Unknown"
    
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes} minutes {seconds} seconds"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} hours {minutes} minutes"

def download(yt_link):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'noprogress': True,
        'no_color': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_link])
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="red")

def start_download():
    yt_link = link_entry.get()
    if not yt_link:
        status_label.configure(text="Please input a valid URL", text_color="red")
        return

    download_thread = threading.Thread(target=download, args=(yt_link,))
    download_thread.start()

app = ctk.CTk()
app.geometry("500x350")
app.title("YouTube Downloader")
app.configure(fg_color="black")

header_label = ctk.CTkLabel(app, text="YouTube Downloader by _dunkelmut_", font=("Arial", 20), text_color="white")
header_label.pack(pady=20)

link_entry = ctk.CTkEntry(app, width=400, placeholder_text="Input your Youtube URL here")
link_entry.pack(pady=10)

download_button = ctk.CTkButton(
    app, text="start download", command=start_download,
    fg_color="red", hover_color="#361111"
)
download_button.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=400, progress_color="red")
progress_bar.set(0)
progress_bar.pack(pady=10)

estimated_time_label = ctk.CTkLabel(app, text="Estimated download time: -", font=("Arial", 14), text_color="white")
estimated_time_label.pack(pady=5)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 14), text_color="white")
status_label.pack(pady=10)

if __name__ == "__main__":
    app.mainloop()