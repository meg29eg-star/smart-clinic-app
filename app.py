import streamlit as st
import pandas as pd
from datetime import date
import google.generativeai as genai

# =================================================================
# ⚙️ إعداد الصفحة وإعدادات محرك الذكاء الاصطناعي (AI CDSS)
# =================================================================
st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")

# إعداد الذاكرة
if 'app_page' not in st.session_state:
    st.session_state.app_page = 'reception_screen'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

# الشريط الجانبي لتفعيل المحرك الحقيقي
st.sidebar.header("🧠 إعدادات محرك AI CDSS")
st.sidebar.info("لإجراء تحليل طبي حقيقي، يرجى إدخال مفتاح Gemini API الخاص بك بالأسفل.")
api_key = st.sidebar.text_input("API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest') # النموذج الاحترافي الأقوى طبياً

# =================================================================
# 📱 1. شاشة موظف الاستقبال (Front Desk Module) - لم يُمس منها سطر
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

        submit_reception = st.form_submit_button("حفظ البيانات وإحالة إلى الطبيب ➡️")

    if submit_reception:
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
        st.session_state.app_page = 'doctor_screen'
        st.rerun()

# =================================================================
# 💻 2. واجهة الطبيب الاستشاري التوسعية (Clinical Modules - Scroll View)
# =================================================================
elif st.session_state.app_page == 'doctor_screen':
    st.title("💻 واجهة الطبيب الاستشاري - الشيت الطبي الشامل")
    
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
        
        # 2. العلاجات والأطباء السابقين
        st.subheader("2. العلاجات والأطباء السابقين")
        c1, c2, c3 = st.columns(3)
        past_physio = c1.toggle("هل خضع لعلاج طبيعي سابقاً؟")
        past_surgery = c2.toggle("هل خضع لتدخل جراحي للمفاصل؟")
        past_injection = c3.toggle("هل خضع لحقن موضعي في المفاصل؟")
        past_doctors = st.text_area("قائمة الأطباء السابقين الذين تم استشارتهم لنفس الشكوى")
        
        # 3. مصفوفة التاريخ العائلي للأمراض الروماتيزمية
        st.write("---")
        st.subheader("🧬 3. مصفوفة التاريخ العائلي للأمراض الروماتيزمية (Family History Grid)")
        
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
        with f_col1:
            st.markdown("**الذئبة الحمراء (Lupus)**")
            f_lupus_pt = st.checkbox("المريض نفسه", key="fl1")
            f_lupus_fa = st.checkbox("الأب", key="fl2")
            f_lupus_mo = st.checkbox("الأم", key="fl3")
            f_lupus_sib = st.checkbox("الأخوة/الأخوات", key="fl4")
        with f_col2:
            st.markdown("**الروماتويد (RA)**")
            f_ra_pt = st.checkbox("المريض نفسه", key="fr1")
            f_ra_fa = st.checkbox("الأب", key="fr2")
            f_ra_mo = st.checkbox("الأم", key="fr3")
            f_ra_sib = st.checkbox("الأخوة", key="fr4")
        with f_col3:
            st.markdown("**النقرس (Gout)**")
            f_gout_pt = st.checkbox("المريض نفسه", key="fg1")
            f_gout_fa = st.checkbox("الأب", key="fg2")
            f_gout_sib = st.checkbox("الأخوة", key="fg3")
        with f_col4:
            st.markdown("**التيبس الفقاري (AS)**")
            f_as_pt = st.checkbox("المريض", key="fa1")
            f_as_fam = st.checkbox("الأب/الأخوة", key="fa2")
        with f_col5:
            st.markdown("**الصدفية والخشونة**")
            f_oa_pt = st.checkbox("خشونة (المريض)", key="fo1")
            f_oa_mo = st.checkbox("خشونة (الأم)", key="fo2")
            f_pso_pt = st.checkbox("صدفية (المريض)", key="fp1")
            f_pso_fam = st.checkbox("صدفية (الأقارب)", key="fp2")

        # 4. مراجعة الأنظمة الطبية الشاملة
        st.write("---")
        st.subheader("🫁 4. مراجعة الأنظمة الطبية الشاملة بالتفصيل (Complete Systems Review - ROS)")
        
        r_c1, r_c2, r_c3 = st.columns(3)
        dexa_date = r_c1.text_input("آخر فحص هشاشة عظام (DEXA Scan)")
        cxr_date = r_c2.text_input("آخر أشعة عادية على الصدر (Chest X-ray)")
        mammo_date = r_c3.text_input("آخر فحص ماموجرام للثدي")

        ros_col1, ros_col2 = st.columns(2)
        with ros_col1:
            st.markdown("**👁️ فحص العيون، الأنف، الأذن والحلق (HEENT & Sicca):**")
            dry_eyes = st.toggle("جفاف مزمن في العين (Dry Eyes / Sicca)")
            red_eyes = st.toggle("احمرار متكرر أو مؤلم في العين (Scleritis)")
            dry_mouth = st.toggle("جفاف شديد في الفم وصعوبة بلع الطعام الجاف")
            
            st.markdown("**🫀 فحص القلب، الأوعية الدموية والجهاز التنفسي:**")
            pleuritic_pain = st.toggle("ألم في الصدر يزداد مع التنفس العميق (Pleuritic Pain)")
            dyspnea = st.toggle("ضيق في التنفس عند بذل مجهود بسيط")

        with ros_col2:
            st.markdown("**🩺 فحص الجهاز الهضمي، البولي والتناسلي:**")
            foam_urine = st.toggle("وجود رغوة كثيفة في البول (Proteinuria - ذئبة كلوية)")
            genital_ulcers = st.toggle("قرح متكررة في الأعضاء التناسلية (بهجت - Behcet's)")
            
            st.markdown("**🤰 التاريخ النسائي والولادة (خاص بالسيدات):**")
            abortions_count = st.number_input("عدد مرات الإجهاض التلقائي", min_value=0, max_value=10, value=0)
            
            st.markdown("**🧠 الغدد، المناعة والجهاز العصبي:**")
            purpura_spots = st.toggle("ظهور بقع زرقاء أو كدمات على الجلد بدون إصابة")
            alopecia = st.toggle("تساقط شعر كثيف ومفاجئ يؤدي لصلع بقعي")
            sclerodactyly = st.toggle("تغير لون جلد اليدين مع شد وسمك (Sclerodactyly)")

        # 5. التقييم العضلي الحركي والمبدئي
        st.write("---")
        st.subheader("🏃 5. التقييم الحركي والتيبس الإكلينيكي المبدئي")
        
        col_left_2, col_right_2 = st.columns(2)
        with col_left_2:
            st.write("**الأعراض الإدارية السابقة:**")
            weight_loss_old = st.toggle("فقدان وزن عام (قديم)", key="wl_old")
            fever_old = st.toggle("حمى متكررة (قديم)", key="fe_old")
            oral_ulcers_old = st.toggle("قرح فم (قديمة)", key="ou_old")
            malar_rash_old = st.toggle("طفح جلدي على الخدين والأنف (Butterfly)", key="mr_old")
            
        with col_right_2:
            st.write("**التقييم الحركي والنوع الحركي الفعلي:**")
            morning_stiffness = st.selectbox("مدة التيبس الصباحي في المفاصل", ["لا يوجد", "أقل من 30 دقيقة", "من 30-60 دقيقة", "أكثر من ساعة"], key="ms_new")
            movement_improve_old = st.toggle("هل يتحسن ألم وتيبس المفاصل مع الحركة؟", key="mi_old")
            joint_swelling_old = st.toggle("وجود تورم واضح وملاحظ بالعين في المفاصل", key="js_old")
            symmetrical_swelling_old = st.toggle("هل التورم متماثل في جانبي الجسم؟", key="ss_old")

        st.markdown("**🔥 مقياس الألم الوظيفي الموحد:**")
        pain_score = st.slider("مقياس تقييم المريض العام لشدة الألم الحالية (PtGA)", 0, 10, 5, key="ps_final")

        submit_doctor = st.form_submit_button("🧠 تحليل الحالة الطبية واستخراج التشخيص الفعلي (Real AI CDSS)")

    # =================================================================
    # 🤖 معالجة وربط الذكاء الاصطناعي الحقيقي عند الضغط على الزر
    # =================================================================
    if submit_doctor:
        if not api_key:
            st.error("⚠️ يرجى إدخال مفتاح API في الشريط الجانبي لتشغيل المحرك الحقيقي.")
        else:
            with st.spinner('⏳ يقوم الذكاء الاصطناعي (Gemini Medical Engine) بتحليل الحالة وربط المتلازمات...'):
                
                # تجميع كافة البيانات السريرية في "Prompt" طبي احترافي
                clinical_summary = f"""
                أنت محرك ذكاء اصطناعي طبي متخصص في الروماتيزم (Rheumatology CDSS).
                تم إدخال حالة المريض التالية في العيادة، والمطلوب منك إصدار تقرير استشاري دقيق:
                
                - الديموغرافيا: {p.get('الجنس')}، السن {p.get('السن')} سنة.
                - الشكوى الرئيسية: {chief_complaint}
                - تاريخ البداية: {onset_duration}
                - تقييم الألم: {pain_score}/10
                - مدة التيبس الصباحي: {morning_stiffness}
                - تحسن الألم مع الحركة: {"نعم" if movement_improve_old else "لا"}
                - تورم المفاصل: {"نعم" if joint_swelling_old else "لا"}، متماثل: {"نعم" if symmetrical_swelling_old else "لا"}
                
                الأعراض المصاحبة (Positive ROS):
                - حمى: {"نعم" if fever_old else "لا"}
                - طفح جلدي (Malar): {"نعم" if malar_rash_old else "لا"}
                - قرح الفم: {"نعم" if oral_ulcers_old else "لا"}
                - رغوة بالبول: {"نعم" if foam_urine else "لا"}
                - جفاف عين/فم: {"نعم" if dry_eyes or dry_mouth else "لا"}
                - عدد مرات الإجهاض: {abortions_count}
                
                التاريخ العائلي:
                - ذئبة حمراء: {"نعم" if f_lupus_pt or f_lupus_fa or f_lupus_mo or f_lupus_sib else "لا"}
                - روماتويد: {"نعم" if f_ra_pt or f_ra_fa or f_ra_mo or f_ra_sib else "لا"}
                - تيبس فقاري: {"نعم" if f_as_pt or f_as_fam else "لا"}

                المطلوب عرض الرد حصرياً بالتنسيق التالي باللغة العربية:
                1. 📊 الاحتمالات التشخيصية (Differential Diagnosis): اذكر أهم 3 تشخيصات محتملة مع وضع نسبة مئوية تقديرية لكل منها.
                2. 🧬 التفسير السريري (Clinical Reasoning): اشرح بإيجاز شديد لماذا تم اختيار التشخيص الأول كأعلى احتمال بناءً على المعايير.
                3. 🧪 خطة الفحص المقترحة (Suggested Workup): اذكر التحاليل المخبرية والأشعة المحددة لتأكيد التشخيص واستبعاد الاحتمالات الأخرى.
                """
                
                try:
                    # استدعاء العقل المدبر الفعلي
                    response = model.generate_content(clinical_summary)
                    
                    st.success("✅ اكتمل التحليل السريري الذكي.")
                    st.write("---")
                    st.header("🎯 تقرير محرك دعم اتخاذ القرار (Real AI CDSS Output)")
                    
                    # عرض إجابة الذكاء الاصطناعي بشكل منسق
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال بالمحرك الذكي: {e}")

    st.write("---")
    if st.button("🔄 استقبال مريض جديد"):
        st.session_state.app_page = 'reception_screen'
        st.rerun()
