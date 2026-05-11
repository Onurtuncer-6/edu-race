# language/translations.py
from flask import Blueprint, request, g, session;


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
            }
        }
    }
}

lang_bp = Blueprint('language', __name__);

@lang_bp.before_app_request
def set_language():
    url_lang = request.args.get('lang');

    if url_lang in ['tr', 'en']:
        session['selected_lang'] = url_lang;

    lang = session.get('selected_lang', 'tr');

    g.lang = lang;
    g.text = languages[lang];