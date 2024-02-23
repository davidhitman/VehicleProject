import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from tkinter import font

class Manager:
    def __init__(self, root):
        self.rental_history = []  # List to store rental data
        self.conn = sqlite3.connect("nextbike.db")

        self.root = root
        self.root.title("Manager")
        self.root.geometry("600x600")

        self.button_position = {
            1: (1, 1), 2: (1, 2), 3: (1, 3)
        }

        self.display_frame = self.create_display_frame()
        self.button_frame = self.create_button_frame()

        custom_font1 = font.nametofont("TkDefaultFont")
        custom_font1.configure(family="Arial", size=32)

        custom_font2 = font.nametofont("TkDefaultFont")
        custom_font2.configure(family="Arial", size=16)
        self.display_title = tk.Label(self.display_frame, text='Manager Dashboard', font=custom_font1).pack(anchor='center')

        for i in range(1, 4):
            self.button_frame.rowconfigure(i, weight=1)
            self.button_frame.columnconfigure(i, weight=1)

        button1 = tk.Button(self.button_frame, text='Most bikes available', borderwidth=0, font=custom_font2, command=self.plot_data_bikes)
        button1.grid(row=1, column=1, sticky=tk.NSEW)
        button2 = tk.Button(self.button_frame, text='Most docks available', borderwidth=0, font=custom_font2, command=self.plot_data_docks)
        button2.grid(row=1, column=2, sticky=tk.NSEW)
        button3 = tk.Button(self.button_frame, text='Most used station', borderwidth=0, font=custom_font2, command=self.plot_data_most_used)
        button3.grid(row=1, column=3, sticky=tk.NSEW)

    def plot_data_bikes(self):
        plot_window = tk.Tk()
        ffr = tk.Frame(plot_window)
        ffr.pack()
        data_to_plot = pd.DataFrame(self.fetch_data("""SELECT stations.name, station_status.num_bikes_available
                                               FROM stations JOIN station_status 
                                               ON stations.station_id = station_status.station_id 
                                               ORDER BY station_status.num_bikes_available 
                                               DESC LIMIT 10;"""))

        x, y = data_to_plot['name'], data_to_plot['num_bikes_available']
        fig, ax = plt.subplots()
        ax.set_title("Stations with most available bikes")
        ax.bar(x, y)
        fig.autofmt_xdate(rotation=45)
        fig.set_size_inches(5, 3)
        canvas = FigureCanvasTkAgg(fig, master=ffr)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        plot_window.mainloop()

    def plot_data_most_used(self):
        plot_window = tk.Tk()
        ffr = tk.Frame(plot_window)
        ffr.pack()
        data_to_plot = pd.DataFrame(self.fetch_data("""SELECT s.name AS most_used_station_name, r.station_from AS most_used_station_id, COUNT(*) AS rental_count
                                                    FROM bike_in_use AS r
                                                    JOIN stations AS s
                                                    ON r.station_from = s.station_id
                                                    GROUP BY r.station_from, s.name
                                                    ORDER BY rental_count DESC
                                                    LIMIT 3;"""))

        x, y = data_to_plot['most_used_station_name'], data_to_plot['rental_count']
        fig, ax = plt.subplots()
        ax.set_title("Stations with most used station")
        ax.bar(x, y)
        fig.autofmt_xdate(rotation=45)
        fig.set_size_inches(5, 3)
        canvas = FigureCanvasTkAgg(fig, master=ffr)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        plot_window.mainloop()

    def plot_data_docks(self):
        plot_window = tk.Tk()
        ffr = tk.Frame(plot_window)
        ffr.pack()
        data_to_plot = pd.DataFrame(self.fetch_data("""SELECT stations.name, station_status.num_docks_available
                                               FROM stations JOIN station_status 
                                               ON stations.station_id = station_status.station_id 
                                               ORDER BY station_status.num_docks_available 
                                               DESC LIMIT 10;"""))

        x, y = data_to_plot['name'], data_to_plot['num_docks_available']
        fig, ax = plt.subplots()
        ax.set_title("Stations with most available docks")
        ax.bar(x, y)
        fig.autofmt_xdate(rotation=45)
        fig.set_size_inches(5, 3)
        canvas = FigureCanvasTkAgg(fig, master=ffr)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        plot_window.mainloop()

    def create_display_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')

        return frame

    def create_button_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')
        return frame

    def run(self):
        self.root.mainloop()

    def fetch_data(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data

# if __name__ == "__main__":
#     root = tk.Tk()
#     manager = Manager(root)
#     manager.run()
