from flask import Blueprint, render_template
from app.models import DeviceAssignment, Employee

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    rows = (
        DeviceAssignment.query
        .join(DeviceAssignment.employee)
        .join(DeviceAssignment.laptop)
        .filter(Employee.status != 'Offboard')
        .order_by(Employee.department, Employee.name)
        .all()
    )
    return render_template('dashboard.html', rows=rows)