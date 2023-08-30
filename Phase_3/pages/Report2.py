from tkinter import *
from tkinter import messagebox
from db_helper import dbConn

class Report2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #UI layout
        label_title = Label(self, text="Manufacturer/model search", font=("Sans-serif", 30))
        label_title.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        search_label = Label(self, text="Please enter the Manufacturer/Model Name:", font=("Sans-serif", 12))
        search_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        self.search_entry = Entry(self, width=50, font=("Sans-serif", 12))
        self.search_entry.grid(row=2, column=0, sticky='w', padx=10)

        search_button = Button(self, text="Search", command=self.search_button_clicked, font=("Sans-serif", 12, "bold"))
        search_button.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        return_main_label = Label(self, text="Return to the main menu", fg="blue", font=("Sans-serif", 15, "underline"))
        return_main_label.grid(row=5, column=0, sticky='w', padx=10, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))

        self.entries = []
        self.no_result_label = None  # To store the "No result found" label

        # Add a frame for the results
        self.results_frame = Frame(self)
        self.results_frame.grid(row=4, column=0, sticky='w', padx=10, pady=10)

        # Add a canvas in that frame
        self.canvas = Canvas(self.results_frame,width=550,height=500)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add a scrollbar in the frame
        self.scrollbar = Scrollbar(self.results_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Attach the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Add another frame in the canvas to hold the contents
        self.contents_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.contents_frame, anchor="nw")

        self.contents_frame.bind("<Configure>", self.on_frame_configure)

        # Display the column names
        column_names = ["Manufacturer Name", "Model"]
        column_frame = Frame(self.contents_frame)
        column_frame.pack(side=TOP, fill=X)
        for name in column_names:
            label = Label(column_frame, text=name, font=("Sans-serif"), width=30, relief=RIDGE)
            label.pack(side=LEFT, expand=True, fill=X)

    def on_frame_configure(self, event=None):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def clear_results(self):
        # Clear previous search results 
        for frame in self.entries:
            frame.destroy()
        self.entries = []

        if self.no_result_label is not None:
            self.no_result_label.destroy()
            self.no_result_label = None

    def search_button_clicked(self):
        # Clear previous search results
        self.clear_results()

        # Get the search keyword
        keyword = self.search_entry.get().lower()
        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword.")
            return
        
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"SELECT manufacturer_name, model FROM Appliance WHERE (model LIKE '%{keyword}%' OR manufacturer_name LIKE '%{keyword}%') ORDER BY manufacturer_name ASC, model ASC"
        cursor.execute(query)
        results = cursor.fetchall()

        if len(results) == 0:
            #If no match 
            self.no_result_label = Label(self.contents_frame, text="No result found", font=("Sans-serif"))
            self.no_result_label.pack(side=TOP, padx=10, pady=10)
        else:
            # Display the search results
            for i, result in enumerate(results):
                manufacturer_name = result[0] if result[0] is not None else ""
                model_name = result[1] if result[1] is not None else ""

                # Check if any cell matches the search keyword, if -1, no match
                manufacturer_match = manufacturer_name.lower().find(keyword) != -1
                model_match = model_name.lower().find(keyword) != -1

                row_frame = Frame(self.contents_frame)
                row_frame.pack(side=TOP, fill=X, anchor="w")  # align the row frame to the left
                # appending matched cells
                for manufacturer, model in enumerate([manufacturer_name, model_name]):
                    entry = Entry(row_frame, font=("Sans-serif"), width=30, justify="center")
                    entry.insert(0, model)
                    entry.pack(side=LEFT, expand=True, fill=X)

                    if (manufacturer == False and manufacturer_match) or (manufacturer == True and model_match):
                        entry.config(bg="light green")

                self.entries.append(row_frame)

        cursor.close()



if __name__ == "__main__":
    root = Tk()
    app = Report2(root, None)
    app.pack()
    root.mainloop()
