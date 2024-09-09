# helper functions
from PIL import Image
import os
import base64
import shutil
import mimetypes

def load_image(image_file):
    img = Image.open(image_file)
    return img

def save_image_file(image_file):
    temp_data_dir = "temp-data"
    os.makedirs(temp_data_dir, exist_ok=True)
    
    for filename in os.listdir(temp_data_dir):
        file_path = os.path.join(temp_data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            
    with open(os.path.join("temp-data",image_file.name), "wb") as f:
        f.write(image_file.getbuffer())
        
def save_problem_file(problem):
    temp_data_dir = "temp-data"
    file_path = "problem_description.txt"
    with open(os.path.join(temp_data_dir,file_path), "w") as file:
        file.write(problem)
        
def encode_base_64(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def get_image():
    temp_data_dir = "temp-data"
    files = os.listdir(temp_data_dir)
    if files:
        image_path =  os.path.join(temp_data_dir, files[0])
        mime_type, _ = mimetypes.guess_type(image_path)
        return image_path, mime_type
    
    return None, None
    
def clear_directory():
    temp_data_dir = "temp-data"
    os.makedirs(temp_data_dir, exist_ok=True)
    
    for filename in os.listdir(temp_data_dir):
        file_path = os.path.join(temp_data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    
    