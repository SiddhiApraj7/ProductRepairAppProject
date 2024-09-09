import streamlit as st
from local_rag import prepare_db

# Check if the vector_db_instance is already stored in the session state
if "vector_db_instance" not in st.session_state:
    st.session_state.vector_db_instance = prepare_db()

# Access the vector_db_instance from session state
vector_db_instance = st.session_state.vector_db_instance