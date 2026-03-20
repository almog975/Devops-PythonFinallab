# Lab Station Monitor
DevOps Bootcamp - Python Final Lab

---
## Motivation for this tool
This tool has been created as this is really a tool that I need as my work as lab manager,
I did something similar, and use it on my daily work with WebServer 




## What is this project

This is a terminalbased tool for managing a computer lab.
You can track stations, users, and technical issues all from one place.
The program runs in the terminal and uses a simple number menu to navigate.

---

## How to run it

Run the following command in your terminal:
python3 main.py

Make sure all the files are in the same folder before running.

---

## Files in this project

| File | What it does |
|---|---|
| `main.py` | Starts the program, shows the main menu, and handles data saving 
| `stations.py` | Add and manage lab stations |
| `users.py` | Register users and assign them to stations |
| `issues.py` | Log and resolve technical issues |
| `reports.py` | View stats and summarias
| `dummy_data.py` | Loads sample data into the program |
| `dummy_data.json` | Holds the actual sample data in JSON format |
| `ascii_art.py` | Holds all the ASCII art used in the program |

---

## Features

- View all stations with their status and hardware info
- Filter and sort stations by status or ID
- Add new stations with custom hardware specs
- Register users and assign them to available stations
- Log issues with low / medium / high severity
- Resolve issues and add a resolution note
- High severity issues automatically flag the station as maintenance
- Dashboard report with live counts and utilization percentage
- Load sample data from an external JSON file
- Export and save current lab data to a local JSON file

---

## Data structures used

- `stations` - dictionary where the key is the station ID 
- `users` - list of user dictionaries
- `issues` - list of issue dictionaries
- `categories` - set of unique OS types (no duplicates)

---

## Sample data

The dummy data includes stations, users, and issues stored in `dummy_data.json`.


---
## Open for contribution

Hey if you want to contribute to this project here are 3 small features i didnt get to implement yet.
they are all pretty simple and each one is in a single file so you dont need to understand the whole project to do them.

---

### Feature 1 – Search station by ID

go into `stations.py` and add a new menu option that asks the user to type a station ID and then prints that station's details.
you can look at the `view_all_stations()` function to see how i print station info and just do the same thing for one station.
if the ID doesnt exist just print: `Station not found.`

---

### Feature 2 – Filter issues by severity

go into `issues.py` and add a menu option that asks the user to pick a severity - `high`, `medium` or `low` - and then prints all the issues that match.
just loop through the `issues` list and check the `"severity"` field on each one.
if nothing matches print: `No issues found for that severity.`

---

### Feature 3 – Delete a user

go into `users.py` and add a menu option that asks for a User ID and deletes that user from the `users` list.
one thing to be careful about - if the user is assigned to a station you need to set that station's `"status"` back to `"available"` and `"assigned_user"` back to `None` before removing them.
if the ID doesnt exist print: `User not found.`



