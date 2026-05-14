from flask import Blueprint, request, g, session

languages = {
    "tr": {
        "home": {
            "title": "Edu-Race - Okullar Arası Yarış Platformu",
            "nav": {
                "logo": "EDURACE",
                "links": {
                    "how": "Nasıl Çalışır",
                    "features": "Özellikler",
                    "categories": "Kategoriler",
                    "ranking": "Sıralama"
                },
                "cta": "Ücretsiz Başla ->",
            },
            "hero": {
                "badge": "2026 Yarış Sezonu Başladı",
                "title_part1": "OKULUNU",
                "title_part2": "ZİRVEYE",
                "title_part3": "TAŞIMAYA HAZIR MISIN?",
                "description": "Türkiye genelindeki okullarla yarışın, kategorinizde en iyisi olduğunuzu kanıtlayın. Eğitimde rekabetin en dijital hali burada.",
                "btn_register": "Hemen Kaydol",
                "btn_demo": "Yarışları İzle"
            },
            "stats": {
                "schools": "Kayıtlı Okul",
                "races": "Aktif Yarış",
                "students": "Toplam Öğrenci",
                "cities": "Şehir"
            },
            "how_it_works": {
                "label": "SİSTEM İŞLEYİŞİ",
                "title": "4 Adımda Dijital Yönetim",
                "steps": [
                    {"title": "Kurumsal Tanımlama", "desc": "Okul yöneticisi yetkilendirmesiyle kurumunuzu sisteme entegre edin ve resmi profilinizi oluşturun."},
                    {"title": "Faaliyet Alanı Seçimi", "desc": "Akademik, kültürel veya sportif branşlar arasından kurumunuzun yetkinliklerine uygun alanları belirleyin."},
                    {"title": "Veri Girişi ve Analiz", "desc": "Gerçekleştirilen faaliyetlerin sonuçlarını sisteme aktararak performans verilerinin işlenmesini sağlayın."},
                    {"title": "Sertifikasyon", "desc": "Elde edilen başarıları resmi raporlara dönüştürün ve kurum sıralamasındaki yerinizi güncelleyin."}
                ]
            },
            "ranking": {
                "title": "KURUMSAL PERFORMANS SIRALAMASI",
                "subtitle": "ULUSAL AKADEMİK BAŞARI ENDEKSİ — 2026",
                "math_ranking_title": "CANLI MATEMATİK SIRALAMASI",
                "live_text": "CANLI",
                "no_data": "Henüz veri girişi yapılmadı.",
                "global": "Küresel Ölçek",
                "tr": "Ulusal Ölçek",
                "table_school": "Okul Adı",
                "table_city": "Şehir",
                "table_points": "Puan"
            }
        }
    },
    "en": {
        "home": {
            "title": "EduRace — School Competition Platform",
            "nav": {
                "logo": "EDURACE",
                "links": {
                    "how": "How It Works",
                    "features": "Features",
                    "categories": "Categories",
                    "ranking": "Rankings"
                },
                "cta": "Get Started Free ->"
            },
            "hero": {
                "badge": "2026 Race Season Started",
                "title_part1": "BRING YOUR",
                "title_part2": "SCHOOL",
                "title_part3": "TO THE TOP",
                "description": "Compete with schools across the nation. Prove that you are the best in your category. The most digital form of educational competition is here.",
                "btn_register": "Register Now",
                "btn_demo": "Watch Races"
            },
            "stats": {
                "schools": "Registered Schools",
                "races": "Active Races",
                "students": "Total Students",
                "cities": "Cities"
            },
            "how_it_works": {
                "label": "SYSTEM OPERATIONS",
                "title": "Digital Management in 4 Steps",
                "steps": [
                    {"title": "Institutional Integration", "desc": "Integrate your institution through authorized administrator access and establish your official profile."},
                    {"title": "Category Selection", "desc": "Identify fields consistent with your institution's competencies among academic, cultural, or athletic branches."},
                    {"title": "Data Entry & Analysis", "desc": "Transfer activity results to the system to ensure the processing of institutional performance data."},
                    {"title": "Official Reporting", "desc": "Convert achievements into official reports and update your standing in the institutional rankings."}
                ]
            },
            "ranking": {
                "title": "INSTITUTIONAL PERFORMANCE RANKINGS",
                "subtitle": "NATIONAL ACADEMIC ACHIEVEMENT INDEX — 2026",
                "math_ranking_title": "LIVE MATHEMATICS RANKINGS",
                "live_text": "LIVE",
                "no_data": "No data available yet.",
                "global": "Global Scale",
                "tr": "National Scale",
                "table_school": "School Name",
                "table_city": "City",
                "table_points": "Points"
            }
        }
    }
}

lang_bp = Blueprint('language', __name__)

@lang_bp.before_app_request
def set_language():
    url_lang = request.args.get('lang')
    if url_lang in ['tr', 'en']:
        session['selected_lang'] = url_lang
    lang = session.get('selected_lang', 'tr')
    g.lang = lang
    g.text = languages[lang]