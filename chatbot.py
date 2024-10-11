# Import Dependencies
import streamlit as st
import requests

# Title
st.title("Wikipedia RAG Chatbot :robot_face:")

# Initialize session state variables if they don't exist
if 'load_on_enter' not in st.session_state:
    st.session_state.load_on_enter = False
if 'query_on_enter' not in st.session_state:
    st.session_state.query_on_enter = False

# Adding flags
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'queries' not in st.session_state:
    st.session_state.queries = []

# Form for loading data
with st.form("load_form", clear_on_submit=False):
    url = st.text_input("Enter Wikipedia URL:")
    load_button = st.form_submit_button("Load URL")

    if load_button or st.session_state.load_on_enter:
        response = requests.post("http://localhost:8000/load", json={"url": url})
        print(f"Load URL Request: {response.request.url}, Status Code: {response.status_code}, Response: {response.json()}")
        if response.status_code == 200:
        if response.status_code == 200:
            st.success("Data loaded successfully!")
            st.session_state.load_on_enter = False  # Reset state
            st.session_state.data_loaded = True  # Set data loaded flag
            st.session_state.queries.clear()  # Clear previous queries
        else:
            st.error(f"Failed to load data: {response.json().get('detail', 'Unknown error')}")

# Form for querying
with st.form("query_form", clear_on_submit=False):
    query = st.text_input("Enter your question:")
    query_button = st.form_submit_button("Ask Question")

    if query_button or st.session_state.query_on_enter:
        if not st.session_state.data_loaded:
            st.error("Please load the Wikipedia URL first.")
        else:
            response = requests.post("http://localhost:8000/query", json={"question": query})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
                st.write(f"Answer: {answer}")
                st.session_state.query_on_enter = False  # Reset state
                st.session_state.queries.append(query)  # Save the query
            else:
                st.error(f"Failed to retrieve answer: {response.json().get('detail', 'Unknown error')}")

# # Display previously asked questions
# if st.session_state.queries:
#     st.write("Previous Questions:")
#     for q in st.session_state.queries:
#         st.write(q)

# Handling Enter key submissions
if st.session_state.load_on_enter or st.session_state.query_on_enter:
    if st.session_state.load_on_enter:
        load_button = st.session_state.load_on_enter
    else:
        load_button = st.session_state.query_on_enter