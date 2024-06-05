from experta import *
import tkinter as tk
from tkinter import messagebox

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

class DiagnosisApp:
    def __init__(self, root):
        self.engine = DiseaseDiagnosis()

        self.root = root
        self.root.title("Sistema Experto de Diagnóstico Médico")

        # Variables de los síntomas
        self.fever = tk.StringVar(value="low")
        self.cough = tk.StringVar(value="none")
        self.fatigue = tk.StringVar(value="no")
        self.breath = tk.StringVar(value="normal")

        # Crear la interfaz
        tk.Label(root, text="Fiebre:").grid(row=0, column=0, sticky=tk.W)
        tk.OptionMenu(root, self.fever, "low", "high").grid(row=0, column=1, sticky=tk.W)

        tk.Label(root, text="Tos:").grid(row=1, column=0, sticky=tk.W)
        tk.OptionMenu(root, self.cough, "none", "dry", "wet").grid(row=1, column=1, sticky=tk.W)

        tk.Label(root, text="Fatiga:").grid(row=2, column=0, sticky=tk.W)
        tk.OptionMenu(root, self.fatigue, "no", "yes").grid(row=2, column=1, sticky=tk.W)

        tk.Label(root, text="Dificultad para respirar:").grid(row=3, column=0, sticky=tk.W)
        tk.OptionMenu(root, self.breath, "normal", "short").grid(row=3, column=1, sticky=tk.W)

        tk.Button(root, text="Diagnosticar", command=self.diagnose).grid(row=4, column=0, columnspan=2)

    def diagnose(self):
        # Obtener valores de los síntomas
        symptoms = {
            'fever': self.fever.get(),
            'cough': self.cough.get(),
            'fatigue': self.fatigue.get(),
            'breath': self.breath.get()
        }

        # Declarar los síntomas en el motor de inferencia
        self.engine.reset()
        self.engine.declare(Symptom(fever=symptoms['fever'], cough=symptoms['cough'], fatigue=symptoms['fatigue'], breath=symptoms['breath']))

        # Ejecutar el motor de inferencia
        self.engine.run()

        # Mostrar el diagnóstico
        messagebox.showinfo("Diagnóstico", f"Diagnóstico: {self.engine.diagnosis_result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisApp(root)
    root.mainloop()
