<p align="center">
  <a href="./README_en.md">English</a> |
  <a href="./README.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)    [![support: Ollama](https://img.shields.io/badge/Support-Ollama-green.svg)](https://ollama.com/)    [![support: LlamaIndex](https://img.shields.io/badge/Support-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)   

</div>

### Table of Contents

- 🤔 [Overview](#What-is-ThinkRAG)
- ✨ [Features](#Key-Features)
- 🧸 [Model Support](#Support-Models)
- 🛫 [Quick Start](#quick-start)
- 📖 [User Guide](#Instructions)
- 🔬 [Architecture](#Architecture)
- 📜 [Roadmap](#Roadmap)
- 📄 [License](#License)

<div id='What-is-ThinkRAG'></a>

# ThinkRAG

ThinkRAG is a LLM RAG system that can be easily deployed on a laptop to implement Q&A with local knowledge base.

This system is built on LlamaIndex and Streamlit, and has been optimized for Chinese users in various fields such as model selection and text processing.

<div id='Key-Features'></a>

# Key Features

ThinkRAG is a LLM application developed for professionals, researchers, students, and other knowledge workers, which can be used directly on a laptop with all knowledge and data stored locally on the computer.

ThinkRAG has the following features:
- Complete application of the LlamaIndex framework
- Development mode supports local file storage without the need to install any databases
- No GPU support is required to run on a laptop
- Supports locally deployed models and offline use

Specifically, ThinkRAG has also made a lot of customizations and optimizations for Chinese users:
- Uses Spacy text splitter for better handling of Chinese characters
- Employs Chinese title enhancement features
- Uses Chinese prompt templates for Q&A and refinement processes
- Default support for China LLM service provider such as ZhiPu, Moonshot, and DeepSeek
- Uses bilingual embedding models, such as bge-large-zh-v1.5 from BAAI

<div id='Support-Models'></a>

# Model Support

ThinkRAG can use all models supported by the LlamaIndex data framework. For model list information, please refer to [relevant documentation](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/modules/). 

ThinkRAG is committed to creating an application system that is directly usable, useful, and easy to use.

Therefore, we have made careful selections and trade-offs in various models, components, and technologies.

Firstly, using large models, ThinkRAG supports the OpenAI API and all compatible LLM APIs, including LLM service providers in China, such as:

- ZhiPu
- Moonshot
- DeepSeek
- ...

If you want to deploy LLMs locally, ThinkRAG chooses Ollama, which is easy to use. We can download models to run locally through Ollama.

Currently, Ollama supports the local deployment of almost all large language models, including Llama, Gemma, GLM, Mistral, Phi, Llava, etc. For details, please visit the [Ollama official website](https://ollama.com/).

The system also uses embedding models and reranking models, which can support most models from Hugging Face. Currently, ThinkRAG mainly selects the BGE series models from BAAI. Chinese users can visit the [mirror website](https://hf-mirror.com/BAAI) to learn about and download them.

## Known Issues

Currently, there are issues from Windows users that have not been reproduced or resolved. Please use ThinkRAG on Linux or MacOS systems.

Due to incompatibility between llama_index and the latest ollama 0.4, please install ollama 0.3.3, which is reflected in the requirements.txt file.

<div id='quick-start'></a>

# Quick Start

## Step 1 Download and Installation

After downloading the code from Github, use pip to install the required components.
```zsh
pip3 install -r requirements.txt
```
If you want to run the system offline, please first download Ollama from the official website. Then, use the Ollama command to download LLMs such as GLM, Gemma, and QWen.

Then, download the embedding model (BAAI/bge-large-zh-v1.5) and reranking model (BAAI/bge-reranker-base) from Hugging Face to the `localmodels` directory.

For specific steps, please refer to the document in the `docs` directory: HowToDownloadModels.md

## Step 2 System Configuration

For better performance, it is recommended to use commercial LLM APIs.

First, obtain the API key from the LLM service provider and configure the following environment variables.

```zsh
ZHIPU_API_KEY = ""
MOONSHOT_API_KEY = ""
DEEPSEEK_API_KEY = ""
OPENAI_API_KEY = ""
```

You can skip this step and configure the API keys through the application interface after the system is running.

If you choose to use one or more LLM APIs, please delete the unused service providers in the config.py configuration file.

Of course, you can also add other service providers compatible with the OpenAI API in the configuration file.

ThinkRAG runs in development mode by default. In this mode, the system uses local file storage, and you do not need to install any databases.

If you want to switch to production mode, you can configure the environment variables as follows.

```zsh
THINKRAG_ENV = production
```

In production mode, the system uses vector databases Chroma and key-value databases Redis.

If you do not have Redis installed, it is recommended to install it through Docker or use an existing Redis instance. Please configure the parameters of the Redis instance in the config.py file.

## Step 3 Running the System

Now, you are ready to run ThinkRAG.

Please run the following command in the directory containing the app.py file.

```zsh
streamlit run app.py
```

The system will run and automatically open the following URL in the browser to display the application interface.

http://localhost:8501/

The first run may take a moment. If you have not downloaded the embedding model from Hugging Face in advance, the system will automatically download the model, which will take a longer time.

<div id='Instructions'></a>

# User Guide

## 1. System Configuration

ThinkRAG supports configuration and selection of large models in the user interface, including: the Base URL and API key of the large model LLM API, and the specific model to be used, such as ZhiPu's glm-4.

<div align="center">
<img src="docs/images/Model_LLM.png" width="700" alt="file_uploads">
</a>
</div>

The system will automatically detect whether the API and key are available, and if available, display the current selected large model instance in green text at the bottom.

Similarly, the system can automatically obtain models downloaded by Ollama, and users can select the required models on the user interface.

<div align="center">
<img src="docs/images/Model_Reranker.png" width="700" alt="file_uploads">
</a>
</div>

If you have already downloaded the embedding model and reranking model to the local localmodels directory, you can switch and select the model to be used on the user interface, and set the parameters of the reranking model, such as Top N.

<div align="center">
<img src="docs/images/Settings_Advanced.png" width="700" alt="file_uploads">
</a>
</div>

In the left navigation bar, click on Advanced Settings (Settings-Advanced), and you can also set the following parameters:
- Top K
- Temperature
- System Prompt
- Response Mode

By using different parameters, we can compare the output results of large models and find the most effective parameter combination.

## 2. Knowledge Base Management

ThinkRAG supports uploading various types of files such as PDF, DOCX, PPTX, and also supports uploading web page URLs.

<div align="center">
<img src="docs/images/KB_File.png" width="700" alt="file_uploads">
</a>
</div>

Click the `Browse files` button, select the files on your computer, and then click the Load button to load, at which point all loaded files will be listed.

Then, click the `Save` button, and the system will process the files, including text splitting and embedding, and save them to the knowledge base.

<div align="center">
<img src="docs/images/KB_Web.png" width="700" alt="file_uploads">
</a>
</div>

Similarly, you can enter or paste the web page URL to obtain web page information, process it, and save it to the knowledge base.

The system supports knowledge base management.

<div align="center">
<img src="docs/images/KB_Manage.png" width="700" alt="file_uploads">
</a>
</div>

As shown in the figure above, ThinkRAG can list all documents in the knowledge base in pages.

Select the document to be deleted, and the Delete selected documents button will appear, click the button to delete the document from the knowledge base.

## 3. Query

In the left navigation bar, click on `Query`, and the Q&A page will appear.

After entering the question, the system will search the knowledge base and provide an answer. In this process, the system will use hybrid retrieval and reranking technologies to obtain accurate content from the knowledge base.

For example, we have uploaded a Word document about business process management to the knowledge base.

Now enter the question: "What are the three characteristics of the process?"

<div align="center">
<img src="docs/images/Query.png" width="700" alt="file_uploads">
</a>
</div>

As shown in the figure, the system took 2.49 seconds to provide an accurate answer: The process has the characteristics of goal orientation, repetition, and processuality. At the same time, the system also provided 2 reference documents retrieved from the knowledge base.

It can be seen that ThinkRAG fully and effectively implements the function of large model retrieval and enhanced generation based on the local knowledge base.

<div id='Architecture'></a>

# Architecture

ThinkRAG is developed using the LlamaIndex data framework, with Streamlit for the front end. The development mode and production mode of the system use different technical components, as shown in the table below:

| |Development Mode|Production Mode|
|:----|:----|:----|
|RAG Framework|LlamaIndex|LlamaIndex|
|Frontend Framework|Streamlit|Streamlit|
|Embedding Model|BAAI/bge-small-zh-v1.5|BAAI/bge-large-zh-v1.5|
|Reranking Model|BAAI/bge-reranker-base|BAAI/bge-reranker-large|
|Text Splitter|SentenceSplitter|SpacyTextSplitter|
|Conversation Storage|SimpleChatStore|Redis|
|Document Storage|SimpleDocumentStore|Redis|
|Index Storage|SimpleIndexStore|Redis|
|Vector Storage|SimpleVectorStore|LanceDB|

These technical components are designed according to the Frontend, Framework, LLM, Tools, Storage, and Infrastructure, which are six parts of the architecture.

As shown in the figure below:

<div align="center">
<img src="docs/images/ThinkRAG_Architecture.png" width="700" alt="file_uploads">
</a>
</div>

<div id='Roadmap'></a>

# Roadmap

ThinkRAG will continue to optimize core functions and continuously improve the efficiency and accuracy of retrieval, including:

- Optimize the processing of documents and web pages, support multimodal knowledge bases and multimodal retrieval
- Build a knowledge graph, enhance retrieval through the knowledge graph, and reason based on the graph
- Process complex scenarios through intelligent agents, especially accurately calling other tools and data to complete tasks

At the same time, we will further improve the application architecture and enhance the user experience, mainly including:
- Design: A user interface with a sense of design and excellent user experience
- Frontend: Build a desktop client application based on Electron, React, Vite, etc., to provide users with an extremely simple way to download, install, and run
- Backend: Provide interfaces through FastAPI, and improve overall performance and scalability through technologies such as message queues

Welcome to join the ThinkRAG open source project, and together create AI products that users love!

<div id='License'></a>

# License

ThinkRAG uses the [MIT License](LICENSE).