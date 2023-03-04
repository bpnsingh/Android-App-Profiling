from config import *
import csv
import subprocess
import time


# Open the output CSV file for writing
with open(output_file, "w", newline="") as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(
        ["Timestamp", "CPU usage (%)", "Memory usage (KB)", "Battery percentage (%)", "CPU temperature (°C)"])

    # Get the current time
    start_time = time.time()

    # Start monitoring the target application
    while time.time() - start_time < monitoring_duration:
        # Get the current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Get the CPU usage of the target application
        cpu_output = subprocess.check_output(
            ["adb", "shell", "top", "-n", "1", "-d", "1", "|", "grep", package_name[0:14]]).decode().strip()
        try:
            #format
            # 8427 u0_a395      10 -10  34G 302M 173M S  123   5.4  25:31.76 us.zoom.videome+
            cpu_usage = float(cpu_output.split()[9].replace("%", ""))
            # print("CPU usage:", cpu_usage)
        except ValueError as e:
            print("Error:", e)
            continue

        # Get the memory usage of the target application
        mem_output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "meminfo", package_name, "|", "grep", "TOTAL"]).decode().strip()
        mem_usage = int(mem_output.split()[1])

        # Get the battery percentage of the device
        battery_output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "battery", "|", "grep", "level"]).decode().strip()
        battery_percentage = int(battery_output.split()[1])

        # Get the CPU temperature of the device
        #This part did not work, may work on some devices.
        # temp_output = subprocess.check_output(
        #     ["adb", "shell", "cat", "/sys/class/thermal/thermal_zone*/temp"]).decode().strip()
        # cpu_temp = int(temp_output.split()[0]) / 1000

        # Write the data to the CSV file
        print ("{0} {1} {2} {3}".format(timestamp, cpu_usage, mem_usage, battery_percentage))
        writer.writerow([timestamp, cpu_usage, mem_usage, battery_percentage])

        # Wait for the next sampling interval
        time.sleep(sampling_interval)
