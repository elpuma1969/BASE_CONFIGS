from netmiko import ConnectHandler

devices = ['192.168.122.11', '192.168.122.12', '192.168.122.110', '192.168.122.100']

# Create an empty list to store the output for each device
all_device_output = []

for device in devices:
    ip_address_of_device = device
    cisco = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': 'puma',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    }

    try:
        netconnect = ConnectHandler(**cisco)
        print(f'Connected to device: {device}')

        output = netconnect.send_command('sh ip int br | in Vlan')
        
        # Append the output to the list
        all_device_output.append((device, output))

        netconnect.disconnect()
    except Exception as e:
        print(f'Error connecting to {device}: {str(e)}')

# Print the output for all devices after the loop
for device, output in all_device_output:
    print(f'Output from {device}:\n{output}\n')
