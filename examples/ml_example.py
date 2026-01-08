#!/usr/bin/env python3
"""
MOFNet ML Example - Termux Compatible
"""

import mofnet

print("🤖 MOFNet Machine Learning Demo")
print("=" * 50)

# Create predictor
predictor = mofnet.MOFNetPredictor()

# Train model
print("Training model...")
predictor.train()
print("✅ Model trained successfully")

# Test with sample patients
patients = [
    {
        "name": "Patient A (Stable)",
        "vitals": {"heart_rate": 75, "sbp": 120, "dbp": 80, "rr": 16, "spo2": 98}
    },
    {
        "name": "Patient B (Moderate)",
        "vitals": {"heart_rate": 105, "sbp": 145, "dbp": 90, "rr": 22, "spo2": 94}
    },
    {
        "name": "Patient C (Critical)",
        "vitals": {"heart_rate": 130, "sbp": 85, "dbp": 55, "rr": 30, "spo2": 82}
    }
]

print("\n📊 AI Predictions:")
print("-" * 40)

for patient in patients:
    result = predictor.predict_risk(patient["vitals"])
    
    print(f"\n👤 {patient['name']}")
    print(f"  Vitals: HR={patient['vitals']['heart_rate']}, "
          f"BP={patient['vitals']['sbp']}/{patient['vitals']['dbp']}, "
          f"RR={patient['vitals']['rr']}, SpO2={patient['vitals']['spo2']}%")
    print(f"  🤖 AI Prediction: {result['risk_level']} risk")
    print(f"  📈 Risk Score: {result['risk_score']:.3f}")
    
    # Show organ risks
    print(f"  🏥 Organ Risks:")
    for organ, score in result['organ_scores'].items():
        level = "Low" if score < 0.3 else "Medium" if score < 0.6 else "High"
        print(f"    • {organ.title()}: {level} ({score:.2f})")

print("\n" + "=" * 50)
print("✅ ML Demo Complete")
print(f"📁 Model saved: mofnet_model.json")
