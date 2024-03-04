import streamlit as st
import requests

# Define FastAPI endpoint URL
FASTAPI_URL = 'http://localhost:8000/search/'

# Streamlit UI
st.title('Similarity Search')

# Input query
query_text = st.text_input('Enter your query:')

# Send query to FastAPI endpoint
if st.button('Search'):
    if query_text:
        response = requests.post(FASTAPI_URL, json={'query': query_text})
        print(response.text)
        print(query_text)
        if response.status_code == 200:
            search_results = response.json()
            st.write('Search Results:')
            for result in search_results:
                st.json(result['tags'])
        else:
            st.error('Failed to retrieve search results.')


