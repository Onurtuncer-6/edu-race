# routes/views.py
from flask import Blueprint, render_template, g;

views_bp = Blueprint('views', __name__);

@views_bp.route('/', methods=['GET'])
def home():
    welcome_text = g.text['home']['title'];
    return render_template(template_name_or_list='home.html', title=f"{welcome_text}");