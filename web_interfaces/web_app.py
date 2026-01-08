from flask import Flask, render_template_string, request
import mofnet

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🏥 MOFNet Clinical Analyzer</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #2c3e50; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #3498db; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
        .result { background: #ecf0f1; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .good { color: #27ae60; }
        .warning { color: #f39c12; }
        .danger { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 MOFNet Clinical Analyzer</h1>
        
        <form method="post">
            <h3>Patient Vitals:</h3>
            
            <label>Heart Rate (bpm):</label>
            <input type="number" name="hr" value="80" min="40" max="200" required>
            
            <label>Systolic BP (mmHg):</label>
            <input type="number" name="sbp" value="120" min="60" max="250" required>
            
            <label>Diastolic BP (mmHg):</label>
            <input type="number" name="dbp" value="80" min="40" max="150" required>
            
            <label>Respiratory Rate (breaths/min):</label>
            <input type="number" name="rr" value="16" min="8" max="40" required>
            
            <label>Oxygen Saturation (%):</label>
            <input type="number" name="spo2" value="98" min="75" max="100" required>
            
            <br><br>
            <button type="submit">🔬 Analyze Patient</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h3>📊 Analysis Results:</h3>
            <p><strong>PRI Score:</strong> {{ result.pri|round(3) }}</p>
            <p><strong>Classification:</strong> 
                <span class="
                    {% if result.classification == 'Excellent' %}good
                    {% elif result.classification == 'Good' %}good
                    {% elif result.classification == 'Moderate' %}warning
                    {% else %}danger{% endif %}
                ">
                    {{ result.classification }}
                </span>
            </p>
            
            <h4>🤖 AI Risk Prediction:</h4>
            <p><strong>Risk Level:</strong> {{ result.risk_level }}</p>
            <p><strong>Risk Score:</strong> {{ result.risk_score|round(3) }}</p>
            
            <h4>🏥 Organ Risks:</h4>
            <ul>
                {% for organ, score in result.organ_scores.items() %}
                <li>{{ organ|title }}: {{ "%.2f"|format(score) }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <hr>
        <p><small>MOFNet v{{ version }} | Runs on Termux</small></p>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    
    if request.method == 'POST':
        # Get form data
        hr = int(request.form['hr'])
        sbp = int(request.form['sbp'])
        dbp = int(request.form['dbp'])
        rr = int(request.form['rr'])
        spo2 = int(request.form['spo2'])
        
        # Calculate PRI
        pri = mofnet.calculate_pri(hr, sbp, dbp, rr, spo2)
        classification = mofnet.classify_pri_level(pri)
        
        # Get AI prediction
        predictor = mofnet.MOFNetPredictor()
        predictor.train()
        risk_prediction = predictor.predict_risk({
            'heart_rate': hr,
            'sbp': sbp,
            'dbp': dbp,
            'rr': rr,
            'spo2': spo2
        })
        
        result = {
            'pri': pri,
            'classification': classification,
            'risk_level': risk_prediction['risk_level'],
            'risk_score': risk_prediction['risk_score'],
            'organ_scores': risk_prediction['organ_scores']
        }
    
    return render_template_string(
        HTML_TEMPLATE, 
        result=result,
        version=mofnet.__version__
    )

if __name__ == '__main__':
    print("🚀 MOFNet Web App starting...")
    print("🌐 Open: http://localhost:5000")
    print("📱 Works on Termux!")
    app.run(host='0.0.0.0', port=5000, debug=True)
