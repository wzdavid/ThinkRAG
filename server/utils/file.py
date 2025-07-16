import os
from config import DATA_DIR

def get_save_dir():
    save_dir = os.getcwd() + "/" + DATA_DIR
    return save_dir

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks"""
    # Remove directory separators and other dangerous characters
    filename = os.path.basename(filename)
    # Remove any remaining path separators that might exist
    filename = filename.replace("..", "").replace("/", "").replace("\\", "")
    # Ensure the filename is not empty after sanitization
    if not filename or filename.startswith('.'):
        filename = "uploaded_file"
    return filename

def save_uploaded_file(uploaded_file: bytes, save_dir: str):
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # Sanitize the filename to prevent path traversal
        safe_filename = sanitize_filename(uploaded_file.name)
        path = os.path.join(save_dir, safe_filename)
        
        # Additional check to ensure the file is within the intended directory
        if not os.path.abspath(path).startswith(os.path.abspath(save_dir)):
            raise ValueError("Invalid file path detected")
            
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            print(f"已保存 {path}")
    except Exception as e:
        print(f"Error saving upload to disk: {e}")