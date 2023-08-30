import tkinter as tk 


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.initUI()

    def initUI(self):
        label_title = tk.Label(self, text="Welcome to Alternakraft!", font=("Sans-serif", 30))
        label_title.pack(side="top", anchor='w', padx=10, pady=10)
        
        label_description = tk.Label(self, text="Please choose what you'd like to do:", font=("Sans-serif", 20))
        label_description.pack(side="top", anchor='w', padx=10, pady=10)

        enter_info_label = tk.Label(self, text="Enter my household Info", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        enter_info_label.pack(side="top", anchor='w', padx=10, pady=10)
        enter_info_label.bind("<Button-1>", lambda event: self.controller.display("HouseholdInfoPage"))

        view_reports_label = tk.Label(self, text="View reports/query data", fg="blue", cursor="hand2", font=("Sans-serif", 15,"underline"))
        view_reports_label.pack(side="top", anchor='w', padx=10, pady=10)
        view_reports_label.bind("<Button-1>", lambda event: self.controller.display("ViewReportPage"))

