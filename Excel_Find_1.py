import pandas as pd
from pyxlsb import open_workbook as open_xlsb


def count_nexus_models_in_sheets(file_path, sheet_names):
    nexus_counts = {}
    with open_xlsb(file_path) as wb:
        for sheet_name in sheet_names:
            if sheet_name in wb.sheets:
                with wb.get_sheet(sheet_name) as sheet:
                    rows = list(sheet.rows())
                    df = pd.DataFrame([[item.v for item in row] for row in rows[1:]], columns=[item.v for item in rows[0]])

                    # Assuming 'Model' is one of the column headers
                    count = df['Model'].str.contains('FortiGate', na=False).sum()
                    nexus_counts[sheet_name] = count
            else:
                nexus_counts[sheet_name] = "Sheet not found"

    return nexus_counts


# Path to your Excel file
file_path = 'Master.xlsb'
sheet_names = ["Queens", "Bronx", "MTS", "Brooklyn", "Manhattan", "Staten Island"]

# Get the counts and print the results
counts = count_nexus_models_in_sheets(file_path, sheet_names)
for sheet_name, count in counts.items():
    print(f"Number of 'FortiGate' models in '{sheet_name}': {count}")
