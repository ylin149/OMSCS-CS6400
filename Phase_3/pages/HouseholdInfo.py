from tkinter import *
import tkinter as tk
from db_helper import dbConn
from tkinter import messagebox

cursor = dbConn.get_conn().cursor()

class TopSection(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=50,  bg="lightgray")
        self.grid_columnconfigure(0, weight=0)  # Use weight to control the width

        # Create labels for each page
        page_labels = ["Household info", "Appliance","Power generation","Done"]

        # Display the page labels
        for i, label_text in enumerate(page_labels):
            label = tk.Label(self, text=label_text, font=("Sans-serif", 12))
            label.grid(row=0, column=i, padx=10, pady=10, sticky="W")

            # Highlight the current page label
            if i == 0:
                label.config(bg="blue", fg="white")

# household information page layout
class HouseholdInfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        top_section = TopSection(self)
        top_section.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # label of household info page framework
        label_household = tk.Label(self, text="Enter household info", font=("Sans-serif", 25))
        label_household.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        # label of email address
        label_email = tk.Label(self, text="Please enter your email address:", font=("Sans-serif", 15))
        label_email.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        # entry field of email address
        self.input_email = tk.Entry(self, textvariable=tk.StringVar(),width=100)
        self.input_email.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        # label of postal code
        label_postal = tk.Label(self, text="Please enter your five digit postal code:", font=("Sans-serif", 15))
        label_postal.grid(row=4, column=0, padx=10, pady=10, sticky="W")

        # entry field of postal code
        self.input_postal = tk.Entry(self, textvariable=tk.StringVar())
        self.input_postal.grid(row=4, column=0, padx=450, pady=10, sticky="W")

        # label of household details
        label_household_details = tk.Label(self, text="Please enter the following details for your household.", font=("Sans-serif", 15))
        label_household_details.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        # label of home type
        label_home_type = tk.Label(self, text="Home type:", font=("Sans-serif", 15))
        label_home_type.grid(row=6, column=0, padx=10, pady=10, sticky="W")

        # home type dropdown
        self.home_type_lists = [
            "House",
            "Apartment",
            "TownHome",
            "Condominium",
            "Modular home",
            "Tiny House"
        ]

        # dropdown field of home type
        self.home_data_type = tk.StringVar()
        self.home_data_type.set(self.home_type_lists[0])
        input_home_type = tk.OptionMenu(self, self.home_data_type, *self.home_type_lists)
        input_home_type.config(width=14) 
        input_home_type.grid(row=6, column=0, padx=200, pady=10, sticky="W")


        # label of square footage
        label_square_footage = tk.Label(self, text="Square footage:", font=("Sans-serif", 15))
        label_square_footage.grid(row=7, column=0, padx=10, pady=10, sticky="W")

        # entry field of square footage
        self.input_square_footage = tk.Entry(self, textvariable=tk.IntVar())
        self.input_square_footage.grid(row=7, column=0, padx=200, pady=10, sticky="W")


        # label of thermostat heating
        label_heating = tk.Label(self, text="Thermostat setting for heating:", font=("Sans-serif", 15))
        label_heating.grid(row=8, column=0, padx=10, pady=10, sticky="W")

        # entry field of thermostat heating
        self.input_heating = tk.Entry(self, textvariable=tk.IntVar())
        self.input_heating.grid(row=8, column=0, padx=350, pady=10, sticky="W")

        # No heat checkbox
        self.heating_data_type = tk.IntVar()
        checkbox_heating = tk.Checkbutton(self, text='No heat', variable=self.heating_data_type, onvalue=1, offvalue=0)
        checkbox_heating.grid(row=8, column=0, padx=450, pady=10, sticky="W")

        # label of thermostat cooling
        label_cooling = tk.Label(self, text="Thermostat setting for cooling:", font=("Sans-serif", 15))
        label_cooling.grid(row=9, column=0, padx=10, pady=10, sticky="W")

        # entry field of thermostat cooling
        self.input_cooling = tk.Entry(self, textvariable=tk.IntVar())
        self.input_cooling.grid(row=9, column=0, padx=350, pady=10, sticky="W")

        # No cooling checkbox
        self.cooling_data_type = tk.IntVar()
        checkbox_cooling = tk.Checkbutton(self, text='No cooling', variable=self.cooling_data_type, onvalue=1, offvalue=0)
        checkbox_cooling.grid(row=9, column=0, padx=450, pady=10, sticky="W")

        # label of public utilities
        label_public_utilities = tk.Label(self, text="Public utilities:\n(if none, leave unchecked)", font=("Sans-serif", 15), anchor="w")
        label_public_utilities.grid(row=10, column=0, padx=10, pady=10, sticky="W")

        # create listbox of public utilities
        list_box = tk.Listbox(self)
        list_box.grid(row=10, column=0, padx=250, pady=10, sticky="W")

        # electric checkbox
        self.electric_data_type = tk.IntVar()
        checkbox_electric = tk.Checkbutton(list_box, text="Electric", variable=self.electric_data_type, onvalue=1, offvalue=0)
        checkbox_electric.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # gas checkbox
        self.gas_data_type = tk.IntVar()
        checkbox_gas = tk.Checkbutton(list_box, text="Gas", variable=self.gas_data_type, onvalue=1, offvalue=0)
        checkbox_gas.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        # steam checkbox
        self.steam_data_type = tk.IntVar()
        checkbox_steam = tk.Checkbutton(list_box, text="Steam", variable=self.steam_data_type, onvalue=1, offvalue=0)
        checkbox_steam.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        # liquid fuel checkbox
        self.liquid_fuel_data_type = tk.IntVar()
        checkbox_liquid_fuel = tk.Checkbutton(list_box, text="Liquid fuel", variable=self.liquid_fuel_data_type, onvalue=1, offvalue=0)
        checkbox_liquid_fuel.grid(row=3, column=0, padx=10, pady=5, sticky="W")

        # Next button
        next_button = tk.Button(
            self, 
            text="Next", 
            command=self.next_button_clicked,
            bg="blue",
            fg="white",   
            height=2,     
            width=20      
        )
        next_button.grid(row=10, column=0, padx=450, pady=10, sticky="W")

    # When click on next botton, it triggers the following
    def next_button_clicked(self):
        # Retrieve input values from UI elements
        params = {
            "input_email": self.input_email.get(),
            "input_postal": self.input_postal.get(),
            "input_home_type": self.home_data_type.get(),
            "input_square_footage": self.input_square_footage.get(),
            "input_heating": self.input_heating.get(),
            "checkbox_heating": self.heating_data_type.get(),
            "input_cooling": self.input_cooling.get(),
            "checkbox_cooling": self.cooling_data_type.get(),
            "checkbox_electric": self.electric_data_type.get(),
            "checkbox_gas": self.gas_data_type.get(),
            "checkbox_steam": self.steam_data_type.get(),
            "checkbox_liquid_fuel": self.liquid_fuel_data_type.get()
        }

        # Call household_info_execute_command and check the return value
        if not household_info_execute_command(self.controller, params):
            return

        # set email for current session
        self.controller.input_email = self.input_email.get()
    
        # Transition to AddAppliancePage
        self.controller.display("AddAppliancePage")

#Household sql command
def household_info_execute_command(controller, params):
    ##return True #to test later pages
    #data params
    input_email = params["input_email"]
    input_postal = params["input_postal"]
    input_home_type = params["input_home_type"]
    input_square_footage = params["input_square_footage"]
    input_heating = params["input_heating"]
    checkbox_heating = params["checkbox_heating"]
    input_cooling = params["input_cooling"]
    checkbox_cooling = params["checkbox_cooling"]
    checkbox_electric = params["checkbox_electric"]
    checkbox_gas = params["checkbox_gas"]
    checkbox_steam = params["checkbox_steam"]
    checkbox_liquid_fuel = params["checkbox_liquid_fuel"]

    # Perform data validation
    validation_passed = True
    # Empty value
    if not input_email or not input_postal or not input_home_type or not input_square_footage:
        messagebox.showerror("Error", "Please fill in all required fields.")
        validation_passed = False
    # Email
    if "@" not in input_email:
        messagebox.showerror("Error", "Please enter a valid email address")
        validation_passed = False 

    cursor.execute("SELECT COUNT(*) FROM Household WHERE email = %s", (input_email,))
    result = cursor.fetchone()
    if result[0] > 0:
        messagebox.showerror("Error", "Email address already exists")
        validation_passed = False
    # Potal code
    cursor.execute("SELECT EXISTS(SELECT 1 FROM Location WHERE postal_code = %s)", (input_postal,))
    result = cursor.fetchone()
    if result[0] == 0:
        messagebox.showerror("Error", "Postal code does not exist")
        validation_passed = False
    #heating/cooling and square footage
    if (checkbox_heating == 0 and (not input_heating.isdigit() or int(input_heating) <= 0)) or \
       (checkbox_cooling == 0 and (not input_cooling.isdigit() or int(input_cooling) <= 0)):
        messagebox.showerror("Error", "Heating/Cooling thermostat setting must be a positive integer")
        validation_passed = False

    if not input_square_footage.isdigit() or int(input_square_footage) <= 0:
        messagebox.showerror("Error", "Square footage must be a positive integer")
        validation_passed = False

    #Return false when validation failed and stay on the same page
    if not validation_passed:
        return False
    
    # Prepare the SQL query parameters
    household_sql_params = (
        input_email,
        input_square_footage,
        input_home_type,
        input_postal,
        input_heating if checkbox_heating == 0 else None,
        input_cooling if checkbox_cooling == 0 else None
    )

    try:
        # Execute the SQL query
        cursor.execute(
            "INSERT INTO Household (email, square_footage, household_type, postal_code, heating_setting, cooling_setting) \
            VALUES (%s, %s, %s, %s, %s, %s)",
            household_sql_params
        )

        # Check the utility checkboxes and insert email and utility type into publicutility table
        if checkbox_electric == 1:
            cursor.execute(
                "INSERT INTO PublicUtility (email, public_utility) VALUES (%s, %s)",
                (input_email, "electric")
            )

        if checkbox_gas == 1:
            cursor.execute(
                "INSERT INTO PublicUtility (email, public_utility) VALUES (%s, %s)",
                (input_email, "gas")
            )

        if checkbox_steam == 1:
            cursor.execute(
                "INSERT INTO PublicUtility (email, public_utility) VALUES (%s, %s)",
                (input_email, "steam")
            )

        if checkbox_liquid_fuel == 1:
            cursor.execute(
                "INSERT INTO PublicUtility (email, public_utility) VALUES (%s, %s)",
                (input_email, "liquid fuel")
            )

        # Commit the changes to the database
        dbConn.get_conn().commit()
        #cursor.execute("SELECT * FROM PublicUtility where email = %s ", (input_email, ))
        #messagebox.showerror("Added public utility  %s", cursor.fetchone())
        
        return True

    except Exception as e:
        # Display error message if an exception occurs during database insertion
        messagebox.showerror("Error", str(e))
        return False
