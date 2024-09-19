# Authors of this Code & File: P2785659, P2724555, P2796362, P2836714, P2839572
'''
Brief Description of what this code does:
This code defines the AddressBookApp class, implementing an 
address book application using the Tkinter library. It allows 
users to add, view, edit, and delete contacts, as well as 
sort and filter them. Contacts are saved to and loaded from 
a file. The code includes several methods for managing contacts, 
UI creation, and handling various user interactions. Authors are 
annotated as P2785659, P2724555, P2796362, P2836714, and P2839572.
'''

import os
import sys
import tkinter as tk
from tkinter import PhotoImage, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
from Contact import Contact
from contact_entry_dialog import ContactEntryDialog

# Class representing the Address Book application 
class AddressBookApp:
    # Constructor to initialise the application with the root window - P2785659 and P2796362
    def __init__(self, root):
        self.root = root
        self.root.title("Address Book App")
        self.contacts = []
        self.load_contacts()  # Load contacts on startup - P2796362
        self.create_contact_management_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.newly_added_contact = None  # Variable to store the most recently added contact

        # Update the contacts listbox after loading contacts - P2796362
        self.update_contacts_listbox()

    # Method to handle the closing of the application - P2785659
    def on_close(self):
        self.save_contacts()
        self.root.destroy()

    # Method to create the UI elements for contact management - P2785659, P2724555 & P2796362
    def create_contact_management_ui(self):
        # Logo Image - P2796362
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            logo_path = os.path.join(sys._MEIPASS, "logo.png")
        else:
            # Running as script
            logo_path = "C:/IMAT1704-Labs/Assignment - Coursework - Address Book Application/Source Code/Address Book Application/logo.png"

        logo_image = PhotoImage(file=logo_path)
        
        # Resizing - P2796362
        resized_logo = logo_image.subsample(8, 8)

        # Label to display the resized logo - P2796362
        logo_label = tk.Label(self.root, image=resized_logo)
        logo_label.image = resized_logo
        logo_label.pack(side="top", anchor="w", padx=10, pady=0)

        # Frame to hold the buttons - P2724555
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, side="left")

        # Buttons for various contact management actions - P2785659 & P2724555
        add_button = tk.Button(button_frame, text="Add Contact", command=self.add_contact_and_display, bg="#4CAF50", fg="white", width=15)
        add_button.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        view_button = tk.Button(button_frame, text="View Contacts", command=self.view_contacts, bg="#2196F3", fg="white", width=15)
        view_button.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        edit_button = tk.Button(button_frame, text="Edit Contact", command=self.edit_contact, bg="#FFC107", fg="black", width=15)
        edit_button.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        delete_button = tk.Button(button_frame, text="Delete Contact", command=self.delete_contact, bg="#F44336", fg="white", width=15)
        delete_button.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        erase_all_button = tk.Button(button_frame, text="Erase All Entries", command=self.erase_all_entries, bg="#607D8B", fg="white", width=15)
        erase_all_button.grid(row=2, column=0, pady=5, padx=5, sticky="w")

        shutdown_button = tk.Button(button_frame, text="Shutdown", command=self.shutdown_application, bg="#795548", fg="white", width=15)
        shutdown_button.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # Create a frame to hold the buttons (Sort Contacts and Filter Contacts) - P2785659
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", fill="both", expand=True)

        # Sort Contacts button on the left - P2796362
        sort_button = tk.Button(button_frame, text="Sort Contacts", command=self.sort_contacts, bg="#FF9800", fg="white", width=15)
        sort_button.pack(side="left", padx=10, pady=5)

        # Filter Contacts button on the right - P2796362
        filter_button = tk.Button(button_frame, text="Filter Contacts", command=self.filter_contacts, bg="#009688", fg="white", width=15)
        filter_button.pack(side="left", padx=(0, 10), pady=5)

        # Listbox to display the contacts - P2785659
        self.contacts_listbox = tk.Listbox(self.root, width=25, height=20)
        self.contacts_listbox.pack(side="left", padx=(10, 0))

        # Create a Scrollbar - P2785659
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.contacts_listbox.yview)
        scrollbar.pack(side="left", fill="y", padx=(0, 10))

        # Attach the Scrollbar to the Listbox - P2785659
        self.contacts_listbox.config(yscrollcommand=scrollbar.set)

    # Method to add a new contact - P2785659
    def add_contact(self):
        contact_info = self.get_contact_info()

        # Check if all contact information is blank - P2785659
        if all(value == '' for value in contact_info):
            messagebox.showwarning("Warning", "Please enter contact information before adding a new contact.")
            return None

        new_contact = Contact(*contact_info)
        self.contacts.append(new_contact)
        self.contacts = sorted(self.contacts, key=lambda x: x.first_name.lower())  # Sort contacts by first name - P2796362
        self.update_contacts_listbox()
        messagebox.showinfo("Success", "Thank you! The new contact has been added successfully.")
        return new_contact

    # Method to get contact information through a dialog - P2785659
    def get_contact_info(self, initial_contact=None):
        dialog = ContactEntryDialog(self.root, "Add Contact", initial_contact=initial_contact)
        if not dialog.result:
            return None

        return dialog.result

    # Method to view contacts - P2785659
    def view_contacts(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            contact_to_view = self.contacts[selected_index[0]]
            self.display_contact_details(contact_to_view, view_mode=True)
        else:
            # If no contact is selected, show a message - P2785659
            messagebox.showinfo("No Contact Selected", "Please select a contact from the list to view.")

    # Method to edit a contact - P2785659 
    def edit_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if not selected_index:
            # If no contact is selected, show a message - P2785659
            messagebox.showinfo("No Contact Selected", "Please select a contact from the list to edit.")
            return

        contact_to_edit = self.contacts[selected_index[0]]

        # Use the ContactEntryDialog for editing - P2785659
        dialog = ContactEntryDialog(self.root, "Edit Contact", initial_contact=contact_to_edit)
        updated_contact_info = dialog.result  # Capture the result before destroying the dialog - P2785659
        if updated_contact_info:
            # Update the contact information with the edited details - P2785659
            contact_to_edit.first_name = updated_contact_info[0]
            contact_to_edit.last_name = updated_contact_info[1]
            contact_to_edit.address = updated_contact_info[2]
            contact_to_edit.mobile_number = updated_contact_info[3]
            contact_to_edit.secondary_number = updated_contact_info[4]
            contact_to_edit.email_address = updated_contact_info[5]
            contact_to_edit.picture_path = updated_contact_info[6]  
            self.update_contacts_listbox()

            # Show confirmation message - P2785659
            self.show_confirmation(self.root, contact_to_edit, edit_mode=True, dialog=dialog)
    
    # Add a new method for showing the confirmation message - P2785659
    def show_confirmation(self, master, contact, edit_mode, dialog):
        if edit_mode:
            messagebox.showinfo("Success", "Contact has been updated successfully.")
        dialog.destroy()

    # Method to delete a contact - P2785659
    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
            if confirmation:
                del self.contacts[selected_index[0]]
                self.update_contacts_listbox()
                messagebox.showinfo("Success", "Contact has been removed successfully.")

    # Method to erase all contact entries - P2785659
    def erase_all_entries(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to erase all entries?")
        if confirmation:
            self.contacts = []
            self.update_contacts_listbox()
            messagebox.showinfo("Success", "All entries erased.")

    # Method to shut down the application - P2785659
    def shutdown_application(self):
        confirmation = messagebox.askokcancel("Shutdown Application", "Are you sure you want to close the application?")
        if confirmation:
            self.save_contacts()
            self.root.destroy()

    # Method to update the contacts listbox with current contact information - P2785659
    def update_contacts_listbox(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, str(contact))

    # Method to save contacts to a file - P2836714 
    def save_contacts(self, file_path="contacts.txt"):
        try:
            with open(file_path, "w") as file:
                for contact in self.contacts:
                    file.write(f"{contact.first_name},{contact.last_name},{contact.address},{contact.mobile_number},{contact.secondary_number},{contact.email_address},{contact.picture_path}\n")
            messagebox.showinfo("Success", "Contacts saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving contacts: {str(e)}")

    # Method to load contacts from a file - P2839572
    def load_contacts(self, file_path="contacts.txt"):
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        data = line.strip().split(",")
                        new_contact = Contact(*data)
                        self.contacts.append(new_contact)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading contacts: {str(e)}")

    # Method to display contact details with various modes (view, edit) - P2785659 & P2724555
    def display_contact_details(self, contact, view_mode=False, edit_mode=False, dialog=None, details_str=None):
        # Create a new window for displaying the picture and contact details - P2724555
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{contact.first_name} {contact.last_name}'s Details")

        if contact.picture_path:
            # Display the picture if available - P2724555
            picture = Image.open(contact.picture_path)
            picture.thumbnail((150, 150))  # Adjust the size as needed
            picture = ImageTk.PhotoImage(picture)

            # Display the picture in a Label - P2724555 
            picture_label = tk.Label(details_window, image=picture, text="Picture:")
            picture_label.image = picture
            picture_label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        # Display other contact details in the same window - P2785659
        labels = ["First Name", "Last Name", "Address", "Mobile Number", "Secondary Number", "Email Address"]

        for row, label in enumerate(labels, start=1):
            attr_value = getattr(contact, label.lower().replace(" ", "_"))
            if attr_value:
                label_widget = tk.Label(details_window, text=f"{label}:", anchor="w")
                label_widget.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                value_widget = tk.Label(details_window, text=attr_value, anchor="w")
                value_widget.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Back Button - P2785659
        back_button = tk.Button(details_window, text="Back", command=details_window.destroy, width=10)
        back_button.grid(row=row + 1, column=0, pady=10)

        # OK Button - P2785659
        ok_button = tk.Button(details_window, text="OK", command=details_window.destroy, width=10)
        ok_button.grid(row=row + 1, column=1, pady=10)
        
        # Destroy the details window when the user closes it - P2785659
        details_window.protocol("WM_DELETE_WINDOW", details_window.destroy)

    # Sorting Contacts - P2796362 & P2836714 
    def sort_contacts(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Contacts")

        # Label for sorting options - P2796362
        sort_label = tk.Label(sort_window, text="Sort Contacts:")
        sort_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        # Buttons for sorting options - P2796362
        sort_first_name_button = tk.Button(sort_window, text="First Name Alphabetically", command=lambda: self.sort_and_display("first_name", sort_window))
        sort_first_name_button.grid(row=1, column=0, pady=5, padx=5)

        sort_surname_button = tk.Button(sort_window, text="Last Name Alphabetically", command=lambda: self.sort_and_display("last_name", sort_window))
        sort_surname_button.grid(row=1, column=2, pady=5, padx=5)

        # Back button for initial sorting options - P2836714
        back_button = tk.Button(sort_window, text="Back", command=sort_window.destroy, width=10)
        back_button.grid(row=3, column=1, pady=5, padx=5, sticky="e")

    # Sort and Display Contacts - P2796362, P2785659 & P2836714 
    def sort_and_display(self, option, parent):
        # Close the main sorting options page - P2796362
        parent.destroy()

        # Sorting Contacts - P2796362
        sort_option_window = tk.Toplevel(self.root)
        sort_option_window.title(f"Sorted by {option.replace('_', ' ').title()} Alphabetically")

        # Label for sorting options - P2785659
        sort_label = tk.Label(sort_option_window, text=f"Sorted by {option.replace('_', ' ').title()} Alphabetically")
        sort_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Sorting the contacts based on the selected option - P2836714
        if option == "first_name":
            sorted_contacts = sorted(self.contacts, key=lambda x: x.first_name.lower())
        elif option == "last_name":
            sorted_contacts = sorted(self.contacts, key=lambda x: x.last_name.lower())
        else:
            # Handle other cases if needed - P2836714
            sorted_contacts = self.contacts

        # Listbox to display the sorted contacts - P2796362
        sorted_listbox = tk.Listbox(sort_option_window, width=25, height=20)
        sorted_listbox.grid(row=1, column=0, columnspan=3, pady=10)

        # Bind double click event to show contact details - P2785659
        sorted_listbox.bind("<Double-Button-1>", lambda event, window=sort_option_window: self.display_contact_details(sorted_contacts[sorted_listbox.curselection()[0]], view_mode=True))

        for contact in sorted_contacts:
            sorted_listbox.insert(tk.END, str(contact))

        # Back button to go back to the main sorting options - P2796362
        back_button = tk.Button(sort_option_window, text="Back", command=lambda: (sort_option_window.destroy(), self.sort_contacts()), width=10)
        back_button.grid(row=2, column=2, pady=5, padx=5)

        # OK button to close the window (only for sorted options) - P2796362
        ok_button = tk.Button(sort_option_window, text="OK", command=sort_option_window.destroy, width=10)
        ok_button.grid(row=2, column=0, pady=5, padx=5)

    # Sort Contacts Page - P2796362 & P2836714
    def sort_contacts_page(self, sort_option_window):
        # Destroy the sort option window - P2796362
        sort_option_window.destroy()

        # Re-open the main sorting options page - P2796362
        self.sort_contacts()

    # Filtering Contacts - P2796362, P2836714 & P2785659
    def filter_contacts(self):
        # Filtering Contacts - P2796362
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Contacts")

        # Set the top attribute to ensure the filter window stays on top - P2785659
        filter_window.attributes('-topmost', True)

        # Label for filter options - P2836714
        filter_label = tk.Label(filter_window, text="Filter Contacts:")
        filter_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Label for filter instructions - P2796362
        filter_instructions_label = tk.Label(filter_window, text="Enter filter conditions (e.g., first name, surname, address, mobile number, secondary number or email address):")
        filter_instructions_label.grid(row=1, column=0, columnspan=2, pady=5, padx=10)

        # Entry for user input - P2836714
        filter_entry = tk.Entry(filter_window)
        filter_entry.grid(row=2, column=0, columnspan=2, pady=5, padx=10)

        # Button to apply filter - P2796362
        apply_filter_button = tk.Button(filter_window, text="Apply Filter", command=lambda: self.apply_filter(filter_entry.get(), filter_window))
        apply_filter_button.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        # Button to go back to filter contacts page - P2796362
        back_button = tk.Button(filter_window, text="Back", command=filter_window.destroy)
        back_button.grid(row=3, column=1, pady=5, padx=5, sticky="w")

    def filter_contacts_page(self, filtered_window):
        # Destroy the filtered window - P2796362
        filtered_window.destroy()

        # Re-open the filter contacts page - P2796362
        self.filter_contacts()

    def apply_filter(self, filter_condition, filter_window):
        if not filter_condition.strip():  # Check if filter_condition is empty - P2785659
            # Display a message to input filter conditions - P2785659
            messagebox.showinfo("Filter Contacts", "Please input filter conditions.")
            return

        filtered_contacts = [
            contact for contact in self.contacts
            if (
                filter_condition.lower() in str(contact.first_name).lower() or
                filter_condition.lower() in str(contact.last_name).lower() or
                filter_condition.lower() in str(contact.address).lower() or
                filter_condition.lower() in str(contact.mobile_number).lower() or
                filter_condition.lower() in str(contact.secondary_number).lower() or
                filter_condition.lower() in str(contact.email_address).lower()
            )
        ]

        # Destroy the filter window before displaying the filtered results - P2796362
        filter_window.destroy()

        # Display filtered contacts in a new window - P2796362
        self.display_filtered_contacts(filtered_contacts)

    def display_filtered_contacts(self, filtered_contacts):
        # Window to show the filtered list - P2836714
        filtered_window = tk.Toplevel(self.root)
        filtered_window.title("Filtered Contacts")

        # Label for filtered contacts - P2836714
        filtered_label = tk.Label(filtered_window, text="Filtered Contacts:")
        filtered_label.pack(pady=10)

        # Listbox to display the filtered contacts - P2836714
        filtered_listbox = tk.Listbox(filtered_window, width=25, height=20)
        filtered_listbox.pack(side="top", pady=5)

        for contact in filtered_contacts:
            filtered_listbox.insert(tk.END, str(contact))

        # Bind double-click event to view_contact_details function - P2836714
        filtered_listbox.bind("<Double-Button-1>", lambda event: self.view_contact_details(filtered_listbox))

        # Add "OK" button to close the window - P2836714
        ok_button = tk.Button(filtered_window, text="OK", command=filtered_window.destroy, width=10)
        ok_button.pack(side="left", pady=10, padx=5)

        # Add "Back" button to go back to filter contacts page - P2836714
        back_button = tk.Button(filtered_window, text="Back", command=lambda: self.filter_contacts_page(filtered_window), width=10)
        back_button.pack(side="left", pady=10, padx=5)

    # Double-Click to View Contact Details - P2785659
    def view_contact_details(self, sorted_listbox):
        # Get the selected index from the sorted listbox
        selected_index = sorted_listbox.curselection()

        # Check if a contact is selected
        if selected_index:
            # Get the contact from the selected index
            contact_to_view = self.contacts[selected_index[0]]

            # Display the contact details in view mode
            self.display_contact_details(contact_to_view, view_mode=True)

    # Add Contact and Dsiplay - P2785659
    def add_contact_and_display(self):
        self.newly_added_contact = self.add_contact()
