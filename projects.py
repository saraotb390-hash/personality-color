import streamlit as st
import pandas as pd
import os


import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== تحديد الوضع =====
mode = st.query_params.get("mode", "user")

# ===== ملف البيانات =====
file = "results.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["color"])

# ================================
# 👤 وضع المستخدم (الأسئلة)
# ================================
if mode == "user":

    st.markdown("<h1 style='text-align:center;'>🎨 اختبار لون الشخصية</h1>", unsafe_allow_html=True)

    red = blue = green = yellow = 0

    # ===== الأسئلة =====
    # ===== الأسئلة =====
q1 = st.radio("عندما تواجه موقفاً صعباً ماذا تفعل غالباً؟", [
    "أتصرف بسرعة وأحاول حل المشكلة فوراً",
    "أفكر بهدوء وأحلل الخيارات",
    "أطلب رأي الآخرين وأتعاون معهم",
    "أحاول إيجاد فكرة جديدة أو حل مبتكر"
], key=f"{mode}_q1")

if q1 == "أتصرف بسرعة وأحاول حل المشكلة فوراً":
    red += 1
elif q1 == "أفكر بهدوء وأحلل الخيارات":
    blue += 1
elif q1 == "أطلب رأي الآخرين وأتعاون معهم":
    green += 1
else:
    yellow += 1


q2 = st.radio("أي نوع من الأنشطة تستمتع به أكثر؟", [
    "التحديات والمنافسة",
    "القراءة أو التفكير العميق",
    "قضاء الوقت مع الأصدقاء والعمل الجماعي",
    "تجربة أفكار أو أشياء جديدة"
], key=f"{mode}_q2")

if q2 == "التحديات والمنافسة":
    red += 1
elif q2 == "القراءة أو التفكير العميق":
    blue += 1
elif q2 == "قضاء الوقت مع الأصدقاء والعمل الجماعي":
    green += 1
else:
    yellow += 1


q3 = st.radio("كيف تتخذ قراراتك عادة؟", [
    "بسرعة وثقة",
    "بعد تحليل وتفكير طويل",
    "بعد استشارة الآخرين",
    "بناء على الحدس والأفكار الجديدة"
], key=f"{mode}_q3")

if q3 == "بسرعة وثقة":
    red += 1
elif q3 == "بعد تحليل وتفكير طويل":
    blue += 1
elif q3 == "بعد استشارة الآخرين":
    green += 1
else:
    yellow += 1


q4 = st.radio("كيف يصفك أصدقاؤك؟", [
    "قوي الشخصية ومباشر",
    "هادئ ومفكر",
    "لطيف ومتعاون",
    "مبدع ومليء بالأفكار"
], key=f"{mode}_q4")

if q4 == "قوي الشخصية ومباشر":
    red += 1
elif q4 == "هادئ ومفكر":
    blue += 1
elif q4 == "لطيف ومتعاون":
    green += 1
else:
    yellow += 1


q5 = st.radio("في العمل الجماعي ما الدور الذي تميل إليه؟", [
    "قيادة الفريق وتنظيم العمل",
    "تحليل المشكلة ووضع الخطة",
    "دعم الفريق والحفاظ على الانسجام",
    "اقتراح أفكار جديدة ومبتكرة"
], key=f"{mode}_q5")

if q5 == "قيادة الفريق وتنظيم العمل":
    red += 1
elif q5 == "تحليل المشكلة ووضع الخطة":
    blue += 1
elif q5 == "دعم الفريق والحفاظ على الانسجام":
    green += 1
else:
    yellow += 1


q6 = st.radio("أي شيء يحفزك أكثر؟", [
    "الإنجاز وتحقيق الأهداف",
    "الفهم والتحليل العميق",
    "العلاقات الجيدة مع الآخرين",
    "الابتكار والتجربة"
], key=f"{mode}_q6")

if q6 == "الإنجاز وتحقيق الأهداف":
    red += 1
elif q6 == "الفهم والتحليل العميق":
    blue += 1
elif q6 == "العلاقات الجيدة مع الآخرين":
    green += 1
else:
    yellow += 1
    # ===== زر =====
    show = st.button("✨ إظهار النتيجة")

    if show:

        scores = {
            "الأحمر": red,
            "الأزرق": blue,
            "الأخضر": green,
            "الأصفر": yellow
        }

        result = max(scores, key=scores.get)

        # Google Sheets
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/18jwfUdACBIASrZTv7TJ4DNkPxob3MUulvHxKqdr1srY/edit?usp=sharing")
        sheet.append_row([result])

        # حفظ محلي
        new_data = pd.DataFrame({"color": [result]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file, index=False)

        st.success(f"🎉 نتيجتك: {result}")

# ================================
# 📊 وضع العرض (البروجكتر)
# ================================
elif mode == "admin":

    st.title("📊 توزيع الألوان")

    if os.path.exists(file):
        df = pd.read_csv(file)

    if not df.empty:

        chart = df["color"].value_counts()

        colors_map = {
            "الأحمر": "red",
            "الأزرق": "blue",
            "الأخضر": "green",
            "الأصفر": "yellow"
        }

        colors = [colors_map.get(c, "gray") for c in chart.index]
        labels = [get_display(arabic_reshaper.reshape(label)) for label in chart.index]

        fig, ax = plt.subplots()
        ax.bar(labels, chart.values, color=colors)

        st.pyplot(fig)

    else:
        st.write("لا توجد بيانات بعد")
st.markdown("""
<style>

/* يخلي كل الصفحة عربي */
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}

/* الراديو (الخيارات) */
.stRadio > div {
    direction: rtl;
    text-align: right;
}

/* كل النصوص */
div, p, span, label {
    text-align: right !important;
}

</style>
""", unsafe_allow_html=True)

# ===== تنسيق + ألوان =====
st.markdown("""
<style>

/* النص */
div, p, span, label {
    color: black !important;
}

/* الخلفية */
.stApp {
    background: linear-gradient(to right, #fdfbfb, #ebedee);
}

/* زر */
div.stButton > button {
    background-color: #ff4b4b;
    color: white !important;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 20px;
}

</style>
""", unsafe_allow_html=True)

# ===== عنوان =====
st.markdown("""
<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>
🎨 اختبار لون الشخصية
</h1>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>اكتشفي شخصيتك من خلال الألوان 🌈</p>", unsafe_allow_html=True)

# ===== ملف البيانات =====
file = "results.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["color"])

# ===== العدادات =====
red = blue = green = yellow = 0

# ===== الأسئلة =====
q1 = st.radio("عندما تواجه موقفاً صعباً ماذا تفعل غالباً؟", [
    "أتصرف بسرعة وأحاول حل المشكلة فوراً",
    "أفكر بهدوء وأحلل الخيارات",
    "أطلب رأي الآخرين وأتعاون معهم",
    "أحاول إيجاد فكرة جديدة أو حل مبتكر"
])

if q1 == "أتصرف بسرعة وأحاول حل المشكلة فوراً":
    red += 1
elif q1 == "أفكر بهدوء وأحلل الخيارات":
    blue += 1
elif q1 == "أطلب رأي الآخرين وأتعاون معهم":
    green += 1
else:
    yellow += 1

q2 = st.radio("أي نوع من الأنشطة تستمتع به أكثر؟", [
    "التحديات والمنافسة",
    "القراءة أو التفكير العميق",
    "قضاء الوقت مع الأصدقاء والعمل الجماعي",
    "تجربة أفكار أو أشياء جديدة"
])

if q2 == "التحديات والمنافسة":
    red += 1
elif q2 == "القراءة أو التفكير العميق":
    blue += 1
elif q2 == "قضاء الوقت مع الأصدقاء والعمل الجماعي":
    green += 1
else:
    yellow += 1

q3 = st.radio("كيف تتخذ قراراتك عادة؟", [
    "بسرعة وثقة",
    "بعد تحليل وتفكير طويل",
    "بعد استشارة الآخرين",
    "بناء على الحدس والأفكار الجديدة"
])

if q3 == "بسرعة وثقة":
    red += 1
elif q3 == "بعد تحليل وتفكير طويل":
    blue += 1
elif q3 == "بعد استشارة الآخرين":
    green += 1
else:
    yellow += 1

q4 = st.radio("كيف يصفك أصدقاؤك؟", [
    "قوي الشخصية ومباشر",
    "هادئ ومفكر",
    "لطيف ومتعاون",
    "مبدع ومليء بالأفكار"
])

if q4 == "قوي الشخصية ومباشر":
    red += 1
elif q4 == "هادئ ومفكر":
    blue += 1
elif q4 == "لطيف ومتعاون":
    green += 1
else:
    yellow += 1

q5 = st.radio("في العمل الجماعي ما الدور الذي تميل إليه؟", [
    "قيادة الفريق وتنظيم العمل",
    "تحليل المشكلة ووضع الخطة",
    "دعم الفريق والحفاظ على الانسجام",
    "اقتراح أفكار جديدة ومبتكرة"
])

if q5 == "قيادة الفريق وتنظيم العمل":
    red += 1
elif q5 == "تحليل المشكلة ووضع الخطة":
    blue += 1
elif q5 == "دعم الفريق والحفاظ على الانسجام":
    green += 1
else:
    yellow += 1

q6 = st.radio("أي شيء يحفزك أكثر؟", [
    "الإنجاز وتحقيق الأهداف",
    "الفهم والتحليل العميق",
    "العلاقات الجيدة مع الآخرين",
    "الابتكار والتجربة"
])

if q6 == "الإنجاز وتحقيق الأهداف":
    red += 1
elif q6 == "الفهم والتحليل العميق":
    blue += 1
elif q6 == "العلاقات الجيدة مع الآخرين":
    green += 1
else:
    yellow += 1

# ===== زر =====
show = st.button("✨ إظهار النتيجة")

if show:

    # حساب السكور
    scores = {
        "الأحمر": red,
        "الأزرق": blue,
        "الأخضر": green,
        "الأصفر": yellow
    }

    # Google Sheets setup
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # وصف الشخصيات
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

    # النتيجة
    result = max(scores, key=scores.get)

    # إرسال إلى الشيت
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/18jwfUdACBIASrZTv7TJ4DNkPxob3MUulvHxKqdr1srY/edit?usp=sharing")
    sheet.append_row([result])

    # عرض نصي بسيط
    st.write(f"✨ نتيجتك: {result}")

    # حساب النسب
    total = red + blue + green + yellow

    percentages = {
        "الأحمر": round((red / total) * 100),
        "الأزرق": round((blue / total) * 100),
        "الأخضر": round((green / total) * 100),
        "الأصفر": round((yellow / total) * 100)
    }

    # الألوان
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

    # 🎉 بوكس النتيجة
    st.markdown(f"""
    <div style='
        background-color: {color_bg.get(result)};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        color: black;
        box-shadow: 0px 0px 10px #ccc;
    '>

    🎉 لون شخصيتك هو:
    <span style="color:{color_text.get(result)}; font-weight:bold;">
    {result}
    </span>

    <hr>

    🔴 الأحمر: {percentages["الأحمر"]}% <br>
    🔵 الأزرق: {percentages["الأزرق"]}% <br>
    🟢 الأخضر: {percentages["الأخضر"]}% <br>
    🟡 الأصفر: {percentages["الأصفر"]}%

    </div>
    """, unsafe_allow_html=True)

    # 🔥 الوصف
    st.markdown(f"""
    <div style='
        margin-top: 15px;
        font-size: 18px;
        line-height: 1.8;
    '>
    {descriptions[result]}
    </div>
    """, unsafe_allow_html=True)
    new_data = pd.DataFrame({"color": [result]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file, index=False)
    # ✨ جملة احترافية
st.markdown("""
    <p style='text-align:center; color:gray;'>
    ✨ هذا التحليل يعكس ميولك العامة، وقد يختلف حسب المواقف والخبرات.
    </p>
    """, unsafe_allow_html=True)

 
# ===== الرسم =====
st.subheader("📊 توزيع الألوان")

if os.path.exists(file):
    df = pd.read_csv(file)

if not df.empty:
    chart = df["color"].value_counts()

    colors_map = {
        "الأحمر": "red",
        "الأزرق": "blue",
        "الأخضر": "green",
        "الأصفر": "yellow"
    }

    colors = [colors_map.get(color, "gray") for color in chart.index]
    labels = [get_display(arabic_reshaper.reshape(label)) for label in chart.index]

    fig, ax = plt.subplots()
    ax.bar(labels, chart.values, color=colors)

    st.pyplot(fig)

else:
    st.write("لا توجد بيانات بعد")
