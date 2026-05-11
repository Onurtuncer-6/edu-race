# routes/views.py
from flask import Blueprint, render_template, g;
from helpers import DatabaseHelper;

views_bp = Blueprint('views', __name__);

@views_bp.route('/', methods=['GET'])
def home():
    live_stats = DatabaseHelper.get_home_views_stats();
    return render_template(template_name_or_list='home.html', stats=live_stats);