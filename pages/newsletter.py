import streamlit as st
import os
from newspaper import Article
import openai
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_main import get_rappler_href_links, generate_summary
import smtplib
import webbrowser
from email.message import EmailMessage
import tempfile
import time

try:
    st.set_page_config(layout='centered')
except Exception as e:
    st.set_page_config(layout='centered')
    
st.title("📩 Newsletter Generator")
EMAIL_ADDRESS = 'hello@markmcrg.com'
email_pass = st.secrets["EMAIL_PASSWORD"]
EMAIL_PASSWORD = email_pass

api_key = st.sidebar.text_input("API Key", type="password", key="api_key")
openai.api_base = "https://api.openai.com/v1" 
openai.api_key = api_key
model = "gpt-3.5-turbo"

user_email = st.text_input("Email Address", key="user_email", value="contact@markmcrg.com")
generate_newsletter = st.button("Generate Newsletter")

with open('newsletter_template.html', 'r') as file:
    template_content = file.read()

url = "https://www.rappler.com/nation/weather"

article_title = []
article_content = []
article_images = []
article_urls = get_rappler_href_links(url, 3)
for i, url in enumerate(article_urls):
    article = Article(url)
    article.download()
    article.parse() 
    article_title.append(article.title)
    if article.text.startswith("This is AI generated summarization"):
        article_content.append(article.text[105:])
    else:
        article_content.append(article.text)
    # article_dates.append(article.publish_date.strftime("%B %d, %Y"))
    article_images.append(article.top_image)

if generate_newsletter and user_email:
    if api_key:
        with st.spinner("Generating newsletter... This may take a while. (30 seconds to 1 minute)"):
            my_bar = st.progress(0, text="Initializing...")
            msg = EmailMessage()
            my_bar.progress(10, text="Fetching date...")
            date_today = datetime.now().strftime("%B %d, %Y")
            my_bar.progress(20, text="Setting up email...")
            msg['Subject'] = f'Daily Newsletter - {date_today}'
            msg['From'] = EMAIL_ADDRESS 
            msg['To'] = user_email
            my_bar.progress(30, text="Generating newsletter content...")
            # Replace template content
            news_category = 'WEATHER'
            template_content = template_content.replace('{{NEWS_CATEGORY}}', news_category)
            
            template_content = template_content.replace('{{ARTICLE_TITLE_1}}', article_title[0])
            template_content = template_content.replace('{{ARTICLE_TITLE_2}}', article_title[1])
            template_content = template_content.replace('{{ARTICLE_TITLE_3}}', article_title[2])        
            
            template_content = template_content.replace('{{ARTICLE_CONTENT_1}}', generate_summary(article_content[0]))
            template_content = template_content.replace('{{ARTICLE_CONTENT_2}}', generate_summary(article_content[1]))
            template_content = template_content.replace('{{ARTICLE_CONTENT_3}}', generate_summary(article_content[2]))
            
            template_content = template_content.replace('{{ARTICLE_URL_1}}', article_urls[0])
            template_content = template_content.replace('{{ARTICLE_URL_2}}', article_urls[1])
            template_content = template_content.replace('{{ARTICLE_URL_3}}', article_urls[2])
            
            template_content = template_content.replace('{{ARTICLE_IMAGE_1}}', article_images[0])
            template_content = template_content.replace('{{ARTICLE_IMAGE_2}}', article_images[1])
            template_content = template_content.replace('{{ARTICLE_IMAGE_3}}', article_images[2])
            
            template_content = template_content.replace('{{AWAS_STATE}}', 'No current weather alerts for any employee.')
            
            msg.set_content(template_content, subtype='html')
            my_bar.progress(70, text="Sending newsletter to email...")
            with smtplib.SMTP_SSL('smtp.ionos.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
                smtp.send_message(msg)
            my_bar.progress(100, text="Done!")
            st.write(f'Newsletter sent to {user_email}!')
        # with st.spinner("Opening newsletter in new tab..."):
        #     time.sleep(3)            
        # temp_html = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
        # temp_html.write(template_content)
        # temp_html.close()

        # webbrowser.open_new_tab(f'file://{temp_html.name}')
    else:
        st.error("Please enter your API key.")
else:
    st.info("Enter your email address and click the button to generate a newsletter.")
