from flask import Blueprint, render_template
from app.models import Laptop

bp = Blueprint('laptop', __name__, url_prefix='/laptops')

@bp.route('/')
def index():
    laptops = Laptop.query.order_by(Laptop.device_number).all()
    return render_template('laptop.html', laptops=laptops)