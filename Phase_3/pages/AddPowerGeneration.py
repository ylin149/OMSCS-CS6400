from tkinter import *
import tkinter as tk
from db_helper import dbConn
from tkinter import messagebox

cursor = dbConn.get_conn().cursor()

class TopSectionPowerGeneration(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=50,  bg="lightgray")
        self.grid_columnconfigure(0, weight=0)  # Use weight to control the width

        # Create labels for each page
        page_labels = ["Household info", "Appliance","Power generation","Done"]

        # Display the page labels
        for i, label_text in enumerate(page_labels):
            label = tk.Label(self, text=label_text, font=("Sans-serif", 12))
            label.grid(row=0, column=i, padx=10, pady=10, sticky="W")

            # Highliht the current page label
            if i == 2:
                label.config(bg="blue", fg="white")

# power generation information page window frame
class PowerGenerationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        top_section = TopSectionPowerGeneration(self)
        top_section.grid(row=0, column=0, columnspan=2, sticky="nsew")
    
        self.refresh()
        


    def refresh(self):

        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2 :
                widget.grid_forget()

         # label of power generation page framework
        label_power_generation = tk.Label(self, text="Add power generation", font=("Sans-serif", 25))
        label_power_generation.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        # label of power generation type
        label_power_generation_type = tk.Label(self, text="Type:", font=("Sans-serif", 15))
        label_power_generation_type.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        # power generation type dropdown
        self.power_generation_type_lists = [
            "solar",
            "wind-turbine"
        ]

        # dropdown field of power generation type
        self.power_generation_data_type = tk.StringVar()
        self.power_generation_data_type.set(self.power_generation_type_lists[0])
        input_power_generation_type = tk.OptionMenu(self, self.power_generation_data_type, *self.power_generation_type_lists)
        input_power_generation_type.grid(row=2, column=0, padx=400, pady=10, sticky="W")

        # label of monthly kwh
        label_monthly_kwh = tk.Label(self, text="Monthly kWh (int):", font=("Sans-serif", 15))
        label_monthly_kwh.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        # entry field of monthly kwh
        self.input_monthly_kwh = tk.Entry(self, textvariable=tk.IntVar(value=""))
        self.input_monthly_kwh.grid(row=3, column=0, padx=400, pady=10, sticky="W")


        # label of storage kwh
        label_storage_kwh = tk.Label(self, text="Storage kWh (int, optional):", font=("Sans-serif", 15))
        label_storage_kwh.grid(row=4, column=0, padx=10, pady=10, sticky="W")

        # entry field of monthly kwh
        self.input_storage_kwh = tk.Entry(self, textvariable=tk.IntVar(value=""))
        self.input_storage_kwh.grid(row=4, column=0, padx=400, pady=10, sticky="W")

        # Next button
        next_button = tk.Button(
            self, 
            text="Next", 
            command=self.power_generation_next_button_clicked,
            bg='blue',
            fg='white',   
            height=2,     
            width=20      
        )
        next_button.grid(row=6, column=0, padx=400, pady=10, sticky="W")

        self.input_email = self.controller.input_email
        #self.input_email =  'aacey@golddex.com' # SOS: need to be deleted later # for testing only
        
        # Call power_generation_skip_command and check the return value
        if power_generation_skip_command( self.controller.input_email):
            self.controller.refresh("PowerGenerationListingPage")
            # Skip button
            skip_button = tk.Button(self, text="Skip", bg='blue', fg='white',   height=2, width=20)
            skip_button.bind("<Button-1>", lambda event: self.controller.display("PowerGenerationListingPage"))
            skip_button.grid(row=5, column=0, padx=400, pady=10, sticky="W")
            
            

    # When click on next botton, it triggers the following
    def power_generation_next_button_clicked(self):
        # Retrieve input values from UI elements
        params = {
            "input_email": self.controller.input_email,
            "power_generation_data_type": self.power_generation_data_type.get(),
            "input_monthly_kwh": self.input_monthly_kwh.get(),
            "input_storage_kwh": self.input_storage_kwh.get(),
            "generatorID": self.controller.power_generator_number
        }

        # Call power_generation_execute_command and check the return value
        if not power_generation_execute_command(params):
            return

        # Transition to PowerGenerationListingPage

        self.input_monthly_kwh.delete(0, END)
        self.input_storage_kwh.delete(0, END)
        self.controller.increase_power_generator_number()
        self.controller.refresh("PowerGenerationListingPage")
        self.controller.display("PowerGenerationListingPage")
        
        return

# power generation skip command
def power_generation_skip_command( input_email):
        
    # Perform data validation
    validation_passed = True
    
    cursor.execute("SELECT COUNT(email) FROM PublicUtility WHERE email = %s", (input_email,))
    result = cursor.fetchone()

    #only houshold that has public utility can skip
    if result is None or  len(result) == 0 or result[0] == 0:
        #messagebox.showerror("Error", "No Public Utility Available. Please Enter Power Generator!")
        validation_passed = False
    
    return validation_passed
    

#power generation sql command
def power_generation_execute_command( params):
        #data params
    input_email = params["input_email"]
    power_generation_data_type = params["power_generation_data_type"]
    input_monthly_kwh = params["input_monthly_kwh"]
    input_storage_kwh = params["input_storage_kwh"]
    generatorID = params["generatorID"]

    # Perform data validation
    validation_passed = True
    # Empty value
    if not power_generation_data_type or not input_monthly_kwh:
        messagebox.showerror("Error", "Please fill in all required fields.")
        validation_passed = False
    
    if not  input_monthly_kwh.isdigit() or  int(input_monthly_kwh) <= 0:
        messagebox.showerror("Error", "Please enter vailid monthly kwh.")
        validation_passed = False

    if input_storage_kwh and (not  input_storage_kwh.isdigit() or  int(input_storage_kwh) <= 0):
        messagebox.showerror("Error", "Please enter vailid storage kwh.")
        validation_passed = False
    

    if not validation_passed:
        return False
    
    # Prepare the SQL query parameters
    power_generation_sql_params = (
        input_email,
        generatorID,
        power_generation_data_type,
        input_monthly_kwh,
        input_storage_kwh
    )

    try:
        if input_storage_kwh and (not input_storage_kwh == 0) :
        # Execute the SQL query
            cursor.execute(
                "INSERT INTO PowerGenerator (email, generatorID, generator_type, average_monthly_kilowatt_hours_generated, battery_storage_capacity_kilowatt_hours) \
                VALUES (%s, %s, %s, %s, %s)",
                power_generation_sql_params
            )
        else:
            cursor.execute(
            "INSERT INTO PowerGenerator (email, generatorID, generator_type, average_monthly_kilowatt_hours_generated) \
            VALUES (%s, %s, %s, %s)",
            power_generation_sql_params[:-1]
            )
        # Commit the changes to the database
        dbConn.get_conn().commit()
        return True

    except Exception as e:
        # Display error message if an exception occurs during database insertion
        messagebox.showerror("Error", str(e))
        return False

    