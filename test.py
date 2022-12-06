import platform
import cpuinfo
import psutil
import tabulate
def byteToGigabyte(bytes):
    return '{0:.2f}'.format(bytes/1000000000)

data = psutil.disk_partitions()
def get_device_names():
    return [i.device for i in data]

print(get_device_names())
# print(details(get_device_names()[0]))
# print(psutil.disk_usage("C:\\"))
# print(byteToGigabyte(psutil.disk_usage("C:\\").total))
# print(byteToGigabyte(psutil.disk_usage("C:\\").used))
#
#
# info = details("C:\\")
# print(info)
# print(info[0])
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

def all_partitions():
    all = []
    for i in get_device_names():
        all.append(disk_info(i))
    return all
def display_all_partitions():
    info = []

    for i in get_partition_names():
        info.append(disk_info(i))

    info_values = [i.values() for i in info]
    info_tabulated = tabulate.tabulate(info_values, headers=info[0].keys())
    return info_tabulated

print(display_all_partitions())
#
# print(disk_info("C:\\"))
# print(disk_info("E:\\"))
info = all_partitions()
info_values = [i.values() for i in info]
info_tabulated = tabulate.tabulate(info_values, headers=info[0].keys())
print(info_tabulated)