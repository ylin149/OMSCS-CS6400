from tkinter import *

class ViewReportPage:
    def __init__(self):
        self.view_report_window = None

    def display(self):
        self.view_report_window = Tk()
        self.view_report_window.title("View Reports")
        self.view_report_window.geometry("800x800")
        # Add widgets and functionality for the view report page here

        # Example: Adding a label in the view report page
        label = Label(self.view_report_window, text="This is the View Reports Page")
        label.pack()

        self.view_report_window.mainloop()

# Run the view report page as a standalone application
if __name__ == "__main__":
    view_report_page = ViewReportPage()
    view_report_page.display()
