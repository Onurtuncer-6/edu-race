# routes/views.py
from flask import Blueprint, render_template, g, request;
from helpers import DatabaseHelper;

views_bp = Blueprint('views', __name__);

@views_bp.route('/', methods=['GET'])
def home():
    scope = request.args.get('scope')
    live_stats = DatabaseHelper.get_home_views_stats();
    performance_rankings= DatabaseHelper.get_home_performance_rankings(scope=scope);
    
    return render_template(
        template_name_or_list='home.html', 
        stats=live_stats, 
        rankings=performance_rankings,
    );