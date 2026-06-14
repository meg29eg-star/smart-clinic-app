import streamlit as st
from datetime import date

st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")

# إعداد الذاكرة لنقل البيانات بين الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'reception'

# 1. صفحة الاستقبال
if st.session_state.page == 'reception':
    st.title("🏥 شاشة الاستقبال")
    with st.form("reception_form"):
        st.subheader("البيانات الأساسية")
        col1, col2 = st.columns(2)
        patient_name = col1.text_input("اسم المريض")
        appointment_date = col2.date_input("التاريخ")
        
        # عند الضغط هنا، نغير الحالة وننتقل
        if st.form_submit_button("إحالة إلى الطبيب"):
            st.session_state.patient_name = patient_name
            st.session_state.page = 'doctor'
            st.rerun()

# 2. صفحة الطبيب (تظهر بعد الإحالة)
elif st.session_state.page == 'doctor':
    st.title("👨‍⚕️ شاشة الطبيب - الملف الطبي")
    st.info(f"المريض الحالي: {st.session_state.patient_name}")
    
    with st.form("doctor_clinical_form"):
        # هنا سنضع كل الأسئلة سكيرول تحت بعضها
        st.subheader("7. الشكوى")
        st.text_area("وصف الشكوى")
        
        st.subheader("8-16. الفحص السريري")
        st.toggle("وجود حمى")
        st.toggle("إجهاد عام")
        st.selectbox("مدة التيبس الصباحي", ["لا يوجد", "أقل من 30 دقيقة", "أكثر من ساعة"])
        
        st.subheader("17. التقييم الحركي")
        st.slider("مقياس شدة الألم", 0, 10, 5)
        
        if st.form_submit_button("حفظ الملف الطبي بالكامل"):
            st.success("تم حفظ الملف الطبي بنجاح!")
            if st.button("عودة للاستقبال"):
                st.session_state.page = 'reception'
                st.rerun()
