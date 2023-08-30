from tkinter import *
from db_helper import dbConn

class Report5(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        
        label_title = Label(self, text="Off-the-grid Household Dashboard ", font=("Sans-serif", 18))
        label_title.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.refresh_sql()
        
    def refresh_sql(self):
        first_report_title = Label(self, text="State with Most Off-the-grid Household", font=("Sans-serif", 10, "bold"))
        first_report_title.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for first table
        self.results_frame_first = Frame(self)
        self.results_frame_first.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        # Insert first table
        self.insert_most_off_household()

        second_report_title = Label(self, text="Average Battery Storage Capacity", font=("Sans-serif", 10, "bold"))
        second_report_title.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for second table
        self.results_frame_second = Frame(self)
        self.results_frame_second.grid(row=4, column=0, sticky='w', padx=10, pady=10)

        # Insert second table
        self.insert_avg_battery_capacity()

        third_report_title = Label(self, text="Percentage of Power Generation Type", font=("Sans-serif", 10, "bold"))
        third_report_title.grid(row=5, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for third table
        self.results_frame_third = Frame(self)
        self.results_frame_third.grid(row=6, column=0, sticky='w', padx=10, pady=10)

        # Insert third table
        self.insert_perct_power_generation()

        fourth_report_title = Label(self, text="Percentage of Household Type", font=("Sans-serif", 10, "bold"))
        fourth_report_title.grid(row=7, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for fourth table
        self.results_frame_fourth = Frame(self)
        self.results_frame_fourth.grid(row=8, column=0, sticky='w', padx=10, pady=10)

        # Insert fourth table
        self.insert_perct_household()

        fifth_report_title = Label(self, text="Average Water Heater Tank Size", font=("Sans-serif", 10, "bold"))
        fifth_report_title.grid(row=9, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for fifth table
        self.results_frame_fifth = Frame(self)
        self.results_frame_fifth.grid(row=10, column=0, sticky='w', padx=10, pady=10)

        # Insert fifth table
        self.insert_avg_water_tank_size()

        sixth_report_title = Label(self, text="Min, Max, Average BTU", font=("Sans-serif", 10, "bold"))
        sixth_report_title.grid(row=11, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for sixth table
        self.results_frame_sixth = Frame(self)
        self.results_frame_sixth.grid(row=12, column=0, sticky='w', padx=10, pady=10)

        # Insert sixth table
        self.insert_btu_info()

        return_main_label = Label(self, text="Return to the main menu", fg="blue", cursor="hand2", font=("Sans-serif", 12,"underline"))
        return_main_label.grid(row=13, column=0, sticky='w', padx=10, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))

    def insert_most_off_household(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"SELECT tmp.state, count(*) as household_count FROM (SELECT L.state FROM Household as H LEFT JOIN Location as L ON H.postal_code = L.postal_code WHERE H.email NOT IN (SELECT email FROM PublicUtility)) as tmp GROUP BY tmp.state ORDER BY count(*) DESC LIMIT 1"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["State","Household Count"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_first, font=("Sans-serif",10,"bold"), width=20, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_first, font=("Sans-serif",10), width=20, justify="center")
                entry.grid(row=i+1,column=j)
                entry.insert(END, r[j])

    def insert_avg_battery_capacity(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"SELECT ROUND(avg(tmp.battery_storage_capacity_kilowatt_hours)) as avg_battery_capacity FROM (SELECT P.battery_storage_capacity_kilowatt_hours FROM PowerGenerator as P WHERE P.email NOT IN (SELECT email FROM PublicUtility)) as tmp"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["Average Battery Capacity"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_second, font=("Sans-serif",10,"bold"), width=40, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_second, font=("Sans-serif",10), width=40, justify="center")
                entry.grid(row=i+1,column=j)
                entry.insert(END, r[j])
    
    def insert_perct_power_generation(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"WITH Off_grid_household AS(SELECT P.email, P.generator_type FROM Household as H LEFT JOIN PowerGenerator as P ON H.email = P.email WHERE H.email NOT IN(SELECT email FROM PublicUtility)),\
                Type_generator_count AS(SELECT * FROM (SELECT 'solar' as generator_type, COUNT(DISTINCT email) as count_type FROM  Off_grid_household WHERE email IN (SELECT email from Off_grid_household WHERE generator_type ='solar') AND email NOT IN (SELECT email from Off_grid_household WHERE generator_type ='wind-turbine') )as tmp1 UNION ALL\
                SELECT * FROM (SELECT 'wind-turbine' as generator_type,  COUNT(DISTINCT email) as count_type FROM  Off_grid_household WHERE email IN (SELECT email from Off_grid_household WHERE generator_type ='wind-turbine') AND email NOT IN (SELECT email from Off_grid_household WHERE generator_type ='solar'))as tmp2 UNION ALL\
                SELECT * FROM (SELECT 'mixed' as generator_type, COUNT(DISTINCT email) as count_type FROM  Off_grid_household WHERE email IN (SELECT email from Off_grid_household WHERE generator_type ='solar') AND email IN (SELECT email from Off_grid_household WHERE generator_type ='wind-turbine')) as tmp3)\
                SELECT generator_type, ROUND(count_type/(SELECT SUM(count_type) FROM Type_generator_count)*100,1) as count_percent FROM  Type_generator_count"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["Generator Type","Count %"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_third, font=("Sans-serif",10,"bold"), width=25, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_third, font=("Sans-serif",10), width=25, justify="center")
                entry.grid(row=i+1,column=j)
                entry.insert(END, r[j])
    
    def insert_perct_household(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"WITH Off_grid_household AS(SELECT H.household_type FROM Household as H WHERE H.email NOT IN (SELECT email FROM PublicUtility)),\
                    Type_houshold_count AS(SELECT * FROM (SELECT 'house' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type ='house') as tmp1 UNION ALL\
                                           SELECT * FROM (SELECT 'apartment' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type = 'apartment') as tmp2 UNION ALL\
                                           SELECT * FROM  (SELECT 'townhome' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type ='townhome') as tmp3 UNION ALL\
                                           SELECT * FROM  (SELECT 'condominium' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type ='condominium') as tmp4 UNION ALL\
                                           SELECT * FROM  (SELECT 'modular home' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type ='modular home') as tmp5 UNION ALL\
                                           SELECT * FROM  (SELECT 'tiny house' as household_type, COALESCE(count(*),0) as count_type FROM  Off_grid_household WHERE household_type ='tiny house') as tmp6)\
                    SELECT household_type, ROUND(count_type/(SELECT SUM(count_type) FROM Type_houshold_count)*100,1) as count_percent FROM  Type_houshold_count"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["Household Type","Count %"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_fourth, font=("Sans-serif",10,"bold"), width=25, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_fourth, font=("Sans-serif",10), width=25, justify="center")
                entry.grid(row=i+1,column=j)
                entry.insert(END, r[j])

    def insert_avg_water_tank_size(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"SELECT * FROM (SELECT 'off-the-grid' as type, ROUND(avg(tank_size),1) as avg_size FROM\
                (SELECT W.tank_size FROM WaterHeater as W WHERE W.email NOT IN (SELECT  email FROM PublicUtility))as tmp1) as tmpoff UNION ALL\
                SELECT * FROM (SELECT 'on-the-grid' as type, ROUND(avg(tank_size),1) as avg_size FROM\
                (SELECT W.tank_size FROM WaterHeater as W WHERE W.email IN (SELECT email FROM PublicUtility)) as tmp2) as tmpon"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["Household Type","Average Size"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_fifth, font=("Sans-serif",10,"bold"), width=25, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_fifth, font=("Sans-serif",10), width=25, justify="center")
                entry.grid(row=i+1,column=j)
                val = "" if not r[j] else r[j]
                entry.insert(END, val)

    def insert_btu_info(self):
        # Perform the search query
        conn = dbConn.get_conn()
        cursor = conn.cursor()
        query = f"WITH Off_the_appliance AS(SELECT A.email, A.applianceID, A.BTU FROM  Appliance as A WHERE A.email NOT IN (SELECT email FROM PublicUtility))\
                    SELECT * FROM (SELECT 'WaterHeater' as appliance_type, ROUND(COALESCE(min(BTU),0),0) as min_BTU, ROUND(COALESCE(avg(BTU),0),0) as avg_BTU, ROUND(COALESCE(max(BTU),0),0) as max_BTU FROM\
                     (SELECT  O.BTU FROM WaterHeater as W LEFT JOIN Off_the_appliance as O ON O.email = W.email AND O.applianceID = W.applianceID) as tmp1) as tmpwh UNION ALL\
                SELECT * FROM (SELECT 'AirHandler' as appliance_type, ROUND(COALESCE(min(BTU),0),0) as min_BTU, ROUND(COALESCE(avg(BTU),0),0) as avg_BTU, ROUND(COALESCE(max(BTU),0),0) as max_BTU FROM\
                    (SELECT  O.BTU FROM AirHandler as A LEFT JOIN Off_the_appliance as O ON O.email = A.email AND O.applianceID = A.applianceID) as tmp2) as tmpah UNION ALL\
                SELECT * FROM (SELECT 'AirConditioner' as appliance_type, ROUND(COALESCE(min(BTU),0),0) as min_BTU, ROUND(COALESCE(avg(BTU),0),0) as avg_BTU, ROUND(COALESCE(max(BTU),0),0) as max_BTU FROM\
                (SELECT  O.BTU FROM AirConditioner as A LEFT JOIN Off_the_appliance as O ON O.email = A.email AND O.applianceID = A.applianceID) as tmp3) as tmpac UNION ALL\
                SELECT * FROM (SELECT 'Heater' as appliance_type, ROUND(COALESCE(min(BTU),0),0) as min_BTU, ROUND(COALESCE(avg(BTU),0),0) as avg_BTU, ROUND(COALESCE(max(BTU),0),0) as max_BTU FROM\
                (SELECT  O.BTU FROM Heater as H LEFT JOIN Off_the_appliance as O ON O.email = H.email AND  O.applianceID = H.applianceID) as tmp4) as tmph UNION ALL\
                SELECT * FROM (SELECT 'HeatPump' as appliance_type, ROUND(COALESCE(min(BTU),0),0) as min_BTU, ROUND(COALESCE(avg(BTU),0),0) as avg_BTU, ROUND(COALESCE(max(BTU),0),0) as max_BTU FROM\
                (SELECT  O.BTU FROM HeatPump as H LEFT JOIN Off_the_appliance as O ON O.email = H.email AND O.applianceID = H.applianceID) as tmp5) as tmphp"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # column names
        col_name = ["Appliance Type","Min BTU","Avg BTU","Max BTU"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame_sixth, font=("Sans-serif",10,"bold"), width=25, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame_sixth, font=("Sans-serif",10), width=25, justify="center")
                entry.grid(row=i+1,column=j)
                val = "" if not r[j] else r[j]
                entry.insert(END, val)
