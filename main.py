import cv2
import pytesseract
import matplotlib.pyplot as plt
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

data_file = "calorie_log.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

def extract_calories_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    calories = sum(int(word) for word in text.split() if word.isdigit())
    return calories

def add_calories_manually(food_item, calorie_count):
    data = load_data()
    date = datetime.today().strftime('%Y-%m-%d')
    if date not in data:
        data[date] = {}
    data[date][food_item] = data[date].get(food_item, 0) + int(calorie_count)
    save_data(data)
    messagebox.showinfo("Success", f"{food_item} added with {calorie_count} calories on {date}.")

def submit_photo():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            calories = extract_calories_from_image(file_path)
            data = load_data()
            date = datetime.today().strftime('%Y-%m-%d')
            if date not in data:
                data[date] = {}
            data[date][file_path] = data[date].get(file_path, 0) + calories
            save_data(data)
            messagebox.showinfo("Success", f"Extracted {calories} calories from image on {date}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {e}")

def plot_calorie_graph():
    data = load_data()
    if not data:
        messagebox.showinfo("No Data", "No calorie data to display.")
        return

    dates = list(data.keys())
    total_calories = [sum(data[date].values()) for date in dates]

    plt.plot(dates, total_calories, marker='o', linestyle='-', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Total Calories')
    plt.title('Daily Calorie Intake Overview')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.show()

def create_gui():
    root = tk.Tk()
    root.title("Calorie Tracker")
    root.geometry("400x300")

    tk.Label(root, text="Food Item:").pack(pady=5)
    food_entry = tk.Entry(root)
    food_entry.pack(pady=5)

    tk.Label(root, text="Calories:").pack(pady=5)
    calorie_entry = tk.Entry(root)
    calorie_entry.pack(pady=5)

    tk.Button(root, text="Add Calories", command=lambda: add_calories_manually(food_entry.get(), calorie_entry.get())).pack(pady=10)
    tk.Button(root, text="Submit Photo", command=submit_photo).pack(pady=10)
    tk.Button(root, text="View Graph", command=plot_calorie_graph).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()