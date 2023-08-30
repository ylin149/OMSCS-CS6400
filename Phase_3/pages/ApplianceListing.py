from tkinter import *
import tkinter as tk
from db_helper import dbConn
from tkinter import messagebox

cursor = dbConn.get_conn().cursor()

# Add appliance
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
            if i == 1:
                label.config(bg="blue", fg="white")
                
# Appliance listing
class ApplianceListingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # label of  appliance listing framework
        label_appliance_listing = tk.Label(self, text="Appliance Listing", font=("Sans-serif", 25))
        label_appliance_listing.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        label_description = Label(self, text="You have added these to your household: ", font=("Sans-serif", 15))
        label_description.grid(row=2,  column=0, padx=10, pady=10, columnspan = 3, sticky="W")

    def refresh(self):
        input_email = self.controller.input_email
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3 :
                widget.grid_forget()
        cursor.execute("SELECT applianceID, appliance_type, manufacturer_name, model FROM Appliance where email = %s", (input_email,))
        rows = cursor.fetchall()    
        num_rows = len(rows)
        start_row = 4

        label = tk.Label(self, text="Appliance #", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=0)

        label = tk.Label(self, text="Type", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=1)

        label = tk.Label(self, text="Manufacturer", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=2)

        label = tk.Label(self, text="Model", font=("Sans-serif", 15, "bold"))
        label.grid(row=3, column=3)


        for row in range(num_rows):
            applianceID, appliance_type, manufacturer_name, model_name = rows[row]
            if model_name == "NULL":
                model_name = ""
            num_label = tk.Label(self, text= row + 1, font=("Sans-serif", 15 ))
            num_label.grid(row = start_row + row, column=0)

            type_label = tk.Label(self, text=appliance_type, font=("Sans-serif", 15 ))
            type_label.grid(row = start_row + row, column=1)

            manufacturer_label = tk.Label(self, text= manufacturer_name, font=("Sans-serif", 15 ))
            manufacturer_label.grid(row = start_row + row, column=2)

            model_label = tk.Label(self, text=model_name , font=("Sans-serif", 15 ))
            model_label.grid(row = start_row + row, column=3)

            delete_label = tk.Label(self, text= "delete", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
            delete_label.grid(row = start_row + row, column=4)
            delete_label.bind("<Button-1>", lambda event: self.appliance_delete_clicked(input_email, applianceID))

        add_more_appliance_label = tk.Label(self, text="+Add more appliance", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        add_more_appliance_label.grid(row=start_row + num_rows+1, column=4, padx=0, pady=10)
        add_more_appliance_label.bind("<Button-1>", lambda event: self.add_more_appliance())
        
        # Finish button
        finish_button = tk.Button(
            self, 
            text="Next", 
            command=self.appliance_finish_button_clicked,
            bg='blue',
            fg='white',   
            height=2,     
            width=20      
        )
        finish_button.grid(row=start_row + num_rows + 2, column=4, padx=10, pady=10, sticky="W")

    def add_more_appliance(self):
        # self.controller.refresh("AddAppliancePage")
        self.controller.display("AddAppliancePage")

    def appliance_finish_button_clicked(self):

        # Call power_generation_execute_command and check the return value
        if not self.appliance_finish_command():
            return

        # Transition to WrappingUpPage
        self.controller.refresh("PowerGenerationPage")
        self.controller.display("PowerGenerationPage")
        self.controller.appliance_number = 1
        return

    def appliance_delete_clicked(self, input_email, applianceID):
        try:            
            cursor.execute("SELECT * FROM AirConditioner where email = %s AND applianceID = %s ", (input_email, applianceID))
            AC = cursor.fetchone()
            if AC:
                cursor.execute("DELETE FROM AirConditioner where email = %s AND applianceID = %s ", (input_email, applianceID))
            cursor.execute("SELECT * FROM Heater where email = %s AND applianceID = %s ", (input_email, applianceID))

            HT = cursor.fetchone()
            if HT:
                cursor.execute("DELETE FROM Heater where email = %s AND applianceID = %s ", (input_email, applianceID))    

            cursor.execute("SELECT * FROM HeatPump where email = %s AND applianceID = %s ", (input_email, applianceID))
            HP = cursor.fetchone()
            if HP:
                cursor.execute("DELETE FROM HeatPump where email = %s AND applianceID = %s ", (input_email, applianceID))    

            cursor.execute("SELECT * FROM AirHandler where email = %s AND applianceID = %s ", (input_email, applianceID))
            AH = cursor.fetchone()
            if AH:
                cursor.execute("DELETE FROM AirHandler where email = %s AND applianceID = %s ", (input_email, applianceID))     

            cursor.execute("SELECT * FROM WaterHeater where email = %s AND applianceID = %s ", (input_email, applianceID))
            WH = cursor.fetchone()
            if WH:
                cursor.execute("DELETE FROM WaterHeater where email = %s AND applianceID = %s ", (input_email, applianceID))     

            cursor.execute("DELETE FROM Appliance where email = %s AND applianceID = %s ", (input_email, applianceID))
            dbConn.get_conn().commit()
            
        except Exception as e:
            # Display error message if an exception occurs during database insertion
            messagebox.showerror("Deletion Error", str(e))
            dbConn.get_conn().rollback()

        self.refresh()
        return 
    
    def appliance_finish_command(self):
            # Perform data validation
        validation_passed = True
        input_email =  self.controller.input_email
        # input_email = 'aacey@golddex.com' # SOS: need to be deleted later # for testing only

        cursor.execute("SELECT COUNT(email) FROM Appliance WHERE email = %s", (input_email,))
        appliance = cursor.fetchone()


        #only houshold that has public utility can skip
        if  appliance is None or len(appliance) == 0 or appliance[0] == 0:
            messagebox.showerror("Error", "Please add at least one appliance!")
            validation_passed = False
        return validation_passed