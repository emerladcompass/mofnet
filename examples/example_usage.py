#!/usr/bin/env python3
"""
MOFNet Usage Example
"""

import mofnet

print("🏥 Physiological Resilience Analysis Report")
print("=" * 50)

# Patient data
patients = [
    {
        "name": "Patient A",
        "vitals": {
            "heart_rate": 80,
            "sbp": 120,
            "dbp": 80,
            "rr": 16,
            "spo2": 98
        }
    },
    {
        "name": "Patient B", 
        "vitals": {
            "heart_rate": 95,
            "sbp": 140,
            "dbp": 90,
            "rr": 20,
            "spo2": 95
        }
    },
    {
        "name": "Patient C",
        "vitals": {
            "heart_rate": 110,
            "sbp": 160,
            "dbp": 100,
            "rr": 24,
            "spo2": 92
        }
    },
    {
        "name": "Patient D",
        "vitals": {
            "heart_rate": 130,
            "sbp": 85,
            "dbp": 55,
            "rr": 32,
            "spo2": 82
        }
    }
]

for patient in patients:
    # Get vitals
    v = patient["vitals"]
    
    # Method 1: Direct calculation
    pri = mofnet.calculate_pri(
        v["heart_rate"],
        v["sbp"],
        v["dbp"],
        v["rr"],
        v["spo2"]
    )
    
    # Method 2: Using dictionary (alternative)
    # pri = mofnet.calculate_pri_from_dict(v)
    
    # Classify result
    classification = mofnet.classify_pri_level(pri)
    
    # Display results
    print(f"\n👤 Patient: {patient['name']}")
    print(f"  Heart Rate: {v['heart_rate']} bpm")
    print(f"  Blood Pressure: {v['sbp']}/{v['dbp']} mmHg")
    print(f"  Respiratory Rate: {v['rr']} bpm")
    print(f"  Oxygen Saturation: {v['spo2']}%")
    print(f"  PRI Index: {pri:.3f}")
    print(f"  Classification: {classification}")

print("\n" + "=" * 50)
print("✅ Report ready!")
