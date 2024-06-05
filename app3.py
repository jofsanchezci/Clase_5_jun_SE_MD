from experta import *
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

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

class DiagnosisApp(App):
    def build(self):
        self.engine = DiseaseDiagnosis()

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Crear widgets
        self.fever_label = Label(text='Fiebre:')
        self.fever_spinner = Spinner(text='low', values=('low', 'high'))

        self.cough_label = Label(text='Tos:')
        self.cough_spinner = Spinner(text='none', values=('none', 'dry', 'wet'))

        self.fatigue_label = Label(text='Fatiga:')
        self.fatigue_spinner = Spinner(text='no', values=('no', 'yes'))

        self.breath_label = Label(text='Dificultad para respirar:')
        self.breath_spinner = Spinner(text='normal', values=('normal', 'short'))

        self.diagnose_button = Button(text='Diagnosticar', on_press=self.diagnose)

        # Añadir widgets al layout
        self.root.add_widget(self.fever_label)
        self.root.add_widget(self.fever_spinner)
        self.root.add_widget(self.cough_label)
        self.root.add_widget(self.cough_spinner)
        self.root.add_widget(self.fatigue_label)
        self.root.add_widget(self.fatigue_spinner)
        self.root.add_widget(self.breath_label)
        self.root.add_widget(self.breath_spinner)
        self.root.add_widget(self.diagnose_button)

        return self.root

    def diagnose(self, instance):
        # Obtener valores de los síntomas
        symptoms = {
            'fever': self.fever_spinner.text,
            'cough': self.cough_spinner.text,
            'fatigue': self.fatigue_spinner.text,
            'breath': self.breath_spinner.text
        }

        # Declarar los síntomas en el motor de inferencia
        self.engine.reset()
        self.engine.declare(Symptom(fever=symptoms['fever'], cough=symptoms['cough'], fatigue=symptoms['fatigue'], breath=symptoms['breath']))

        # Ejecutar el motor de inferencia
        self.engine.run()

        # Mostrar el diagnóstico
        popup = Popup(title='Diagnóstico',
                      content=Label(text=f'Diagnóstico: {self.engine.diagnosis_result}'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    DiagnosisApp().run()
