import streamlit as st
from helper_functions import load_image, save_image_file, save_problem_file, get_image, clear_directory
from frontend_helper import display_model_info, display_model_input
from graph_info import run_complete_agent
from openai import OpenAI
from image_recognition import recognize_image
import dotenv
import os
import re
import torch

clear_directory()

from local_rag import prepare_db

"""
# Welcome to the Product Repair App!
Tell us about your product and we'll try to help you fix it.
"""

st.write("#### Upload an image of your damaged product:")
label_image = "_Image of damaged product_"
image_file = st.file_uploader(label=label_image, type=None, accept_multiple_files=False, key="image-upload", help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
if image_file is not None:
    file_details = {"FileName": image_file.name, "FileType": image_file.type}
    img = load_image(image_file)
    st.image(img, width=200)
    save_image_file(image_file)
    

st.write("#### What seems to not be working? Is there anything specific you need help with?")
label_text = "What's not working?"
problem = st.text_input(label=label_text, value=None, max_chars=2000, key="problem-faced", type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="What's not working?", disabled=False, label_visibility="collapsed")
if problem is not None:
    save_problem_file(problem)
    
    

dotenv.load_dotenv()
if os.environ.get("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ["LANGCHAIN_PROJECT"] = "L3 Research Agent"

model=None
product=None
company=None
image_path, image_type = get_image()
if image_path and image_type:
    with st.spinner("Processing"):
        message = recognize_image(client, image_filepath=image_path, image_type=image_type)
        product = re.search(r"Product:\s*(.*)", message).group(1)
        model = re.search(r"Model:\s*(.*)", message).group(1)
        company = re.search(r"Company:\s*(.*)", message).group(1)

if model == 'TBD' or product == 'TBD' or company == 'TBD':
    model, company = display_model_input()
    
file_path = "temp-data/problem_description.txt"
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        problem = file.read()

if problem and model: 
    with st.spinner("Processing"):       
        query = f"""
        Help me solve a problem I'm facing with a device. Further information is provided below:
        Product: {product}
        Company: {company}
        Model: {model}
        Problem: {problem}
        """

        output = run_complete_agent(query)

        if output:
            st.write("#### Response:")
            st.write(output["generation"])