import streamlit as st
import pandas as pd
from datetime import date
import time

# =================================================================
# ⚙️ إعداد الصفحة والمحرك الذكي
# =================================================================
st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")

if 'app_page' not in st.session_state:
    st.session_state.app_page = 'reception_screen'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

# دالة محاكاة محرك الذكاء الاصطناعي (AI CDSS Engine)
def simulate_ai_cdss(p_data, history, symptoms):
    # النسب المبدئية
    sle_prob, ra_prob, as_prob = 5, 5, 5
    workup = []

    # 1. الفلترة الديموغرافية (السن والجنس)
    age = p_data.get('السن', 30)
    gender = p_data.get('الجنس', "أنثى")
    if gender == "أنثى" and age <= 45:
        sle_prob += 20
        ra_prob += 10
    elif gender == "ذكر" and age <= 40:
        as_prob += 20

    # 2. وزن الجينات (التاريخ العائلي)
    if history.get('lupus'): sle_prob += 20
    if history.get('ra'): ra_prob += 20
    if history.get('as_fam'): as_prob += 20

    # 3. مطابقة الأعراض والأنظمة
    if symptoms.get('malar_rash'): sle_prob += 35
    if symptoms.get('oral_ulcers'): sle_prob += 10
    if symptoms.get('foam_urine'): 
        sle_prob += 15
        workup.append("تحليل بول كامل (Urinalysis) و بروتين في بول 24 ساعة")
    if symptoms.get('abortions'): 
        sle_prob += 10
        workup.append("فحص متلازمة الفوسفوليبيد (Antiphospholipid Antibodies)")
    
    if symptoms.get('morning_stiffness') == "أكثر من ساعة": ra_prob += 25
    if symptoms.get('symmetrical'): ra_prob += 20
    
    if symptoms.get('movement_improve'): as_prob += 25
    if symptoms.get('pleuritic_pain'): sle_prob += 10

    # ضبط الحدود القصوى
    sle_prob = min(sle_prob, 96)
    ra_prob = min(ra_prob, 94)
    as_prob = min(as_prob, 92)

    # تحديد التوصيات الأساسية بناءً على أعلى احتمال
    if sle_prob > 50 and "ANA (Antinuclear Antibodies)" not in workup:
        workup.append("فحص الأجسام المضادة للنواة (ANA) و Anti-dsDNA")
    if ra_prob > 50:
        workup.append("عامل الروماتويد (RF) و Anti-CCP")
    if as_prob > 50:
        workup.append("رنين مغناطيسي على المفاصل الحرقفية (MRI SIJ) و HLA-B27")

    return {
        "SLE": sle_prob,
        "RA": ra_prob,
        "AS": as_prob,
        "workup": list(set(workup)) # إزالة التكرار
    }

# =================================================================
# 📱 1. شاشة موظف الاستقبال
# =================================================================
if st.session_state.app_page == 'reception_screen':
    st.title("🏥 العيادة الروماتيزمية الذكية (Smart Rheum Clinic)")
    st.caption("إشراف: د. محمد مجاهد - استشاري الروماتيزم والتأهيل")
    st.write("---")
    
    with st.form("reception_form"):
        st.subheader("1. البيانات الشخصية والديموغرافية للمريض")
        c1, c2, c3 = st.columns(3)
        first_name = c1.text_input("الاسم الأول")
        last_name = c2.text_input("اسم العائلة")
        id_number = c3.text_input("الرقم القومي (14 رقم)")
        
        c4, c5 = st.columns(2)
        age = c4.number_input("السن", min_value=1, max_value=120, value=30)
        gender = c5.selectbox("الجنس", ["ذكر", "أنثى"])
        
        st.subheader("2. معلومات الاتصال والإدارة")
        c6, c7 = st.columns(2)
        phone_1 = c6.text_input("رقم الهاتف الأساسي")
        insurance_provider = c7.selectbox("جهة التأمين", ["تأمين صحي شامل", "هيئة قناة السويس", "نقابة", "خاص", "بدون"])

        submit_reception = st.form_submit_button("حفظ البيانات وإحالة إلى الطبيب ➡️")

    if submit_reception:
        if not first_name:
            st.warning("برجاء إدخال اسم المريض أولاً.")
        else:
            st.session_state.patient_data = {
                "اسم المريض": f"{first_name} {last_name}",
                "السن": age,
                "الجنس": gender,
                "الهاتف": phone_1,
                "جهة التأمين": insurance_provider
            }
            st.session_state.app_page = 'doctor_screen'
            st.rerun()

# =================================================================
# 💻 2. واجهة الطبيب ومحرك اتخاذ القرار
# =================================================================
elif st.session_state.app_page == 'doctor_screen':
    st.title("💻 الشيت الطبي ومحرك الذكاء الاصطناعي (AI CDSS)")
    
    p = st.session_state.patient_data
    st.info(f"👤 **المريض المحال:** {p.get('اسم المريض')} | **السن:** {p.get('السن')} | **الجنس:** {p.get('الجنس')} | **جهة العمل:** {p.get('جهة التأمين')}")
    
    with st.form("doctor_form"):
        st.subheader("1. الشكوى والفحص المبدئي")
        chief_complaint = st.text_area("وصف الشكوى الرئيسية")
        
        st.write("---")
        st.subheader("🧬 2. التاريخ العائلي والأعراض (للتغذية الذكية)")
        col_hist, col_symp = st.columns(2)
        
        with col_hist:
            st.markdown("**التاريخ العائلي (Genetics):**")
            f_lupus = st.checkbox("تاريخ عائلي للذئبة الحمراء (SLE)")
            f_ra = st.checkbox("تاريخ عائلي للروماتويد (RA)")
            f_as = st.checkbox("تاريخ عائلي للتيبس الفقاري (AS)")
            
        with col_symp:
            st.markdown("**مراجعة الأنظمة (ROS):**")
            malar_rash = st.toggle("طفح جلدي الفراشة (Malar Rash)")
            oral_ulcers = st.toggle("قرح متكررة في الفم")
            foam_urine = st.toggle("رغوة كثيفة في البول (مؤشر كلوي)")
            abortions = st.toggle("تاريخ إجهاض متكرر (للسيدات)")
            pleuritic_pain = st.toggle("ألم في الصدر مع التنفس")
            
        st.write("---")
        st.subheader("🏃 3. التقييم الحركي")
        col_motor1, col_motor2 = st.columns(2)
        with col_motor1:
            morning_stiffness = st.selectbox("مدة التيبس الصباحي", ["لا يوجد", "أقل من 30 دقيقة", "من 30-60 دقيقة", "أكثر من ساعة"])
            symmetrical = st.toggle("التورم متماثل في الجانبين")
        with col_motor2:
            movement_improve = st.toggle("الألم يتحسن مع الحركة وبذل المجهود")
            pain_score = st.slider("مقياس شدة الألم", 0, 10, 5)

        submit_doctor = st.form_submit_button("🤖 تحليل الحالة عبر الذكاء الاصطناعي (CDSS)")

    if submit_doctor:
        # تجميع البيانات لإرسالها للمحرك
        hist_data = {'lupus': f_lupus, 'ra': f_ra, 'as_fam': f_as}
        symp_data = {
            'malar_rash': malar_rash, 'oral_ulcers': oral_ulcers, 
            'foam_urine': foam_urine, 'abortions': abortions,
            'pleuritic_pain': pleuritic_pain, 'morning_stiffness': morning_stiffness,
            'symmetrical': symmetrical, 'movement_improve': movement_improve
        }
        
        # تأثير تحميل وهمي للإبهار في العرض
        with st.spinner('يتم تحليل البيانات ومقارنتها بالمعايير العالمية (ACR/EULAR)...'):
            time.sleep(2)
            
        ai_results = simulate_ai_cdss(p, hist_data, symp_data)
        
        st.write("---")
        st.header("🎯 تقرير محرك دعم اتخاذ القرار (AI CDSS Output)")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.subheader("الاحتمالات التشخيصية (Differential Diagnosis)")
            st.write("**الذئبة الحمراء الجهازية (SLE):**")
            st.progress(ai_results["SLE"] / 100)
            st.caption(f"الاحتمالية: {ai_results['SLE']}%")
            
            st.write("**التهاب المفاصل الروماتويدي (RA):**")
            st.progress(ai_results["RA"] / 100)
            st.caption(f"الاحتمالية: {ai_results['RA']}%")
            
            st.write("**التهاب الفقار اللاصق (AS):**")
            st.progress(ai_results["AS"] / 100)
            st.caption(f"الاحتمالية: {ai_results['AS']}%")

        with res_col2:
            st.subheader("🧪 خطة الفحص المقترحة (Suggested Workup)")
            if len(ai_results["workup"]) > 0:
                for item in ai_results["workup"]:
                    st.info(f"✔️ {item}")
            else:
                st.write("الأعراض الحالية لا تتطلب فحوصات مناعية متقدمة عاجلة. يرجى المتابعة السريرية.")
                
    st.write("---")
    if st.button("🔄 استقبال مريض جديد"):
        st.session_state.app_page = 'reception_screen'
        st.rerun()
