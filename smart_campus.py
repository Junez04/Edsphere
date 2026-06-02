"""
=============================================================
  SMART CAMPUS INFORMATION SYSTEM
  Integrating: Lists, Dicts, Arrays, Sorting, Searching,
  Functions, File Handling, Exception Handling,
  NumPy, Pandas, Matplotlib
=============================================================
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import json
import csv
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# SECTION 1: DATA STRUCTURES  (list, dict, array)
# ─────────────────────────────────────────────────────────────

COURSES = {
    "CS101": {"name": "Introduction to Programming",  "credits": 4, "fee": 8000},
    "BT201": {"name": "Biotechnology Fundamentals",   "credits": 4, "fee": 9000},
    "MA101": {"name": "Engineering Mathematics",       "credits": 3, "fee": 6000},
    "PH101": {"name": "Applied Physics",               "credits": 3, "fee": 6500},
    "EC301": {"name": "Electronics & Circuits",        "credits": 4, "fee": 8500},
}

GRADE_SCALE = [
    (90, "O",  10), (80, "A+",  9), (70, "A",  8),
    (60, "B+",  7), (50, "B",   6), (40, "C",  5), (0,  "F",  0),
]

students = []           # list of student dicts
enrollment_map = {}     # dict: student_id -> list of course codes


# ─────────────────────────────────────────────────────────────
# SECTION 2: STUDENT REGISTRATION & GRADE EVALUATION
# ─────────────────────────────────────────────────────────────

def assign_grade(marks):
    """Evaluate letter grade and grade point using conditional statements."""
    for threshold, letter, point in GRADE_SCALE:
        if marks >= threshold:
            return letter, point
    return "F", 0


def register_student(student_id, name, dept, semester, marks_list):
    """
    Register a new student and compute grades.
    Parameters: student_id, name, dept, semester, marks_list (list)
    Returns: student dict
    """
    # Validate using conditional + exception
    if not student_id or not name:
        raise ValueError("Student ID and Name are required fields.")
    for s in students:
        if s["id"] == student_id:
            raise ValueError(f"Student ID '{student_id}' already exists.")

    grades = []
    for mark in marks_list:
        letter, point = assign_grade(mark)
        grades.append({"marks": mark, "grade": letter, "point": point})

    avg_marks  = sum(marks_list) / len(marks_list) if marks_list else 0
    cgpa       = sum(g["point"] for g in grades) / len(grades) if grades else 0.0
    status     = "Pass" if avg_marks >= 40 else "Fail"

    student = {
        "id":       student_id,
        "name":     name,
        "dept":     dept,
        "semester": semester,
        "marks":    marks_list,
        "grades":   grades,
        "avg":      round(avg_marks, 2),
        "cgpa":     round(cgpa, 2),
        "status":   status,
        "fee_paid": False,
    }
    students.append(student)
    enrollment_map[student_id] = []
    return student


# ─────────────────────────────────────────────────────────────
# SECTION 3: COURSE ENROLLMENT MANAGEMENT
# ─────────────────────────────────────────────────────────────

def enroll_student(student_id, course_codes):
    """Enroll a student in multiple courses using loops & conditions."""
    if student_id not in enrollment_map:
        raise KeyError(f"Student '{student_id}' not found.")

    enrolled   = []
    skipped    = []
    for code in course_codes:
        code = code.upper()
        if code not in COURSES:
            skipped.append(f"{code} (invalid course)")
        elif code in enrollment_map[student_id]:
            skipped.append(f"{code} (already enrolled)")
        else:
            enrollment_map[student_id].append(code)
            enrolled.append(code)
    return enrolled, skipped


def get_enrollment_summary(student_id):
    """Return course details for a student."""
    codes = enrollment_map.get(student_id, [])
    return [{"code": c, **COURSES[c]} for c in codes if c in COURSES]


# ─────────────────────────────────────────────────────────────
# SECTION 4: BUBBLE SORT — sort by average marks
# ─────────────────────────────────────────────────────────────

def bubble_sort_by_avg(data):
    """Bubble sort descending on 'avg' field (returns new list)."""
    arr = data[:]                         # shallow copy
    n   = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j]["avg"] < arr[j + 1]["avg"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# ─────────────────────────────────────────────────────────────
# SECTION 5: SELECTION SORT — sort by CGPA
# ─────────────────────────────────────────────────────────────

def selection_sort_by_cgpa(data):
    """Selection sort descending on 'cgpa' field (returns new list)."""
    arr = data[:]
    n   = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j]["cgpa"] > arr[max_idx]["cgpa"]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr


# ─────────────────────────────────────────────────────────────
# SECTION 6: BINARY SEARCH & LINEAR SEARCH
# ─────────────────────────────────────────────────────────────

def linear_search_by_name(query):
    """Linear search — scan all students for a name match (partial, case-insensitive)."""
    query  = query.lower()
    result = [s for s in students if query in s["name"].lower()]
    return result


def binary_search_by_id(sorted_list, target_id):
    """
    Binary search on a list sorted by 'id'.
    Returns the student dict or None.
    """
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_id = sorted_list[mid]["id"]
        if mid_id == target_id:
            return sorted_list[mid]
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None


# ─────────────────────────────────────────────────────────────
# SECTION 7: FEE CALCULATION USING FUNCTIONS (parameters)
# ─────────────────────────────────────────────────────────────

BASE_FEE       = 15000
HOSTEL_FEE     = 8000
TRANSPORT_FEE  = 3000
SCHOLARSHIP_PCT= 0.20    # 20 % discount for CGPA >= 8

def calculate_fee(student_id, include_hostel=False, include_transport=False):
    """
    Calculate total fee for a student.
    Parameters:
        student_id      : str
        include_hostel  : bool (optional, default False)
        include_transport: bool (optional, default False)
    Returns: dict with fee breakdown
    """
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise KeyError(f"Student '{student_id}' not found.")

    course_fee = sum(COURSES[c]["fee"] for c in enrollment_map.get(student_id, []) if c in COURSES)
    total      = BASE_FEE + course_fee
    hostel     = HOSTEL_FEE    if include_hostel    else 0
    transport  = TRANSPORT_FEE if include_transport else 0
    total     += hostel + transport

    scholarship = 0
    if student["cgpa"] >= 8.0:
        scholarship = round(total * SCHOLARSHIP_PCT)
    net_fee = total - scholarship

    return {
        "student_id":   student_id,
        "base_fee":     BASE_FEE,
        "course_fee":   course_fee,
        "hostel_fee":   hostel,
        "transport_fee":transport,
        "scholarship":  scholarship,
        "total_fee":    total,
        "net_fee":      net_fee,
    }


# ─────────────────────────────────────────────────────────────
# SECTION 8: FILE-BASED ACADEMIC RECORD MANAGEMENT
# ─────────────────────────────────────────────────────────────

RECORDS_DIR = "/home/claude/campus_records"

def save_records_to_file():
    """Save student list to JSON and CSV files."""
    os.makedirs(RECORDS_DIR, exist_ok=True)

    # JSON
    json_path = os.path.join(RECORDS_DIR, "students.json")
    with open(json_path, "w") as f:
        json.dump(students, f, indent=2)

    # CSV (flat)
    csv_path = os.path.join(RECORDS_DIR, "students.csv")
    if students:
        fieldnames = ["id", "name", "dept", "semester", "avg", "cgpa", "status"]
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in students:
                writer.writerow({k: s[k] for k in fieldnames})

    # Enrollment
    enroll_path = os.path.join(RECORDS_DIR, "enrollment.json")
    with open(enroll_path, "w") as f:
        json.dump(enrollment_map, f, indent=2)

    return json_path, csv_path, enroll_path


def load_records_from_file():
    """Load student records from JSON file with exception handling."""
    global students, enrollment_map
    json_path   = os.path.join(RECORDS_DIR, "students.json")
    enroll_path = os.path.join(RECORDS_DIR, "enrollment.json")
    try:
        with open(json_path, "r") as f:
            students = json.load(f)
        with open(enroll_path, "r") as f:
            enrollment_map = json.load(f)
        return True
    except FileNotFoundError:
        print("  [Warning] Record files not found; starting fresh.")
        return False
    except json.JSONDecodeError as e:
        print(f"  [Error] Corrupt JSON: {e}")
        return False


# ─────────────────────────────────────────────────────────────
# SECTION 9: DIRECTORY SCANNING WITH EXCEPTION HANDLING
# ─────────────────────────────────────────────────────────────

def scan_records_directory(path):
    """
    Scan a directory for record files.
    Demonstrates exception handling with multiple except blocks.
    """
    file_info = []
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory '{path}' does not exist.")
        entries = os.listdir(path)
        if not entries:
            raise ValueError("Directory is empty.")
        for entry in entries:
            full = os.path.join(path, entry)
            size = os.path.getsize(full)
            file_info.append({"file": entry, "size_bytes": size,
                               "modified": datetime.fromtimestamp(
                                   os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M:%S")})
    except FileNotFoundError as e:
        print(f"  [FileNotFoundError] {e}")
    except PermissionError:
        print(f"  [PermissionError] Cannot access directory '{path}'.")
    except ValueError as e:
        print(f"  [ValueError] {e}")
    except Exception as e:
        print(f"  [UnexpectedError] {e}")
    return file_info


# ─────────────────────────────────────────────────────────────
# SECTION 10: PERFORMANCE ANALYTICS — NumPy, Pandas, Matplotlib
# ─────────────────────────────────────────────────────────────

def run_analytics(output_dir="/home/claude"):
    """
    Compute and visualise student performance using NumPy, Pandas, Matplotlib.
    Saves all charts to output_dir.
    """
    if not students:
        print("  No student data available for analytics.")
        return []

    # ── NumPy arrays ──────────────────────────────────────────
    avg_array  = np.array([s["avg"]  for s in students])
    cgpa_array = np.array([s["cgpa"] for s in students])

    np_mean   = np.mean(avg_array)
    np_median = np.median(avg_array)
    np_std    = np.std(avg_array)
    np_max    = np.max(avg_array)
    np_min    = np.min(avg_array)
    np_pass   = np.sum(avg_array >= 40)
    np_fail   = np.sum(avg_array <  40)

    print("\n  ── NumPy Statistical Summary ──────────────────────")
    print(f"  Mean Marks  : {np_mean:.2f}")
    print(f"  Median Marks: {np_median:.2f}")
    print(f"  Std Dev     : {np_std:.2f}")
    print(f"  Max / Min   : {np_max} / {np_min}")
    print(f"  Pass Count  : {np_pass}   Fail Count: {np_fail}")

    # ── Pandas DataFrame ──────────────────────────────────────
    df = pd.DataFrame([{
        "ID":       s["id"],
        "Name":     s["name"],
        "Dept":     s["dept"],
        "Semester": s["semester"],
        "Avg":      s["avg"],
        "CGPA":     s["cgpa"],
        "Status":   s["status"],
    } for s in students])

    print("\n  ── Pandas Department-wise Performance ────────────")
    dept_summary = df.groupby("Dept")[["Avg", "CGPA"]].agg(
        Mean_Avg=("Avg", "mean"),
        Mean_CGPA=("CGPA", "mean"),
        Count=("Avg", "count")
    ).round(2)
    print(dept_summary.to_string())

    # ── Matplotlib Charts ─────────────────────────────────────
    saved = []
    plt.style.use("seaborn-v0_8-whitegrid")
    COLORS = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#44BBA4"]

    names  = [s["name"].split()[-1] for s in students]  # last names for axis
    ids    = [s["id"] for s in students]

    # Chart 1: Bar — Average Marks per Student
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(ids, avg_array, color=COLORS[:len(students)], edgecolor="white", linewidth=0.8)
    ax.axhline(np_mean, color="red", linestyle="--", linewidth=1.5, label=f"Mean ({np_mean:.1f})")
    ax.axhline(40, color="orange", linestyle=":", linewidth=1.5, label="Pass Threshold (40)")
    for bar, val in zip(bars, avg_array):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Student Average Marks", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Student ID");  ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 105);  ax.legend()
    plt.xticks(rotation=20)
    plt.tight_layout()
    p = os.path.join(output_dir, "chart1_avg_marks.png")
    plt.savefig(p, dpi=120);  plt.close();  saved.append(p)

    # Chart 2: CGPA Comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ids, cgpa_array, marker="o", color="#2E86AB",
            linewidth=2.5, markersize=9, markerfacecolor="white", markeredgewidth=2.5)
    for i, (x, y) in enumerate(zip(ids, cgpa_array)):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=9, color="#2E86AB")
    ax.fill_between(range(len(ids)), cgpa_array, alpha=0.12, color="#2E86AB")
    ax.set_title("CGPA Trend Across Students", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Student ID");  ax.set_ylabel("CGPA (0–10)")
    ax.set_ylim(0, 10.5);  ax.set_xticks(range(len(ids)));  ax.set_xticklabels(ids, rotation=20)
    plt.tight_layout()
    p = os.path.join(output_dir, "chart2_cgpa_trend.png")
    plt.savefig(p, dpi=120);  plt.close();  saved.append(p)

    # Chart 3: Pie — Pass vs Fail
    fig, ax = plt.subplots(figsize=(6, 6))
    sizes  = [int(np_pass), int(np_fail)]
    labels = [f"Pass ({int(np_pass)})", f"Fail ({int(np_fail)})"]
    colors = ["#44BBA4", "#C73E1D"]
    explode= (0.05, 0.05)
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct="%1.1f%%",
                                       colors=colors, explode=explode,
                                       startangle=140, shadow=True,
                                       textprops={"fontsize": 11})
    for at in autotexts:
        at.set_fontweight("bold")
    ax.set_title("Pass / Fail Distribution", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    p = os.path.join(output_dir, "chart3_pass_fail.png")
    plt.savefig(p, dpi=120);  plt.close();  saved.append(p)

    # Chart 4: Grouped Bar — Dept-wise Avg & CGPA
    dept_df = dept_summary.reset_index()
    x       = np.arange(len(dept_df))
    w       = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar(x - w/2, dept_df["Mean_Avg"],  w, label="Mean Avg Marks", color="#2E86AB", edgecolor="white")
    b2 = ax.bar(x + w/2, dept_df["Mean_CGPA"]*10, w, label="Mean CGPA ×10",  color="#A23B72", edgecolor="white")
    ax.set_title("Department-wise Performance (Avg Marks & CGPA)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x);  ax.set_xticklabels(dept_df["Dept"])
    ax.set_ylabel("Score");  ax.legend()
    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h:.1f}",
                ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    p = os.path.join(output_dir, "chart4_dept_performance.png")
    plt.savefig(p, dpi=120);  plt.close();  saved.append(p)

    # Chart 5: Histogram — Marks Distribution
    all_marks = [m for s in students for m in s["marks"]]
    fig, ax   = plt.subplots(figsize=(8, 5))
    n, bins, patches = ax.hist(all_marks, bins=10, color="#F18F01", edgecolor="white",
                                linewidth=0.8, rwidth=0.88)
    ax.axvline(np.mean(all_marks), color="red", linestyle="--", linewidth=1.5, label=f"Mean ({np.mean(all_marks):.1f})")
    ax.set_title("Distribution of All Subject Marks", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Marks");  ax.set_ylabel("Frequency");  ax.legend()
    plt.tight_layout()
    p = os.path.join(output_dir, "chart5_marks_hist.png")
    plt.savefig(p, dpi=120);  plt.close();  saved.append(p)

    print(f"\n  ── Charts saved: {len(saved)} files ──────────────────")
    for fp in saved:
        print(f"     {fp}")

    return saved


# ─────────────────────────────────────────────────────────────
# SECTION 11:  MAIN DEMO RUNNER
# ─────────────────────────────────────────────────────────────

def print_section(title):
    print("\n" + "═"*60)
    print(f"  {title}")
    print("═"*60)


def main():
    print("\n" + "█"*60)
    print("  SMART CAMPUS INFORMATION SYSTEM")
    print("  Complete Demonstration")
    print("█"*60)

    # ── 1. Register Students ──────────────────────────────────
    print_section("1. STUDENT REGISTRATION & GRADE EVALUATION")

    raw_data = [
        ("S001", "Arjun Sharma",   "CSE", 3, [85, 78, 92, 88, 76]),
        ("S002", "Priya Nair",     "BIO", 2, [91, 95, 88, 97, 90]),
        ("S003", "Rahul Mehta",    "ECE", 4, [55, 62, 48, 70, 58]),
        ("S004", "Sneha Pillai",   "CSE", 1, [33, 45, 28, 50, 38]),
        ("S005", "Kiran Desai",    "BIO", 3, [74, 80, 71, 68, 83]),
        ("S006", "Ananya Iyer",    "ECE", 2, [88, 92, 85, 90, 94]),
    ]

    for sid, name, dept, sem, marks in raw_data:
        try:
            s = register_student(sid, name, dept, sem, marks)
            grade_str = ", ".join(f"{g['marks']}→{g['grade']}" for g in s["grades"])
            print(f"  [{sid}] {name:<18} | Avg:{s['avg']:5.1f} | CGPA:{s['cgpa']} | "
                  f"Status:{s['status']} | Grades:[{grade_str}]")
        except ValueError as e:
            print(f"  [Registration Error] {e}")

    # ── 2. Course Enrollment ──────────────────────────────────
    print_section("2. COURSE ENROLLMENT MANAGEMENT")

    enrollments = [
        ("S001", ["CS101", "MA101", "PH101"]),
        ("S002", ["BT201", "MA101", "CS101"]),
        ("S003", ["EC301", "MA101", "CS101"]),
        ("S004", ["CS101", "MA101"]),
        ("S005", ["BT201", "PH101", "EC301"]),
        ("S006", ["EC301", "CS101", "MA101", "BT201"]),
    ]

    for sid, codes in enrollments:
        enrolled, skipped = enroll_student(sid, codes)
        print(f"  [{sid}] Enrolled: {enrolled}  |  Skipped: {skipped}")

    # ── 3. Sorting — Bubble Sort ──────────────────────────────
    print_section("3a. BUBBLE SORT — by Average Marks (desc)")
    sorted_avg = bubble_sort_by_avg(students)
    for rank, s in enumerate(sorted_avg, 1):
        print(f"  Rank {rank}: [{s['id']}] {s['name']:<18} | Avg: {s['avg']}")

    # ── 4. Sorting — Selection Sort ───────────────────────────
    print_section("3b. SELECTION SORT — by CGPA (desc)")
    sorted_cgpa = selection_sort_by_cgpa(students)
    for rank, s in enumerate(sorted_cgpa, 1):
        print(f"  Rank {rank}: [{s['id']}] {s['name']:<18} | CGPA: {s['cgpa']}")

    # ── 5. Searching ──────────────────────────────────────────
    print_section("4. SEARCHING — Linear & Binary Search")

    # Linear search
    query  = "ra"
    result = linear_search_by_name(query)
    print(f"\n  Linear Search (name contains '{query}'):")
    for r in result:
        print(f"    → [{r['id']}] {r['name']} | Avg: {r['avg']}")

    # Binary search (sort by id first)
    sorted_by_id = sorted(students, key=lambda x: x["id"])
    target_id    = "S004"
    found        = binary_search_by_id(sorted_by_id, target_id)
    print(f"\n  Binary Search for ID '{target_id}':")
    if found:
        print(f"    → Found: {found['name']} | CGPA: {found['cgpa']} | Status: {found['status']}")
    else:
        print(f"    → Not found.")

    # ── 6. Fee Calculation ────────────────────────────────────
    print_section("5. FEE CALCULATION USING FUNCTIONS")
    for sid in ["S001", "S002", "S004"]:
        try:
            fee = calculate_fee(sid, include_hostel=True, include_transport=(sid == "S001"))
            print(f"\n  [{sid}] {next(s['name'] for s in students if s['id']==sid)}")
            print(f"    Base Fee      : ₹{fee['base_fee']:>7,}")
            print(f"    Course Fee    : ₹{fee['course_fee']:>7,}")
            print(f"    Hostel Fee    : ₹{fee['hostel_fee']:>7,}")
            print(f"    Transport Fee : ₹{fee['transport_fee']:>7,}")
            print(f"    Scholarship   : ₹{fee['scholarship']:>7,}")
            print(f"    ─────────────────────────")
            print(f"    NET FEE       : ₹{fee['net_fee']:>7,}")
        except KeyError as e:
            print(f"  [Fee Error] {e}")

    # ── 7. File Handling ──────────────────────────────────────
    print_section("6. FILE-BASED ACADEMIC RECORD MANAGEMENT")
    j, c, e = save_records_to_file()
    print(f"  Records saved:")
    print(f"    JSON     → {j}")
    print(f"    CSV      → {c}")
    print(f"    Enroll   → {e}")

    load_records_from_file()
    print(f"  Records reloaded: {len(students)} students.")

    # ── 8. Directory Scan ─────────────────────────────────────
    print_section("7. DIRECTORY SCANNING WITH EXCEPTION HANDLING")
    files = scan_records_directory(RECORDS_DIR)
    print(f"  Files in '{RECORDS_DIR}':")
    for fi in files:
        print(f"    {fi['file']:<25} {fi['size_bytes']:>6} bytes  |  {fi['modified']}")

    # Also demo exception for missing dir
    print("\n  Scanning non-existent directory:")
    scan_records_directory("/home/claude/no_such_folder")

    # ── 9. Analytics ──────────────────────────────────────────
    print_section("8. PERFORMANCE ANALYTICS (NumPy, Pandas, Matplotlib)")
    charts = run_analytics(output_dir="/home/claude")

    print_section("DEMO COMPLETE")
    print("  All components demonstrated successfully.")
    print(f"  Total Students : {len(students)}")
    print(f"  Total Courses  : {len(COURSES)}")
    print(f"  Charts Created : {len(charts)}")
    print()


if __name__ == "__main__":
    main()
