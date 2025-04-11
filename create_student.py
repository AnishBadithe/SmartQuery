import pandas as pd
import sqlite3

# Load the Excel files
student_path = "student_info.xlsx"
registration_path = "registration.xlsx"
marks_path = "marks.xlsx"

s = pd.ExcelFile(student_path)
r = pd.ExcelFile(registration_path)
m = pd.ExcelFile(marks_path)

# Load data
df = pd.read_excel(s, sheet_name=s.sheet_names[0])
df1 = pd.read_excel(r, sheet_name=r.sheet_names[0])
df2 = pd.read_excel(m, sheet_name=m.sheet_names[0])

# Rename columns for SQL compatibility
df.rename(columns={
    "REGISTER NO": "reg_no",
    "NAME": "name",
    "MOBILE NUMBER": "mobile_number",
    "EMAIL": "email",
    "SCHOOL": "school",
    "COURSE MODE": "course_mode",
}, inplace=True)

# Convert reg_no to string for consistency
df["reg_no"] = df["reg_no"].astype(str)
df1["reg_no"] = df1["reg_no"].astype(str)
df2["reg_no"] = df2["reg_no"].astype(str)

# Create SQLite database
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Create student table
cursor.execute('''
CREATE TABLE student (
    reg_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mobile_number TEXT,
    email TEXT,
    school TEXT,
    course_mode TEXT
)
''')

# Create registered table with foreign key constraint
cursor.execute('''
CREATE TABLE registered (
    reg_no TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    slot TEXT,
    venue TEXT,
    FOREIGN KEY (reg_no) REFERENCES student(reg_no) ON DELETE CASCADE ON UPDATE CASCADE
)
''')

cursor.execute('''
CREATE TABLE marks (
    reg_no TEXT PRIMARY KEY,
    assignment INT,
    quiz_1 INT,
    quiz_2 INT,
    cat_1 INT,
    cat_2 INT,
    fat INT,
    grade TEXT,
    FOREIGN KEY (reg_no) REFERENCES student(reg_no) ON DELETE CASCADE ON UPDATE CASCADE
)
''')

# Insert data into the tables
df.to_sql("student", conn, if_exists="replace", index=False)
df1.to_sql("registered", conn, if_exists="replace", index=False)
df2.to_sql("marks", conn, if_exists="replace", index=False)

# Commit and close
conn.commit()
conn.close()

print("Student, Registered and Marks tables created with foreign key constraint successfully!")