import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAIAPIKEY"])

st.title("Chef chat app")

def generate_content(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            { 'role':'system',
             'content': """
                You are a 2 star michelin star chef who wants to help home cooks 
                improve their cooking skills. You may only answer home cooking related
                questions.
                If they ask about any nonsense outside of cooking, SCOLD THEM!
                """
            },
            {
                'role':'user', 'content':prompt
            }
        ],
        n=1,
        max_tokens=150
    )
    return response.choices[0].message.content

#Initialise the chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content": "How may I help you"
        }
    ]

#Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Process and store prompts and responses
def ai_function(prompt):
    response = generate_content(prompt)

    #display the assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    #Storing the user message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": prompt
        }
    )

    #Store the assistant message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response
        }
    )

#Accept user prompts
prompt = st.chat_input("Ask me everything")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    ai_function(prompt)