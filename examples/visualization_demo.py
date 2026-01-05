"""
Visualization Demo for mofnet Results
Shows different ways to visualize PRI data
"""

import mofnet
import random
import matplotlib.pyplot as plt
import numpy as np

class mofnetVisualizer:
    """Creates visualizations for mofnet data"""
    
    def __init__(self):
        self.sample_data = self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample patient data for visualization"""
        patients = []
        conditions = ['Hypertension', 'Diabetes', 'Post-op', 'ICU', 'Recovery']
        
        for i in range(1, 11):
            patient = {
                'id': f'P{i:03d}',
                'condition': random.choice(conditions),
                'age': random.randint(25, 80),
                'vitals': {
                    'hr': random.randint(60, 120),
                    'bp_sys': random.randint(100, 160),
                    'bp_dia': random.randint(60, 100),
                    'rr': random.randint(12, 28),
                    'spo2': random.randint(88, 100)
                }
            }
            # Calculate PRI
            patient['pri'] = mofnet.calculate_pri_from_dict(patient['vitals'])
            patient['classification'] = mofnet.classify_pri_level(patient['pri'])
            patients.append(patient)
        
        return patients
    
    def plot_pri_distribution(self):
        """Plot distribution of PRI scores"""
        pri_scores = [p['pri'] for p in self.sample_data]
        
        plt.figure(figsize=(10, 6))
        
        # Create histogram
        n, bins, patches = plt.hist(pri_scores, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add classification zones
        zones = [(0, 0.3, 'Critical', 'red'),
                (0.3, 0.5, 'Poor', 'orange'),
                (0.5, 0.7, 'Moderate', 'yellow'),
                (0.7, 0.85, 'Good', 'lightgreen'),
                (0.85, 1.0, 'Excellent', 'green')]
        
        for zone in zones:
            plt.axvspan(zone[0], zone[1], alpha=0.2, color=zone[3], label=zone[2])
        
        plt.title('PRI Score Distribution Across Patients', fontsize=14, fontweight='bold')
        plt.xlabel('PRI Score', fontsize=12)
        plt.ylabel('Number of Patients', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        print("📊 Generated: PRI Score Distribution Chart")
        plt.show()
    
    def plot_vitals_vs_pri(self):
        """Plot relationship between vitals and PRI"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        vitals_to_plot = [
            ('hr', 'Heart Rate (bpm)', axes[0, 0]),
            ('bp_sys', 'Systolic BP (mmHg)', axes[0, 1]),
            ('rr', 'Respiratory Rate (bpm)', axes[1, 0]),
            ('spo2', 'Oxygen Saturation (%)', axes[1, 1])
        ]
        
        for vital, title, ax in vitals_to_plot:
            x_data = [p['vitals'][vital] for p in self.sample_data]
            y_data = [p['pri'] for p in self.sample_data]
            
            # Scatter plot
            scatter = ax.scatter(x_data, y_data, c=y_data, cmap='RdYlGn', s=100, alpha=0.7, edgecolors='black')
            
            # Add trend line
            if len(x_data) > 1:
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)
                ax.plot(x_data, p(x_data), "r--", alpha=0.5)
            
            ax.set_title(title, fontweight='bold')
            ax.set_xlabel(title)
            ax.set_ylabel('PRI Score')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Relationship Between Vital Signs and PRI Scores', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        print("📊 Generated: Vital Signs vs PRI Correlation Charts")
        plt.show()
    
    def plot_classification_chart(self):
        """Plot patient classification chart"""
        # Count classifications
        classifications = [p['classification'] for p in self.sample_data]
        unique_classifications = ['Excellent', 'Good', 'Moderate', 'Poor', 'Critical']
        counts = [classifications.count(c) for c in unique_classifications]
        
        # Colors for each classification
        colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
        
        plt.figure(figsize=(10, 6))
        
        # Create bar chart
        bars = plt.bar(unique_classifications, counts, color=colors, edgecolor='black', alpha=0.8)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Patient Classification Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Classification', fontsize=12)
        plt.ylabel('Number of Patients', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add percentage labels
        total = sum(counts)
        for i, (classification, count) in enumerate(zip(unique_classifications, counts)):
            percentage = (count / total) * 100
            plt.text(i, count/2, f'{percentage:.1f}%', ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        
        print("📊 Generated: Patient Classification Distribution Chart")
        plt.show()
    
    def plot_patient_radar(self, patient_index=0):
        """Create radar chart for a specific patient"""
        patient = self.sample_data[patient_index]
        
        # Categories for radar chart
        categories = ['Heart Rate', 'Systolic BP', 'Diastolic BP', 'Respiratory Rate', 'SpO2', 'PRI']
        
        # Normalize values for radar chart (0-1 scale)
        values = [
            self.normalize(patient['vitals']['hr'], 60, 120),
            self.normalize(patient['vitals']['bp_sys'], 100, 160),
            self.normalize(patient['vitals']['bp_dia'], 60, 100),
            self.normalize(patient['vitals']['rr'], 12, 28),
            self.normalize(patient['vitals']['spo2'], 88, 100),
            patient['pri']  # PRI is already 0-1
        ]
        
        # Complete the circle
        values += values[:1]
        categories_radar = categories + [categories[0]]
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories_radar), endpoint=True).tolist()
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        ax.plot(angles, values, 'o-', linewidth=2, label=f"Patient {patient['id']}")
        ax.fill(angles, values, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        
        # Add grid
        ax.grid(True)
        
        plt.title(f'Patient {patient["id"]} - {patient["condition"]}\n'
                 f'PRI: {patient["pri"]:.3f} ({patient["classification"]})', 
                 fontsize=12, fontweight='bold', pad=20)
        
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        print(f"📊 Generated: Radar Chart for Patient {patient['id']}")
        plt.show()
    
    def normalize(self, value, min_val, max_val):
        """Normalize value to 0-1 range"""
        return (value - min_val) / (max_val - min_val)
    
    def run_all_visualizations(self):
        """Run all visualization demos"""
        print("📈 mofnet Visualization Demo")
        print("=" * 60)
        print(f"Sample Data: {len(self.sample_data)} patients")
        print()
        
        try:
            self.plot_pri_distribution()
            self.plot_vitals_vs_pri()
            self.plot_classification_chart()
            self.plot_patient_radar(patient_index=2)
            
            print("\n" + "=" * 60)
            print("✅ All visualizations completed successfully!")
            print("\nTo run specific visualizations, call:")
            print("  - plot_pri_distribution()")
            print("  - plot_vitals_vs_pri()")
            print("  - plot_classification_chart()")
            print("  - plot_patient_radar(patient_index)")
            
        except ImportError:
            print("❌ Matplotlib is not installed.")
            print("Install it with: pip install matplotlib")
            print("\nSample data is still available:")
            for i, patient in enumerate(self.sample_data[:3]):
                print(f"\nPatient {patient['id']}:")
                print(f"  Condition: {patient['condition']}")
                print(f"  PRI: {patient['pri']:.3f}")
                print(f"  Classification: {patient['classification']}")

def main():
    """Main visualization function"""
    visualizer = mofnetVisualizer()
    visualizer.run_all_visualizations()

if __name__ == "__main__":
    main()
