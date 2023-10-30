import os
from datetime import datetime
from netmiko import ConnectHandler

# Create a folder called "INFO_TECH" if it doesn't exist
output_folder = "INFO_TECH"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Read the device IP addresses from the "devices" file
with open("devices.txt", "r") as devices_file:
    device_ips = devices_file.read().splitlines()

# List of show commands to send for Dell OS6 switches
show_commands = ["show version", "show interfaces status", "show vlan-switch", "show running-config"]

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Iterate through the list of device IP addresses
for device_ip in device_ips:
    # Define the device connection parameters for each device (Dell OS6)
    dell_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": "puma",
        "password": "cisco",
        "port": 22,
    }

    try:
        # Create an SSH connection to the Dell switch
        conn = ConnectHandler(**dell_device)

        # Retrieve the hostname of the device
        prompt = conn.find_prompt()
        hostname = prompt[0:-1]

        # Send commands to the device and save the output to a file
        for cmd in show_commands:
            output = conn.send_command(cmd)
            # Create a filename based on the hostname, device IP, command, and date
            file_name = f"{hostname}_{device_ip}_{cmd.replace(' ', '_')}_{current_datetime}.txt"
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, "w") as output_file:
                output_file.write(output)
            print(f"Device IP: {device_ip}, Hostname: {hostname}, Command: {cmd}\nOutput saved to {file_path}\n")

        # Disconnect from the Dell switch
        conn.disconnect()

    except Exception as e:
        # Handle exceptions here, you can print an error message or log the exception
        print(f"Error connecting to device {device_ip}: {str(e)}")
