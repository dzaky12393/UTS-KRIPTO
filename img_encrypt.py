import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DES Image Encryption/Decryption")
        self.create_ui()
        self.image_shape = None

    def create_ui(self):
        self.key_label = tk.Label(self.root, text="Masukan Kunci:")
        self.key_label.pack(pady=5)

        self.key_entry = tk.Entry(self.root)
        self.key_entry.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.pack(pady=10)

        self.encrypt_button = tk.Button(self.root, text="Encrypt and Obfuscate Image", command=self.encrypt_image)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image)
        self.decrypt_button.pack(pady=10)

        self.display_label = tk.Label(self.root, text="")
        self.display_label.pack()

    def encrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg")])
        if not file_path:
            return

        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Kunci Harus Memiliki 8 Karakter!")
            return

        try:
            image = Image.open(file_path)
            image_data = np.array(image)
            self.image_shape = image_data.shape

            obfuscated_image_data = self.obfuscate_image(image_data)

            encrypted_data = self.des_encrypt_decrypt(obfuscated_image_data, key, mode='encrypt')

            save_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary Files", "*.bin")])
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(encrypted_data.tobytes())
                messagebox.showinfo("Success", f"Gambar Berhasil di Enkripsi dan Disimpan di : {save_path}")

            obfuscated_image = Image.fromarray(obfuscated_image_data.astype(np.uint8))
            self.display_image(obfuscated_image)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted File", filetypes=[("Binary Files", "*.bin")])
        if not file_path:
            return

        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Kunci Haruslah Memiliki 8 Karakter!")
            return

        if self.image_shape is None:
            messagebox.showerror("Error", "Tidak ada Gambar Dekrispsi!")
            return

        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()

            encrypted_data = np.frombuffer(encrypted_data, dtype=np.uint8)

            decrypted_data = self.des_encrypt_decrypt(encrypted_data, key, mode='decrypt')
            decrypted_image = Image.fromarray(decrypted_data.reshape(self.image_shape))

            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                decrypted_image.save(save_path)
                messagebox.showinfo("Success", f"Gambar Berhasil di Dekripsi dan Disimpan di : {save_path}")
                self.display_image(decrypted_image)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def des_encrypt_decrypt(self, data, key, mode='encrypt'):
        des = DES.new(key.encode('utf-8'), DES.MODE_CBC)
        flat_data = data.flatten().tobytes()
        
        if mode == 'encrypt':
            data_padded = pad(flat_data, DES.block_size)
            encrypted = des.iv + des.encrypt(data_padded)
            return np.frombuffer(encrypted, dtype=np.uint8)
        else:
            iv = data[:DES.block_size].tobytes()
            cipher_text = data[DES.block_size:].tobytes()
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv)
            decrypted = unpad(des.decrypt(cipher_text), DES.block_size)
            return np.frombuffer(decrypted, dtype=np.uint8)

    def display_image(self, image):
        self.display_label.config(text="Image displayed below")
        image.thumbnail((300, 300))
        img = ImageTk.PhotoImage(image)
        self.canvas.create_image(150, 150, image=img)
        self.canvas.image = img

    def obfuscate_image(self, image_data, pixel_size=10):
        height, width, _ = image_data.shape
        small_image = Image.fromarray(image_data).resize(
            (width // pixel_size, height // pixel_size), resample=Image.NEAREST
        )
        obfuscated_image = np.array(small_image.resize((width, height), Image.NEAREST))
        return obfuscated_image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
