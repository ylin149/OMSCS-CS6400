import tkinter as tk
from pages.MainMenu import MainPage
from pages.HouseholdInfo import HouseholdInfoPage
from pages.AddAppliance import AddAppliancePage
from pages.ApplianceListing import ApplianceListingPage
from pages.AddPowerGeneration import PowerGenerationPage
from pages.PowerGenerationListing import PowerGenerationListingPage
from pages.ViewReports import ViewReportPage
from pages.WrappingUp import WrappingUpPage
from pages.Report1 import Report1
from pages.Report2 import Report2
from pages.Report3 import Report3
from pages.Report4 import Report4
from pages.Report5 import Report5
from pages.Report6 import Report6
from db_helper import dbConn, create_tables, create_testdata


create_tables()
create_testdata()

class HouseholdApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1050x1000")
        self.title("Alternakraft - CS6400_Summer2023_Team025")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # current email selection
        self.input_email = None
        self.appliance_number = 1
        self.power_generator_number = 1
        self.frames = {}

        all_report_pages = [MainPage, HouseholdInfoPage, AddAppliancePage,ApplianceListingPage, PowerGenerationPage, PowerGenerationListingPage, WrappingUpPage, ViewReportPage,Report1,Report2,Report3,Report4,Report5,Report6]
        for F in all_report_pages:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.display("MainPage")
    
    def display(self, page_name):
        """
        stack the frames on top of each other, then raise one above the other in the stacking order
        """
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "refresh_sql"):
            frame.refresh_sql()

    def increase_appliance_number(self):
        self.appliance_number += 1
        return
    
    def increase_power_generator_number(self):
        self.power_generator_number += 1
        return
    
    def refresh(self, page_name):
        frame = self.frames[page_name]
        frame.refresh()
    

if __name__ == "__main__":
    app = HouseholdApp()
    app.mainloop()