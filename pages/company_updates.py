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

prompt = f"""For the company named {company_name}

🏢 Provide an introductory description of {company_name}.

📰 For {company_name}, find the 5 most recent news articles within the last 3 months. For each article, include a summary, the publication date, and the URL source.

🌐 For the industry related to {company_name}, find the 5 most recent news articles within the last 3 months. For each article, provide a summary, the publication date, and the URL source.

🔗 List all your sources with their URLs and display them in the results so that the reader can click on the URL for the full news.

Begin each bullet point with a distinct emoji, and present the information directly as requested."""


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