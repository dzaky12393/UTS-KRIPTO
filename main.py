import customtkinter as ctk
from tkinter import messagebox
from vid_encrypt import VideoEncryptionApp
from teks_encrypt import TextEncryptionApp
from img_encrypt import ImageEncryptorApp
from lagu_encrypt import EncryptionAudioApp
from FILE_encrypt import EncryptionFilesApp

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Encryption Standard (DES) App")
        self.root.geometry("660x525")

        # Header
        self.header_label = ctk.CTkLabel(self.root, text="DES Encryption App", font=("Helvetica", 30, "bold"))
        self.header_label.pack(pady=(10, 20))

        # Tombol untuk membuka halaman enkripsi teks
        self.text_button = ctk.CTkButton(self.root, text="Text Encryption", command=self.open_text_page, width=300, height=70)
        self.text_button.pack(pady=10)

        # Tombol untuk membuka halaman enkripsi file
        self.file_button = ctk.CTkButton(self.root, text="File Encryption", command=self.open_file_page, width=300, height=70)
        self.file_button.pack(pady=10)

        # Tombol untuk membuka halaman enkripsi gambar
        self.image_button = ctk.CTkButton(self.root, text="Image Encryption", command=self.open_image_page, width=300, height=70)
        self.image_button.pack(pady=10)

        # Tombol untuk membuka halaman enkripsi video
        self.video_button = ctk.CTkButton(self.root, text="Video Encryption", command=self.open_video_page, width=300, height=70)
        self.video_button.pack(pady=10)

        # Tombol untuk membuka halaman enkripsi audio
        self.audio_button = ctk.CTkButton(self.root, text="Audio Encryption", command=self.open_audio_page, width=300, height=70)
        self.audio_button.pack(pady=10)

    # Metode untuk membuka halaman enkripsi gambar
    def open_image_page(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = ImageEncryptorApp(self.new_window)

    # Metode untuk membuka halaman enkripsi video
    def open_video_page(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = VideoEncryptionApp(self.new_window)

    # Metode untuk membuka halaman enkripsi teks
    def open_text_page(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = TextEncryptionApp(self.new_window)

    # Metode untuk membuka halaman enkripsi file
    def open_file_page(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = EncryptionFilesApp(self.new_window)

    # Metode untuk membuka halaman enkripsi audio
    def open_audio_page(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = EncryptionAudioApp(self.new_window)

# Titik masuk utama program
if __name__ == "__main__":
    app = ctk.CTk()
    ctk.set_default_color_theme("green")
    homepage = HomePage(app)
    app.mainloop()
