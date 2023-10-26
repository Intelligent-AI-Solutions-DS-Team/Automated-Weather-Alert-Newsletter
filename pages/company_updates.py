import streamlit as st
from email.message import EmailMessage
from hugchat import hugchat
from hugchat.login import Login
import smtplib
import time

openai_api_key = st.secrets['openai_api_key']

# secrets.toml
EMAIL_ADDRESS = 'hello@markmcrg.com'
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

passwd = st.secrets['huggingface_password']
email = 'contact@markmcrg.com'

cookie_token = st.secrets['cookie_token']
cookie_hf_chat = st.secrets['cookie_hf_chat']

st.set_page_config(page_title="Company Updates", page_icon=":bar_chart:")
st.title("📊 Company Updates")
company_name = st.text_input ("Enter company name here")

generate_button = st.button("Generate Updates")

prompt = f""""For the company named {company_name}

Give me an introductory description of the company. 

Give me also the 5 pieces of latest news regarding the company, each with a summary.

Give me also the 5 pieces of latest news regarding the industry related to the company, each with a summary as well.

Each bullet point in your answer should begin with an emoji, and no need to talk to me as if I prompted you. Just give me the answer as I've instructed so."""

# prompt = f"Generate five bulleted talking points starting with an emoji. The bulleted talking points should focus on the most recent news and updates about {topic}. "

if generate_button:
    with st.spinner('Generating...'):
        sign = Login(email, passwd)
        cookies = sign.login()
        cookies = {"token": cookie_token, "hf-chat": cookie_hf_chat}
        chatbot = hugchat.ChatBot(cookies=cookies)

        response = chatbot.query(prompt, web_search=True)
        # convert response to string
        response = str(response)
        st.write(response)