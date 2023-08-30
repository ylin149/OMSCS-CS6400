from tkinter import *
import tkinter as tk

class ViewReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.initUI()

    def initUI(self):    
        label_title = Label(self, text="View Report", font=("Sans-serif", 30))
        label_title.pack(side=TOP, anchor='w', padx=10, pady=10)
        label_description = Label(self, text="Please choose which report you want to reivew:", font=("Sans-serif", 20))
        label_description.pack(side=TOP, anchor='w', padx=10, pady=10)

        view_report1_label = Label(self, text="Top 25 popular manufacturers", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report1_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report1_label.bind("<Button-1>", lambda event: self.controller.display("Report1"))
 
        view_report2_label = Label(self, text="Manufacturer/model search", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report2_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report2_label.bind("<Button-1>", lambda event: self.controller.display("Report2"))

        view_report3_label = Label(self, text="Heating/cooling method details", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report3_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report3_label.bind("<Button-1>", lambda event: self.controller.display("Report3"))
        
        view_report4_label = Label(self, text="Water heater statistics by state", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report4_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report4_label.bind("<Button-1>", lambda event: self.controller.display("Report4"))
 
        view_report5_label = Label(self, text="Off-the-grid household dashboard", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report5_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report5_label.bind("<Button-1>", lambda event: self.controller.display("Report5"))

        view_report6_label = Label(self, text="Household averages by radius", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_report6_label.pack(side=TOP, anchor='w', padx=10, pady=10)
        view_report6_label.bind("<Button-1>", lambda event: self.controller.display("Report6"))