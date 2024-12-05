import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import csv

# Connect to SQLite Database
def connect_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add Student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()

    if not name or not age or not grade:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)
    messagebox.showinfo("Success", "Student added successfully!")
    refresh_table()

# View Students in Table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert('', tk.END, values=row)

# Delete Student
def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a student to delete!")
        return

    student_id = tree.item(selected_item)['values'][0]

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")
    refresh_table()

# Export Data to CSV
def export_to_csv():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Grade"])
        writer.writerows(rows)
    messagebox.showinfo("Success", "Data exported to students.csv successfully!")

# Main Window
connect_db()
root = tk.Tk()
root.title("Student Management System")

# Input Fields
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Age:").grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(frame_input)
entry_age.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
entry_grade = tk.Entry(frame_input)
entry_grade.grid(row=2, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Add Student", command=add_student)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

# Table to Display Students
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ("ID", "Name", "Age", "Grade")
tree = ttk.Treeview(frame_table, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Grade", text="Grade")
tree.pack()

btn_delete = tk.Button(root, text="Delete Student", command=delete_student)
btn_delete.pack(pady=5)

btn_export = tk.Button(root, text="Export to CSV", command=export_to_csv)
btn_export.pack(pady=5)

# Load Data into Table
refresh_table()

# Run Application
root.mainloop()
