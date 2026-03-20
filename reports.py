"""
reports.py - Reports and summary module.
Shows stats and overviews of stations, users, and issues.
"""

import ascii_art

def reports_menu(stations, users, issues):
    """Show the reports sub-menu and keep it running until the user goes back."""
    print(ascii_art.REPORTS)
    while True:
       
        print("  === REPORTS MENU ===")
        print("  1. Overall Dashboard")
        print("  2. Station Status Breakdown")
        print("  3. Issues Summary")
        print("  4. Hardware Overview")
        print("  0. Back to Main Menu")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            overall_dashboard(stations, users, issues)
        elif choice == "2":
            station_status_breakdown(stations)
        elif choice == "3":
            issues_summary(issues)
        elif choice == "4":
            hardware_overview(stations)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid option.")



  # collect all the numbers we need before printing the dashboard
    # we go through stations, users and issues and count everything first
    # only after all the counting is done we print the results at the bottom
def overall_dashboard(stations, users, issues):
    """Print a summary dashboard with key numbers."""
    total_stations = len(stations)
    available = 0
    occupied = 0
    maintenance = 0
    for s in stations.values():
        if s["status"] == "available":
            available += 1
        elif s["status"] == "occupied":
            occupied += 1
        else:
            maintenance += 1

    total_users = len(users)
    assigned_users = 0
    for u in users:
        if u["station"] is not None:
            assigned_users += 1

    
    total_issues = len(issues)
    open_issues = 0
    high_open = 0
    for i in issues:
        if i["state"] == "open":
            open_issues += 1
            if i["severity"] == "high":
                high_open += 1

   
    if total_stations > 0:
        utilization = (occupied / total_stations) * 100
    else:
        utilization = 0.0  

    print("\n  ========================================")
    print("           LAB MONITOR DASHBOARD")
    print("  ========================================")
    print(f"  Stations Total     : {total_stations}")
    print(f"  Available          : {available}")
    print(f"  Occupied           : {occupied}")
    print(f"  Maintenance        : {maintenance}")
    print(f"  Utilization        : {utilization:.1f}%")
    print("  ----------------------------------------")
    print(f"  Registered Users   : {total_users}")
    print(f"  Currently Assigned : {assigned_users}")
    print("  ----------------------------------------")
    print(f"  Total Issues       : {total_issues}")
    print(f"  Open Issues        : {open_issues}")
    print(f"  High Severity Open : {high_open}")
    print("  ========================================")


def station_status_breakdown(stations):
    """Show stations grouped by their status."""
    if not stations:
        print("\n  No stations available.")
        return

    available_list = [(sid, s) for sid, s in stations.items() if s["status"] == "available"]
    occupied_list = [(sid, s) for sid, s in stations.items() if s["status"] == "occupied"]
    maintenance_list = [(sid, s) for sid, s in stations.items() if s["status"] == "maintenance"]

    print(f"\n  AVAILABLE ({len(available_list)})")
    if not available_list:
        print("    none")
    for sid, s in available_list:
        print(f"    {sid:<10} {s['name']}")

    print(f"\n  OCCUPIED ({len(occupied_list)})")
    if not occupied_list:
        print("    none")
    for sid, s in occupied_list:
        user = s["assigned_user"] if s["assigned_user"] else "-"
        print(f"    {sid:<10} {s['name']:<20} -> {user}")

    print(f"\n  MAINTENANCE ({len(maintenance_list)})")
    if not maintenance_list:
        print("    none")
    for sid, s in maintenance_list:
        print(f"    {sid:<10} {s['name']}")


def issues_summary(issues):
    """Show issue counts broken down by severity."""
    if not issues:
        print("\n  No issues have been logged.")
        return

    print("\n  === ISSUES SUMMARY ===")

    for sev in ["high", "medium", "low"]:
        total = sum(1 for i in issues if i["severity"] == sev)
        open_count = sum(1 for i in issues if i["severity"] == sev and i["state"] == "open")
        resolved_count = total - open_count
        print(f"  {sev.upper():<10}  Total: {total}   Open: {open_count}   Resolved: {resolved_count}")

    print("\n  Open high severity issues:")
    found = False
    for i in issues:
        if i["severity"] == "high" and i["state"] == "open":
            print(f"    #{i['id']} | Station {i['station_id']} | {i['description'][:50]}")
            found = True
            
    if not found:
        print("    None - all clear!")


def hardware_overview(stations):
    """Display hardware specs for all stations."""
    if not stations:
        print("\n  No stations available.")
        return

    print("\n  Station    Name                 OS             RAM        CPU")
    print("  " + "-" * 72)

    for sid, s in stations.items():
        hw = s["hardware"]
        print(f"  {sid:<10} {s['name']:<20} {hw['os']:<14} {hw['ram']:<10} {hw['cpu']}")

    os_types = {s["hardware"]["os"] for s in stations.values()}

    print("\n  Unique OS types in the lab:")
    for os_name in os_types:
        print(f"    - {os_name}")