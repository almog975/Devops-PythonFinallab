"""
users.py - User management module.
Handles adding users and assigning them to stations.
"""

import ascii_art

def users_menu(users, stations):
    """Show the users sub-menu and keep it running until the user goes back."""
    print(ascii_art.USERS)
    while True:
      
        print("  === USERS MENU ===")
        print("  1. View All Users")
        print("  2. Add New User")
        print("  3. Assign User to Station")
        print("  4. Release User from Station")
        print("  5. Search User by Name")
        print("  6. Delete User")
        print("  0. Back to Main Menu")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            view_all_users(users)
        elif choice == "2":
            users = add_user(users)
        elif choice == "3":
            users, stations = assign_user(users, stations)
        elif choice == "4":
            users, stations = release_user(users, stations)
        elif choice == "5":
            search_user(users)
        elif choice == "6":
            users, stations = delete_user(users, stations)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid option.")

    return users, stations


def view_all_users(users):
    """Display all registered users in a table."""
    if not users:
        print("\n  No users registered yet.")
        return

    print("\n  ID     Name                   Role               Station")
    print("  " + "-" * 55)

    for u in users:
        station = u["station"] if u["station"] else "-"
        print(f"  {u['id']:<6} {u['name']:<22} {u['role']:<18} {station}")


def add_user(users):
    """Add a new user to the list."""
    print("\n  === ADD NEW USER ===")

    name = _get_non_empty_input("  Full name: ")
    role = _get_non_empty_input("  Role (e.g. Student, Technician, Instructor): ")

    new_id = 1 if not users else users[-1]["id"] + 1

    users.append({
        "id": new_id,
        "name": name,
        "role": role,
        "station": None,
    })

    print(f"\n  [+] User '{name}' added with ID {new_id}.")
    return users


def assign_user(users, stations):
    """Assign a user to an available station."""
    if not users:
        print("\n  No users registered yet.")
        return users, stations

    available_stations = [sid for sid, s in stations.items() if s["status"] == "available"]

    if not available_stations:
        print("\n  No available stations right now.")
        return users, stations

    view_all_users(users)
    user_id = _get_valid_number("  Enter User ID: ")
    user = _find_user(users, user_id)

    if not user:
        print("  [!] User not found.")
        return users, stations

    if user["station"]:
        print(f"  [!] This user is already assigned to station {user['station']}.")
        return users, stations

    print("\n  Available stations:")
    for sid in available_stations:
        print(f"  - {sid}  ({stations[sid]['name']})")

    station_id = input("\n  Enter Station ID: ").strip().upper()

    if station_id not in stations:
        print("  [!] Station not found.")
        return users, stations

    if stations[station_id]["status"] != "available":
        print("  [!] That station is not available.")
        return users, stations

    user["station"] = station_id
    stations[station_id]["status"] = "occupied"
    stations[station_id]["assigned_user"] = user["name"]

    print(f"  [+] {user['name']} assigned to {station_id}.")
    return users, stations


def release_user(users, stations):
    """Release a user from their station."""
    assigned = [u for u in users if u["station"]]

    if not assigned:
        print("\n  No users are currently assigned to a station.")
        return users, stations

    print("\n  Currently assigned users:")
    print("  " + "-" * 40)
    for u in assigned:
        print(f"  {u['id']:<6} {u['name']:<22} {u['station']}")

    user_id = _get_valid_number("\n  Enter User ID to release: ")
    user = _find_user(users, user_id)

    if not user or not user["station"]:
        print("  [!] User not found or not assigned to any station.")
        return users, stations

    old_station = user["station"]
    user["station"] = None

    if old_station in stations:
        stations[old_station]["status"] = "available"
        stations[old_station]["assigned_user"] = None

    print(f"  [+] {user['name']} released from {old_station}.")
    return users, stations


def search_user(users):
    """Search for a user by name."""
    if not users:
        print("\n  No users registered yet.")
        return

    query = input("  Search name: ").strip().lower()

    if not query:
        print("  [!] Search cannot be empty.")
        return

    print(f"\n  Results for '{query}':")
    print("  " + "-" * 50)

    found = False
    for u in users:
        if query in u["name"].lower():
            station = u["station"] if u["station"] else "-"
            print(f"  {u['id']:<6} {u['name']:<22} {u['role']:<18} {station}")
            found = True

    if not found:
        print(f"  No users found matching '{query}'.")


def delete_user(users, stations):
    """Remove a user by ID; free their station if they were assigned."""
    if not users:
        print("\n  No users registered yet.")
        return users, stations

    user_id = _get_valid_number("  Enter User ID: ")
    user = _find_user(users, user_id)

    if not user:
        print("  User not found.")
        return users, stations

    if user["station"]:
        sid = user["station"]
        if sid in stations:
            stations[sid]["status"] = "available"
            stations[sid]["assigned_user"] = None

    users.remove(user)
    print(f"  [+] User {user_id} deleted.")
    return users, stations


def _find_user(users, user_id):
    """Find a user by ID and return it, or None if not found."""
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def _get_non_empty_input(prompt):
    """Keep asking until the user types something."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] This field cannot be empty.")


def _get_valid_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            return int(raw)
        print("  [!] Please enter a number.")