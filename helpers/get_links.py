import requests
import streamlit as st
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_rappler_links(category, subcategory, n=3):
  response = requests.get(f'https://www.rappler.com/{category}/{subcategory}')
  if response.status_code != 200:
    st.write("Failed to fetch the page.")

  soup = BeautifulSoup(response.content, "html.parser")
  post_card_titles = soup.find_all("h3", class_="post-card__title")
  href_links = [h3.a["href"] for h3 in post_card_titles[1:n+1]]

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

def get_oa_links(category, n=3):
    response = requests.get(f'https://www.outsourceaccelerator.com/source/{category}/')
    if response.status_code != 200:
        st.write("Failed to fetch the page.")

    soup = BeautifulSoup(response.content, "html.parser")
    article_links = soup.find('div', class_='js-lists browse-articles__lists')
    href_links = [link.get('href') for link in article_links.find_all('a') if link.get('href')]
    return href_links[:n]

def get_article_urls(category, n=3):
  if category == "National":
      article_urls = get_rappler_links("nation", "national-news", n)
  elif category == "Metro Manila":
      article_urls = get_rappler_links("nation", "metro-manila", n)
  elif category == "Weather":
      article_urls = get_rappler_links("nation", "weather", n)
  elif category == "Companies":
      article_urls = get_smh_links("business", "companies", n)
  elif category == "Market":
      article_urls = get_smh_links("business", "markets", n)
  elif category == "Top Stories":
      article_urls = get_sbs_links("top-stories", n+1)
      article_urls = article_urls[1:]
  elif category == "Life":
      article_urls = get_sbs_links("life-articles", n)
  elif category == "BPO News":
      article_urls = get_oa_links('news', n)
  elif category == "BPO Articles":
      article_urls = get_oa_links('articles', n)
  elif category == "Environment":
      article_urls = get_rappler_links("environment", "", n)

  return article_urls