"""
Retrospective Patient Data Analysis Example
Analyzes historical patient data
"""

import mofnet
import json
import statistics
from datetime import datetime, timedelta

class PatientDataAnalyzer:
    """Analyzes historical patient data"""
    
    def __init__(self):
        self.patients_data = []
    
    def load_sample_data(self):
        """Load sample patient data"""
        self.patients_data = [
            {
                "patient_id": "P001",
                "name": "John Smith",
                "age": 45,
                "condition": "Hypertension",
                "vitals_history": [
                    {"timestamp": "2024-01-01 08:00", "hr": 85, "bp_sys": 140, "bp_dia": 90, "rr": 18, "spo2": 96},
                    {"timestamp": "2024-01-01 14:00", "hr": 82, "bp_sys": 138, "bp_dia": 88, "rr": 17, "spo2": 97},
                    {"timestamp": "2024-01-01 20:00", "hr": 88, "bp_sys": 142, "bp_dia": 92, "rr": 19, "spo2": 95},
                ]
            },
            {
                "patient_id": "P002",
                "name": "Maria Garcia",
                "age": 62,
                "condition": "Diabetes",
                "vitals_history": [
                    {"timestamp": "2024-01-01 09:00", "hr": 92, "bp_sys": 130, "bp_dia": 85, "rr": 20, "spo2": 94},
                    {"timestamp": "2024-01-01 15:00", "hr": 95, "bp_sys": 135, "bp_dia": 88, "rr": 22, "spo2": 93},
                    {"timestamp": "2024-01-01 21:00", "hr": 90, "bp_sys": 128, "bp_dia": 83, "rr": 19, "spo2": 95},
                ]
            },
            {
                "patient_id": "P003",
                "name": "Robert Chen",
                "age": 38,
                "condition": "Post-operative",
                "vitals_history": [
                    {"timestamp": "2024-01-01 10:00", "hr": 75, "bp_sys": 118, "bp_dia": 78, "rr": 16, "spo2": 98},
                    {"timestamp": "2024-01-01 16:00", "hr": 78, "bp_sys": 120, "bp_dia": 80, "rr": 15, "spo2": 99},
                    {"timestamp": "2024-01-01 22:00", "hr": 72, "bp_sys": 116, "bp_dia": 76, "rr": 14, "spo2": 99},
                ]
            }
        ]
    
    def analyze_patient(self, patient):
        """Analyze a single patient's history"""
        pri_scores = []
        classifications = []
        
        for reading in patient["vitals_history"]:
            # Calculate PRI for each reading
            vitals = {k: reading[k] for k in ['hr', 'bp_sys', 'bp_dia', 'rr', 'spo2']}
            pri = mofnet.calculate_pri_from_dict(vitals)
            classification = mofnet.classify_pri_level(pri)
            
            pri_scores.append(pri)
            classifications.append(classification)
        
        # Calculate statistics
        if pri_scores:
            avg_pri = statistics.mean(pri_scores)
            min_pri = min(pri_scores)
            max_pri = max(pri_scores)
            pri_trend = "stable"
            if len(pri_scores) >= 2:
                if pri_scores[-1] > pri_scores[0]:
                    pri_trend = "improving"
                elif pri_scores[-1] < pri_scores[0]:
                    pri_trend = "declining"
        else:
            avg_pri = min_pri = max_pri = 0
            pri_trend = "no data"
        
        return {
            "patient_id": patient["patient_id"],
            "name": patient["name"],
            "average_pri": avg_pri,
            "min_pri": min_pri,
            "max_pri": max_pri,
            "pri_trend": pri_trend,
            "latest_classification": classifications[-1] if classifications else "Unknown",
            "readings_count": len(pri_scores)
        }
    
    def run_analysis(self):
        """Run comprehensive analysis"""
        print("📊 Retrospective Patient Data Analysis")
        print("=" * 60)
        
        # Load and analyze data
        self.load_sample_data()
        
        all_patients_results = []
        department_stats = {
            'total_patients': 0,
            'average_pri': 0,
            'critical_patients': 0,
            'stable_patients': 0
        }
        
        # Analyze each patient
        print("\n📋 Individual Patient Analysis:")
        print("-" * 40)
        
        for patient in self.patients_data:
            result = self.analyze_patient(patient)
            all_patients_results.append(result)
            
            print(f"\n👤 Patient: {result['name']} (ID: {result['patient_id']})")
            print(f"   Average PRI: {result['average_pri']:.3f}")
            print(f"   PRI Range: {result['min_pri']:.3f} - {result['max_pri']:.3f}")
            print(f"   Trend: {result['pri_trend']}")
            print(f"   Latest Status: {result['latest_classification']}")
            print(f"   Readings Analyzed: {result['readings_count']}")
            
            # Update department stats
            department_stats['total_patients'] += 1
            department_stats['average_pri'] += result['average_pri']
            
            if result['latest_classification'] in ['Critical', 'Poor']:
                department_stats['critical_patients'] += 1
            else:
                department_stats['stable_patients'] += 1
        
        # Calculate department averages
        if department_stats['total_patients'] > 0:
            department_stats['average_pri'] /= department_stats['total_patients']
        
        # Generate department report
        print("\n" + "=" * 60)
        print("🏥 Department Summary Report")
        print("=" * 60)
        
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Patients: {department_stats['total_patients']}")
        print(f"   Department Average PRI: {department_stats['average_pri']:.3f}")
        print(f"   Stable Patients: {department_stats['stable_patients']}")
        print(f"   Patients Requiring Attention: {department_stats['critical_patients']}")
        
        print(f"\n📋 Recommendations:")
        if department_stats['critical_patients'] > 0:
            print(f"   ⚠️  {department_stats['critical_patients']} patient(s) require immediate attention")
            print(f"   Consider increasing monitoring frequency")
        else:
            print(f"   ✅ All patients are stable")
            print(f"   Continue current monitoring protocols")
        
        print(f"\n📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

def main():
    """Main analysis function"""
    analyzer = PatientDataAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
