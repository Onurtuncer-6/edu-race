# routes/views.py
from flask import Blueprint, render_template, g, request
from helpers.db_helper import DatabaseHelper
from datetime import datetime

views_bp = Blueprint('views', __name__)

@views_bp.route('/', methods=['GET'])
def home():
    scope = request.args.get('scope')
    lang = g.lang
    
    # Mevcut veriler
    live_stats = DatabaseHelper.get_home_views_stats()
    performance_rankings = DatabaseHelper.get_home_performance_rankings(scope=scope)
    weekly_rankings = DatabaseHelper.get_weekly_leaderboard(scope=scope)
    weekly_stats = DatabaseHelper.get_weekly_stats()
    
    # YENİ: Madalyalar ve Haftalık Detaylar
    top_medal_city = DatabaseHelper.get_medals_by_city(lang=lang)
    rising_school = DatabaseHelper.get_weekly_ranking_details(lang=lang)
    current_date = datetime.now().strftime("%d.%m.%Y") # Güncel tarih
    
    return render_template(
        'home.html', 
        stats=live_stats,
        rankings=performance_rankings,
        weekly_rankings=weekly_rankings,
        weekly_stats=weekly_stats,
        top_medal_city=top_medal_city,   # Şehir bazlı madalyalar
        rising_school=rising_school,     # Haftalık liderin detayları
        current_date=current_date        # Tablo başındaki tarih
    )