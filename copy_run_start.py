from netmiko import ConnectHandler
from getpass import getpass

def read_device_ips(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]

def send_command_to_device(device_ip, username, password, device_type='cisco_ios'):
    device = {
        'device_type': device_type,
        'ip': device_ip,
        'username': username,
        'password': password,
    }
    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command_timing("copy run start")
            if 'Destination filename' in output:
                output += net_connect.send_command_timing("\n")
            return output
    except Exception as e:
        return str(e)

def main():
    username = input("Enter your SSH username: ")
    password = getpass("Enter your SSH password: ")
    device_type = 'cisco_ios'  # Change this as per your device type
    device_file = 'devices.txt'  # The text file with device IPs

    device_ips = read_device_ips(device_file)
    for ip in device_ips:
        print(f"Sending 'copy run start' to {ip}")
        result = send_command_to_device(ip, username, password, device_type)
        print(result)

if __name__ == "__main__":
    main()
