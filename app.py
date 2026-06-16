import os
import streamlit as st
from google import genai 
from google.genai import types

def converter_para_gemini(historico):
    mensagens_gemini = []

    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]

        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"

        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )

    return mensagens_gemini

def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.4,
        )
    )

    return resposta.text

MODELO = "gemini-2.5-flash-lite"
INSTRUCAO_SISTEMA = """
Você é o Homem de Ferro, mais conhecido como Tony Stark, sempre que alguém lhe perguntar algo você faz o seguinte:
Dar uma resposta com uma pitada de sarcasmo, agindo como você e relacionando a resposta com acontecimentos da sua vida.
"""

st.set_page_config(page_title="Chat_Iron", page_icon="🩶")
st.title("Chatbot do Iron Man")

chave_api = st.sidebar.text_input("Digite a sua chave de API", type = "password")

if not chave_api:
    st.warning("Insira sua chave de API ns bsrrs lateral.")
    st.stop()

cliente = genai.Client(api_key=chave_api)

if "historico" not in st.session_state: #Se não existir histórico
    st.session_state.historico = []#Criar histórico

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"]) #Montando a estrutura "role":... "content":...

entrada_usuario = st.chat_input("Digite a sua pergunta: ")

if entrada_usuario: #Se existir uma pergunta
    st.session_state.historico.append({ # Adicionar a pergunta ao histórico
        "role":"user",
        "content":entrada_usuario
    })

    with st.chat_message("user"): #Adicionar a pergunta ao chat_message
        st.markdown(entrada_usuario)
    
    with st.chat_message("assistant"): #Adicionar a resposta da IA ao chat_message
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)

    st.session_state.historico.append({ # Adicionar a pergunta ao histórico
        "role":"assistant",
        "content":resposta_ia
    })
    
