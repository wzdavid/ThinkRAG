<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![support: LanceDB](https://img.shields.io/badge/Support-LanceDB-blue.svg)](https://lancedb.com/) [![support: Ollama](https://img.shields.io/badge/Support-Ollama-green.svg)](https://ollama.com/) [![support: LlamaIndex](https://img.shields.io/badge/Support-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)



</div>

### 目录

- 🤔 [ThinkRAG](#What-is-ThinkRAG)
- ✨ [主要特点](#Key-Features)
- 🛫 [快速开始](#quick-start)
- 📖 [用法说明](#engine-interface-instructions)
- 🔬 [技术栈](#Modes-Comparison)
- 🧸 [模型支持](#Support-Models)
- 📄 [协议](#license)

<div id='What-is-ThinkRAG'></a>

# ThinkRAG 🤔

ThinkRAG 是一个基于 LlamaIndex 和 Streamlit 的大型语言模型（LLM）RAG 系统，专为中国用户优化。它整合了 BAAI 嵌入/重排序模型和 Ollama 本地模型，并利用来自 Zhipu、DeepSeek 和 Moonshot 等中国服务提供商的 LLM API。


<div id='Key-Features'></a>

# 主要特点 ✨

ThinkRAG 特别为中国用户量身定制，具备多项关键功能：

- 完整实现 LlamaIndex，使 RAG 系统能够在个人电脑上完美运行。Ollama 模型还确保了个人数据的隐私，并实现在本地的完整实施。
- 为中文字符特别设计的 Spacy 文本分割器和中文标题增强功能（参考 Langchain-Chatchat, QAnything）。
- 为问答和精炼回答过程量身定制的中文提示模板。
- Zhipu、DeepSeek 和 Moonshot 等大型中文语言模型。
- Hugging Face 的中文嵌入模型（BAAI/bge-large-zh-v1.5），为中文任务设计，以达到最佳性能。

<div id='quick-start'></a>

# 快速开始 🛫

## Step 1

```zsh
pip3 install -r requirements.txt
```

## Step 2

您可以选择下载并调用嵌入模型 BAAI/bge-large-zh-v1.5 和 BAAI/bge-reranker-base。具体请参考[此文档](Instructions_zh.md)，了解如何将模型下载到 localmodels 目录中。

## Step 3

根据您打算使用的模型，将对应的 API 密钥设置为全局变量，或从官方网站下载模型（Ollama）：

1. 要将您的 API 密钥设置为全局变量，支持的大型语言模型（LLMs）的变量名称如下：

```zsh
ZHIPU_API_KEY = ""
MOONSHOT_API_KEY = ""
DEEPSEEK_API_KEY = ""
OPENAI_API_KEY = ""
```

2. 若使用 Ollama 模型，建议您从库中下载 [Ollama](https://ollama.com/download) 和选择的[模型](https://ollama.com/library)，如 gemma 和 llama（所有 Ollama 模型均受支持）。

## step 4

请注意，ThinkRAG 当前支持开发模式（默认设置）和生产模式。要切换到生产模式，请将 THINKRAG_ENV 设置为全局变量：

```zsh
THINKRAG_ENV = prod
```

有关这两种模式的区别，请参阅[技术栈](#Modes-Comparison).

## Step 5

要运行 ThinkRAG，请执行以下命令（事先确保您位于 ThinkRAG 的根目录）：

```zsh
streamlit run app.py
```

<div align="center">
<img src="web/src/Home_Page.png" width="700" alt="the_knowledge_base_is_empty">
</a>
</div>

<div id='engine-interface-instructions'></a>

# 用法说明 📖

有关 ThinkRAG 关键功能的详细说明以及如何根据您的具体需求调整这些功能，请参考这份[文档](Instructions_zh.md)。

<div id='Modes-Comparison'></a>

# 技术栈 🔬

| |开发模式（DEV_MODE）|生产模式（PROD_MODE）|
|:----|:----|:----|
|框架|LlamaIndex|LlamaIndex|
|前段|Streamlit|Streamlit|
|嵌入模型|BAAI/bge-large-zh-v1.5 & BAAI/bge-reranker-base|BAAI/bge-large-zh-v1.5 & BAAI/bge-reranker-base|
|巡回检索|FusionRetriever|HybridRetriever|
|文本分割器|SentenceSplitter|SpacyTextSplitter|
|对话存储|SimpleChatStore|Redis|
|文档存储|SimpleDocumentStore|Redis or MangoDB|
|索引存储|SimpleIndexStore|Redis or MangoDB|
|向量存储|SimpleVectorStore|LanceDB as default, Chroma and ES available.|

<div id='Support-Models'></a>

# 模型支持 🧸

Ollama, Zhipu, Moonshot, DeepSeek, OpenAI

<div id='license'></a>

# 协议 📄

ThinkRAG 使用 MIT 协议. 详情见[此处](LICENSE).