from tkinter import *
import tkinter as tk
from db_helper import dbConn

class Report4(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent

        label = tk.Label(self, text="Water heater statistics by state", font=("Sans-serif", 25))
        label.grid(row=0, column=0, sticky="w", pady=10)

        header_frame = tk.Frame(self)
        header_frame.grid(row=1, column=0, columnspan=6, padx=3, sticky='nw')

        label = tk.Label(header_frame, text="State", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=0)

        label = tk.Label(header_frame, text="Average Tank Size", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=1)

        label = tk.Label(header_frame, text="Average BTUs", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=2)

        label = tk.Label(header_frame, text="Average Temp Settings", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=3)

        label = tk.Label(header_frame, text="# with Temp Settings", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=4)

        label = tk.Label(header_frame, text="# with No Temp Settings", width=18, font=("Sans-serif", 12), relief=RIDGE)
        label.grid(row=0, column=5)
    
        self.refresh_sql()
           
    def refresh_sql(self):
        sql1 = """
            WITH temp_table AS (
            SELECT l.state, ROUND(AVG(w.tank_size),0) AS avg_tank_size,
            ROUND(AVG(a.BTU),0) AS avg_btu, ROUND(AVG(w.current_temperature),1) AS avg_temp,
            SUM(CASE WHEN ISNULL(w.current_temperature) THEN 0 ELSE 1 END) AS has_temp,
            SUM(CASE WHEN ISNULL(w.current_temperature) THEN 1 ELSE 0 END) AS no_temp
            FROM WaterHeater w
            INNER JOIN Appliance a
            ON w.email = a.email and w.applianceID = a.applianceID
            INNER JOIN Household h
            ON w.email = h.email
            INNER JOIN Location l
            ON h.postal_code = l.postal_code
            GROUP BY l.state
            ), 
            state_table AS 
            (
            SELECT DISTINCT(STATE) state
            FROM Location
            )
            SELECT s.state, t.avg_tank_size, avg_btu, avg_temp, has_temp, no_temp
            FROM state_table s
            LEFT JOIN temp_table t
            ON s.state = t.state
            ORDER BY s.state ASC
            ;

        """
        result_frame = tk.Frame(self)
        result_frame.grid(row=2, column=0, columnspan=6, sticky='nw')

        self.canvas = tk.Canvas(result_frame, width=1025, height=600)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar=tk.Scrollbar(result_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y, expand=False)
        self.canvas.configure(yscrollcommand=scrollbar.set, scrollregion='0 0 1000 1000')
        self.contents_frame = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.contents_frame, anchor="nw")
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql1)
        rows = cursor.fetchall()
        start_row = 2
        num_rows = len(rows)
        for r in range(num_rows):
            state = rows[r][0]
            avg_tank_size = rows[r][1]
            avg_btu = rows[r][2]
            avg_temp = rows[r][3]
            has_temp = rows[r][4]
            no_temp = rows[r][5]

            state_label = tk.Label(self.contents_frame, text=state, fg="blue", cursor="hand2", font=("Sans-serif", 12, "underline"), width=18, relief=RIDGE)
            state_label.grid(row=start_row + r, column=0)
            state_label.bind("<Button-1>", lambda event, state=state: self.drilldown(state))

            avg_tank_size_label = tk.Label(self.contents_frame, text=avg_tank_size, width=18,font=("Sans-serif", 12),relief=RIDGE)
            avg_tank_size_label.grid(row=start_row + r, column=1)

            avg_btu_label = tk.Label(self.contents_frame, text=avg_btu, width=18,font=("Sans-serif", 12),relief=RIDGE)
            avg_btu_label.grid(row=start_row + r, column=2)

            avg_temp_label = tk.Label(self.contents_frame, text=avg_temp, width=18,font=("Sans-serif", 12),relief=RIDGE)
            avg_temp_label.grid(row=start_row + r, column=3)

            has_temp_label = tk.Label(self.contents_frame, text=has_temp,width=18,font=("Sans-serif", 12),relief=RIDGE)
            has_temp_label.grid(row=start_row + r, column=4)

            no_temp_label = tk.Label(self.contents_frame, text=no_temp,width=18,font=("Sans-serif", 12),relief=RIDGE)
            no_temp_label.grid(row=start_row + r, column=5)

        return_main_label = tk.Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 14, "underline"))
        return_main_label.grid(row=start_row+num_rows+2, column=0, sticky="w", padx=0, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))
    
    def drilldown(self, state):
        popup = tk.Toplevel(self)
        popup.wm_title("Water Heater Drilldown Report")
        popup.geometry('1000x400')
        
        title_label = tk.Label(popup, text=state, font=("Sans-serif", 20))
        title_label.grid(row=0, column=0, sticky="w", pady=10)

        title_label = tk.Label(popup, text='type', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=0, sticky="w")

        title_label = tk.Label(popup, text='min_tank_size', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=1, sticky="w")

        title_label = tk.Label(popup, text='avg_tank_size', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=2, sticky="w")

        title_label = tk.Label(popup, text='max_tank_size', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=3, sticky="w")

        title_label = tk.Label(popup, text='min_temp', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=4, sticky="w")

        title_label = tk.Label(popup, text='avg_temp', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=5, sticky="w")

        title_label = tk.Label(popup, text='max_temp', width=13, font=("Sans-serif", 12, "bold"))
        title_label.grid(row=1, column=6, sticky="w")

        sql1 = f"""
            WITH temp_table AS
            (SELECT w.energy_source,
            ROUND(MIN(w.tank_size),0) as min_tank_size,
            ROUND(AVG(w.tank_size),0) as avg_tank_size,
            ROUND(MAX(w.tank_size),0) as max_tank_size,
            MIN(w.current_temperature) as min_temp,
            ROUND(AVG(w.current_temperature),1) as avg_temp,
            MAX(w.current_temperature) as max_temp
            FROM WaterHeater w
            INNER JOIN Appliance a
            ON w.email = a.email and w.applianceID = a.applianceID
            INNER JOIN Household h
            ON w.email = h.email
            INNER JOIN Location l
            ON h.postal_code = l.postal_code
            WHERE l.state = '{state}'
            GROUP BY w.energy_source
            ),
            all_source AS
            (SELECT 'electric' as energy_source
            UNION
            SELECT 'gas' as energy_source
            UNION
            SELECT 'fuel oil' as energy_source
            UNION
            SELECT 'heat pump' as energy_source
            )
            SELECT a.energy_source,
            min_tank_size,
            avg_tank_size,
            max_tank_size,
            min_temp,
            avg_temp,
            max_temp
            FROM temp_table t
            RIGHT JOIN all_source a
            ON t.energy_source = a.energy_source
            ORDER BY a.energy_source ASC
            ;
            """

        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql1)
        rows = cursor.fetchall() 
        num_rows = len(rows)

        start_row = 2
        for r in range(num_rows):
            energy_source = rows[r][0]
            energy_source_label = tk.Label(popup, text=energy_source, width=13, font=("Sans-serif", 12))
            energy_source_label.grid(row=start_row + r, column=0, sticky="W")

            min_tank_size = rows[r][1]
            min_tank_size_label = tk.Label(popup, text=min_tank_size, width=13, font=("Sans-serif", 12))
            min_tank_size_label.grid(row=start_row + r, column=1, sticky="W")

            avg_tank_size = rows[r][2]
            avg_tank_size_label = tk.Label(popup, text=avg_tank_size, width=13, font=("Sans-serif", 12))
            avg_tank_size_label.grid(row=start_row + r, column=2, sticky="W")

            max_tank_size = rows[r][3]
            max_tank_size_label = tk.Label(popup, text=max_tank_size, width=13, font=("Sans-serif", 12))
            max_tank_size_label.grid(row=start_row + r, column=3, sticky="W")

            min_temp = rows[r][4]
            min_temp_label = tk.Label(popup, text=min_temp, width=13, font=("Sans-serif", 12))
            min_temp_label.grid(row=start_row + r, column=4, sticky="W")

            avg_temp = rows[r][5]
            avg_temp_label = tk.Label(popup, text=avg_temp, width=13, font=("Sans-serif", 12))
            avg_temp_label.grid(row=start_row + r, column=5, sticky="W")

            max_temp = rows[r][6]
            max_temp_label = tk.Label(popup, text=max_temp, width=13, font=("Sans-serif", 12))
            max_temp_label.grid(row=start_row + r, column=6, sticky="W")