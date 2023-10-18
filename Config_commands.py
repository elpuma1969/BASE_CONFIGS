import sys
import os
from datetime import datetime
from netmiko import ConnectHandler

# Get the path of the current application script
application_path = os.path.dirname(os.path.abspath(sys.argv[0]))

# Define the base script function
def base_script():
    # Set your username and password
    username = 'xxxxx'
    password = "xxxxxx"

    # Define the path to the file containing a list of device IP addresses
    bk_file_path = os.path.join(application_path, "devices.txt")

    # Read the list of device IP addresses from the file
    with open(bk_file_path) as f:
        devices_list = f.read().splitlines()

    # Iterate over each device in the list
    for device in devices_list:
        print('Connecting to device: ' + device)
        ip_address_of_device = device

        # Define the parameters for connecting to a Cisco IOS device using Netmiko
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': username,
            'password': password,
            'secret': password,  # Secret password for enable mode (typically the same as the login password)
            'port': 22,  # SSH port
        }

        try:
            # Connect to the device
            connection = ConnectHandler(**ios_device)
            print('Entering enable mode...')

            # Read commands from a file and send them one by one
            command_file_path = os.path.join(application_path, "config1.txt")
            with open(command_file_path) as cmd_file:
                commands = cmd_file.read().splitlines()

            for cmd in commands:
                output = connection.send_command(cmd)
                print(output)

            # Get the hostname from the device prompt
            prompt = connection.find_prompt()
            hostname = prompt[0:-1]

            # Get the current date
            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            # Define the output directory and create it if it doesn't exist
            output_directory = os.path.join(application_path, "Backup_1")
            os.makedirs(output_directory, exist_ok=True)

            # Define the backup filename using the hostname and date
            filename = os.path.join(output_directory, f"{hostname}_{year}-{month}-{day}_base.txt")

            # Write the output to the backup file
            with open(filename, "w") as final:
                final.write(output)
                print(f"Backup of {hostname} completed successfully")
                print("#" * 30)

            # Disconnect from the device
            print('Closing connection')
            connection.disconnect()

        except Exception as e:
            # Handle any exceptions that occur during the process
            print(f"Failed to backup device {device}. Error: {e}")
            print('#' * 30)

# Call the base_script function to start the backup process
base_script()
