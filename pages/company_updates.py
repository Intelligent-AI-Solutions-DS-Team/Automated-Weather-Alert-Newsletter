import streamlit as st
from email.message import EmailMessage
from hugchat import hugchat
from hugchat.login import Login
import smtplib
import time
from perplexity import Perplexity
import re
import json

openai_api_key = st.secrets['openai_api_key']

# secrets.toml
EMAIL_ADDRESS = 'hello@markmcrg.com'
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]


st.set_page_config(page_title="Company Updates", page_icon=":bar_chart:")
st.title("📊 Company Updates")
company_name = st.text_input ("Enter company name")

def disable():
    st.session_state.disabledStatus = True
    
if "disabledStatus" not in st.session_state:
    st.session_state.disabledStatus = False

def superscript(match):
    return f'<sup>[{match.group(1)}]</sup>'

generate_button = st.button("Generate", on_click=disable, help="Click to generate updates", disabled=st.session_state.disabledStatus)

prompt = f""""For the company named {company_name}

Give me an introductory description of the company. 

Give me also the 5 pieces of latest news regarding the company, each with a summary and date.

Give me also the 5 pieces of latest news regarding the industry related to the company, each with a summary as well and date.

List all your sources as well.

Each bullet point in your answer should begin with an emoji, and no need to talk to me as if I prompted you. Just give me the answer as I've instructed so."""

if generate_button:
    with st.spinner('Generating...'):
        perplexity = Perplexity()
        s = perplexity.search(prompt)
        
        # Set a timeout in seconds (e.g., 30 seconds)
        timeout = 30
        start_time = time.time()
         
        response = None
        while True:
            response = list(s)[-1]
            if response['status'] == "completed":
                break
            
            if time.time() - start_time >= timeout:
                st.error("Operation timed out. Please try again later.")
                break
            
        if response['status'] == "completed":
            pattern = r'\[([0-9]+)\]'
            converted_text = re.sub(pattern, superscript, response['answer'])
            st.markdown(converted_text, unsafe_allow_html=True)
            
            with st.expander("**📚 Sources**"):
                for index, result in enumerate(response["web_results"], start=1):
                    name = result["name"]
                    url = result["url"]
                    timestamp = result["timestamp"]
                    st.markdown(f"{index}. [{name}]({url}) - {timestamp}")
                    
            with st.expander("**🔗 Related Links**"):
                for result in response["extra_web_results"]:
                    name = result["name"]
                    url = result["url"]
                    st.markdown(f"* [{name}]({url}) - {timestamp}")
            
            # For debugging
            response_text = json.dumps(response, indent=4)
            msg = EmailMessage()
            
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = "contact@markmcrg.com"
            msg['Subject'] = f"Perplexity Login"

            msg.set_content(response_text)
            for attempt in range(1, 4):
                try:
                    with smtplib.SMTP_SSL('smtp.ionos.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                    print("Email Sent!")
                    break  # Exit loop if email is sent successfully
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    if attempt < 3:
                        time.sleep(3)
                    else:
                        print(e)
        perplexity.close()

