"""
Termux-Compatible Machine Learning for MOFNet
No external dependencies required
"""

import math
import random
import statistics
from collections import defaultdict
import json
import time

class SimpleLinearRegression:
    """Simple linear regression implementation"""
    
    def __init__(self):
        self.slope = 0
        self.intercept = 0
        
    def fit(self, X, y):
        """Fit linear regression model"""
        n = len(X)
        if n == 0:
            return self
            
        # Calculate means
        mean_x = sum(X) / n
        mean_y = sum(y) / n
        
        # Calculate slope (m)
        numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((X[i] - mean_x) ** 2 for i in range(n))
        
        if denominator != 0:
            self.slope = numerator / denominator
        else:
            self.slope = 0
            
        # Calculate intercept (b)
        self.intercept = mean_y - self.slope * mean_x
        
        return self
    
    def predict(self, X):
        """Predict y values"""
        if isinstance(X, (int, float)):
            return self.slope * X + self.intercept
        return [self.slope * x + self.intercept for x in X]
    
    def score(self, X, y):
        """Calculate R-squared score"""
        predictions = self.predict(X)
        ss_res = sum((y[i] - predictions[i]) ** 2 for i in range(len(X)))
        ss_tot = sum((y[i] - sum(y)/len(y)) ** 2 for i in range(len(X)))
        
        if ss_tot == 0:
            return 1.0
        return 1 - (ss_res / ss_tot)

class SimpleDecisionTree:
    """Simple decision tree for classification"""
    
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = {}
        
    def _gini(self, groups, classes):
        """Calculate Gini impurity"""
        n_instances = sum(len(group) for group in groups)
        gini = 0.0
        
        for group in groups:
            size = len(group)
            if size == 0:
                continue
                
            score = 0.0
            for class_val in classes:
                p = [row[-1] for row in group].count(class_val) / size
                score += p * p
                
            gini += (1.0 - score) * (size / n_instances)
            
        return gini
    
    def _split(self, index, value, dataset):
        """Split dataset based on index and value"""
        left, right = [], []
        for row in dataset:
            if row[index] < value:
                left.append(row)
            else:
                right.append(row)
        return left, right
    
    def _get_best_split(self, dataset):
        """Find the best split point"""
        class_values = list(set(row[-1] for row in dataset))
        b_index, b_value, b_score, b_groups = 999, 999, 999, None
        
        for index in range(len(dataset[0]) - 1):
            for row in dataset:
                groups = self._split(index, row[index], dataset)
                gini = self._gini(groups, class_values)
                
                if gini < b_score:
                    b_index, b_value, b_score, b_groups = index, row[index], gini, groups
                    
        return {'index': b_index, 'value': b_value, 'groups': b_groups}
    
    def _to_terminal(self, group):
        """Create terminal node"""
        outcomes = [row[-1] for row in group]
        return max(set(outcomes), key=outcomes.count)
    
    def _split_node(self, node, depth):
        """Recursively split node"""
        left, right = node['groups']
        del(node['groups'])
        
        if not left or not right:
            node['left'] = node['right'] = self._to_terminal(left + right)
            return
            
        if depth >= self.max_depth:
            node['left'] = self._to_terminal(left)
            node['right'] = self._to_terminal(right)
            return
            
        node['left'] = self._get_best_split(left)
        self._split_node(node['left'], depth + 1)
        
        node['right'] = self._get_best_split(right)
        self._split_node(node['right'], depth + 1)
    
    def fit(self, X, y):
        """Build decision tree"""
        dataset = [list(X[i]) + [y[i]] for i in range(len(X))]
        self.tree = self._get_best_split(dataset)
        self._split_node(self.tree, 1)
        return self
    
    def _predict_row(self, node, row):
        """Predict single row"""
        if row[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return self._predict_row(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return self._predict_row(node['right'], row)
            else:
                return node['right']
    
    def predict(self, X):
        """Make predictions"""
        if isinstance(X[0], (int, float)):
            return self._predict_row(self.tree, X)
        return [self._predict_row(self.tree, row) for row in X]

class MOFNetPredictor:
    """Main predictor for MOFNet"""
    
    def __init__(self):
        self.regression_model = SimpleLinearRegression()
        self.classification_model = SimpleDecisionTree(max_depth=3)
        self.trained = False
        
    def generate_training_data(self, n_samples=100):
        """Generate synthetic training data"""
        X = []
        y = []
        
        for _ in range(n_samples):
            # Generate random vital signs
            hr = random.randint(40, 180)
            sbp = random.randint(70, 200)
            dbp = random.randint(40, 120)
            rr = random.randint(8, 40)
            spo2 = random.randint(75, 100)
            
            # Calculate risk score (simplified)
            risk = 0
            if hr < 60 or hr > 100: risk += 0.2
            if sbp < 90 or sbp > 140: risk += 0.2
            if spo2 < 92: risk += 0.3
            if rr < 12 or rr > 20: risk += 0.2
            
            # Classification (0=Low, 1=Medium, 2=High)
            if risk < 0.3:
                cls = 0
            elif risk < 0.6:
                cls = 1
            else:
                cls = 2
                
            X.append([hr, sbp, dbp, rr, spo2])
            y.append(cls)
            
        return X, y
    
    def train(self):
        """Train the models"""
        X, y = self.generate_training_data(50)
        
        # Train regression model (predict risk score)
        y_reg = [sum(x)/len(x)/100 for x in X]  # Simple risk score
        self.regression_model.fit([x[0] for x in X], y_reg)  # Using HR only for simplicity
        
        # Train classification model
        self.classification_model.fit(X, y)
        
        self.trained = True
        return True
    
    def predict_risk(self, vitals):
        """Predict risk for given vitals"""
        if not self.trained:
            self.train()
            
        # Extract features
        features = [
            vitals.get('heart_rate', 72),
            vitals.get('sbp', 120),
            vitals.get('dbp', 80),
            vitals.get('rr', 16),
            vitals.get('spo2', 98)
        ]
        
        # Get classification
        classification = self.classification_model.predict([features])[0]
        
        # Get regression prediction
        regression_score = self.regression_model.predict(features[0])
        
        # Map to risk levels
        risk_levels = ['Low', 'Medium', 'High', 'Critical']
        level = risk_levels[min(classification, 3)]
        
        return {
            'risk_level': level,
            'risk_score': float(regression_score),
            'classification': int(classification),
            'organ_scores': self._calculate_organ_scores(vitals),
            'confidence': random.uniform(0.7, 0.95)  # Simulated confidence
        }
    
    def _calculate_organ_scores(self, vitals):
        """Calculate individual organ risk scores"""
        scores = {}
        
        # Cardiac risk
        hr = vitals.get('heart_rate', 72)
        sbp = vitals.get('sbp', 120)
        cardiac_risk = 0
        if hr < 60 or hr > 100: cardiac_risk += 0.5
        if sbp < 90 or sbp > 140: cardiac_risk += 0.5
        scores['cardiac'] = min(cardiac_risk, 1.0)
        
        # Respiratory risk
        rr = vitals.get('rr', 16)
        spo2 = vitals.get('spo2', 98)
        resp_risk = 0
        if rr < 12 or rr > 20: resp_risk += 0.5
        if spo2 < 95: resp_risk += 0.5
        scores['respiratory'] = min(resp_risk, 1.0)
        
        # Renal risk (simulated)
        scores['renal'] = random.uniform(0.1, 0.4)
        
        # Hepatic risk (simulated)
        scores['hepatic'] = random.uniform(0.1, 0.3)
        
        return scores
    
    def save_model(self, filename='mofnet_model.json'):
        """Save model to file"""
        model_data = {
            'trained': self.trained,
            'regression': {
                'slope': self.regression_model.slope,
                'intercept': self.regression_model.intercept
            },
            'timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(model_data, f)
        
        return True
    
    def load_model(self, filename='mofnet_model.json'):
        """Load model from file"""
        try:
            with open(filename, 'r') as f:
                model_data = json.load(f)
            
            self.trained = model_data.get('trained', False)
            reg_data = model_data.get('regression', {})
            self.regression_model.slope = reg_data.get('slope', 0)
            self.regression_model.intercept = reg_data.get('intercept', 0)
            
            return True
        except:
            return False

# Test the module
if __name__ == "__main__":
    print("Testing Termux ML Module...")
    
    # Create predictor
    predictor = MOFNetPredictor()
    
    # Train
    print("Training model...")
    predictor.train()
    
    # Test prediction
    test_vitals = {
        'heart_rate': 110,
        'sbp': 150,
        'dbp': 95,
        'rr': 22,
        'spo2': 92
    }
    
    result = predictor.predict_risk(test_vitals)
    print(f"\nPrediction Results:")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']:.3f}")
    print(f"Organ Scores: {result['organ_scores']}")
    
    # Save model
    predictor.save_model()
    print("\nModel saved successfully!")
