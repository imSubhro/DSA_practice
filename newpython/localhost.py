

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class StudentRecordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")
        self.root.geometry("800x500")
        
        # Database connection
        self.conn = None
        self.connect_to_database()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load data from database
        self.refresh_table()
        
    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # default XAMPP username
                password="",  # default XAMPP password is empty
                database="student_management"
            )
            if self.conn.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
    
    def create_widgets(self):
        # Frame for buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Buttons
        tk.Button(btn_frame, text="Add Student", width=15, command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Student", width=15, command=self.update_student).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Student", width=15, command=self.delete_student).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh", width=15, command=self.refresh_table).grid(row=0, column=3, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview for displaying student records
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Roll", "Name", "Age", "Gender", "Address", "Image"), show="headings")
        
        # Set column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Roll", text="Roll Number")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Image", text="Image")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Roll", width=80)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=50)
        self.tree.column("Gender", width=80)
        self.tree.column("Address", width=200)
        self.tree.column("Image", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Check database connection
        if not self.conn or not self.conn.is_connected():
            self.connect_to_database()
            if not self.conn or not self.conn.is_connected():
                return
        
        # Fetch and display data from database
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert("", "end", values=row)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")
    
    def add_student(self):
        # Create a new window for adding student
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("400x300")
        
        # Form fields
        tk.Label(add_window, text="Roll Number:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        roll_entry = tk.Entry(add_window, width=30)
        roll_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(add_window, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        age_entry = tk.Entry(add_window, width=30)
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="Gender:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        gender_entry = tk.Entry(add_window, width=30)
        gender_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        address_entry = tk.Entry(add_window, width=30)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="Image:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        image_entry = tk.Entry(add_window, width=30)
        image_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Submit button
        def submit():
            roll = roll_entry.get().strip()
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_entry.get().strip()
            address = address_entry.get().strip()
            image = image_entry.get().strip()
            
            # Validate inputs
            if not roll or not name:
                messagebox.showerror("Error", "Roll Number and Name are required!")
                return
            
            # Check database connection
            if not self.conn or not self.conn.is_connected():
                self.connect_to_database()
                if not self.conn or not self.conn.is_connected():
                    return
            
            # Add student to database
            try:
                cursor = self.conn.cursor()
                
                # Check if roll number exists
                cursor.execute("SELECT * FROM students WHERE roll_number = %s", (roll,))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"Student with Roll Number {roll} already exists!")
                    cursor.close()
                    return
                
                # Insert new student
                query = """
                INSERT INTO students (roll_number, name, age, gender, address, image) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (roll, name, age, gender, address, image))
                self.conn.commit()
                cursor.close()
                
                # Refresh table
                self.refresh_table()
                messagebox.showinfo("Success", f"Student {name} added successfully!")
                add_window.destroy()
            except Error as e:
                messagebox.showerror("Database Error", f"Error adding student: {e}")
        
        # Submit button
        tk.Button(add_window, text="Add Student", width=15, command=submit).grid(row=6, column=0, columnspan=2, pady=10)
    
    def update_student(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update!")
            return
        
        # Get values of selected student
        values = self.tree.item(selected_item[0], "values")
        student_id = values[0]
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("400x300")
        
        # Form fields with current values
        tk.Label(update_window, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(update_window, text=values[0]).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(update_window, text="Roll Number:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        roll_entry = tk.Entry(update_window, width=30)
        roll_entry.insert(0, values[1])
        roll_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, values[2])
        name_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Age:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        age_entry = tk.Entry(update_window, width=30)
        age_entry.insert(0, values[3])
        age_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Gender:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        gender_entry = tk.Entry(update_window, width=30)
        gender_entry.insert(0, values[4])
        gender_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        address_entry = tk.Entry(update_window, width=30)
        address_entry.insert(0, values[5])
        address_entry.grid(row=5, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Image:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        image_entry = tk.Entry(update_window, width=30)
        image_entry.insert(0, values[6] if values[6] else "")
        image_entry.grid(row=6, column=1, padx=10, pady=5)
        
        # Submit button
        def submit():
            roll = roll_entry.get().strip()
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_entry.get().strip()
            address = address_entry.get().strip()
            image = image_entry.get().strip()
            
            # Validate inputs
            if not roll or not name:
                messagebox.showerror("Error", "Roll Number and Name are required!")
                return
            
            # Check database connection
            if not self.conn or not self.conn.is_connected():
                self.connect_to_database()
                if not self.conn or not self.conn.is_connected():
                    return
            
            # Update student in database
            try:
                cursor = self.conn.cursor()
                
                # Check if roll number exists for a different student
                cursor.execute("SELECT id FROM students WHERE roll_number = %s AND id != %s", (roll, student_id))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"Another student with Roll Number {roll} already exists!")
                    cursor.close()
                    return
                
                # Update student
                query = """
                UPDATE students 
                SET roll_number = %s, name = %s, age = %s, gender = %s, address = %s, image = %s 
                WHERE id = %s
                """
                cursor.execute(query, (roll, name, age, gender, address, image, student_id))
                self.conn.commit()
                cursor.close()
                
                # Refresh table
                self.refresh_table()
                messagebox.showinfo("Success", f"Student information updated successfully!")
                update_window.destroy()
            except Error as e:
                messagebox.showerror("Database Error", f"Error updating student: {e}")
        
        # Submit button
        tk.Button(update_window, text="Update Student", width=15, command=submit).grid(row=7, column=0, columnspan=2, pady=10)
    
    def delete_student(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete!")
            return
        
        # Get student id and name
        values = self.tree.item(selected_item[0], "values")
        student_id = values[0]
        student_name = values[2]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?")
        if confirm:
            # Check database connection
            if not self.conn or not self.conn.is_connected():
                self.connect_to_database()
                if not self.conn or not self.conn.is_connected():
                    return
            
            # Delete student from database
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                self.conn.commit()
                cursor.close()
                
                # Refresh table
                self.refresh_table()
                messagebox.showinfo("Success", f"Student {student_name} deleted successfully!")
            except Error as e:
                messagebox.showerror("Database Error", f"Error deleting student: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordManager(root)
    root.mainloop()