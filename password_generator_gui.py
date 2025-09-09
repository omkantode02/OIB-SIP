# file: password_generator_gui.py
import tkinter as tk
from tkinter import messagebox
import random, string

def generate_password():
    try:
        length = int(entry_length.get())
        if length <= 0:
            messagebox.showerror("Error", "Password length must be positive.")
            return

        char_pool = ""
        if var_lower.get():
            char_pool += string.ascii_lowercase
        if var_upper.get():
            char_pool += string.ascii_uppercase
        if var_digits.get():
            char_pool += string.digits
        if var_symbols.get():
            char_pool += "!@#$%^&*()-_=+[]{};:,.?/"

        if not char_pool:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        password = "".join(random.choice(char_pool) for _ in range(length))
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")

def copy_to_clipboard():
    password = entry_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x350")

# Length input
tk.Label(root, text="Password Length:").pack(pady=5)
entry_length = tk.Entry(root)
entry_length.pack(pady=5)

# Character set options
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=var_lower).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=var_upper).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Include Digits (0-9)", variable=var_digits).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Include Symbols (!@#$...)", variable=var_symbols).pack(anchor="w", padx=20)

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, bg="green", fg="white").pack(pady=10)

# Display generated password
entry_password = tk.Entry(root, font=("Arial", 12), justify="center")
entry_password.pack(pady=10, fill="x", padx=20)

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="blue", fg="white").pack(pady=5)

root.mainloop()
