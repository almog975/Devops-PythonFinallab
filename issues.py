"""
issues.py - Issues and incidents module.
Log, view, filter, and resolve station issues.
"""

import ascii_art

# list of allowed severity values
VALID_SEVERITIES = ["low", "medium", "high"]

def issues_menu(issues, stations):
    """Show the issues sub-menu and keep it running until the user goes back."""
    print(ascii_art.ISSUES)
    while True:
        # count how many issues are still open
        open_count = 0
        for i in issues:
            if i["state"] == "open":
                open_count += 1

        # print the issues art and the menu
       
        print(f"  === ISSUES MENU ===  ({open_count} open)")
        print("  1. View All Issues")
        print("  2. Filter by Severity")
        print("  3. Filter by State (open / resolved)")
        print("  4. Log New Issue")
        print("  5. Resolve an Issue")
        print("  0. Back to Main Menu")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            view_all_issues(issues)
        elif choice == "2":
            filter_by_severity(issues)
        elif choice == "3":
            filter_by_state(issues)
        elif choice == "4":
            issues = log_issue(issues, stations)
        elif choice == "5":
            issues = resolve_issue(issues)
        elif choice == "0":
            break  # go back to main menu
        else:
            print("  [!] Invalid option.")

    # send back the updated issues list
    return issues


def view_all_issues(issues):
    """Show all logged issues."""
    if len(issues) == 0:
        print("\n  No issues logged yet.")
        return

    # use the helper to print the table
    _print_issues_table(issues)


def filter_by_severity(issues):
    """Show only issues with a chosen severity."""
    if len(issues) == 0:
        print("\n  No issues logged yet.")
        return

    print("\n  Filter by severity:")
    print("  1. Low")
    print("  2. Medium")
    print("  3. High")

    choice = input("\n  Enter your choice: ").strip()

    # convert the number choice into a severity word
    if choice == "1":
        target = "low"
    elif choice == "2":
        target = "medium"
    elif choice == "3":
        target = "high"
    else:
        print("  [!] Invalid choice.")
        return

    # build a new list with only the matching issues
    filtered = []
    for i in issues:
        if i["severity"] == target:
            filtered.append(i)

    if len(filtered) == 0:
        print(f"  No {target} severity issues found.")
        return

    print(f"\n  Showing {target} severity issues:")
    _print_issues_table(filtered)


def filter_by_state(issues):
    """Show only open or only resolved issues."""
    if len(issues) == 0:
        print("\n  No issues logged yet.")
        return

    print("\n  Filter by state:")
    print("  1. Open")
    print("  2. Resolved")

    choice = input("\n  Enter your choice: ").strip()

    # convert the number choice into a state word
    if choice == "1":
        target = "open"
    elif choice == "2":
        target = "resolved"
    else:
        print("  [!] Invalid choice.")
        return

    # build a new list with only the matching issues
    filtered = []
    for i in issues:
        if i["state"] == target:
            filtered.append(i)

    if len(filtered) == 0:
        print(f"  No {target} issues found.")
        return

    print(f"\n  Showing {target} issues:")
    _print_issues_table(filtered)


def log_issue(issues, stations):
    """Log a new issue for a station."""
    if len(stations) == 0:
        print("\n  No stations exist yet.")
        return issues

    print("\n  === LOG NEW ISSUE ===")

    # show all stations so the user can pick one
    print("\n  Stations:")
    print("  " + "-" * 35)
    for sid, s in stations.items():
        print(f"  {sid:<10} {s['name']:<20} {s['status']}")

    station_id = input("\n  Enter Station ID: ").strip().upper()

    if station_id not in stations:
        print("  [!] Station not found.")
        return issues

    description = _get_non_empty_input("  Description: ")

    print("  Severity options: low, medium, high")
    severity = _get_valid_severity()

    # generate next issue ID
    if len(issues) == 0:
        new_id = 1
    else:
        new_id = issues[-1]["id"] + 1

    # add the new issue to the list
    issues.append({
        "id": new_id,
        "station_id": station_id,
        "description": description,
        "severity": severity,
        "state": "open",          
        "resolution_note": None,   
    })

    # if the issue is serious, flag the station for maintenance
    if severity == "high":
        stations[station_id]["status"] = "maintenance"
        print(f"  [!] Station '{station_id}' flagged as maintenance (high severity).")

    print(f"  [+] Issue #{new_id} logged for station {station_id}.")
    return issues


def resolve_issue(issues):
    """Mark an open issue as resolved."""

    # build a list of only the open issues
    open_issues = []
    for i in issues:
        if i["state"] == "open":
            open_issues.append(i)

    if len(open_issues) == 0:
        print("\n  No open issues to resolve.")
        return issues

    print("\n  Open issues:")
    _print_issues_table(open_issues)

    issue_id = _get_valid_number("\n  Enter Issue ID to resolve: ")
    issue = _find_issue(issues, issue_id)

    if issue is None:
        print("  [!] Issue not found.")
        return issues

    if issue["state"] == "resolved":
        print("  [!] That issue is already resolved.")
        return issues

  
    note = input("  Resolution note (optional): ").strip()

    # update the issue state
    issue["state"] = "resolved"

    # if the user left the note empty use a default message
    if note == "":
        issue["resolution_note"] = "Resolved."
    else:
        issue["resolution_note"] = note

    print(f"  [+] Issue #{issue_id} marked as resolved.")
    return issues


# helper functions

def _print_issues_table(issues):
    """Print a table of issues."""
    print("\n  #     Station    Severity   State        Description")
    print("  " + "-" * 65)

    for i in issues:
        
        desc = i["description"]
        if len(desc) > 35:
            desc = desc[:35] + "..."

        print(f"  {i['id']:<5} {i['station_id']:<10} {i['severity']:<10} {i['state']:<12} {desc}")


def _find_issue(issues, issue_id):
    """Find an issue by ID and return it, or None if not found."""
    for i in issues:
        if i["id"] == issue_id:
            return i
    return None  


def _get_non_empty_input(prompt):
    """Keep asking until the user types something."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("  [!] This field cannot be empty.")


def _get_valid_severity():
    """Keep asking until the user types a valid severity."""
    while True:
        sev = input("  Severity: ").strip().lower()
        if sev in VALID_SEVERITIES:
            return sev
        print("  [!] Please enter: low, medium, or high")


def _get_valid_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            return int(raw)  
        print("  [!] Please enter a number.")