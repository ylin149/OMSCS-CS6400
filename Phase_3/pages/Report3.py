from tkinter import *
import tkinter as tk 
from tkinter import ttk
from db_helper import dbConn

class Report3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent

        label = tk.Label(self, text="Heating/Cooling method details", font=("Sans-serif", 25))
        label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.refresh_sql()
        
    def refresh_sql(self):
        label = tk.Label(self, text="Air Conditioner", font=("Sans-serif", 15))
        label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # label = tk.Label(self, text="Household Type", font=("Sans-serif", 15))
        # label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        # label = tk.Label(self, text="Count", font=("Sans-serif", 15))
        # label.grid(row=2, column=1, padx=10, sticky="W")

        # label = tk.Label(self, text="Average BTUs", font=("Sans-serif", 15))
        # label.grid(row=2, column=2, padx=10, sticky="W")
        
        # label = tk.Label(self, text="Average RPM", font=("Sans-serif", 15))
        # label.grid(row=2, column=3, padx=10, sticky="W")

        # label = tk.Label(self, text="Average EER", font=("Sans-serif", 15))
        # label.grid(row=2, column=4, padx=10, sticky="W")

        sql1 = """
            WITH temp AS
            (
            SELECT h.household_type, 
            COUNT(ac.email) AS ac_count,
            ROUND(AVG(ap.BTU),0) AS avg_btu,
            ROUND(AVG(ah.RPM),1) AS avg_rpm,
            ROUND(AVG(ac.EER),1) AS avg_eer
            FROM Household h
            INNER JOIN Appliance ap
            ON h.email = ap.email
            INNER JOIN AirHandler ah
            ON ap.email = ah.email AND ap.applianceID = ah.applianceID
            INNER JOIN AirConditioner ac
            ON ah.email = ac.email AND ah.applianceID = ac.applianceID
            GROUP BY h.household_type
            ),
            all_type AS
            (SELECT 'house' as household_type
            UNION
            SELECT 'apartment' as household_type
            UNION
            SELECT 'townhome' as household_type
            UNION
            SELECT 'condominium' as household_type
            UNION
            SELECT 'modular home' as household_type
            UNION
            SELECT 'tiny house' as household_type
            )
            SELECT a.household_type, 
            ac_count,
            avg_btu,
            avg_rpm,
            avg_eer
            FROM temp t
            RIGHT JOIN all_type a
            ON t.household_type = a.household_type
            ORDER BY a.household_type
            ;
        """
        
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql1)
        rows = cursor.fetchall()
        num_rows = len(rows)
        start_row = 3

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=6)
        tree.grid(row=start_row, column=0, padx=10, sticky="w")
        tree.column("# 1", width=100, anchor=tk.CENTER)
        tree.heading("# 1", text="Household Type")
        tree.column("# 2", width=100, anchor=tk.CENTER)
        tree.heading("# 2", text="Count")
        tree.column("# 3", width=100, anchor=tk.CENTER)
        tree.heading("# 3", text="Average BTUs")
        tree.column("# 4", width=100, anchor=tk.CENTER)
        tree.heading("# 4", text="Average RPM")
        tree.column("# 5", width=100, anchor=tk.CENTER)
        tree.heading("# 5", text="Average EER")

        for row in rows:
            tree.insert("", tk.END, values=row) 

        # for r in range(num_rows):
        #     household = rows[r][0]
        #     count = rows[r][1]
        #     avg_btu = rows[r][2]
        #     avg_rpm = rows[r][3]
        #     avg_eer = rows[r][4]

        #     household_label = tk.Label(self, text=household, font=("Sans-serif", 15))
        #     household_label.grid(row=start_row + r, column=0, padx=10, pady=5, sticky="W")

        #     count_label = tk.Label(self, text=count, font=("Sans-serif", 15))
        #     count_label.grid(row=start_row + r, column=1, padx=10, pady=5, sticky="W")

        #     avg_btu_label = tk.Label(self, text=avg_btu, font=("Sans-serif", 15))
        #     avg_btu_label.grid(row=start_row + r, column=2, padx=10, pady=5, sticky="W")

        #     avg_rpm_label = tk.Label(self, text=avg_rpm, font=("Sans-serif", 15))
        #     avg_rpm_label.grid(row=start_row + r, column=3, padx=10, pady=5, sticky="W")
            
        #     avg_eer_label = tk.Label(self, text=avg_eer, font=("Sans-serif", 15))
        #     avg_eer_label.grid(row=start_row + r, column=4, padx=10, pady=5, sticky="W")
        
        start_row += num_rows
        
        label = tk.Label(self, text="Heater", font=("Sans-serif", 15))
        label.grid(row=start_row, column=0, padx=10, pady=10, sticky="w")

        # label = tk.Label(self, text="Household Type", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=0, padx=10, pady=10, sticky="W")

        # label = tk.Label(self, text="Count", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=1, padx=10, pady=10, sticky="W")

        # label = tk.Label(self, text="Average BTUs", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=2, padx=10, pady=10, sticky="W")
        
        # label = tk.Label(self, text="Average RPM", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=3, padx=10, pady=10, sticky="W")

        # label = tk.Label(self, text="Average EER", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=4, padx=10, pady=10, sticky="W")

        sql2 = """
            WITH a AS (
            SELECT h.household_type, ht.energy_source, count(*) AS cnt
            FROM Household h
            INNER JOIN Appliance ap
            ON h.email = ap.email
            INNER JOIN AirHandler ah
            ON ap.email = ah.email AND ap.applianceID = ah.applianceID
            INNER JOIN Heater ht
            ON ah.email = ht.email AND ah.applianceID = ht.applianceID
            GROUP BY h.household_type, ht.energy_source
            ), b AS
            (
            SELECT household_type, energy_source, cnt, ROW_NUMBER() OVER (PARTITION BY household_type ORDER BY cnt DESC) row_num
            FROM a
            ), c AS
            (
            SELECT household_type, energy_source
            FROM b
            WHERE row_num=1
            ), temp AS
            (
            SELECT 
            h.household_type, 
            COUNT(ht.email) AS ht_count,
            ROUND(AVG(ap.BTU),0) AS avg_btu,
            ROUND(AVG(ah.RPM),1) AS avg_rpm
            FROM Household h
            INNER JOIN Appliance ap
            ON h.email = ap.email
            INNER JOIN AirHandler ah
            ON ap.email = ah.email AND ap.applianceID = ah.applianceID
            INNER JOIN Heater ht
            ON ah.email = ht.email AND ah.applianceID = ht.applianceID
            GROUP BY h.household_type
            ),
            all_type AS
            (SELECT 'house' as household_type
            UNION
            SELECT 'apartment' as household_type
            UNION
            SELECT 'townhome' as household_type
            UNION
            SELECT 'condominium' as household_type
            UNION
            SELECT 'modular home' as household_type
            UNION
            SELECT 'tiny house' as household_type
            )
            SELECT all_type.household_type, 
            ht_count,
            avg_btu,
            avg_rpm,
            c.energy_source
            FROM temp t
            INNER JOIN c
            ON t.household_type = c.household_type
            RIGHT JOIN all_type
            ON t.household_type = all_type.household_type
            ORDER BY all_type.household_type
            ;
        """
        
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql2)
        rows = cursor.fetchall()
        num_rows = len(rows)
        start_row += 2

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=6)
        tree.grid(row=start_row, column=0, padx=10, sticky="w")
        tree.column("# 1", width=100, anchor=tk.CENTER)
        tree.heading("# 1", text="Household Type")
        tree.column("# 2", width=100, anchor=tk.CENTER)
        tree.heading("# 2", text="Count")
        tree.column("# 3", width=100, anchor=tk.CENTER)
        tree.heading("# 3", text="Average BTUs")
        tree.column("# 4", width=100, anchor=tk.CENTER)
        tree.heading("# 4", text="Average RPM")
        tree.column("# 5", width=200, anchor=tk.CENTER)
        tree.heading("# 5", text="Most Common Energy Source")

        for row in rows:
            tree.insert("", tk.END, values=row) 

        # for r in range(num_rows):
        #     household = rows[r][0]
        #     count = rows[r][1]
        #     avg_btu = rows[r][2]
        #     avg_rpm = rows[r][3]
        #     avg_eer = rows[r][4]

        #     household_label = tk.Label(self, text=household, font=("Sans-serif", 15))
        #     household_label.grid(row=start_row + r, column=0, padx=10, pady=5, sticky="W")

        #     count_label = tk.Label(self, text=count, font=("Sans-serif", 15))
        #     count_label.grid(row=start_row + r, column=1, padx=10, pady=5, sticky="W")

        #     avg_btu_label = tk.Label(self, text=avg_btu, font=("Sans-serif", 15))
        #     avg_btu_label.grid(row=start_row + r, column=2, padx=10, pady=5, sticky="W")

        #     avg_rpm_label = tk.Label(self, text=avg_rpm, font=("Sans-serif", 15))
        #     avg_rpm_label.grid(row=start_row + r, column=3, padx=10, pady=5, sticky="W")
            
        #     avg_eer_label = tk.Label(self, text=avg_eer, font=("Sans-serif", 15))
        #     avg_eer_label.grid(row=start_row + r, column=4, padx=10, pady=5, sticky="W")
        
        # start_row += num_rows

        #     most_common_energy_source = '' if most_common_energy_source is None else most_common_energy_source
        #     most_common_energy_source_label = tk.Label(self, text=most_common_energy_source, font=("Sans-serif", 15))
        #     most_common_energy_source_label.grid(row=start_row + r, column=3, padx=10, pady=10, sticky="W")

        # ht_label = tk.Label(self, text="Heat Pump Count", font=("Sans-serif", 15))
        # ht_label.grid(row=start_row, column=1, padx=10, pady=10, sticky="W")

        # ht_label = tk.Label(self, text="Average HeatPump BTUs", font=("Sans-serif", 15))
        # ht_label.grid(row=start_row, column=2, padx=10, pady=10, sticky="W")

        # ht_label = tk.Label(self, text="Average SEER", font=("Sans-serif", 15))
        # ht_label.grid(row=start_row, column=3, padx=10, pady=10, sticky="W")

        # ht_label = tk.Label(self, text="Average SEER", font=("Sans-serif", 15))
        # ht_label.grid(row=start_row, column=4, padx=10, pady=10, sticky="W")

        # start_row += 1

        # for r in range(query_3_row):
        #     householdType = HeatPump_query_result[r][0]
        #     count = HeatPump_query_result[r][1]
        #     average_btu_rating = HeatPump_query_result[r][2]
        #     average_seer = HeatPump_query_result[r][3]
        #     average_hspf = HeatPump_query_result[r][4]
        #     # First Table Col Names
        #     householdType_label = tk.Label(self, text=householdType, font=("Sans-serif", 15))
        #     householdType_label.grid(row=start_row + r, column=0, padx=10, pady=10, sticky="W")

        #     count_label = tk.Label(self, text=count, font=("Sans-serif", 15))
        #     count_label.grid(row=start_row + r, column=1, padx=10, pady=10, sticky="W")

        #     average_btu_rating_label = tk.Label(self, text=average_btu_rating, font=("Sans-serif", 15))
        #     average_btu_rating_label.grid(row=start_row + r, column=2, padx=10, pady=10, sticky="W")

        #     average_seer_label = tk.Label(self, text=average_seer, font=("Sans-serif", 15))
        #     average_seer_label.grid(row=start_row + r, column=3, padx=10, pady=10, sticky="W")

        #     average_hspf_label = tk.Label(self, text=average_hspf, font=("Sans-serif", 15))
        #     average_hspf_label.grid(row=start_row + r, column=4, padx=10, pady=10, sticky="W")
        

        
        # 3rd table
        start_row += num_rows
        label = tk.Label(self, text="Heat Pump", font=("Sans-serif", 15))
        label.grid(row=start_row, column=0, padx=10, pady=10, sticky="W")

        # label = tk.Label(self, text="Household Type", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=0, padx=10, sticky="W")

        # label = tk.Label(self, text="Count", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=1, padx=10, sticky="W")

        # label = tk.Label(self, text="Average BTUs", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=2, padx=10, sticky="W")
        
        # label = tk.Label(self, text="Average RPM", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=3, padx=10, sticky="W")

        # label = tk.Label(self, text="Average SEER", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=4, padx=10, sticky="W")

        # label = tk.Label(self, text="Average HSPF", font=("Sans-serif", 15))
        # label.grid(row=start_row+1, column=4, padx=10, sticky="W")

        sql3 = """
            WITH temp AS
            (
            SELECT h.household_type, 
            COUNT(hp.email) AS hp_count,
            ROUND(AVG(ap.BTU),0) AS avg_btu,
            ROUND(AVG(ah.RPM),1) AS avg_rpm,
            ROUND(AVG(hp.SEER),1) AS avg_seer,
            ROUND(AVG(hp.HSPF),1) AS avg_hspf
            FROM Household h
            INNER JOIN Appliance ap
            ON h.email = ap.email
            INNER JOIN AirHandler ah
            ON ap.email = ah.email AND ap.applianceID = ah.applianceID
            INNER JOIN HeatPump hp
            ON ah.email = hp.email AND ah.applianceID = hp.applianceID
            GROUP BY h.household_type
            ),
            all_type AS
            (SELECT 'house' as household_type
            UNION
            SELECT 'apartment' as household_type
            UNION
            SELECT 'townhome' as household_type
            UNION
            SELECT 'condominium' as household_type
            UNION
            SELECT 'modular home' as household_type
            UNION
            SELECT 'tiny house' as household_type
            )
            SELECT a.household_type, 
            hp_count,
            avg_btu,
            avg_rpm,
            avg_seer,
            avg_hspf
            FROM temp t
            RIGHT JOIN all_type a
            ON t.household_type = a.household_type
            ORDER BY a.household_type
            ;
        """
        
        cursor = dbConn.get_conn().cursor()
        cursor.execute(sql3)
        rows = cursor.fetchall()
        num_rows = len(rows)
        start_row += 2

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=6)
        tree.grid(row=start_row, column=0, padx=10, sticky="w")
        tree.column("# 1", width=100, anchor=tk.CENTER)
        tree.heading("# 1", text="Household Type")
        tree.column("# 2", width=100, anchor=tk.CENTER)
        tree.heading("# 2", text="Count")
        tree.column("# 3", width=100, anchor=tk.CENTER)
        tree.heading("# 3", text="Average BTUs")
        tree.column("# 4", width=100, anchor=tk.CENTER)
        tree.heading("# 4", text="Average RPM")
        tree.column("# 5", width=100, anchor=tk.CENTER)
        tree.heading("# 5", text="Average SEER")
        tree.column("# 6", width=100, anchor=tk.CENTER)
        tree.heading("# 6", text="Average HSPF")
        for row in rows:
            tree.insert("", tk.END, values=row) 


        return_main_label = tk.Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 15, "underline"))
        return_main_label.grid(row=start_row+num_rows+2, column=0, sticky='w', padx=0, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))

        # for r in range(num_rows):
        #     household = rows[r][0]
        #     count = rows[r][1]
        #     avg_btu = rows[r][2]
        #     avg_rpm = rows[r][3]
        #     avg_seer = rows[r][4]
        #     avg_hspf = rows[r][5]

        #     household_label = tk.Label(self, text=household, font=("Sans-serif", 15))
        #     household_label.grid(row=start_row + r, column=0, padx=10, pady=5, sticky="W")

        #     count_label = tk.Label(self, text=count, font=("Sans-serif", 15))
        #     count_label.grid(row=start_row + r, column=1, padx=10, pady=5, sticky="W")

        #     avg_btu_label = tk.Label(self, text=avg_btu, font=("Sans-serif", 15))
        #     avg_btu_label.grid(row=start_row + r, column=2, padx=10, pady=5, sticky="W")

        #     avg_rpm_label = tk.Label(self, text=avg_rpm, font=("Sans-serif", 15))
        #     avg_rpm_label.grid(row=start_row + r, column=3, padx=10, pady=5, sticky="W")
            
        #     avg_seer_label = tk.Label(self, text=avg_seer, font=("Sans-serif", 15))
        #     avg_seer_label.grid(row=start_row + r, column=4, padx=10, pady=5, sticky="W")

        #     avg_hspf_label = tk.Label(self, text=avg_hspf, font=("Sans-serif", 15))
        #     avg_hspf_label.grid(row=start_row + r, column=4, padx=10, pady=5, sticky="W")


