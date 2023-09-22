import sys
import os
from datetime import datetime
from netmiko import ConnectHandler

application_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def run_script():
    username = 'xxxxxx'
    password = "xxxxxx"

    bk_file_path = os.path.join(application_path, "cisco_master.txt")
    with open(bk_file_path) as f:
        devices_list = f.read().splitlines()

    for device in devices_list:
        try:
            print('Connecting to device: ' + device)
            ip_address_of_device = device
            ios_device = {
                'device_type': 'cisco_ios',
                'ip': ip_address_of_device,
                'username': username,
                'password': password,
                'secret': password,
                'port': 22,
            }
            connection = ConnectHandler(**ios_device)
            print('Entering enable mode...')

            output = connection.send_command('sh int status | i notconnect')
            print(output)

            prompt = connection.find_prompt()
            hostname = prompt[0:-1]

            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            output_directory = os.path.join(application_path, "cisco_outcome")
            os.makedirs(output_directory, exist_ok=True)
            filename = os.path.join(output_directory, f"{hostname}_{year}-{month}-{day}_Down.txt")

            with open(filename, "a") as final:
                final.write(output)
                print(f"Backup of {hostname} completed successfully")
                print("#" * 30)

            print('Closing connection')
            connection.disconnect()

        except Exception as e:
            print(f"An error occurred while processing device {device}: {str(e)}")
            print("#" * 30)


run_script()
