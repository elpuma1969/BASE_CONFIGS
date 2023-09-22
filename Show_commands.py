import sys
import os
from datetime import datetime
from netmiko import ConnectHandler

application_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def base_script():
    username = 'xxxxx'
    password = "xxxx"

    bk_file_path = os.path.join(application_path, "devices.txt")
    with open(bk_file_path) as f:
        devices_list = f.read().splitlines()

    for devices in devices_list:
        print('Connecting to device: ' + devices)
        ip_address_of_device = devices
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': username,
            'password': password,
            'secret': password,
            'port': 22,
        }

        try:
            connection = ConnectHandler(**ios_device)
            print('Entering enable mode...')

            output = connection.send_command('show run')
            print(output)

            prompt = connection.find_prompt()
            hostname = prompt[0:-1]

            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            output_directory = os.path.join(application_path, "Backup_1")
            os.makedirs(output_directory, exist_ok=True)
            filename = os.path.join(output_directory, f"{hostname}_{year}-{month}-{day}_BASE.txt")

            with open(filename, "w") as final:
                final.write(output)
                print(f"Backup of {hostname} completed successfully")
                print("#" * 30)

            print('Closing connection')
            connection.disconnect()

        except Exception as e:
            print(f"Failed to backup device {devices}. Error: {e}")
            print('#' * 30)


base_script()
