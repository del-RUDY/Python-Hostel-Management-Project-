# ============================================================
# HOSTEL MANAGEMENT SYSTEM - GRAPHICAL FRONT END (FINAL)
# Tkinter GUI | Course: 2026CSAE100
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

students = []
rooms = [
    [101, 1, 0], [102, 1, 0],
    [103, 2, 0], [104, 2, 0], [105, 2, 0],
    [201, 3, 0], [202, 3, 0], [203, 3, 0],
]
STUDENTS_FILE = "students.csv"
ROOMS_FILE = "rooms.csv"


def get_room_status(room):
    capacity, occupied = room[1], room[2]
    left = capacity - occupied
    if occupied == 0:
        return "Available (empty, " + str(capacity) + " seats)"
    elif occupied < capacity:
        return "Available (occupied by " + str(occupied) + ", " + str(left) + " left)"
    return "Fully Occupied (" + str(occupied) + "/" + str(capacity) + ")"


def sharing_label(capacity):
    if capacity == 1:
        return "1-person (single)"
    return str(capacity) + "-person sharing"


def get_students_in_room(room_no):
    return [s[0] + " (" + s[1] + ")" for s in students if s[4] == room_no]


def find_student_index(roll):
    for i, s in enumerate(students):
        if s[1] == roll:
            return i
    return -1


def find_room_index(room_no):
    for i, r in enumerate(rooms):
        if r[0] == room_no:
            return i
    return -1


def save_data():
    with open(STUDENTS_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Roll", "Branch", "Year", "Room"])
        for s in students:
            w.writerow([s[0], s[1], s[2], s[3], s[4] if s[4] is not None else ""])
    with open(ROOMS_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["RoomNo", "Capacity", "Occupied"])
        for r in rooms:
            w.writerow([r[0], r[1], r[2]])


def load_data():
    global students, rooms
    if os.path.exists(STUDENTS_FILE):
        students = []
        with open(STUDENTS_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 5:
                    room_val = int(row[4]) if row[4].isdigit() else None
                    year_val = int(row[3]) if row[3].isdigit() else 1
                    students.append([row[0], row[1], row[2], year_val, room_val])
    if os.path.exists(ROOMS_FILE):
        rooms = []
        with open(ROOMS_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    rooms.append([int(row[0]), int(row[1]), int(row[2])])


class HostelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management System - Final")
        self.root.geometry("900x580")
        self.root.minsize(780, 500)
        self.root.configure(bg="#F7F5F0")
        self.bg, self.accent, self.card, self.ink = "#F7F5F0", "#7B2D26", "#FFFFFF", "#1A1A1A"

        load_data()
        self.build_header()
        self.build_buttons()
        self.build_display()
        self.refresh_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_header(self):
        header = tk.Frame(self.root, bg=self.accent, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="HOSTEL MANAGEMENT SYSTEM", font=("Georgia", 17, "bold"),
                 bg=self.accent, fg="white").pack(side="left", padx=18, pady=12)
        tk.Label(header, text="Final Project  |  1 / 2 / 3 Person Rooms", font=("Calibri", 10),
                 bg=self.accent, fg="#F0E6E4").pack(side="right", padx=18)

    def build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.bg)
        btn_frame.pack(fill="x", padx=12, pady=10)
        style = {"font": ("Calibri", 10, "bold"), "bg": self.accent, "fg": "white",
                 "activebackground": "#5A201C", "activeforeground": "white",
                 "relief": "flat", "padx": 10, "pady": 6, "cursor": "hand2"}
        actions = [
            ("Register", self.open_register),
            ("Allocate", self.open_allocate),
            ("Search", self.open_search),
            ("Room Change", self.open_room_change),
            ("View Rooms", self.refresh_display),
            ("Students", self.show_students_window),
            ("Analysis", self.show_analysis),
            ("Save", self.do_save),
            ("Exit", self.on_close),
        ]
        for text, cmd in actions:
            tk.Button(btn_frame, text=text, command=cmd, **style).pack(side="left", padx=4)

    def build_display(self):
        left = tk.Frame(self.root, bg=self.bg)
        left.pack(side="left", fill="both", expand=True, padx=(12, 6), pady=(0, 12))
        tk.Label(left, text="Rooms & Occupancy", font=("Georgia", 12, "bold"),
                 bg=self.bg, fg=self.ink).pack(anchor="w", pady=(0, 4))
        self.room_text = tk.Text(left, font=("Consolas", 10), bg=self.card, fg=self.ink,
                                 relief="solid", borderwidth=1, wrap="word", state="disabled")
        self.room_text.pack(fill="both", expand=True)

        right = tk.Frame(self.root, bg=self.bg, width=260)
        right.pack(side="right", fill="y", padx=(6, 12), pady=(0, 12))
        right.pack_propagate(False)
        tk.Label(right, text="Without Room", font=("Georgia", 11, "bold"),
                 bg=self.bg, fg=self.ink).pack(anchor="w", pady=(0, 4))
        self.pending_list = tk.Listbox(right, font=("Calibri", 10), bg=self.card, fg=self.ink,
                                       relief="solid", borderwidth=1, height=10)
        self.pending_list.pack(fill="x", pady=(0, 10))
        tk.Label(right, text="Quick Stats", font=("Georgia", 11, "bold"),
                 bg=self.bg, fg=self.ink).pack(anchor="w", pady=(4, 4))
        self.stats_label = tk.Label(right, text="", font=("Calibri", 10), bg=self.card, fg=self.ink,
                                    relief="solid", borderwidth=1, justify="left", anchor="nw", padx=8, pady=8)
        self.stats_label.pack(fill="both", expand=True)

    def refresh_display(self):
        self.room_text.config(state="normal")
        self.room_text.delete("1.0", "end")
        lines = []
        for room in rooms:
            lines.append("Room " + str(room[0]) + "  |  " + sharing_label(room[1]))
            lines.append("  " + get_room_status(room))
            occ = get_students_in_room(room[0])
            if not occ:
                lines.append("  Students: (none)")
            else:
                lines.append("  Students:")
                for n in occ:
                    lines.append("     • " + n)
            lines.append("-" * 40)
        self.room_text.insert("1.0", "\n".join(lines))
        self.room_text.config(state="disabled")

        self.pending_list.delete(0, "end")
        pending = 0
        for s in students:
            if s[4] is None:
                self.pending_list.insert("end", s[1] + " - " + s[0])
                pending += 1
        if pending == 0:
            self.pending_list.insert("end", "(all have rooms)")

        total = len(students)
        allocated = sum(1 for s in students if s[4] is not None)
        seats = sum(r[1] for r in rooms)
        occupied = sum(r[2] for r in rooms)
        self.stats_label.config(text=(
            "Students : " + str(total) + "\n"
            "Allocated: " + str(allocated) + "\n"
            "Pending  : " + str(pending) + "\n\n"
            "Seats    : " + str(seats) + "\n"
            "Occupied : " + str(occupied) + "\n"
            "Free     : " + str(seats - occupied)
        ))

    def do_save(self):
        save_data()
        messagebox.showinfo("Saved", "Data saved to students.csv and rooms.csv")

    def on_close(self):
        save_data()
        self.root.destroy()

    def open_register(self):
        win = tk.Toplevel(self.root)
        win.title("Register Student")
        win.geometry("360x300")
        win.configure(bg=self.bg)
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text="Register Student", font=("Georgia", 13, "bold"),
                 bg=self.bg, fg=self.accent).pack(pady=(14, 10))
        form = tk.Frame(win, bg=self.bg)
        form.pack(padx=20, fill="x")
        fields = ["Name", "Roll Number", "Branch", "Year (1-4)"]
        entries = {}
        for i, label in enumerate(fields):
            tk.Label(form, text=label, font=("Calibri", 10), bg=self.bg).grid(row=i, column=0, sticky="w", pady=5)
            e = tk.Entry(form, font=("Calibri", 10), width=22)
            e.grid(row=i, column=1, pady=5, padx=(8, 0))
            entries[label] = e

        def save():
            name = entries["Name"].get().strip()
            roll = entries["Roll Number"].get().strip()
            branch = entries["Branch"].get().strip()
            year_text = entries["Year (1-4)"].get().strip()
            if not name or not roll or not branch:
                messagebox.showerror("Error", "Name, Roll and Branch are required.", parent=win)
                return
            year = int(year_text) if year_text.isdigit() else 1
            if find_student_index(roll) != -1:
                messagebox.showerror("Error", "Roll number already exists.", parent=win)
                return
            students.append([name, roll, branch, year, None])
            messagebox.showinfo("Success", name + " registered!", parent=win)
            win.destroy()
            self.refresh_display()

        tk.Button(win, text="Register", command=save, font=("Calibri", 10, "bold"),
                  bg=self.accent, fg="white", relief="flat", padx=16, pady=5, cursor="hand2").pack(pady=14)

    def open_allocate(self):
        pending = [s for s in students if s[4] is None]
        if not pending:
            messagebox.showinfo("Info", "No students without a room.")
            return
        win = tk.Toplevel(self.root)
        win.title("Allocate Room")
        win.geometry("440x440")
        win.configure(bg=self.bg)
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text="Allocate Room", font=("Georgia", 13, "bold"),
                 bg=self.bg, fg=self.accent).pack(pady=(12, 6))

        tk.Label(win, text="Student:", font=("Calibri", 10), bg=self.bg).pack(anchor="w", padx=20)
        student_var = tk.StringVar()
        opts = [s[1] + " - " + s[0] for s in pending]
        ttk.Combobox(win, textvariable=student_var, values=opts, state="readonly",
                     font=("Calibri", 10), width=38).pack(padx=20, pady=4, anchor="w")
        if opts:
            student_var.set(opts[0])

        tk.Label(win, text="Room type:", font=("Calibri", 10), bg=self.bg).pack(anchor="w", padx=20, pady=(8, 0))
        share_var = tk.StringVar(value="any")
        sf = tk.Frame(win, bg=self.bg)
        sf.pack(anchor="w", padx=20)
        for text, val in [("1-person", "1"), ("2-person", "2"), ("3-person", "3"), ("Any", "any")]:
            tk.Radiobutton(sf, text=text, variable=share_var, value=val, font=("Calibri", 9),
                           bg=self.bg, activebackground=self.bg, selectcolor=self.bg).pack(anchor="w")

        tk.Label(win, text="Available rooms:", font=("Calibri", 10), bg=self.bg).pack(anchor="w", padx=20, pady=(6, 0))
        room_lb = tk.Listbox(win, font=("Consolas", 9), height=7, width=50, bg=self.card, relief="solid", borderwidth=1)
        room_lb.pack(padx=20, pady=4, anchor="w")

        def update_rooms(*a):
            room_lb.delete(0, "end")
            pref = None if share_var.get() == "any" else int(share_var.get())
            for room in rooms:
                if room[2] >= room[1]:
                    continue
                if pref is not None and room[1] != pref:
                    continue
                room_lb.insert("end", "Room " + str(room[0]) + " | " + sharing_label(room[1]) + " | " + get_room_status(room))

        share_var.trace_add("write", update_rooms)
        update_rooms()

        def do_alloc():
            sel = student_var.get()
            if not sel:
                return
            roll = sel.split(" - ")[0]
            si = find_student_index(roll)
            if si == -1 or students[si][4] is not None:
                messagebox.showerror("Error", "Invalid student.", parent=win)
                return
            choice = room_lb.curselection()
            if not choice:
                messagebox.showerror("Error", "Select a room.", parent=win)
                return
            room_no = int(room_lb.get(choice[0]).split()[1])
            ri = find_room_index(room_no)
            if ri == -1 or rooms[ri][2] >= rooms[ri][1]:
                messagebox.showerror("Error", "Room not available.", parent=win)
                return
            rooms[ri][2] += 1
            students[si][4] = room_no
            messagebox.showinfo("Success", "Room " + str(room_no) + " allocated to " + students[si][0], parent=win)
            win.destroy()
            self.refresh_display()

        tk.Button(win, text="Allocate", command=do_alloc, font=("Calibri", 10, "bold"),
                  bg=self.accent, fg="white", relief="flat", padx=16, pady=5, cursor="hand2").pack(pady=10)

    def open_search(self):
        roll = messagebox.askstring("Search Student", "Enter Roll Number:", parent=self.root)
        if not roll:
            return
        si = find_student_index(roll.strip())
        if si == -1:
            messagebox.showinfo("Result", "Student not found.")
            return
        s = students[si]
        room_info = "Not Allocated" if s[4] is None else str(s[4])
        msg = "Name: " + s[0] + "\nRoll: " + s[1] + "\nBranch: " + s[2] + "\nYear: " + str(s[3]) + "\nRoom: " + room_info
        if s[4] is not None:
            ri = find_room_index(s[4])
            if ri != -1:
                msg += "\nType: " + sharing_label(rooms[ri][1]) + "\nStatus: " + get_room_status(rooms[ri])
        messagebox.showinfo("Student Found", msg)

    def open_room_change(self):
        allocated = [s for s in students if s[4] is not None]
        if not allocated:
            messagebox.showinfo("Info", "No students have rooms yet.")
            return
        win = tk.Toplevel(self.root)
        win.title("Room Change")
        win.geometry("440x400")
        win.configure(bg=self.bg)
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text="Room Change", font=("Georgia", 13, "bold"),
                 bg=self.bg, fg=self.accent).pack(pady=(12, 6))

        tk.Label(win, text="Student:", font=("Calibri", 10), bg=self.bg).pack(anchor="w", padx=20)
        student_var = tk.StringVar()
        opts = [s[1] + " - " + s[0] + " (Room " + str(s[4]) + ")" for s in allocated]
        ttk.Combobox(win, textvariable=student_var, values=opts, state="readonly",
                     font=("Calibri", 10), width=40).pack(padx=20, pady=4, anchor="w")
        if opts:
            student_var.set(opts[0])

        share_var = tk.StringVar(value="any")
        sf = tk.Frame(win, bg=self.bg)
        sf.pack(anchor="w", padx=20, pady=4)
        for text, val in [("1-person", "1"), ("2-person", "2"), ("3-person", "3"), ("Any", "any")]:
            tk.Radiobutton(sf, text=text, variable=share_var, value=val, font=("Calibri", 9),
                           bg=self.bg, activebackground=self.bg, selectcolor=self.bg).pack(anchor="w")

        room_lb = tk.Listbox(win, font=("Consolas", 9), height=6, width=50, bg=self.card, relief="solid", borderwidth=1)
        room_lb.pack(padx=20, pady=4, anchor="w")

        def update_rooms(*a):
            room_lb.delete(0, "end")
            pref = None if share_var.get() == "any" else int(share_var.get())
            for room in rooms:
                if room[2] >= room[1]:
                    continue
                if pref is not None and room[1] != pref:
                    continue
                room_lb.insert("end", "Room " + str(room[0]) + " | " + sharing_label(room[1]) + " | " + get_room_status(room))

        share_var.trace_add("write", update_rooms)
        update_rooms()

        def do_change():
            sel = student_var.get()
            if not sel:
                return
            roll = sel.split(" - ")[0]
            si = find_student_index(roll)
            if si == -1 or students[si][4] is None:
                return
            choice = room_lb.curselection()
            if not choice:
                messagebox.showerror("Error", "Select a new room.", parent=win)
                return
            new_room = int(room_lb.get(choice[0]).split()[1])
            old_room = students[si][4]
            if new_room == old_room:
                messagebox.showinfo("Info", "Already in this room.", parent=win)
                return
            ri_new = find_room_index(new_room)
            if ri_new == -1 or rooms[ri_new][2] >= rooms[ri_new][1]:
                messagebox.showerror("Error", "Room not available.", parent=win)
                return
            ri_old = find_room_index(old_room)
            if ri_old != -1 and rooms[ri_old][2] > 0:
                rooms[ri_old][2] -= 1
            rooms[ri_new][2] += 1
            students[si][4] = new_room
            messagebox.showinfo("Success", students[si][0] + " moved from " + str(old_room) + " to " + str(new_room), parent=win)
            win.destroy()
            self.refresh_display()

        tk.Button(win, text="Change Room", command=do_change, font=("Calibri", 10, "bold"),
                  bg=self.accent, fg="white", relief="flat", padx=16, pady=5, cursor="hand2").pack(pady=10)

    def show_students_window(self):
        win = tk.Toplevel(self.root)
        win.title("All Students")
        win.geometry("560x340")
        win.configure(bg=self.bg)
        tk.Label(win, text="Registered Students", font=("Georgia", 13, "bold"),
                 bg=self.bg, fg=self.accent).pack(pady=(10, 6))
        cols = ("Name", "Roll No", "Branch", "Year", "Room")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=11)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor="center")
        tree.column("Name", width=140, anchor="w")
        tree.pack(padx=14, pady=4, fill="both", expand=True)
        if not students:
            tree.insert("", "end", values=("No students", "", "", "", ""))
        else:
            for s in students:
                tree.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4] if s[4] is not None else "Not Allocated"))
        tk.Button(win, text="Close", command=win.destroy, font=("Calibri", 10),
                  bg=self.accent, fg="white", relief="flat", padx=14, pady=4).pack(pady=8)

    def show_analysis(self):
        total = len(students)
        allocated = sum(1 for s in students if s[4] is not None)
        seats = sum(r[1] for r in rooms)
        occupied = sum(r[2] for r in rooms)
        full = sum(1 for r in rooms if r[2] >= r[1])
        pct = round((occupied / seats) * 100, 1) if seats else 0
        single = sum(1 for r in rooms if r[1] == 1)
        double = sum(1 for r in rooms if r[1] == 2)
        triple = sum(1 for r in rooms if r[1] == 3)
        msg = (
            "STUDENTS\n"
            "  Total: " + str(total) + "\n"
            "  With room: " + str(allocated) + "\n"
            "  Without room: " + str(total - allocated) + "\n\n"
            "ROOMS\n"
            "  Total rooms: " + str(len(rooms)) + "\n"
            "  1-person: " + str(single) + " | 2-person: " + str(double) + " | 3-person: " + str(triple) + "\n"
            "  Fully occupied: " + str(full) + "\n\n"
            "OCCUPANCY\n"
            "  Seats: " + str(seats) + " | Occupied: " + str(occupied) + " | Free: " + str(seats - occupied) + "\n"
            "  Occupancy: " + str(pct) + "%"
        )
        messagebox.showinfo("Hostel Analysis", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = HostelApp(root)
    root.mainloop()
