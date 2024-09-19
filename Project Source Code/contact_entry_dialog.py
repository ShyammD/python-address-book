# Authors of this Code & File: P2785659, P2724555
'''
# Brief Description of what this code does:
# This code defines a ContactEntryDialog class for entering or editing contact information. 
It includes authorship annotations (P2785659, P2724555). The dialog is created using the 
Tkinter library, providing entry fields for contact details and the option to choose a 
picture file. It handles the initialization, layout, and retrieval of entered information.
'''

import tkinter as tk
from tkinter import simpledialog, filedialog
from Contact import Contact  # Import the Contact class from contact.py

# Dialog class for entering or editing contact information - P2785659
class ContactEntryDialog(tk.simpledialog.Dialog):
    # Initialise the dialog with a master window, a title, and an optional initial contact
    def __init__(self, master, title, initial_contact=None):
        self.initial_contact = initial_contact
        self.picture_path_var = tk.StringVar()  # Initialise picture path variable
        # Call the constructor of the parent class (tk.simpledialog.Dialog)
        super().__init__(master, title)

    # Override the body method to create the content of the dialog - P2785659 & P2724555
    def body(self, master):
        # Dictionary to store Entry widgets for each contact field - P2785659
        self.entries = {}
        # List of contact fields - P2785659
        fields = ["First Name", "Last Name", "Address", "Mobile Number", "Secondary Number", "Email Address"]

        # Create Entry widgets for each field and arrange them in the dialog - P2785659
        for row, field in enumerate(fields):
            tk.Label(master, text=field).grid(row=row, column=0, sticky='w')
            entry = tk.Entry(master)
            entry.grid(row=row, column=1, pady=5, sticky='w')
            self.entries[field] = entry

        # Display the picture in the dialog if available - P2724555
        self.picture_path_var = tk.StringVar()

        picture_label = tk.Label(master, text="Insert a photo:") 
        picture_label.grid(row=len(fields), column=0, sticky='w', pady=5)

        self.picture_entry = tk.Entry(master, textvariable=self.picture_path_var, width=25)
        self.picture_entry.grid(row=len(fields), column=1, pady=5, sticky='w')

        picture_button = tk.Button(master, text="Choose Picture", command=self.choose_picture)
        picture_button.grid(row=len(fields), column=2, pady=5, padx=5, sticky='w')

        # Enable editing of the picture entry after a picture is chosen - P2724555
        self.picture_entry.config(state="normal")

        # If an initial contact is provided, fill the Entry widgets with its information - P2785659
        if self.initial_contact:
            self.entries["First Name"].insert(tk.END, self.initial_contact.first_name)
            self.entries["Last Name"].insert(tk.END, self.initial_contact.last_name)
            self.entries["Address"].insert(tk.END, self.initial_contact.address)
            self.entries["Mobile Number"].insert(tk.END, self.initial_contact.mobile_number)
            self.entries["Secondary Number"].insert(tk.END, self.initial_contact.secondary_number) 
            self.entries["Email Address"].insert(tk.END, self.initial_contact.email_address)
            self.picture_path_var.set(self.initial_contact.picture_path)

        # Return the Entry widget for the first name to set the initial focus - P2785659
        return self.entries["First Name"]

    # Method to choose a picture file - P2724555
    def choose_picture(self):
        picture_path = filedialog.askopenfilename(title="Select Picture", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if picture_path:
            self.picture_path_var.set(picture_path)
            self.picture_entry.delete(0, tk.END)
            self.picture_entry.insert(tk.END, picture_path)
            self.lift()  

    # Override the apply method to retrieve and store the entered information - P2785659
    def apply(self):
        # Get the values from Entry widgets, strip extra whitespaces, and store them in self.result - P2785659
        self.result = [
            self.entries["First Name"].get().strip(),
            self.entries["Last Name"].get().strip(),
            self.entries["Address"].get().strip(),
            self.entries["Mobile Number"].get().strip(),
            self.entries["Secondary Number"].get().strip(), 
            self.entries["Email Address"].get().strip(),
            self.picture_path_var.get().strip()  # Get the picture path
        ]
        # Explicitly destroy the dialog after applying changes - P2785659
        self.destroy()
