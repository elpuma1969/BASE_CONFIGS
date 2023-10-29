import os
from datetime import datetime
from netmiko import BaseConnection

# Create a subclass of BaseConnection for a specific device type (e.g., Cisco IOS)
class CiscoIOSConnection(BaseConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def disable_paging(self, *args, **kwargs):
        # Implement device-specific paging disable command
        self.send_command("terminal length 0")

    def connect(self):
        pass

# Create a folder called "INFO_TECH" if it doesn't exist
output_folder = "INFO_TECH"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Read the device IP addresses from the "devices" file
with open("devices.txt", "r") as devices_file:
    device_ips = devices_file.read().splitlines()

# List of show commands to send
show_commands = ["show version", "show interfaces", "show running-config"]

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Iterate through the list of device IP addresses
for device_ip in device_ips:
    # Define the device connection parameters for each device
    ios_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": "puma",
        "password": "cisco",
        "port": 22,
    }

    # Create an instance of the CiscoIOSConnection class for each device
    conn = CiscoIOSConnection(**ios_device)

    # Connect to the device
    conn.connect()

    # Disable paging on the device (using the device-specific method implemented in the subclass)
    conn.disable_paging()

    # Iterate through the list of commands, send them to the device, and save the output to a file
    for cmd in show_commands:
        output = conn.send_command(cmd)
        # Create a filename based on the device IP, command, and date
        prompt = conn.find_prompt()
        file_name = f"{prompt}_{cmd.replace(' ', '_')}_{current_datetime}.txt"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "w") as output_file:
            output_file.write(output)
        print(f"Device IP: {device_ip}, Command: {cmd}\nOutput saved to {file_path}\n")

    # Close the connection for each device
    conn.disconnect()
