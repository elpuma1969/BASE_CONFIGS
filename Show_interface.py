import sys
import os
from datetime import datetime
from netmiko import ConnectHandler

# Get the path of the directory containing the script
application_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def run_script():
    # Define the username and password for connecting to Cisco devices
    username = 'xxxxx'
    password = "xxxxx"

    # Define the path to the file containing a list of device IP addresses
    ex_file_path = os.path.join(application_path, "cisco_master.txt")

    # Read the list of device IP addresses from the file
    with open(ex_file_path) as f:
        devices_list = f.read().splitlines()

    # Loop through each device in the list
    for device in devices_list:
        try:
            print('Connecting to device: ' + device)
            ip_address_of_device = device

            # Define the parameters for connecting to the Cisco device using Netmiko
            ios_device = {
                'device_type': 'cisco_ios',
                'ip': ip_address_of_device,
                'username': username,
                'password': password,
                'secret': password,
                'port': 22,
            }

            # Establish a connection to the device
            connection = ConnectHandler(**ios_device)
            print('Entering enable mode...')

            # Send a command to the device to retrieve information about down interfaces
            output = connection.send_command('sh int status | i notconnect')
            print(output)

            # Extract the hostname from the command prompt
            prompt = connection.find_prompt()
            hostname = prompt[0:-1]

            # Get the current date
            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            # Create a directory for saving the output files if it doesn't exist
            output_directory = os.path.join(application_path, "cisco_outcome")
            os.makedirs(output_directory, exist_ok=True)

            # Define the filename for the output file
            filename = os.path.join(output_directory, f"{hostname}_{year}-{month}-{day}_Down.txt")

            # Write the output to the output file
            with open(filename, "a") as final:
                final.write(output)
                print(f"Backup of {hostname} completed successfully")
                print("#" * 30)

            # Close the connection to the device
            print('Closing connection')
            connection.disconnect()

        except Exception as e:
            # Handle any exceptions that may occur during the process
            print(f"An error occurred while processing device {device}: {str(e)}")
            print("#" * 30)


# Call the run_script function to start the script
run_script()
