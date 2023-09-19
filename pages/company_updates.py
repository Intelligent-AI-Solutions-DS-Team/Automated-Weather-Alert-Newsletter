import streamlit as st
import pandas as pd
import datetime
import openai
import smtplib
from email.message import EmailMessage
import time


openai.api_base = "https://api.openai.com/v1"
api_key = st.secrets["openai_api_key"]
openai.api_key = api_key
model = "gpt-3.5-turbo-16k"

EMAIL_ADDRESS = 'hello@markmcrg.com'
email_pass = st.secrets["EMAIL_PASSWORD"]
EMAIL_PASSWORD = email_pass

# add streamlit title
st.set_page_config(page_title="LinkedIn Updates", page_icon=":bar_chart:")
st.title("📊 LinkedIn Updates")


docu_id = st.secrets['job_sheets_docu_id']

companies = ['Zookal', 'Stanton Hillier Parker', 'X Commercial', 'Solar Juice Pty Ltd', 'AutoGrab', 'Elite Office Furniture', 'NPM', 'VYSPA', 'Whale Logistics (Australia) Pty Ltd', 'TheGuarantors', 'M2']

@st.cache_data
def fetch_job_df(company_name):
    company_sheet_mapping = {
        "Zookal": "2028206938",
        "Stanton Hillier Parker": "1913252330",  
        "X Commercial": "1862120702",  
        "Solar Juice Pty Ltd": "358830246",  
        "AutoGrab": "1199841788",  
        "Elite Office Furniture": "747554974",  
        "NPM": "1916801077",  
        "VYSPA": "1984980421", 
        "Whale Logistics (Australia) Pty Ltd": "977195592",  
        "TheGuarantors": "153394626", 
        "M2": "1043528360"  
    }
    
    if company_name in company_sheet_mapping:
        sheet_id = company_sheet_mapping[company_name]
    else:
        sheet_id = "Company not found"

    url = f'https://docs.google.com/spreadsheets/d/{docu_id}/export?gid={sheet_id}&format=csv'

    try:
        df = pd.read_csv(url)
    except:
        raise Exception("Unable to fetch data from Google Sheets.")

    return df

@st.cache_data
def fetch_company_info(company_name):
    url = f"https://docs.google.com/spreadsheets/d/{docu_id}/export?format=csv"
    df = pd.read_csv(url)
    
    company_row = df.loc[df['name'] == company_name]
    
    if company_row.empty:
        return "Company not found."
    
    return company_row.to_dict(orient='records')[0]

def parse_jobs_df(df):
    if df['job_title'].isnull().any():
        return None

    data = {}

    for column in df.columns:
        data[column] = df[column].values.tolist()

    return data

def generate_summary(jobs_data):
    chat_completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a dictionary parser. Please concisely summarize the job postings of this company without separating each individual job. Ensure that the total output is limited to 4 sentences."},
            {"role": "user", "content": f"{jobs_data}"}
        ]   
    )
    content = chat_completion['choices'][0]['message']['content']
    return content

date_today = pd.to_datetime('today').strftime('%B %d, %Y')
# st.write(f"**Current Date:** {date_today}")

user_email = st.text_input("Email Address", key="user_email", value="contact@markmcrg.com")
generate_updates = st.button("Generate Updates & Send Email")

# FOR TESTING
# if generate_updates:
#     with st.spinner("Fetching company updates..."):
#         for company in companies:
#             with st.expander(company):
#                 df = fetch_job_df(company)
#                 company_info = fetch_company_info(company)
#                 st.write(f"**Last Data Update:** {company_info['last_update']}")
#                 st.write(f"**Company:** [{company_info['name']}]({company_info['company_link']})")
#                 st.write(f"**Headline:** {company_info['headline']}")
#                 st.write(f"**Followers:** {company_info['followers']}")
#                 st.write(f"**Employees:** {company_info['employees']}")
#                 st.write(f"**About:** {company_info['about']}")
#                 st.write(f"**Latest Post:** {company_info['latest_post_1']}")
#                 jobs_data = parse_jobs_df(df)
#                 if jobs_data:
#                     summary = generate_summary(jobs_data)
#                     st.subheader("Job Updates")
#                     st.write(summary)
#                 else:
#                     st.write("**Job Updates:** No job postings found.")

if generate_updates:
    with st.spinner("Fetching company updates..."):
        email_body = "<html><body>"
        for company in companies:
            df = fetch_job_df(company)
            company_info = fetch_company_info(company)
            
            #email_body += f"<strong>Last Data Update:</strong> {company_info['last_update']}<br>"
            email_body += f"<strong>Company:</strong> <a href='{company_info['company_link']}'>{company_info['name']}</a><br><br>"
            email_body += f"<strong>Headline:</strong> {company_info['headline']}<br><br>"
            email_body += f"<strong>Followers:</strong> {company_info['followers']}<br><br>"
            email_body += f"<strong>Employees:</strong> {company_info['employees']}<br><br>"
            email_body += f"<strong>About:</strong> {company_info['about']}<br><br>"
            email_body += f"<strong>Latest Post:</strong> {company_info['latest_post_1']}<br><br>"
            jobs_data = parse_jobs_df(df)
            if jobs_data:
                summary = generate_summary(jobs_data)
                email_body += "<strong>Job Updates</strong><br>"
                email_body += summary
            else:
                email_body += "<strong>Job Updates:</strong> No job postings found.<br><br>"
            email_body += "<hr>"
                
        email_body += "</body></html>"
        # Create the email
        msg = EmailMessage()
        
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = f"Weekly Company Updates - {date_today}"

        msg.set_content(email_body, subtype='html')
        for attempt in range(1, 4):
            try:
                with smtplib.SMTP_SSL('smtp.ionos.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                st.write(f'Email sent to {user_email}!')
                break  # Exit loop if email is sent successfully
            except Exception as e:
                print(f"Attempt {attempt} failed: {str(e)}")
                if attempt < 3:
                    time.sleep(3)
                else:
                    st.error(f"Failed to send newsletter to {user_email}. Please try again.")