# language/translations.py
from flask import Blueprint, request, g, session;


languages = {
    "tr": {
        "home": {
            "title": "Edu-Race"
        }
    },
    "en": {
        "home": {
            "title": "Edu-Race"
        }
    }
};

lang_bp = Blueprint('language', __name__);

@lang_bp.before_app_request
def set_language():
    url_lang = request.args.get('lang');

    if url_lang in ['tr', 'en']:
        session['selected_lang'] = url_lang;

    lang = session.get('selected_lang', 'tr');

    g.lang = lang;
    g.text = languages[lang];