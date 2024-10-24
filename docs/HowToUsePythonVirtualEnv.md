# Create an environment with venv and installing Streamlit and other packages with pip.
# Refer to: https://docs.streamlit.io/get-started/installation/command-line
### 1. Open a terminal and navigate to your project folder
```zsh
cd ThinkRAG
```
### 2. In your terminal, type:
```zsh
python -m venv .venv
```
A folder named ".venv" will appear in your project. This directory is where your virtual environment and its dependencies are installed.
### 3. Activate your environment with one of the following commands
```zsh
# Windows command prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS and Linux
source .venv/bin/activate
```
Once activated, you will see your environment name in parentheses before your prompt. "(.venv)"
### 4. In the terminal with your environment activated, install all required packages:
```zsh
pip3 install -r requirements.txt
```
### 5. Run your Streamlit app
```zsh
python3 -m streamlit run app.py
```
### 6. When you're done using this environment, return to your normal shell by typing:
```zsh
deactivate
```