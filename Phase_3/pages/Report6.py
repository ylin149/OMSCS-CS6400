from tkinter import *
import tkinter as tk 
from db_helper import dbConn
from tkinter import messagebox

class Report6(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        label_title = Label(self, text="Household averages by radius", font=("Sans-serif", 30))
        label_title.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # get postal code
        search_label = Label(self, text="Please enter postal code:", font=("Sans-serif", 12))
        search_label.grid(row=1, column=0, sticky='W', padx=10, pady=10)

        self.postal_code_entry = Entry(self, width=50, font=("Sans-serif", 12))
        self.postal_code_entry.config(width=14) 
        self.postal_code_entry.grid(row=1, column=0,  padx=200, pady=10, sticky='W')

        # get radius
        self.radius_list = [0,5,10,25,50,100,250]

        # label of radius
        radius_label = tk.Label(self, text="Please enter search radius:", font=("Sans-serif", 12))
        radius_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        # dropdown field of home type
        self.radius_entry = tk.IntVar()
        self.radius_entry.set(self.radius_list[0])
        radius_choice = tk.OptionMenu(self, self.radius_entry, *self.radius_list)
        radius_choice.config(width=14) 
        radius_choice.grid(row=2, column=0, padx=200, pady=10, sticky="W")

        #search button
        search_button = Button(self, text="Search", command=self.search_button_clicked, font=("Sans-serif", 12, "bold"))
        search_button.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        # Add a resut frame for result table
        self.results_frame = Frame(self)
        self.results_frame.grid(row=4, column=0, sticky='w', padx=10, pady=10)
        
        # return to main page link
        return_main_label = Label(self, text="Return to the main menu", fg="blue", font=("Sans-serif", 15, "underline"))
        return_main_label.grid(row=5, column=0, sticky='w', padx=10, pady=10)
        return_main_label.bind("<Button-1>", lambda event: self.controller.display("MainPage"))

    def search_button_clicked(self):
        # connect to database
        conn = dbConn.get_conn()
        cursor = conn.cursor()

        # Get search input
        postal_code = self.postal_code_entry.get().lower()
        if not postal_code:
            messagebox.showerror("Error", "Please enter a postal code.")
            return
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Location WHERE postal_code = %s)", (postal_code,))
        result = cursor.fetchone()
        if result[0] == 0:
            messagebox.showerror("Error", "Postal code does not exist")
            return 
        radius =self.radius_entry.get()

        # Perform the search query
        query = f"WITH target_latitude AS(SELECT latitude  FROM Location  WHERE postal_code= '{postal_code}'),\
                        target_longitude AS(SELECT longitude  FROM Location  WHERE postal_code= '{postal_code}'),\
                        Location_distance AS(SELECT L.postal_code, L.latitude,L.longitude,3958.75*2*ATAN2(SQRT(POWER(SIN((TLA.latitude-L.latitude)/2),2)+COS(L.latitude)*COS(TLA.latitude)* POWER(SIN((TLO.longitude-L.longitude)/2),2)),SQRT(1-POWER(SIN((TLA.latitude-L.latitude)/2),2)+COS(L.latitude)*COS(TLA.latitude)* POWER(SIN((TLO.longitude-L.longitude)/2),2))) as distance \
                            FROM Location AS L, target_latitude AS TLA, target_longitude AS TLO),\
                        In_radius_household AS(SELECT H.email, H.household_type, H.square_footage, H.heating_setting, H.cooling_setting FROM Household as H LEFT JOIN Location_distance as L ON H.postal_code = L.postal_code WHERE L.distance <= {radius}),\
                        In_radius_household_with_power AS(SELECT H.email, P.generator_type, P. average_monthly_kilowatt_hours_generated, P. battery_storage_capacity_kilowatt_hours FROM Household as H LEFT JOIN Location_distance as L ON H.postal_code = L.postal_code INNER JOIN PowerGenerator as P ON H.email = P.email WHERE L.distance <= {radius}),\
                        In_radius_most_common_power AS(SELECT generator_type FROM In_radius_household_with_power GROUP BY generator_type ORDER BY count(*) DESC LIMIT 1),\
                        In_radius_power_with_battery AS(SELECT email FROM In_radius_household_with_power WHERE battery_storage_capacity_kilowatt_hours IS NOT NULL),\
                        In_radius_household_with_utility AS(SELECT H.email, P.public_utility FROM Household as H LEFT JOIN Location_distance as L ON H.postal_code = L.postal_code LEFT JOIN PublicUtility as P ON H.email = P.email WHERE L.distance <= {radius}),\
                        H as (SELECT '{postal_code}' as postal_code, {radius} as search_radius,COALESCE(count(DISTINCT IRH.email),0) as count_houshold,COALESCE(SUM(IRH.household_type= 'house'),0) as count_house, COALESCE(SUM(IRH.household_type= 'apartment'),0) as count_apartment, COALESCE(SUM(IRH.household_type= 'townhome'),0) as count_townhome,\
                            COALESCE(SUM(IRH.household_type= 'condominium'),0) as count_condominium, COALESCE(SUM(IRH.household_type= 'modular home'),0) as count_modular_home, COALESCE(SUM(IRH.household_type= 'tiny house'),0) as count_tiny_house, ROUND(AVG(IRH.square_footage),0) as avg_footage, ROUND(AVG(IRH.heating_setting),1) as avg_heat_temp,\
                            ROUND(AVG(IRH.cooling_setting),1) as avg_cool_temp from In_radius_household as IRH),\
                        HU as(SELECT GROUP_CONCAT(DISTINCT(IRU.public_utility) SEPARATOR ',') as public_utilities, count(IRU.email)- count(IRU.public_utility) as num_off_grid from In_radius_household_with_utility as IRU),\
                        HP as(SELECT COALESCE(count(DISTINCT IRP.email),0) as count_with_power,ROUND(AVG(IRP.average_monthly_kilowatt_hours_generated),0) as avg_monthly_power from In_radius_household_with_power as IRP),\
                        CP as(SELECT GROUP_CONCAT(DISTINCT(IRCP. generator_type) SEPARATOR '') as most_common_generator_method from In_radius_most_common_power as IRCP),\
                        PB as(SELECT COALESCE(count(DISTINCT IRPB.email),0) as count_with_battery from In_radius_power_with_battery as IRPB)\
                    SELECT * FROM (SELECT 'postal code' as field_name, H.postal_code as field_value FROM H) AS tmp1 UNION ALL\
                    SELECT * FROM (SELECT 'search radius' as field_name, H.search_radius as field_value FROM H) AS tmp2 UNION ALL\
                    SELECT * FROM (SELECT 'household count' as field_name, H.count_houshold as field_value FROM H) AS tmp3 UNION ALL\
                    SELECT * FROM (SELECT 'house count' as field_name, H.count_house as field_value FROM H) AS tmp18 UNION ALL\
                    SELECT * FROM (SELECT 'apartment count' as field_name, H.count_apartment as field_value FROM H) AS tmp4 UNION ALL\
                    SELECT * FROM (SELECT 'townhome count' as field_name, H.count_townhome as field_value FROM H) AS tmp5 UNION ALL\
                    SELECT * FROM (SELECT 'condominium count' as field_name, H.count_condominium as field_value FROM H) AS tmp6 UNION ALL\
                    SELECT * FROM (SELECT 'modular home count' as field_name, H.count_modular_home as field_value FROM H) AS tmp7 UNION ALL\
                    SELECT * FROM (SELECT 'tiny house count' as field_name, H.count_tiny_house as field_value FROM H) AS tmp8 UNION ALL\
                    SELECT * FROM (SELECT 'average footage' as field_name, H.avg_footage as field_value FROM H) AS tmp9 UNION ALL\
                    SELECT * FROM (SELECT 'average heat temperature' as field_name, H.avg_heat_temp as field_value FROM H) AS tmp10 UNION ALL\
                    SELECT * FROM (SELECT 'average cool temperature' as field_name, H.avg_cool_temp as field_value FROM H) AS tmp11 UNION ALL\
                    SELECT * FROM (SELECT 'public utilities' as field_name, HU.public_utilities as field_value FROM HU) AS tmp12 UNION ALL\
                    SELECT * FROM (SELECT 'num off-the-grid' as field_name, HU.num_off_grid as field_value FROM HU) AS tmp13 UNION ALL\
                    SELECT * FROM (SELECT 'count with power generation' as field_name, HP.count_with_power as field_value FROM HP) AS tmp14 UNION ALL\
                    SELECT * FROM (SELECT 'most common generation method' as field_name, CP.most_common_generator_method as field_value FROM CP) AS tmp15 UNION ALL\
                    SELECT * FROM (SELECT 'avg monthly power generation' as field_name, HP.avg_monthly_power as field_value FROM HP) AS tmp16 UNION ALL\
                    SELECT * FROM (SELECT 'count with battery storage' as field_name, PB.count_with_battery as field_value FROM PB) AS tmp17"
        cursor.execute(query)
        results = cursor.fetchall()

        # column names
        col_name = ["Field Name","Field Value"]
        for j, col in enumerate(col_name):
            entry = Entry(self.results_frame, font=("Sans-serif",12,"bold"), width=35, justify="center")
            entry.grid(row=0,column=j)
            entry.insert(END,col)

        # insert result
        for i, r in enumerate(results):
            for j in range(len(r)):
                entry = Entry(self.results_frame, font=("Sans-serif",12), width=35, justify="center")
                entry.grid(row=i+1,column=j)
                val = "" if not r[j] else r[j]
                entry.insert(END, val)

        cursor.close()