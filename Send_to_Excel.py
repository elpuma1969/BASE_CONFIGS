import pandas as pd
import glob
import os


def convert_text_to_excel(text_files):
    excel_file = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    for file in text_files:
        with open(file, 'r') as f:
            lines = f.readlines()

        device_data = {
            'Interface': [],
            'Status': [],
            'VLAN': [],
            'Duplex': [],
            'Speed': [],
            'Type': []
        }

        for line in lines:
            line = line.strip()
            if line.startswith('Gi') or line.startswith('Fa'):
                interface_info = line.split()
                device_data['Interface'].append(interface_info[0])
                device_data['Status'].append(interface_info[1])
                vlan = interface_info[2] if interface_info[2] != 'notconnect' else ''
                device_data['VLAN'].append(vlan)
                device_data['Duplex'].append(interface_info[3])
                device_data['Speed'].append(interface_info[4])
                device_data['Type'].append(interface_info[5])

        df = pd.DataFrame(device_data)

        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(file))[0]

        # Truncate the filename if necessary
        sheet_name = filename[:31]

        # Save the DataFrame to a sheet in the Excel file
        df.to_excel(excel_file, sheet_name=sheet_name, index=False)

    excel_file.close()


# Specify the path to the directory containing the text files
text_files_path = 'cisco_outcome/*.txt'

# Get a list of all text files in the directory
text_files = glob.glob(text_files_path)

# Call the function to convert text files to Excel files
convert_text_to_excel(text_files)

print('Done')
