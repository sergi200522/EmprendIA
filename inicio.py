import streamlit as st
import google.generativeai as genai

# Configuración básica de la app
st.set_page_config(page_title="EmprendIA - Generador de Facturas", page_icon="🧾", layout="centered")

st.title("🧾 EmprendIA: Generador de Facturas y Cotizaciones")
st.caption("De la idea a tu primera venta digital con Inteligencia Artificial")

# 1. Configuración de Gemini API
# Reemplaza "TU_API_KEY" con tu clave real de Google AI Studio
API_KEY = "TU_API_KEY"
genai.configure(api_key=API_KEY)

st.subheader("1. Datos Generales del Cliente y Servicio")

# Formulario en dos columnas
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nombre del Cliente / Empresa", placeholder="Ej. Comercializadora Lopez")
with col2:
    servicio = st.text_input("Descripción del Servicio / Producto", placeholder="Ej. Limpieza profunda de salas y tapetes")

col3, col4 = st.columns(2)
with col3:
    cantidad = st.number_input("Cantidad", min_value=1, value=1, step=1)
with col4:
    precio_unitario = st.number_input("Precio Unitario ($ MXN)", min_value=0.0, value=0.0, format="%.2f")

# 2. Lógica Financiera en Python
subtotal = cantidad * precio_unitario
iva = subtotal * 0.16
total = subtotal + iva

# Mostrar desglose financiero rápido
if subtotal > 0:
    st.markdown("---")
    st.subheader("2. Desglose de Montos")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Subtotal", f"${subtotal:,.2f}")
    m_col2.metric("IVA (16%)", f"${iva:,.2f}")
    m_col3.metric("Total a Pagar", f"${total:,.2f}")

st.markdown("---")

# 3. Generación con IA
if st.button("🚀 Generar Factura / Cotización con IA", use_container_width=True):
    if cliente and servicio and subtotal > 0:
        with st.spinner("Conectando con Gemini para redactar las condiciones comerciales..."):
            try:
                # Consulta a la API de Gemini
                prompt = (
                    f"Redacta un párrafo profesional y amable para incluir al final de una cotización/factura "
                    f"dirigida al cliente '{cliente}' por el servicio/producto '{servicio}'. "
                    f"Incluye un agradecimiento, políticas de pago (50% anticipo y 50% al entregar) y "
                    f"vigencia de 7 días naturales. Sé breve, formal y persuasivo."
                )
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                respuesta = model.generate_content(prompt)
                texto_ia = respuesta.text

                # Mostrar Documento Estilizado
                st.success("¡Documento generado exitosamente!")
                
                st.markdown("---")
                st.markdown(f"## 📄 Cotización / Factura Digital")
                st.markdown(f"*Cliente:* {cliente}")
                st.markdown(f"*Concepto:* {servicio} (x{cantidad})")
                st.markdown(f"*Monto Subtotal:* ${subtotal:,.2f} MXN")
                st.markdown(f"*IVA (16%):* ${iva:,.2f} MXN")
                st.markdown(f"### *Total Final:* ${total:,.2f} MXN")
                st.markdown("---")
                
                st.info(f"💡 *Términos y Notas Comerciales (IA):*\n\n{texto_ia}")

            except Exception as e:
                st.error(f"Error al conectar con la API de Gemini: {e}")
    else:
        st.warning("⚠️ Por favor completa el nombre del cliente, la descripción del servicio y un monto mayor a $0.")
