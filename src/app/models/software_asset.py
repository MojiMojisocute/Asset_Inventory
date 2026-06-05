from .database import db
from datetime import datetime

class SoftwareAsset(db.Model):
    __tablename__ = 'software_assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_serial_no = db.Column(db.String(100), unique=True, nullable=False)
    software_name = db.Column(db.String(200), nullable=False)
    specifications = db.Column(db.Text)
    operating_system = db.Column(db.String(100))
    internal_function = db.Column(db.String(200))
    registration_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    number_of_licenses = db.Column(db.Integer)
    hardware_serial_no = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SoftwareAsset {self.software_name} - {self.asset_serial_no}>'

    def to_dict(self):
        return {
            'id': self.id,
            'asset_serial_no': self.asset_serial_no,
            'software_name': self.software_name,
            'specifications': self.specifications,
            'operating_system': self.operating_system,
            'internal_function': self.internal_function,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'number_of_licenses': self.number_of_licenses,
            'hardware_serial_no': self.hardware_serial_no,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }