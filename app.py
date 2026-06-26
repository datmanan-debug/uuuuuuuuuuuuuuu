import streamlit as st
import datetime
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# =========================
# تحميل الموديل
# =========================
MODEL_PATH = "best_efficientnet.keras"
model = load_model(MODEL_PATH)

def preprocess_image(image):
    img = Image.open(image).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_mammogram(image):
    processed = preprocess_image(image)
    prediction = model.predict(processed)[0]

    class_names = ["Normal", "Benign", "Malignant"]
    idx = np.argmax(prediction)

    return class_names[idx], float(np.max(prediction))


# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="Mammogram AI", page_icon="🎀", layout="wide")

# =========================
# Session State
# =========================
if 'lang' not in st.session_state:
    st.session_state.lang = 'Ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'database' not in st.session_state:
    st.session_state.database = []

# =========================
# النصوص
# =========================
text = {
    'Ar': {
        'title': "🎀 نظام فحص الماموجرام الذكي",
        'login': "👩‍⚕️ تسجيل دخول الطبيب",
        'user': "اسم المستخدم",
        'pass': "كلمة المرور",
        'btn_login': "دخول",
        'patient_sec': "📋 بيانات المريض",
        'p_name': "اسم المريض",
        'p_phone': "الهاتف",
        'p_age': "العمر",
        'family_q': "تاريخ عائلي؟",
        'upload_sec': "📷 رفع صورة الماموجرام",
        'result_sec': "🔬 النتيجة",
        'save_record': "💾 حفظ السجل",
        'footer': "✨ صحتك تهمنا ✨",
        'menu_title': "⚙️ القائمة",
        'db_view': "📊 السجل",
        'support': "الدعم الفني",
        'support_desc': "اكتب المشكلة:",
        'send': "إرسال",
        'msg_record_added': "تم الحفظ بنجاح"
    }
}

L = text['Ar']

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {background-color:#FFF5F5;}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.title(L['title'])

# =========================
# Login
# =========================
st.markdown("### تسجيل الدخول")
username = st.text_input(L['user'])
password = st.text_input(L['pass'], type="password")

if st.button(L['btn_login']):
    if username and password:
        st.session_state.logged_in = True
        st.success("تم الدخول")
    else:
        st.warning("املأ البيانات")

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## القائمة")

    if st.session_state.database:
        df = pd.DataFrame(st.session_state.database)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("لا توجد بيانات")

# =========================
# Main App
# =========================
if st.session_state.logged_in:

    st.markdown("## بيانات المريض")

    name = st.text_input("اسم المريض")
    phone = st.text_input("الهاتف")
    age = st.number_input("العمر", 1, 120, 40)

    st.markdown("## رفع صورة")
    uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])

    prediction_label = ""
    confidence = 0

    if uploaded_file:
        st.image(uploaded_file, width=300)

        prediction_label, confidence = predict_mammogram(uploaded_file)

        st.success(f"🔬 النتيجة: {prediction_label}")
        st.info(f"📊 الثقة: {confidence:.2f}")

    st.markdown("## حفظ النتيجة")

    if st.button(L['save_record']):
        if name and uploaded_file:

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            new_record = {
                "Name": name,
                "Phone": phone,
                "Age": age,
                "Diagnosis": prediction_label,
                "Confidence": confidence,
                "Time": now
            }
st.session_state.database.append(new_record)

            st.success(L['msg_record_added'])

            st.rerun()
        else:
            st.error("أدخل البيانات والصورة")

# =========================
# Footer
# =========================
st.markdown(f"<h3 style='text-align:center'>{L['footer']}</h3>", unsafe_allow_html=True)