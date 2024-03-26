from flask import Flask, request, render_template_string, jsonify
import joblib
import pandas as pd

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar los modelos
modelo_desregulacion_emocional = joblib.load('modelo_rf_3.joblib')
modelo_casis = joblib.load('casis_logistic_regression_model.pkl')

# Preguntas para Desregulación Emocional
preguntas_desregulacion = [
    "P33. Me asusto con facilidad.",
    "P22. Estoy insatisfecho(a) con mi peso.",
    "P59. No logro mantenerme al dia con el trabajo academico.",
    "P20. Me siento inutil.",
    "P15. Confio en que puedo triunfar academicamente.",
    "P37. Tengo pensamientos indeseados que no puedo controlar.",
    "P16. Me pongo ansioso cuando tengo que hablar en publico.",
    "P11. Mi familia me altera los nervios."
]

# Preguntas para CASIS
preguntas_casis = [
    "¿Tiene preocupaciones sobre su alimentación? (Si/No)",
    "¿Tiene dificultades con el sueño? (Si/No)",
    "¿Ha asistido a consejería o psicoterapia por preocupaciones con su salud mental? (Si/No)",
    "¿Ha sentido necesidad de reducir el uso de bebidas alcohólicas u otras drogas? (Si/No)",
    "¿Ha tenido ataques de pánico o episodios de ansiedad severa? (Si/No)",
    "¿Ha considerado seriamente lastimar a otra persona? (Si/No)",
    "¿Ha tenido contactos sexuales u otras experiencias sexuales sin desearlo? (Si/No)"
]

# Página de inicio
@app.route('/')
def home():
    return """
    <h1>Bienvenido a la Evaluación</h1>
    <ul>
        <li><a href="/desregulacion">Evaluación de Desregulación Emocional</a></li>
        <li><a href="/casis">Evaluación de Riesgo de CASIS</a></li>
    </ul>
    """

# Ruta para Desregulación Emocional
@app.route('/desregulacion', methods=['GET', 'POST'])
def desregulacion():
    if request.method == 'POST':
        answers = [1 if request.form.get(f'question_{i}') == 'si' else 0 for i in range(len(preguntas_desregulacion))]
        datos_para_prediccion = pd.DataFrame([answers], columns=preguntas_desregulacion)
        prediction = modelo_desregulacion_emocional.predict(datos_para_prediccion)
        result = "Alta posibilidad de desregulación emocional." if prediction[0] == 1 else "Baja posibilidad de desregulación emocional."
        return render_template_string("""<h1>Resultado de la Evaluación</h1><p>{{ result }}</p>""", result=result)
    # Formulario de Desregulación Emocional
    formulario_html = """
    <h1>Evaluación de Desregulación Emocional</h1>
    <form method="POST">
        """ + "".join([f"""
        <label for="question_{i}">{question}</label><br>
        <input type="radio" id="si_question_{i}" name="question_{i}" value="si" required> Si<br>
        <input type="radio" id="no_question_{i}" name="question_{i}" value="no"> No<br><br>
        """ for i, question in enumerate(preguntas_desregulacion)]) + """
        <input type="submit" value="Enviar">
    </form>
    """
    return formulario_html

# Ruta para CASIS
@app.route('/casis', methods=['GET', 'POST'])
def casis():
    if request.method == 'POST':
        answers = [1 if request.form.get(f'question_{i}') == 'si' else 0 for i in range(len(preguntas_casis))]
        prediction = modelo_casis.predict([answers])
        result = "Tiene alta posibilidad de tener CASIS." if prediction[0] == 1 else "Tiene una alta posibilidad de NO tener CASIS."
        return render_template_string("""<h1>Resultado en la Evaluación de Riesgo de CASIS</h1><p>{{ result }}</p>""", result=result)
    # Formulario CASIS
    formulario_html = """
    <h1>Evaluación de Riesgo de CASIS</h1>
    <form method="POST">
        """ + "".join([f"""
        <label for="question_{i}">{question}</label><br>
        <input type="radio" id="si_question_{i}" name="question_{i}" value="si" required> Si<br>
        <input type="radio" id="no_question_{i}" name="question_{i}" value="no"> No<br><br>
        """ for i, question in enumerate(preguntas_casis)]) + """
        <input type="submit" value="Enviar">
    </form>
    """
    return formulario_html

if __name__ == '__main__':
    app.run(debug=True)
