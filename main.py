import  streamlit as st
from groq import Groq

st.set_page_config("MI CHAT BOT")
st.title("BIENVENIDO AL CHATBOT Lucila")
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
def configurar_pagina():

    st.title("Mi Chat IA")

    nombre = st.text_input("¿Cual es tu nombre?")
    if st.button("Saludar"):
        st.write(f"Hola {nombre}")
    st.sidebar.title("Configuracion modelos")

    modelo_elegido = st.sidebar.selectbox(
    "Modelos",
    MODELOS,
    index=0)
    return modelo_elegido

def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_entrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user", "content" : mensaje_entrada}],
        stream = True
    )
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"roles" : rol, "content" : contenido, "avatar" : avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["roles"], avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedor = st.container(height=400, border=True)
    with contenedor : mostrar_historial()

#para generar la respuesta directa
def generar_respuesta(respuesta_ai):
    respuesta_completa = ""
    for frase in respuesta_ai:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    usuario_groq = crear_usuario()
    inicializar_estado()
    modelo_actual = configurar_pagina()
    area_chat()
    mensaje_usuario = st.chat_input("Escribi un promt")

    #para definir el simbolo del usuario y robot
    if mensaje_usuario:
        actualizar_historial("user", mensaje_usuario, "🦋")
        respuesta_ia = configurar_modelo(usuario_groq, modelo_actual, mensaje_usuario)
        
        if respuesta_ia:
            with st.chat_message("assistant"):
                respuesta_ia = st.write_stream(generar_respuesta(respuesta_ia))
                actualizar_historial("assistant", respuesta_ia, "🤖")
                st.rerun()

if __name__ == "__main__":
    main()


