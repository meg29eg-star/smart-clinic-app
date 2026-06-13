import streamlit as st
import pandas as pd
from datetime import date

# إعداد الصفحة
st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="centered")

st.title("🏥 نموذج استقبال المرضى - العيادة الذكية")

# نموذج إدخال البيانات
with st.form("patient_form"):
    st.subheader("بيانات الموعد")
    appointment_date = st.date_input("تاريخ الموعد", date.today())
    appointment_time = st.time_input("وقت الموعد")

    st.subheader("البيانات الشخصية")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("الاسم الأول")
        middle_name = st.text_input("الاسم الأوسط")
    with col2:
        last_name = st.text_input("اسم العائلة")
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    
    id_number = st.text_input("الرقم القومي")

    # زر الحفظ
    submit_button = st.form_submit_button("حفظ البيانات")

# معالجة الضغط على الزر
if submit_button:
    # تجميع البيانات
    data = {
        "تاريخ الموعد": [str(appointment_date)],
        "وقت الموعد": [str(appointment_time)],
        "الاسم الأول": [first_name],
        "الاسم الأوسط": [middle_name],
        "اسم العائلة": [last_name],
        "الجنس": [gender],
        "الرقم القومي": [id_number]
    }
    df = pd.DataFrame(data)

    # عرض التأكيد والبيانات
    st.success("تم الحفظ بنجاح!")
    st.write("### البيانات المدخلة:")
    st.table(df.T) # عرض البيانات بشكل جدول مقلوب لسهولة القراءة
