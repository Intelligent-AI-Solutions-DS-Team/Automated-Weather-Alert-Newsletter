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

st.title("🗞️ Talking Points Generator")
topic = st.text_input ("Enter your topic here")

user_email = st.text_input("Email Address", key="user_email", value="contact@markmcrg.com")
generate_button = st.button("Generate and Send Email")
prompt = f"Please generate three categories related to the topic of {topic}. For each category, provide five bulleted talking points starting with an emoji. The talking points should focus on the most recent news and updates about {topic}. Finally, conclude with a general summary of the up-to-date information."
# prompt = f"Generate five bulleted talking points starting with an emoji. The bulleted talking points should focus on the most recent news and updates about {topic}. "

if generate_button and user_email:
    with st.spinner('Generating...'):
        sign = Login(email, passwd)
        cookies = sign.login()
        cookie_path_dir = "./cookies_snapshot"
        cookies = {"token": cookie_token, "hf-chat": cookie_hf_chat}
        chatbot = hugchat.ChatBot(cookies=cookies)

        response = chatbot.query(prompt, web_search=True)
        st.write(response)
    with st.spinner("Sending email..."):
        msg = EmailMessage()
        msg['Subject'] = f'Talking points about {topic}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        response = str(response)
        msg.set_content(response)
        for attempt in range(1, 4):
            try:
                with smtplib.SMTP_SSL('smtp.ionos.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                st.write(f'Newsletter sent to {user_email}!')
                break  # Exit loop if email is sent successfully
            except Exception as e:
                print(f"Attempt {attempt} failed: {str(e)}")
                if attempt < 3:
                    time.sleep(3)
                else:
                    st.error(f"Failed to send newsletter to {user_email}. Please try again.")