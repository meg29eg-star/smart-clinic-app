import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")
st.title("🏥 نموذج استقبال المرضى - العيادة الذكية")

with st.form("patient_form"):
    # 1 إلى 4 (تمت سابقاً)
    st.subheader("1-4. بيانات الموعد والشخصية والديموغرافيا والتواصل")
    c1, c2 = st.columns(2)
    appointment_date = c1.date_input("تاريخ الموعد", date.today())
    phone = c2.text_input("رقم الهاتف الأساسي")

    # 5. بيانات الشريك (المضافة حديثاً)
    st.subheader("5. بيانات الشريك")
    c3, c4 = st.columns(2)
    spouse_age = c3.number_input("سن الشريك", min_value=0, max_value=100)
    spouse_health = c4.selectbox("الحالة الصحية العامة للشريك", ["سليم", "يعاني من أمراض مزمنة", "متوفى"])

    # 6. الوظيفة وجهة الإحالة (المضافة حديثاً)
    st.subheader("6. الوظيفة وجهة الإحالة")
    c5, c6 = st.columns(2)
    job = c5.text_input("الوظيفة الحالية")
    referral = c6.selectbox("جهة الإحالة", ["طبيب آخر", "مريض سابق", "صديق", "وسائل التواصل", "من تلقاء نفسه"])
    notes = st.text_area("ملاحظات إدارية من الاستقبال")

    submit_button = st.form_submit_button("حفظ البيانات")

if submit_button:
    # عرض النتيجة
    st.success("تم الحفظ بنجاح!")
    data = {
        "الحقل": ["التاريخ", "الهاتف", "سن الشريك", "الحالة الصحية للشريك", "الوظيفة", "جهة الإحالة"],
        "القيمة": [str(appointment_date), phone, spouse_age, spouse_health, job, referral]
    }
    st.table(pd.DataFrame(data))
