from tkinter import *
from tkinter import messagebox
import customtkinter

import os
from PIL import Image

import cpuinfo
import platform
import psutil
import tabulate

import sqlite3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages

from datetime import datetime

connection = sqlite3.connect("test.db")
cursor=connection.cursor()

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sidebar_title = customtkinter.CTkLabel(self, text="Resource Monitor",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebar_title.grid(row=0, column=0, padx=20, pady=10)


class RtdFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((1,2,3), weight=1)


class InfoFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.CPUplatformLabel = customtkinter.CTkLabel(self, text=f'Platform: {platform.processor()}',
                                                       font=customtkinter.CTkFont(size=20))
        self.CPUplatformLabel.grid(row=0, column=0, padx=20, pady=10)

        self.CPUnameLabel = customtkinter.CTkLabel(self,
                                                   text=f'Name: {cpuinfo.get_cpu_info()["brand_raw"].split("6-Core")[0]}',
                                                   font=customtkinter.CTkFont(size=20))
        self.CPUnameLabel.grid(row=1, column=0, padx=20, pady=10)

        self.CPUcores = customtkinter.CTkLabel(self, text=cpuinfo.get_cpu_info()["brand_raw"].split("5600X ")[1],
                                               font=customtkinter.CTkFont(size=20))
        self.CPUcores.grid(row=2, column=0, padx=20, pady=10)

        self.CPU_freq = str(psutil.cpu_freq().current) + "MHz"
        self.CPUfreqLabel = customtkinter.CTkLabel(self, text=f'Nominal Frequency: {self.CPU_freq}', padx=10,
                                                   pady=5,
                                                   font=customtkinter.CTkFont(size=20))
        self.CPUfreqLabel.grid(row=3, column=0, padx=20, pady=10)

class DiskUsageFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.disk_partition_info = customtkinter.CTkTextbox(self, width=290, height=90)
        self.disk_partition_info.grid(row=0, column=0, padx=20, pady=10)
        self.disk_partition_info.insert("0.0", text=self.display_all_partitions())
        self.disk_partition_info.configure(state="disabled")


    def get_partition_names(self):
        self.data = psutil.disk_partitions()
        return [i.device for i in self.data]

    def disk_info(self, device_name):
        disk_info = {}
        usage = psutil.disk_usage(device_name)
        disk_info['Device'] = device_name
        disk_info['Total'] = f"{self.byteToGigabyte(usage.total)} GB"
        disk_info['Used'] = f"{self.byteToGigabyte(usage.used)} GB"
        disk_info['Free'] = f"{self.byteToGigabyte(usage.free)} GB"
        disk_info['Percent'] = f"{usage.percent} %"
        return disk_info

    def byteToGigabyte(self, bytes):
        return '{0:.2f}'.format(bytes / 1000000000)

    def display_all_partitions(self):
        info = []

        for i in self.get_partition_names():
            info.append(self.disk_info(i))

        info_values = [i.values() for i in info]
        info_tabulated = tabulate.tabulate(info_values, headers=info[0].keys())
        return info_tabulated

class CircularFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def displayCPU(self):
        self.CPUusageLabel = customtkinter.CTkLabel(self, text="",
                                                    font=customtkinter.CTkFont(size=20),
                                                    )
        self.CPUusageLabel.grid(row=0, column=0, padx=20, pady=10)
        self.updateCPUUsage()

    def displayRAM(self):
        self.RAMlabel = customtkinter.CTkLabel(self, text="", padx=10, pady=5,
                                               font=customtkinter.CTkFont(size=20))
        self.RAMlabel.grid(row=0, column=1, padx=20, pady=10)
        self.updateRAMusage()

    def byteToGigabyte(self, bytes):
        return '{0:.2f}'.format(bytes / 1000000000)

    def updateCPUUsage(self):
        usage = str(psutil.cpu_percent()) + "%"
        self.CPUusageLabel.configure(text="CPU usage: " + usage)
        self.CPUusageLabel.after(1000, self.updateCPUUsage)

    def updateRAMusage(self):
        used = str(self.byteToGigabyte(psutil.virtual_memory().used)) + "GB"
        total = str(self.byteToGigabyte(psutil.virtual_memory().total)) + "GB"
        percent = str(psutil.virtual_memory().percent) + "%"

        self.RAMlabel.configure(text="RAM: " + used + "/" + total + " " + percent)
        self.RAMlabel.after(1000, self.updateRAMusage)

# class Circle:
#     def __init__(self, *args, master=None, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.master = master
#         self.create()
#
#     def create(self):
#         self.canvas = tk.Canvas(self.master, bd = 0, bg="#1D1D1D", relief='sunken')
#         self.canvas.create_oval(10,10, 40, 40,fill='#1D1D1D', width=2)
#         self.canvas.grid(row=0, column=0)

class Last24Frame(customtkinter.CTkFrame):
    def __init__(self, *args, day, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((1,2,3), weight=1)

        self.day = day

        if(self.day == 1):
            self.title = customtkinter.CTkLabel(self, text="Last 24 hours: ",
                                                font = ("Helvetica", 20))
        else:
            self.title = customtkinter.CTkLabel(self, text=f"Last {self.day} days:",
                                                font = ("Helvetica", 20))
        self.title.grid(row=0, column=0, padx=10, pady=10)

        self.SensorLabel = customtkinter.CTkLabel(self, text="Sensor", padx=10, pady=5)
        self.SensorLabel.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.MinLabel = customtkinter.CTkLabel(self, text="Minimum", padx=10, pady=5)
        self.MinLabel.grid(row=1, column=1, sticky='nsew')

        self.MaxLabel = customtkinter.CTkLabel(self, text="Maximum", padx=10, pady=5)
        self.MaxLabel.grid(row=1, column=2, sticky='nsew')

        self.AverageLabel = customtkinter.CTkLabel(self, text="Average", padx=10, pady=5)
        self.AverageLabel.grid(row=1, column=3, sticky='nsew')

        self.CPUimage = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "cpu.png")), size=(20, 20))
        self.RAMimage = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "ram-memory.png")), size=(20, 20))

        self.CPUbutton = customtkinter.CTkButton(self, corner_radius=0, text="CPU",
                                                          fg_color="transparent", text_color=("gray75", "gray90"),
                                                          bg_color="#676767",
                                                          anchor="w",
                                                          image=self.CPUimage,
                                                          )
        self.CPUbutton.grid(row=2, column=0, columnspan=4, sticky='nsew')

        self.CPUusageLabel = customtkinter.CTkLabel(self, text="Usage", bg_color="#313131")
        self.CPUusageLabel.grid(row=3, column=0, sticky='nsew')

        CPUinfo = self.getInfoFrom('cpu_usage_percent', 'CPU', day)
        RAMinfo = self.getInfoFrom('RAM_used', 'RAM', day)

        self.CPUminLabel = customtkinter.CTkLabel(self, text=f'''{CPUinfo[0]} %''',
                                                  bg_color="#313131",padx=10, pady=5)
        self.CPUminLabel.grid(row=3, column=1, sticky='nsew')

        self.CPUmaxLabel = customtkinter.CTkLabel(self, text=f'''{CPUinfo[1]} %''',
                                                  bg_color="#313131", padx=10, pady=5)
        self.CPUmaxLabel.grid(row=3, column=2, sticky='nsew')

        self.CPUaverageLabel = customtkinter.CTkLabel(self, text=f'''{CPUinfo[2]} %''',
                                                      bg_color="#313131", padx=10, pady=5)
        self.CPUaverageLabel.grid(row=3, column=3, sticky='nsew')

        self.RAMbutton = customtkinter.CTkButton(self, corner_radius=0, text="RAM",
                                                          fg_color="transparent", text_color=("gray75", "gray90"),
                                                          bg_color="#676767",
                                                          anchor="w",
                                                          image=self.RAMimage,
                                                          )
        self.RAMbutton.grid(row=4, column=0, columnspan=4, sticky='nsew')

        self.RAMusageLabel = customtkinter.CTkLabel(self, text="Usage", bg_color="#313131")
        self.RAMusageLabel.grid(row=5, column=0, sticky='nsew')

        self.RAMminLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfo[0]} %''',
                                             bg_color="#313131", padx=10, pady=5)
        self.RAMminLabel.grid(row=5, column=1, sticky='nsew')

        self.RAMmaxLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfo[1]} %''',
                                             bg_color="#313131", padx=10, pady=5)
        self.RAMmaxLabel.grid(row=5, column=2, sticky='nsew')

        self.RAMaverageLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfo[2]} %''',
                                                 bg_color="#313131", padx=10, pady=5)
        self.RAMaverageLabel.grid(row=5, column=3, sticky='nsew')

    def average(self,li):
        return round(sum(li) / len(li), 2)

    def getInfoFrom(self, data, table, day):
        myList = []
        info = []

        date_column = table + "_date"
        time_column = table + "_time"

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = end_date.split("-")

        start_date[2] = str(int(start_date[2]) - int(day))
        start_date = "-".join(start_date)

        time = datetime.now().strftime("%H:%M:%S")

        cursor.execute(f"""select {data} from {table} where ({date_column} = ? and {time_column} between ? and '23:59:59') or
                                                    ({date_column} = ? and {time_column} <= ?) or
                                                    ({date_column} > ? and {time_column} < ?)""",
                       (start_date, time, end_date, time, start_date, end_date,))
        row = cursor.fetchall()

        for r in row:
            # print(r)
            myList.append(float(r[0]))

        info.append(min(myList))
        info.append(max(myList))
        info.append(self.average(myList))

        return info


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Resource monitor")
        self.geometry("1500x700")

        #self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = SidebarFrame(self, width=140, corner_radius=2)
        self.sidebar_frame.grid(row=0, column=0,rowspan = 3, sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.rtd_frame = RtdFrame(self, fg_color = "transparent")
        self.history_frame = HistoryFrame(self, fg_color = "transparent")

        self.info_frame = InfoFrame(self.rtd_frame, corner_radius=10)
        self.info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.disk_usage_frame = DiskUsageFrame(self.rtd_frame, width=290)
        self.disk_usage_frame.grid(row=1, column=0, padx=20, pady=100, sticky="nsew")

        self.circle_usage_frame = CircularFrame(self.rtd_frame)
        self.circle_usage_frame.displayCPU()
        self.circle_usage_frame.displayRAM()
        self.circle_usage_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.last_24_frame = Last24Frame(self.rtd_frame, day=1)
        self.last_24_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


        self.y1 = []
        self.y2 = []
        self.frame_length = 5

        self.plot_cpu_button = customtkinter.CTkButton(self.circle_usage_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Plot CPU usage",
                                                       fg_color="transparent", text_color=("gray75", "gray90"),
                                                       hover_color=("#01284E", "#024280"), anchor="center",
                                                       command=lambda: self.startGraph("CPU"))
        self.plot_cpu_button.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.plot_ram_button = customtkinter.CTkButton(self.circle_usage_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Plot RAM usage",
                                                       fg_color="transparent", text_color=("gray75", "gray90"),
                                                       hover_color=("#01284E", "#024280"), anchor="center",
                                                       command=lambda: self.startGraph("RAM"))
        self.plot_ram_button.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


        self.rtd_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "real-time.png")), size=(20, 20))
        self.history_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "history.png")), size=(20, 20))
        self.sidebar_rtd_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40,
                                                          border_spacing=10, text="Real Time Data",
                                                          fg_color="transparent", text_color=("gray75", "gray90"),
                                                          hover_color=("#01284E", "#024280"), anchor="w",
                                                          image=self.rtd_image,
                                                          command=self.rtd_button_event
                                                          )
        self.sidebar_rtd_button.grid(row=1, column=0)

        self.sidebar_history_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40,
                                                              border_spacing=10, text="History",
                                                              fg_color="transparent", text_color=("gray75", "gray90"),
                                                              hover_color=("#01284E", "#024280"), anchor="w",
                                                              image=self.history_image,
                                                              command=self.history_button_event,
                                                              )
        self.sidebar_history_button.grid(row=2, column=0)

        self.custom_history = Last24Frame(self.history_frame, day=1)
        self.custom_history.grid(row=0, column=1, sticky='nsew')

        self.entry = customtkinter.CTkEntry(self.history_frame,
                                       placeholder_text="Your choice: ",
                                       width=120,
                                       height=25,
                                       border_width=2,
                                       corner_radius=10)
        self.entry.grid(row=1, column=1)

        self.entry_label = customtkinter.CTkLabel(self.history_frame, text="Enter a number to see the history")

        self.history_button = customtkinter.CTkButton(self.history_frame, text="View History", command=self.checkIfNum)
        self.history_button.grid(row=2, column=1)


    def checkIfNum(self):
        try:
            isinstance(self.entry.get(),int)
            self.custom_history = Last24Frame(self.history_frame, day=int(self.entry.get()))
            self.custom_history.grid(row=0, column=1, sticky='nsew')
        except ValueError:
            messagebox.showinfo("showwarning", "Please enter a number")


    def rtd_button_event(self):
        self.select_frame_by_name("rtd")

    def history_button_event(self):
        self.select_frame_by_name("history")

    def select_frame_by_name(self, name):
        self.sidebar_rtd_button.configure(fg_color=("gray75", "gray25") if name == "rtd" else "transparent")
        self.sidebar_history_button.configure(fg_color=("gray75", "gray25") if name == "history" else "transparent")

        if name == "rtd":
            # rtd frame
            self.rtd_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.rtd_frame.grid_forget()

        if name == "history":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()

    def animateCPUusage(self,i):
        self.y1.append(psutil.cpu_percent())

        if len(self.y1) < self.frame_length:
            plt.cla()
            plt.plot(self.y1, 'g', label="Real-Time CPU Usage")
            plt.title("Real-Time CPU Usage")
        elif len(self.y1) == self.frame_length:
            #show the graphic at a specific time = frame_length
            date = datetime.now().strftime("%Y-%m-%d")
            time = datetime.now().strftime("%H-%M-%S")
            plt.savefig(f"CPU {date} {time}.png")
            pp = PdfPages(f"CPUpdf {date} {time}.pdf")
            pp.savefig()
            pp.close()

        plt.ylim(0, 100)
        plt.xlabel("Time (s)")
        plt.ylabel("Cpu usage (%) ")
        plt.legend(loc = "upper right")
        #automatic padding
        plt.tight_layout()

    def animateMemoryusage(self,i):
        self.y2.append(psutil.virtual_memory().percent)
        if len(self.y2) < self.frame_length:
            plt.cla()
            plt.plot(self.y2, 'g', label="Real-Time RAM Usage")
            plt.title("RAM usage")
        elif len(self.y2) == self.frame_length:
            #show the graphic at a specific time = frame_length
            date = datetime.now().strftime("%Y-%m-%d")
            time = datetime.now().strftime("%H-%M-%S")
            plt.savefig(f"RAM {date} {time}.png")
            pp = PdfPages(f"RAMpdf {date} {time}.pdf")
            pp.savefig()
            pp.close()

        plt.ylim(0, 100)
        plt.xlabel("Time (s)")
        plt.ylabel("RAM usage (%) ")
        plt.legend(loc = "upper right")
        plt.tight_layout()

    # gcf = get current figure
    def startGraph(self, choice):
        if choice == "CPU":
            ani = FuncAnimation(plt.gcf(), self.animateCPUusage, interval=1000)
        elif choice == "RAM":
            ani = FuncAnimation(plt.gcf(), self.animateMemoryusage, interval=1000)
        # automatic padding
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()
