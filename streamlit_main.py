import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests 
from newspaper import Article

st.set_page_config(layout="wide", page_title="News Summarizer", page_icon="📰")

from st_pages import show_pages_from_config
show_pages_from_config()

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

openai.api_base = "https://api.openai.com/v1"
openai.api_key = api_key
model = "gpt-3.5-turbo"

def clear_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

st.sidebar.header("📰 News Summarizer")
category = st.sidebar.radio("News Category", ("National", "Metro Manila", "Weather"), on_change=clear_session_state)
if category == "National":
    rappler_url = "https://www.rappler.com/nation/national-news/"
elif category == "Metro Manila":
    rappler_url = "https://www.rappler.com/nation/metro-manila"
elif category == "Weather":
    rappler_url = "https://www.rappler.com/nation/weather"
    

url = st.sidebar.text_area("Rappler URL", rappler_url, disabled=True, label_visibility="collapsed")

scrape = st.sidebar.button("Scrape Articles")

def get_href_links(url, n=3):
  response = requests.get(url)
  if response.status_code != 200:
    st.write("Failed to fetch the page.")

  soup = BeautifulSoup(response.content, "html.parser")
  post_card_titles = soup.find_all("h3", class_="post-card__title")
  href_links = [h3.a["href"] for h3 in post_card_titles[:n]]

  return href_links

article_title = []
article_content = []
st.session_state.disabled = True

if scrape:
    with st.spinner("Scraping articles..."):
        article_urls = get_href_links(url, 3)
        for i, url in enumerate(article_urls):
            article = Article(url)
            article.download()
            article.parse() 
            article_title.append(article.title)
            if article.text.startswith("This is AI generated summarization"):
                article_content.append(article.text[105:])
            else:
                article_content.append(article.text)
            st.session_state.article_title = article_title
            st.session_state.article_content = article_content
    st.session_state.disabled = False
        

summary_button = st.sidebar.button("Summarize Articles", disabled=st.session_state.disabled)
def generate_summary(article_content):
    chat_completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": f""""You are a news summary bot. Given the content of an article, your task is to summarize it into one short paragraph, 4 sentences maximum."""},
            {"role": "user", "content": f"Content: {article_content}"}
        ]   
    )
    content = chat_completion['choices'][0]['message']['content']
    return content

col1, col2, = st.columns(2, gap="medium")

with col1:
    st.header("News Content")
    st.divider()
    if 'article_title' and 'article_content' in st.session_state:
        for i, content in enumerate(st.session_state.article_content):
            st.subheader(st.session_state.article_title[i])
            st.write(content)
            st.write("---")
with col2:
    st.header("Summarized Content")
    st.divider()
    if summary_button and 'article_title' and 'article_content' in st.session_state:
        if api_key:
            for i, content in enumerate(st.session_state.article_content):
                st.subheader(st.session_state.article_title[i])
                with st.spinner("Generating summary..."):
                    summary = generate_summary(st.session_state.article_content[i])
                    st.success(summary)
                    st.write("---")
        else:
            st.sidebar.error("Please enter your API key.")