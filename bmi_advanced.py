# file: bmi_advanced.py
import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt

HISTORY_FILE = "bmi_history.csv"

# --- Helper functions ---
def calculate_bmi(weight, height):
    """Calculate BMI using formula."""
    return weight / (height ** 2)

def classify_bmi(bmi):
    """Classify BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_to_history(name, weight, height, bmi, category):
    """Save record to CSV file."""
    new_file = not os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["Name", "Weight (kg)", "Height (m)", "BMI", "Category"])
        writer.writerow([name, weight, height, round(bmi, 2), category])

def view_history():
    """Open BMI history file in a popup window."""
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo("Info", "No history available.")
        return
    
    history_win = tk.Toplevel(root)
    history_win.title("BMI History")
    history_win.geometry("400x300")
    
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()
    
    text = tk.Text(history_win, wrap="word")
    text.pack(fill="both", expand=True)
    text.insert("1.0", "".join(lines))

def show_trend():
    """Show BMI trend graph from history."""
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo("Info", "No history available to plot.")
        return
    
    names, bmis = [], []
    with open(HISTORY_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row["Name"])
            bmis.append(float(row["BMI"]))
    
    plt.figure(figsize=(7,5))
    plt.plot(names, bmis, marker="o", linestyle="-", color="blue")
    plt.axhline(18.5, color="green", linestyle="--", label="Normal Lower")
    plt.axhline(24.9, color="orange", linestyle="--", label="Normal Upper")
    plt.title("BMI Trend")
    plt.xlabel("Users")
    plt.ylabel("BMI")
    plt.legend()
    plt.show()

# --- Main function for GUI ---
def on_calculate():
    try:
        name = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Please enter positive numbers.")
            return

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        # Update result on screen
        label_result.config(text=f"{name}, your BMI is {bmi:.2f}\nCategory: {category}", fg="blue")

        # Save result
        save_to_history(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("350x350")

# Input fields
tk.Label(root, text="Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

tk.Label(root, text="Weight (kg):").pack(pady=5)
entry_weight = tk.Entry(root)
entry_weight.pack(pady=5)

tk.Label(root, text="Height (m):").pack(pady=5)
entry_height = tk.Entry(root)
entry_height.pack(pady=5)

# Buttons
btn_calc = tk.Button(root, text="Calculate BMI", command=on_calculate, bg="green", fg="white")
btn_calc.pack(pady=10)

btn_history = tk.Button(root, text="View History", command=view_history, bg="blue", fg="white")
btn_history.pack(pady=5)

btn_trend = tk.Button(root, text="Show Trend Graph", command=show_trend, bg="purple", fg="white")
btn_trend.pack(pady=5)

# Result label
label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.pack(pady=10)

root.mainloop()
