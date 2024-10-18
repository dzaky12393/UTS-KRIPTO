import customtkinter as ctk
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

class EncryptionAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Encryption/Decryption (DES)")
        self.root.geometry("660x525")
        self.file_path = None
        self.initialize_ui()

    def initialize_ui(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=5)

        self.browse_button = ctk.CTkButton(self.frame, text="Browse Audio File", command=self.browse_file, width=626, height=70)
        self.browse_button.grid(row=1, column=0, padx=6, pady=5, sticky='ew')

        self.input_file_label = ctk.CTkLabel(self.frame, text="No file selected")
        self.input_file_label.grid(row=2, column=0, padx=6, pady=5)

        self.key_label = ctk.CTkLabel(self.frame, text="Enter 8-Char Key:")
        self.key_label.grid(row=3, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.frame)
        self.key_entry.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        self.encrypt_button = ctk.CTkButton(self.frame, text="Encrypt", command=self.encrypt_file, width=256)
        self.encrypt_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.decrypt_button = ctk.CTkButton(self.frame, text="Decrypt", command=self.decrypt_file, width=256)
        self.decrypt_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.aac *.enc")])
        if self.file_path:
            self.input_file_label.configure(text=os.path.basename(self.file_path))

    def encrypt_file(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Key must be 8 characters long.")
            return

        if not self.file_path:
            messagebox.showerror("Error", "Please select an audio file first.")
            return

        try:
            with open(self.file_path, 'rb') as file:
                data = file.read()

            des = DES.new(key.encode('utf-8'), DES.MODE_CBC)
            encrypted_data = des.iv + des.encrypt(pad(data, DES.block_size))

            save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted files", "*.enc")])
            if save_path:
                with open(save_path, 'wb') as file:
                    file.write(encrypted_data)
                messagebox.showinfo("Success", f"Audio encrypted and saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt_file(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Key must be 8 characters long.")
            return

        if not self.file_path or not self.file_path.endswith(".enc"):
            messagebox.showerror("Error", "Please select a valid encrypted (.enc) file.")
            return

        try:
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()

            iv = encrypted_data[:DES.block_size]
            cipher_text = encrypted_data[DES.block_size:]
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv)
            decrypted_data = unpad(des.decrypt(cipher_text), DES.block_size)

            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
            if save_path:
                with open(save_path, 'wb') as file:
                    file.write(decrypted_data)
                messagebox.showinfo("Success", f"Audio decrypted and saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EncryptionAudioApp(root)
    root.mainloop()
