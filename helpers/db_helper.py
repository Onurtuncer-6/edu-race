# helpers/db_helper.py
import time
from supabase import create_client
from config import Config

# Supabase bağlantısı
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

class DatabaseHelper:
    _cache = {}
    CACHE_DURATION = 600  # 10 dakika önbellek

    @classmethod
    def _get_cached_data(cls, key):
        """Önbellekten veri çeker, süresi dolmuşsa None döner."""
        if key in cls._cache:
            data, expiry = cls._cache[key]
            if time.time() < expiry:
                return data
            else:
                del cls._cache[key]
        return None

    @classmethod
    def _set_cached_data(cls, key, data):
        """Veriyi belirlenen süreyle önbelleğe kaydeder."""
        cls._cache[key] = (data, time.time() + cls.CACHE_DURATION)

    @staticmethod
    def get_home_views_stats():
        """
        get_site_stats RPC fonksiyonunu çağırarak ana sayfa sayaçlarını döndürür.
        """
        cache_key = "global_stats"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            # SQL tarafındaki JSON dönen get_site_stats fonksiyonunu çağırıyoruz
            response = supabase.rpc('get_site_stats').execute()
            if response.data:
                DatabaseHelper._set_cached_data(cache_key, response.data)
                return response.data
        except Exception as e:
            print(f"Stats Veri Çekme Hatası: {e}")
        
        return {"total_schools": 0, "active_races": 0, "total_students": 0, "total_cities": 0}

    @staticmethod
    def get_home_performance_rankings(scope=None):
        """
        get_leaderboard RPC fonksiyonunu kullanarak okul bazlı puanları (dinamik SUM) getirir.
        """
        try:
            from flask import g
            lang = scope or getattr(g, 'lang', 'tr')
        except ImportError:
            lang = scope or 'tr'

        cache_key = f"leaderboard_{lang}"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached

        # SQL parametresi için Türkiye veya boş string gönderiyoruz
        country_param = "Türkiye" if lang == "tr" else ""

        try:
            # SQL'deki get_leaderboard(p_country) fonksiyonunu çağırıyoruz
            response = supabase.rpc(
                'get_leaderboard', 
                {'p_country': country_param}
            ).execute()

            if response.data:
                # SQL'den res_name, res_points, res_city, res_district olarak geliyor
                formatted_rankings = [
                    {
                        "school_name": item.get("res_name"),
                        "total_points": int(item.get("res_points", 0)), # BIGINT'i güvenli int yapıyoruz
                        "city": item.get("res_city"),
                        "district": item.get("res_district")
                    } for item in response.data
                ]
                DatabaseHelper._set_cached_data(cache_key, formatted_rankings)
                return formatted_rankings
        except Exception as e:
            print(f"Sıralama Veri Çekme Hatası: {e}")

        return []

    @staticmethod
    def clear_cache():
        """Gerektiğinde önbelleği temizlemek için kullanılır."""
        DatabaseHelper._cache = {}