import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
import random
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
import os
from wallet_page import WalletPage
windowWidth=380
windowHeight=580
formBackgroundColour="#35608f"
headerBackgroundColour="#000000"
current_directory = os.path.dirname(__file__)
db_connection_string = "nextbike.db"
connection = sqlite3.connect(db_connection_string)
cursor = connection.cursor()


class ChooseVehicle:
    def __init__(self, root, userID):
        self.root = root
        self.userID = userID
        self.db_connection_string = "nextbike.db"
        self.connection = sqlite3.connect(self.db_connection_string)
        self.cursor = self.connection.cursor()
        self.root.title("Choose Vehicle")
        self.root.geometry("600x600")

        self.radio_var = tk.StringVar()
        self.headerFrame = tk.Frame(self.root)
        self.headerFrame.pack()
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack()
        self.footerFrame = tk.Frame(self.root)
        self.footerFrame.pack(pady=30)
        self.lastFrame = tk.Frame(self.root)
        self.lastFrame.pack()

        self.entry = tk.Entry(self.footerFrame)
        self.entry.grid(row=0, column=1)
        self.errorLabel = tk.Label(self.lastFrame, text="", fg="red")
        self.errorLabel.grid(row=4, column=0)

    def checkValuesOfChooseVehicle(self):
        self.selected_option = self.radio_var.get()
        if self.selected_option == "":
            self.errorLabel.configure(text="No option selected.")
        else:
            if len(self.entry.get()) == 0:
                self.errorLabel.configure(text="Please Enter The Time You Would Like To Rent")
            else:
                try:
                    self.time = int(self.entry.get())
                    if self.time < 30:
                        self.errorLabel.configure(text="Minimum Time To Rent Is 30 Minutes")
                    else:
                        self.choosePickUpLocation()
                except:
                    self.errorLabel.configure(text="The Time Has To Be An Integer")

    def searchLocation(self):
        entry_text = self.entry1.get()
        self.search_query = entry_text.lower()
        query = """SELECT name FROM stations WHERE name Like ?"""
        self.cursor.execute(query, ('%' + self.search_query + '%',))
        results = self.cursor.fetchall()
        self.listbox.delete(0, tk.END)
        for item in results:
            self.listbox.insert(tk.END, item[0])

    def on_select(self, event):
        self.selected_field = self.listbox.get(self.listbox.curselection())
        self.selected_field_label.config(text=f"Selected Field: {self.selected_field}")

    def choosePickUpLocation(self):
        self.headerFrame.destroy()
        self.mainFrame.destroy()
        self.footerFrame.destroy()
        self.lastFrame.destroy()

        self.mainFrame1 = tk.Frame(self.root)
        self.mainFrame1.pack()

        self.frame1 = tk.Frame(self.mainFrame1, pady=30)
        self.frame1.pack()

        self.frame2 = tk.Frame(self.mainFrame1)
        self.frame2.pack()

        self.label1 = tk.Label(self.frame1, text="Enter Your Current Address or preferred pickup address", pady=5)
        self.label1.pack()

        self.entry1 = tk.Entry(self.frame1)
        self.entry1.pack(pady=10)
        self.searchButton = tk.Button(self.frame1, text="Search", command=self.searchLocation)
        self.searchButton.pack()

        self.listbox = tk.Listbox(self.frame2, height=18, width=50)
        self.listbox.pack()
        self.selected_field_label = tk.Label(self.frame2, text="Selected Field:")
        self.selected_field_label.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.bookButton = tk.Button(self.frame2, text="Start Trip", padx=60, pady=10, command= self.writeData)
        self.start_time = datetime.now()
        self.bookButton.pack(pady=20)



    # def open_wallet(self):
    #     subprocess.call(['python', '/Users/dhananjaygupta/Documents/Developer/ProgrammingSystem/TeamPRoject/ProgrammingSystemProject/evehicleproject/src/wallet_page.py'])

    def writeData(self):
       
        # print(self.selected_filed)
        self.station_name = self.selected_field

        # Step 1: Get the station_id for the given station_name
        cursor.execute("SELECT station_id FROM stations WHERE name = ?", (self.station_name,))
        self.station_id = cursor.fetchone()[0]
        print(self.station_id)

        # Step 2: Retrieve a random bike_id from free_bike for the specified station_id
        cursor.execute("SELECT bike_id, vehicle_type_id FROM free_bike WHERE station_id = ?", (self.station_id,))
        available_bikes = cursor.fetchall()
        if available_bikes:
            self.random_bike = random.choice(available_bikes)[0]
            print(self.random_bike)
            self.result = [item[1] for item in available_bikes if item[0] == self.random_bike]

            # Step 3: Insert station_id and bike_id into bike_in_use
            current_time = datetime.now()
            cursor.execute("INSERT INTO bike_in_use (user_id, bike_id, station_from, station_to, start_time, end_time, duration) VALUES (?, ?, ?, NULL, ?, NULL, NULL)", (self.userID, self.random_bike, self.station_id, current_time))

            # Step 4: Update station_status to reduce num_bike_available
            cursor.execute("UPDATE station_status SET num_bikes_available = num_bikes_available - 1 WHERE station_id = ?", (self.station_id,))

            # Step 5: Remove the bike from free_bike
            cursor.execute("DELETE FROM free_bike WHERE station_id = ? AND bike_id = ?", (self.station_id, self.random_bike))

            # Commit the changes
            connection.commit()
            print(f"Bike {self.random_bike} is now in use at station {self.station_id}.")
            self.getToReportPage()
            # self.random_bike.append(random_bike)
    def getToReportPage(self):
        self.root.withdraw()
        reportPageroot = tk.Toplevel(self.root)
        reportPageroot = ReportPage(reportPageroot, self.selected_field, self.userID, self.start_time,self.random_bike,self.result,self.station_id)

    def openWallet(self):
        
        walletPageWindow = tk.Toplevel(self.root)
        newwalletPageWindow = WalletPage(walletPageWindow)
        newwalletPageWindow.run()


    def run(self):
        walletButton = tk.Button(self.headerFrame,text='Wallet', command=self.openWallet)
        walletButton.grid(row=0,column=0,sticky='w')

        header = tk.Label(self.headerFrame, text="Please Select The Vehicle You Would Like To Rent")
        header.config(padx=120, pady=30, font=('Helvetica', 18, 'bold'))
        header.grid(row=1, column=0)

        frame1 = tk.Frame(self.mainFrame, highlightbackground="black", highlightthickness=1, width=200, height=200)
        frame1.grid(row=0, column=0)

        frame2 = tk.Frame(self.mainFrame, highlightbackground="black", highlightthickness=1, width=200, height=250)
        frame2.grid(row=0, column=1, padx=40)

        bikeHeader = tk.Label(frame1, text="Electric Bicycle")
        bikeHeader.pack()

        scooterHeader = tk.Label(frame2, text="Electric Scooter")
        scooterHeader.pack()


        relative_path_cycle = "photos/cycle.jpg"
        image_path_cycle = os.path.join(current_directory, relative_path_cycle)


        bikeImg = Image.open(image_path_cycle)
        resized_bikeImage = bikeImg.resize((200, 200), Image.LANCZOS)
        new_bikeImage = ImageTk.PhotoImage(resized_bikeImage)

        bikeLabel = tk.Label(frame1, image=new_bikeImage)
        bikeLabel.pack(expand=True, fill=tk.BOTH)

        bikeLabel.bind("<Button-1>", lambda e:
        print("Bike")) 

        relative_path_scooter = "photos/Scooter.jpg"
        image_path_scooter = os.path.join(current_directory, relative_path_scooter)
        scooterImg = Image.open(image_path_scooter)
        resized_scooterImage = scooterImg.resize((200, 200), Image.LANCZOS)
        new_scooterImage = ImageTk.PhotoImage(resized_scooterImage)

        scooterLabel = tk.Label(frame2, image=new_scooterImage)
        scooterLabel.pack(expand=True, fill=tk.BOTH)

        bikeRadioButton = tk.Radiobutton(frame1, variable=self.radio_var, value="Bicycle")
        bikeRadioButton.pack()

        scooterRadioButton = tk.Radiobutton(frame2, variable=self.radio_var, value="Scooter")
        scooterRadioButton.pack()

        label1 = tk.Label(self.footerFrame, text="How Long You Want To Rent The Vehicle:")
        label1.grid(row=0, column=0)

        label2 = tk.Label(self.lastFrame, text="*Enter Time in Minutes*", fg="red", padx=30)
        label2.grid(row=1, column=0)

        label3 = tk.Label(self.lastFrame, text="*The minimum time you can rent a vehicle is 30 minutes*", fg="red", padx=30)
        label3.grid(row=2, column=0)

        button = tk.Button(self.lastFrame, text="Next", command=self.checkValuesOfChooseVehicle, padx=50, pady=10)
        button.grid(row=3, column=0, pady=10)
        self.root.mainloop()

class ReportPage:
    
    def __init__(self, root, selected_filed, userID, start_time,random_bike,result,station_id):
        self.root = root
        self.selected_filed = selected_filed
        self.userID = userID
        self.start_time = start_time
        self.random_bike = random_bike
        self.result = result
        self.station_id = station_id
        self.root.title("Report Page")
        self.mainFrame = tk.Frame(self.root, width=windowWidth, height=windowHeight)
        self.createReportPage()
        self.random_bike = []

    def createReportPage(self):
        self.headerFrame = tk.Frame(self.mainFrame, bg=headerBackgroundColour, width=windowWidth, height=50)
        self.titleFrame = tk.Frame(self.headerFrame, padx=1, pady=1)
        self.labelTitle = tk.Label(self.titleFrame, text="Ongoing Ride", font=('verdana', 20), width=7, fg='#fff', padx=20, pady=5,
                                   bg='red')
        self.headerFrame.pack()
        self.titleFrame.pack()
        self.labelTitle.pack()
        self.titleFrame.place(y=26, relx=0.5, anchor=tk.CENTER)
        self.stopFrame = tk.Frame(self.mainFrame, width=windowWidth, height=windowHeight)
        self.reportFrame = tk.Frame(self.mainFrame, width=windowWidth, height=windowHeight)
        self.stopLabel = tk.Label(self.stopFrame, text="End Ride", font=('verdana', 20))
        self.stopButton = tk.Button(self.stopFrame, text='Stop', command=self.upateBikeInUse)
        self.reportLabel = tk.Label(self.reportFrame, text="Report Problem", font=('verdana', 20))
        # self.securityQuestionVar = tk.StringVar(value=self.securityQuestions[0][1])
        self.reportProblemMenu = ttk.Combobox(self.reportFrame,
                                              values=["Bike Availability", "Bike Condition", "Battery Level",
                                                      "Charging Infrastructure", "App or Kiosk Issues",
                                                      "User Authentication", "Inaccurate Location Data", "Rider Safety", ],
                                              state="readonly")
        self.confirmationbutton = tk.Button(self.reportFrame, text="Report the issue", font=('verdana', 12),
                                            highlightbackground=formBackgroundColour, command=self.getReport)
        self.stopButton.grid(row=1, column=6, pady=50, padx=50, columnspan=2, sticky='e')
        self.reportLabel.grid(row=0, column=0, columnspan=2)
        self.reportProblemMenu.grid(row=1, column=0, padx=10, pady=10)
        self.confirmationbutton.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        self.mainFrame.pack(fill='both', expand=1)
        self.stopFrame.pack(fill='both', expand=1)
        self.reportFrame.pack(fill='both', expand=1)
        self.mainFrame.pack_propagate(False)
        self.root.mainloop()
            
    # def random_bike_data(bike_data):
    #     return bike_data
        

    def upateBikeInUse(self):
        try:
            
            # Step 1: Extract a random station_id from the stations table
            cursor.execute("SELECT station_id FROM stations ORDER BY RANDOM() LIMIT 1;")
            random_station_id = cursor.fetchone()[0]

            # Step 2: Update the bike_in_use table with station_id and end_time
            self.end_time = datetime.now()
            self.duration = (self.end_time - self.start_time).total_seconds() / 60
            update_query = "UPDATE bike_in_use SET station_to = ?, end_time = ?, duration = ? WHERE bike_id = ? AND station_from = ?;"
            cursor.execute(update_query, (random_station_id, self.end_time, self.duration, self.random_bike, self.station_id))

            # Step 3: Insert a record into the free_bike table
            insert_query = "INSERT INTO free_bike (bike_id, is_reserved, is_disabled, vehicle_type_id, station_id) VALUES (?, 0, 0, ?, ?);"
            cursor.execute(insert_query, (self.random_bike, str(self.result), random_station_id))

            # Commit the changes
            connection.commit()
            self.choose()

        except Exception as error:
            # Handle any exceptions or errors here
            print("Error print:", error)
            connection.rollback()

    def choose(self):
        self.root.withdraw()
        chooseVehiclePage = tk.Toplevel(self.root)
        cv = ChooseVehicle(chooseVehiclePage, self.userID)
        cv.run()

    def getReport(self):
        try:
            get_data = self.reportProblemMenu
            specific_bike_id = self.random_bike
            self.end_time = datetime.now()
            update_query = f"UPDATE bike_in_use SET end_time = ? WHERE bike_id = ?;"
            cursor.execute(update_query, (self.end_time, specific_bike_id))
            insert_query = "INSERT INTO free_bike (bike_id, is_disabled) VALUES (?, ?);"
            cursor.execute(insert_query, (specific_bike_id, 1))
            connection.commit()
        except (Exception, sqlite3.Error) as error:
            print("Error:", error)
            connection.rollback()

# if __name__ == "__main__":
#     root = tk.Tk()
#     cv = ChooseVehicle(root, '2da70bc4-b9ba-4665-b465-9f6ae814dc4e')
#     cv.run()
#     root.mainloop()
