from flask import Blueprint, render_template
from app.models import Laptop, DeviceAssignment

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    rows = (
        DeviceAssignment.query
        .filter_by(return_date=None)
        .join(DeviceAssignment.laptop)
        .join(DeviceAssignment.employee)
        .order_by(Laptop.device_number)
        .all()
    )
    return render_template('dashboard.html', rows=rows)