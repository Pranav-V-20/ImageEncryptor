import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def encrypt_image(image_path, key, output_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return False

    # Convert the key into a numpy array for XOR operation
    key_array = np.frombuffer(key.encode('utf-8'), dtype=np.uint8)
    key_length = len(key_array)

    # Flatten the image and encrypt pixel values
    flat_image = image.flatten()
    encrypted_flat = np.empty_like(flat_image)

    for i, pixel in enumerate(flat_image):
        encrypted_flat[i] = pixel ^ key_array[i % key_length]

    # Reshape back to the original image shape
    encrypted_image = encrypted_flat.reshape(image.shape)

    # Save the encrypted image
    cv2.imwrite(output_path, encrypted_image)
    return True

def decrypt_image(image_path, key, output_path):
    # The decryption process is identical to encryption for XOR
    return encrypt_image(image_path, key, output_path)

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return filename

def save_file():
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return filename

def encrypt_action():
    input_path = browse_file()
    if not input_path:
        messagebox.showerror("Error", "No input file selected.")
        return

    output_path = save_file()
    if not output_path:
        messagebox.showerror("Error", "No output file selected.")
        return

    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "No encryption key provided.")
        return

    success = encrypt_image(input_path, key, output_path)
    if success:
        messagebox.showinfo("Success", f"Encrypted image saved at {output_path}")
    else:
        messagebox.showerror("Error", "Failed to encrypt the image.")

def decrypt_action():
    input_path = browse_file()
    if not input_path:
        messagebox.showerror("Error", "No input file selected.")
        return

    output_path = save_file()
    if not output_path:
        messagebox.showerror("Error", "No output file selected.")
        return

    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "No decryption key provided.")
        return

    success = decrypt_image(input_path, key, output_path)
    if success:
        messagebox.showinfo("Success", f"Decrypted image saved at {output_path}")
    else:
        messagebox.showerror("Error", "Failed to decrypt the image.")

# GUI Setup
app = tk.Tk()
app.title("Image Encryption/Decryption")

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(pady=20)

tk.Label(frame, text="Enter Encryption/Decryption Key:").grid(row=0, column=0, pady=5)
key_entry = tk.Entry(frame, show="*", width=30)
key_entry.grid(row=0, column=1, pady=5)

encrypt_button = tk.Button(frame, text="Encrypt Image", command=encrypt_action)
encrypt_button.grid(row=1, column=0, pady=10)

decrypt_button = tk.Button(frame, text="Decrypt Image", command=decrypt_action)
decrypt_button.grid(row=1, column=1, pady=10)

app.mainloop()
