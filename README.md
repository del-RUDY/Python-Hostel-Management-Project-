# Hostel Management System

**Python Collaborative Project**  
Course: Computational Thinking and Programming (2026CSAE100)

A beginner-friendly console + GUI application to manage hostel students and rooms with **1 / 2 / 3 person sharing**, capacity-based allocation, search, room change, occupancy analysis, and CSV data storage.

---

## Team Members

| Member | Role |
|--------|------|
| **Rudarpartap Singh** (Team Leader) | Menu, integration, CSV save/load |
| **Pratiksha** | Student Registration |
| **Rakshit Anand** | project testing and validation |
| **Akshar Khajuria** | Student Search & Room Change |
| **Janhvi Gupta** | Room Management, Allocation & Analysis |

---

## Features

1. **Register Student** – Name, roll number, branch, year (duplicate roll check)
2. **Allocate Room** – Choose 1-person / 2-person / 3-person / any; allocate only if seats are free
3. **View Rooms** – Status + list of students living in each room
4. **View Students** – All registered students with room status
5. **Search Student** – Find by roll number
6. **Room Change** – Move student; free old seat; fill new seat
7. **Hostel Analysis** – Totals, free seats, occupancy %
8. **Save / Load CSV** – Data persists in `students.csv` and `rooms.csv`
9. **GUI (optional)** – Tkinter front-end with the same features

**Meaningful computational feature:** Capacity-based room allocation (search free seats → decide → update student + room records).

---

## How to Run

### Console version
```bash
python hostel_management.py
```

### GUI version
```bash
python hostel_gui.py
```
*(Requires Tkinter — included with standard Python on Windows/Mac. On Ubuntu: `sudo apt install python3-tk`)*

---

## Project Structure

```
├── hostel_management.py   # Main console program
├── hostel_gui.py          # Graphical front-end (Tkinter)
├── students.csv           # Saved student data (auto-created)
├── rooms.csv              # Saved room data (auto-created)
└── README.md
```

---

## Data Design (Beginner Python)

```python
# Each student: [Name, Roll Number, Branch, Year, Room Number]
students = [["Rahul", "24CS101", "CSE", 1, 101], ...]

# Each room: [Room Number, Capacity, Occupied Count]
rooms = [[101, 1, 0], [103, 2, 1], [201, 3, 2], ...]
```

A room stays **Available** until Occupied Count reaches Capacity.  
Example status: `Available (occupied by 2, 1 left)`

---

## Python Concepts Used

- `if` / `elif` / `else` — menu choices, availability checks  
- `while` loop — main menu  
- `for` loop — search and display  
- strings & type casting  
- lists and nested lists  
- functions (one per feature)  
- `csv` module — file storage  

No classes, databases, or advanced libraries — follows course guidelines.

---

## Course Details

- **Course:** Computational Thinking and Programming  
- **Code:** 2026CSAE100  
- **Institution:** Bennett University  
- **Milestone 1:** Project Proposal (done)  
- **Final evaluation:** Complete working project + report + viva  

---

## License

Academic project for coursework submission only.
