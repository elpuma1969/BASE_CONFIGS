from getpass import getpass
from netmiko import ConnectHandler
from datetime import datetime

# Prompt the user for their SSH credentials
username = input('Enter your SSH username: ')
password = getpass()

# Open the file containing a list of device IP addresses
with open("BK.txt") as f:
    devices_list = f.read().splitlines()

# Loop through the list of devices
for device in devices_list:
    try:
        print('Connecting to device: ' + device)
        ip_address_of_device = device

        # Define device information for SSH connection
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': username,
            'password': password
        }

        # Connect to the device
        connection = ConnectHandler(**ios_device)
        print('Entering enable mode...')
        connection.enable()

        # Define TFTP copy command and TFTP server IP address
        command = "copy running-config tftp:"
        command2 = '10.216.2.230'

        start_time = datetime.now()

        # Create a new connection for sending commands
        net_connect = ConnectHandler(**ios_device)

        # Send the TFTP copy command and TFTP server IP address
        output = net_connect.send_command_timing(command, strip_prompt=False, read_timeout=100, strip_command=False, delay_factor=4)
        output2 = net_connect.send_command_timing(command2, strip_prompt=False, read_timeout=100, strip_command=False, delay_factor=4)

        # Check if "Address or name of remote host" prompt appears
        if "Address or name of remote host" in output:
            print("Starting copy...")
            output += net_connect.send_command("\n", delay_factor=4, read_timeout=100, expect_string=r"#")
            output2 += net_connect.send_command("\n", delay_factor=4, read_timeout=100, expect_string=r"#")

        # Check if "Destination filename" prompt appears
        if "Destination filename" in output:
            print("Starting copy...")
            output += net_connect.send_command("\n", delay_factor=4, read_timeout=100, expect_string=r"#")

        # Disconnect from the device
        net_connect.disconnect()

        end_time = datetime.now()
        print(f"\n{output}\n")
        print(f'\n{output2}\n')
        print("Done")
        print(f"Execution time: {end_time - start_time}")

    except Exception as e:
        print(f"An error occurred while connecting to device {device}: {str(e)}")
