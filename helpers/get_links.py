import requests
import streamlit as st
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_rappler_links(category, subcategory, n=3):
  response = requests.get(f'https://www.rappler.com/{category}/{subcategory}/')
  if response.status_code != 200:
    st.write("Failed to fetch the page.")

  soup = BeautifulSoup(response.content, "html.parser")
  post_card_titles = soup.find_all("h3", class_="post-card__title")
  href_links = [h3.a["href"] for h3 in post_card_titles[:n]]

  return href_links

def get_smh_links(category, subcategory, n=3):
    response = requests.get(f'https://www.smh.com.au/{category}/{subcategory}')
    if response.status_code != 200:
        st.write("Failed to fetch the page.")

    soup = BeautifulSoup(response.content, "html.parser")
    article_links = soup.find_all(attrs={"data-testid": "article-link"})
    href_links = [link["href"] for link in article_links]
    href_links = list(OrderedDict.fromkeys(href_links))
    href_links = [f"https://www.smh.com.au/{category}/{subcategory}" + link for link in href_links]    
    return href_links[:n]

def get_sbs_links(category, n=3):
    url = f'https://www.sbs.com.au/news/collection/{category}'
    response = requests.get(url)
    if response.status_code != 200:
        st.write("Failed to fetch the page.")
    soup = BeautifulSoup(response.content, "html.parser")
    article_links = soup.find_all('div', class_='SBS_ShelfItem css-6mfr8')
    href_links = [link.a["href"] for link in article_links]
    href_links = [f"https://www.sbs.com.au{link}" for link in href_links]
    return href_links[:n]
