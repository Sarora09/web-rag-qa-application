import streamlit as st
import requests

# Configure page
st.set_page_config(page_title="Web RAG QA Application", page_icon="🔍")

# API base URL
API_BASE_URL = "http://localhost:9999"

if "db_id" not in st.session_state:
    st.session_state.db_id = None
if "response_text" not in st.session_state:
    st.session_state.response_text = ""
if "show_success" not in st.session_state:
    st.session_state.show_success = False

st.title("🔍 Web RAG QA Application")
st.markdown("Enter a URL to index and ask questions about the content")

url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

if st.button("Submit", key="submit_url"):
    if url_input:
        with st.spinner("Indexing..."):
            try:
                response = requests.post(f"{API_BASE_URL}/setupdatabase", json={"url": url_input})
                if response.status_code == 200:
                    st.session_state.db_id = response.json()["db_id"]
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Failed to setup database')}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a URL")

if st.session_state.db_id:
    if st.session_state.show_success:
        st.success("✅ Database indexed successfully!")
        st.session_state.show_success = False
    
    st.divider()
    st.subheader("Ask Questions")
    
    with st.form("query_form", clear_on_submit=False):
        query_input = st.text_area("Enter your query:", placeholder="What is this page about?")
        col1, col2 = st.columns(2)
        with col1:
            submit_query = st.form_submit_button("Submit Query")
        with col2:
            clear_db = st.form_submit_button("Clear Database")
    
    if submit_query and query_input.strip():
        with st.status("Processing your query...", expanded=True):
            try:
                response = requests.post(f"{API_BASE_URL}/fetchdata", json={"query": query_input, "dbname": st.session_state.db_id})
                if response.status_code == 200:
                    st.session_state.response_text = response.json()["response"]
                    st.write("✓ Complete")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Failed to fetch data')}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    elif submit_query:
        st.warning("⚠️ Please enter a query")
    
    if clear_db:
        with st.status("Clearing database...", expanded=True):
            try:
                response = requests.post(f"{API_BASE_URL}/cleardb", json={"dbname": st.session_state.db_id})
                if response.status_code == 200:
                    st.write("✓ Cleared")
                else:
                    st.error(f"❌ Error")
            except Exception as e:
                st.error(f"❌ Error")
        st.session_state.db_id = None
        st.session_state.response_text = ""
        st.rerun()
    
    if st.session_state.response_text:
        st.divider()
        st.subheader("Response:")
        st.markdown(st.session_state.response_text)