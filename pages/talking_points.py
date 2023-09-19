from langchain.agents import load_tools, initialize_agent 
from langchain.chat_models import ChatOpenAI
import streamlit as st
from email.message import EmailMessage
import smtplib
import time

openai_api_key = st.secrets['openai_api_key']
serpapi_api_key = st.secrets['serpapi_key']
EMAIL_ADDRESS = 'hello@markmcrg.com'
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

st.title("🗞️ Talking Points Generator")
topic = st.text_input ("Enter your topic here")

llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.6, max_tokens=1024, model_name="gpt-3.5-turbo")

tool_names = ['serpapi']

tools = load_tools (tool_names, serpapi_api_key=serpapi_api_key)

agent = initialize_agent(tools, 
                          llm, 
                          agent='chat-zero-shot-react-description', 
                          verbose=True,
                          handle_parsing_errors=True,
                          early_stopping_method="generate")

user_email = st.text_input("Email Address", key="user_email", value="contact@markmcrg.com")
generate_button = st.button("Generate and Send Email")
# prompt = f"Please generate three categories related to the topic of {topic}. For each category, provide five bulleted talking points starting with an emoji. The talking points should focus on the most recent news and updates about {topic}. Finally, conclude with a general summary of the up-to-date information."
prompt = f"Generate five bulleted talking points starting with an emoji. The bulleted talking points should focus on the most recent news and updates about {topic}. "

if generate_button and user_email:
    with st.spinner('Generating...'):
        response = agent.run(prompt)
        st.write(response)
    with st.spinner("Sending email..."):
        msg = EmailMessage()
        msg['Subject'] = f'Talking points about {topic}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
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