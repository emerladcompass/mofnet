"""
Real-time Patient Monitoring Example
Simulates continuous vital sign monitoring
"""

import mofnet
import time
import random

class PatientMonitor:
    """Simulates real-time patient monitoring"""
    
    def __init__(self, patient_id="P001"):
        self.patient_id = patient_id
        self.vitals_history = []
        
    def generate_vitals(self):
        """Generate simulated vital signs"""
        return {
            'hr': random.randint(60, 140),
            'bp_sys': random.randint(80, 180),
            'bp_dia': random.randint(50, 120),
            'rr': random.randint(12, 32),
            'spo2': random.randint(85, 100)
        }
    
    def analyze_vitals(self, vitals):
        """Analyze vitals and return results"""
        pri = mofnet.calculate_pri_from_dict(vitals)
        classification = mofnet.classify_pri_level(pri)
        
        return {
            'pri': pri,
            'classification': classification,
            'timestamp': time.time(),
            'vitals': vitals.copy()
        }
    
    def monitor(self, duration_seconds=30, interval_seconds=2):
        """Run monitoring simulation"""
        print(f"🏥 Real-time Patient Monitoring - Patient: {self.patient_id}")
        print("=" * 60)
        
        start_time = time.time()
        readings = 0
        
        while time.time() - start_time < duration_seconds:
            # Generate new vitals
            current_vitals = self.generate_vitals()
            
            # Analyze
            result = self.analyze_vitals(current_vitals)
            self.vitals_history.append(result)
            
            # Display
            readings += 1
            print(f"\n📊 Reading #{readings}")
            print(f"   Time: {time.strftime('%H:%M:%S')}")
            print(f"   HR: {current_vitals['hr']} bpm")
            print(f"   BP: {current_vitals['bp_sys']}/{current_vitals['bp_dia']} mmHg")
            print(f"   RR: {current_vitals['rr']} bpm")
            print(f"   SpO2: {current_vitals['spo2']}%")
            print(f"   PRI: {result['pri']:.3f}")
            print(f"   Status: {result['classification']}")
            
            # Alert if critical
            if result['classification'] in ['Critical', 'Poor']:
                print(f"   ⚠️  ALERT: Patient requires attention!")
            
            time.sleep(interval_seconds)
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate monitoring session summary"""
        print("\n" + "=" * 60)
        print("📋 Monitoring Session Summary")
        print("=" * 60)
        
        total_readings = len(self.vitals_history)
        if total_readings == 0:
            print("No readings recorded.")
            return
        
        # Calculate statistics
        pri_values = [r['pri'] for r in self.vitals_history]
        avg_pri = sum(pri_values) / total_readings
        min_pri = min(pri_values)
        max_pri = max(pri_values)
        
        # Count classifications
        classifications = [r['classification'] for r in self.vitals_history]
        critical_count = classifications.count('Critical')
        poor_count = classifications.count('Poor')
        moderate_count = classifications.count('Moderate')
        good_count = classifications.count('Good')
        excellent_count = classifications.count('Excellent')
        
        print(f"Total Readings: {total_readings}")
        print(f"Average PRI: {avg_pri:.3f}")
        print(f"Minimum PRI: {min_pri:.3f}")
        print(f"Maximum PRI: {max_pri:.3f}")
        print(f"\nClassification Distribution:")
        print(f"  Excellent: {excellent_count} ({excellent_count/total_readings*100:.1f}%)")
        print(f"  Good: {good_count} ({good_count/total_readings*100:.1f}%)")
        print(f"  Moderate: {moderate_count} ({moderate_count/total_readings*100:.1f}%)")
        print(f"  Poor: {poor_count} ({poor_count/total_readings*100:.1f}%)")
        print(f"  Critical: {critical_count} ({critical_count/total_readings*100:.1f}%)")
        
        if critical_count > 0 or poor_count > 0:
            print(f"\n⚠️  ALERT: {critical_count + poor_count} readings indicated poor/critical status!")
            print("   Immediate medical attention recommended.")
        else:
            print(f"\n✅ Patient maintained stable status throughout monitoring.")

def main():
    """Main function to run monitoring simulation"""
    monitor = PatientMonitor(patient_id="ICU-P001")
    monitor.monitor(duration_seconds=20, interval_seconds=1.5)

if __name__ == "__main__":
    main()
