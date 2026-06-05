import pandas as pd
import sqlite3
from datetime import datetime, date

DB_PATH = 'src/instance/device_management.db'
EMPLOYEE_FILE = 'Employee.xlsx'
LAPTOP_FILE   = 'Laptops.xlsx'

def parse_date(val):
    if pd.isna(val) or str(val).strip().lower() in ('null', ''):
        return None
    if isinstance(val, (int, float)):
        try:
            return (pd.Timestamp('1899-12-30') + pd.Timedelta(days=int(val))).date().isoformat()
        except:
            return None
    if isinstance(val, (datetime, date)):
        return val.date().isoformat() if isinstance(val, datetime) else val.isoformat()
    try:
        return pd.to_datetime(str(val), dayfirst=True).date().isoformat()
    except:
        return None

def clean(val):
    if pd.isna(val) or str(val).strip().lower() in ('null', ''):
        return None
    return str(val).strip()

def bool_col(val):
    if pd.isna(val):
        return 0
    return 1 if str(val).strip().lower() in ('yes', 'true', '1') else 0

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    employee_type TEXT,
    department TEXT,
    onboard_date TEXT,
    offboard_date TEXT,
    duration_months INTEGER,
    status TEXT,
    remarks TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS laptops (
    id INTEGER PRIMARY KEY,
    device_number TEXT UNIQUE NOT NULL,
    product_serial_no TEXT UNIQUE,
    brand TEXT,
    model TEXT,
    state TEXT,
    is_borrowed INTEGER DEFAULT 0,
    disposal_status INTEGER DEFAULT 0,
    purchase_date TEXT,
    warranty_end_date TEXT,
    remarks TEXT,
    vendor_borrow_date TEXT,
    vendor_return_date TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS device_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    laptop_id INTEGER NOT NULL REFERENCES laptops(id),
    assigned_date TEXT NOT NULL,
    return_date TEXT,
    return_reason TEXT,
    remarks TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
""")

df_emp = pd.read_excel(EMPLOYEE_FILE)
df_emp = df_emp[df_emp['name'].notna() & (df_emp['name'].astype(str).str.strip() != '')]

cur.execute("DELETE FROM employees")
for _, r in df_emp.iterrows():
    cur.execute("""
        INSERT INTO employees (id, name, employee_type, department, onboard_date, offboard_date, duration_months, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(r['id']) if pd.notna(r['id']) else None,
        clean(r['name']),
        clean(r.get('employee_type')),
        clean(r.get('department')),
        parse_date(r.get('onboard_date')),
        parse_date(r.get('offboard_date')),
        int(r['duration_months']) if pd.notna(r.get('duration_months')) else None,
        clean(r.get('status')),
    ))

print(f"Imported {len(df_emp)} employees")

df_lap = pd.read_excel(LAPTOP_FILE)
cur.execute("DELETE FROM laptops")
for _, r in df_lap.iterrows():
    cur.execute("""
        INSERT INTO laptops (id, device_number, product_serial_no, brand, model, state,
                             is_borrowed, disposal_status, purchase_date, warranty_end_date,
                             remarks, vendor_borrow_date, vendor_return_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(r['id']),
        clean(r['device_number']),
        clean(r.get('product_serial_no')),
        clean(r.get('brand')),
        clean(r.get('model')),
        clean(r.get('state')),
        bool_col(r.get('is_borrowed')),
        bool_col(r.get('disposal_status')),
        parse_date(r.get('purchase_date')),
        parse_date(r.get('warranty_end_date')),
        clean(r.get('remarks')),
        parse_date(r.get('vendor_borrow_date')),
        parse_date(r.get('vendor_return_date')),
    ))

print(f"Imported {len(df_lap)} laptops")

df_emp2 = pd.read_excel(EMPLOYEE_FILE)
df_emp2 = df_emp2[df_emp2['device_number'].notna() & (df_emp2['device_number'].astype(str).str.strip().str.lower() != 'null')]

cur.execute("DELETE FROM device_assignments")
for _, r in df_emp2.iterrows():
    serial = clean(r['device_number'])
    cur.execute("SELECT id FROM laptops WHERE product_serial_no = ?", (serial,))
    lap = cur.fetchone()
    if not lap:
        print(f"  ข้าม {r['name']} — ไม่เจอ laptop serial {serial}")
        continue
    assigned = parse_date(r.get('onboard_date')) or date.today().isoformat()
    return_date = parse_date(r.get('offboard_date'))
    cur.execute("""
        INSERT INTO device_assignments (employee_id, laptop_id, assigned_date, return_date)
        VALUES (?, ?, ?, ?)
    """, (int(r['id']), lap[0], assigned, return_date))

print(f"Imported {cur.rowcount and 'assignments done'}")

con.commit()
con.close()
print("เสร็จแล้ว!")