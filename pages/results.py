import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display

st.title("📊 توزيع الألوان")

file = "results.csv"

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
else:
    st.write("لا يوجد ملف بيانات")
