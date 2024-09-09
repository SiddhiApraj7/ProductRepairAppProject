import streamlit as st

def display_model_input():
    col1, col2 = st.columns(2, gap="small", vertical_alignment="top")

    with col1:
        st.write("#### Model of the product?")
        model = st.text_input(label="", value="", max_chars=2000, key="model", type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="What model is this? eg. macbook pro 16", disabled=False, label_visibility="collapsed")
    
    with col2:
        st.write("#### What's the company?")
        company_name = st.text_input(label="", value="", max_chars=2000, key="company-name", type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="What company manufactured this? eg.Apple", disabled=False, label_visibility="collapsed")
        
    return model, company_name

def display_model_info(info):
    st.write(info)