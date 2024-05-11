import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd
import google.generativeai as genai
import time
import os
from PIL import Image

dashboard_location = os.path.dirname(__file__)

duck = Image.open(dashboard_location + '/pato_icon.png')
question = Image.open(dashboard_location + '/question_icon.png')

# Carregar a chave secreta da variável de ambiente
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "candidate_count": 1,
    "temperature": 0
}

safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

col1, col2 = st.columns([1, 3])

with col1:
   st.image('pato_detetive_1.png', width=150)

with col2:
  st.title('Pato Check')
  st.caption('Bem-vindo ao Pato Check! O único lugar onde você descobre que algumas histórias são mais falsas do que o bronzeado de um pinguim na Antártida! Se você já foi enganado por uma notícia absurda, não se preocupe, acontece nas melhores famílias. Mas agora você não será mais enganado, o Pato chegou para te ajudar a descobrir a verdade de forma rápida e sem enrolação.')


model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config = generation_config,
                              safety_settings = safety_settings)
                              
                    
chat = model.start_chat(history=[])


prompt = st.chat_input("O que você quer saber se é uma fake news?")
if prompt:
  with st.chat_message("user", avatar=np.array(question)):
      st.write(prompt)

  with st.spinner("Aguarde um momento que o Pato vai checar..."):
    
    response = chat.send_message(prompt)
    fontes = chat.send_message("Quais fontes do " + str(response) + "?")
    resposta_sim_nao = str(response.text)[:3].lower()
    time.sleep(2)

    if resposta_sim_nao == "sim" or resposta_sim_nao == "nao" or resposta_sim_nao == "não":
      resposta = "Resposta: " + response.text + "\n" + "Fontes: " + fontes.text + "\n"
      with st.chat_message("assistant", avatar=np.array(duck)):
        st.write("Resposta: ", response.text, "\n")
        st.write("Fontes: ", fontes.text, "\n")
    else:
      with st.chat_message("assistant", avatar=np.array(duck)):
        st.write("Sua pergunta não é válida, faça uma pergunta que o Pato consiga responder com SIM ou NÃO sobre Fake News, por favor :)", "\n")


