import streamlit as st
import pandas as pd
import datetime

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

date_today = pd.to_datetime('today').strftime('%B %d, %Y')
st.write(f"**Current Date:** {date_today}")
with st.spinner("Fetching company updates..."):
    for company in companies:
        with st.expander(company):
            df = fetch_job_df(company)
            company_info = fetch_company_info(company)
            st.write(f"**Last Data Update:** {company_info['last_update']}")
            st.write(f"**Company:** [{company_info['name']}]({company_info['company_link']})")
            st.write(f"**Headline:** {company_info['headline']}")
            st.write(f"**Followers:** {company_info['followers']}")
            st.write(f"**Employees:** {company_info['employees']}")
            st.write(f"**About:** {company_info['about']}")
            if company_info['latest_post_1']:
                st.write(f"**Latest Post:** {company_info['latest_post_1']}")
            st.write(df)
        



    

