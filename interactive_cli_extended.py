#!/usr/bin/env python3
"""
MOFNet Extended CLI - واجهة سطر أوامر للمؤشرات الثمانية
"""

import mofnet
import mofnet.extended as extended
import os
import sys

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print("╔════════════════════════════════════════════╗")
    print("║     🏥 MOFNet EXTENDED Clinical Analyzer   ║")
    print("║     8-Variable Edition v{}          ║".format(mofnet.__version__))
    print("╚════════════════════════════════════════════╝")
    print()

def get_extended_vitals():
    print("📊 أدخل المؤشرات السريرية (8 متغيرات):")
    print("=" * 50)
    
    vitals = {}
    
    # المؤشرات الأساسية الخمسة
    print("\n🔴 المؤشرات الأساسية:")
    vitals['heart_rate'] = int(input("معدل ضربات القلب (نبضة/دقيقة) [80]: ") or "80")
    vitals['sbp'] = int(input("الضغط الانقباضي (ملم زئبق) [120]: ") or "120")
    vitals['dbp'] = int(input("الضغط الانبساطي (ملم زئبق) [80]: ") or "80")
    vitals['rr'] = int(input("معدل التنفس (نفس/دقيقة) [16]: ") or "16")
    vitals['spo2'] = int(input("تشبع الأكسجين (%) [98]: ") or "98")
    
    # المؤشرات الجديدة الثلاثة
    print("\n🟢 المؤشرات الموسعة:")
    vitals['gcs'] = int(input("مقياس غلاسكو للوعي (3-15) [15]: ") or "15")
    vitals['urine_output'] = int(input("كمية البول (مل/ساعة) [50]: ") or "50")
    vitals['temperature'] = float(input("درجة الحرارة (°م) [37.0]: ") or "37.0")
    
    return vitals

def display_extended_results(vitals, pri, epri, risk_prediction):
    print("\n" + "═" * 60)
    print("📋 تقرير التحليل السريري الموسع")
    print("═" * 60)
    
    print("\n📊 المؤشرات المدخلة:")
    print(f"  ❤️  معدل ضربات القلب: {vitals['heart_rate']} نبضة/دقيقة")
    print(f"  💪 الضغط الدموي: {vitals['sbp']}/{vitals['dbp']} ملم زئبق")
    print(f"  💨 معدل التنفس: {vitals['rr']} نفس/دقيقة")
    print(f"  💨 تشبع الأكسجين: {vitals['spo2']}%")
    print(f"  🧠 مقياس غلاسكو: {vitals['gcs']}/15")
    print(f"  🚰 كمية البول: {vitals['urine_output']} مل/ساعة")
    print(f"  🌡️  درجة الحرارة: {vitals['temperature']}°م")
    
    print("\n🔬 تحليل PRI:")
    print(f"  📈 PRI الأساسي (5 متغيرات): {pri:.3f} → {mofnet.classify_pri_level(pri)}")
    print(f"  📊 ePRI الموسع (8 متغيرات): {epri:.3f} → {extended.classify_epri_level(epri)}")
    
    print("\n🤖 تنبؤات الذكاء الاصطناعي:")
    print(f"  ⚠️  مستوى الخطورة: {risk_prediction['risk_level']}")
    print(f"  📊 درجة الخطورة: {risk_prediction['risk_score']:.3f}")
    
    if 'epri' in risk_prediction and risk_prediction['epri']:
        print(f"  🔄 ePRI المحسوب: {risk_prediction['epri']:.3f}")
    
    print("\n🏥 خطورة الأعضاء:")
    for organ, score in risk_prediction['organ_scores'].items():
        bar_len = int(score * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        
        if 'neuro' in organ.lower():
            icon = "🧠"
        elif 'renal' in organ.lower():
            icon = "🫀"
        elif 'cardiac' in organ.lower():
            icon = "❤️"
        elif 'resp' in organ.lower():
            icon = "💨"
        elif 'hepatic' in organ.lower():
            icon = "🫁"
        else:
            icon = "⚕️"
            
        print(f"  {icon} {organ.title():15} [{bar}] {score:.2f}")
    
    print("\n" + "═" * 60)
    print("💡 التوصيات السريرية:")
    
    if risk_prediction['risk_level'] == "Low":
        print("  ✅ استمر في المراقبة الروتينية")
        print("  ✅ حالة مستقرة")
    elif risk_prediction['risk_level'] == "Medium":
        print("  ⚠️  زيادة وتيرة المراقبة (كل 2-4 ساعات)")
        print("  📋 فحص سريري مفصل")
        print("  💊 مراجعة الأدوية")
    else:
        print("  🚨 مراجعة سريرية فورية مطلوبة")
        print("  📞 تنبيه الفريق الطبي")
        print("  🏥 مراقبة مكثفة")
        
        # توصيات خاصة حسب العضو الأكثر خطورة
        max_organ = max(risk_prediction['organ_scores'].items(), key=lambda x: x[1])
        if max_organ[0] == 'neurological':
            print("  🧠 فحص عصبي عاجل")
        elif max_organ[0] == 'renal':
            print("  🫀 فحص وظائف الكلى")

def main():
    # تهيئة المتنبئ الموسع
    predictor = extended.ExtendedMOFNetPredictor()
    
    while True:
        print_header()
        
        print("1. 🔬 تحليل مريض جديد (8 متغيرات)")
        print("2. 📊 مقارنة PRI vs ePRI")
        print("3. 🤖 تدريب النموذج الموسع")
        print("4. ℹ️  عن الإصدار الموسع")
        print("5. 🚪 العودة (إغلاق)")
        print()
        
        choice = input("اختر الخيار [1]: ") or "1"
        
        if choice == "1":
            vitals = get_extended_vitals()
            
            # حساب PRI الأساسي (5 متغيرات)
            pri = mofnet.calculate_pri(
                vitals['heart_rate'],
                vitals['sbp'],
                vitals['dbp'],
                vitals['rr'],
                vitals['spo2']
            )
            
            # حساب ePRI الموسع (8 متغيرات)
            epri = extended.calculate_epri(
                vitals['heart_rate'],
                vitals['sbp'],
                vitals['dbp'],
                vitals['rr'],
                vitals['spo2'],
                vitals['gcs'],
                vitals['urine_output'],
                vitals['temperature']
            )
            
            # تنبؤات الذكاء الاصطناعي
            predictor.train()
            risk_prediction = predictor.predict_risk(vitals)
            
            display_extended_results(vitals, pri, epri, risk_prediction)
            
            input("\nاضغط Enter للمتابعة...")
            
        elif choice == "2":
            print("\n📊 مقارنة بين PRI و ePRI:")
            print("-" * 40)
            print("PRI (5 متغيرات): القلب، الضغط، التنفس، الأكسجين")
            print("ePRI (8 متغيرات): + مقياس غلاسكو، البول، الحرارة")
            print()
            print("فوائد ePRI:")
            print("  • تقييم عصبي عبر مقياس غلاسكو")
            print("  • تقييم كلوي عبر كمية البول")
            print("  • تقييم استقلابي عبر درجة الحرارة")
            print("  • تحسين التمييز بين الحالات")
            input("\nاضغط Enter للمتابعة...")
            
        elif choice == "3":
            print("\n🤖 تدريب النموذج الموسع...")
            predictor.train()
            print("✅ تم تدريب النموذج بنجاح")
            print(f"✅ يدعم 8 متغيرات سريرية")
            input("\nاضغط Enter للمتابعة...")
            
        elif choice == "4":
            print("\nℹ️  MOFNet الإصدار الموسع:")
            print(f"الإصدار: {mofnet.__version__}")
            print("المؤلف: Samir Baladi")
            print("الوصف: نظام تحليل سريري بـ 8 متغيرات")
            print("المتغيرات: 5 أساسية + 3 موسعة")
            print("الميزات: PRI، ePRI، تنبؤات ذكاء اصطناعي")
            input("\nاضغط Enter للمتابعة...")
            
        elif choice == "5":
            print("\n👋 شكراً لاستخدام MOFNet الموسع!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تم إنهاء الجلسة")
    except Exception as e:
        print(f"\n⚠️  خطأ: {e}")
        input("اضغط Enter للخروج...")

# في display_extended_results()، أضف:
print(f"  📊 تصنيف ePRI: {risk_prediction.get('epri_classification', 'N/A')}")
print(f"  ✅ التوافق: {'نعم' if risk_prediction.get('consistent', False) else 'لا'}")
