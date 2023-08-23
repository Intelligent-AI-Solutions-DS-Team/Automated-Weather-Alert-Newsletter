import streamlit as st
import os
from newspaper import Article
import openai
from datetime import datetime
import streamlit.components.v1 as components
from helpers.get_links import get_rappler_links, get_smh_links, get_sbs_links
from streamlit_main import generate_summary
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

with open('newsletter_template2.html', 'r') as file:
    template_content = file.read()

article_title = []
article_content = []
article_images = []
news_source = st.sidebar.selectbox("**Select news source**", ("Rappler", "The Sydney Morning Herald", "Special Broadcasting Service"))
if news_source == "Rappler":
    category = st.sidebar.radio("Category", ("National", "Metro Manila", "Weather"))
elif news_source == "The Sydney Morning Herald":
    category = st.sidebar.radio("Category", ("Companies", "Market"))
elif news_source == "Special Broadcasting Service":
    category = st.sidebar.radio("Category", ("Top Stories", "Life"))
    
awas_state = "No current weather alerts for any employee."
# Number of articles to include in newsletter
n = 5
if category == "National":
    article_urls = get_rappler_links("nation", "national-news", n)
elif category == "Metro Manila":
    article_urls = get_rappler_links("nation", "metro-manila", n)
elif category == "Weather":
    article_urls = get_rappler_links("nation", "weather", n)
elif category == "Companies":
    article_urls = get_smh_links("business", "companies", n)
elif category == "Market":
    article_urls = get_smh_links("business", "market", n)
elif category == "Top Stories":
    article_urls = get_sbs_links("top-stories", n)
elif category == "Life":
    article_urls = get_sbs_links("life-articles", n)
            
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
            
            # Replace template content (title, summarized content, image, url, source)
            
            # Create placeholders for replacements
            placeholders = {
                'date_today': date_today,
                'news_category': category,
                'article_source': article_urls[0],
                'awas_state': awas_state
            }

            # Generate and add article related replacements
            for i in range(5):
                placeholders[f'article_title_{i+1}'] = article_title[i]
                placeholders[f'article_content_{i+1}'] = generate_summary(article_content[i], content="You are a news summary bot. Given the content of an article, your task is to summarize it into two short sentences.")
                placeholders[f'article_url_{i+1}'] = article_urls[i]
                placeholders[f'article_image_{i+1}'] = article_images[i]
            for placeholder, value in placeholders.items():
                template_content = template_content.replace(f'{{{placeholder}}}', value)

            # Set replaced template as email content
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
