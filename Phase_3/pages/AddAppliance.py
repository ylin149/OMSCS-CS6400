from tkinter import *
from tkinter import ttk,messagebox
import tkinter as tk
from db_helper import dbConn

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

class AddAppliancePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        top_section = TopSection(self)
        top_section.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # label of add appliance framework
        label_appliance = tk.Label(self, text="Add appliance", font=("Sans-serif", 25))
        label_appliance.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.refresh()

    def selection_changed(self, event):
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) >= 5 and int(widget.grid_info()["row"]) < 11:
                widget.grid_forget()

        if self.input_appliance_type.get() == "air_handler":
            # label of public utilities
            label_heating_cooling = tk.Label(self, text="heating/cooling methods:\n(select at least one)", font=("Sans-serif", 15), anchor="w")
            label_heating_cooling.grid(row=5, column=0, padx=10, pady=10, sticky="W")

            # create listbox of public utilities
            list_box = tk.Listbox(self)
            list_box.grid(row=5, column=0, padx=500, pady=10, sticky="W")

            # electric checkbox
            self.air_conditioner = tk.IntVar()
            checkbox_ac = tk.Checkbutton(list_box, text="Air conditioner", variable=self.air_conditioner, onvalue=1, offvalue=0)
            checkbox_ac.grid(row=0, column=0, padx=10, pady=5, sticky="W")

            # gas checkbox
            self.heater = tk.IntVar()
            checkbox_ht = tk.Checkbutton(list_box, text="Heater", variable=self.heater, onvalue=1, offvalue=0)
            checkbox_ht.grid(row=1, column=0, padx=10, pady=5, sticky="W")

            # steam checkbox
            self.heat_pump = tk.IntVar()
            checkbox_hp = tk.Checkbutton(list_box, text="Heat pump", variable=self.heat_pump, onvalue=1, offvalue=0)
            checkbox_hp.grid(row=2, column=0, padx=10, pady=5, sticky="W")

            # entering RPM
            RPM = tk.Label(self, text="RPM:", font=("Sans-serif", 15))
            RPM.grid(row=6, column=0, padx=10, pady=10, sticky="W")
            self.input_RPM = tk.Entry(self, textvariable=tk.IntVar())
            self.input_RPM.grid(row=6, column=0, padx=500, pady=10, sticky="W")

            # TODO: required for air conditioner
            EER = tk.Label(self, text="Energy efficiency ratio (EER):", font=("Sans-serif", 15))
            EER.grid(row=7, column=0, padx=10, pady=10, sticky="W")
            self.input_EER = tk.Entry(self, textvariable=tk.DoubleVar())
            self.input_EER.grid(row=7, column=0, padx=500, pady=10, sticky="W")

            # TODO: required for heater
            self.energy_source_list_ah = [
                "Electric",
                "Gas",
                "Thermosolar"
            ]

            # dropdown field of power generation type
            energy_source_label_ah = tk.Label(self, text = "Energy Source", font=("Sans-serif", 15))
            energy_source_label_ah.grid(row=8, column=0, padx=10, pady=10, sticky="W")
            self.input_energy_source_ah = tk.StringVar()
            energy_source_ah = tk.OptionMenu(self, self.input_energy_source_ah, *self.energy_source_list_ah)
            energy_source_ah.grid(row=8, column=0, padx=500, pady=10, sticky="W")

            # required for heat pump
            SEER = tk.Label(self, text="Seasonal energy efficiency rating (SEER):", font=("Sans-serif", 15))
            SEER.grid(row=9, column=0, padx=10, pady=10, sticky="W")
            self.input_SEER = tk.Entry(self, textvariable=tk.DoubleVar())
            self.input_SEER.grid(row=9, column=0, padx=500, pady=10, sticky="W")

            HSPF = tk.Label(self, text="Heating seasonal performance factor (HSPF):", font=("Sans-serif", 15))
            HSPF.grid(row=10, column=0, padx=10, pady=10, sticky="W")
            self.input_HSPF = tk.Entry(self, textvariable=tk.DoubleVar())
            self.input_HSPF.grid(row=10, column=0, padx=500, pady=10, sticky="W")

        elif self.input_appliance_type.get() == "water_heater":
            # entering tank size in gallons
            # TODO: check the decimal?
            TankSize = tk.Label(self, text="Tank size in gallons:", font=("Sans-serif", 15))
            TankSize.grid(row=5, column=0, padx=10, pady=10, sticky="W")
            self.input_tank_size = tk.Entry(self, textvariable=tk.DoubleVar())
            self.input_tank_size.grid(row=5, column=0, padx=500, pady=10, sticky="W")

            # TODO: optional
            CurTemp = tk.Label(self, text="Current temperature setting (optional):", font=("Sans-serif", 15))
            CurTemp.grid(row=6, column=0, padx=10, pady=10, sticky="W")
            self.input_cur_temp = tk.Entry(self, textvariable=tk.IntVar(value=""))
            self.input_cur_temp.grid(row=6, column=0, padx=500, pady=10, sticky="W")

            self.energy_source_list_wh = [
                "electric",
                "gas",
                "fuel oil",
                "heat pump"
            ]
            energy_source_label_wh = tk.Label(self, text = "Energy source", font=("Sans-serif", 15))
            energy_source_label_wh.grid(row=7, column=0, padx=10, pady=10, sticky="W")
            # dropdown field of power generation type
            self.input_energy_source_wh = tk.StringVar()
            energy_source_wh = tk.OptionMenu(self, self.input_energy_source_wh, *self.energy_source_list_wh)
            energy_source_wh.grid(row=7, column=0, padx=500, pady=10, sticky="W")

        next_button = tk.Button(
            self, 
            text="Next", 
            command=self.add_appliance_next_button_clicked,
            bg='blue',
            fg='white',   
            height=2,     
            width=20      
        )
        next_button.grid(row=11, column=0, padx=10, pady=10, sticky="W")

    def refresh(self):
        # variables saveds
        self.manufacturer_name_list = None
        self.input_manu_name = None
        self.input_manu_combobox = None
        self.other_manu_name = None
        self.new_manu_name = False

        self.input_model_name = None
        self.input_appliance_type = None
        self.intput_BTUs = None

        ## for air handler
        self.input_RPM = None

        # for ac
        self.air_conditioner = None
        self.input_EER = None

        # for heater
        self.heater = None
        self.input_energy_source_ah = None

        # for heat pump 
        self.heat_pump = None
        self.input_SEER = None
        self.input_HSPF = None

        self.input_tank_size = None
        self.input_cur_temp = None
        self.input_energy_source_wh = None

        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2:
                widget.grid_forget()
                
        sql1 = '''
        SELECT manufacturer_name FROM Manufacturer
        '''
        cursor.execute(sql1)
        rows = cursor.fetchall()    

        self.manufacturer_name_list = []
        for row in rows:
            self.manufacturer_name_list.append(row[0])
        self.manufacturer_name_list.append("Others: add your own")

        def filter_list(event):
            filter_word = self.input_manu_combobox.get().lower() 
            if filter_word == '':
                self.input_manu_combobox['values'] = self.manufacturer_name_list
            else:   
                self.input_manu_combobox['values'] = [x for x in self.manufacturer_name_list if filter_word in x.lower()]

        def update_list(event):
            if self.input_manu_combobox.get() == "Others: add your own":
                self.other_manu_name = tk.Entry(self, textvariable=tk.StringVar())
                self.other_manu_name.grid(row=2, column=0, padx=650, pady=10, sticky="W")
                self.input_manu_name = self.other_manu_name
                self.new_manu_name = True
            else:
                if self.other_manu_name:
                    self.other_manu_name.grid_forget()
                self.input_manu_name = self.input_manu_combobox
                self.new_manu_name = False
                

        # entering manufacturer name
        manufacturer_name = tk.Label(self, text="Search manufacturer name: \
                                     \n 1.enter lower case and click the scroll-down \
                                     \n 2.if you want to add new names, please select \
                                     \n   'Others: add your own' and type in the additional box \
                                     \n   please don not directly type in the search box", 
                                     font=("Sans-serif", 15), justify="left")
        manufacturer_name.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.input_manu_combobox = ttk.Combobox(self, values=self.manufacturer_name_list)
        self.input_manu_combobox.grid(row=2, column=0, padx=500, pady=10, sticky="W")
        self.input_manu_combobox.bind('<KeyRelease>', filter_list)
        self.input_manu_combobox.bind('<<ComboboxSelected>>', update_list)

        # entering model name
        model_name = tk.Label(self, text="Model name (optional):", font=("Sans-serif", 15))
        model_name.grid(row=3, column=0, padx=10, pady=10, sticky="W")
        self.input_model_name = tk.Entry(self, textvariable=tk.StringVar())
        self.input_model_name.grid(row=3, column=0, padx=500, pady=10, sticky="W")
        
        # entering BTU
        BTUs = tk.Label(self, text="BTU rating:", font=("Sans-serif", 15))
        BTUs.grid(row=4, column=0, padx=10, pady=10, sticky="W")
        self.intput_BTUs = tk.Entry(self, textvariable=tk.IntVar())
        self.intput_BTUs.grid(row=4, column=0, padx=500, pady=10, sticky="W")

        self.input_appliance_type = ttk.Combobox(self, values=["air_handler", "water_heater"])
        self.input_appliance_type.grid(row=1, column=0, padx=500, pady=10, sticky="W")
        self.input_appliance_type.bind("<<ComboboxSelected>>", self.selection_changed)
        
    # When click on next botton, it triggers the following
    def add_appliance_next_button_clicked(self):
        # Call power_generation_execute_command and check the return value
        if not self.appliance_check_validity():
            return
        input_email = self.controller.input_email
        input_manu_name = str(self.input_manu_name.get())
        input_model_name = self.input_model_name.get()
        if not input_model_name:
            input_model_name = "NULL"

        input_appliance_type = self.input_appliance_type.get()
        input_applianceID = self.controller.appliance_number
        intput_BTUs = self.intput_BTUs.get()

        try:
            # we only insert the new manu name once
            if self.new_manu_name:
                cursor.execute(
                "INSERT INTO Manufacturer (manufacturer_name) VALUES (%s)",
                (input_manu_name,)
                )
                self.new_manu_name = False
            print("(input_email, input_applianceID, input_appliance_type, input_manu_name, input_model_name, intput_BTUs)",(input_email, input_applianceID, input_appliance_type, input_manu_name, input_model_name, intput_BTUs))

            cursor.execute(
                "INSERT INTO Appliance (email, applianceID, appliance_type, manufacturer_name, model, BTU) \
                VALUES (%s, %s, %s, %s, %s, %s)",
                (input_email, input_applianceID, input_appliance_type, input_manu_name, input_model_name, intput_BTUs)
            )
            if input_appliance_type == "air_handler":
                input_RPM = self.input_RPM.get()
                cursor.execute(
                "INSERT INTO AirHandler (email, applianceID, RPM) \
                VALUES (%s, %s, %s)",
                (input_email, input_applianceID,  input_RPM)
                )

                air_conditioner = self.air_conditioner.get() 
                heater = self.heater.get()
                heat_pump = self.heat_pump.get()

                if air_conditioner == 1:
                    input_EER = round(float(self.input_EER.get()),1)
                    cursor.execute(
                    "INSERT INTO AirConditioner (email, applianceID, EER) \
                    VALUES (%s, %s, %s)",
                    (input_email, input_applianceID, str(input_EER))
                    )
                if heater  == 1:
                    input_energy_source_ah = self.input_energy_source_ah.get()
                    cursor.execute(
                    "INSERT INTO Heater (email, applianceID, energy_source) \
                    VALUES (%s, %s, %s)",
                    (input_email, input_applianceID, input_energy_source_ah)
                    )                    
                if heat_pump == 1:
                    input_SEER = round(float(self.input_SEER.get()),1)
                    input_HSPF = round(float(self.input_HSPF.get()),1)
                    cursor.execute(
                    "INSERT INTO HeatPump (email, applianceID, SEER, HSPF) \
                    VALUES (%s, %s, %s, %s)",
                    (input_email, input_applianceID, str(input_SEER), str(input_HSPF))
                    )
            else:
                input_tank_size = round(float(self.input_tank_size.get()),1)
                input_cur_temp = self.input_cur_temp.get() # this is optional
                input_energy_source_wh = self.input_energy_source_wh.get()

                if input_cur_temp:
                    cursor.execute(
                    "INSERT INTO WaterHeater (email, applianceID, tank_size, current_temperature, energy_source) \
                    VALUES (%s, %s, %s, %s, %s)",
                    (input_email, input_applianceID, str(input_tank_size), input_cur_temp, input_energy_source_wh)
                    )
                else:
                    cursor.execute(
                    "INSERT INTO WaterHeater (email, applianceID, tank_size, energy_source) \
                    VALUES (%s, %s, %s, %s)",
                    (input_email, input_applianceID, str(input_tank_size), input_energy_source_wh)
                    )
            # Commit the changes to the database
            dbConn.get_conn().commit()

        except Exception as e:
            # Display error message if an exception occurs during database insertion
            messagebox.showerror("Error", str(e))
            return
            
        # Transition to AddAppliancePage
        self.controller.increase_appliance_number()
        self.controller.display("ApplianceListingPage")
        self.controller.refresh("ApplianceListingPage")
        self.refresh()
        return
    
    def appliance_check_validity(self):
        is_valid = True
        if not self.input_manu_name:
            messagebox.showerror("Error", "Must select in Manufacturer name From the Populated List")
            is_valid = False
        else:
            input_manu_name = self.input_manu_name.get()
            if not input_manu_name:
                messagebox.showerror("Error", "Must select in Manufacturer name From the Populated List")
                is_valid = False
            
        # variables saved
        input_model_name = self.input_model_name.get()
        input_appliance_type = self.input_appliance_type.get()
        intput_BTUs = self.intput_BTUs.get()

        if not input_appliance_type:
            messagebox.showerror("Error", "Must input appliance type")
            is_valid = False
        
        # for BTU
        if (not intput_BTUs.isdigit()) or (int(intput_BTUs) <= 0):
            messagebox.showerror("Error", "BTU rating must be a positive integer")
            is_valid = False

        if input_appliance_type == "air_handler":     
            air_conditioner = self.air_conditioner.get()
            heater = self.heater.get()
            heat_pump = self.heat_pump.get()

            # for general air handler
            if (air_conditioner == 0) and (heater == 0) and (heat_pump == 0):
                messagebox.showerror("Error", "Must select at least one of them: air conditioner, heater and heat pump")
                is_valid = False

            input_RPM = self.input_RPM.get()
            if (not input_RPM.isdigit()) or (int(input_RPM) <= 0):
                messagebox.showerror("Error", "RPM must be a positive integer")
                is_valid = False

            if air_conditioner == 1:
                input_EER = self.input_EER.get()
                if (not isfloat(input_EER)) or (float(input_EER) <= 0):
                    messagebox.showerror("Error", "EER must be a positive number")
                    is_valid = False
            
            if heater == 1:
                input_energy_source_ah = self.input_energy_source_ah.get()
                if not input_energy_source_ah:
                    messagebox.showerror("Error", "Please select input energy source for heater")
                    is_valid = False               

            if heat_pump == 1:
                input_SEER = self.input_SEER.get()
                input_HSPF = self.input_HSPF.get()
                if (not isfloat(input_SEER)) or (not isfloat(input_HSPF)) or (float(input_SEER) <= 0) or (float(input_HSPF) <= 0):
                    messagebox.showerror("Error", "SEER and HSPF must be a positive number")
                    is_valid = False
            
        elif input_appliance_type == "water_heater":
            # for water heater
            input_tank_size = self.input_tank_size.get()
            input_cur_temp = self.input_cur_temp.get() # this is optional
            input_energy_source_wh = self.input_energy_source_wh.get()
            if (not isfloat(input_tank_size)) or (float(input_tank_size) <= 0):
                messagebox.showerror("Error", "input tank size must be a positive number")
                is_valid = False
            if not input_energy_source_wh:
                messagebox.showerror("Error", "must select energy source for water heater")
                is_valid = False
            if input_cur_temp and (not input_cur_temp.isdigit() or  int(input_cur_temp) <= 0):
                messagebox.showerror("Error", "Please enter vailid current temperature.")
                is_valid = False
        return is_valid
    
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False