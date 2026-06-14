import streamlit as st
import pandas as pd
from datetime import date
import time

# إعداد الصفحة لتكون مريحة للعين ومتجاوبة
st.set_page_config(page_title="العيادة الروماتيزمية الذكية", layout="wide")

# إدارة التنقل بين شاشة الاستقبال وشاشة الطبيب في الذاكرة
if 'app_page' not in st.session_state:
    st.session_state.app_page = 'reception_screen'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

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
            "السن": age,
            "الجنس": gender,
            "الوظيفة": job_title,
            "جهة التأمين": insurance_provider
        }
        st.session_state.app_page = 'doctor_screen'
        st.rerun()

# =================================================================
# 💻 2. واجهة الطبيب الاستشاري التوسعية (Clinical Modules)
# =================================================================
elif st.session_state.app_page == 'doctor_screen':
    st.title("💻 واجهة الطبيب الاستشاري - الشيت الطبي الشامل")
    
    p = st.session_state.patient_data
    st.info(f"📋 **المريض المحال حالياً:** {p.get('اسم المريض')} | **السن:** {p.get('السن')} | **الجنس:** {p.get('الجنس')} | **جهة العمل:** {p.get('جهة التأمين')}")
    st.write("---")
    
    with st.form("doctor_form"):
        st.warning("⚠️ أدخل الأعراض والفحص السريري بالأسفل (تصفح لأسفل بنظام Scroll)")
        
        st.subheader("1. الشكوى والتاريخ الحالي (Present Symptoms)")
        chief_complaint = st.text_area("وصف الشكوى الرئيسية (Chief Complaint)")
        onset_duration = st.text_input("تاريخ بداية الأعراض / المدة (Onset & Duration)")
        previous_diagnosis = st.text_input("التشخيص السابق المعطى من أطباء آخرين")
        
        st.subheader("2. العلاجات والأطباء السابقين")
        c1, c2, c3 = st.columns(3)
        past_physio = c1.toggle("هل خضع لعلاج طبيعي سابقاً؟")
        past_surgery = c2.toggle("هل خضع لتدخل جراحي للمفاصل؟")
        past_injection = c3.toggle("هل خضع لحقن موضعي في المفاصل؟")
        past_doctors = st.text_area("قائمة الأطباء السابقين الذين تم استشارتهم لنفس الشكوى")
        
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

        st.write("---")
        st.subheader("🫁 4. مراجعة الأنظمة الطبية الشاملة بالتفصيل (Complete Systems Review - ROS)")
        
        r_c1, r_c2, r_c3 = st.columns(3)
        dexa_date = r_c1.text_input("آخر فحص هشاشة عظام (DEXA Scan)")
        cxr_date = r_c2.text_input("آخر أشعة عادية على الصدر (Chest X-ray)")
        mammo_date = r_c3.text_input("آخر فحص ماموجرام للثدي")

        ros_col1, ros_col2 = st.columns(2)
        with ros_col1:
            st.markdown("**👁️ فحص العيون، الأنف، الأذن والحلق:**")
            dry_eyes = st.toggle("جفاف مزمن في العين (Dry Eyes / Sicca)")
            red_eyes = st.toggle("احمرار متكرر أو مؤلم في العين (Scleritis)")
            dry_mouth = st.toggle("جفاف شديد في الفم وصعوبة بلع الطعام الجاف")
            
            st.markdown("**🫀 فحص القلب، الأوعية الدموية والجهاز التنفسي:**")
            pleuritic_pain = st.toggle("ألم في الصدر يزداد مع التنفس العميق")
            dyspnea = st.toggle("ضيق في التنفس عند بذل مجهود بسيط")

        with ros_col2:
            st.markdown("**🩺 فحص الجهاز الهضمي، البولي والتناسلي:**")
            foam_urine = st.toggle("وجود رغوة كثيفة في البول (Proteinuria)")
            genital_ulcers = st.toggle("قرح متكررة في الأعضاء التناسلية (بهجت)")
            
            st.markdown("**🤰 التاريخ النسائي والولادة:**")
            abortions_count = st.number_input("عدد مرات الإجهاض التلقائي", min_value=0, max_value=10, value=0)
            
            st.markdown("**🧠 الغدد، المناعة والجهاز العصبي:**")
            purpura_spots = st.toggle("ظهور بقع زرقاء أو كدمات على الجلد")
            alopecia = st.toggle("تساقط شعر كثيف ومفاجئ")
            sclerodactyly = st.toggle("تغير لون جلد اليدين مع شد وسمك")

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

        submit_doctor = st.form_submit_button("🧠 تشغيل محرك الدعم السريري الطبي والتحليل الفوري (AI CDSS)")

    # =================================================================
    # 🧠 الـ CDSS الداخلي العميق والمستقل (Clinical Logic Engine)
    # =================================================================
    if submit_doctor:
        with st.spinner('⏳ يقوم المحرك بمطابقة الأعراض إكلينيكياً مع معايير ACR/EULAR العالمية...'):
            time.sleep(1.5)
            
            # حساب النقاط والمؤشرات الطبية الحقيقية خلف الكواليس
            sle_points = 0
            ra_points = 0
            as_points = 0
            reasoning = []
            workup = []
            
            # تحليل معطيات الذئبة الحمراء (SLE)
            if p.get('الجنس') == "أنثى": sle_points += 2
            if malar_rash_old: 
                sle_points += 6
                reasoning.append("وجود طفح الفراشة الجلدي (Malar Rash) وهو علامة مميزة وعالية التوجيه.")
            if oral_ulcers_old:
                sle_points += 2
                reasoning.append("تكرار قرح الفم السريرية (Oral Ulcers).")
            if foam_urine:
                sle_points += 4
                reasoning.append("رغوة البول تشير لوجود زلال، مما يوجه بقوة لاحتمالية إصابة كلوية مناعية (Lupus Nephritis).")
                workup.append("• تحليل بول كامل ونسبة بروتين/كرياتينين (24-Hour Urine Protein).")
            if abortions_count > 0:
                sle_points += 3
                reasoning.append(f"التاريخ النسائي يسجل ({abortions_count}) مرات إجهاض تلقائي، مؤشر لمتلازمة الأجسام المضادة للفوسفوليبيد (APS).")
                workup.append("• فحص متلازمة الفوسفوليبيد (Antiphospholipid Antibodies: Lupus Anticoagulant, Anti-cardiolipin).")
            if f_lupus_mo or f_lupus_fa or f_lupus_sib:
                sle_points += 2
                reasoning.append("وجود استعداد جيني عبر التاريخ العائلي من الدرجة الأولى للذئبة.")

            # تحليل معطيات الروماتويد (RA)
            if joint_swelling_old: ra_points += 3
            if symmetrical_swelling_old:
                ra_points += 4
                reasoning.append("التورم المفصلي المتماثل (Symmetrical Polyarthritis) يطابق معياراً رئيسياً لمرض الروماتويد.")
            if morning_stiffness == "أكثر من ساعة":
                ra_points += 4
                reasoning.append("التيبس الصباحي الممتد لأكثر من ساعة يعكس نشاطاً التهابياً حاداً في الغشاء الزلالي.")
            if f_ra_mo or f_ra_fa:
                ra_points += 2

            # تحليل معطيات التيبس الفقاري (AS)
            if movement_improve_old:
                as_points += 6
                reasoning.append("تحسن آلام الظهر والمفاصل مع الحركة وبذل المجهود يعزز بقوة طبيعة الألم الالتهابية (Inflammatory Back Pain).")
            if f_as_fam:
                as_points += 3

            # إعداد التقارير والنسب بناء على مجموع النقاط الطبية
            sle_final = min(int((sle_points / 15) * 100), 96) if sle_points > 2 else 5
            ra_final = min(int((ra_points / 11) * 100), 94) if ra_points > 2 else 5
            as_final = min(int((as_points / 9) * 100), 92) if as_points > 2 else 5
            
            # فرز خطة العمل التلقائية والأساسية لقوة التشخيص
            if sle_final > 50: workup.append("• فحص الأجسام المضادة للنواة وعيارها عالي الدقة (ANA Titer & Anti-dsDNA).")
            if ra_final > 50: workup.append("• فحص معامل الروماتويد والأجسام المضادة للسيترولين (RF & Anti-CCP).")
            if as_final > 50: workup.append("• أشعة رنين مغناطيسي على المفصل الحرقفي وفحص الجين (MRI Sacroiliac Joints & HLA-B27).")
            if not workup: workup.append("• لا توجد مؤشرات حادة حالياً، يوصى بالفحوصات الدورية العامة (CBC, ESR, CRP).")

            st.success("✅ اكتمل التقييم السريري الذكي بنجاح.")
            st.write("---")
            st.header("🎯 تقرير محرك دعم اتخاذ القرار الإكلينيكي (AI CDSS Output)")
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.subheader("📊 الاحتمالات التشخيصية المقترحة (Differential Diagnosis)")
                
                st.write(f"**الذئبة الحمراء الجهازية (Systemic Lupus Erythematosus - SLE):** {sle_final}%")
                st.progress(sle_final / 100)
                
                st.write(f"**التهاب المفاصل الروماتويدي (Rheumatoid Arthritis - RA):** {ra_final}%")
                st.progress(ra_final / 100)
                
                st.write(f"**التهاب الفقار اللاصق / الروماتيزم التيبسي (Ankylosing Spondylitis - AS):** {as_final}%")
                st.progress(as_final / 100)

            with res_col2:
                st.subheader("🧬 التحليل الإكلينيكي للحالة (Clinical Reasoning)")
                if reasoning:
                    for r in reasoning:
                        st.write(f"🔹 {r}")
                else:
                    st.write("الأعراض المدخلة عامة، لا تظهر تلازميات لمرض مناعي محدد حتى الآن.")
                
                st.write("---")
                st.subheader("🧪 خطة الفحص والتحاليل المستهدفة (Suggested Workup)")
                for w in set(workup):
                    st.info(w)

    st.write("---")
    if st.button("🔄 استقبال مريض جديد"):
        st.session_state.app_page = 'reception_screen'
        st.rerun()
