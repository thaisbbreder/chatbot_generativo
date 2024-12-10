import streamlit as st
from openai import OpenAI

st.title("Chatbot Generativo com ChatGPT e Streamlit")

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

if "messages" not in st.session_state:
        st.session_state['messages'] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("Whats is up?"):
    instrunctions = "Responda as perguntas do usuário de maneira engracada utilizando frases e gírias como se voce fosse o Barney Stinson da série How i met your mother"
    #instrunctions = """Você é um secretário de uma clínica médica. Vocês atendem várias especialidades médicas. Interaja com o usuário e responda normalmente às perguntas dele quando ele quiser marcar uma consulta. Se o plano de saúde for Unimed, informamos que não atendemos esse plano."""

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
             model = st.session_state['openai_model'],
             messages= [
                {"role": "user", "content": prompt},
                {"role": "system", "content": instrunctions}
             ],
             stream=True,
        )
    response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

