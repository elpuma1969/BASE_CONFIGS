from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

# Define the device connection parameters
ESW1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.11",
    "username": "puma",
    "password": "cisco",
}

NJ_CORE_1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.12",
    "username": "puma",
    "password": "cisco",
}

ESW10 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.110",
    "username": "puma",
    "password": "cisco",
}

BK_CORE_1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.100",
    "username": "puma",
    "password": "cisco",
}
# Create a thread pool with a maximum of 2 threads
with ThreadPoolExecutor(max_workers=2) as executor:
    # Submit the tasks to the thread pool
    task1 = executor.submit(ConnectHandler, **ESW1)
    task2 = executor.submit(ConnectHandler, **NJ_CORE_1)
    task3 = executor.submit(ConnectHandler, **ESW10)
    task4 = executor.submit(ConnectHandler, **BK_CORE_1)

# Get the results of the tasks
result1 = task1.result()
result2 = task2.result()
result3 = task3.result()
result4 = task4.result()

command_1 = ['line vty 0 4',
             'exec-timeout 15 30']

command_2 = ['line vty 0 4',
             'exec-timeout 15 30']

command_3 = ['line vty 0 4',
             'exec-timeout 15 30']

command_4 = ['int vlan 999', 'ip address 10.10.0.1 255.255.255', 'no shut']

# Use the results to send commands to the devices
output1 = result1.send_config_set(command_1)
output2 = result2.send_config_set(command_2)
output3 = result3.send_config_set(command_3)
output4 = result4.send_config_set(command_4)

# Print the results
print()
print("#" * 45)
print('Printing ESW1')
print("#" * 45)
print(output1)
print()
print("#" * 45)
print('Printing NJ_CORE_1')
print("#" * 45)
print(output2)
print()
print("#" * 45)
print('Printing ES10')
print("#" * 45)
print(output3)
print('Printing BK_CORE_1')
print("#" * 45)
print(output4)

# Disconnect from the devices
result1.disconnect()
result2.disconnect()
result3.disconnect()
result4.disconnect()
