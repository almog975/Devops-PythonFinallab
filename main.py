"""
main.py - Main entry point for the Lab Station Monitor.
"""

import json
from stations import stations_menu
from users import users_menu
from issues import issues_menu
from reports import reports_menu
from dummy_data import load_dummy_data
import ascii_art

def initialize_data():
    """Create the empty data structures before the program starts."""
    stations = {}
    users = []
    issues = []
    categories = set()
    return stations, users, issues, categories


def print_banner():
    """Print the banner when the program starts."""
    print(ascii_art.BANNER)
    print("  ------------------------------------------")
    print("  DevOps Bootcamp - Python Final Lab")
    print("  ------------------------------------------\n")

# main func for station part, count each status and print the stats
def print_main_menu(stations):
    """Show the main menu and current station stats."""
    total = len(stations)

    available = 0
    occupied = 0
    maintenance = 0
    for station in stations.values():
        if station["status"] == "available":
            available += 1
        elif station["status"] == "occupied":
            occupied += 1
        else:
            maintenance += 1

    print(f"  Total stations: {total}  |  Available: {available}  Occupied: {occupied}  Maintenance: {maintenance}\n")

    print("  === MAIN MENU ===")
    print("  1. View Stations")
    print("  2. Manage Users")
    print("  3. Issues and Incidents")
    print("  4. Reports and Summary")
    print("  5. Load Dummy Data")
    print("  6. Save Data to File")
    print("  0. Exit")
    print()


def save_to_file(stations, users, issues):
    """Save all current data to a JSON file."""

    if not stations and not users and not issues:
        print("\n  Nothing to save - no data loaded yet.")
        return

    filename = input("  Enter filename to save (e.g. backup): ").strip()

    if filename == "":
        print("  [!] Filename cannot be empty.")
        return

    # add .json at the end in any case(no duplicate .json)
    if not filename.endswith(".json"):
        filename = filename + ".json"


    stations_list = []
    for sid, s in stations.items():
        
        station_dict = {
            "id": sid,
            "name": s["name"],
            "status": s["status"],
            "assigned_user": s["assigned_user"],
            "hardware": s["hardware"],
        }
        stations_list.append(station_dict)

   
    data_to_save = {
        "STATIONS": stations_list,
        "USERS": users,
        "ISSUES": issues,
    }

    
    try:
      
        f = open(filename, "w")

        json.dump(data_to_save, f, indent=4)
   
        f.close()
    
        print(f"\n  [+] Data saved to '{filename}'.")
        print(f"      Stations: {len(stations_list)}  Users: {len(users)}  Issues: {len(issues)}")

    except OSError as e:
        print(f"  [!] Could not save file: {e}")

def main():
    """Start the program, initialize data, and run the main loop."""
    stations, users, issues, categories = initialize_data()
    print_banner()

    while True:
        print_main_menu(stations)
        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            stations = stations_menu(stations, users)
        elif choice == "2":
            users, stations = users_menu(users, stations)
        elif choice == "3":
            issues = issues_menu(issues, stations)
        elif choice == "4":
            reports_menu(stations, users, issues)
        elif choice == "5":
            stations, users, issues, categories = load_dummy_data(
                stations, users, issues, categories
            )
        elif choice == "6":
            save_to_file(stations, users, issues)
        elif choice == "0":
            print(ascii_art.GOODBYE)
            break
        else:
            print("  [!] Invalid option. Please enter a number from the menu.")

if __name__ == "__main__":
    main()