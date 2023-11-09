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

prompt = f"""
Using only existing and verifiable sources, please do the following for a company named {company_name}:

1. Provide an introductory description of {company_name}, drawing from current, credible sources.

2. Search for and list the five most recent verifiable news articles about {company_name} that were published in the last six months. For each article, provide:
   - A summary (ensure that the content of the summary is drawn from the article and not generated).
   - The publication date (confirm this date is accurate according to the source).
   - The direct URL to the full article (verify that the URL leads to the actual article).

3. Similarly, find the five most recent, verifiable news articles about the industry related to {company_name}, published within the last six months. For each, include:
   - A summary (summarize the actual content of the article).
   - The publication date (make sure the date matches the source).
   - The direct URL to the full article (check that the URL is correct and the link is live).

Please ensure:
   - Each bullet point starts with a unique emoji.
   - The information provided is accurate and verifiable.
   - You do not invent or include any speculative information.
   - All URLs provided are live and lead to real, credible sources.

If you are unable to verify the information or find real articles, please state so clearly.
"""


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