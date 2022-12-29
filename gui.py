import psutil
import tkinter as tk
import customtkinter

import platform

import os
import subprocess

import cpuinfo
import tabulate
import sqlite3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages

from datetime import datetime

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

y1 = []
frame_length = 20

def animateCPUusage(i):
    y1.append(psutil.cpu_percent())

    if len(y1) < frame_length:
        plt.cla()
        plt.plot(y1, 'g', label="Real-Time CPU Usage")
        plt.title("Real-Time CPU Usage")
    elif len(y1) == frame_length:
        #show the graphic at a specific time = frame_length
        plt.savefig("CPU.png")
        pp = PdfPages("cpuPdf.pdf")
        pp.savefig()
        pp.close()

    plt.ylim(0, 100)
    plt.xlabel("Time (s)")
    plt.ylabel("Cpu usage (%) ")
    plt.legend(loc = "upper right")
    #automatic padding
    plt.tight_layout()

y2 = []
def animateMemoryusage(i):
    y2.append(psutil.virtual_memory().percent)
    if len(y2) < frame_length:
        plt.cla()
        plt.plot(y2, 'g', label="Real-Time RAM Usage")
        plt.title("RAM usage")
    elif len(y2) == frame_length:
        #show the graphic at a specific time = frame_length
        plt.savefig("RAM.png")
        pp = PdfPages("ramPdf.pdf")
        pp.savefig()
        pp.close()

    plt.ylim(0, 100)
    plt.xlabel("Time (s)")
    plt.ylabel("RAM usage (%) ")
    plt.legend(loc = "upper right")
    plt.tight_layout()

# gcf = get current figure
def startGraph(user_input):
    if user_input == "CPU":
        ani = FuncAnimation(plt.gcf(), animateCPUusage, interval=1000)
    elif user_input == "RAM":
        ani = FuncAnimation(plt.gcf(), animateMemoryusage, interval=1000)
    # automatic padding
    plt.tight_layout()
    plt.show()





########################## GUI #########################
def show_frame(frame):
    frame.tkraise()

def openScreenshot(path):
    subprocess.Popen([path], shell=True)

#cursor.execute("create table CPU (cpu_date text not null, cpu_time text not null, cpu_usage_percent text not null, cpu_freq text not null) ")
CPU_freq = str(psutil.cpu_freq().current) + "MHz"
def updateCPUUsage():
    usage = str(psutil.cpu_percent()) + "%"
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    # cursor.execute("""insert into CPU (cpu_date, cpu_time, cpu_usage_percent, cpu_freq) values(?, ?, ?, ?)""",
    #                (date, time, usage, CPU_freq))
    CPUusageLabel.config(text="CPU usage: " + usage)
    CPUusageLabel.after(1000,updateCPUUsage)

#cursor.execute("create table RAM (RAM_date text not null, RAM_time text not null, RAM_used text, RAM_total text, RAM_percent text) ")
def updateRAMUsage():
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    used = str(byteToGigabyte(psutil.virtual_memory().used)) + "GB"
    total = str(byteToGigabyte(psutil.virtual_memory().total)) + "GB"
    percent = str(psutil.virtual_memory().percent) + "%"

    RAMlabel.config(text="RAM: " + used + "/" + total + " " + percent)
    # cursor.execute("""insert into RAM (RAM_date, RAM_time, RAM_used, RAM_total, RAM_percent) values (?,?,?,?,?)""", (date, time, used, total, percent))
    RAMlabel.after(1000, updateRAMUsage)

def average(li):
    return round(sum(li) / len(li), 2)

def getInfoFrom(data, table):
    myList = []
    info = []
    cursor.execute(f"""select {data} from {table}""")
    row = cursor.fetchall()

    for r in row:
        myList.append(float(r[0]))

    info.append(min(myList))
    info.append(max(myList))
    info.append(average(myList))

    return info


data = psutil.disk_partitions()
#device = name of the partition ex: C\\  D\\ etc
def get_partition_names():
    return [i.device for i in data]

def disk_info(device_name):
    disk_info = {}
    usage = psutil.disk_usage(device_name)
    disk_info['Device'] = device_name
    disk_info['Total'] = f"{byteToGigabyte(usage.total)} GB"
    disk_info['Used'] = f"{byteToGigabyte(usage.used)} GB"
    disk_info['Free'] = f"{byteToGigabyte(usage.free)} GB"
    disk_info['Percent'] = f"{usage.percent} %"
    return disk_info

def display_all_partitions():
    info = []

    for i in get_partition_names():
        info.append(disk_info(i))

    info_values = [i.values() for i in info]
    info_tabulated = tabulate.tabulate(info_values, headers=info[0].keys())
    return info_tabulated

def byteToGigabyte(bytes):
    return '{0:.2f}'.format(bytes/1000000000)

######################### GUI #########################


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.state("zoomed")

# root.rowconfigure(0, weight=1)
# root.columnconfigure(0, weight=1)

homeFrame = tk.Frame(root, bg="#00311C")
cpuFrame = tk.Frame(root, bg="#00311C")
ramFrame = tk.Frame(root, bg="#00311C")
#frame.place(relwidth=0.8,relheight=0.8, relx=0.1, rely=0.1)

for frame in (homeFrame, cpuFrame, ramFrame):
    frame.grid(row=0, column=0, sticky='nsew')

### Home frame
#CPUusage = tk.Button(root, text="CPU usage",padx=10, pady=5, fg="white", bg="#00311C", command=lambda: startGraph("CPU")
homeFrame_title = tk.Label(homeFrame, text='Home Page', fg='white',bg='#00311C')
homeFrame_title.grid(row=0, column=0)

#Button 1
CPUBtn = tk.Button(homeFrame, text="CPU",padx=10, pady=5, fg="white", bg="#00311C", command=lambda:show_frame(cpuFrame))
CPUBtn.grid(row=1,column=1)

#button 2
RAMusageBtn = tk.Button(homeFrame, text="RAM usage",padx=10, pady=5, fg="white", bg="#00311C", command=lambda: startGraph("RAM"))
RAMusageBtn.grid(row=1, column=2)

#button 3
DiskusageBtn = tk.Button(homeFrame, text="Disk usage",padx=10, pady=5, fg="white", bg="#00311C")
DiskusageBtn.grid(row=1, column=3)



# CPUplatformLabel = tk.Label(homeFrame, text=platform.processor(), padx=10,pady=5)
# CPUplatformLabel.grid(row=2, column=1)

label = customtkinter.CTkLabel(master=root, text=platform.processor())
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

CPUnameLabel = tk.Label(homeFrame, text=cpuinfo.get_cpu_info()["brand_raw"], padx=10, pady=5)
CPUnameLabel.grid(row=3, column=1)

CPUfreqLabel = tk.Label(homeFrame, text=str(psutil.cpu_freq().current), padx=10, pady=5)
CPUfreqLabel.grid(row=4, column=1,pady=10)


CPUusageLabel = tk.Label(homeFrame, text="", padx=10, pady=5)
CPUusageLabel.grid(row=5, column=1, pady=10)
updateCPUUsage()

CPUminLabel = tk.Label(homeFrame, text=f'''{getInfoFrom('cpu_usage_percent', 'CPU')[0]} %''', padx=10, pady=5)
CPUminLabel.grid(row=5, column=4, pady=10)

CPUmaxLabel =tk.Label(homeFrame, text=f'''{getInfoFrom('cpu_usage_percent', 'CPU')[1]} %''', padx=10, pady=5)
CPUmaxLabel.grid(row=5, column=3, pady=10)

CPUaverageLabel = tk.Label(homeFrame, text=f'''{getInfoFrom('cpu_usage_percent', 'CPU')[2]} %''', padx=10, pady=5)
CPUaverageLabel.grid(row=5, column=2, pady=10)


RAMlabel = tk.Label(homeFrame, text="", padx=10, pady=5)
RAMlabel.grid(row=6, column=1, pady=10)
updateRAMUsage()

diskLabel = tk.Label(homeFrame, text="Disk usage")
diskLabel.grid(row=7, column=1, pady=10)

textArea = tk.Text(homeFrame, bg="#00311C", fg='yellow',width=50, height=5)
textArea.grid(row=8, column=1, pady=10)
textArea.insert(tk.END, display_all_partitions())

### CPU frame
cpuFrame_title = tk.Label(cpuFrame, text='CPU', bg='yellow')
cpuFrame_title.pack()

#Button1
homeBtn = tk.Button(cpuFrame, text='Home', fg='white', bg="#00311C", command=lambda:show_frame(homeFrame))
homeBtn.pack()

#Button2
realTimeDataBtn = tk.Button(cpuFrame, text="Real time data",padx=10, pady=5, fg="white", bg="#00311C", command=lambda: startGraph("CPU"))
realTimeDataBtn.pack()

#Button3
pngBtn = tk.Button(cpuFrame, text="png", fg='white', bg='#00311C', command=lambda: openScreenshot(os.getcwd() + "\CPU.png"))
pngBtn.pack()

#Button4
pdfBtn = tk.Button(cpuFrame, text="pdf", fg='white', bg='#00311C', command=lambda: openScreenshot(os.getcwd() + "\cpuPdf.pdf"))
pdfBtn.pack()

### RAM frame
ramFrame_title = tk.Label(ramFrame, text='RAM', bg='green')
ramFrame_title.pack()

#Button1
homeBtn = tk.Button(ramFrame, text='Home', fg='white', bg="#00311C", command=lambda:show_frame(homeFrame))
homeBtn.pack()

#Button2
realTimeDataBtn = tk.Button(ramFrame, text="Real time data",padx=10, pady=5, fg="white", bg="#00311C", command=lambda: startGraph("CPU"))
realTimeDataBtn.pack()

#Button3
pngBtn = tk.Button(ramFrame, text = "png", fg='white', bg='#00311C')
pngBtn.pack()

show_frame(homeFrame)

root.mainloop()

############################## END OF GUI #############################

connection.commit()
connection.close()
