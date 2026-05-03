# program that will enable the user to export the data
# Author: Stephen Kerr

import csv
import os
from datetime import datetime
from colorama import init, Fore 

init(autoreset=True) # initialize colorama

# function to export data to a csv file
def export_to_csv(filename, headers, data):

    try: 
        
        # create output folder if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        
        # add a timestamp to the filename to avoid overwriting existing files  
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        full_filename = os.path.join("output", f"{filename}_{timestamp}.csv")

        with open(full_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        print(Fore.GREEN + f"Data exported to {full_filename}")
    except Exception as e:
        print(Fore.RED + f"Error occurred while exporting data: {e}")