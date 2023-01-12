from tkinter import *
from tkinter import messagebox
import customtkinter

import sqlite3

import cpuinfo
import platform
import psutil
import tabulate

import os
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages

from datetime import datetime

connection = sqlite3.connect("test.db")
cursor=connection.cursor()

#https://github.com/TomSchimansky/CustomTkinter/wiki
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

        self.cpu_info_frame = CPUinfoFrame(self, corner_radius=10)
        self.cpu_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.system_info_frame = SystemInfoFrame(self, corner_radius=10)
        self.system_info_frame.grid(row=1, column=0, padx=20, pady=10)

        self.circle_usage_frame = HardwareFrame(self)
        self.circle_usage_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        self.last_24_frame = Last24Frame(self, day=1)
        self.last_24_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


        self.disk_usage_frame = DiskUsageFrame(self, width=290)
        self.disk_usage_frame.grid(row=2, column=0, padx=20, pady=10)


class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((1,2,3), weight=1)
        self.custom_history = Last24Frame(self, day=1)
        self.custom_history.grid(row=0, column=1, sticky='nsew')

        self.entry = customtkinter.CTkEntry(self,
                                            placeholder_text="Your choice: ",
                                            width=120,
                                            height=25,
                                            border_width=2,
                                            corner_radius=10)
        self.entry.grid(row=1, column=1)

        self.entry_label = customtkinter.CTkLabel(self, text="Enter a number to see the history")

        self.history_button = customtkinter.CTkButton(self, text="View History", command=self.checkIfNum)
        self.history_button.grid(row=2, column=1)

    def checkIfNum(self):
        try:
            myEntry = self.entry.get()
            if int(myEntry) <= 0:
                raise ValueError
            #https://stackoverflow.com/questions/11204789/how-to-properly-use-pythons-isinstance-to-check-if-a-variable-is-a-number
            isinstance(myEntry, int)
            self.custom_history = Last24Frame(self, day=int(self.entry.get()))
            self.custom_history.grid(row=0, column=1, sticky='nsew')
        except ValueError:
            messagebox.showinfo("Warning!", "Please enter a positive number")


class CPUinfoFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #https://pyshark.com/system-and-hardware-information-using-python/
        self.CPUplatformLabel = customtkinter.CTkLabel(self, text=f'Processor Type: {platform.processor()}',
                                                       font=customtkinter.CTkFont(size=20))
        self.CPUplatformLabel.grid(row=1, column=0, padx=20, pady=10)

        self.CPUnameLabel = customtkinter.CTkLabel(self,
                                                   text=f'CPU Name: {cpuinfo.get_cpu_info()["brand_raw"]}',
                                                   font=customtkinter.CTkFont(size=20))
        self.CPUnameLabel.grid(row=2, column=0, padx=20, pady=10)

        self.CPUcores = customtkinter.CTkLabel(self, text=f'Total Cores: {psutil.cpu_count(logical=False)}',
                                               font=customtkinter.CTkFont(size=20))
        self.CPUcores.grid(row=3, column=0, padx=20, pady=10)

        self.CPUthreads = customtkinter.CTkLabel(self, text=f'Total Threads: {psutil.cpu_count(logical=True)}',
                                                 font=customtkinter.CTkFont(size=20))
        self.CPUthreads.grid(row=4, column=0, padx=20, pady=10)


        self.CPU_freq = str(psutil.cpu_freq().current) + "MHz"
        self.CPUfreqLabel = customtkinter.CTkLabel(self, text=f'Processor Base Frequency: {self.CPU_freq}', padx=10,
                                                   pady=5,
                                                   font=customtkinter.CTkFont(size=20))
        self.CPUfreqLabel.grid(row=5, column=0, padx=20, pady=10)

class SystemInfoFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # https://pyshark.com/system-and-hardware-information-using-python/
        self.uname = platform.uname()

        self.computerNetwork = customtkinter.CTkLabel(self, text=f"Computer network name: {self.uname.node}",
                                                      font=customtkinter.CTkFont(size=20))
        self.computerNetwork.grid(row=0, column=0, padx=20, pady=10)

        self.systemName = customtkinter.CTkLabel(self, text=f"System: {self.uname.system}",
                                                 font=customtkinter.CTkFont(size=20))
        self.systemName.grid(row=1, column=0, padx=20, pady=10)

        self.release = customtkinter.CTkLabel(self, text=f"Release: {self.uname.release}",
                                              font=customtkinter.CTkFont(size=20))
        self.release.grid(row=2, column=0, padx=20, pady=10)

        self.version = customtkinter.CTkLabel(self, text=f"Version: {self.uname.version}",
                                              font=customtkinter.CTkFont(size=20))
        self.version.grid(row=3, column=0, padx=20, pady=10)


class DiskUsageFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.disk_partition_info = customtkinter.CTkTextbox(self, width=290, height=90)
        self.disk_partition_info.grid(row=0, column=0, padx=20, pady=10)
        self.disk_partition_info.insert("0.0", text=self.display_all_partitions())
        self.disk_partition_info.configure(state="disabled")


    def get_partition_names(self):
        #https://psutil.readthedocs.io/en/latest/index.html?highlight=disk%20usage
        #return a list with all partition names
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
        #info = list with n dictionaries, n = no of partitions
        info = []
        for i in self.get_partition_names():
            info.append(self.disk_info(i))

        #https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
        info_values = [i.values() for i in info]
        info_tabulated = tabulate.tabulate(info_values, headers=info[0].keys())
        return info_tabulated

class HardwareFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.y1 = []
        self.y2 = []
        self.frame_length = 20

        self.plot_cpu_button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                       border_spacing=10, text="Plot CPU usage",
                                                       fg_color="transparent", text_color=("gray75", "gray90"),
                                                       hover_color=("#01284E", "#024280"), anchor="center",
                                                       command=lambda: self.startGraph("CPU"))
        self.plot_cpu_button.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.plot_ram_button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                       border_spacing=10, text="Plot RAM usage",
                                                       fg_color="transparent", text_color=("gray75", "gray90"),
                                                       hover_color=("#01284E", "#024280"), anchor="center",
                                                       command=lambda: self.startGraph("RAM"))
        self.plot_ram_button.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.displayCPU()
        self.displayRAM()

    def animateCPUusage(self, i):
        #https://www.youtube.com/watch?v=Ercd-Ip5PfQ&list=PL986Lus2SJNVjMtu54C81E4Kq8UoF3gcD&index=6
        self.y1.append(psutil.cpu_percent())

        if len(self.y1) < self.frame_length:
            #cla=clear axis
            plt.cla()
            plt.plot(self.y1, 'g', label="Real-Time CPU Usage")
            plt.title("Real-Time CPU Usage")
        elif len(self.y1) == self.frame_length:
            # show the graphic at a specific time = frame_length
            date = datetime.now().strftime("%Y-%#m-%#d")
            time = datetime.now().strftime("%H-%M-%S")
            plt.savefig(f"CPU {date} {time}.png")
            pp = PdfPages(f"CPUpdf {date} {time}.pdf")
            pp.savefig()
            pp.close()

        plt.ylim(0, 100)
        plt.xlabel("Time (s)")
        plt.ylabel("Cpu usage (%) ")
        plt.legend(loc="upper right")
        # automatic padding
        plt.tight_layout()
        #return plt

    def animateMemoryusage(self, i):
        self.y2.append(psutil.virtual_memory().percent)
        if len(self.y2) < self.frame_length:
            plt.cla()
            plt.plot(self.y2, 'g', label="Real-Time RAM Usage")
            plt.title("RAM usage")
        elif len(self.y2) == self.frame_length:
            # show the graphic at a specific time = frame_length
            date = datetime.now().strftime("%Y-%#m-%#d")
            time = datetime.now().strftime("%H-%M-%S")
            plt.savefig(f"RAM {date} {time}.png")
            pp = PdfPages(f"RAMpdf {date} {time}.pdf")
            pp.savefig()
            pp.close()

        plt.ylim(0, 100)
        plt.xlabel("Time (s)")
        plt.ylabel("RAM usage (%) ")
        plt.legend(loc="upper right")
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
        plt.close()

    #first create the label for the component then in another func change the value
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
        #https://stackoverflow.com/questions/44725090/python-tkinter-update-every-second
        self.CPUusageLabel.after(1000, self.updateCPUUsage)

    def updateRAMusage(self):
        used = str(self.byteToGigabyte(psutil.virtual_memory().used)) + "GB"
        total = str(self.byteToGigabyte(psutil.virtual_memory().total)) + "GB"
        percent = str(psutil.virtual_memory().percent) + "%"

        self.RAMlabel.configure(text="RAM: " + used + "/" + total + " " + percent)
        self.RAMlabel.after(1000, self.updateRAMusage)


class Last24Frame(customtkinter.CTkFrame):
    def __init__(self, *args, day, **kwargs):
        super().__init__(*args, **kwargs)

        #weight = proportional
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

        #for images/icons : https://www.youtube.com/watch?v=NoTM8JciWaQ&list=PL986Lus2SJNVjMtu54C81E4Kq8UoF3gcD&index=7&t=150s
        #current directory: https://www.geeksforgeeks.org/get-directory-of-current-python-script/
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

        #lists with 3 values: min, max, avg
        CPUinfo = self.getInfoFrom('cpu_usage_percent', 'CPU', day)
        RAMinfoGB = self.getInfoFrom('RAM_used', 'RAM', day)
        RAMinfoPercent = self.getInfoFrom('RAM_percent', 'RAM', day)

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

        self.RAMminLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfoPercent[0]}% ({RAMinfoGB[0]} GB)''',
                                             bg_color="#313131", padx=10, pady=5)
        self.RAMminLabel.grid(row=5, column=1, sticky='nsew')

        self.RAMmaxLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfoPercent[1]}% ({RAMinfoGB[1]} GB)''',
                                             bg_color="#313131", padx=10, pady=5)
        self.RAMmaxLabel.grid(row=5, column=2, sticky='nsew')

        self.RAMaverageLabel = customtkinter.CTkLabel(self, text=f'''{RAMinfoPercent[2]}% ({RAMinfoGB[2]} GB)''',
                                                 bg_color="#313131", padx=10, pady=5)
        self.RAMaverageLabel.grid(row=5, column=3, sticky='nsew')

    def average(self,li):
        return round(sum(li) / len(li), 2)

    def getInfoFrom(self, data, table, days_ago):
        myList = []
        info = []
        #date-time: https://www.programiz.com/python-programming/datetime/current-datetime
        date_column = table + "_date"
        time_column = table + "_time"

        # '#' is used to eliminate leading zeros
        end_date = datetime.now().strftime("%Y-%#m-%#d")
        start_date = end_date.split("-")
        # start_date[0] = year
        # start_date[1] = month
        # start_date[2] = day

        # the subtraction between current day and the asked day
        sub = int(start_date[2]) - int(days_ago)
        # if the asked date is in another month
        if (sub <= 0):
            aux_month = int(start_date[1]) - 1 - -sub // 31
            # if the asked date is in the past year
            if (aux_month <= 0):
                start_date[0] = str(int(start_date[0]) - 1)
                start_date[1] = str(12 - -sub // 31)
            else:
                # if the asked date is in the same year
                start_date[1] = str(aux_month)
            start_date[2] = str(31 - -sub % 31)
        else:
            start_date[2] = str(sub)
        start_date = "-".join(start_date)

        time = datetime.now().strftime("%H:%M:%S")
        #select query https://www.sqlitetutorial.net/sqlite-select/
        #query with parameters://stackoverflow.com/questions/22776756/parameterized-queries-in-sqlite3-using-question-marks
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = SidebarFrame(self, width=140, corner_radius=2)
        self.sidebar_frame.grid(row=0, column=0,rowspan = 3, sticky="nsew")

        self.rtd_frame = RtdFrame(self, fg_color = "transparent")
        self.history_frame = HistoryFrame(self, fg_color = "transparent")


        self.rtd_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "real-time.png")), size=(20, 20))
        self.history_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "history.png")), size=(20, 20))
        self.sidebar_rtd_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40,
                                                          border_spacing=10, text="Real Time Data",
                                                          fg_color="transparent", text_color=("gray75", "gray90"),
                                                          hover_color=("#01284E", "#024280"), anchor="w",
                                                          image=self.rtd_image,
                                                          command=lambda:self.select_frame_by_name('rtd')
                                                          )
        self.sidebar_rtd_button.grid(row=1, column=0)

        self.sidebar_history_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40,
                                                              border_spacing=10, text="History",
                                                              fg_color="transparent", text_color=("gray75", "gray90"),
                                                              hover_color=("#01284E", "#024280"), anchor="w",
                                                              image=self.history_image,
                                                              command=lambda:self.select_frame_by_name('history')
                                                              )
        self.sidebar_history_button.grid(row=2, column=0)

        self.select_frame_by_name("rtd")

    # def rtd_button_event(self):
    #     self.select_frame_by_name("rtd")
    #
    # def history_button_event(self):
    #     self.select_frame_by_name("history")

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



if __name__ == "__main__":
    app = App()
    app.mainloop()