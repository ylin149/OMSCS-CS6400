import tkinter as tk 
from db_helper import dbConn

class Report1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        super().__init__(parent)

        label = tk.Label(self, text="Top 25 Popular Manufacturers", font=("Sans-serif", 24))
        label.grid(row=0, column=0)

        label = tk.Label(self, text="Manufacturer", font=("Sans-serif", 16, "bold"))
        label.grid(row=1, column=0)

        label = tk.Label(self, text="Raw Count", font=("Sans-serif", 16, "bold"))
        label.grid(row=1, column=1)
        
        self.refresh_sql()
    
    def refresh_sql(self):
        sql1 = '''
            SELECT manufacturer_name, count(*) AS count_appliances 
            FROM Appliance 
            GROUP BY manufacturer_name 
            ORDER BY count_appliances DESC 
            LIMIT 25;
            '''

        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql1)
        rows = cursor.fetchall()    

        num_rows = len(rows)
        start_row = 2

        for row in range(num_rows):
            manufacturer_name, count = rows[row][0], rows[row][1]

            name_label = tk.Label(self, text=manufacturer_name, fg="blue", cursor="hand2", font=("Sans-serif", 14, "underline"))
            name_label.grid(row = start_row + row, column=0)

            count_label = tk.Label(self, text=count, font=("Sans-serif", 14))
            count_label.grid(row = start_row + row, column=1)

            name_label.bind("<Button-1>", lambda event, manufacturer_name=manufacturer_name: self.drilldown(manufacturer_name))
           
        return_main_label = tk.Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        return_main_label.grid(row=num_rows+6, column=0, padx=0, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))

    def drilldown(self, manufacturer_name):
        popup = tk.Toplevel(self)
        popup.wm_title("Manufacturer Drilldown Report")
        popup.geometry('600x400')
        
        title_label = tk.Label(popup, text=manufacturer_name, font=("Sans-serif", 15, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        title_label = tk.Label(popup, text='Appliance Type', font=("Sans-serif", 14))
        title_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        title_label = tk.Label(popup, text='Raw Count', font=("Sans-serif", 14))
        title_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")


        sql1 = f"""
            SELECT 'Water Heater', COUNT(*) AS appliance_count 
            FROM Appliance 
            WHERE manufacturer_name = '{manufacturer_name}' 
            AND appliance_type = 'water_heater'
            """
        
        sql2 = f"""
            SELECT 'Air Handler', COUNT(*) AS appliance_count 
            FROM Appliance 
            WHERE manufacturer_name = '{manufacturer_name}' 
            AND appliance_type = 'air_handler'
            """
        
        sql3 = f"""
            SELECT 'Air Conditioner', COUNT(*) AS appliance_count 
	        FROM Appliance as A 
            INNER JOIN AirConditioner as AC 
		    ON (A.email = AC.email AND A.applianceID = AC.applianceID) 
			WHERE A.manufacturer_name = '{manufacturer_name}'
        """

        sql4 = f"""
            SELECT 'Heater', COUNT(*) AS appliance_count 
	        FROM Appliance as A 
            INNER JOIN Heater as AC 
		    ON (A.email = AC.email AND A.applianceID = AC.applianceID) 
			WHERE A.manufacturer_name = '{manufacturer_name}'
        """

        sql5 = f"""
            SELECT 'Heat Pump', COUNT(*) AS appliance_count 
	        FROM Appliance as A 
            INNER JOIN HeatPump as AC 
		    ON (A.email = AC.email AND A.applianceID = AC.applianceID) 
			WHERE A.manufacturer_name = '{manufacturer_name}'
        """
        
        # tree = ttk.Treeview(popup, column=("c1", "c2"), show='headings')

        # tree.column("#1", anchor=tk.CENTER)
        # tree.heading("#1", text="Appliance Type")
        # tree.column("#2", anchor=tk.CENTER)
        # tree.heading("#2", text="Raw Count")
        # tree.grid(row=1,column=0, padx=10)
        
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql1)
        rows = cursor.fetchall() 
        appliance_type_label = tk.Label(popup, text='Water Heater', font=("Sans-serif", 14))
        number_label = tk.Label(popup, text=rows[0][1], font=("Sans-serif", 14))
        appliance_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        number_label.grid(row=2, column=1, padx=10)
        
        # tree.insert('', 'end', '1', value=rows[0],open=False)
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql2)
        rows = cursor.fetchall() 
        appliance_type_label = tk.Label(popup, text='Air Handler', font=("Sans-serif", 14))
        number_label = tk.Label(popup, text=rows[0][1], font=("Sans-serif", 14))
        appliance_type_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        number_label.grid(row=3, column=1, padx=10)
        # tree.insert('', 'end', '2', value=rows[0],open=False)
        # cursor = dbConn.get_conn().cursor()
        # cursor.execute(sql3)
        # rows = cursor.fetchall() 
        # appliance_type_label = tk.Label(popup, text='Air Conditioner')
        # number_label = tk.Label(popup, text=rows[0][1])
        # appliance_type_label.grid(row=4, column=0, padx=30, pady=10, sticky="w")
        # number_label.grid(row=4, column=1, padx=10)
        # # tree.insert('2', 'end', '3', value=rows[0],open=False)
        # cursor = dbConn.get_conn().cursor()
        # cursor.execute(sql4)
        # rows = cursor.fetchall() 
        # appliance_type_label = tk.Label(popup, text='Heater')
        # number_label = tk.Label(popup, text=rows[0][1])
        # appliance_type_label.grid(row=5, column=0, padx=30, pady=10, sticky="w")
        # number_label.grid(row=5, column=1, padx=10)
        # # tree.insert('2', 'end', '4', value=rows[0],open=False)
        # cursor = dbConn.get_conn().cursor()
        # cursor.execute(sql5)
        # rows = cursor.fetchall() 
        # appliance_type_label = tk.Label(popup, text='Heat Pump')
        # number_label = tk.Label(popup, text=rows[0][1])
        # appliance_type_label.grid(row=6, column=0, padx=30, pady=10, sticky="w")
        # number_label.grid(row=6, column=1, padx=10)
        # tree.insert('2', 'end', '5', value=rows[0],open=False)
