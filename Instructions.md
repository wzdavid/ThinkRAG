# Create Your Own Knowledge Base 👤

ThinkRAG, functioning as a local LLM knowledge base Q&A system, requires a populated knowledge base to operate effectively.

For first-time users, the initial step before proceeding is to establish your own knowledge base.

<div align="center">
<img src="web/src/the_knowledge_base_is_empty.png" width="700" alt="the_knowledge_base_is_empty">
</a>
</div>

### ThinkRAG currently support file uploads and URL uploads: 

#### File Uploads ⏫

<div align="center">
<img src="web/src/file_uploads.png" width="700" alt="file_uploads">
</a>
</div>

This section of the interface is dedicated to uploading and managing files (supporting all commonly used file types) within the knowledge base. Key features include:

- A drag-and-drop area and an upload button to facilitate the addition of files, subject to a maximum size limit of 200MB per file.

- Adjustable settings for text processing parameters, such as block length and the overlap between blocks, with an enhancement option specifically for Chinese title processing.

- A feature to generate an index for the uploaded files, improving the ease of search and retrieval within the knowledge base.

<br/>

#### URL Uploads ⏫

<div align="center">
<img src="web/src/url_uploads.png" width="700" alt="url_uploads">
</a>
</div>


This interface section is tailored for adding and processing URLs within the knowledge base. It offers the following functionalities:

- A designated field and button for inputting URLs of web pages that need processing.

- Text processing settings similar to those in the file upload section, maintaining uniformity in content handling across different sources.

- A "generate index" button, which processes the added URLs to make the web content searchable and retrievable within the knowledge base.

<br/>

<div align="center">
<img src="web/src/knowledge_base_content.png" width="700" alt="knowledge_base_content">
</a>
</div>

</br>

Once you have successfully uploaded your content, you can view and manage it in the Knowledge Base Management interface.

#### Please Note ⚠️
>__*After customizing your preferred text processing parameters (or keeping them as defaults), you will need to generate the index. If the index is not created, the retrieval function will not operate correctly.*__


</details>

# Settings ⚙️

<div align="center">
<img src="web/src/settings_1.png" width="700" alt="settings_1">
</a>
</div>


<div align="center">
<img src="web/src/settings_2.png" width="700" alt="settings_2">
</a>
</div>



This interface serves as the hub for managing settings related to API services and advanced configurations, enabling users to fine-tune and oversee different types of API services:

- **Ollama API**: Users can configure the address for the Ollama API service, monitor its status, refresh, and choose from available models.

- **LLMs API**: This section allows users to view and adjust settings for various large language models' APIs.

- **Embedding Models**: Here, users can select and configure embedding models, activate re-ranking capabilities, and choose specific re-ranker models.

- **Show Advanced Settings Toggle**: This option allows users to reveal or conceal advanced configuration settings.

- **Top-K**: Adjusts the parameter to determine how many top results to consider in a process (ranging from 0 to 10).

- **System Prompt**: Users can customize the default system prompt.

- **Chat Mode**: Offers choices for the display style of chat interactions, such as compact or full (default set to compact).

These interfaces grant comprehensive control over the application's functionalities, allowing users to customize the behavior of APIs and other system components to suit their individual needs or preferences.




</br></br>
</details>

# Choose your preferred LLM 👀

</br>

<div align="center">
<img src="web/src/choose_your_llms.png" width="700" alt="choose_your_llms">
</a>
</div>

</br>
As the final step to complete the configuration, select the LLM that you prefer, and you're all set! Enjoy!