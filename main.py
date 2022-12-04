import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages

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



