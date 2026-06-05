from .database import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    employee_type = db.Column(db.String(50))
    department = db.Column(db.String(100))

    onboard_date = db.Column(db.Date, nullable=True)
    offboard_date = db.Column(db.Date, nullable=True)
    duration_months = db.Column(db.Integer, nullable=True)

    remarks = db.Column(db.Text)

    status = db.Column(db.String(50), default=None)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device_assignments = db.relationship('DeviceAssignment', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.name}>'