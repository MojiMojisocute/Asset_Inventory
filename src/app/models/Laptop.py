from .database import db
from datetime import datetime, date

class Laptop(db.Model):
    __tablename__ = 'laptops'

    id = db.Column(db.Integer, primary_key=True)
    device_number = db.Column(db.String(100), unique=True, nullable=False)
    product_serial_no = db.Column(db.String(100), unique=True)

    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))

    state = db.Column(db.String(50))
    is_borrowed = db.Column(db.Boolean, default=False)
    disposal_status = db.Column(db.Boolean, default=False)

    vendor_borrow_date = db.Column(db.Date, nullable=True)
    vendor_return_date = db.Column(db.Date, nullable=True)

    purchase_date = db.Column(db.Date)
    warranty_end_date = db.Column(db.Date)

    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('DeviceAssignment', backref='laptop', lazy=True)

    @property
    def vendor_borrow_duration_days(self):
        if not self.vendor_borrow_date:
            return None
        end = self.vendor_return_date or date.today()
        return (end - self.vendor_borrow_date).days

    @property
    def current_user(self):
        from app.models.Device_assignment import DeviceAssignment
        assignment = DeviceAssignment.query.filter_by(
            laptop_id=self.id,
            return_date=None
        ).first()
        return assignment.employee if assignment else None

    def __repr__(self):
        return f'<Laptop {self.device_number}>'