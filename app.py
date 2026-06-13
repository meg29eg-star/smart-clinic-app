import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")
st.title("🏥 نموذج استقبال المرضى - العيادة الذكية")

with st.form("patient_form"):
    # 1. بيانات الموعد
    st.subheader("1. بيانات الموعد")
    col1, col2 = st.columns(2)
    appointment_date = col1.date_input("تاريخ الموعد", date.today())
    appointment_time = col2.time_input("وقت الموعد")

    # 2. البيانات الشخصية
    st.subheader("2. البيانات الشخصية")
    c1, c2, c3 = st.columns(3)
    first_name = c1.text_input("الاسم الأول")
    middle_name = c2.text_input("الاسم الأوسط")
    last_name = c3.text_input("اسم العائلة")
    id_number = st.text_input("الرقم القومي")

    # 3. الديموغرافيا
    st.subheader("3. البيانات الديموغرافية")
    c4, c5 = st.columns(2)
    age = c4.number_input("السن", min_value=0, max_value=120)
    gender = c5.selectbox("الجنس", ["ذكر", "أنثى"])

    # 4. التواصل والحالة الاجتماعية
    st.subheader("4. التواصل والحالة الاجتماعية")
    phone = st.text_input("رقم الهاتف الأساسي")
    governorate = st.selectbox("المحافظة", ["الإسماعيلية", "السويس", "بورسعيد", "القاهرة", "أخرى"])
    marital_status = st.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلاق", "أرمل"])

    # 5. بيانات الشريك
    st.subheader("5. بيانات الشريك")
    c6, c7 = st.columns(2)
    spouse_age = c6.number_input("سن الشريك", min_value=0, max_value=100)
    spouse_health = c7.selectbox("الحالة الصحية العامة للشريك", ["سليم", "يعاني من أمراض مزمنة", "متوفى"])

    # 6. الوظيفة وجهة الإحالة
    st.subheader("6. الوظيفة وجهة الإحالة")
    c8, c9 = st.columns(2)
    job = c8.text_input("الوظيفة الحالية")
    referral = c9.selectbox("جهة الإحالة", ["طبيب آخر", "مريض سابق", "صديق", "وسائل التواصل", "من تلقاء نفسه"])
    notes = st.text_area("ملاحظات إدارية من الاستقبال")

    submit_button = st.form_submit_button("حفظ البيانات")

if submit_button:
    st.success("تم الحفظ بنجاح!")
    # تجميع كل الحقول في جدول واحد
    data = {
        "الحقل": ["التاريخ", "الاسم الكامل", "الرقم القومي", "السن", "الجنس", "الهاتف", "المحافظة", "سن الشريك", "الوظيفة"],
        "القيمة": [str(appointment_date), f"{first_name} {middle_name} {last_name}", id_number, age, gender, phone, governorate, spouse_age, job]
    }
    st.table(pd.DataFrame(data))
