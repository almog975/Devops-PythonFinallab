"""
stations.py - Station management module.
Handles viewing, adding, and updating lab stations.
"""

import ascii_art

# list of the only allowed status values
VALID_STATUSES = ["available", "occupied", "maintenance"]


def stations_menu(stations, users):
    """Show the stations sub-menu and keep it running until the user goes back."""
    print(ascii_art.STATIONS)
    while True:

        
        print("\n  === STATIONS MENU ===")
        print("\n  1. View All Stations")
        print("  2. Filter by Status")
        print("  3. Sort by Station ID")
        print("  4. Add New Station")
        print("  5. Update Station Status")
        print("  6. Update Hardware Specs")
        print("  0. Back to Main Menu")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            view_all_stations(stations)
        elif choice == "2":
            filter_stations_by_status(stations)
        elif choice == "3":
            sort_stations(stations)
        elif choice == "4":
            stations = add_station(stations)
        elif choice == "5":
            stations = update_station_status(stations)
        elif choice == "6":
            stations = update_hardware_specs(stations)
        elif choice == "0":
            break  
        else:
            print("  [!] Invalid option.")

    
    return stations

  # loop through each station and print one row
def view_all_stations(stations):
    """Display all stations in a table."""

    if len(stations) == 0:
        print("\n  No stations found.")
        return

  
    print("\n  ID       Name                 Status         OS           RAM      User")
    print("  " + "-" * 70)

    
    for sid, s in stations.items():
        user = s["assigned_user"]
        if user is None:
            user = "-"  

        hw = s["hardware"]
        print(f"  {sid:<8} {s['name']:<20} {s['status']:<14} {hw['os']:<12} {hw['ram']:<8} {user}")


def filter_stations_by_status(stations):
    """Show only stations that match a chosen status."""
    print("\n  Filter by:")
    print("\n  1. Available")
    print("  2. Occupied")
    print("  3. Maintenance")
    print("  0. Back to Main Menu")

    choice = input("\n  Enter your choice: ").strip()

    # convert the number choice into a status word
    if choice == "1":
        target = "available"
    elif choice == "2":
        target = "occupied"
    elif choice == "3":
        target = "maintenance"
    elif choice == "0":
        return
    else:
        print("  [!] Invalid choice.")
        return

    print(f"\n  Stations with status: {target}")
    print("  " + "-" * 40)

   
    found = False
    for sid, s in stations.items():
        if s["status"] == target:
            user = s["assigned_user"]
            if user is None:
                user = "-"
            print(f"  {sid:<8} {s['name']:<20} {user}")
            found = True

  
    if found == False:
        print(f"  No stations with status '{target}'.")


def sort_stations(stations):
    """Display all stations sorted by station ID."""
    if len(stations) == 0:
        print("\n  No stations to sort.")
        return

    # sorted() returns the keys in alphabetical order
    sorted_ids = sorted(stations.keys())
    print("\n  Stations sorted by ID:")
    print("  " + "-" * 40)

    for sid in sorted_ids:
        s = stations[sid]
        print(f"  {sid:<8} {s['name']:<20} {s['status']}")


def add_station(stations):
    """Ask the user for details and add a new station."""
    print("\n  === ADD NEW STATION ===")

 
    station_id = _get_unique_id(stations)
    name = _get_non_empty_input("  Station name: ")

    print("  Status options: available, occupied, maintenance")
    status = _get_valid_status()

   
    print("\n  Hardware Specs (press Enter to skip):")
    os_type = input("  OS (e.g. Windows 11): ").strip()
    ram = input("  RAM (e.g. 16GB): ").strip()
    cpu = input("  CPU (e.g. Intel i7): ").strip()
    storage = input("  Storage (e.g. 512GB SSD): ").strip()

    if os_type == "":
        os_type = "Unknown"
    if ram == "":
        ram = "Unknown"
    if cpu == "":
        cpu = "Unknown"
    if storage == "":
        storage = "Unknown"

    
    stations[station_id] = {
        "name": name,
        "status": status,
        "assigned_user": None, 
        "hardware": {
            "os": os_type,
            "ram": ram,
            "cpu": cpu,
            "storage": storage,
        },
    }

    print(f"\n  [+] Station '{station_id}' added!")
    return stations


def update_station_status(stations):
    """Change the status of an existing station."""
    if len(stations) == 0:
        print("\n  No stations available.")
        return stations

    # show the table first so the user can see the IDs
    view_all_stations(stations)
    station_id = input("\n  Enter Station ID to update: ").strip().upper()

    # check that the ID exists
    if station_id not in stations:
        print(f"  [!] Station '{station_id}' not found.")
        return stations

    current = stations[station_id]["status"]
    print(f"  Current status: {current}")
    print("  Options: available, occupied, maintenance")
    new_status = _get_valid_status()

    # if station becomes free or goes to maintenance, remove the user
    if new_status == "available" or new_status == "maintenance":
        stations[station_id]["assigned_user"] = None

    stations[station_id]["status"] = new_status
    print(f"  [+] Status updated to '{new_status}'.")
    return stations


def update_hardware_specs(stations):
    """Update the hardware details of an existing station."""
    if len(stations) == 0:
        print("\n  No stations available.")
        return stations

    view_all_stations(stations)
    station_id = input("\n  Enter Station ID to update: ").strip().upper()

    if station_id not in stations:
        print(f"  [!] Station '{station_id}' not found.")
        return stations

    
    hw = stations[station_id]["hardware"]
    print(f"\n  Current: OS={hw['os']}, RAM={hw['ram']}, CPU={hw['cpu']}, Storage={hw['storage']}")
    print("  Press Enter to keep the current value.\n")


    new_os = input(f"  OS [{hw['os']}]: ").strip()
    new_ram = input(f"  RAM [{hw['ram']}]: ").strip()
    new_cpu = input(f"  CPU [{hw['cpu']}]: ").strip()
    new_storage = input(f"  Storage [{hw['storage']}]: ").strip()

    # only update if the user actually typed something
    if new_os != "":
        stations[station_id]["hardware"]["os"] = new_os
    if new_ram != "":
        stations[station_id]["hardware"]["ram"] = new_ram
    if new_cpu != "":
        stations[station_id]["hardware"]["cpu"] = new_cpu
    if new_storage != "":
        stations[station_id]["hardware"]["storage"] = new_storage

    print(f"  [+] Hardware updated for station '{station_id}'.")
    return stations


# helper functions

def _get_unique_id(stations):
    """Keep asking until the user gives a station ID that does not already exist."""
    while True:
        sid = input("  Station ID (e.g. PC-01): ").strip().upper()
        if sid == "":
            print("  [!] ID cannot be empty.")
        elif sid in stations:
            # this ID is taken, ask again
            print(f"  [!] ID '{sid}' already exists.")
        else:
            return sid


def _get_non_empty_input(prompt):
    """Keep asking until the user types something."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("  [!] This field cannot be empty.")


def _get_valid_status():
    """Keep asking until the user types a valid status."""
    while True:
        status = input("  Status: ").strip().lower()
        if status in VALID_STATUSES:
            return status
        # the input was not one of the 3 allowed values
        print("  [!] Please enter: available, occupied, or maintenance")