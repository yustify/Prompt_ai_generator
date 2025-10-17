import streamlit as st
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Prompt Generator", page_icon="🧠", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    .stApp > header {
        background-color: transparent;
    }
    .stSelectbox > label,
    .stTextArea > label,
    .stTextInput > label {
        font-weight: 700;
    }
    h1 {
        color: #1E3A8A;
        text-align: center;
        font-size: 3.5em;
        font-weight: 700;
        padding-top: 1rem;
    }
    .st-emotion-cache-cnjvw8 p {
        text-align: center;
        font-size: 1.2em;
        color: #555;
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8C4B 100%);
        color: white;
        padding: 0.8em 1.5em;
        border-radius: 25px;
        font-size: 1.2em;
        font-weight: 700;
        box-shadow: 0 4px 14px 0 rgba(255, 75, 75, 0.39);
        transition: all 0.3s ease-in-out;
        border: none;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px 0 rgba(255, 75, 75, 0.5);
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    #prompt_output textarea {
        background-color: #282c34;
        color: #abb2bf;
        border: 2px solid #FF4B4B;
        border-radius: 10px;
        padding: 1em;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.1em;
        height: 300px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE LA API ---
def generate_optimized_prompt(api_key, objetivo, tema, rol_ia, formato, audiencia, tono, contexto):
    
    # Lógica de generación del prompt del bot de Telegram
    meta_prompt = f"""
    Actúa como un experto mundial en ingeniería de prompts.
    Tu tarea es construir un único prompt detallado y de alta calidad, listo para usar en otra IA generativa.

    Parámetros:
    - Objetivo: {objetivo}
    - Tema: {tema}
    - Rol: {rol_ia}
    - Formato: {formato}
    - Audiencia: {audiencia}
    - Tono: {tono}
    - Contexto adicional: {contexto}

    Devuelve solo el prompt optimizado, sin explicaciones adicionales.
    """
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "HTTP-Referer": "https://tudominio.com"}
    payload = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": meta_prompt}], "max_tokens": 1024, "temperature": 0.7}

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
        if response.status_code != 200: return f"Error HTTP {response.status_code}: {response.text}"
        data = response.json()
        if "error" in data: return f"Error de OpenRouter: {data['error'].get('message', 'Sin mensaje')}"
        final_prompt = data["choices"][0]["message"]["content"]
        return final_prompt.strip()
    except Exception as e:
        return f"Error interno de la aplicación: {str(e)}"

# --- ÁREA DE CONTENIDO PRINCIPAL ---
st.title("🧠 Prompt Generator")
st.write("Crea prompts de alta calidad para cualquier IA en segundos. Rellena los siguientes campos y genera tu prompt.")

with st.container(border=True):
    st.subheader("Configura los Parámetros de tu Prompt")
    
    col1, col2 = st.columns(2)

    with col1:
        objetivo = st.selectbox("🎯 Objetivo", ["Generar", "Resumir", "Traducir", "Criticar", "Explicar", "Comparar", "Crear un plan", "Escribir código", "Hacer una lluvia de ideas"])
        tema = st.text_area("📚 Tema principal", placeholder="Ej: La historia de la computación cuántica")
        rol_ia = st.text_input("🤖 Rol / Personalidad de la IA", placeholder="Ej: experto en ciberseguridad")

    with col2:
        formato = st.selectbox("📜 Formato de salida", ["Párrafo", "Lista con viñetas", "Tabla Markdown", "Código JSON", "Correo electrónico"])
        tono = st.selectbox("🎨 Tono del texto", ["Profesional", "Conversacional", "Humorístico", "Académico", "Persuasivo"])
        audiencia = st.text_input("👥 Dirigido a la audiencia", placeholder="Ej: principiantes, expertos, niños")
        
    contexto = st.text_area("🗒️ Contexto y detalles adicionales", placeholder="Ej: No más de 300 palabras. Incluye ejemplos.")

st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("✨ Generar Prompt Optimizado", use_container_width=True):
        if not tema or not rol_ia or not audiencia:
            st.warning("Por favor, completa todos los campos de texto.")
        # Lógica para leer desde los secrets de Streamlit
        elif "OPENROUTER_API_KEY" not in st.secrets:
            st.error("Error: La clave API no está configurada en los 'Secrets' de la aplicación.")
        else:
            api_key = st.secrets["OPENROUTER_API_KEY"]
            with st.spinner("Creando el prompt perfecto... por favor, espera."):
                generated_prompt = generate_optimized_prompt(api_key, objetivo, tema, rol_ia, formato, audiencia, tono, contexto)
            st.session_state.generated_prompt = generated_prompt

if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
    st.markdown("---")
    st.subheader("✅ ¡Aquí tienes tu prompt optimizado!")
    
    st.text_area(
        label="Prompt Generado:",
        value=st.session_state.generated_prompt,
        height=300,
        key="prompt_output"
    )
    
    st.info("Selecciona y copia el prompt de la caja de texto superior.")