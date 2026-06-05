from .database import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    device_number = db.Column(db.String(100), unique=True, nullable=False)
    product_serial_no = db.Column(db.String(100), unique=True)

    device_type = db.Column(db.String(50))

    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))

    description = db.Column(db.Text)

    state = db.Column(db.String(50))
    is_borrowed = db.Column(db.Boolean, default=False)
    disposal_status = db.Column(db.Boolean, default=False)

    purchase_date = db.Column(db.Date)
    warranty_end_date = db.Column(db.Date)

    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('DeviceAssignment', backref='device', lazy=True)

    @property
    def current_user(self):
        from .Device_assignment import DeviceAssignment
        assignment = DeviceAssignment.query.filter_by(
            device_id=self.id,
            return_date=None
        ).first()
        return assignment.employee if assignment else None

    def __repr__(self):
        return f'<Device {self.device_type}: {self.device_number}>'