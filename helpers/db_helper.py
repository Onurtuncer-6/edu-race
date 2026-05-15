import time
from supabase import create_client
from config import Config

# Supabase bağlantısı
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

class DatabaseHelper:
    _cache = {}
    CACHE_DURATION = 600  # Standart cache süresi: 10 dakika

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
    def _set_cached_data(cls, key, data, duration=None):
        """Veriyi belirlenen süreyle önbelleğe kaydeder."""
        expire_time = time.time() + (duration if duration else cls.CACHE_DURATION)
        cls._cache[key] = (data, expire_time)

    @staticmethod
    def get_school_medal_counts(school_id):
        """
        Bir okulun geçmişten bugüne kazandığı madalya özetini 
        doğrudan medal_history tablosundan döner.
        """
        if not school_id:
            return {"gold": 0, "silver": 0, "bronze": 0}
            
        try:
            response = supabase.table('medal_history')\
                .select('medal_type')\
                .eq('school_id', school_id)\
                .execute()
            
            counts = {"gold": 0, "silver": 0, "bronze": 0}
            if response.data:
                for row in response.data:
                    m_type = row['medal_type']
                    if m_type in counts:
                        counts[m_type] += 1
            return counts
        except Exception as e:
            print(f"Madalya çekme hatası: {e}")
            return {"gold": 0, "silver": 0, "bronze": 0}

    @staticmethod
    def get_home_views_stats():
        """Genel istatistikleri döndürür (tüm zamanlar)."""
        cache_key = "global_stats"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            response = supabase.rpc('get_site_stats').execute()
            if response.data:
                DatabaseHelper._set_cached_data(cache_key, response.data)
                return response.data
        except Exception as e:
            print(f"Stats Veri Çekme Hatası: {e}")
        
        return {
            "total_schools": 0,
            "active_races": 0,
            "total_students": 0,
            "total_cities": 0
        }

    @staticmethod
    def get_weekly_stats():
        """Haftalık istatistikleri döndürür."""
        cache_key = "weekly_stats"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            response = supabase.rpc('get_weekly_stats').execute()
            if response.data:
                DatabaseHelper._set_cached_data(cache_key, response.data)
                return response.data
        except Exception as e:
            print(f"Weekly Stats Veri Çekme Hatası: {e}")
        
        return {
            "total_schools": 0,
            "weekly_activities": 0,
            "weekly_points_distributed": 0,
            "total_students": 0,
            "total_cities": 0
        }

    @staticmethod
    def get_home_performance_rankings(scope=None):
        """Genel (All-Time) okul sıralamalarını ve madalyalarını döndürür."""
        try:
            from flask import g
            lang = scope or getattr(g, 'lang', 'tr')
        except ImportError:
            lang = 'tr'
        
        cache_key = f"leaderboard_{lang}"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached
        
        country_param = "Türkiye" if lang == "tr" else ""
        
        try:
            response = supabase.rpc(
                'get_leaderboard',
                {'p_country': country_param}
            ).execute()
            
            if response.data:
                formatted_rankings = []
                for item in response.data:
                    # Okul ID'sini (res_id) kullanarak madalyaları çekiyoruz
                    s_id = item.get("res_id")
                    medals = DatabaseHelper.get_school_medal_counts(s_id)
                    
                    formatted_rankings.append({
                        "school_name": item.get("res_name"),
                        "total_points": int(item.get("res_points", 0)),
                        "city": item.get("res_city"),
                        "district": item.get("res_district"),
                        "medal_counts": medals
                    })
                DatabaseHelper._set_cached_data(cache_key, formatted_rankings)
                return formatted_rankings
        except Exception as e:
            print(f"Sıralama Veri Çekme Hatası: {e}")
        
        return []

    @staticmethod
    def get_weekly_leaderboard(scope=None):
        """HAFTALIK okul sıralamalarını ve madalyalarını döndürür."""
        try:
            from flask import g
            lang = scope or getattr(g, 'lang', 'tr')
        except ImportError:
            lang = 'tr'
        
        cache_key = f"weekly_leaderboard_{lang}"
        cached = DatabaseHelper._get_cached_data(cache_key)
        if cached:
            return cached
        
        country_param = "Türkiye" if lang == "tr" else ""
        
        try:
            response = supabase.rpc(
                'get_weekly_leaderboard',
                {'p_country': country_param}
            ).execute()
            
            if response.data:
                formatted_rankings = []
                for item in response.data:
                    s_id = item.get("res_id")
                    medals = DatabaseHelper.get_school_medal_counts(s_id)
                    
                    formatted_rankings.append({
                        "school_name": item.get("res_name"),
                        "weekly_points": int(item.get("res_weekly_points", 0)),
                        "activity_count": item.get("res_activity_count", 0),
                        "city": item.get("res_city"),
                        "district": item.get("res_district"),
                        "medal_counts": medals
                    })
                # Haftalık veriyi 2 dakika cache'le
                DatabaseHelper._set_cached_data(cache_key, formatted_rankings, duration=120)
                return formatted_rankings
        except Exception as e:
            print(f"Haftalık Sıralama Veri Çekme Hatası: {e}")
        
        return []

    @staticmethod
    def get_weekly_ranking_details(lang='tr'):
        """Haftalık en yükselen okulu ve detaylarını (madalyalar dahil) döndürür."""
        try:
            # Önce haftalık sıralamayı alıyoruz
            weekly = DatabaseHelper.get_weekly_leaderboard(lang)
            all_time = DatabaseHelper.get_home_performance_rankings(lang)
            
            if not weekly or not all_time:
                return None
            
            # Haftalık 1. olan okulun tüm verilerini al
            top_weekly_school = weekly[0] 
            # DİKKAT: get_weekly_leaderboard zaten içinde madalyaları çekiyor (medal_counts)
            
            top_school_name = top_weekly_school['school_name']
            
            # Genel sıralamadaki yerini bul
            all_time_rank = None
            for idx, school in enumerate(all_time, 1):
                if school['school_name'] == top_school_name:
                    all_time_rank = idx
                    break
            
            # Burada tüm verileri birleştirip gönderiyoruz
            return {
                "school_name": top_school_name,
                "city": top_weekly_school.get('city'),
                "weekly_points": top_weekly_school.get('weekly_points'),
                "all_time_rank": all_time_rank,
                "rise_amount": all_time_rank if all_time_rank else "N/A",
                "medal_counts": top_weekly_school.get('medal_counts') # BU SATIR EKSİKTİ
            }
        except Exception as e:
            print(f"Haftalık Detay Çekme Hatası: {e}")
            return None

    @staticmethod
    def get_medals_by_city(lang='tr'):
        """Şehir bazında en çok madalyası olan şehri (hesaplayarak) döndürür."""
        try:
            rankings = DatabaseHelper.get_home_performance_rankings(lang)
            if not rankings:
                return None
            
            medals_by_city = {}
            for idx, school in enumerate(rankings, 1):
                city = school.get('city', 'Unknown')
                if city not in medals_by_city:
                    medals_by_city[city] = {"gold": 0, "silver": 0, "bronze": 0, "city": city}
                
                if idx == 1: medals_by_city[city]["gold"] += 1
                elif idx in [2, 3]: medals_by_city[city]["silver"] += 1
                elif idx in range(4, 7): medals_by_city[city]["bronze"] += 1
            
            if medals_by_city:
                return max(medals_by_city.values(), 
                           key=lambda x: (x["gold"] * 3 + x["silver"] * 2 + x["bronze"]))
            return None
        except Exception as e:
            print(f"Madalya Hesaplama Hatası: {e}")
            return None

    @staticmethod
    def clear_cache():
        """Önbelleği temizler."""
        DatabaseHelper._cache = {}