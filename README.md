# Automated Weather Alert Newsletter
The Automated Weather Alert Newsletter is a repository for a Python-based application that provides summaries of news articles from selected news sources and sends them as a newsletter to a specified email address. It also provides weather alerts for cities in the Philippines.

![Screenshot of Demo](https://gcdnb.pbrd.co/images/6sHHaQAAp2zP.png?o=1](https://gcdnb.pbrd.co/images/mCXUb6zUp9cv.png?o=1))

## File Structure

Below is the structure of the repository:
- streamlit_main.py: The main file that controls the web application's user interface and user interactions. It fetches news articles from selected news sources, summarizes them, and displays the summarized and original content side by side.

- helpers/get_links.py: This module contains helper functions for fetching news articles' URLs from the selected news sources.

- pages/newsletter.py: This script generates a newsletter containing summaries of news articles and sends it to a specified email address.

- pages/weatherAlerts.py: This script fetches weather alerts for cities in the Philippines and provides a summary of the latest Philippine weather news.

## How to Use
### Streamlit 
https://automated-newsletter.streamlit.app/


### Local
1. Clone the repository to your local machine.
2. Install the required dependencies listed in the requirements.txt file.
3. Run the streamlit_main.py file to start the web application.
4. On the sidebar, you can select the news source and category to fetch news articles from.
5. Click the "Get latest news" button to fetch the latest news articles.
6. Click the "Summarize Articles" button to generate summaries for the fetched articles.
7. On the "Newsletter Generator" page, enter your email address and click the "Generate Newsletter" button to generate a newsletter containing the summarized news articles and send it to the entered email address.
8. On the "Weather Alerts" page, click the "Fetch Weather Alerts" button to fetch weather alerts for cities in the Philippines.

## Requirements
### Libraries
1. Streamlit (pip install streamlit)
2. OpenAI (pip install openai)
3. BeautifulSoup (pip install beautifulsoup4)
4. requests (pip install requests)
5. newspaper3k (pip install newspaper3k)
6. overpy (pip install overpy)


### Secrets
- The API key for OpenAI is required to generate summaries for the news articles. You need to input this key in the sidebar's text input field.
- The email password for the sender's email address is required to send the newsletter. This password is stored as a secret (secrets.toml) in Streamlit.
