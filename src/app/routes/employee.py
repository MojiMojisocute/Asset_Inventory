from flask import Blueprint, render_template
from app.models import Employee

bp = Blueprint('employee', __name__, url_prefix='/users')

@bp.route('/')
def index():
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('user.html', employees=employees, active_page='users')