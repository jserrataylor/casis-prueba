from flask import Flask, request, render_template_string
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar los modelos
modelo_desregulacion_emocional = joblib.load('modelo_rf_3.joblib')
modelo_casis = joblib.load('casis_logistic_regression_model.pkl')

# Preguntas Desregulación Emocional
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

# Preguntas CASIS
preguntas_casis = [
    "¿Tiene preocupaciones sobre su alimentación? (Si/No)",
    "¿Tiene dificultades con el sueño? (Si/No)",
    "¿Ha asistido a consejería o psicoterapia por preocupaciones con su salud mental? (Si/No)",
    "¿Ha sentido necesidad de reducir el uso de bebidas alcohólicas u otras drogas? (Si/No)",
    "¿Ha tenido ataques de pánico o episodios de ansiedad severa? (Si/No)",
    "¿Ha considerado seriamente lastimar a otra persona? (Si/No)",
    "¿Ha tenido contactos sexuales u otras experiencias sexuales sin desearlo? (Si/No)"
]

# Combinar las preguntas de ambos cuestionarios
preguntas_combinadas = preguntas_desregulacion + preguntas_casis

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion_combinada():
    if request.method == 'POST':
        # Extraer respuestas y asignarlas a cada modelo
        respuestas = [1 if request.form.get(f'question_{i}') == 'si' else 0 for i in range(len(preguntas_combinadas))]
        respuestas_desregulacion = respuestas[:len(preguntas_desregulacion)]
        respuestas_casis = respuestas[len(preguntas_desregulacion):]
        
        # Realizar predicciones
        datos_desregulacion = pd.DataFrame([respuestas_desregulacion], columns=preguntas_desregulacion)
        prediccion_desregulacion = modelo_desregulacion_emocional.predict(datos_desregulacion)
        
        datos_casis = pd.DataFrame([respuestas_casis], columns=preguntas_casis)
        prediccion_casis = modelo_casis.predict(datos_casis)
        
        # Interpretar resultados
        resultado_desregulacion = "Alta posibilidad de desregulación emocional." if prediccion_desregulacion[0] == 1 else "Baja posibilidad de desregulación emocional."
        resultado_casis = "Tiene alta posibilidad de tener CASIS." if prediccion_casis[0] == 1 else "Tiene una alta posibilidad de NO tener CASIS."
        resultado_combinado = f"{resultado_desregulacion}<br>{resultado_casis}"
        
        return render_template_string("<h1>Resultados de la Evaluación Combinada</h1><p>{{ resultado }}</p>", resultado=resultado_combinado)
    
    # Formulario combinado
    formulario_html = """
    <h1>Evaluación Combinada</h1>
    <form method="POST">
    """ + "".join([f"""
    <label>{q}</label><br>
    <input type="radio" name="question_{i}" value="si" required> Si<br>
    <input type="radio" name="question_{i}" value="no"> No<br><br>
    """ for i, q in enumerate(preguntas_combinadas)]) + """
    <input type="submit" value="Enviar">
    </form>
    """
    
    return formulario_html

if __name__ == '__main__':
    app.run(debug=True)
