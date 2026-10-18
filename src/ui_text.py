"""Interface text for the AirShift dashboard in English, Tamil, Marathi and Hindi."""

LANG_LABELS = {"en": "English", "ta": "தமிழ்", "mr": "मराठी", "hi": "हिन्दी"}

T = {
    "en": {
        "tagline": "Find the cleanest hours to work or play outside.",
        "tab_plan": "My day", "tab_past": "A past day", "tab_india": "City patterns", "tab_eval": "How accurate", "tab_about": "About",
        "plan_intro": "Choose where you are and what you do. We will tell you the best hours to be outside.",
        "pick_city": "Choose your city", "result_title": "Your result",
        "hint_steps": "Choose your city and your work below. Your best time and forecast will appear here.",
        "where": "1. Where are you?", "when": "2. When?", "who": "3. Who are you?",
        "tomorrow": "Tomorrow", "today": "Rest of today", "best": "Best time",
        "avoid": "Avoid if you can", "saving": "About {pct}% less pollution than your usual time ({fixed})",
        "usual_ok": "Your usual time is already close to the best.", "confidence": "Confidence",
        "hourly": "Hour by hour", "your_plan": "Your plan", "usual": "Usual time",
        "periods": ("Morning", "Afternoon", "Evening", "Night"), "share": "Message to share",
        "share_help": "Copy this and send it on WhatsApp or SMS.", "details": "More details",
        "no_time": "Not enough time is left today for this plan. Choose Tomorrow.",
        "no_net": "Live air-quality data could not be loaded. Check the internet connection and try again.",
        "source": "Forecast from the CAMS global air-quality model (Open-Meteo.com). A planning aid, not medical advice.",
        "updated_on": "Updated {t}.", "dose_note": "Forecast pollution breathed with this plan: {d:,.0f} µg.",
        "first_then": "First {a}, then {b}", "then": "then",
        "custom_title": "Describe your work", "group": "Who will do it?", "adult": "Adult", "youth": "Student (16 to 20)",
        "start_w": "Earliest start", "end_w": "Must finish by", "usual_start": "Usual start", "task": "Task", "hours": "Hours",
        "effort": "Effort", "wording": "This is for", "work": "Work", "sport": "Sports",
        "add_task": "Add at least one task with hours.", "too_long": "These tasks need {n} hours, but the window has only {w}. Widen the window or shorten the tasks.",
        "bad_usual": "The usual start must let all tasks finish inside the window.",
        "past_intro": "Pick any day in 2024. AirShift plans it using only the forecast it would have had the evening before. Then you can see what really happened.",
        "city": "City", "day": "Day", "reveal": "Show what really happened",
        "reveal_note": "Top row: forecast. Thin row: measured air that day.",
        "no_meas": "Some hours of this day have no measurement, so the air breathed cannot be worked out. Please pick another day.",
        "m_with": "Breathed with AirShift", "m_usual": "Breathed at usual time", "m_best": "Best possible, in hindsight",
        "vs_usual": "vs usual time", "new_note": "This is a new city. The model never saw it during training.", "new_tag": "(new city)",
        "india_intro": "When is the air cleanest, and how much does it change through the day? Data: pollution stations across India, 2020 to 2024.",
        "ratio": "On a typical day in {city}, the dirtiest hour has {r} times the pollution of the cleanest hour.",
        "cleanest_cap": "Usually the cleanest hour between 6 AM and 9 PM in each city.",
        "rhythm": "Daily pattern of all cities", "eigen": "Day types (advanced)",
        "eval_intro": "We tested AirShift on real 2024 measurements in {n} cities, and on {m} new cities it had never seen.",
        "m_mae": "Typical error of the forecast", "m_mae_help": "{x}% better than yesterday's pattern",
        "m_cover": "Forecast range is right", "m_cover_help": "in core cities",
        "m_new": "Right in new cities", "m_new_help": "in new cities",
        "avoid_q": "How much pollution could people have avoided?",
        "captured_help": "\"Captured\" means how much of the best possible saving AirShift actually reached.",
        "new_expander": "New cities ({n}), including Vellore and Coimbatore", "conf_expander": "Does the confidence label mean anything?",
        "col_who": "Who", "col_saving": "Less pollution than usual time (%)", "col_best": "Best possible (%)",
        "col_airshift": "AirShift reached (%)", "col_typical": "Typical-day plan reached (%)",
        "about_body": """**AirShift** tells outdoor workers and students *when* to be outside, not just how bad the air is.

1. It forecasts pollution for every hour from 6 AM to 9 PM.
2. It works out how much pollution a person breathes for their kind of work, using breathing rates from the U.S. EPA Exposure Factors Handbook (2011).
3. It tries every possible start time and task order and picks the one with the least pollution breathed.
4. It explains the result in English, Tamil, Marathi or Hindi, with a confidence level.

**My day** uses live forecasts from the CAMS global model (Open-Meteo.com). **A past day** uses the trained {model} model on pollution station data for {n} cities across India, so you can compare the plan with what really happened.

This is a planning aid, not medical advice.""",
    },
    "ta": {
        "tagline": "வெளியே வேலை செய்ய அல்லது விளையாட மிகச் சுத்தமான நேரத்தைக் கண்டறியுங்கள்.",
        "tab_plan": "இன்றைய நாள்", "tab_past": "கடந்த நாள்", "tab_india": "நகர நிலவரம்", "tab_eval": "எவ்வளவு சரி", "tab_about": "பற்றி",
        "plan_intro": "நீங்கள் எங்கே இருக்கிறீர்கள், என்ன வேலை செய்கிறீர்கள் என்பதைத் தேர்ந்தெடுங்கள். வெளியே இருக்க சிறந்த நேரத்தை நாங்கள் சொல்வோம்.",
        "pick_city": "உங்கள் நகரத்தைத் தேர்ந்தெடுக்கவும்", "result_title": "உங்கள் முடிவு",
        "hint_steps": "கீழே உங்கள் நகரத்தையும் வேலையையும் தேர்ந்தெடுக்கவும். உங்கள் சிறந்த நேரமும் முன்னறிவிப்பும் இங்கே தோன்றும்.",
        "where": "1. நீங்கள் எங்கே இருக்கிறீர்கள்?", "when": "2. எப்போது?", "who": "3. நீங்கள் யார்?",
        "tomorrow": "நாளை", "today": "இன்று மீதமுள்ள நேரம்", "best": "சிறந்த நேரம்",
        "avoid": "முடிந்தால் தவிர்க்கவும்", "saving": "உங்கள் வழக்கமான நேரத்தை விட சுமார் {pct}% குறைவான மாசு ({fixed})",
        "usual_ok": "உங்கள் வழக்கமான நேரமே ஏறக்குறைய சிறந்த நேரம்தான்.", "confidence": "நம்பகத்தன்மை",
        "hourly": "மணி மணியாக காற்றின் நிலை", "your_plan": "உங்கள் திட்டம்", "usual": "வழக்கமான நேரம்",
        "periods": ("காலை", "மதியம்", "மாலை", "இரவு"), "share": "மற்றவர்களுக்கு அனுப்ப",
        "share_help": "இதை நகலெடுத்து WhatsApp அல்லது SMS மூலம் அனுப்புங்கள்.", "details": "மேலும் விவரங்கள்",
        "no_time": "இன்று இந்தத் திட்டத்திற்கு போதிய நேரம் இல்லை. 'நாளை' என்பதைத் தேர்ந்தெடுக்கவும்.",
        "no_net": "நேரடி காற்றுத் தகவல் கிடைக்கவில்லை. இணைய இணைப்பைச் சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
        "source": "முன்னறிவிப்பு CAMS உலகளாவிய மாடலில் இருந்து (Open-Meteo.com). திட்டமிட உதவும் கருவி மட்டுமே, மருத்துவ ஆலோசனை அல்ல.",
        "updated_on": "{t} அன்று புதுப்பிக்கப்பட்டது.", "dose_note": "இந்தத் திட்டத்தில் முன்னறிவிப்பின்படி சுவாசிக்கும் மாசு: {d:,.0f} µg.",
        "first_then": "முதலில் {a}, பிறகு {b}", "then": "பிறகு",
        "custom_title": "உங்கள் வேலையை விவரியுங்கள்", "group": "யார் செய்வார்கள்?", "adult": "பெரியவர்", "youth": "மாணவர் (16 முதல் 20 வயது)",
        "start_w": "எந்த நேரத்திலிருந்து தொடங்கலாம்", "end_w": "எந்த நேரத்திற்குள் முடிக்க வேண்டும்", "usual_start": "வழக்கமான தொடக்கம்",
        "task": "வேலை", "hours": "மணி நேரம்", "effort": "உழைப்பு", "wording": "இது எதற்காக", "work": "வேலை", "sport": "விளையாட்டு",
        "add_task": "குறைந்தது ஒரு வேலையையும் அதற்கான மணி நேரத்தையும் சேர்க்கவும்.",
        "too_long": "இந்த வேலைகளுக்கு {n} மணி நேரம் தேவை, ஆனால் நேரம் {w} மணி மட்டுமே உள்ளது. நேரத்தை நீட்டவும் அல்லது வேலையைக் குறைக்கவும்.",
        "bad_usual": "வழக்கமான தொடக்க நேரத்தில் எல்லா வேலைகளும் நேர வரம்புக்குள் முடிய வேண்டும்.",
        "past_intro": "2024 இல் எந்த நாளையும் தேர்ந்தெடுங்கள். அந்த மாலைக்கு முன் கிடைத்த முன்னறிவிப்பை மட்டும் வைத்து AirShift திட்டமிடும். பிறகு உண்மையில் என்ன நடந்தது என்று பார்க்கலாம்.",
        "city": "நகரம்", "day": "நாள்", "reveal": "உண்மையில் என்ன நடந்தது என்று காட்டு",
        "reveal_note": "மேல் வரிசை: முன்னறிவிப்பு. மெல்லிய வரிசை: அந்த நாளில் அளக்கப்பட்ட காற்று.",
        "no_meas": "இந்த நாளின் சில மணி நேரங்களுக்கு அளவீடு இல்லை. அதனால் சுவாசித்த மாசை கணக்கிட முடியவில்லை. வேறு நாளைத் தேர்ந்தெடுக்கவும்.",
        "m_with": "AirShift உடன் சுவாசித்தது", "m_usual": "வழக்கமான நேரத்தில் சுவாசித்தது", "m_best": "பின்னோக்கிப் பார்த்தால் சிறந்தது",
        "vs_usual": "வழக்கமான நேரத்தை விட", "new_note": "இது புதிய நகரம். பயிற்சியின் போது இந்த மாடல் இதைப் பார்த்ததில்லை.", "new_tag": "(புதிய நகரம்)",
        "india_intro": "காற்று எப்போது மிகச் சுத்தமாக இருக்கும், நாள் முழுவதும் அது எவ்வளவு மாறுகிறது? தரவு: இந்தியா முழுவதும் உள்ள மாசு அளவீட்டு நிலையங்கள், 2020 முதல் 2024 வரை.",
        "ratio": "{city} நகரில் ஒரு சாதாரண நாளில், மிக மாசான மணி நேரத்தில் உள்ள மாசு, மிகச் சுத்தமான மணி நேரத்தை விட {r} மடங்கு.",
        "cleanest_cap": "ஒவ்வொரு நகரத்திலும் காலை 6 முதல் இரவு 9 வரை பொதுவாக மிகச் சுத்தமான மணி நேரம்.",
        "rhythm": "எல்லா நகரங்களின் நாள் முறை", "eigen": "நாள் வகைகள் (மேம்பட்டது)",
        "eval_intro": "2024 இன் உண்மை அளவீடுகளில் {n} நகரங்களிலும், AirShift இதுவரை பார்த்திராத {m} புதிய நகரங்களிலும் சோதித்தோம்.",
        "m_mae": "முன்னறிவிப்பின் சராசரி பிழை", "m_mae_help": "நேற்றைய வடிவத்தை விட {x}% சிறந்தது",
        "m_cover": "முன்னறிவிப்பு வரம்பு சரியாக உள்ளது", "m_cover_help": "முக்கிய நகரங்களில்",
        "m_new": "புதிய நகரங்களில் சரியாக உள்ளது", "m_new_help": "புதிய நகரங்களில்",
        "avoid_q": "மக்கள் எவ்வளவு மாசைத் தவிர்த்திருக்கலாம்?",
        "captured_help": "\"அடைந்தது\" என்றால்: சாத்தியமான சிறந்த சேமிப்பில் AirShift உண்மையில் எவ்வளவு அடைந்தது என்பது.",
        "new_expander": "புதிய நகரங்கள் ({n}), வேலூர் மற்றும் கோயம்புத்தூர் உட்பட", "conf_expander": "நம்பகத்தன்மைக் குறியீட்டுக்கு பொருள் உள்ளதா?",
        "col_who": "யார்", "col_saving": "வழக்கமான நேரத்தை விடக் குறைவான மாசு (%)", "col_best": "சாத்தியமான சிறந்தது (%)",
        "col_airshift": "AirShift அடைந்தது (%)", "col_typical": "சாதாரண நாள் திட்டம் அடைந்தது (%)",
        "about_body": """**AirShift** வெளியே வேலை செய்பவர்களுக்கும் மாணவர்களுக்கும் காற்று எவ்வளவு மோசம் என்பதை மட்டும் சொல்லாமல், *எப்போது* வெளியே செல்வது நல்லது என்றும் சொல்கிறது.

1. காலை 6 முதல் இரவு 9 வரை ஒவ்வொரு மணி நேரத்துக்கும் மாசு அளவை முன்னறிவிக்கிறது.
2. ஒருவரின் வேலைக்கு ஏற்ப எவ்வளவு மாசு சுவாசிக்கப்படும் என்று கணக்கிடுகிறது (அமெரிக்க EPA கையேட்டின் சுவாச அளவுகள், 2011).
3. சாத்தியமான எல்லா தொடக்க நேரங்களையும் வேலை வரிசைகளையும் சோதித்து, குறைந்த மாசு சுவாசிக்கும் திட்டத்தைத் தேர்ந்தெடுக்கிறது.
4. முடிவை ஆங்கிலம், தமிழ், மராத்தி அல்லது ஹிந்தியில் நம்பகத்தன்மையுடன் விளக்குகிறது.

**இன்றைய நாள்** பகுதி CAMS உலகளாவிய மாடலின் நேரடி முன்னறிவிப்பைப் பயன்படுத்துகிறது (Open-Meteo.com). **கடந்த நாள்** பகுதி இந்தியா முழுவதும் {n} நகரங்களின் மாசு அளவீடுகளில் பயிற்சி பெற்ற {model} மாடலைப் பயன்படுத்துகிறது. அதனால் திட்டத்தையும் உண்மையில் நடந்ததையும் ஒப்பிட்டுப் பார்க்கலாம்.

இது திட்டமிட உதவும் கருவி மட்டுமே, மருத்துவ ஆலோசனை அல்ல.""",
    },
    "mr": {
        "tagline": "बाहेर काम किंवा खेळासाठी सर्वात स्वच्छ हवेचे तास शोधा.",
        "tab_plan": "माझा दिवस", "tab_past": "मागील दिवस", "tab_india": "शहरांचे पॅटर्न", "tab_eval": "किती अचूक", "tab_about": "माहिती",
        "plan_intro": "तुम्ही कुठे आहात आणि काय करता ते निवडा. बाहेर जाण्यासाठी सर्वोत्तम वेळ आम्ही सांगू.",
        "pick_city": "तुमचे शहर निवडा", "result_title": "तुमचा निकाल",
        "hint_steps": "खाली तुमचे शहर आणि काम निवडा. तुमची सर्वोत्तम वेळ आणि अंदाज इथे दिसेल.",
        "where": "1. तुम्ही कुठे आहात?", "when": "2. कधी?", "who": "3. तुम्ही कोण?",
        "tomorrow": "उद्या", "today": "आज उरलेला दिवस", "best": "सर्वात चांगली वेळ",
        "avoid": "शक्य असल्यास टाळा", "saving": "नेहमीच्या वेळेपेक्षा ({fixed}) सुमारे {pct}% कमी प्रदूषण",
        "usual_ok": "तुमची नेहमीची वेळही जवळपास सर्वात चांगली आहे.", "confidence": "खात्री",
        "hourly": "तासानुसार हवा", "your_plan": "तुमची योजना", "usual": "नेहमीची वेळ",
        "periods": ("सकाळ", "दुपार", "संध्याकाळ", "रात्र"), "share": "पाठवण्यासाठी संदेश",
        "share_help": "हा संदेश कॉपी करून WhatsApp किंवा SMS ने पाठवा.", "details": "अधिक माहिती",
        "no_time": "आज या योजनेसाठी पुरेसा वेळ उरलेला नाही. 'उद्या' निवडा.",
        "no_net": "लाईव्ह हवेची माहिती मिळाली नाही. इंटरनेट तपासून पुन्हा प्रयत्न करा.",
        "source": "अंदाज CAMS जागतिक मॉडेलवरून (Open-Meteo.com). फक्त नियोजनासाठी, वैद्यकीय सल्ला नाही.",
        "updated_on": "{t} रोजी अद्ययावत.", "dose_note": "या योजनेनुसार अंदाजित श्वासातून जाणारे प्रदूषण: {d:,.0f} µg.",
        "first_then": "आधी {a}, नंतर {b}", "then": "नंतर",
        "custom_title": "तुमचे काम सांगा", "group": "कोण करणार?", "adult": "प्रौढ", "youth": "विद्यार्थी (16 ते 20)",
        "start_w": "सर्वात लवकर सुरुवात", "end_w": "किती वाजेपर्यंत संपवायचे", "usual_start": "नेहमीची सुरुवात", "task": "काम",
        "hours": "तास", "effort": "मेहनत", "wording": "हे कशासाठी", "work": "काम", "sport": "खेळ",
        "add_task": "किमान एक काम आणि त्याचे तास लिहा.", "too_long": "या कामांना {n} तास लागतात, पण वेळेत फक्त {w} तास आहेत. वेळ वाढवा किंवा कामे कमी करा.",
        "bad_usual": "नेहमीची सुरुवात अशी हवी की सर्व कामे वेळेत संपतील.",
        "past_intro": "2024 मधील कोणताही दिवस निवडा. AirShift त्या दिवसाचे नियोजन फक्त आदल्या संध्याकाळी उपलब्ध असलेल्या अंदाजावर करेल. मग खरोखर काय घडले ते पाहा.",
        "city": "शहर", "day": "दिवस", "reveal": "खरोखर काय घडले ते दाखवा",
        "reveal_note": "वरची ओळ: अंदाज. पातळ ओळ: त्या दिवशी मोजलेली हवा.",
        "no_meas": "या दिवसाच्या काही तासांची नोंद नाही, त्यामुळे श्वासातून गेलेले प्रदूषण मोजता येत नाही. दुसरा दिवस निवडा.",
        "m_with": "AirShift सह श्वासातून गेलेले", "m_usual": "नेहमीच्या वेळी श्वासातून गेलेले", "m_best": "मागे वळून पाहता शक्य असलेले सर्वोत्तम",
        "vs_usual": "नेहमीच्या वेळेच्या तुलनेत", "new_note": "हे नवीन शहर आहे. प्रशिक्षणात मॉडेलने हे शहर कधीच पाहिले नव्हते.", "new_tag": "(नवीन शहर)",
        "india_intro": "हवा सर्वात स्वच्छ कधी असते आणि दिवसभरात ती किती बदलते? माहिती: संपूर्ण भारतातील प्रदूषण मापन केंद्रे, 2020 ते 2024.",
        "ratio": "{city} मध्ये सामान्य दिवशी सर्वात प्रदूषित तासात सर्वात स्वच्छ तासाच्या {r} पट प्रदूषण असते.",
        "cleanest_cap": "प्रत्येक शहरात सकाळी 6 ते रात्री 9 यादरम्यान साधारणपणे सर्वात स्वच्छ तास.",
        "rhythm": "सर्व शहरांचा दैनंदिन पॅटर्न", "eigen": "दिवसांचे प्रकार (प्रगत)",
        "eval_intro": "2024 मधील खऱ्या मोजमापांवर {n} शहरांमध्ये, आणि AirShift ने कधीच न पाहिलेल्या {m} नवीन शहरांमध्ये आम्ही चाचणी केली.",
        "m_mae": "अंदाजातील सरासरी चूक", "m_mae_help": "कालच्या पॅटर्नपेक्षा {x}% चांगले",
        "m_cover": "अंदाजाची मर्यादा बरोबर आहे", "m_cover_help": "मुख्य शहरांमध्ये",
        "m_new": "नवीन शहरांमध्ये बरोबर", "m_new_help": "नवीन शहरांमध्ये",
        "avoid_q": "लोक किती प्रदूषण टाळू शकले असते?",
        "captured_help": "\"मिळवलेले\" म्हणजे शक्य असलेल्या सर्वोत्तम बचतीपैकी AirShift ने प्रत्यक्ष किती मिळवले.",
        "new_expander": "नवीन शहरे ({n}), वेल्लोर आणि कोइंबतूरसह", "conf_expander": "खात्रीच्या चिन्हाला काही अर्थ आहे का?",
        "col_who": "कोण", "col_saving": "नेहमीच्या वेळेपेक्षा कमी प्रदूषण (%)", "col_best": "शक्य सर्वोत्तम (%)",
        "col_airshift": "AirShift ने मिळवले (%)", "col_typical": "सामान्य दिवसाची योजना मिळवली (%)",
        "about_body": """**AirShift** बाहेर काम करणाऱ्यांना आणि विद्यार्थ्यांना हवा किती वाईट आहे एवढेच नाही, तर *कधी* बाहेर जावे तेही सांगते.

1. सकाळी 6 ते रात्री 9 या प्रत्येक तासाचे प्रदूषण अंदाजते.
2. कामाच्या प्रकारानुसार व्यक्ती किती प्रदूषण श्वासातून घेईल याची गणना करते (U.S. EPA Exposure Factors Handbook, 2011 मधील श्वसन दर वापरून).
3. सुरुवातीच्या सर्व शक्य वेळा आणि कामांचे क्रम तपासते, आणि सर्वात कमी प्रदूषण असलेली योजना निवडते.
4. निकाल इंग्रजी, तमिळ, मराठी किंवा हिंदीत खात्रीच्या पातळीसह समजावते.

**माझा दिवस** भाग CAMS जागतिक मॉडेलचे थेट अंदाज वापरतो (Open-Meteo.com). **मागील दिवस** भाग भारतातील {n} शहरांच्या प्रदूषण डेटावर प्रशिक्षित {model} मॉडेल वापरतो, त्यामुळे योजना आणि प्रत्यक्ष घडलेले यांची तुलना करता येते.

हे नियोजनासाठी मदत करणारे साधन आहे, वैद्यकीय सल्ला नाही.""",
    },
    "hi": {
        "tagline": "बाहर काम या खेल के लिए सबसे साफ़ हवा के घंटे जानें।",
        "tab_plan": "मेरा दिन", "tab_past": "बीता हुआ दिन", "tab_india": "शहरों के पैटर्न", "tab_eval": "कितना सही", "tab_about": "जानकारी",
        "plan_intro": "बताएं आप कहाँ हैं और क्या करते हैं। हम बताएंगे बाहर जाने का सबसे अच्छा समय।",
        "pick_city": "अपना शहर चुनें", "result_title": "आपका नतीजा",
        "hint_steps": "नीचे अपना शहर और काम चुनें। आपका सबसे अच्छा समय और अनुमान यहाँ दिखेगा।",
        "where": "1. आप कहाँ हैं?", "when": "2. कब?", "who": "3. आप कौन हैं?",
        "tomorrow": "कल", "today": "आज का बाकी दिन", "best": "सबसे अच्छा समय",
        "avoid": "हो सके तो बचें", "saving": "सामान्य समय ({fixed}) से लगभग {pct}% कम प्रदूषण",
        "usual_ok": "आपका सामान्य समय भी लगभग सबसे अच्छा है।", "confidence": "भरोसा",
        "hourly": "घंटे के हिसाब से हवा", "your_plan": "आपकी योजना", "usual": "सामान्य समय",
        "periods": ("सुबह", "दोपहर", "शाम", "रात"), "share": "भेजने के लिए संदेश",
        "share_help": "यह संदेश कॉपी करके WhatsApp या SMS से भेजें।", "details": "और जानकारी",
        "no_time": "आज इस योजना के लिए पर्याप्त समय नहीं बचा। 'कल' चुनें।",
        "no_net": "लाइव हवा की जानकारी नहीं मिली। इंटरनेट जांचकर फिर कोशिश करें।",
        "source": "अनुमान CAMS वैश्विक मॉडल से (Open-Meteo.com)। सिर्फ़ योजना के लिए, चिकित्सा सलाह नहीं।",
        "updated_on": "{t} को अपडेट किया गया।", "dose_note": "इस योजना के अनुसार अनुमानित साँस से अंदर गया प्रदूषण: {d:,.0f} µg।",
        "first_then": "पहले {a}, फिर {b}", "then": "फिर",
        "custom_title": "अपना काम बताएं", "group": "कौन करेगा?", "adult": "वयस्क", "youth": "छात्र (16 से 20)",
        "start_w": "सबसे जल्दी शुरुआत", "end_w": "कब तक खत्म करना है", "usual_start": "सामान्य शुरुआत", "task": "काम",
        "hours": "घंटे", "effort": "मेहनत", "wording": "यह किसके लिए", "work": "काम", "sport": "खेल",
        "add_task": "कम से कम एक काम और उसके घंटे लिखें।", "too_long": "इन कामों में {n} घंटे लगते हैं, पर समय में सिर्फ़ {w} घंटे हैं। समय बढ़ाएं या काम कम करें।",
        "bad_usual": "सामान्य शुरुआत ऐसी हो कि सारे काम समय में खत्म हों।",
        "past_intro": "2024 का कोई भी दिन चुनें। AirShift उस दिन की योजना सिर्फ़ उस शाम तक मिले अनुमान से बनाएगा। फिर देखें असल में क्या हुआ।",
        "city": "शहर", "day": "दिन", "reveal": "असल में क्या हुआ, दिखाएं",
        "reveal_note": "ऊपर की पंक्ति: अनुमान। पतली पंक्ति: उस दिन मापी गई हवा।",
        "no_meas": "इस दिन के कुछ घंटों की माप नहीं है, इसलिए साँस से गया प्रदूषण नहीं निकाला जा सकता। कोई और दिन चुनें।",
        "m_with": "AirShift के साथ साँस से गया", "m_usual": "सामान्य समय पर साँस से गया", "m_best": "पीछे मुड़कर देखें तो सबसे अच्छा संभव",
        "vs_usual": "सामान्य समय की तुलना में", "new_note": "यह एक नया शहर है। प्रशिक्षण के समय मॉडल ने इसे कभी नहीं देखा था।", "new_tag": "(नया शहर)",
        "india_intro": "हवा सबसे साफ़ कब होती है, और दिन भर में कितना बदलती है? आंकड़े: पूरे भारत के प्रदूषण माप केंद्र, 2020 से 2024।",
        "ratio": "{city} में आम दिन पर सबसे गंदे घंटे का प्रदूषण सबसे साफ़ घंटे से {r} गुना होता है।",
        "cleanest_cap": "हर शहर में सुबह 6 से रात 9 बजे के बीच आमतौर पर सबसे साफ़ घंटा।",
        "rhythm": "सभी शहरों का दैनिक पैटर्न", "eigen": "दिन के प्रकार (उन्नत)",
        "eval_intro": "हमने 2024 की असली माप पर {n} शहरों में, और AirShift ने कभी न देखे {m} नए शहरों में जांच की।",
        "m_mae": "अनुमान में औसत गलती", "m_mae_help": "कल के पैटर्न से {x}% बेहतर",
        "m_cover": "अनुमान की सीमा सही है", "m_cover_help": "मुख्य शहरों में",
        "m_new": "नए शहरों में सही", "m_new_help": "नए शहरों में",
        "avoid_q": "लोग कितना प्रदूषण बचा सकते थे?",
        "captured_help": "\"हासिल\" का मतलब: संभव सबसे बड़ी बचत में से AirShift ने असल में कितनी हासिल की।",
        "new_expander": "नए शहर ({n}), वेल्लोर और कोयंबटूर समेत", "conf_expander": "क्या भरोसे का चिह्न कुछ बताता है?",
        "col_who": "कौन", "col_saving": "सामान्य समय से कम प्रदूषण (%)", "col_best": "संभव सबसे अच्छा (%)",
        "col_airshift": "AirShift ने हासिल किया (%)", "col_typical": "आम दिन की योजना ने हासिल किया (%)",
        "about_body": """**AirShift** बाहर काम करने वालों और छात्रों को सिर्फ़ यह नहीं बताता कि हवा कितनी खराब है, बल्कि यह भी बताता है कि *कब* बाहर जाना बेहतर है।

1. सुबह 6 से रात 9 बजे तक हर घंटे के प्रदूषण का अनुमान लगाता है।
2. काम के प्रकार के हिसाब से व्यक्ति कितना प्रदूषण साँस में लेगा, यह निकालता है (U.S. EPA Exposure Factors Handbook, 2011 की साँस दरों से)।
3. शुरू होने के हर संभव समय और कामों के हर क्रम को जांचता है, और सबसे कम प्रदूषण वाली योजना चुनता है।
4. नतीजा अंग्रेज़ी, तमिल, मराठी या हिंदी में भरोसे के स्तर के साथ समझाता है।

**मेरा दिन** भाग CAMS वैश्विक मॉडल के लाइव अनुमान लेता है (Open-Meteo.com)। **बीता हुआ दिन** भाग भारत के {n} शहरों के प्रदूषण आंकड़ों पर प्रशिक्षित {model} मॉडल का इस्तेमाल करता है, ताकि योजना की तुलना असल में हुई बात से की जा सके।

यह योजना बनाने में मदद का साधन है, चिकित्सा सलाह नहीं।""",
    },
}

ROLES = {
    "construction": {"en": "Construction worker", "ta": "கட்டுமானத் தொழிலாளி", "mr": "बांधकाम कामगार", "hi": "निर्माण मज़दूर"},
    "delivery": {"en": "Delivery rider", "ta": "டெலிவரி ஓட்டுநர்", "mr": "डिलिव्हरी रायडर", "hi": "डिलीवरी राइडर"},
    "vendor": {"en": "Street vendor", "ta": "தெரு வியாபாரி", "mr": "फेरीवाला", "hi": "फेरीवाला"},
    "student_sports": {"en": "Student sports", "ta": "மாணவர்: விளையாட்டு", "mr": "विद्यार्थी: खेळ", "hi": "छात्र: खेल"},
    "custom": {"en": "My own plan", "ta": "என் சொந்தத் திட்டம்", "mr": "माझी योजना", "hi": "मेरी योजना"},
}

TASK_NAMES = {
    "Heavy lifting": {"ta": "கனமான பொருட்களைத் தூக்குதல்", "mr": "जड वजन उचलणे", "hi": "भारी सामान उठाना"},
    "Site work": {"ta": "வேலை இடத்து வேலை", "mr": "साइटवरील काम", "hi": "साइट का काम"},
    "Delivery riding": {"ta": "டெலிவரி", "mr": "डिलिव्हरी", "hi": "डिलीवरी"},
    "Vending": {"ta": "வியாபாரம்", "mr": "विक्री", "hi": "बिक्री"},
    "Sports": {"ta": "விளையாட்டு", "mr": "खेळ", "hi": "खेल"},
    "Warm-up and drills": {"ta": "பயிற்சி", "mr": "वॉर्म-अप आणि सराव", "hi": "वार्म-अप और अभ्यास"},
}

EFFORT = {"sedentary": {"en": "Sitting", "ta": "உட்கார்ந்து", "mr": "बसून", "hi": "बैठकर"},
          "light": {"en": "Light", "ta": "லேசான", "mr": "हलके", "hi": "हल्का"},
          "moderate": {"en": "Moderate", "ta": "மிதமான", "mr": "मध्यम", "hi": "मध्यम"},
          "high": {"en": "Heavy", "ta": "கடினமான", "mr": "जड", "hi": "भारी"}}

CATEGORY_NAMES = {
    "en": ["Good", "Satisfactory", "Moderate", "Poor", "Very poor", "Severe"],
    "ta": ["நல்லது", "திருப்திகரம்", "மிதமானது", "மோசம்", "மிகவும் மோசம்", "ஆபத்தானது"],
    "mr": ["चांगली", "समाधानकारक", "मध्यम", "खराब", "अतिशय खराब", "गंभीर"],
    "hi": ["अच्छी", "संतोषजनक", "मध्यम", "खराब", "बहुत खराब", "गंभीर"],
}


def task_name(name, lang):
    return TASK_NAMES.get(name, {}).get(lang, name)
