"""
dummy_data.py - Data loader module.
Loads sample or saved data from an external JSON file into the app.
"""

import json
import os
import ascii_art

def load_dummy_data(stations, users, issues, categories):
    """Load data from a JSON file. User can choose to replace or append."""
    print(ascii_art.DUMMY_DATA)
    print("  === LOAD DATA ===")
    print("  1. Replace all existing data")
    print("  2. Append to existing data")

    choice = input("\n  Enter your choice: ").strip()

    if choice not in ("1", "2"):
        print("  [!] Invalid choice.")
        return stations, users, issues, categories

    # ask which file to load
    filename = input("  Enter filename to load (press Enter for 'dummy_data.json'): ").strip()

    # if the user just pressed Enter use the default file
    if filename == "":
        filename = "dummy_data.json"
    elif not filename.endswith(".json"):
        filename = filename + ".json"

    # check the file actually exists before trying to open it
    if not os.path.exists(filename):
        print(f"  [!] File '{filename}' not found.")
        return stations, users, issues, categories

    # open the file and read the JSON into a dict
    with open(filename, "r") as f:
        raw_data = json.load(f)

   
    raw_stations = raw_data.get("STATIONS", [])
    raw_users    = raw_data.get("USERS", [])
    raw_issues   = raw_data.get("ISSUES", [])


    if choice == "1":
        stations.clear()
        users.clear()
        issues.clear()
        categories.clear()
        print("  Existing data cleared.")

    # --- load stations ---
    loaded_stations = 0
    for s in raw_stations:
        sid = s["id"]
        # skip if this station ID already exists
        if sid not in stations:
            stations[sid] = {
                "name": s["name"],
                "status": s["status"],
                "assigned_user": s["assigned_user"],
                "hardware": s["hardware"],
            }
            loaded_stations += 1

    # --- load users ---
    loaded_users = 0

    # figure out the next ID to use
    if len(users) == 0:
        next_user_id = 1
    else:
        next_user_id = users[-1]["id"] + 1

    for u in raw_users:
        users.append({
            "id": next_user_id,
            "name": u["name"],
            "role": u["role"],
            "station": u["station"],
        })
        next_user_id += 1
        loaded_users += 1

    # --- load issues ---
    loaded_issues = 0

    if len(issues) == 0:
        next_issue_id = 1
    else:
        next_issue_id = issues[-1]["id"] + 1

    for iss in raw_issues:
        # only add the issue if the station it references a
        if iss["station_id"] in stations:
            issues.append({
                "id": next_issue_id,
                "station_id": iss["station_id"],
                "description": iss["description"],
                "severity": iss["severity"],
                "state": iss["state"],
                "resolution_note": iss["resolution_note"],
            })
            next_issue_id += 1
            loaded_issues += 1

 
    for s in stations.values():
        categories.add(s["hardware"]["os"])

    print(f"\n  [+] Loaded: {loaded_stations} stations, {loaded_users} users, {loaded_issues} issues from '{filename}'.")
    return stations, users, issues, categories