# Automated Weather Alert Newsletter

This program is a Streamlit-based application designed to generate and send daily newsletters via email. The program gathers news articles from a specific URL, summarizes them using the OpenAI GPT-3.5 Turbo model, and compiles them into an HTML newsletter template. The generated newsletter is then sent to the specified email address.

![Screenshot of Demo](https://gcdnb.pbrd.co/images/6sHHaQAAp2zP.png?o=1)

## Features
- Input Configuration: Configure your API key for OpenAI's GPT-3.5 Turbo model and provide your email address.
- Newsletter Generation: Click the "Generate Newsletter" button to initiate the newsletter generation process.
- Article Retrieval: The program extracts news articles from a given URL, focusing on a specific category (e.g., weather).
- Summarization: It uses the GPT-3.5 Turbo model to summarize the extracted articles.
- Email Delivery: The generated newsletter is sent to the specified email address.
- Customization: The program replaces placeholders in an HTML template with article titles, summaries, URLs, and images.

## Usage
1. Run the program.
2. Enter your OpenAI API key in the provided input field on the sidebar.
3. Enter your email address in the corresponding text input field.
4. Click the "Generate Newsletter" button to initiate the newsletter generation process.
Please note that generating the newsletter may take some time (approximately 30 seconds to 1 minute). The program provides progress updates as it completes each step of the process.

## Dependencies
- Streamlit
- Newspaper3k
- OpenAI
- smtplib (for sending emails)

