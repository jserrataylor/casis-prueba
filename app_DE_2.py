from flask import Flask, request, render_template_string
import joblib
import pandas as pd

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar el modelo
model = joblib.load('modelo_ajustado_rf_2.joblib')

# Definir las preguntas
preguntas = [
    "P33. Me asusto con facilidad.",
#    "P19. Estoy satisfecho(a) con mi apariencia fisica.",
    "P22. Estoy insatisfecho(a) con mi peso.",
    "P59. No logro mantenerme al dia con el trabajo academico.",
    "P20. Me siento inutil.",
    "P15. Confio en que puedo triunfar academicamente.",
    "P37. Tengo pensamientos indeseados que no puedo controlar.",
    "P16. Me pongo ansioso cuando tengo que hablar en publico.",
    "P11. Mi familia me altera los nervios.",
#    "P30. Me siento tenso(a)."
]

# Plantilla HTML para el formulario
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cuestionario de Evaluación de Desregulación Emocional</title>
</head>
<body>
    <h1>Cuestionario de Evaluación de Desregulación Emocional</h1>
    <form method="POST">
        {% for i, question in questions %}
            <label for="question_{{ i }}">{{ question }}</label><br>
            <input type="radio" id="si_question_{{ i }}" name="question_{{ i }}" value="si" required>
            <label for="si_question_{{ i }}">Si</label><br>
            <input type="radio" id="no_question_{{ i }}" name="question_{{ i }}" value="no">
            <label for="no_question_{{ i }}">No</label><br><br>
        {% endfor %}
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answers = [1 if request.form.get(f'question_{i}') == 'si' else 0 for i in range(len(preguntas))]
        datos_para_prediccion = pd.DataFrame([answers], columns=preguntas)
        prediction = model.predict(datos_para_prediccion)
        result = "Alta posibilidad de desregulación emocional." if prediction[0] == 1 else "Baja posibilidad de desregulación emocional."
        return render_template_string("""<!DOCTYPE html><html><head><title>Resultado</title></head><body><h1>Resultado de la Evaluación</h1><p>{{ result }}</p></body></html>""", result=result)
    return render_template_string(INDEX_HTML, questions=enumerate(preguntas))

if __name__ == '__main__':
    app.run(debug=True)
