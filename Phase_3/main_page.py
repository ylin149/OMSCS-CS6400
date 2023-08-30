from tkinter import *
from household_info_page import HouseholdInfoPage
from view_report_page import ViewReportPage

class MainPage(Frame):
    def __init__(self, parent, enter_info_func, view_reports_func):
        super().__init__(parent)
        self.parent = parent
        self.enter_info_func = enter_info_func
        self.view_reports_func = view_reports_func
        self.initUI()

    def initUI(self):
        self.parent.title('Alternakraft - Summer2023 Team025')
        self.parent.geometry("800x800")
        
        menu_frame = Frame(self.parent)
        menu_frame.pack(pady=50, anchor='w')
        
        label_title = Label(menu_frame, text="Welcome to Alternakraft!", font=("Sans-serif", 30))
        label_title.pack(side=TOP, anchor='w', padx=10, pady=10)
        
        label_description = Label(menu_frame, text="Please choose what you'd like to do:", font=("Sans-serif", 20))
        label_description.pack(side=TOP, anchor='w', padx=10, pady=10)

        enter_info_label = Label(menu_frame, text="Enter my household Info", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        enter_info_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        enter_info_label.bind("<Button-1>", lambda event: self.enter_info_func())

        view_reports_label = Label(menu_frame, text="View reports/query data", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_reports_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_reports_label.bind("<Button-1>", lambda event: self.view_reports_func())



def enter_household_info():
    root.destroy()
    household_info_page = HouseholdInfoPage()
    household_info_page.display()

def view_reports():
    root.destroy()  
    view_report_page = ViewReportPage()
    view_report_page.display()

root = Tk()
main_page = MainPage(root, enter_household_info, view_reports)
main_page.pack()

root.mainloop()
