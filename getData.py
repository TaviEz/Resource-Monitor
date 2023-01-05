import sqlite3
import psutil
from datetime import datetime

def byteToGigabyte(bytes):
    return '{0:.2f}'.format(bytes/1000000000)

def average(li):
    return round(sum(li)/len(li), 2)

connection = sqlite3.connect("test.db")
cursor = connection.cursor()


cursor.execute("create table if not exists CPU (cpu_date text not null, cpu_time text not null, cpu_usage_percent text not null, cpu_freq text not null) ")
cursor.execute("create table if not exists RAM (RAM_date text not null, RAM_time text not null, RAM_used text, RAM_total text, RAM_percent text) ")
info =[]
cpu_percent =[]
i = 0
freq = str(psutil.cpu_freq().current) + "MHz"
while True:
    cpu_usage = str(psutil.cpu_percent(interval=1))
    date = datetime.now().strftime("%Y-%#m-%#d")
    time = datetime.now().strftime("%H:%M:%S")
    ram_used = str(byteToGigabyte(psutil.virtual_memory().used))
    ram_total = str(byteToGigabyte(psutil.virtual_memory().total))
    percent = str(psutil.virtual_memory().percent)
    cursor.execute("""insert into CPU (cpu_date, cpu_time, cpu_usage_percent, cpu_freq) values(?, ?, ?, ?)""", (date, time, cpu_usage, freq))
    cursor.execute("""insert into RAM (RAM_date, RAM_time, RAM_used, RAM_total, RAM_percent) values (?,?,?,?,?)""",
                   (date, time, ram_used, ram_total, percent))
    if i == 5:
        break
    i += 1

connection.commit()
connection.close()