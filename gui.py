import platform
import tkinter as tk
import os
import subprocess
import psutil
import cpuinfo
import tabulate
from main import startGraph



def show_frame(frame):
    frame.tkraise()

def openScreenshot(path):
    subprocess.Popen([path], shell=True)

def updateCPUUsage():
    CPUusageLabel.config(text="CPU usage: " + str(psutil.cpu_percent()) + "%")
    CPUusageLabel.after(1000,updateCPUUsage)

def updateRAMUsage():
    total = byteToGigabyte(psutil.virtual_memory().total)
    used = byteToGigabyte(psutil.virtual_memory().used)
    RAMlabel.config(text="RAM: " + used + "GB/" + total + "GB " + str(psutil.virtual_memory().percent) + "%")
    RAMlabel.after(1000, updateRAMUsage)


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

root = tk.Tk()
root.state("zoomed")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# canvas = tk.Canvas(root, height = 700, width = 700, bg = "#00311C")
# canvas.pack()

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



CPUplatformLabel = tk.Label(homeFrame, text=platform.processor(), padx=10,pady=5)
CPUplatformLabel.grid(row=2, column=1)

CPUnameLabel = tk.Label(homeFrame, text=cpuinfo.get_cpu_info()["brand_raw"], padx=10, pady=5)
CPUnameLabel.grid(row=3, column=1)

CPUfreqLabel = tk.Label(homeFrame, text=str(psutil.cpu_freq().current), padx=10, pady=5)
CPUfreqLabel.grid(row=4, column=1,pady=10)


CPUusageLabel = tk.Label(homeFrame, text="", padx=10, pady=5)
CPUusageLabel.grid(row=5, column=1, pady=10)
#CPUlabel.after(2000, lambda:updateText(CPUlabel, "CPU " + displayCPU()))
updateCPUUsage()

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

# y1 = cpu y2 = ram
# print(max(y1))
# print(max(y2))