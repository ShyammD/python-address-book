# Authors of this Code & File: P2785659, P2724555
'''
Brief Description of what this code does:
This code defines a Contact class representing a contact with specific 
attributes, and it includes authorship annotations (P2785659, P2724555). 
The class uses slots for attribute restriction, initializes instances 
with provided information, and defines a string representation.
'''

# Class representing a contact with specific attributes - P2785659 & P2724555
class Contact:
    # Define slots to restrict attribute creation to these specific attributes - P2785659 & P2724555
    __slots__ = ("first_name", "last_name", "address", "mobile_number", "secondary_number", "email_address", "picture_path")

    # Initialise a Contact instance with provided information - P2785659 & P2724555
    def __init__(self, first_name, last_name, address, mobile_number, secondary_number, email_address, picture_path=""):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.mobile_number = mobile_number
        self.secondary_number = secondary_number
        self.email_address = email_address
        self.picture_path = picture_path

    # Define a string representation for the Contact instance - P2785659 & P2724555
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
