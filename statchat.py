# Course: CSC525
# Sean Bohuslavsky

'''
Python Program 
'''

import streamlit as st
import nlp

# Set the title and caption
st.title('StatChat')
st.caption('\U0001F3C0 A NBA Statistical Chatbot')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I am StatChat. Ask me anything about NBA statistics!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    ##### Pass the user input to the NLP layer here #####
    ##### Get a response from the NLP layer here ########
    response = nlp.proc(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)