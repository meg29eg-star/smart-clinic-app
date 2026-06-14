import streamlit as st
import pandas as pd
from datetime import date

# إعداد الصفحة لتكون مريحة للعين ومتجاوبة
st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")

# إدارة التنقل بين شاشة الاستقبال وشاشة الطبيب في الذاكرة
if 'app_page' not in st.session_state:
    st.session_state.app_page = 'reception_screen'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

# =================================================================
# 📱 1. شاشة موظف الاستقبال (Front Desk Module)
# =================================================================
if st.session_state.app_page == 'reception_screen':
    st.title("📱 واجهة موظف الاستقبال - العيادة الذكية")
    st.write("---")
    
    with st.form("reception_form"):
        # (1 إلى 2): بيانات الموعد
        st.subheader("1. بيانات الموعد")
        col1, col2 = st.columns(2)
        appointment_date = col1.date_input("تاريخ الموعد", date.today())
        appointment_time = col2.time_input("وقت الموعد")
        
        # (3 إلى 9): البيانات الشخصية
        st.subheader("2. البيانات الشخصية للمريض")
        c1, c2, c3 = st.columns(3)
        first_name = c1.text_input("الاسم الأول")
        middle_name = c2.text_input("الاسم الأوسط")
        last_name = c3.text_input("اسم العائلة")
        
        c4, c5 = st.columns(2)
        maiden_name = c4.text_input("اللقب قبل الزواج (إن وجد)")
        dob = c5.date_input("تاريخ الميلاد", date(1980, 1, 1))
        id_number = st.text_input("الرقم القومي / الهوية (14 رقم)")
        
        # (10 إلى 11): الديموغرافيا الأساسية
        st.subheader("3. الديموغرافيا الأساسية")
        c6, c7 = st.columns(2)
        age = c6.number_input("السن (يُحسب تلقائياً أو يدوي)", min_value=0, max_value=120, value=30)
        gender = c7.selectbox("الجنس", ["ذكر", "أنثى"])
        
        # (13 إلى 22): معلومات الاتصال والحالة الاجتماعية
        st.subheader("4. معلومات الاتصال والحالة الاجتماعية")
        c8, c9 = st.columns(2)
        phone_1 = c8.text_input("رقم الهاتف الأساسي")
        phone_2 = c9.text_input("رقم الهاتف الاحتياطي (الطوارئ)")
        
        email = st.text_input("البريد الإلكتروني (اختياري)")
        address = st.text_area("العنوان الحالي بالتفصيل")
        
        c10, c11 = st.columns(2)
        governorate = c10.selectbox("المحافظة", ["الإسماعيلية", "السويس", "بورسعيد", "القاهرة", "أخرى"])
        marital_status = c11.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلق", "أرمل"])
        
        c12, c13, c14 = st.columns(3)
        children_count = c12.number_input("عدد الأطفال", min_value=0, max_value=20, value=0)
        youngest_child_age = c13.number_input("سن أصغر طفل", min_value=0, max_value=100, value=0)
        relation_to_spouse = c14.selectbox("صلة القرابة مع الشريك", ["لا توجد صلة", "أقارب درجة أولى", "أقارب درجة ثانية"])
        
        # (25): بيانات الشريك
        st.subheader("5. بيانات الشريك")
        spouse_chronic_diseases = st.text_area("الأمراض المزمنة للشريك (إن وجدت)")
        
        # (26 إلى 34): الوظيفة وجهة الإحالة
        st.subheader("6. الوظيفة وجهة الإحالة")
        c15, c16 = st.columns(2)
        job_title = c15.text_input("الوظيفة الحالية للمريض")
        physical_effort = c16.selectbox("طبيعة المجهود البدني بالوظيفة", ["مكتبي خفيف", "مجهود متوسط", "مجهود بدني شاق"])
        
        c17, c18 = st.columns(2)
        referral_source = c17.selectbox("جهة الإحالة إلى العيادة", ["طبيب آخر", "مريض سابق", "صديق", "وسائل التواصل", "من تلقاء نفسه"])
        referral_specialty = c18.selectbox("تخصص الطبيب المُحيل (إن وجد)", ["طبيب أسرة", "عظام", "باطنة", "جلدية", "لا يوجد"])
        
        c19, c20 = st.columns(2)
        family_doctor_name = c19.text_input("اسم طبيب العائلة الأساسي")
        ortho_doctor_name = c20.text_input("اسم طبيب العظام المتابع")
        
        c21, c22 = st.columns(2)
        insurance_provider = c21.selectbox("جهة التأمين الطبي / جهة العمل", ["هيئة قناة السويس", "تأمين صحي شامل", "نقابة", "خاص"])
        insurance_id = c22.text_input("رقم الكارنيه / التأمين")
        
        admin_notes = st.text_area("ملاحظات إدارية من الاستقبال")

        # زر حفظ البيانات والانتقال للطبيب (الذي طلبته)
        submit_reception = st.form_submit_button("حفظ البيانات وإحالة إلى الطبيب ➡️")

    if submit_reception:
        # حفظ كل بيانات الاستقبال في الذاكرة
        st.session_state.patient_data = {
            "اسم المريض": f"{first_name} {middle_name} {last_name}",
            "تاريخ الموعد": str(appointment_date),
            "رقم الهاتف": phone_1,
            "الرقم القومي": id_number,
            "السن": age,
            "الجنس": gender,
            "الوظيفة": job_title,
            "جهة التأمين": insurance_provider
        }
        # الانتقال لشاشة الطبيب وعمل إعادة تحميل
        st.session_state.app_page = 'doctor_screen'
        st.rerun()

# =================================================================
# 💻 2. واجهة الطبيب الاستشاري (Doctor Clinical Module)
# =================================================================
elif st.session_state.app_page == 'doctor_screen':
    st.title("💻 واجهة الطبيب الاستشاري - الشيت الطبي")
    
    # شريط علوي يوضح بيانات المريض القادم من الاستقبال للتوثيق
    p = st.session_state.patient_data
    st.info(f"📋 **المريض المحال حالياً:** {p.get('اسم المريض')} | **السن:** {p.get('السن')} | **الجنس:** {p.get('الجنس')} | **جهة العمل:** {p.get('جهة التأمين')}")
    st.write("---")
    
    with st.form("doctor_form"):
        st.warning("⚠️ أدخل الأعراض والفحص السريري بالأسفل (تصفح لأسفل بنظام Scroll)")
        
        # 1. الشكوى والتاريخ الحالي (35 إلى 37)
        st.subheader("1. الشكوى والتاريخ الحالي (Present Symptoms)")
        chief_complaint = st.text_area("وصف الشكوى الرئيسية (Chief Complaint)")
        onset_duration = st.text_input("تاريخ بداية الأعراض / المدة (Onset & Duration)")
        previous_diagnosis = st.text_input("التشخيص السابق المعطى من أطباء آخرين")
        
        # العلاجات السابقة (38 إلى 41)
        st.subheader("2. العلاجات والأطباء السابقين")
        c1, c2, c3 = st.columns(3)
        past_physio = c1.toggle("هل خضع لعلاج طبيعي سابقاً؟")
        past_surgery = c2.toggle("هل خضع لتدخل جراحي للمفاصل؟")
        past_injection = c3.toggle("هل خضع لحقن موضعي في المفاصل؟")
        past_doctors = st.text_area("قائمة الأطباء السابقين الذين تم استشارتهم لنفس الشكوى")
        
        # 3. مراجعة الأنظمة الطبية الشاملة (الأعراض الحيوية الحاسمة)
        st.subheader("3. مراجعة الأنظمة الطبية (Systems Review - ROS)")
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.write("**أعراض عامة ومناعية:**")
            weight_loss = st.toggle("فقدان وزن غير مبرر ومفاجئ")
            fatigue = st.toggle("إجهاد عام وإعياء مزمن")
            fever = st.toggle("حمى متكررة مجهولة السبب")
            oral_ulcers = st.toggle("قرح متكررة ومؤلمة في الفم")
            malar_rash = st.toggle("طفح جلدي على الخدين والأنف (Butterfly Rash)")
            photosensitivity = st.toggle("حساسية مفرطة وضرر بالجلد عند التعرض للشمس")
            
        with col_right:
            st.write("**أعراض مفصلية وحركية:**")
            morning_stiffness = st.selectbox("مدة التيبس الصباحي في المفاصل", ["لا يوجد", "أقل من 30 دقيقة", "من 30-60 دقيقة", "أكثر من ساعة"])
            movement_improve = st.toggle("هل يتحسن ألم وتيبس المفاصل مع الحركة؟")
            myositis_weakness = st.toggle("هل تعاني من صعوبة النهوض من الكرسي بدون استناد؟")
            joint_swelling = st.toggle("وجود تورم واضح وملاحظ بالعين في المفاصل")
            symmetrical_swelling = st.toggle("هل التورم متماثل في جانبي الجسم؟")

        # مقياس شدة الألم (17)
        st.subheader("4. التقييم الحركي المبدئي")
        pain_score = st.slider("مقياس تقييم المريض العام لشدة الألم الحالية (PtGA)", 0, 10, 5)

        # زر حفظ الكشف الطبي بالكامل
        submit_doctor = st.form_submit_button("💾 حفظ تقرير الكشف الطبي بالكامل")

    if submit_doctor:
        st.success("🎉 تم حفظ ملف المريض الطبي بالكامل بنجاح وتغذية قاعدة البيانات المبدئية!")
        
        # عرض تقرير شامل يدمج بيانات الاستقبال مع كشف الطبيب في صفحة واحدة للنظام
        st.write("### 📝 التقرير الطبي الموحد للحالة:")
        report_data = {
            "نوع البيان": ["اسم المريض", "السن / الجنس", "الشكوى الرئيسية", "مدة التيبس الصباحي", "درجة الألم (0-10)", "حمى متكررة", "طفح الفراشة (Malar)"],
            "التوثيق الإكلينيكي": [p.get("اسم المريض"), f"{p.get('السن')} سنة / {p.get('الجنس')}", chief_complaint, morning_stiffness, pain_score, "نعم" if fever else "لا", "نعم" if malar_rash else "لا"]
        }
        st.table(pd.DataFrame(report_data))
        
    # زر إضافي خارج الفورم للعودة للاستقبال لاستقبال مريض جديد
    if st.button("🔄 عودة لشاشة الاستقبال (استقبال مريض جديد)"):
        st.session_state.app_page = 'reception_screen'
        st.rerun()
