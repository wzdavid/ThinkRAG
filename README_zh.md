<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![support: Ollama](https://img.shields.io/badge/Support-Ollama-green.svg)](https://ollama.com/) [![support: LlamaIndex](https://img.shields.io/badge/Support-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)



</div>

### 目录

- 🤔 [ThinkRAG](#What-is-ThinkRAG)
- ✨ [主要特点](#Key-Features)
- 🛫 [快速开始](#quick-start)
- 📖 [用法说明](#engine-interface-instructions)
- 🔬 [技术栈](#Modes-Comparison)
- 🧸 [模型支持](#Support-Models)
- 📄 [许可协议](#license)

<div id='What-is-ThinkRAG'></a>

# ThinkRAG 🤔

ThinkRAG 是一个设计精良的大型语言模型（LLM）检索式生成（RAG）系统，可以轻松部署在您的笔记本电脑上。该系统基于 LlamaIndex 和 Streamlit 构建，并针对中国用户在许多领域进行了优化。系统支持本地的 Ollama 语言模型，以及来自 HuggingFace 的 BAAI 嵌入和重排模型。它还支持使用 OpenAI API 以及兼容的 LLM API，如 Zhipu、DeepSeek、Moonshot 等。

<div id='Key-Features'></a>

# 主要特点 ✨

ThinkRAG 是一个为专业人士准备的、可以在个人电脑上使用本地多模态知识库的生产就绪系统，在这个系统中，私人数据永远不会离开您的电脑。

- 完全应用 LlamaIndex
- 支持本地存储，无需安装数据库
- 无需 GPU 支持即可在笔记本电脑上轻松运行
- 支持本地模型和离线使用

以下是针对中国用户的一些特性：
- 使用 Spacy 文本分割器，更好地处理中文字符
- 采用中文标题增强功能
- 使用中文的提示模板进行问答和细化过程
- 支持中国本地用户使用的 LLM 服务提供商，如 Zhipu、DeepSeek 和 Moonshot
- 使用双语嵌入模型，如 BAAI/bge-large-zh-v1.5

<div id='quick-start'></a>

# 快速开始 🛫

## Step 1

```zsh
pip3 install -r requirements.txt
```

## Step 2

您可以将模型（BAAI/bge-large-zh-v1.5, BAAI/bge-reranker-base）下载到本地计算机上，以防您需要在没有互联网连接的情况下运行系统。

请参阅此[说明](Instructions.md)，了解如何将模型从 HuggingFace 下载到您的 "localmodels" 目录中。


## Step 3

为了获得更好的性能，建议使用 LLM API。

1. 从 LLM 服务提供商处获取您的 API 密钥，并按照以下方式配置环境变量。您可以选择使用其中一个或多个，并在 config.py 文件中删除其他模型服务商。当然，您也可以在文件中添加其他兼容的 LLM API 服务商。

```zsh
ZHIPU_API_KEY = ""
MOONSHOT_API_KEY = ""
DEEPSEEK_API_KEY = ""
OPENAI_API_KEY = ""
```

2. 如果您更倾向于使用本地 LLM，可以通过 Ollama 来实现。请首先下载 [Ollama](https://ollama.com/download)。然后使用 Ollama 命令下载如 Gemma 和 QWen 等 [模型](https://ollama.com/library)。

您可以在 Ollama 官网上找到它提供的完整 LLM 列表。

## step 4

ThinkRAG 默认以开发模式运行。

请按照以下方式配置环境变量 THINKRAG_ENV 以切换到生产模式。

```zsh
THINKRAG_ENV = prod
```

请参阅[详细比较](#Modes-Comparison)以了解两种模式的详细信息。

## Step 5

现在您已经准备好运行 ThinkRAG。请在包含 app.py 文件的目录中运行以下命令。

```zsh
streamlit run app.py
```

<div align="center">
<img src="web/src/Home_Page.png" width="700" alt="the_knowledge_base_is_empty">
</a>
</div>

<div id='engine-interface-instructions'></a>

# 用法说明 📖

有关如何使用 ThinkRAG 以及如何根据您的目的进行定制的详细说明，请参考此[文档](Instructions.md)。

<div id='Modes-Comparison'></a>

# 技术栈 🔬

| |开发模式|生产模式|
|:----|:----|:----|
|RAG框架|LlamaIndex|LlamaIndex|
|前端框架|Streamlit|Streamlit|
|嵌入模型|BAAI/bge-small-zh-v1.5|BAAI/bge-large-zh-v1.5|
|重排模型|BAAI/bge-reranker-base|BAAI/bge-reranker-large|
|文本分割器|SentenceSplitter|SpacyTextSplitter|
|对话存储|SimpleChatStore|Redis|
|文档存储|SimpleDocumentStore|Redis|
|索引存储|SimpleIndexStore|Redis|
|向量存储|SimpleVectorStore|Chroma|

<div id='Support-Models'></a>

# 模型支持 🧸

由 Ollama 支持的所有大语言模型（LLM），OpenAI，以及Zhipu、Moonshot、DeepSeek 等所有与 OpenAI 兼容的 LLM API。

<div id='license'></a>

# 协议 📄

ThinkRAG 使用 MIT 协议. 详情见[此处](LICENSE).