from flask import Flask, request, render_template_string, jsonify, url_for
import joblib
import streamlit as st

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar el modelo
model = joblib.load('casis_logistic_regression_model.pkl')

# Definir las preguntas
questions = [
    "¿Tiene preocupaciones sobre su alimentación? (Si/No)",
    "¿Tiene dificultades con el sueño? (Si/No)",
    "¿Ha asistido a consejería o psicoterapia por preocupaciones con su salud mental? (Si/No)",
    "¿Ha sentido necesidad de reducir el uso de bebidas alcohólicas u otras drogas? (Si/No)",
    "¿Ha tenido ataques de pánico o episodios de ansiedad severa? (Si/No)",
    "¿Ha considerado seriamente lastimar a otra persona? (Si/No)",
    "¿Ha tenido contactos sexuales u otras experiencias sexuales sin desearlo? (Si/No)"
]

# Plantilla HTML para el formulario
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cuestionario de Evaluación de Riego de CASIS</title>
</head>
<body>
    <h1>Cuestionario de Evaluación de Riego de CASIS</h1>
    <form method="POST">
        {% for i, question in questions %}
            <label for="question_{{ i }}">{{ question }}</label><br>
            <input type="radio" id="si_question_{{ i }}" name="question_{{ i }}" value="si">
            <label for="si_question_{{ i }}">Si</label><br>
            <input type="radio" id="no_question_{{ i }}" name="question_{{ i }}" value="no">
            <label for="no_question_{{ i }}">No</label><br>
        {% endfor %}
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
"""

# Plantilla HTML para la página de resultados
RESULT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Resultado en la Evaluación de Riego de CASIS</title>
</head>
<body>
    <h1>Resultado en la Evaluación de Riego de CASIS</h1>
    <p>{{ result }}</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answers = [1 if request.form.get(f'question_{i}') == 'si' else 0 for i in range(len(questions))]
        prediction = model.predict([answers])
        result = "Tiene alta posibilidad de tener CASIS." if prediction[0] == 1 else "Tiene una alta posiblidad de NO tener CASIS."
        return render_template_string(RESULT_HTML, result=result)

    questions_with_index = [(i, q) for i, q in enumerate(questions)]
    return render_template_string(INDEX_HTML, questions=questions_with_index)

if __name__ == '__main__':
    app.run(debug=True)
