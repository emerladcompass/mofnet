"""
Basic Usage Example for mofnet Library
Demonstrates core functionality
"""

import mofnet

def main():
    print("🏥 mofnet - Medical MOF Prediction - Basic Usage")
    print("=" * 60)
    
    # Example 1: Direct parameter calculation
    print("\n1. Using calculate_pri() with individual parameters:")
    pri1 = mofnet.calculate_pri(
        hr=80,
        bp_sys=120,
        bp_dia=80,
        rr=16,
        spo2=98
    )
    print(f"   Inputs: HR=80, BP=120/80, RR=16, SpO2=98%")
    print(f"   Result: PRI = {pri1}")
    print(f"   Classification: {mofnet.classify_pri_level(pri1)}")
    
    # Example 2: Dictionary calculation (preferred method)
    print("\n2. Using calculate_pri_from_dict() with dictionary:")
    vitals = {
        'hr': 85,
        'bp_sys': 130,
        'bp_dia': 85,
        'rr': 18,
        'spo2': 96
    }
    pri2 = mofnet.calculate_pri_from_dict(vitals)
    print(f"   Inputs: {vitals}")
    print(f"   Result: PRI = {pri2}")
    print(f"   Classification: {mofnet.classify_pri_level(pri2)}")
    
    # Example 3: Different key naming conventions
    print("\n3. Using alternative key names:")
    vitals_alt = {
        'heart_rate': 90,
        'blood_pressure_systolic': 140,
        'blood_pressure_diastolic': 90,
        'respiratory_rate': 20,
        'oxygen_saturation': 94
    }
    pri3 = mofnet.calculate_pri_from_dict(vitals_alt)
    print(f"   Inputs: {vitals_alt}")
    print(f"   Result: PRI = {pri3}")
    print(f"   Classification: {mofnet.classify_pri_level(pri3)}")
    
    # Example 4: Partial data (uses defaults)
    print("\n4. Using partial data (missing values use defaults):")
    vitals_partial = {
        'hr': 100,
        'bp_sys': 150
        # Missing: bp_dia, rr, spo2 will use defaults
    }
    pri4 = mofnet.calculate_pri_from_dict(vitals_partial)
    print(f"   Inputs: {vitals_partial}")
    print(f"   Result: PRI = {pri4}")
    print(f"   Classification: {mofnet.classify_pri_level(pri4)}")
    
    # Example 5: Critical patient
    print("\n5. Critical patient scenario:")
    vitals_critical = {
        'hr': 130,
        'bp_sys': 85,
        'bp_dia': 55,
        'rr': 32,
        'spo2': 82
    }
    pri5 = mofnet.calculate_pri_from_dict(vitals_critical)
    print(f"   Inputs: {vitals_critical}")
    print(f"   Result: PRI = {pri5}")
    print(f"   Classification: {mofnet.classify_pri_level(pri5)}")
    
    print("\n" + "=" * 60)
    print("✅ Basic usage examples completed successfully!")

if __name__ == "__main__":
    main()
