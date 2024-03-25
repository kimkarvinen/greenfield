import os # to work with file paths
import subprocess 

def edit_rd5000(trans_date, invoice_or):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        backup_filename = os.path.join(script_dir, "rd5000_backup.txt")
        new_filename = os.path.join(script_dir, "rd5000.txt")
        
        with open(backup_filename, 'r') as file:
            lines = file.readlines()
        
        for i, line in enumerate(lines):
            parts = line.split('\t')  # Split the line by tabs
            
            # Replace date
            for j, part in enumerate(parts):
                if "yyyy-mm-dd" in part:
                    parts[j] = part.replace("yyyy-mm-dd", trans_date)  # Replace "yyyy-mm-dd" with the input date
            
            # Replace invoice number
            for j, part in enumerate(parts):
                if part.strip() == "01234567":  # invoice number source backup
                    parts[j] = invoice_or  # Replace the invoice number with the error invoice
            
            lines[i] = '\t'.join(parts)  # Join the modified parts back into a line
        
        with open(new_filename, 'w') as file:
            file.writelines(lines)
        
        print(f"File {new_filename} has been edited successfully.")
        
        # Use double backslashes in the file path for Windows
        new_filename = new_filename.replace('\\', '\\\\')
        
        # MySQL commands to use the database and load data
        mysql_commands = f"""
        USE tsceressql;
        LOAD DATA INFILE "{new_filename}" INTO TABLE rd5000;
        """
        
        print("Please wait... Executing commands:")
        print(mysql_commands)
        
        # Execute MySQL commands
        result = subprocess.run(["D:\\MYSQL\\BIN\\MYSQL.EXE"], input=mysql_commands.encode(), shell=True, capture_output=True)
        
        if result.returncode == 0:
            print("Fix has been executed successfully. Please Regenerate and re-submit the error sales file")
            input("press any key to exit")
        else:
            print("Please double check your entry")
            print("Error output:")
            print(result.stderr.decode())
        
    except FileNotFoundError:
        print(f"File {backup_filename} not found.")

if __name__ == "__main__":
    print("Please carefully double check your input")
    trans_date = input("Enter the error date (yyyy-mm-dd): ")
    invoice_or = input("Enter the invoice error (01234567): ")
    edit_rd5000(trans_date, invoice_or)
