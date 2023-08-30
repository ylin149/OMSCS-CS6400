from tkinter import *
import tkinter as tk 

class WrappingUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label_title = Label(self, text="Submission Complete!", font=("Sans-serif", 30))
        label_title.pack(side=TOP, anchor='w', padx=10, pady=10)

        label_description = Label(self, text="Thank you for providing your information to Alternakraft!", font=("Sans-serif", 20))
        label_description.pack(side=TOP, anchor='w', padx=10, pady=10)

        return_main_label = Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        return_main_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        return_main_label.bind("<Button-1>", self.return_to_main_menu)
class WrappingUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label_title = Label(self, text="Submission Complete!", font=("Sans-serif", 30))
        label_title.pack(side=TOP, anchor='w', padx=10, pady=10)

        label_description = Label(self, text="Thank you for providing your information to Alternakraft!", font=("Sans-serif", 20))
        label_description.pack(side=TOP, anchor='w', padx=10, pady=10)

        return_main_label = Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        return_main_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        return_main_label.bind("<Button-1>", self.return_to_main_menu)

    def return_to_main_menu(self, event):
        # Loop through all frames
        for frame_name, frame in self.controller.frames.items():
            # Loop through all attributes of the frame
            for attr_name, attr_value in frame.__dict__.items():
                # Check if the attribute is a tkinter Entry widget and not manufacturer_name_list
                if isinstance(attr_value, tk.Entry) and attr_name != "manufacturer_name_list":
                    # If the attribute is not None, delete its contents
                    if attr_value is not None:
                        attr_value.delete(0, 'end')
        
        # Uncheck checkboxes
        self.controller.frames["HouseholdInfoPage"].heating_data_type.set(0)
        self.controller.frames["HouseholdInfoPage"].cooling_data_type.set(0)
        self.controller.frames["HouseholdInfoPage"].electric_data_type.set(0)
        self.controller.frames["HouseholdInfoPage"].gas_data_type.set(0)
        self.controller.frames["HouseholdInfoPage"].steam_data_type.set(0)
        self.controller.frames["HouseholdInfoPage"].liquid_fuel_data_type.set(0)

        # Return to the main menu
        self.controller.display("MainPage")
