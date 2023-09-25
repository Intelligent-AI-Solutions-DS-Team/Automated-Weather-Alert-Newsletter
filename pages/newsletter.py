import streamlit as st
import os
from newspaper import Article
import openai
from datetime import datetime
import streamlit.components.v1 as components
from helpers.get_links import get_article_urls
from streamlit_main import generate_summary
import smtplib
import webbrowser
from email.message import EmailMessage
import tempfile
import time
from pages.weatherAlerts import get_cities_data, get_coordinates, fetch_weather_alerts, determine_status_and_description, load_data

st.title("📩 Newsletter Generator")
EMAIL_ADDRESS = 'hello@markmcrg.com'
email_pass = st.secrets["EMAIL_PASSWORD"]
EMAIL_PASSWORD = email_pass

# api_key = st.sidebar.text_input("API Key", type="password", key="api_key")
openai.api_base = "https://api.openai.com/v1" 
api_key = st.secrets["openai_api_key"]
openai.api_key = api_key
model = "gpt-3.5-turbo"

user_email = st.text_input("Email Address", key="user_email", value="contact@markmcrg.com")
generate_newsletter = st.button("Generate Newsletter")

with open('newsletter_template2.html', 'r') as file:
    template_content = file.read()

article_title = []
article_content = []
article_images = []

news_source = st.sidebar.selectbox("**Select news source**", ("Rappler", "The Sydney Morning Herald", "Special Broadcasting Service", "Outsource Accelerator"))
if news_source == "Rappler":
    category = st.sidebar.radio("Category", ("National", "Metro Manila", "Weather", "Environment"))
elif news_source == "The Sydney Morning Herald":
    category = st.sidebar.radio("Category", ("Companies", "Market"))
elif news_source == "Special Broadcasting Service":
    category = st.sidebar.radio("Category", ("Top Stories", "Life"))
elif news_source == "Outsource Accelerator":
    category = st.sidebar.radio("Category", ("BPO News", "BPO Articles"))

    
# Number of articles to include in newsletter
n = 5
article_urls = get_article_urls(category, 5)

for i, url in enumerate(article_urls):
    article = Article(url)
    article.download()
    article.parse() 
    article_title.append(article.title)
    if article.text.startswith("This is AI generated summarization"):
        if len(article.text) > 10000:
            article_content.append(article.text[105:10000])
        else:
            article_content.append(article.text[105:])
    else:
        if len(article.text) > 10000:
            article_content.append(article.text[:10000])
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
            
            my_bar.progress(30, text="Fetching weather alerts...")
            
            cities_data = get_cities_data()
            gsheets_url = st.secrets["public_gsheets_url"]
            
            df = load_data(gsheets_url)
            df['Latitude'], df['Longitude'] = zip(*df['city'].map(get_coordinates))
            df['status'], df['description'] = zip(*df.apply(lambda row: determine_status_and_description(fetch_weather_alerts(row['Latitude'], row['Longitude'])), axis=1))

            df = df.sort_values(by=['status'])
            st.dataframe(df, hide_index=True)
            grouped_df = df.groupby('status')
            
            awas_state = ""
            for status, group in grouped_df:
                if status != 'No Alert':
                    awas_state += f"<b>{status}</b><br>"
                    for index, row in group.iterrows():
                        awas_state += f"<b>{row['name']}</b> - {row['city']}<br>"
                    awas_state += "<br>"
            
            my_bar.progress(50, text="Generating newsletter content...")
            
            # Replace template content (title, summarized content, image, url, source,)
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
            for attempt in range(1, 4):
                try:
                    with smtplib.SMTP_SSL('smtp.ionos.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                    my_bar.progress(100, text="Done!")
                    st.write(f'Newsletter sent to {user_email}!')
                    break  # Exit loop if email is sent successfully
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    if attempt < 3:
                        time.sleep(3)
                    else:
                        st.error(f"Failed to send newsletter to {user_email}. Please try again.")

    else:
        st.error("Please enter your API key.")
else:
    st.info("Enter your email address and click the button to generate a newsletter.")
