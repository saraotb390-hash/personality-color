import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== RTL + ستايل =====
st.markdown("""
<style>
html, body, [class*="css"]  { direction: rtl; text-align: right; }
.stRadio > div { direction: rtl; text-align: right; }
div, p, span, label { text-align: right !important; color: black !important; }
.stApp { background: linear-gradient(to right, #fdfbfb, #ebedee); }
div.stButton > button {
background-color: #ff4b4b; color: white !important;
font-size: 18px; border-radius: 10px; padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== ملف البيانات =====
file = "results.csv"
if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["color"])

# ===============================
# 👤 المستخدم
# ===============================


    st.markdown("""
<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>
🎨 اختبار لون الشخصية
</h1>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>اكتشفي شخصيتك من خلال الألوان 🌈</p>", unsafe_allow_html=True)

red = blue = green = yellow = 0

# ===== الأسئلة =====
q1 = st.radio("عندما تواجه موقفاً صعباً ماذا تفعل غالباً؟", [
    "أتصرف بسرعة وأحاول حل المشكلة فوراً",
    "أفكر بهدوء وأحلل الخيارات",
    "أطلب رأي الآخرين وأتعاون معهم",
    "أحاول إيجاد فكرة جديدة أو حل مبتكر"
], key="q1")

if q1 == "أتصرف بسرعة وأحاول حل المشكلة فوراً": red+=1
elif q1 == "أفكر بهدوء وأحلل الخيارات": blue+=1
elif q1 == "أطلب رأي الآخرين وأتعاون معهم": green+=1
else: yellow+=1

q2 = st.radio("أي نوع من الأنشطة تستمتع به أكثر؟", [
    "التحديات والمنافسة",
    "القراءة أو التفكير العميق",
    "قضاء الوقت مع الأصدقاء والعمل الجماعي",
    "تجربة أفكار أو أشياء جديدة"
], key="q2")

if q2 == "التحديات والمنافسة": red+=1
elif q2 == "القراءة أو التفكير العميق": blue+=1
elif q2 == "قضاء الوقت مع الأصدقاء والعمل الجماعي": green+=1
else: yellow+=1

q3 = st.radio("كيف تتخذ قراراتك عادة؟", [
    "بسرعة وثقة",
    "بعد تحليل وتفكير طويل",
    "بعد استشارة الآخرين",
    "بناء على الحدس والأفكار الجديدة"
], key="q3")

if q3 == "بسرعة وثقة": red+=1
elif q3 == "بعد تحليل وتفكير طويل": blue+=1
elif q3 == "بعد استشارة الآخرين": green+=1
else: yellow+=1

q4 = st.radio("كيف يصفك أصدقاؤك؟", [
    "قوي الشخصية ومباشر",
    "هادئ ومفكر",
    "لطيف ومتعاون",
    "مبدع ومليء بالأفكار"
], key="q4")

if q4 == "قوي الشخصية ومباشر": red+=1
elif q4 == "هادئ ومفكر": blue+=1
elif q4 == "لطيف ومتعاون": green+=1
else: yellow+=1

q5 = st.radio("في العمل الجماعي ما الدور الذي تميل إليه؟", [
    "قيادة الفريق وتنظيم العمل",
    "تحليل المشكلة ووضع الخطة",
    "دعم الفريق والحفاظ على الانسجام",
    "اقتراح أفكار جديدة ومبتكرة"
], key="q5")

if q5 == "قيادة الفريق وتنظيم العمل": red+=1
elif q5 == "تحليل المشكلة ووضع الخطة": blue+=1
elif q5 == "دعم الفريق والحفاظ على الانسجام": green+=1
else: yellow+=1

q6 = st.radio("أي شيء يحفزك أكثر؟", [
    "الإنجاز وتحقيق الأهداف",
    "الفهم والتحليل العميق",
    "العلاقات الجيدة مع الآخرين",
    "الابتكار والتجربة"
], key="q6")

if q6 == "الإنجاز وتحقيق الأهداف": red+=1
elif q6 == "الفهم والتحليل العميق": blue+=1
elif q6 == "العلاقات الجيدة مع الآخرين": green+=1
else: yellow+=1

show = st.button("✨ إظهار النتيجة")

if show:
    st.write("دخلت الزر")
    scores = {
        "الأحمر": red,
        "الأزرق": blue,
        "الأخضر": green,
        "الأصفر": yellow
    }

    result = max(scores, key=scores.get)
    st.write(result)
    # ===== Google Sheets =====
try :
    scope = ["https://spreadsheets.google.com/feeds",
     "https://www.googleapis.com/auth/drive"]

    creds_dict = st.secrets["gcp_service_account"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
      creds_dict,
      scope
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1rh_qlc52ytF5vntax0iRL6vkmZzGKt37MC_L2_iaojc/edit?usp=sharing")

    sheet.append_row([result])
except Exception as e:

    st.write("خطأ في Google Sheets:", e)
    # ===== الوصف =====
descriptions = {
        "الأحمر": """🔴 شخصية قيادية، تحب التحدي، سريعة في اتخاذ القرار.

👥 دورك في الفريق: القائد

💪 نقاط القوة:
- القيادة
- الحسم
- الجرأة

⚠️ نقطة تحتاج تطوير:
- التسرع
- الاستماع للآخرين
""",
        "الأزرق": """🔵 شخصية تحليلية تحب الفهم العميق.

👥 دورك في الفريق: المحلل

💪 نقاط القوة:
- التحليل
- التفكير المنطقي

⚠️ نقطة تحتاج تطوير:
- التردد
""",
        "الأخضر": """🟢 شخصية اجتماعية ومتعاونة.

👥 دورك في الفريق: الداعم

💪 نقاط القوة:
- التعاون
- التعاطف

⚠️ نقطة تحتاج تطوير:
- تجنب المواجهة
""",
        "الأصفر": """🟡 شخصية مبدعة ومليئة بالأفكار.

👥 دورك في الفريق: المبدع

💪 نقاط القوة:
- الإبداع
- الحماس

⚠️ نقطة تحتاج تطوير:
- التشتت
"""
    }

color_bg = {
        "الأحمر": "#ffdddd",
        "الأزرق": "#ddeeff",
        "الأخضر": "#ddffdd",
        "الأصفر": "#fff6cc"
    }

color_text = {
        "الأحمر": "red",
        "الأزرق": "blue",
        "الأخضر": "green",
        "الأصفر": "orange"
    }

total = red + blue + green + yellow

percentages = {
        "الأحمر": round((red / total) * 100),
        "الأزرق": round((blue / total) * 100),
        "الأخضر": round((green / total) * 100),
        "الأصفر": round((yellow / total) * 100)
    }

st.markdown(f"""
    <div style="
        background-color: {color_bg.get(result,'#ffffff')};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        color: black;
        box-shadow: 0px 0px 10px #ccc;
    ">
    🎉 لون شخصيتك:
    <span style="color:{color_text.get(result,"black")}; font-weight:bold;">
    {result}
    </span>
    <hr>
    🔴 الأحمر: {percentages["الأحمر"]}% <br>
    🔵 الأزرق: {percentages["الأزرق"]}% <br>
    🟢 الأخضر: {percentages["الأخضر"]}% <br>
    🟡 الأصفر: {percentages["الأصفر"]}%
    </div>
    """, unsafe_allow_html=True)

st.markdown(descriptions[result])

    # ===== حفظ محلي =====
new_data = pd.DataFrame({"color": [result]})
df = pd.concat([df, new_data], ignore_index=True)
df.to_csv(file, index=False)

st.markdown("""
    <p style='text-align:center; color:gray;'>
    ✨ هذا التحليل يعكس ميولك العامة، وقد يختلف حسب المواقف والخبرات.
    </p>
    """, unsafe_allow_html=True)

# ===============================
