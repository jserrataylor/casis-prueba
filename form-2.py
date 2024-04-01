import streamlit as st
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Debes configurar estos valores según tu servidor de correo y cuenta
SMTP_SERVER = 'smtp.tu-servidor.com'
SMTP_PORT = 587  # o 465 para SSL
SMTP_USER = 'tu-usuario'
SMTP_PASSWORD = 'tu-contraseña'

# Información de los proveedores y sus correos electrónicos
PROVEEDORES = {
    'Proveedor A': 'correoA@example.com',
    'Proveedor B': 'correoB@example.com',
    'Proveedor C': 'correoC@example.com',
}

# Función para crear el PDF
def create_pdf(form_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in form_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    return pdf.output(dest='S').encode('latin1')

# Función para enviar el correo
def send_email(subject, body, attachment, recipients):
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    
    # Cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))
    
    # Adjuntar el archivo PDF
    filename = attachment
    with open(filename, "rb") as attachment_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
    
    # Iniciar servidor SMTP y enviar correo
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

# Formulario
st.title("Formulario de Referido")

with st.form(key='referido_form'):
    nombre_estudiante = st.text_input("Nombre del estudiante:")
    telefono = st.text_input("Teléfono:")
    email = st.text_input("Email del estudiante:")
    proveedor = st.selectbox("Seleccionar Proveedor:", list(PROVEEDORES.keys()))
    nota_referido = st.text_area("Nota de referido:")
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        # Recoger los datos del formulario
        form_data = {
            "Nombre del estudiante": nombre_estudiante,
            "Teléfono": telefono,
            "Email del estudiante": email,
            "Proveedor seleccionado": proveedor,
            "Nota de referido": nota_referido
        }
        
        # Crear el PDF
        pdf_content = create_pdf(form_data)
        pdf_path = '/tmp/referido.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
        
        # Configurar destinatarios del correo y enviar
        recipients = [PROVEEDORES[proveedor], 'consejeria@example.com', email]
        send_email(
            subject="Referido de Consejería",
            body="Por favor encuentre adjunto el referido.",
            attachment=pdf_path,
            recipients=recipients
        )
        
        st.success("Referido enviado correctamente.")
