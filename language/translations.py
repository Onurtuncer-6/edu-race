from flask import Blueprint, request, g, session

languages = {
    "tr": {
        "home": {
            "title": "Edu-Race - Dijital Eğitim ve Performans Ekosistemi",
            "nav": {
                "logo": "EDURACE",
                "links": {
                    "how": "Nasıl Çalışır",
                    "features": "Özellikler",
                    "categories": "Kategoriler",
                    "ranking": "Sıralama"
                },
                "cta": "Kurumsal Erişim",
            },
            "hero": {
                "badge": "2026 Akademik Rekabet Sezonu Aktif",
                "title_part1": "OKULUNU",
                "title_part2": "ZİRVEYE",
                "title_part3": "TAŞIMAYA HAZIR MISIN?",
                "description": "Türkiye genelindeki okullarla yarışın, kategorinizde en iyisi olduğunuzu kanıtlayın. Eğitimde rekabetın en dijital hali burada.",
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
                "label": "ULUSAL SIRALAMA",
                "math_ranking_title": "CANLI MATEMATİK SIRALAMASI",
                "live_text": "CANLI",
                "no_data": "Henüz veri girişi yapılmadı.",
                "global": "Küresel Ölçek",
                "tr": "Ulusal Ölçek",
                "table_rank": "#",
                "table_school": "OKUL",
                "table_city": "ŞEHİR",
                "table_points": "PUAN",
                "table_change": "DEĞİŞİM",
                "weekly_highest": "BU HAFTANIN EN YÜKSELENI",
                "active_season": "AKTİF SEZON",
                "most_winning_city": "EN ÇOK KAZANAN ŞEHİR",
                "season_info": "Sezon sonu: 30 Haziran 2025 • 48 yarışma tamamlandı",
                "highest_riser_desc": "Bu hafta 3 basamak yükseldi — Konya, Fen & Matematik",
                "season_achievement": "Bu sezonda 14 altın, 9 gümüş, 12 bronz madalya",
                "medal_gold": "1. Altın",
                "medal_silver": "2. Gümüş",
                "medal_bronze": "3. Tunç",
                "medal_collection": "Okul Madalya Koleksiyonu",
                "total_medals": "Toplam Başarı",
                "week_suffix": ". Hafta",
                "medal_summary": "{gold} Altın, {silver} Gümüş, {bronze} Bronz",
                "medal_gold": "Altın Madalya",
                "medal_silver": "Gümüş Madalya",
                "medal_bronze": "Bronz Madalya"
            },
            "ecosystem": {
                "title": "BÜTÜNLEŞİK EĞİTİM EKOSİSTEMİ",
                "subtitle": "OKUL, VELİ VE ÖĞRENCİ ARASINDAKİ DİJİTAL KÖPRÜ",
                "attendance": {
                    "title": "Akıllı Yoklama ve Anlık Bildirim",
                    "desc": "Müdür tarafından konfigüre edilen okul saatleri uyarınca, öğretmen yoklama aldığı an veriler işlenir ve veliye yüksek öncelikli bildirim iletilir. Devamsızlık takibi sıfır hata payı ile dijitalleştirilir."
                },
                "qa_social": {
                    "title": "Kolektif Bilgi ve Soru Paylaşım Ağı",
                    "desc": "Öğrenciler, kurum içi veya ağlar arası etkileşim kurarak karmaşık problemleri birlikte çözer. Her başarılı çözüm hem bireysel gelişime hem de okulun genel başarı endeksine doğrudan katkı sağlar."
                },
                "parent_portal": {
                    "title": "Veli Stratejik Katılım Merkezi",
                    "desc": "Veliler, müfredat ve ders programı takibinin ötesine geçerek kurumsal anketlere katılır. Bu aktif katılım, okulun gelişim süreçlerini desteklerken kurumsal başarı puanını maksimize eder."
                }
            },
            "categories_section": {
                "label": "YARIŞMA BRANŞLARI",
                "title": "Zirve İçin Yarışacağınız Kategoriler",
                "description": "Akademik disiplinlerden teknolojiye kadar geniş bir yelpazede okulunuzun yetkinliklerini kanıtlayın.",
                "items": [
                    {"icon": "📐", "title": "İleri Matematik", "desc": "Analitik düşünme ve problem çözme hızının ölçüldüğü, okullar arası en prestijli lig."},
                    {"icon": "🧪", "title": "Fen Bilimleri", "desc": "Fizik, Kimya ve Biyoloji alanlarındaki deneysel veriler ve teorik bilgi yarışları."},
                    {"icon": "💻", "title": "Yazılım & Bilişim", "desc": "Algoritma geliştirme ve dijital üretim projeleriyle geleceğin teknolojisinde yarışın."},
                    {"icon": "📚", "title": "Edebiyat & Dil", "desc": "Okuma kültürü, dil bilgisi ve kompozisyon yetkinliklerinin kurumsal bazda değerlendirilmesi."},
                    {"icon": "🌍", "title": "Sosyal Bilimler", "desc": "Tarih, Coğrafya ve Felsefe disiplinlerinde genel kültür ve analiz yeteneği odaklı puanlama."},
                    {"icon": "🇬🇧", "title": "Yabancı Diller", "desc": "İngilizce ve diğer dillerde dil yetkinliği ve küresel iletişim becerileri yarışı."}
                ]
            }
        }
    },
    "en": {
        "home": {
            "title": "EduRace — Digital Education & Performance Ecosystem",
            "nav": {
                "logo": "EDURACE",
                "links": {
                    "how": "How It Works",
                    "features": "Features",
                    "categories": "Categories",
                    "ranking": "Rankings"
                },
                "cta": "Institutional Access"
            },
            "hero": {
                "badge": "2026 Academic Competition Season Active",
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
                "label": "NATIONAL RANKINGS",
                "math_ranking_title": "LIVE MATHEMATICS RANKINGS",
                "live_text": "LIVE",
                "no_data": "No data available yet.",
                "global": "Global Scale",
                "tr": "National Scale",
                "table_rank": "#",
                "table_school": "SCHOOL",
                "table_city": "CITY",
                "table_points": "POINTS",
                "table_change": "CHANGE",
                "weekly_highest": "THIS WEEK'S HIGHEST RISER",
                "active_season": "ACTIVE SEASON",
                "most_winning_city": "MOST WINNING CITY",
                "season_info": "Season ends: June 30, 2025 • 48 competitions completed",
                "highest_riser_desc": "Rose 3 positions this week — Konya, Science & Mathematics",
                "season_achievement": "14 gold, 9 silver, 12 bronze medals this season",
                "medal_gold": "1st Gold",
                "medal_silver": "2nd Silver",
                "medal_bronze": "3rd Bronze",
                "medal_collection": "School Medal Collection",
                "total_medals": "Total Achievements",
                "week_suffix": "th Week",
                "medal_summary": "{gold} Gold, {silver} Silver, {bronze} Bronze",
                "medal_gold": "Gold Medal",
                "medal_silver": "Silver Medal",
                "medal_bronze": "Bronze Medal"
            },
            "ecosystem": {
                "title": "INTEGRATED EDUCATION ECOSYSTEM",
                "subtitle": "THE DIGITAL BRIDGE BETWEEN SCHOOL, PARENT, AND STUDENT",
                "attendance": {
                    "title": "Smart Attendance & Instant Alerts",
                    "desc": "In accordance with hours set by the principal, parents receive high-priority alerts the moment attendance is taken. Attendance tracking is fully digitized with zero margin for error."
                },
                "qa_social": {
                    "title": "Collective Knowledge & Question Network",
                    "desc": "Students solve complex problems through peer-to-peer interaction. Every successful solution contributes to both individual growth and the institution's overall success index."
                },
                "parent_portal": {
                    "title": "Strategic Parent Engagement Center",
                    "desc": "Parents go beyond monitoring schedules to participate in institutional surveys. This active engagement supports development processes while maximizing the school's performance score."
                }
            },
            "categories_section": {
                "label": "COMPETITION CATEGORIES",
                "title": "Disciplines to Race for the Top",
                "description": "Prove your institution's competencies across a wide range of academic and technology disciplines.",
                "items": [
                    {"icon": "📐", "title": "Advanced Mathematics", "desc": "The most prestigious league for analytical thinking and problem-solving speed."},
                    {"icon": "🧪", "title": "Natural Sciences", "desc": "Institutional races based on experimental data and theoretical knowledge in Physics, Chemistry, and Biology."},
                    {"icon": "💻", "title": "Software & IT", "desc": "Compete in the technology of the future with algorithm development and digital production projects."},
                    {"icon": "📚", "title": "Literature & Language", "desc": "Institutional assessment of reading culture, grammar, and composition skills."},
                    {"icon": "🌍", "title": "Social Sciences", "desc": "Scoring focused on general knowledge and analysis in History, Geography, and Philosophy."},
                    {"icon": "🇬🇧", "title": "Foreign Languages", "desc": "A competition of linguistic proficiency and global communication skills."}
                ]
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