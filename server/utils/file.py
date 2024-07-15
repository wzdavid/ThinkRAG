import os
from config import DATA_DIR

def get_save_dir():
    save_dir = os.getcwd() + "/" + DATA_DIR
    return save_dir

def save_uploaded_file(uploaded_file: bytes, save_dir: str):
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        path = os.path.join(save_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            print(f"已保存 {path}")
    except Exception as e:
        print(f"Error saving upload to disk: {e}")