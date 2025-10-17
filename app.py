import streamlit as st
import requests
from streamlit_copy_to_clipboard import st_copy_to_clipboard

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente de Prompts", page_icon="✨", layout="centered")

# --- Lógica para llamar a la API de OpenRouter ---
def generate_optimized_prompt(api_key, objetivo, tema, rol_ia, formato, audiencia, tono, contexto):
    """
    Esta función construye el meta-prompt y llama a la API de OpenRouter.
    """
    meta_prompt = f"""
    Actúa como un "Prompt Perfecter", un experto mundial en refinar y estructurar prompts para IAs generativas.
    Tu única misión es tomar los siguientes parámetros y fusionarlos en un único prompt de alta calidad.

    **Instrucciones Estrictas:**
    1.  **NO ejecutes el prompt.** Tu trabajo no es dar la respuesta al tema, sino crear la pregunta perfecta.
    2.  **Formatea la salida usando títulos claros (ej: ROL:, TAREA:, FORMATO:) y viñetas si es necesario.** Esto es crucial para la legibilidad.
    3.  **NO ofrezcas explicaciones, comentarios o texto introductorio.** Tu respuesta debe ser ÚNICAMENTE el texto del prompt final.

    **Parámetros a fusionar:**
    -   **Tarea principal:** {objetivo}
    -   **Sobre el tema:** {tema}
    -   **La IA debe actuar como:** {rol_ia}
    -   **El formato de la respuesta debe ser:** {formato}
    -   **Dirigido a una audiencia de:** {audiencia}
    -   **Con un tono:** {tono}
    -   **Contexto y restricciones adicionales:** {contexto}

    Crea un prompt claro y estructurado que un usuario pueda copiar y pegar fácilmente.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://tudominio.com", # Puedes cambiar esto por la URL de tu app
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": meta_prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            return f"Error HTTP {response.status_code}: {response.text}"

        data = response.json()
        if "error" in data:
            return f"Error de OpenRouter: {data['error'].get('message', 'Sin mensaje')}"
            
        final_prompt = data["choices"][0]["message"]["content"]
        return final_prompt

    except Exception as e:
        return f"Error interno de la aplicación: {str(e)}"

# --- Interfaz de Usuario con Streamlit ---

st.title("🤖 Asistente para Creación de Prompts")
st.write("Rellena los siguientes campos en orden para generar un prompt de alta calidad optimizado por IA.")
st.markdown("---")

# --- CAMPOS ---

objetivo = st.selectbox(
    "PASO 1: Elige el objetivo principal",
    ["Generar", "Resumir", "Traducir", "Criticar", "Explicar", "Comparar", "Crear un plan", "Escribir código", "Hacer una lluvia de ideas"]
)
tema = st.text_area(
    "PASO 2: Describe el tema principal del prompt",
    placeholder="Ej: La historia de la computación cuántica",
    height=100
)
rol_ia = st.text_input(
    "PASO 3: ¿Qué rol debe adoptar la IA?",
    placeholder="Ej: experto en ciberseguridad"
)
formato = st.selectbox(
    "PASO 4: Elige el formato de salida",
    ["Párrafo", "Lista con viñetas", "Tabla Markdown", "Código JSON", "Correo electrónico"]
)
audiencia = st.text_input(
    "PASO 5: ¿A qué audiencia se dirige?",
    placeholder="Ej: principiantes, expertos, niños"
)
tono = st.selectbox(
    "PASO 6: Elige el tono del texto",
    ["Profesional", "Conversacional", "Humorístico", "Académico", "Persuasivo"]
)
contexto = st.text_area(
    "PASO 7: Añade contexto o detalles adicionales",
    placeholder="Ej: No más de 300 palabras. Incluye ejemplos de pioneros en el campo.",
    height=150
)

st.markdown("---")

# --- BOTÓN DE GENERACIÓN ---
if st.button("✨ Generar Prompt Optimizado", type="primary", use_container_width=True):
    if not tema or not rol_ia or not audiencia:
        st.warning("Por favor, completa todos los campos de texto.")
    # Comprueba si el secret existe en Streamlit Cloud
    elif "OPENROUTER_API_KEY" not in st.secrets:
        st.error("Error: La clave API no está configurada en los 'Secrets' de la aplicación.")
    else:
        # Lee la clave desde los secrets de Streamlit
        api_key = st.secrets["OPENROUTER_API_KEY"]
        with st.spinner("Creando el prompt perfecto... por favor, espera."):
            generated_prompt = generate_optimized_prompt(
                api_key, objetivo, tema, rol_ia, formato, audiencia, tono, contexto
            )
        
        st.subheader("✅ ¡Aquí tienes tu prompt optimizado!")

        st.text_area("Prompt Generado:", value=generated_prompt, height=250, key="prompt_output")
        
        st_copy_to_clipboard(generated_prompt, key="copy_button")
        
        st.info("Copia este prompt y pégalo en tu IA favorita (ChatGPT, Claude, Gemini, etc.).")