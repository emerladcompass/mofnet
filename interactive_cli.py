#!/usr/bin/env python3
"""
MOFNet Interactive CLI - واجهة سطر أوامر تفاعلية
"""

import mofnet
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print("╔══════════════════════════════════════╗")
    print("║     🏥 MOFNet Clinical Analyzer      ║")
    print("║     Terminal Edition v{}     ║".format(mofnet.__version__))
    print("╚══════════════════════════════════════╝")
    print()

def get_vitals():
    print("📊 Enter Patient Vitals:")
    print("-" * 40)
    
    vitals = {}
    vitals['heart_rate'] = int(input("Heart Rate (bpm) [80]: ") or "80")
    vitals['sbp'] = int(input("Systolic BP (mmHg) [120]: ") or "120")
    vitals['dbp'] = int(input("Diastolic BP (mmHg) [80]: ") or "80")
    vitals['rr'] = int(input("Respiratory Rate [16]: ") or "16")
    vitals['spo2'] = int(input("Oxygen Saturation (%) [98]: ") or "98")
    
    return vitals

def display_results(vitals, pri, classification, risk_prediction):
    print("\n" + "=" * 50)
    print("📋 CLINICAL ANALYSIS REPORT")
    print("=" * 50)
    
    print("\n📊 VITAL SIGNS:")
    print(f"  ❤️  Heart Rate: {vitals['heart_rate']} bpm")
    print(f"  💪 Blood Pressure: {vitals['sbp']}/{vitals['dbp']} mmHg")
    print(f"  💨 Respiratory Rate: {vitals['rr']} breaths/min")
    print(f"  💨 Oxygen Saturation: {vitals['spo2']}%")
    
    print("\n🔬 PRI ANALYSIS:")
    print(f"  📈 PRI Score: {pri:.3f}")
    
    # Color code classification
    if classification == "Excellent":
        color = "🟢"
    elif classification == "Good":
        color = "🟡"
    elif classification == "Moderate":
        color = "🟠"
    else:
        color = "🔴"
    
    print(f"  🏷️  Classification: {color} {classification}")
    
    print("\n🤖 AI RISK PREDICTION:")
    print(f"  ⚠️  Risk Level: {risk_prediction['risk_level']}")
    print(f"  📊 Risk Score: {risk_prediction['risk_score']:.3f}")
    
    print("\n🏥 ORGAN-SPECIFIC RISKS:")
    for organ, score in risk_prediction['organ_scores'].items():
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        print(f"  • {organ.title():12} [{bar}] {score:.2f}")
    
    print("\n" + "=" * 50)
    print("💡 CLINICAL RECOMMENDATIONS:")
    
    if risk_prediction['risk_level'] == "Low":
        print("  ✅ Continue routine monitoring")
    elif risk_prediction['risk_level'] == "Medium":
        print("  ⚠️  Increase monitoring frequency")
        print("  📋 Consider additional tests")
    else:
        print("  🚨 Immediate clinical review required")
        print("  📞 Alert medical team")
        print("  🏥 Consider ICU transfer")

def main():
    predictor = mofnet.MOFNetPredictor()
    
    while True:
        print_header()
        
        print("1. 🔬 Analyze New Patient")
        print("2. 🤖 Train AI Model")
        print("3. ℹ️  About MOFNet")
        print("4. 🚪 Exit")
        print()
        
        choice = input("Select option [1]: ") or "1"
        
        if choice == "1":
            vitals = get_vitals()
            
            # Calculate PRI
            pri = mofnet.calculate_pri(
                vitals['heart_rate'],
                vitals['sbp'],
                vitals['dbp'],
                vitals['rr'],
                vitals['spo2']
            )
            classification = mofnet.classify_pri_level(pri)
            
            # Get AI prediction
            predictor.train()
            risk_prediction = predictor.predict_risk(vitals)
            
            display_results(vitals, pri, classification, risk_prediction)
            
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("\n🤖 Training AI Model...")
            accuracy = predictor.train()
            print(f"✅ Model trained successfully")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\nℹ️  ABOUT MOFNet:")
            print(f"Version: {mofnet.__version__}")
            print("Author: Samir Baladi")
            print("Description: Multi-Organ Failure Prediction System")
            print("Platform: Termux/Android Compatible")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            print("\n👋 Thank you for using MOFNet!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session ended")
