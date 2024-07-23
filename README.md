<div align="center">
<img src="web/src/temporary_logo.png" width="350" alt="temporary_logo">
</a>
</div>




<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>




<details open>
<summary></b> Table of Contents</b></summary>

- [What is ThinkRAG](#What-is-ThinkRAG) 🤔
- [Quick Start](#quick-start) 🔜
- [Set API Key](#set-api-key) ⚙️
- [Engine Interface Instructions](#engine-interface-instructions) 📖
- [Model Support](#model-support) 🪀
- [License](#license) 📄

</details>

</br>

<div id='What-is-ThinkRAG'></a>

# What is ThinkRAG 🤔
ThinkRAG is an open-source RAG engine that based on document retrieval.

### Key Features

#### Knowledge Base Management: 

&emsp;&emsp; ThinkRAG allows users to upload, manage, and index content from both files (like PDFs, DOCX, and TXT files) and web pages. This includes setting parameters for text processing to ensure optimal data organization and retrievability.

#### API Configuration:

&emsp;&emsp; ThinkRAG offers extensive settings for configuring APIs, including setting up service addresses, selecting models, and enabling specific features like re-ranking for embedding models. This facilitates integration and management of various language and embedding models that can be used for enhanced data processing and retrieval within the knowledge base.

#### Advanced Settings:

&emsp;&emsp; ThinkRAG also includes advanced settings that allow users to further refine system behaviour and interaction modes, such as adjusting response selection criteria and customizing system prompts.



</br>

<div id='quick-start'></a>

# Quick Start 🔜

### Step 1
```bash
pip3 install -r requirements.txt
```
### Step 2

Refer to [here](/docs/HowToDownloadModels.md) to download embedding models and nltk data into localmodels directory

### Step 3

If you need LLMs API, please set your corresponding API Key first, see [Set API Key](#set-api-key) for detailed instructions.

Then, run ThinkRAG by the following command:
```bash
streamlit run app.py
```
<br/>

<div id='set-api-key'></a>

# Set API Key: ⚙️


## MacOS & Linux

### Set Temporary API Key
### 1. Run the command line in your terminal
```bash
export VARIABLE_NAME=value
```
For instance, to set your API key for OpenAI, just run the following line in your terminal:
```bash
export OPENAI_API_KEY=your_OpenAI_API_key 
```
<br/>

### Set Permanent API Key
### 1. Create or edit '.zshenv' file

```bash
nano ~/.zshenv
```
For Linux, macOS Mojave (10.14) or earlier version, run 
```bash
nano ~/.bashrc
```
### 2. Add Your Configuration
```bash
export VARIABLE_NAME="value"
```
For instance, to set your API key for OpenAI, just type the following line into your '.zshenv' (or '.bashrc') file:
```bash
export OPENAI_API_KEY=your_OpenAI_API_key 
```
### 3. Save and exit
You may now save changes by pressing 'Ctrl + O', then press 'Enter' to confirm, and 'Ctrl + X' to exit the editor.

### 4. Apply the Changes
To ensure the changes take effect in your current terminal session, you can source the file by run
```bash
source ~/.zshenv 
# source ~/.bashrc for Linux, macOS Mojave (10.14) or earlier
```
</br>

## Windows


### Run the command line in your terminal

```bash
set VARIABLE_NAME=value # Set Temporary API Key
```

```bash
setx VARIABLE_NAME "value" -m # Set Permanent API Key
```

<div id='engine-interface-instructions'></a>

</br>

# Engine Interface Instructions 📖

See [here](Instructions.md) for detailed instructions about ThinkRAG's key features and how to use them for your own customized purposes.

<div id='model-support'></a>

</br>

# Model Support 🪀

<table>
<tr>
<th> Ollama models </th>
<th> LLMs </th>
</tr>
<tr>
<td>

gemma:2b

llama2-chinese:13b

llama2:13b

mistral:latest

deepseek-coder:33b

deepseek-coder:latest

gemma:latest

</td>
<td>

glm-4

glm-4v

glm-3-turbo

moonshot-v1-8k

moonshot-v1-32k

moonshot-v1-128k

deepseek-chat

deepseek-coder

gpt-4

gpt-3.5

gpt-4o

</td>
</tr>
</table>

<div id='license'></a>

</br>

# License 📄

ThinkRAG uses MIT License. See [here](LICENSE) for details.







