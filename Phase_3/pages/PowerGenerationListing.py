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

# Power Generation Listing
class PowerGenerationListingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        top_section = TopSectionPowerGeneration(self)
        top_section.grid(row=0, column=0,  columnspan=2, sticky="nsew")


        #input_email = self.controller.input_email

        self.refresh()

    def refresh(self):

        # label of  Power Generation listing framework
        label_pg_listing = tk.Label(self, text="Power Generation", font=("Sans-serif", 25))
        label_pg_listing.grid(row=1, column=0, padx=10, pady=10, columnspan = 3,  sticky="W")

        label_description = Label(self, text="You have added these to your household: ", font=("Sans-serif", 15))
        label_description.grid(row=2,  column=0, padx=10, pady=10, columnspan = 3, sticky="W")
        
        input_email = self.controller.input_email 
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3 :
                widget.grid_forget()

        #input_email = 'aacey@golddex.com' # SOS: need to be deleted later , for testing only

        #cursor.execute("SELECT * FROM PowerGenerator where email = %s AND generatorID = %s ", (input_email, generatorID))
        #messagebox.showerror("Please confirm: Deleting %s", cursor.fetchone())

        cursor.execute("SELECT generatorID, generator_type, average_monthly_kilowatt_hours_generated, battery_storage_capacity_kilowatt_hours FROM PowerGenerator where email = %s", (input_email,))
        rows = cursor.fetchall()    

        num_rows = len(rows)
        start_row = 4

        label = tk.Label(self, text="Num", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=0)

        label = tk.Label(self, text="Type", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=1)

        label = tk.Label(self, text="Monthly kWh", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=2)

        label = tk.Label(self, text="Battery kWh", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=3)

        
        for row in range(num_rows):
            generatorID, generator_type, average_monthly_kilowatt_hours_generated, battery_storage_capacity_kilowatt_hours = rows[row]

            num_label = tk.Label(self, text= row + 1, font=("Sans-serif", 15 ))
            num_label.grid(row = start_row + row, column=0)

            generator_type_label = tk.Label(self, text=generator_type, font=("Sans-serif", 15 ))
            generator_type_label.grid(row = start_row + row, column=1)

            monthlykwh_label = tk.Label(self, text=average_monthly_kilowatt_hours_generated , font=("Sans-serif", 15 ))
            monthlykwh_label.grid(row = start_row + row, column=2)

            batterykwh_label = tk.Label(self, text=battery_storage_capacity_kilowatt_hours , font=("Sans-serif", 15 ))
            batterykwh_label.grid(row = start_row + row, column=3)

            delete_label = tk.Label(self, text= "delete", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
            delete_label.grid(row = start_row + row, column=4)
            delete_label.bind("<Button-1>", lambda event: self.power_generating_delete_clicked(input_email, generatorID))

        
        add_more_power_label = tk.Label(self, text="+Add more power", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        add_more_power_label.grid(row=start_row + num_rows, column=4, padx=0, pady=10)
        add_more_power_label.bind("<Button-1>", lambda event: self.controller.display("PowerGenerationPage"))


        # Finish button
        finish_button = tk.Button(
            self, 
            text="Finish", 
            command=self.power_generation_finish_button_clicked,
            bg='blue',
            fg='white',   
            height=2,     
            width=20      
        )
        finish_button.grid(row=start_row + num_rows + 1, column=4, padx=10, pady=10, sticky="W")

        self.power_generator_number = 1
    
    def power_generating_delete_clicked(self, input_email, generatorID):

        try:
            
            #cursor.execute("SELECT * FROM PowerGenerator where email = %s AND generatorID = %s ", (input_email, generatorID))
            #messagebox.showerror("Please confirm: Deleting %s", cursor.fetchone())
            cursor.execute("DELETE FROM PowerGenerator where email = %s AND generatorID = %s ", (input_email, generatorID))
            #cursor.execute("DELETE FROM PowerGenerator where email = 'aacey@golddex.com' AND generatorID = 1 ")
            dbConn.get_conn().commit()
            
            
        except Exception as e:
            # Display error message if an exception occurs during database insertion
            messagebox.showerror("Deletion Error", str(e))
            dbConn.get_conn().rollback()

        self.refresh()
        return 
    
    def power_generation_finish_button_clicked(self):

        # Call power_generation_execute_command and check the return value
        if not power_generation_finish_command(self.controller):
            return

        # Transition to WrappingUpPage
        self.controller.display("WrappingUpPage")

        return


#power generation sql command
def power_generation_finish_command(controller):
          # Perform data validation
    validation_passed = True
    input_email =  controller.input_email
    # input_email = 'aacey@golddex.com' # SOS: need to be deleted later # for testing only

    cursor.execute("SELECT COUNT(email) FROM PublicUtility WHERE email = %s", (input_email,))
    public_utility = cursor.fetchone()

    cursor.execute("SELECT COUNT(email) FROM PowerGenerator WHERE email = %s", (input_email,))
    power_generator = cursor.fetchone()


    #only houshold that has public utility can skip
    if (public_utility is None or len(public_utility) == 0 or public_utility[0] == 0) and (power_generator is None or len(power_generator) == 0 or power_generator[0] == 0):
        messagebox.showerror("Error", "No Public Utility Available. Please Enter Power Generator!")
        validation_passed = False

    return validation_passed
