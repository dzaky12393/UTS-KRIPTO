import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time

class VideoEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.file_to_encrypt = None
        self.encrypted_file = None
        self.root.title("Video Encryption/Decryption - DES")
        self.root.geometry("660x600")
        self.initialize_ui()

    def initialize_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=10, padx=5)

        self.select_button = ctk.CTkButton(self.main_frame, text="Browse Video File for Encryption", command=self.choose_video, width=626, height=70)
        self.select_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.file_label = ctk.CTkLabel(self.main_frame, text="No file selected for encryption")
        self.file_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)

        self.browse_encrypted_button = ctk.CTkButton(self.main_frame, text="Select Encrypted Video for Decryption", command=self.browse_encrypted_video, width=626, height=70)
        self.browse_encrypted_button.grid(row=3, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.encrypted_file_label = ctk.CTkLabel(self.main_frame, text="No encrypted file selected")
        self.encrypted_file_label.grid(row=4, column=0, columnspan=3, padx=6, pady=5)

        self.key_label = ctk.CTkLabel(self.main_frame, text="Enter 10-digit NIM:")
        self.key_label.grid(row=5, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.main_frame)
        self.key_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        self.encrypt_button = ctk.CTkButton(self.main_frame, text="Encrypt", command=self.encrypt_video, width=256)
        self.encrypt_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

        self.decrypt_button = ctk.CTkButton(self.main_frame, text="Decrypt", command=self.decrypt_video, width=256)
        self.decrypt_button.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

        self.reset_button = ctk.CTkButton(self.main_frame, text="Reset", command=self.reset_fields, fg_color="#D03F2C", hover_color="lightcoral", width=80)
        self.reset_button.grid(row=6, column=2, padx=5, pady=5)

        self.result_box = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.result_box.pack(pady=10)

    def choose_video(self):
        file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov")])
        if file:
            self.file_to_encrypt = file
            self.file_label.configure(text=f"Selected file: {os.path.basename(file)}")

    def browse_encrypted_video(self):
        file = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if file:
            self.encrypted_file = file
            self.encrypted_file_label.configure(text=f"Selected encrypted file: {os.path.basename(file)}")

    def encrypt_video(self):
        key = self.key_entry.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Error", "NIM must be a 10-digit number.")
            return
        if not self.file_to_encrypt:
            messagebox.showerror("Error", "Please select a video file to encrypt.")
            return

        des_key = self.format_key(key)
        original_size = os.path.getsize(self.file_to_encrypt)

        try:
            with open(self.file_to_encrypt, 'rb') as f:
                video_content = f.read()

            start_time = time.time()
            des = DES.new(des_key, DES.MODE_CBC)
            encrypted_content = des.iv + des.encrypt(pad(video_content, DES.block_size))
            save_file = self.file_to_encrypt + '.enc'
            with open(save_file, 'wb') as f:
                f.write(encrypted_content)
            duration = time.time() - start_time

            self.result_box.delete('1.0', 'end')
            self.result_box.insert('end', f"Encryption completed in {duration:.4f} seconds.\nEncrypted file saved to: {save_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt_video(self):
        key = self.key_entry.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Error", "NIM must be a 10-digit number.")
            return
        if not self.encrypted_file:
            messagebox.showerror("Error", "Please select an encrypted file for decryption.")
            return

        des_key = self.format_key(key)
        try:
            with open(self.encrypted_file, 'rb') as f:
                encrypted_content = f.read()

            start_time = time.time()
            iv = encrypted_content[:DES.block_size]
            cipher_text = encrypted_content[DES.block_size:]
            des = DES.new(des_key, DES.MODE_CBC, iv)
            decrypted_content = unpad(des.decrypt(cipher_text), DES.block_size)

            save_file = self.encrypted_file.rsplit('.', 1)[0] + '_decrypted.mp4'
            with open(save_file, 'wb') as f:
                f.write(decrypted_content)
            duration = time.time() - start_time

            self.result_box.delete('1.0', 'end')
            self.result_box.insert('end', f"Decryption completed in {duration:.2f} seconds.\nDecrypted file saved to: {save_file}")
        except ValueError:
            messagebox.showerror("Error", "Decryption failed. Invalid key or corrupted file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def reset_fields(self):
        self.file_label.configure(text="No file selected for encryption")
        self.encrypted_file_label.configure(text="No encrypted file selected")
        self.file_to_encrypt = None
        self.encrypted_file = None
        self.key_entry.delete(0, 'end')
        self.result_box.delete('1.0', 'end')

    def format_key(self, key):
        return key.encode('utf-8').ljust(8)[:8]

if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoEncryptionApp(root)
    root.mainloop()
