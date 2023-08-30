from tkinter import *

class HouseholdInfoPage:
    def __init__(self):
        self.household_info_window = None

    def display(self):
        self.household_info_window = Tk()
        self.household_info_window.title("Household Information")
        self.household_info_window.geometry("800x800")

        label = Label(self.household_info_window, text="This is the Household Information Page")
        label.pack()

        self.household_info_window.mainloop()

# Run the main application
if __name__ == "__main__":
    household_info_page = HouseholdInfoPage()
    household_info_page.display()
