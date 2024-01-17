import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to SQLite database
conn = sqlite3.connect('sports_inventory.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sports_equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        equipment TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        sport TEXT NOT NULL,
        price REAL NOT NULL
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
conn.commit()


# CRUD operations

def create_equipment(name, equipment, quantity, sport, price):
    cursor.execute('''
        INSERT INTO sports_equipment (name, equipment, quantity, sport, price) VALUES (?, ?, ?, ?, ?)
    ''', (name, equipment, quantity, sport, price))
    conn.commit()

def read_all_equipment(role=None):
    if role == 'admin':
        cursor.execute('''
            SELECT * FROM sports_equipment
        ''')
    else:
        cursor.execute('SELECT equipment, quantity, sport FROM sports_equipment')

    return cursor.fetchall()

def update_equipment(equipment_id, name, quantity, sport):
    cursor.execute('''
        UPDATE sports_equipment SET name = ?, quantity = ?, sport = ? WHERE id = ?
    ''', (name, quantity, sport, equipment_id))
    conn.commit()

def delete_equipment(equipment_id):
    cursor.execute('''
        DELETE FROM sports_equipment WHERE id = ?
    ''', (equipment_id,))
    conn.commit()

# GUI
class SportsEquipmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Equipments Inventory")
        self.root.geometry('1500x500')

        #set background color
        background_color = '#c1cdcd'
        self.root.configure(bg=background_color)

#login part
        self.logged_in_user = None

        self.login()

    def login(self):
        
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry('300x300')
        login_window.configure(bg='#eedfcc')

        ttk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show='*')
        password_entry.pack(pady=5)

        
        ttk.Button(login_window, text="Login", command=lambda: self.check_login(login_window, username_entry.get(), password_entry.get())).pack(pady=10)

        ttk.Label(login_window, text="Not an admin?").pack(pady=20)
        ttk.Button(login_window, text='Skip', command=lambda: self.skip_login(login_window)).pack(pady=1)

        self.root.withdraw()

    def skip_login(self, login_window):
        login_window.destroy()
        self.show_limited_view_window()

    def show_limited_view_window(self):
        limited_view_window = tk.Toplevel(self.root)
        limited_view_window.title("Limited View")
        limited_view_window.geometry('800x400')
        limited_view_window.configure(bg='#c1cdcd')

        limited_view_window.columnconfigure(0, weight=1)
        limited_view_window.columnconfigure(1, weight=1)
        limited_view_window.columnconfigure(2, weight=1)


        self.tree = ttk.Treeview(limited_view_window, columns=('Equipments', 'Quantity Available', 'Sport'), show='headings')
        self.tree.heading('Equipments', text='Equipments')
        self.tree.heading('Quantity Available', text='Quantity Available')
        self.tree.heading('Sport', text='Sport')
        self.tree.pack(pady=10)

        #fetch data
        limited_data = read_all_equipment(self.get_user_role(self.logged_in_user))  

        for data in limited_data:
            self.tree.insert('', 'end', values=(data[0], data[1], data[2]))

        self.tree.pack(pady=10)   

    
    def read_all_equipment_by_role(role=None):
        if role == 'admin':
            # Fetch all equipment data for admins
            cursor.execute('''
                SELECT id, name, equipment, quantity, sport, price FROM sports_equipment
            ''')
        else:
            # Fetch limited data for non-admin users
            cursor.execute('SELECT equipment, quantity, sport FROM sports_equipment')

        return cursor.fetchall()
    
    def delete_selected_equipment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        values = self.tree.item(selected_item, 'values')
        if not values:
            return

        equipment_id = self.tree.item(selected_item, 'values')[0]
        delete_equipment(equipment_id)
        self.refresh_table()


    #User authentication and authorization
    def create_user(self, username, password, role=None):

        if role is None:
            role = 'student'
        
        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            # If the user doesn't exist, create a new one
            cursor.execute('''
                        INSERT INTO users (username, password, role) VALUES (?,?,?)
                        ''', (username, password, role))
            conn.commit()

        else:
            # If the user already exists, update their password and role
            cursor.execute('UPDATE users SET password = ?, role = ? WHERE username = ?', (password, role, username))
            conn.commit()


    def check_login(self, login_window, username, password):
        cursor.execute('''
            SELECT * FROM users WHERE username = ?  AND password = ?
                       ''', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            login_window.destroy()
            self.logged_in_user = username
            self.show_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def get_user_role(self, current_user):
        cursor.execute('''
            SELECT role FROM users WHERE username = ?
        ''', (current_user,))
        role = cursor.fetchone()
        return role[0] if role else None

    def show_main_window(self):
        self.root.deiconify()

        if self.logged_in_user and self.get_user_role(self.logged_in_user) == 'admin':
            self.root.title("Sport Equipments Inventory (Admin)")
            self.root.geometry('1500x500')
            

            self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Equipments', 'Quantity Available', 'Sport', 'Price'), show='headings')
            self.tree.heading('ID', text='ID')
            self.tree.heading('Name', text='Name')
            self.tree.heading('Equipments', text='Equipments')
            self.tree.heading('Quantity Available', text='Quantity Available')
            self.tree.heading('Sport', text='Sport')
            self.tree.heading('Price', text='Price')
            self.tree.pack(pady=10)

            btn_frame = ttk.Frame(root)
            btn_frame.pack(pady=10)


            ttk.Button(btn_frame, text="Add Equipment", command=self.show_add_dialog, style='AddButton.TButton').grid(row=0, column=0, padx=5)
            ttk.Button(btn_frame, text="Update Equipment", command=self.show_update_dialog, style='UpdateButton.TButton').grid(row=0, column=1, padx=5)
            ttk.Button(btn_frame, text="Delete Equipment", command=self.delete_selected_equipment, style='DeleteButton.TButton').grid(row=0, column=2, padx=5)
        
            for col in self.tree['columns']:
                self.tree.column(col, width=150)  # Adjust the width as needed

            self.refresh_table()

        else:
            self.root.title("Limited View")
            self.root.geometry('800x400')

            self.tree = ttk.Treeview(self.root, columns=('Equipments', 'Quantity Available', 'Sport'), show='headings')
            self.tree.heading('Equipments', text='Equipments')
            self.tree.heading('Quantity Available', text='Quantity Available')
            self.tree.heading('Sport', text='Sport')

            limited_data = read_all_equipment(self.get_user_role(self.logged_in_user))

            for data in limited_data:
                self.tree.insert('', 'end', values=data)

                self.tree.pack(pady=10)

            for col in self.tree['columns']:
                self.tree.column(col, width=150)  # Adjust the width as needed

            self.tree.pack(pady=10)


        #Custom sytle for the buttons
        self.root.style = ttk.Style()
        self.root.style.configure('AddButton.TButton', bg='#ffe4e1')
        self.root.style.configure('UpdateButton.TButton', bg='#eee8aa')
        self.root.style.configure('DeleteButton.TButton', bg='#ffdab9')

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            equipment_list = read_all_equipment(self.get_user_role(self.logged_in_user))  # Pass the role parameter
        for equipment in equipment_list:
            if self.get_user_role(self.logged_in_user) == 'admin':
                self.tree.insert('', 'end', values=(equipment[0], equipment[1], equipment[2], equipment[3], equipment[4], equipment[5]))
            else:
                self.tree.insert('', 'end', values=(equipment[1], equipment[2], equipment[3]))

        self.tree.pack(pady=10) 

    def show_add_dialog(self):
        add_dialog = tk.Toplevel(self.root)
        add_dialog.title("Add Equipment")
        add_dialog.geometry('300x200')
        add_dialog.configure(bg='#fff0f5')

        ttk.Label(add_dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_dialog)                   
        name_entry.grid(row=0, column=1, padx=5, pady=5,)

        ttk.Label(add_dialog, text="Equipments:").grid(row=1, column=0, padx=5, pady=5)
        equipment_entry = ttk.Entry(add_dialog)                   
        equipment_entry.grid(row=1, column=1, padx=5, pady=5,)

        ttk.Label(add_dialog, text="Quantity Available:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(add_dialog)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_dialog, text="Sport:").grid(row=3, column=0, padx=5, pady=5)
        sport_entry = ttk.Entry(add_dialog)
        sport_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(add_dialog, text="Price:").grid(row=4, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(add_dialog)                   
        price_entry.grid(row=4, column=1, padx=5, pady=5,)

        ttk.Button(add_dialog, text="Add", command=lambda: self.add_equipment(add_dialog, name_entry.get(), 
                                                                      equipment_entry.get(), quantity_entry.get(), 
                                                                      sport_entry.get(), float(price_entry.get()))).grid(row=5, column=1, pady=10)

    def add_equipment(self, dialog, name, equipment, quantity, sport, price):
        create_equipment(name, equipment, quantity, sport, price)
        self.refresh_table()
        dialog.destroy()

    def show_update_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        update_dialog = tk.Toplevel(self.root)
        update_dialog.title("Update Equipment")
        update_dialog.geometry('300x200')
        update_dialog.configure(bg='#e6e6fa')

        equipment_id = self.tree.item(selected_item, 'values')[0]

        ttk.Label(update_dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(update_dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(update_dialog, text="Equipments:").grid(row=1, column=0, padx=5, pady=5)
        equipment_entry = ttk.Entry(update_dialog)                   
        equipment_entry.grid(row=1, column=1, padx=5, pady=5,)

        ttk.Label(update_dialog, text="Quantity Available:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(update_dialog)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(update_dialog, text="Sport:").grid(row=3, column=0, padx=5, pady=5)
        sport_entry = ttk.Entry(update_dialog)
        sport_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(update_dialog, text="Price:").grid(row=4, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(update_dialog)                   
        price_entry.grid(row=4, column=1, padx=5, pady=5,)

        ttk.Button(update_dialog, text="Update", command=lambda: self.update_equipment(update_dialog, 
                                                                                      name_entry.get(), equipment_entry.get(),
                                                                                      quantity_entry.get(),
                                                                                      sport_entry.get(), float(price_entry.get()))).grid(row=5, column=1, pady=10)

    def update_equipment(self, dialog, equipment_id, name, quantity, sport):
        update_equipment(equipment_id, name, quantity, sport)
        self.refresh_table()
        dialog.destroy()

    def delete_equipment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        equipment_id = self.tree.item(selected_item, 'values')[0]
        delete_equipment(equipment_id)
        self.refresh_table()

# Create the main window
root = tk.Tk()
app = SportsEquipmentGUI(root)

#password and username
app.create_user('anis', '497144', 'admin')

root.mainloop()

# Close the connection when done
conn.close()
