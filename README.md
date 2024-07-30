---
layout: default
---

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

### Table of Contents

- [What is ThinkRAG](#What-is-ThinkRAG) 🤔
- [Key features](#Key-Features)
- [Quick Start](#quick-start) 🔜
- [Set API Key](#set-api-key) ⚙️
  - [MacOS & Linux](#MacOS-Linux)
  - [Windows](#Windows)
- [Engine Interface Instructions](#engine-interface-instructions) 📖
- [Model Support](#model-support) 🪀
- [License](#license) 📄
- [Contact Us](#Contact-Us)


<div id='What-is-ThinkRAG'></a>

## What is ThinkRAG 🤔

ThinkRAG is an open-source RAG engine that based on document retrieval.


<div id='Key-Features'></a>

## Key Features

<details open>
  <summary>
    <b>Expand</b>
  </summary>


#### Knowledge Base Management: 

&emsp;&emsp; ThinkRAG allows users to upload, manage, and index content from both files (like PDFs, DOCX, and TXT files) and web pages. This includes setting parameters for text processing to ensure optimal data organization and retrievability.

#### API Configuration:

&emsp;&emsp; ThinkRAG offers extensive settings for configuring APIs, including setting up service addresses, selecting models, and enabling specific features like re-ranking for embedding models. This facilitates integration and management of various language and embedding models that can be used for enhanced data processing and retrieval within the knowledge base.

#### Advanced Settings:

&emsp;&emsp; ThinkRAG also includes advanced settings that allow users to further refine system behaviour and interaction modes, such as adjusting response selection criteria and customizing system prompts.

#### Support LanceDB:

&emsp;&emsp; As a open-source multimodal vector database, LanceDB has following core advantages:
- Optimized for Time Series Data: Designed specifically for handling time series data, making it ideal for real-time monitoring, IoT device data, financial trading data, and more.
- High Performance: Offers high data ingestion rates and fast query performance, suitable for real-time analytics.
- Scalability: Supports horizontal scaling, enabling increased load handling by adding more nodes.
- Efficient Data Compression: Utilizes advanced data compression techniques to optimize storage and enhance I/O efficiency.
- Flexible Data Retention Policies: Allows for customizable data retention policies, supporting automatic downsampling or deletion of old data.
- Robust Query Language: Provides a powerful and flexible query language to facilitate complex data analysis and aggregation directly in the database.
- Integrated Visualization Tools: May include integrated tools for data visualization and dashboarding, simplifying data monitoring and analysis.

Visit [here](https://lancedb.com/) to learn more about LanceDB. 

</br>

</details>


<div id='quick-start'></a>

## Quick Start 🔜
<details open>
  <summary>
    <b>Expand</b>
  </summary>

### Step 1
```zsh
pip3 install -r requirements.txt
```
### Step 2

Refer to [here](/docs/HowToDownloadModels.md) to download embedding models and nltk data into localmodels directory

### Step 3

If you need LLMs API, please set your corresponding API Key first, see [Set API Key](#set-api-key) for detailed instructions.

Then, run ThinkRAG by the following command (after returning to the root directory of ThinkRAG):
```zsh
streamlit run app.py
```

</details>


<div id='set-api-key'></a>

## Set API Key ⚙️

<div id='MacOS-Linux'></a>

- ### MacOS & Linux

<details>
  <summary>
    <b>Expand</b>
  </summary>

#### Set Temporary API Key
##### 1. Run the command line in your terminal
```zsh
export VARIABLE_NAME=value
```
For instance, to set your API key for OpenAI, just run the following line in your terminal:
```zsh
export OPENAI_API_KEY=your_OpenAI_API_key 
```
<br/>

#### Set Permanent API Key
##### 1. Create or edit '.zshenv' file

```zsh
nano ~/.zshenv
```
For Linux, macOS Mojave (10.14) or earlier version, run 
```zsh
nano ~/.bashrc
```
##### 2. Add Your Configuration
```zsh
export VARIABLE_NAME="value"
```
For instance, to set your API key for OpenAI, just type the following line into your '.zshenv' (or '.bashrc') file:
```zsh
export OPENAI_API_KEY=your_OpenAI_API_key 
```
##### 3. Save and exit
You may now save changes by pressing 'Ctrl + O', then press 'Enter' to confirm, and 'Ctrl + X' to exit the editor.

##### 4. Apply the Changes
To ensure the changes take effect in your current terminal session, you can source the file by run
```zsh
source ~/.zshenv 
# source ~/.bashrc for Linux, macOS Mojave (10.14) or earlier
```
</br>

</details>

<div id='Windows'></a>

- ### Windows

<details>
  <summary>
    <b>Expand</b>
  </summary>

#### Run the command line in your terminal

```zsh
set VARIABLE_NAME=value # Set Temporary API Key
```

```zsh
setx VARIABLE_NAME "value" -m # Set Permanent API Key
```

</br>

</details>

<div id='engine-interface-instructions'></a>

## Engine Interface Instructions 📖

<details open>
  <summary>
    <b>Expand</b>
  </summary>

  See [here](Instructions.md) for detailed instructions about ThinkRAG's key features and how to use them for your own customized purposes.

</details>

<div id='model-support'></a>

## Model Support 🪀

<details open>
  <summary>
    <b>Expand</b>
  </summary>

</br>

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

</br>

</details>

<div id='license'></a>

## License 📄

ThinkRAG uses MIT License. See [here](LICENSE) for details.
</details>

<div id='Contact-Us'></a>

## Contact Us ☎️

##### Wechat Official Account
