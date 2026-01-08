import mofnet.extended as ext

test_cases = [
    ("مثالي", 72, 120, 80, 16, 98, 15, 50, 37.0),
    ("متدهور عصبي", 72, 120, 80, 16, 98, 6, 50, 37.0),
    ("متدهور كلوي", 72, 120, 80, 16, 98, 15, 15, 37.0),
    ("حمى شديدة", 72, 120, 80, 16, 98, 15, 50, 39.8),
    ("حالة حرجة", 140, 90, 60, 28, 85, 6, 10, 39.5),
]

predictor = ext.ExtendedMOFNetPredictor()
predictor.train()

print("🧪 اختبار شامل للنموذج الموسع:")
print("=" * 60)

for name, hr, sbp, dbp, rr, spo2, gcs, urine, temp in test_cases:
    vitals = {
        'heart_rate': hr, 'sbp': sbp, 'dbp': dbp, 'rr': rr, 'spo2': spo2,
        'gcs': gcs, 'urine_output': urine, 'temperature': temp
    }
    
    result = predictor.predict_risk(vitals)
    epri = result['epri']
    
    print(f"\n{name}:")
    print(f"  ePRI: {epri:.3f} → {result['epri_classification']}")
    print(f"  الخطورة: {result['risk_level']}")
    print(f"  متسق: {'✓' if result['consistent'] else '✗'}")
    print(f"  ثقة: {result['confidence']:.2f}")
    
print("\n" + "=" * 60)
print("✅ الاختبار اكتمل بنجاح!")
