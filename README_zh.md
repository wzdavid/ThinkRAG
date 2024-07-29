<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a>
</p>


<style>
  summary {
    font-size: 17px; /* This enlarges the triangle */
  }
  summary > span {
    font-size: 28PX; /* This reduces the text size 
    relative to the summary */
    font-weight: bold;
  }
  summary > div {
    font-size: 20PX; /* This reduces the text size 
    relative to the summary */
    font-weight: bold;
  }
</style>

<details open>
<summary><span>目录</span></summary>

- [ThinkRAG](#think-rag) 🤔
- [快速开始](#快速开始) 🔜
- [设置API密钥](#设置密钥) ⚙️
- [应用界面详解](#应用界面详解) 📖
- [模型支持](#模型支持) 🪀
- [授权条款](#授权条款) 📄

</details>


<div id='think-rag'></a>

<details open style="font-size: 14px;">
  <summary>
    <span>什么是ThinkRAG🤔</span>
  </summary>

ThinkRAG是一款基于文档检索的开源RAG引擎。

### 主要功能：
#### 知识库管理：
&emsp;&emsp; ThinkRAG 允许用户从文件（如 PDF、DOCX 和 TXT 文件）和网页上传、管理和索引内容。这包括设置文本处理参数以确保数据的最佳组织和可检索性。

#### API 配置：
&emsp;&emsp; ThinkRAG 提供了广泛的 API 配置设置，包括设置服务地址、选择模型以及启用诸如嵌入模型重排等特定功能。这有助于集成和管理各种语言和嵌入模型，以在知识库中用于增强数据处理和检索。

#### 高级设置：
&emsp;&emsp; ThinkRAG 还包括允许用户进一步优化系统行为和交互模式的高级设置，如调整响应选择标准和自定义系统提示。

#### 支持LanceDB：
&emsp;&emsp; LanceDB 作为开源多模态向量数据库，具备以下核心优势：
- 针对时间序列数据优化：专为时间序列数据设计，适合实时监控，物联网设备数据、金融交易数据等。
- 高性能处理：具有高数据吞吐率和快速查询性能，适用于实时分析。
- 可扩展性强：支持水平扩展，可以通过增加节点来处理更大的负载。
- 高效数据压缩：采用先进的数据压缩技术优化存储并提高 I/O 效率。
- 灵活的数据保留策略：支持自定义数据保留政策，自动降采样或删除旧数据。
- 强大的查询语言：提供强大而灵活的查询语言，支持数据库内复杂的数据分析和聚合。
- 内置可视化工具：可能包括集成的数据可视化和仪表盘工具，简化数据监控和分析。

浏览[LanceDB官网](https://lancedb.com/)以了解更多信息。

</br>
</details>

<div id='快速开始'></a>

<details open style="font-size: 14px;">
  <summary>
    <span>快速开始 🔜</span>
  </summary>

### Step 1
```bash
pip3 install -r requirements.txt
```
### Step 2

参考 [此处](/docs/HowToDownloadModels.md) 将嵌入模型和自然语言工具包下载进localmodels路径

### Step 3
若需使用LLMs API，请优先配置API Key，详见[设置API密钥](#设置密钥)

最后，使用以下命令来运行 ThinkRAG
```bash
streamlit run app.py
```
</br>
</details>

<div id='设置密钥'></a>


<details open style="font-size: 14px;">
  <summary>
    <span>设置密钥 ⚙️</span>
  </summary>

<details style="font-size: 14px;">
  <summary>
    <div>MacOS & Linux</div>
  </summary>

### 设置临时 API 密钥
### 1. 运行以下指令
```bash
export VARIABLE_NAME=value
```
例如，要设置OpenAI的API密钥, 则运行以下指令:
```bash
export OPENAI_API_KEY=your_OpenAI_API_key 
```
<br/>

### 设置永久 API 密钥
### 1. 创建或编辑 '.zshenv' 文件

```bash
nano ~/.zshenv
```
对于Linux, macOS Mojave (10.14) 或更早版本, 运行 
```bash
nano ~/.bashrc
```
### 2. 添加个人配置
```bash
export VARIABLE_NAME="value"
```
例如，要设置OpenAI的API密钥, 则运行以下指令:
```bash
export OPENAI_API_KEY=your_OpenAI_API_key 
```
### 3. 保存并退出
'Ctrl + O'用于保存更改, 按下'Enter'以确认并输入'Ctrl + X‘退出编辑。

### 4. 应用做出的更改
为确保更改生效，运行
```bash
source ~/.zshenv 
# source ~/.bashrc for Linux, macOS Mojave (10.14) or earlier
```
</details>

<details style="font-size: 14px;">
  <summary>
    <div>Windows</div>
  </summary>

### 运行以下命令

```bash
set VARIABLE_NAME=value # Set Temporary API Key
```

```bash
setx VARIABLE_NAME "value" -m # Set Permanent API Key
```

</br>

</details>
</details>

<div id='应用界面详解'></a>

<details open style="font-size: 14px;">
  <summary>
    <span>应用界面详解 📖</span>
  </summary>

应用界面的详细功能及操作详解，见[此处](Instructions_zh.md)

</details>

<div id='模型支持'></a>

<details open style="font-size: 14px;">
  <summary>
    <span>模型支持 🪀<span>
  </summary>


<table>
<tr>
<th> Ollama 模型 </th>
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

<div id='授权条款'></a>

<details open style="font-size: 14px;">
  <summary>
    <span>授权条款 📄<span>
  </summary>

ThinkRAG 遵循 MIT 授权条款，详情请见[此处](LICENSE)
</details>