<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![support: LanceDB](https://img.shields.io/badge/Support-LanceDB-blue.svg)](https://lancedb.com/) [![support: Ollama](https://img.shields.io/badge/Support-Ollama-green.svg)](https://ollama.com/) [![support: LlamaIndex](https://img.shields.io/badge/Support-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)



</div>

### Table of Contents

- 🤔 [What is ThinkRAG](#What-is-ThinkRAG)
- ✨ [Key Features](#Key-Features)
- 🛫 [Quick Start](#quick-start)
- 📖 [Usage](#engine-interface-instructions)
- 🔬 [Technology Stack](#Modes-Comparison)
- 🧸 [Support Models](#Support-Models)
- 📄 [License](#license)

<div id='What-is-ThinkRAG'></a>

# What is ThinkRAG 🤔

ThinkRAG is a Large Language Model (LLM) RAG system leveraging LlamaIndex and Streamlit, specifically optimized for Chinese users. It incorporates BAAI embedding/reranker models and Ollama local models, and utilizes LLM APIs from Chinese service providers such as Zhipu, DeepSeek, and Moonshot.


<div id='Key-Features'></a>

# Key Features ✨

ThinkRAG is specially tailored for Chinese usage, incorporating several key features:

- Complete implementation of LlamaIndex, allows the RAG system to operate flawlessly on personal computers. The Ollama model additionally ensures the privacy of personal data and is fully capable of local implementation.
- A Spacy text splitter and enhancements for Chinese titles, specifically designed for Chinese characters (referencing Langchain-Chatchat, QAnything).
- Chinese prompt templates tailored for Q&A and Refinement processes.
- Large Chinese language models such as Zhipu, DeepSeek and Moonshot.
- Hugging Face’s Chinese embedding model (BAAI/bge-large-zh-v1.5) designed for optimal performance in Chinese language tasks.

</br>


<div id='quick-start'></a>

# Quick Start 🛫

## Step 1
```zsh
pip3 install -r requirements.txt
```
## Step 2

You have the option to download and implement the embedding models BAAI/bge-large-zh-v1.5 and BAAI/bge-reranker-base. If you choose to do so, please refer to this [document](Instructions.md) for instructions on how to download models into the localmodels directory.

## Step 3

Depending on the models you intend to utilize, you should either establish their API keys as global variables or download them from their official websites:

1. To set your API key as a global variable, the variable names for supported Large Language Models (LLMs) are as follows:

```zsh
ZHIPU_API_KEY = ""
MOONSHOT_API_KEY = ""
DEEPSEEK_API_KEY = ""
OPENAI_API_KEY = ""
```

2. Alternatively, should you intend to utilize Ollama models, you are advised to download [Ollama](https://ollama.com/download) and your [models](https://ollama.com/library) of preference from this library, such as gemma and llama (support is extended to all Ollama models).

## step 4

Please be informed that ThinkRAG currently operates in both development mode (the default setting) and production mode. To transition to production mode, designate THINKRAG_ENV as a global variable:

```zsh
THINKRAG_ENV = prod
```

For information regarding the distinctions between these two modes, please consult this [detailed comparison](#Modes-Comparison).

## Step 5

To run ThinkRAG, execute the following command (ensure you are in the root directory of ThinkRAG beforehand):

```zsh
streamlit run app.py
```

<div align="center">
<img src="web/src/Home_Page.png" width="700" alt="the_knowledge_base_is_empty">
</a>
</div>

<div id='engine-interface-instructions'></a>

# Usage 📖

For detailed instructions on the key functionalities of ThinkRAG and how to tailor them for your specific needs, please refer to this [document](Instructions.md).

<div id='Modes-Comparison'></a>

# Technology Stack 🔬

| |DEV_MODE|PROD_MODE|
|:----|:----|:----|
|Framework|LlamaIndex|LlamaIndex|
|Frontend|Streamlit|Streamlit|
|Embedding Models|BAAI/bge-large-zh-v1.5 & BAAI/bge-reranker-base|BAAI/bge-large-zh-v1.5 & BAAI/bge-reranker-base|
|Retriever|FusionRetriever|HybridRetriever|
|Text Splitter|SentenceSplitter|SpacyTextSplitter|
|Chat store|SimpleChatStore|Redis|
|Doc store|SimpleDocumentStore|Redis or MangoDB|
|Index store|SimpleIndexStore|Redis or MangoDB|
|Vector Store|SimpleVectorStore|LanceDB as default, Chroma and ES available.|

<div id='Support-Models'></a>

# Support Models 🧸

Ollama, Zhipu, Moonshot, DeepSeek, OpenAI

<div id='license'></a>

# License 📄

ThinkRAG uses MIT License. See [here](LICENSE) for details.