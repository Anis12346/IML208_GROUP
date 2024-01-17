import tkinter as tk
from tkinter import messagebox
import datetime
import csv

class Task:
    def init(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False

class TaskTracker:
    def init(self):
        self.tasks = []

    def add_task(self, title, description, due_date, priority):
        task = Task(title, description, due_date, priority)
        self.tasks.append(task)

    def list_tasks(self):
        for task in self.tasks:
            completed_status = "Completed" if task.completed else "Incomplete"
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date}")
            print(f"Priority: {task.priority}")
            print(f"Status: {completed_status}")
            print()

    def mark_task_complete(self, title):
        for task in self.tasks:
            if task.title == title:
                task.completed = True
                break

    def delete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                break

    def search_tasks(self, keyword):
        matched_tasks = []
        for task in self.tasks:
            if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower():
                matched_tasks.append(task)
        return matched_tasks

    def filter_tasks_due_date(self, start_date, end_date):
        filtered_tasks = []
        for task in self.tasks:
            if start_date <= task.due_date <= end_date:
                filtered_tasks.append(task)
        return filtered_tasks

    def sort_tasks_by_priority(self):
        self.tasks.sort(key=lambda task: task.priority)

    def get_task_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(task.completed for task in self.tasks)
        current_date = datetime.datetime.now().date()
        tasks_due_within_week = sum(task.due_date <= current_date + datetime.timedelta(days=7) for task in self.tasks)

        return total_tasks, completed_tasks, tasks_due_within_week

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_priority(priority):
    return priority.lower() in ["low", "medium", "high"]

def clear_console():
    print("\033c", end="")

def display_menu():
    print("Task Tracker Menu:")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Search and Filter Tasks")
    print("6. Sort Tasks by Priority")
    print("7. Display Task Statistics")
    print("8. Exit")

def display_error(message):
    print(f"Error: {message}\n")

def display_success(message):
    print(f"Success: {message}\n")

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            completed_status = "Completed" if task.completed else "Incomplete"
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date}")
            print(f"Priority: {task.priority}")
            print(f"Status: {completed_status}")
            print()

def book_event():
    date = date_entry.get()
    time = time_entry.get()
    arena = arena_var.get()

    if not date or not time or not arena:
        messagebox.showerror("Error", "Please fill in all fields")
    else:
        event = {"Date": date, "Time": time, "Arena": arena}
        events.append(event)
        save_events()
        messagebox.showinfo("Success", "Event booked successfully")
        clear_fields()

def clear_fields():
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    arena_var.set(arena_choices[0])

def save_events():
    with open("events.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Time", "Arena"])
        writer.writeheader()
        writer.writerows(events)

def load_events():
    try:
        with open("events.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                events.append(row)
    except FileNotFoundError:
        pass

window = tk.Tk()
window.title("Sport Arena Booking System")
window.geometry("400x300")
window.configure(bg="lightblue")

date_label = tk.Label(window, text="Date (YYYY-MM-DD):")
date_label.pack()
date_entry = tk.Entry(window)
date_entry.pack()

time_label = tk.Label(window, text="Time (HH:MM):")
time_label.pack()
time_entry = tk.Entry(window)
time_entry.pack()

arena_label = tk.Label(window, text="Arena Type:")
arena_label.pack()
arena_var = tk.StringVar()
arena_choices = ["Unit Sukan", "Football Field", "Tennis Court", "Badminton Court", "Mini Stadium"]
arena_dropdown = tk.OptionMenu(window, arena_var, *arena_choices)
arena_dropdown.pack()

book_button = tk.Button(window, text="Book Event", command=book_event, width=20, height=2, bg="green", fg="white")
book_button.pack()

clear_button = tk.Button(window, text="Clear Fields", command=clear_fields, width=20, height=2)
clear_button.pack()

events = []
load_events()

events_label = tk.Label(window, text="Booked Events:")
events_label.pack()

events_textbox = tk.Text(window, height=8, width=40)
events_textbox.pack()

for event in events:
    events_textbox.insert(tk.END, f"Date: {event['Date']}\nTime: {event['Time']}\nArena: {event['Arena']}\n\n")

window.mainloop()