import streamlit as st
import datetime
import pandas as pd
import requests

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Mammogram AI", page_icon="🎀", layout="wide")

# ضع التوكن (Token) الخاص بالبوت مالتك اللي أخذته من BotFather هنا لتفعيل التليجرام:
TOKEN = "YOUR_BOT_TOKEN_HERE"

# دالة إرسال الرسالة إلى التليجرام
def send_telegram_notification(chat_id, message_text):
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        pass

# 2. إدارة الحالة (State Management)
if 'lang' not in st.session_state:
    st.session_state.lang = 'Ar'  # الافتراضي عربي
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'database' not in st.session_state:
    # الجدول يبدأ فارغاً تماماً وبدون أي بيانات وهمية
    st.session_state.database = []

# النصوص المترجمة للغتين (تم إزالة الملصقات وتحديث الحقول للجدول الجديد)
text = {
    'Ar': {
        'title': "نظام فحص الماموجرام الذكي",
        'login': "تسجيل دخول الطبيب",
        'user': "اسم المستخدم",
        'pass': "كلمة المرور",
        'btn_login': "حفظ الحساب ودخول",
        'patient_sec': "بيانات المريض",
        'p_name': "اسم المريض الكامل",
        'p_phone': "رقم الهاتف",
        'p_age': "العمر",
        'family_q': "التاريخ المرضي (هل يوجد تاريخ إصابة بسرطان الثدي في العائلة؟)",
        'p_radiation_date': "موعد الإشعاع",
        'p_total_radiation': "عدد جلسات الإشعاع الكلية التي يأخذها",
        'p_current_radiation': "عدد الجلسات التي وصل إليها حالياً",
        'upload_sec': "رفع صورة أو ملف الماموجرام",
        'upload_placeholder': "اختر صورة الماموجرام أو اسحبها هنا...",
        'result_sec': "نتيجة التحليل الذكي",
        'normal': "طبيعي (Normal)",
        'benign': "غير طبيعي - حميد (Benign)",
        'malignant': "غير طبيعي - خبيث (Malignant)",
        'save_record': "حفظ السجل الحالي في البيانات",
        'footer': "صحتكِ تهمنا",
        'menu_title': "القائمة الذكية",
        'db_view': "سجل البيانات الكامل (Excel Style)",
        'support': "تواصل مع الدعم الفني",
        'support_desc': "إذا واجهت أي خلل تقني، يرجى كتابته هنا:",
        'send': "إرسال بلاغ",
        'msg_saved': "تم الدخول بنجاح! تم فتح القوائم أدناه.",
        'msg_record_added': "تم إضافة المريض بنجاح إلى جدول البيانات وإرسال الإشعار!"
    },
    'En': {
        'title': "Smart Mammogram System",
        'login': "Doctor Login",
        'user': "Username / Email",
        'pass': "Password",
        'btn_login': "Save Account & Login",
        'patient_sec': "Patient Information",
        'p_name': "Patient Full Name",
        'p_phone': "Phone Number",
        'p_age': "Age",
        'family_q': "Family History (Is there a family history of breast cancer?)",
        'p_radiation_date': "Radiation Appointment Date",
        'p_total_radiation': "Total Radiation Sessions Required",
        'p_current_radiation': "Current Radiation Session Reached",
        'upload_sec': "Upload Mammogram",
        'upload_placeholder': "Choose a mammogram image or drag it here...",
        'result_sec': "AI Analysis Result",
        'normal': "NormalLog",
        'benign': "Abnormal - Benign",
        'malignant': "Abnormal - Malignant",
        'save_record': "Save Record to Database",
        'footer': "Your Health Matters",
        'menu_title': "Smart Menu",
        'db_view': "Complete Records Log (Excel Style)",
        'support': "Contact Technical Support",
        'support_desc': "If you encounter any technical glitch, please write it here:",
        'send': "Send Report",
        'msg_saved': "Login Successful! Features unlocked below.",
        'msg_record_added': "Patient successfully added to log!"
    }
}

L = text[st.session_state.lang]

# 3. تصميم الـ CSS المخصص بالألوان المطلوبة (الواجهة رصاصي والكتابة أزرق)
bg_color = "#E5E7EB"        # رصاصي فاتح للخلفية الأساسية
text_color = "#1E3A8A"      # أزرق غامق للنصوص والكتابة الأساسية
card_bg = "#F3F4F6"         # رصاصي مغاير قليلاً للحقول والخلفيات الداخلية
border_color = "#9CA3AF"     # رصاصي للحدود
btn_color = "#2563EB"        # أزرق للأزرار الرئيسية

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    h1, h2, h3, h4, p, label, span {{ color: {text_color} !important; font-family: 'Arial', sans-serif; font-weight: bold; }}
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stDateInput input {{
        border: 2px solid {border_color} !important; border-radius: 8px !important;
        background-color: {card_bg} !important; color: {text_color} !important;
        font-weight: bold;
    }}
    .stButton button {{
        background-color: {btn_color} !important; color: white !important;
        border-radius: 8px !important; border: none !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: #1D4ED8 !important; }}
    .footer {{
        text-align: center; font-size: 24px; font-weight: bold; color: {text_color};
        margin-top: 50px; padding: 20px; border-top: 2px dashed {border_color};
    }}
    </style>
""", unsafe_allow_html=True)

# 4. الشريط العلوي (تبديل اللغة)
top_col1, top_col2 = st.columns([7, 1])
with top_col1:
    st.markdown(f"<h1 style='color: #1E3A8A;'>{L['title']}</h1>", unsafe_allow_html=True)
with top_col2:
    if st.button("🌐 En/عربي"):
        st.session_state.lang = 'En' if st.session_state.lang == 'Ar' else 'Ar'
        st.rerun()

st.markdown(f"<hr style='border: 1px solid {border_color};'>", unsafe_allow_html=True)

# 5. القائمة الجانبية (واجهة تفاعلية مثل الاكسل)
with st.sidebar:
    st.markdown(f"## {L['menu_title']}")
    
    with st.expander(L['db_view'], expanded=True):
        if st.session_state.database:
            df = pd.DataFrame(st.session_state.database)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("السجل فارغ حالياً. البيانات ستظهر هنا بتنسيق جدول إكسل فور حفظها.")
            
    with st.expander(L['support'], expanded=False):
        st.write(L['support_desc'])
        st.text_area("", placeholder="...", key="support_box")
        if st.button(L['send']):
            st.success("تم إرسال بلاغك بنجاح.")

# القسم الرئيسي: تسجيل دخول الطبيب
st.markdown(f"### {L['login']}")
col1, col2 = st.columns(2)
with col1: password = st.text_input(L['pass'], type="password")
with col2: username = st.text_input(L['user'])

if st.button(L['btn_login']):
    if username and password:
        st.session_state.logged_in = True
        st.success(L['msg_saved'])
    else:
        st.warning("الرجاء إدخال بيانات الدخول.")

# ظهور باقي الخصائص بعد تسجيل الدخول
if st.session_state.logged_in:
    st.markdown("<br><hr>", unsafe_allow_html=True)

    # قسم بيانات المريض المطور
    st.markdown(f"### {L['patient_sec']}")
    p_name = st.text_input(L['p_name'])
    
    col3, col4, col5 = st.columns(3)
    with col3: p_phone = st.text_input(L['p_phone'])
    with col4: p_age = st.number_input(L['p_age'], min_value=1, max_value=120, value=40)
    with col5: radiation_date = st.date_input(L['p_radiation_date'], datetime.date.today())
    
    col6, col7 = st.columns(2)
    with col6: total_radiation = st.number_input(L['p_total_radiation'], min_value=0, max_value=100, value=0)
    with col7: current_radiation = st.number_input(L['p_current_radiation'], min_value=0, max_value=100, value=0)
    
    family_history = st.radio(L['family_q'], ("لا" if st.session_state.lang=='Ar' else "No", "نعم" if st.session_state.lang=='Ar' else "Yes"))

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # قسم رفع الملف
    st.markdown(f"### {L['upload_sec']}")
    uploaded_file = st.file_uploader(L['upload_placeholder'], type=["jpg", "jpeg", "png", "pdf"])
    if uploaded_file:
        st.image(uploaded_file, caption="Mammogram file loaded", width=300)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    # قسم النتيجة (مع لمسة وردي مخصصة للنتائج)
    st.markdown(f"### {L['result_sec']}")
    result_type = st.selectbox("", [L['normal'], L['benign'], L['malignant']])

    current_result = ""
    if result_type == L['normal']:
        current_result = "Normal (طبيعي)"
        st.markdown("""
            <div style="background-color: #FCE7F3; padding: 20px; border-radius: 10px; border-left: 8px solid #F472B6;">
                <h3 style="color: #9D174D !important; margin: 0;">النتيجة: طبيعي (Normal)</h3>
            </div>
        """, unsafe_allow_html=True)
    elif result_type == L['benign']:
        current_result = "Benign (حميد)"
        st.markdown("""
            <div style="background-color: #FBCFE8; padding: 20px; border-radius: 10px; border-left: 8px solid #EC4899;">
                <h3 style="color: #831843 !important; margin: 0;">النتيجة: غير طبيعي - حميد (Benign)</h3>
            </div>
        """, unsafe_allow_html=True)
    elif result_type == L['malignant']:
        current_result = "Malignant (خبيث)"
        st.markdown("""
            <div style="background-color: #F472B6; padding: 20px; border-radius: 10px; border-left: 8px solid #9D174D;">
                <h3 style="color: #4C0519 !important; margin: 0;">النتيجة: غير طبيعي - خبيث (Malignant)</h3>
            </div>
        """, unsafe_allow_html=True)

    # زر حفظ السجل الحالي للجدول
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(L['save_record']):
        if p_name:
            now_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            new_record = {
                "الوقت والتاريخ / Timestamp": now_timestamp,
                "اسم المريض / Name": p_name,
                "العمر / Age": p_age,
                "التليفون / Phone": p_phone,
                "التاريخ المرضي / History": family_history,
                "موعد الاشعاع / Appointment": str(radiation_date),
                "كم اشعاع ياخذ / Total": total_radiation,
                "ليا اشعاع وصل / Progress": current_radiation,
                "التشخيص / Diagnosis": current_result
            }
            st.session_state.database.append(new_record)
            
            # إرسال إشعار تلقائي للبوت
            notification_text = (
                f"📢 تسجيل مريض جديد\n\n"
                f"👤 المريض: {p_name}\n"
                f"📞 الهاتف: {p_phone}\n"
                f"📅 موعد الإشعاع: {radiation_date}\n"
                f"🔢 الجلسات: {current_radiation} من أصل {total_radiation}\n"
                f"🩺 التشخيص: {current_result}"
            )
            send_telegram_notification("@atmanan_37", notification_text)
            
            st.success(L['msg_record_added'])
            st.rerun()
        else:
            st.error("الرجاء إدخال اسم المريض أولاً.")

# 6. التذييل الثابت
st.markdown(f"<div class='footer'>{L['footer']}</div>", unsafe_allow_html=True)
