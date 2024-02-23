import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import sqlite3
from tkinter import ttk
from sqlite3 import Error
windowWidth = 380
windowHeight = 580
jumpPageWidth = 380
jumpPageHeight = 500
popUpWidth = 250
popUpHeight = 100
formBackgroundColour = "#35608f"
headerBackgroundColour = "#000000"

try:
    connection = sqlite3.connect("nextbike.db")
    cursor = connection.cursor()
except sqlite3.Error as error:
    print("Error while connecting to SQLite:", error)


class operator:
    def __init__(self, root):
        self.root = root
        self.root.title("Operator")
        self.mainFrame = tk.Frame(self.root, width=windowWidth, height=windowHeight)
        self.createOperatorPage()
        self.frames = {}

    def createOperatorPage(self):
        self.headerFrame = tk.Frame(self.mainFrame, bg=headerBackgroundColour, width=windowWidth, height=50)
        self.titleFrame = tk.Frame(self.headerFrame, padx=1, pady=1)
        self.labelTitle = tk.Label(self.titleFrame, text="Operator", font=('verdana', 20), width=7, fg='#fff', padx=20, pady=5,
                                   bg='red')

        self.headerFrame.pack()
        self.titleFrame.pack()
        self.labelTitle.pack()

        self.titleFrame.place(y=26, relx=0.5, anchor=CENTER)

        self.operatorFrame = tk.Frame(self.mainFrame, width=windowWidth, height=windowHeight)
        self.operatorPageFrame = tk.Frame(self.operatorFrame, padx=30, pady=100, bg=formBackgroundColour)

        self.buttonFrame = tk.Frame(self.operatorPageFrame)
        # self.emptyLabel = tk.Label(self.buttonFrame, text="")
        self.operatorTrackButton = tk.Button(self.buttonFrame, text="Track", font=('verdana', 12),
                                              highlightbackground=formBackgroundColour, command=self.goToTrackVehicle)
        self.operatorChargeButton = tk.Button(self.buttonFrame, text="Charge Vehicle", font=('verdana', 12),
                                               highlightbackground=formBackgroundColour, command=self.goToChargeVehicle)
        self.operatorRepairButton = tk.Button(self.buttonFrame, text="Repair", font=('verdana', 12),
                                              highlightbackground=formBackgroundColour, command=self.goToRepairWindow)
        self.operatorMoveVehicle = tk.Button(self.buttonFrame, text="Move Vehicle", font=('verdana', 12),
                                             highlightbackground=formBackgroundColour, command=self.goToMoreVehicleWindow)

        self.mainFrame.pack(fill='both', expand=1)
        self.operatorFrame.pack(fill='both', expand=1)
        self.operatorPageFrame.pack(fill='both', expand=1)

        self.buttonFrame.grid(row=0, column=0, pady=5)

        self.operatorTrackButton.grid(row=0, column=2, pady=5,padx=10, sticky='nsew')
        self.operatorChargeButton.grid(row=1, column=2, pady=5,padx=10, sticky='nsew')
        self.operatorRepairButton.grid(row=2, column=2, pady=5,padx=10, sticky='nsew')
        self.operatorMoveVehicle.grid(row=3, column=2, pady=5,padx=10, sticky='nsew')

        self.buttonFrame.pack(fill='both', expand=1)

    def displayErrorMessage(self):
        errorWindow = tk.Toplevel(self.root, bg=formBackgroundColour)
        errorWindow.title("Error")
        labelError = tk.Label(errorWindow, text="There is an error please try again", font=('verdana', 12),
                              bg=formBackgroundColour)
        labelError.pack(padx=20, pady=10)
        buttonOkay = tk.Button(errorWindow, text="Okay", font=('verdana', 12), highlightbackground=formBackgroundColour,
                              command=errorWindow.destroy)
        buttonOkay.pack(pady=5)
        self.operatorPageFrame.focus_set()

        self.mainFrame.pack_propagate(FALSE)

    def goToRepairWindow(self):
        repairWindowPage = tk.Toplevel(self.root)
        newRepairWindowPage = repair(repairWindowPage, self.root)
        newRepairWindowPage.createRepairPage()
        return "fetch successful"

    def goToMoreVehicleWindow(self):
        moreVehiclePage = tk.Toplevel(self.root)
        newMoreVehiclePage = moreVehicle(moreVehiclePage, self.root)
        newMoreVehiclePage.createMoreVehiclePage()
        return "fetch successful"

    def goToTrackVehicle(self):
        trackVehiclePage = tk.Toplevel(self.root)
        newTrackVehiclePage = trackVehicle(trackVehiclePage, self.root)
        newTrackVehiclePage.createTrackVehicle()
        return "fetch successful"
    def goToChargeVehicle(self):
        chargeVehiclePage = tk.Toplevel(self.root)
        newchargeVehiclePage = chargeVehicle(chargeVehiclePage, self.root)
        newchargeVehiclePage.createChargeVehicle()
        return "fetch successful"


class trackVehicle(tk.Frame):
    def __init__(self, root, repairRoot):
        self.root = root
        self.repairRoot = repairRoot
        self.root.title("Track Vehicle")

    def createTrackVehicle(self):
        self.root.geometry(f"{jumpPageWidth}x{jumpPageHeight}")
        self.mainFrame = tk.Frame(self.root, bg=formBackgroundColour, width=jumpPageWidth, height=jumpPageHeight)
        self.mainFrame.pack(fill='both', expand=1)
        self.display_title = tk.Label(self.mainFrame, text='Manager Dashboard', font=custom_font1).pack(anchor='center')
        self.buttonFrame = tk.Frame(self.mainFrame, bg=formBackgroundColour)
        self.freeBike = tk.Button(self.buttonFrame, text="Free Bikes Tracking", font=('verdana', 12),
                                  highlightbackground=formBackgroundColour, command=self.displayFreeBike)
        self.freeBike.grid(row=5, column=4, pady=5, sticky='nsew')
        self.bikeInUse = tk.Button(self.buttonFrame, text="Bike in Use", font=('verdana', 12),
                                  highlightbackground=formBackgroundColour, command=self.displayBikeInUse)
        self.bikeInUse.grid(row=8, column=8, pady=5,padx=50)
        self.buttonFrame.grid(row=0, column=5, pady=5)
        self.buttonFrame.pack(fill='both', expand=1)

    def displayBikeInUse(self):
        self.popup_window = tk.Toplevel(self.root)
        self.popup_window.title("Database Records")

        cursor.execute("SELECT * FROM bike_in_use")  # Replace with your table name
        records = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        self.tree = ttk.Treeview(self.popup_window, columns=column_names, show='headings')
        self.tree.pack(fill='both', expand=1, padx=10, pady=10)

        for i in column_names:
            self.tree.column(i, anchor='c', width=200)
            self.tree.heading(i, text=i)

        for row in records:
            self.tree.insert("", 'end', values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    def displayFreeBike(self):
        self.popup_window = tk.Toplevel(self.root)
        self.popup_window.title("Database Records")

        cursor.execute("SELECT bike_id, is_reserved, is_disabled, lat, lon, vehicle_type_id, station_id FROM free_bike")  # Replace with your table name
        records = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        self.tree = ttk.Treeview(self.popup_window, columns=column_names, show='headings')
        self.tree.pack(fill='both', expand=1, padx=10, pady=10)

        for i in column_names:
            self.tree.column(i, anchor='c', width=200)
            self.tree.heading(i, text=i)

        for row in records:
            self.tree.insert("", 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    

class repair(tk.Frame):
    def __init__(self, root, repairRoot):
        self.root = root
        self.repairRoot = repairRoot
        self.root.title("Repair Vehicle")
        # self.createRepairPage()




    def createRepairPage(self):
        self.root.geometry(f"{jumpPageWidth}x{jumpPageHeight}")
        self.mainFrame = tk.Frame(self.root, bg=formBackgroundColour, width=jumpPageWidth, height=jumpPageHeight)
        self.mainFrame.pack(fill='both', expand=1)

        query = "SELECT vehicle_type_id, is_disabled, station_id FROM free_bike WHERE is_disabled = 1"
        cursor.execute(query)
        repairRecords = cursor.fetchall()
        column_names = ["vehicle_type_id", "is_disabled", "station_id"]

        self.tree = ttk.Treeview(self.mainFrame, columns=column_names, show='headings')
        self.tree.pack(fill='both', expand=1)

        for i in column_names:
            self.tree.column(i, anchor='c', width=100)
            self.tree.heading(i, text=i)

        for row in repairRecords:
            self.tree.insert("", 'end', values=(row[0], row[1], row[2]))

        update_button = tk.Button(self.mainFrame, text="Update Selected", command=self.update_is_disabled)
        update_button.pack()

    def update_is_disabled(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            item_values = self.tree.item(item, 'values')
            vehicle_type_id = item_values[0]
            update_query = "UPDATE free_bike SET is_disabled = 0 WHERE vehicle_type_id = ?"
            cursor.execute(update_query, (vehicle_type_id,))
            connection.commit()
            self.tree.delete(item)



class chargeVehicle(tk.Frame):
    def __init__(self, root, chargeVehicle):
        self.root = root
        self.chargeVehicle = chargeVehicle
        self.root.title("Repair Vehicle")

    def assignBatteryCount(self):
        cursor.execute("SELECT user_id FROM user_details WHERE role_type = 'Operator'")
        operator_ids = cursor.fetchall()

        battery_counts = [5, 10, 7]  # You can modify this list as needed

        for operator_id in operator_ids:
            battery_count = battery_counts.pop(0) if battery_counts else 0
            cursor.execute("INSERT INTO charge_vehicle (operator, battery_count) VALUES (?, ?)", (operator_id[0], battery_count))


    def createChargeVehicle(self):
        self.root.geometry(f"{jumpPageWidth}x{jumpPageHeight}")
        self.mainFrame = tk.Frame(self.root, bg=formBackgroundColour, width=jumpPageWidth, height=jumpPageHeight)
        self.mainFrame.pack(fill='both', expand=1)

        query = "SELECT vehicle_type_id, is_disabled, station_id FROM free_bike WHERE is_disabled = 1"
        cursor.execute(query)
        chargeVeh = cursor.fetchall()
        column_names = ["vehicle_type_id", "is_disabled", "station_id"]

        self.tree = ttk.Treeview(self.mainFrame, columns=column_names, show='headings')
        self.tree.pack(fill='both', expand=1)

        for i in column_names:
            self.tree.column(i, anchor='c', width=100)
            self.tree.heading(i, text=i)

        for row in chargeVeh:
            self.tree.insert("", 'end', values=(row[0], row[1], row[2]))

        # Add an "Update Selected" button to trigger the update process
        update_button = tk.Button(self.mainFrame, text="Update Selected", command=self.update_is_disabled)
        update_button.pack()

    def update_is_disabled(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            item_values = self.tree.item(item, 'values')
            vehicle_type_id = item_values[0]
            update_query = "UPDATE free_bike SET is_disabled = 0 WHERE vehicle_type_id = ?"
            cursor.execute(update_query, (vehicle_type_id,))
            connection.commit()
            self.tree.delete(item)

        



class moreVehicle(tk.Frame):
    def __init__(self, root, VehicleTransferApp):
        self.root = root
        self.VehicleTransferApp = VehicleTransferApp
        self.root.title('Vehicle Transfer App')
        self.createMoreVehiclePage()

    def createMoreVehiclePage(self):
        self.initiate_button = tk.Button(self.root, text="Initiate Transfers", command=self.initiate_transfers)
        self.initiate_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

        self.tree = ttk.Treeview(self.root, columns=("Station Name", "Capacity", "Available Bikes"), show='headings')
        self.tree.heading("#1", text="Station Name")
        self.tree.heading("#2", text="Capacity")
        self.tree.heading("#3", text="Available Bikes")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_station_data()  # Initial load

    def load_station_data(self):
        self.tree.delete(*self.tree.get_children())  # Clear the existing data

        cursor.execute("""
            SELECT s.name AS "Station Name", s.capacity AS "Capacity", ss.num_bikes_available AS "Available Bikes"
            FROM stations AS s
            JOIN station_status AS ss ON s.station_id = ss.station_id
        """)
        station_data = cursor.fetchall()

        for row in station_data:
            self.tree.insert("", "end", values=row)

    def initiate_transfers(self):
        try:
            cursor.execute("""
                UPDATE station_status
                SET num_bikes_available = (
                    CASE
                        WHEN station_status.station_id = st.from_station_id THEN
                            CASE
                                WHEN (station_status.num_bikes_available - st.num_bikes_to_transfer) >= 0 THEN
                                    (station_status.num_bikes_available - st.num_bikes_to_transfer)
                                ELSE 0
                            END
                        WHEN station_status.station_id = st.to_station_id THEN
                            (station_status.num_bikes_available + st.num_bikes_to_transfer)
                        ELSE station_status.num_bikes_available
                    END
                )
                FROM (
                    SELECT e.station_id AS from_station_id, b.station_id AS to_station_id, e.num_bikes_available AS num_bikes_to_transfer
                    FROM (
                        SELECT ss.station_id, s.capacity, ss.num_bikes_available
                        FROM stations AS s
                        JOIN station_status AS ss ON s.station_id = ss.station_id
                        WHERE (ss.num_bikes_available > s.capacity)
                    ) AS e
                    CROSS JOIN (
                        SELECT ss.station_id, ss.num_bikes_available
                        FROM station_status AS ss
                        WHERE ss.num_bikes_available < 5
                    ) AS b
                ) AS st
                WHERE station_status.station_id = st.from_station_id OR station_status.station_id = st.to_station_id;
            """)
            cursor.connection.commit()
            self.status_label.config(text="Vehicle transfers initiated.")

            # Reload the table with updated data
            self.load_station_data()
        except (Exception, Error) as error:
            print("Error while transferring vehicles:", error)
def main():
    window = tk.Tk()
    window.columnconfigure(2,{'minsize':20})
    operator(window)
    window.mainloop()

if __name__ == '__main__':
    main()



