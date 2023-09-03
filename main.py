import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt a file using a given key
def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Decrypt a file using a given key
def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
    
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Function to select a folder
def select_folder():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        show_confirmation(selected_folder)

# Function to show a confirmation dialog
def show_confirmation(folder_path):
    confirmation_msg = "Caution: Your files are scheduled for encryption. Access will be restored only after the predetermined time has passed."

    confirm = messagebox.askokcancel("Confirmation", confirmation_msg)
    if confirm:
        set_timer(folder_path)

# Function to set the timer duration using an input dialog
def set_timer(folder_path):
    select_folder_button.grid_remove()
    title_label.grid_remove()

    timer_window = tk.Toplevel(root)
    timer_window.title("Set Timer")

    # Create a label for the subtitle
    subtitle_label = tk.Label(timer_window, text="Hide your files from yourself!", font=("Arial", 12), padx=20, pady=10)
    subtitle_label.grid(row=0, column=0, columnspan=2)

    # Create entry widgets for hours, minutes, and seconds
    hours_label = tk.Label(timer_window, text="Hours:")
    hours_label.grid(row=1, column=0)
    hours_entry = tk.Entry(timer_window)
    hours_entry.grid(row=1, column=1)
    hours_entry.insert(0, "1")  # Set the default value to 1 hour

    minutes_label = tk.Label(timer_window, text="Minutes:")
    minutes_label.grid(row=2, column=0)
    minutes_entry = tk.Entry(timer_window)
    minutes_entry.grid(row=2, column=1)
    minutes_entry.insert(0, "0")  # Set the default value to 0 minutes

    seconds_label = tk.Label(timer_window, text="Seconds:")
    seconds_label.grid(row=3, column=0)
    seconds_entry = tk.Entry(timer_window)
    seconds_entry.grid(row=3, column=1)
    seconds_entry.insert(0, "0")  # Set the default value to 0 seconds

    # Function to start encryption with the specified timer
    def start_encryption_with_timer():
        try:
            hours = int(hours_entry.get())
            minutes = int(minutes_entry.get())
            seconds = int(seconds_entry.get())
            
            timer_duration = hours * 3600 + minutes * 60 + seconds
            timer_window.destroy()

            start_encryption(folder_path, timer_duration)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for hours, minutes, and seconds.")

    start_button = tk.Button(timer_window, text="Start Encryption", command=start_encryption_with_timer)
    start_button.grid(row=4, columnspan=2)

# Function to start encryption after selecting a folder
def start_encryption(folder_path, timer_duration):
    # Show the confirmation message after starting the encryption
    confirmation_msg = "Encryption started. Your files will be encrypted. You will not be able to access them until the preset time has elapsed."
    messagebox.showinfo("Info", confirmation_msg)

    # Record the start time
    start_time = time.time()

    # Encrypt files in the selected folder
    key = generate_key()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

    # Countdown interface
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, timer_duration - elapsed_time)
        hours, remainder = divmod(int(remaining_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_label.config(text=f"Time remaining: {hours:02}:{minutes:02}:{seconds:02}", font=("Arial", 48))
        root.update()
        
        if elapsed_time >= timer_duration:
            break

    # Decrypt files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            decrypt_file(file_path, key)

    countdown_label.config(text="Decryption complete.", font=("Arial", 16))
    messagebox.showinfo("Info", "Decryption complete. You can now access your files.")
    
    select_folder_button.grid()
    title_label.grid()
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Allow closing the window when the timer is done

# Create the main window
root = tk.Tk()
root.title("Folder Encryption")

# Create a frame for the title and button and center-align it
frame = tk.Frame(root)
frame.pack(pady=20, padx=20, anchor="center")

# Create a label for the title
title_label = tk.Label(frame, text="Simple Timer File Encryption", font=("Arial", 16))
title_label.grid(row=0, column=0, padx=10)

# Create the "Select Folder" button
select_folder_button = tk.Button(frame, text="Select Folder", command=select_folder)
select_folder_button.grid(row=0, column=1, padx=10)

# Create a label for the countdown timer
countdown_label = tk.Label(root, text="", font=("Arial", 48))
countdown_label.pack()

# Function to prevent closing the window during encryption
def disable_close():
    pass

root.protocol("WM_DELETE_WINDOW", disable_close)

root.mainloop()
