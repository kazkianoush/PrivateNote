import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import ctypes

# Constants
HOME_DIR = os.path.expanduser("~")
HIDDEN_KEY_DIR = os.path.join(HOME_DIR, ".secure_keys")
NOTE_DIR = os.path.join(HOME_DIR, "secure_notes")
MASTER_KEY_FILE = os.path.join(HIDDEN_KEY_DIR, "master.key")


# Ensure directories exist
os.makedirs(HIDDEN_KEY_DIR, exist_ok=True)

# hide directory
FILE_ATTRIBUTE_HIDDEN = 0x02
ret = ctypes.windll.kernel32.SetFileAttributesW(HIDDEN_KEY_DIR, FILE_ATTRIBUTE_HIDDEN) 

os.makedirs(NOTE_DIR, exist_ok=True)


# Function to generate and save the master key
def generate_master_key():
    if not os.path.exists(MASTER_KEY_FILE):
        key = Fernet.generate_key()
        with open(MASTER_KEY_FILE, "wb") as key_file:
            key_file.write(key)
        # Set restrictive permissions for the master key file
        os.chmod(MASTER_KEY_FILE, 0o600)
        return key
    else:
        with open(MASTER_KEY_FILE, "rb") as key_file:
            return key_file.read()

# Load the master key
MASTER_KEY = generate_master_key()
fernet = Fernet(MASTER_KEY)

# Function to generate and save a key
def generate_key(note_name):
    key = Fernet.generate_key()
    encrypted_key = fernet.encrypt(key)
    key_path = os.path.join(HIDDEN_KEY_DIR, f"{note_name}.key")
    with open(key_path, "wb") as key_file:
        key_file.write(encrypted_key)
    os.chmod(key_path, 0o600)  # Set restrictive permissions for the key file
    return key

# Function to load the key
def load_key(note_name):
    key_path = os.path.join(HIDDEN_KEY_DIR, f"{note_name}.key")
    with open(key_path, "rb") as key_file:
        encrypted_key = key_file.read()
    return fernet.decrypt(encrypted_key)

# Encrypt the note
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Decrypt the note
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Save the note
def save_note():
    note_name = simpledialog.askstring("Note Name", "Enter the name for the note:")
    if not note_name:
        return
    note = text.get("1.0", tk.END).strip()
    if note:
        key = generate_key(note_name)
        encrypted_note = encrypt_message(note, key)
        note_path = os.path.join(NOTE_DIR, f"{note_name}.enc")
        with open(note_path, "wb") as file:
            file.write(encrypted_note)
        text.delete("1.0", tk.END)  # Clear the text box after saving the note
        messagebox.showinfo("Success", f"Note '{note_name}' saved successfully!")

# Load the note
def load_note():
    note_name = simpledialog.askstring("Note Name", "Enter the name of the note to load:")
    if not note_name:
        return
    try:
        key = load_key(note_name)
        note_path = os.path.join(NOTE_DIR, f"{note_name}.enc")
        with open(note_path, "rb") as file:
            encrypted_note = file.read()
        note = decrypt_message(encrypted_note, key)
        text.delete("1.0", tk.END)
        text.insert(tk.END, note)
        messagebox.showinfo("Success", f"Note '{note_name}' loaded successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Note '{note_name}' not found!")

# List available notes
def list_notes():
    notes = [f.split(".enc")[0] for f in os.listdir(NOTE_DIR) if f.endswith(".enc")]
    messagebox.showinfo("Notes", "Available Notes:\n" + "\n".join(notes))

# GUI setup
root = tk.Tk()
root.title("Secure Notes")

note_name_label = tk.Label(root, text="Note")
note_name_label.pack()

text = tk.Text(root, height=20, width=50)
text.pack()

save_button = tk.Button(root, text="Save Note", command=save_note)
save_button.pack()

load_button = tk.Button(root, text="Load Note", command=load_note)
load_button.pack()

list_button = tk.Button(root, text="List Notes", command=list_notes)
list_button.pack()

root.mainloop()
