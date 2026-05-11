# helpers/db_helper.py
from supabase import create_client;
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY);

class DatabaseHelper:
    @staticmethod
    def get_home_views_stats():
        try:
            schools = supabase.table("schools").select("id", count="exact").execute();
            races = supabase.table("activities").select("id", count="exact").execute();
            students = supabase.table("profiles").select("id", count="exact").eq("role", "student").execute();
            city_query = supabase.table("schools").select("city").execute();
            unique_cities = len(set(d['city'] for d in city_query.data)) if city_query.data else 0;
        
            return {
                "total_schools": schools.count or 0,
                "active_races": races.count or 0,
                "total_students": students.count or 0,
                "total_cities": unique_cities if unique_cities > 0 else 81 # Okul yoksa 81 gösterelim şık dursun
            }
        
        except Exception as e:
            print(f"DB Error: {e}")
            return {"total_schools": 0, "active_races": 0, "total_students": 0, "total_cities": 0}