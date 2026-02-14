import os

class LogEntry:
    def __init__(self, date, category, details):
        self.date = date
        self.category = category
        self.details = details

    def to_string(self):
        return f"{self.date} | {self.category} | {self.details}"

    def to_csv_format(self):
        return f"{self.date},{self.category},{self.details}\n"

class LogSystem:
    def __init__(self):
        self.logs_list = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(script_dir, "business_data.txt")

    def add_log(self, date, category, details):
        """Creates an object and adds it to the list."""
        new_log = LogEntry(date, category, details)
        self.logs_list.append(new_log)
        print("Log added to memory.")

    def save_to_file(self):
        """Writes the list to the file manually."""
        try:
            file = open(self.filename, "a")
            for log in self.logs_list:
                file.write(log.to_csv_format())
            file.close()
            print(f"Saved {len(self.logs_list)} entries to {self.filename}")
            self.logs_list = []
        except Exception as e:
            print(f"Error saving file: {e}")

    def read_from_file(self):
        """Reads the file and prints the history."""
        print(f"\n--- Reading History from {self.filename} ---")
        try:
            file = open(self.filename, "r")
            lines = file.readlines()
            file.close()

            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(",")
                    if len(parts) == 3:
                        print(f"Date: {parts[0]}   Type: {parts[1]}   Msg: {parts[2]}")
        except FileNotFoundError:
            print("No log file found yet.")

def main():
    system = LogSystem()
    
    while True:
        print("\n=== BUSINESS LOG MENU ===")
        print("1. Add New Log")
        print("2. Save Logs to File")
        print("3. View Log History")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ")

        if choice == "1":
            d = input("Enter Date (YYYY-MM-DD): ")
            c = input("Enter Category (Sales/Staff/Stock): ")
            msg = input("Enter Details: ")
            system.add_log(d, c, msg)
        
        elif choice == "2":
            system.save_to_file()
            
        elif choice == "3":
            system.read_from_file()
            
        elif choice == "4":
            print("Exiting system...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
