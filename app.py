import os
import streamlit as st

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    
from ask import ask , retrieve_answer

# 1. Page Config & Title
st.set_page_config(page_title = 'Govt Schemes Q&A', page_icon = '📝')

st.title('Indian Govt Schemes Assistant')
st.write("Ask a question about PM-KISAN, Mudra Yojana, PMAY, FCRA, PMKVY, and more. Answers are cited with source and page number.")

# 2. Example Questions UI (drop down)

with st.expander("Example Questions"):
    st.write("- What is the eligibility age for PM-KISAN?")
    st.write("- How much loan can I get under Mudra Yojana?")
    st.write("- What are the conditions for FCRA registration?")


# 3. User Input & Query Execution
question = st.text_input("Your question: ")

if question :
    with st.spinner("Searching documents and generating answer..."):
        answer = ask(question)
        chunks = retrieve_answer(question)

    st.markdown(f"Answer: {answer}")

    with st.expander('View retrieved sources'):
        for i,chunk in enumerate(chunks):
            st.text(f"Source {i+1}:\n {chunk[:300]}...") 