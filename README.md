# Private Note

Private Note is a Python application that allows users to create, encrypt, save, and load notes securely on their computer. Built using tkinter for the GUI and cryptography.fernet for encryption, it ensures that notes are stored in an encrypted format, enhancing data privacy and security.

## Features

- **Encryption**: Notes are encrypted using the Fernet symmetric encryption scheme, ensuring that only the user with the decryption key (stored securely) can read the notes.
- **Graphical User Interface (GUI)**: The application provides a simple GUI using tkinter, making it user-friendly and accessible.
- **Save and Load**: Users can save encrypted notes to their local file system and load them later for viewing or editing.
- **Key Management**: Uses a master key to encrypt and decrypt individual note keys, stored securely in a hidden directory (`/.secure_keys`) to prevent unauthorized access.

## Why Private Note?

Traditional text editors like Notepad lack security features, leaving notes vulnerable to unauthorized access if someone gains access to the computer. Private Note addresses this by:
- Encrypting notes with strong encryption algorithms.
- Storing encryption keys in a hidden directory with restricted access.

## Installation

To run Private Note locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kazkianoush/PrivateNote.git
   cd PrivateNote
