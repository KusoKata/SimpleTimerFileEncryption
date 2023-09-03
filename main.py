import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
    
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def set_timer():
    timer_window = tk.Toplevel(root)
    timer_window.title("Set Timer")

    hours_label = tk.Label(timer_window, text="Hours:")
    hours_label.grid(row=0, column=0)
    hours_entry = tk.Entry(timer_window)
    hours_entry.grid(row=0, column=1)

    minutes_label = tk.Label(timer_window, text="Minutes:")
    minutes_label.grid(row=1, column=0)
    minutes_entry = tk.Entry(timer_window)
    minutes_entry.grid(row=1, column=1)

    seconds_label = tk.Label(timer_window, text="Seconds:")
    seconds_label.grid(row=2, column=0)
    seconds_entry = tk.Entry(timer_window)
    seconds_entry.grid(row=2, column=1)

    def start_encryption_with_timer():
        try:
            hours = int(hours_entry.get())
            minutes = int(minutes_entry.get())
            seconds = int(seconds_entry.get())
            
            timer_duration = hours * 3600 + minutes * 60 + seconds
            timer_window.destroy()

            selected_folder = filedialog.askdirectory()
            if selected_folder:
                start_encryption(selected_folder, timer_duration)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for hours, minutes, and seconds.")

    start_button = tk.Button(timer_window, text="Start Encryption", command=start_encryption_with_timer)
    start_button.grid(row=3, columnspan=2)

def start_encryption(folder_path, timer_duration):
    # Record the start time
    start_time = time.time()

    key = generate_key()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, timer_duration - elapsed_time)
        hours, remainder = divmod(int(remaining_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_label.config(text=f"Time remaining: {hours:02}:{minutes:02}:{seconds:02}", font=("Arial", 48))
        root.update()
        
        if elapsed_time >= timer_duration:
            break

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            decrypt_file(file_path, key)

    countdown_label.config(text="Decryption complete.", font=("Arial", 16))
    messagebox.showinfo("Info", "Decryption complete.")

root = tk.Tk()
root.title("Folder Encryption")

countdown_label = tk.Label(root, text="", font=("Arial", 48))
countdown_label.pack(pady=20)

select_folder_button = tk.Button(root, text="Select Folder and Set Timer", command=set_timer)
select_folder_button.pack()

root.mainloop()
