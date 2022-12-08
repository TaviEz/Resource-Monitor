import psutil
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime


y1 = []
frame_length = 20

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("create table CPU (cpu_date text not null, cpu_time text not null, cpu_usage_percent text not null, cpu_freq text not null) ")
CPU_freq = str(psutil.cpu_freq().current) + "MHz"


def animateCPUusage(i):
    y1.append(psutil.cpu_percent())
    usage = str(psutil.cpu_percent(interval=1)) + "%"
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute("""insert into CPU_usage (cpu_date, cpu_time, cpu_usage_percent, cpu_freq) values(?, ?, ?, ?)""",
                   (date, time, usage, CPU_freq))
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

connection.commit()
connection.close()



