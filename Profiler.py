import csv
import subprocess
import time

# Define the package name of the target application
package_name = "com.uberconf"
package_name_full = "com.uberconference.beta"

# Define the interval between each sampling (in seconds)
sampling_interval = 1

# Define the duration of the monitoring (in seconds)
monitoring_duration = 60

# Define the output file name
output_file = "app_monitoring.csv"

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
            ["adb", "shell", "top", "-n", "1", "-d", "1", "|", "grep", package_name]).decode().strip()
        cpu_usage = float(cpu_output.split()[2].replace("%", ""))

        # Get the memory usage of the target application
        mem_output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "meminfo", package_name_full, "|", "grep", "TOTAL"]).decode().strip()
        mem_usage = int(mem_output.split()[1])

        # Get the battery percentage of the device
        battery_output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "battery", "|", "grep", "level"]).decode().strip()
        battery_percentage = int(battery_output.split()[1])

        # Get the CPU temperature of the device
        #This part did not work
        # temp_output = subprocess.check_output(
        #     ["adb", "shell", "cat", "/sys/class/thermal/thermal_zone*/temp"]).decode().strip()
        # cpu_temp = int(temp_output.split()[0]) / 1000

        # Write the data to the CSV file
        writer.writerow([timestamp, cpu_usage, mem_usage, battery_percentage])

        # Wait for the next sampling interval
        time.sleep(sampling_interval)
