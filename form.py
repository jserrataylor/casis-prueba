import streamlit as st
from fpdf import FPDF

# Función para crear el PDF
def create_pdf(form_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in form_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    return pdf.output(dest='S').encode('latin1')

# Función para enviar el correo
def send_email(attachment, recipients):
    # Aquí iría el código para enviar el correo electrónico.
    # Puedes usar smtplib para esto.
    pass

# Formulario
st.title("Formulario de Referido")

with st.form(key='referido_form'):
    nombre_estudiante = st.text_input("Nombre del estudiante:")
    telefono = st.text_input("Teléfono:")
    email = st.text_input("Email:")
    lista_proveedores = st.selectbox("Lista Proveedores:", ['Proveedor A', 'Proveedor B', 'Proveedor C'])
    nota_referido = st.text_area("Nota de referido:")
    
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        # Recoger los datos del formulario
        form_data = {
            "Nombre del estudiante": nombre_estudiante,
            "Teléfono": telefono,
            "Email": email,
            "Lista Proveedores": lista_proveedores,
            "Nota de referido": nota_referido
        }
        
        # Crear el PDF
        pdf = create_pdf(form_data)
        
        # Guardar el PDF en un archivo
        pdf_path = 'referido.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        # Enviar el correo
        recipients = ['proveedor@example.com', 'consejeria@example.com', email]  # Reemplaza con los correos reales
        send_email(pdf_path, recipients)
        
        st.success("Referido enviado correctamente.")
