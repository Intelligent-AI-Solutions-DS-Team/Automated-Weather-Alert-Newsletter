from langchain.agents import load_tools, initialize_agent 
from langchain.chat_models import ChatOpenAI
import streamlit as st

openai_api_key = st.secrets['openai_api_key']
serpapi_api_key = st.secrets['serpapi_key']

st.title("🗞️ Talking Points Generator")
topic = st.text_input ("Enter your topic here")

llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.6, max_tokens=1024, model_name="gpt-3.5-turbo")

tool_names = ['serpapi']

tools = load_tools (tool_names, serpapi_api_key=serpapi_api_key)

agent = initialize_agent(tools, 
                          llm, 
                          agent='chat-zero-shot-react-description', 
                          verbose=True)


generate_button = st.button("Generate")
prompt = f"Please generate three categories related to the topic of {topic}. For each category, provide five bulleted talking points starting with an emoji. The talking points should focus on the most recent news and updates about {topic}. Finally, conclude with a general summary of the up-to-date information."

if generate_button:
    with st.spinner('Generating...'):
        response = agent.run(prompt)
        st.write(response)
        print(response)