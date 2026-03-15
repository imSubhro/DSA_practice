
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk

class StudentRecordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")
        self.root.geometry("900x600")
        
        # Dictionary to store student records
        self.students = {}
        
        # Dictionary to store image references (to prevent garbage collection)
        self.image_references = {}
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Buttons
        tk.Button(btn_frame, text="Add Student", width=15, command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Student", width=15, command=self.update_student).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Student", width=15, command=self.delete_student).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="View Image", width=15, command=self.view_image).grid(row=0, column=3, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview for displaying student records
        self.tree = ttk.Treeview(table_frame, columns=("Roll", "Name", "Age", "Gender", "Address", "Image"), show="headings")
        
        # Set column headings
        self.tree.heading("Roll", text="Roll Number")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Image", text="Image")
        
        # Set column widths
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
        
        # Populate with current data
        for roll, student in self.students.items():
            image_path = student["image"]
            image_name = os.path.basename(image_path) if image_path else "No Image"
            
            self.tree.insert("", "end", values=(roll, student["name"], student["age"], 
                                                student["gender"], student["address"], 
                                                image_name))
    
    def browse_image(self, image_path_var):
        # Open file dialog to select PNG image
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            image_path_var.set(file_path)
    
    def view_image(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to view the image!")
            return
        
        # Get roll number of selected student
        roll = self.tree.item(selected_item[0], "values")[0]
        student = self.students[roll]
        
        if not student["image"]:
            messagebox.showinfo("Info", "No image available for this student.")
            return
        
        # Check if image file exists
        if not os.path.exists(student["image"]):
            messagebox.showerror("Error", f"Image file not found: {student['image']}")
            return
        
        # Display image in a new window
        image_window = tk.Toplevel(self.root)
        image_window.title(f"Image for {student['name']}")
        
        # Load and display the image
        try:
            # Open and resize image
            img = Image.open(student["image"])
            
            # Calculate new dimensions while maintaining aspect ratio
            max_width, max_height = 500, 500
            width, height = img.size
            
            if width > max_width or height > max_height:
                ratio = min(max_width/width, max_height/height)
                width = int(width * ratio)
                height = int(height * ratio)
                img = img.resize((width, height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Keep a reference to prevent garbage collection
            image_window.photo = photo
            
            # Display the image
            label = tk.Label(image_window, image=photo)
            label.pack(padx=10, pady=10)
            
            # Add student info
            info_text = f"Name: {student['name']}\nRoll: {roll}\nAge: {student['age']}\nGender: {student['gender']}"
            info_label = tk.Label(image_window, text=info_text, justify=tk.LEFT)
            info_label.pack(padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")
            image_window.destroy()
    
    def add_student(self):
        # Create a new window for adding student
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("500x400")
        
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
        
        # Gender radio buttons
        tk.Label(add_window, text="Gender:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        gender_frame = tk.Frame(add_window)
        gender_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        gender_var = tk.StringVar(value="Male")  # Default selection
        
        tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side=tk.LEFT, padx=5)
        
        tk.Label(add_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        address_entry = tk.Entry(add_window, width=30)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Image selection
        tk.Label(add_window, text="Image:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        image_frame = tk.Frame(add_window)
        image_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        image_path_var = tk.StringVar()
        image_entry = tk.Entry(image_frame, width=25, textvariable=image_path_var)
        image_entry.pack(side=tk.LEFT)
        
        browse_btn = tk.Button(image_frame, text="Browse", command=lambda: self.browse_image(image_path_var))
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Image preview
        preview_frame = tk.Frame(add_window)
        preview_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        preview_label = tk.Label(preview_frame, text="No image selected")
        preview_label.pack()
        
        # Function to update preview when image path changes
        def update_preview(*args):
            path = image_path_var.get()
            if path and os.path.exists(path):
                try:
                    # Open and resize image for preview
                    img = Image.open(path)
                    
                    # Calculate new dimensions while maintaining aspect ratio
                    max_width, max_height = 150, 150
                    width, height = img.size
                    
                    if width > max_width or height > max_height:
                        ratio = min(max_width/width, max_height/height)
                        width = int(width * ratio)
                        height = int(height * ratio)
                        img = img.resize((width, height), Image.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update preview
                    preview_label.config(image=photo, text="")
                    preview_label.image = photo  # Keep a reference
                except Exception as e:
                    preview_label.config(text=f"Error loading image: {str(e)}", image="")
            else:
                preview_label.config(text="No image selected", image="")
        
        # Bind the update_preview function to the StringVar
        image_path_var.trace_add("write", update_preview)
        
        # Submit button
        def submit():
            roll = roll_entry.get().strip()
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_var.get()
            address = address_entry.get().strip()
            image = image_path_var.get()
            
            # Validate inputs
            if not roll or not name or not age:
                messagebox.showerror("Error", "Roll Number, Name, and Age are required!")
                return
            
            # Check if roll number already exists
            if roll in self.students:
                messagebox.showerror("Error", f"Student with Roll Number {roll} already exists!")
                return
            
            # Check if image path is valid
            if image and not os.path.exists(image):
                messagebox.showerror("Error", f"Image file not found: {image}")
                return
            
            # Add student to dictionary
            self.students[roll] = {
                "name": name,
                "age": age,
                "gender": gender,
                "address": address,
                "image": image
            }
            
            # Refresh table
            self.refresh_table()
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            add_window.destroy()
        
        # Submit button
        tk.Button(add_window, text="Add Student", width=15, command=submit).grid(row=7, column=0, columnspan=2, pady=10)
    
    def update_student(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update!")
            return
        
        # Get roll number of selected student
        roll = self.tree.item(selected_item[0], "values")[0]
        student = self.students[roll]
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("500x400")
        
        # Form fields with current values
        tk.Label(update_window, text="Roll Number:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(update_window, text=roll).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(update_window, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, student["name"])
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(update_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        age_entry = tk.Entry(update_window, width=30)
        age_entry.insert(0, student["age"])
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Gender radio buttons
        tk.Label(update_window, text="Gender:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        gender_frame = tk.Frame(update_window)
        gender_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        gender_var = tk.StringVar(value=student["gender"])  # Set current gender
        
        tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side=tk.LEFT, padx=5)
        
        tk.Label(update_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        address_entry = tk.Entry(update_window, width=30)
        address_entry.insert(0, student["address"])
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Image selection
        tk.Label(update_window, text="Image:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        image_frame = tk.Frame(update_window)
        image_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        image_path_var = tk.StringVar(value=student["image"])
        image_entry = tk.Entry(image_frame, width=25, textvariable=image_path_var)
        image_entry.pack(side=tk.LEFT)
        
        browse_btn = tk.Button(image_frame, text="Browse", command=lambda: self.browse_image(image_path_var))
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Image preview
        preview_frame = tk.Frame(update_window)
        preview_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        preview_label = tk.Label(preview_frame, text="No image selected")
        preview_label.pack()
        
        # Function to update preview when image path changes
        def update_preview(*args):
            path = image_path_var.get()
            if path and os.path.exists(path):
                try:
                    # Open and resize image for preview
                    img = Image.open(path)
                    
                    # Calculate new dimensions while maintaining aspect ratio
                    max_width, max_height = 150, 150
                    width, height = img.size
                    
                    if width > max_width or height > max_height:
                        ratio = min(max_width/width, max_height/height)
                        width = int(width * ratio)
                        height = int(height * ratio)
                        img = img.resize((width, height), Image.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update preview
                    preview_label.config(image=photo, text="")
                    preview_label.image = photo  # Keep a reference
                except Exception as e:
                    preview_label.config(text=f"Error loading image: {str(e)}", image="")
            else:
                preview_label.config(text="No image selected", image="")
        
        # Bind the update_preview function to the StringVar
        image_path_var.trace_add("write", update_preview)
        
        # Trigger the update_preview function once to display current image
        update_preview()
        
        # Submit button
        def submit():
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_var.get()
            address = address_entry.get().strip()
            image = image_path_var.get()
            
            # Validate inputs
            if not name or not age:
                messagebox.showerror("Error", "Name and Age are required!")
                return
            
            # Check if image path is valid
            if image and not os.path.exists(image):
                messagebox.showerror("Error", f"Image file not found: {image}")
                return
            
            # Update student in dictionary
            self.students[roll] = {
                "name": name,
                "age": age,
                "gender": gender,
                "address": address,
                "image": image
            }
            
            # Refresh table
            self.refresh_table()
            messagebox.showinfo("Success", f"Student with Roll Number {roll} updated successfully!")
            update_window.destroy()
        
        # Submit button
        tk.Button(update_window, text="Update Student", width=15, command=submit).grid(row=7, column=0, columnspan=2, pady=10)
    
    def delete_student(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete!")
            return
        
        # Get roll number of selected student
        roll = self.tree.item(selected_item[0], "values")[0]
        student_name = self.students[roll]["name"]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?")
        if confirm:
            # Delete student from dictionary
            del self.students[roll]
            # Refresh table
            self.refresh_table()
            messagebox.showinfo("Success", f"Student {student_name} deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordManager(root)
    root.mainloop()