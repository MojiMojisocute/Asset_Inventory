from .database import db
from datetime import datetime

class DeviceAssignment(db.Model):
    __tablename__ = 'device_assignments'

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptops.id'), nullable=False)

    assigned_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        employee_name = self.employee.name if self.employee else f'Employee {self.employee_id}'
        return f'<Assignment: {employee_name} -> Laptop {self.laptop_id}>'