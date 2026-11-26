# ============================================================
# HOSTEL MANAGEMENT SYSTEM - FINAL PROJECT
# Course: Computational Thinking and Programming (2026CSAE100)
#
# Team:
#   Rudarpartap Singh (Team Leader) - Menu & Integration, CSV save/load
#   Pratiksha                       - Student Registration
#   Rakshit Anand                   - Room Management & Allocation
#   Akshar Khajuria                 - Student Search & Room Change
#   Janhvi Gupta                    - Hostel Analysis, Testing & Validation
#
# Concepts used:
#   - lists and nested lists
#   - if / elif / else
#   - while loop (main menu)
#   - for loop (search / display)
#   - strings and type casting
#   - functions
#   - csv module (file storage)
# ============================================================

import csv
import os

# ---------- DATA STORAGE (nested lists) ----------
# Each student: [Name, Roll Number, Branch, Year, Room Number]
students = []

# Each room: [Room Number, Capacity, Occupied Count]
# Capacity 1 = single, 2 = double, 3 = triple
rooms = [
    [101, 1, 0],
    [102, 1, 0],
    [103, 2, 0],
    [104, 2, 0],
    [105, 2, 0],
    [201, 3, 0],
    [202, 3, 0],
    [203, 3, 0],
]

STUDENTS_FILE = "students.csv"
ROOMS_FILE = "rooms.csv"


# ---------- HELPER FUNCTIONS ----------

def get_room_status(room):
    capacity = room[1]
    occupied = room[2]
    left = capacity - occupied
    if occupied == 0:
        return "Available (empty, " + str(capacity) + " seats)"
    elif occupied < capacity:
        return "Available (occupied by " + str(occupied) + ", " + str(left) + " left)"
    else:
        return "Fully Occupied (" + str(occupied) + "/" + str(capacity) + ")"


def sharing_label(capacity):
    if capacity == 1:
        return "1-person (single)"
    return str(capacity) + "-person sharing"


def get_students_in_room(room_no):
    names = []
    for s in students:
        if s[4] == room_no:
            names.append(s[0] + " (" + s[1] + ")")
    return names


def find_student_index(roll):
    for i in range(len(students)):
        if students[i][1] == roll:
            return i
    return -1


def find_room_index(room_no):
    for i in range(len(rooms)):
        if rooms[i][0] == room_no:
            return i
    return -1


# ---------- CSV SAVE / LOAD ----------

def save_data():
    """Save students and rooms to CSV files."""
    with open(STUDENTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Roll", "Branch", "Year", "Room"])
        for s in students:
            room_val = s[4] if s[4] is not None else ""
            writer.writerow([s[0], s[1], s[2], s[3], room_val])

    with open(ROOMS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["RoomNo", "Capacity", "Occupied"])
        for r in rooms:
            writer.writerow([r[0], r[1], r[2]])

    print("Data saved to", STUDENTS_FILE, "and", ROOMS_FILE)


def load_data():
    """Load students and rooms from CSV files if they exist."""
    global students, rooms

    if os.path.exists(STUDENTS_FILE):
        students = []
        with open(STUDENTS_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 5:
                    room_val = int(row[4]) if row[4].isdigit() else None
                    year_val = int(row[3]) if row[3].isdigit() else 1
                    students.append([row[0], row[1], row[2], year_val, room_val])
        print("Loaded", len(students), "students from file.")

    if os.path.exists(ROOMS_FILE):
        rooms = []
        with open(ROOMS_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    rooms.append([int(row[0]), int(row[1]), int(row[2])])
        print("Loaded", len(rooms), "rooms from file.")


# ---------- FEATURE FUNCTIONS ----------

def show_menu():
    print("\n" + "=" * 48)
    print("   HOSTEL MANAGEMENT SYSTEM - FINAL")
    print("=" * 48)
    print("1. Register Student")
    print("2. Allocate Room")
    print("3. View Rooms (with students)")
    print("4. View Students")
    print("5. Search Student")
    print("6. Room Change")
    print("7. Hostel Analysis")
    print("8. Save Data")
    print("9. Exit")
    print("=" * 48)


def register_student():
    print("\n--- Student Registration ---")
    name = input("Enter Student Name: ").strip()
    if name == "":
        print("Name cannot be empty.")
        return
    roll = input("Enter Roll Number: ").strip()
    if roll == "":
        print("Roll number cannot be empty.")
        return
    branch = input("Enter Branch: ").strip()
    if branch == "":
        print("Branch cannot be empty.")
        return

    year_text = input("Enter Year (1/2/3/4): ").strip()
    if year_text.isdigit() and int(year_text) in [1, 2, 3, 4]:
        year = int(year_text)
    else:
        print("Invalid year. Using year = 1.")
        year = 1

    if find_student_index(roll) != -1:
        print("Error: A student with this roll number already exists.")
        return

    students.append([name, roll, branch, year, None])
    print("Student registered successfully!")
    print("Name:", name, "| Roll:", roll, "| Branch:", branch, "| Year:", year)


def show_available_rooms(preferred_capacity=None):
    print("\nRooms with free seats:")
    found = False
    for room in rooms:
        capacity = room[1]
        occupied = room[2]
        if occupied >= capacity:
            continue
        if preferred_capacity is not None and capacity != preferred_capacity:
            continue
        status = get_room_status(room)
        print("  Room", room[0], "-", sharing_label(capacity), "-", status)
        found = True
    if not found:
        if preferred_capacity is not None:
            print("  No", preferred_capacity, "-person rooms with free seats.")
        else:
            print("  No rooms with free seats.")
    return found


def allocate_room():
    print("\n--- Room Allocation ---")
    if len(students) == 0:
        print("No students registered yet. Please register a student first.")
        return

    print("\nStudents without a room:")
    pending = 0
    for s in students:
        if s[4] is None:
            print("  ", s[1], "-", s[0])
            pending += 1
    if pending == 0:
        print("All registered students already have rooms.")
        return

    roll = input("\nEnter Roll Number of student to allocate room: ").strip()
    student_index = find_student_index(roll)
    if student_index == -1:
        print("Student not found.")
        return
    if students[student_index][4] is not None:
        print("This student already has room:", students[student_index][4])
        return

    print("\nRoom sharing options:")
    print("  1. 1-person (single) room")
    print("  2. 2-person sharing")
    print("  3. 3-person sharing")
    print("  4. Any available room")
    share_choice = input("Enter choice (1/2/3/4): ").strip()

    preferred_capacity = None
    if share_choice == "1":
        preferred_capacity = 1
    elif share_choice == "2":
        preferred_capacity = 2
    elif share_choice == "3":
        preferred_capacity = 3
    elif share_choice != "4":
        print("Invalid choice. Showing all available rooms.")

    if not show_available_rooms(preferred_capacity):
        return

    room_text = input("\nEnter room number to allocate: ").strip()
    if not room_text.isdigit():
        print("Invalid room number.")
        return
    room_no = int(room_text)
    room_index = find_room_index(room_no)
    if room_index == -1:
        print("Room not found.")
        return

    capacity = rooms[room_index][1]
    occupied = rooms[room_index][2]

    if preferred_capacity is not None and capacity != preferred_capacity:
        print("Room", room_no, "is a", capacity, "-person room, not a", preferred_capacity, "-person room.")
        return
    if occupied >= capacity:
        print("Room", room_no, "is Fully Occupied.")
        return

    rooms[room_index][2] = occupied + 1
    students[student_index][4] = room_no
    new_occupied = rooms[room_index][2]
    left = capacity - new_occupied
    print("Room", room_no, "allocated successfully to", students[student_index][0] + "!")
    if left > 0:
        print("Status now: Available (occupied by", new_occupied, ",", left, "left)")
    else:
        print("Status now: Fully Occupied (" + str(new_occupied) + "/" + str(capacity) + ")")


def view_rooms():
    print("\n--- All Rooms (with students allotted) ---")
    print("-" * 55)
    for room in rooms:
        room_no = room[0]
        capacity = room[1]
        status = get_room_status(room)
        print("Room", room_no, "|", sharing_label(capacity), "|", status)
        occupants = get_students_in_room(room_no)
        if len(occupants) == 0:
            print("   Students: (none)")
        else:
            print("   Students:")
            for name in occupants:
                print("      -", name)
        print("-" * 55)


def view_students():
    print("\n--- Registered Students ---")
    if len(students) == 0:
        print("No students registered yet.")
        return
    print("Name           | Roll No.   | Branch | Year | Room")
    print("-" * 55)
    for s in students:
        room_display = s[4] if s[4] is not None else "Not Allocated"
        print(s[0], "|", s[1], "|", s[2], "|", s[3], "|", room_display)


def search_student():
    print("\n--- Search Student ---")
    if len(students) == 0:
        print("No students registered yet.")
        return
    roll = input("Enter Roll Number to search: ").strip()
    index = find_student_index(roll)
    if index == -1:
        print("Student not found.")
        return
    s = students[index]
    print("\nStudent Found:")
    print("  Name   :", s[0])
    print("  Roll   :", s[1])
    print("  Branch :", s[2])
    print("  Year   :", s[3])
    if s[4] is None:
        print("  Room   : Not Allocated")
    else:
        print("  Room   :", s[4])
        room_index = find_room_index(s[4])
        if room_index != -1:
            print("  Type   :", sharing_label(rooms[room_index][1]))
            print("  Status :", get_room_status(rooms[room_index]))


def room_change():
    print("\n--- Room Change ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    roll = input("Enter Roll Number of student: ").strip()
    student_index = find_student_index(roll)
    if student_index == -1:
        print("Student not found.")
        return

    old_room = students[student_index][4]
    if old_room is None:
        print("This student has no room yet. Use Allocate Room instead.")
        return

    print("Current room of", students[student_index][0] + ":", old_room)

    print("\nRoom sharing options for new room:")
    print("  1. 1-person (single) room")
    print("  2. 2-person sharing")
    print("  3. 3-person sharing")
    print("  4. Any available room")
    share_choice = input("Enter choice (1/2/3/4): ").strip()

    preferred_capacity = None
    if share_choice == "1":
        preferred_capacity = 1
    elif share_choice == "2":
        preferred_capacity = 2
    elif share_choice == "3":
        preferred_capacity = 3

    if not show_available_rooms(preferred_capacity):
        return

    room_text = input("\nEnter new room number: ").strip()
    if not room_text.isdigit():
        print("Invalid room number.")
        return
    new_room_no = int(room_text)

    if new_room_no == old_room:
        print("Student is already in this room.")
        return

    new_room_index = find_room_index(new_room_no)
    if new_room_index == -1:
        print("Room not found.")
        return

    capacity = rooms[new_room_index][1]
    occupied = rooms[new_room_index][2]

    if preferred_capacity is not None and capacity != preferred_capacity:
        print("Room", new_room_no, "is a", capacity, "-person room, not a", preferred_capacity, "-person room.")
        return
    if occupied >= capacity:
        print("Room", new_room_no, "is Fully Occupied.")
        return

    # Free old room
    old_room_index = find_room_index(old_room)
    if old_room_index != -1 and rooms[old_room_index][2] > 0:
        rooms[old_room_index][2] = rooms[old_room_index][2] - 1

    # Assign new room
    rooms[new_room_index][2] = occupied + 1
    students[student_index][4] = new_room_no

    print("Room changed successfully!")
    print(students[student_index][0], "moved from Room", old_room, "to Room", new_room_no)
    print("New status:", get_room_status(rooms[new_room_index]))


def hostel_analysis():
    print("\n--- Hostel Analysis ---")
    total_students = len(students)
    allocated = 0
    for s in students:
        if s[4] is not None:
            allocated += 1
    not_allocated = total_students - allocated

    total_rooms = len(rooms)
    total_seats = 0
    occupied_seats = 0
    single = double = triple = 0
    full_rooms = 0

    for r in rooms:
        total_seats += r[1]
        occupied_seats += r[2]
        if r[1] == 1:
            single += 1
        elif r[1] == 2:
            double += 1
        else:
            triple += 1
        if r[2] >= r[1]:
            full_rooms += 1

    free_seats = total_seats - occupied_seats
    if total_seats > 0:
        occupancy_pct = round((occupied_seats / total_seats) * 100, 1)
    else:
        occupancy_pct = 0.0

    print("STUDENTS")
    print("  Total students     :", total_students)
    print("  With room          :", allocated)
    print("  Without room       :", not_allocated)
    print()
    print("ROOMS")
    print("  Total rooms        :", total_rooms)
    print("  1-person rooms     :", single)
    print("  2-person rooms     :", double)
    print("  3-person rooms     :", triple)
    print("  Fully occupied     :", full_rooms)
    print()
    print("SEATS / OCCUPANCY")
    print("  Total seats        :", total_seats)
    print("  Occupied seats     :", occupied_seats)
    print("  Free seats         :", free_seats)
    print("  Occupancy %        :", str(occupancy_pct) + "%")


# ---------- MAIN PROGRAM ----------

def main():
    print("Welcome to Hostel Management System")
    print("Final Project - Supports 1/2/3 person rooms + CSV storage")
    load_data()

    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            allocate_room()
        elif choice == "3":
            view_rooms()
        elif choice == "4":
            view_students()
        elif choice == "5":
            search_student()
        elif choice == "6":
            room_change()
        elif choice == "7":
            hostel_analysis()
        elif choice == "8":
            save_data()
        elif choice == "9":
            save_data()
            print("\nData saved. Thank you for using Hostel Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
