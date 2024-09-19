# Authors of this Code & File: P2785659, P2724555, P2796362, P2836714, P2839572
''' 
Brief Description of what this code does:
This code initializes a Tkinter GUI application for an address book, 
created by authors with the provided IDs, and runs the main event loop.
'''

import tkinter as tk
from address_book_app import AddressBookApp

# Main block to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AddressBookApp(root)
    root.mainloop()