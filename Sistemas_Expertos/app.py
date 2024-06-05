from flask import Flask, render_template, request, jsonify
from experta import *

class Symptom(Fact):
    """Información sobre los síntomas del paciente"""
    pass

class DiseaseDiagnosis(KnowledgeEngine):
    @Rule(Symptom(fever='high', cough='dry', fatigue='yes', breath='short'))
    def covid19(self):
        self.declare(Fact(disease='COVID-19'))
    
    @Rule(Symptom(fever='high', cough='wet', fatigue='yes', breath='normal'))
    def flu(self):
        self.declare(Fact(disease='Flu'))
    
    @Rule(Symptom(fever='low', cough='none', fatigue='no', breath='normal'))
    def healthy(self):
        self.declare(Fact(disease='Healthy'))
    
    @Rule(Fact(disease=MATCH.disease))
    def diagnosis(self, disease):
        self.diagnosis_result = disease

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptoms = request.json
    engine = DiseaseDiagnosis()
    engine.reset()
    engine.declare(Symptom(fever=symptoms['fever'], cough=symptoms['cough'], fatigue=symptoms['fatigue'], breath=symptoms['breath']))
    engine.run()
    return jsonify({'diagnosis': engine.diagnosis_result})

if __name__ == '__main__':
    app.run(debug=True)
