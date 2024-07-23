## Create Your Own Knowledge Base 👤

ThinkRAG, as a local LLM knowledge base Q&A system, needs a non-empty knowledge base to function.

<div align="center">
<img src="web/src/the_knowledge_base_is_empty.png" width="350" alt="the_knowledge_base_is_empty">
</a>
</div>

</br>
For first-time users, the first thing you need to do before moving forward is to create your own knowledge base.

### ThinkRAG currently support file uploads and URL uploads: 

#### File Uploads ⏫

<div align="center">
<img src="web/src/file_uploads.png" width="350" alt="file_uploads">
</a>
</div>

</br>
This section of the interface is designed for uploading and managing files(all frequently-used file types) in the knowledge base. It features:

&emsp;&emsp; A drag-and-drop area and an upload button for adding files, with a size limit of 200MB per file.

&emsp;&emsp; Settings for configuring text processing parameters, such as the length of text blocks and the overlap between them, with an option to enhance Chinese title processing.

&emsp;&emsp; A button to generate an index for the uploaded files, facilitating easier search and retrieval within the knowledge base. 

<br/>

#### URL Uploads ⏫

<div align="center">
<img src="web/src/url_uploads.png" width="350" alt="url_uploads">
</a>
</div>

</br>
This interface is focused on adding and processing web page URLs in the knowledge base. It includes:

&emsp;&emsp; A field and a button for adding URLs of web pages to be processed.

&emsp;&emsp; Similar text processing settings as the file upload section, ensuring consistency in how content is handled regardless of the source.

&emsp;&emsp; A generate index button that processes the URLs to make the web content searchable within the knowledge base.

<br/>

<div align="center">
<img src="web/src/knowledge_base_content.png" width="350" alt="knowledge_base_content">
</a>
</div>

</br>
Once you've uploaded successfully, you may check out the content in the knowledge base in the Knowledge Base Management interface.

#### Please Note ⚠️
*You are gonna have to generate the index after customized you preferrd text processing parameters (or keep them as defaults), otherwise the retrieval will not function properly.*




</br></br>

## Settings ⚙️

<div align="center">
<img src="web/src/settings_1.png" width="350" alt="settings_1">
</a>
</div>


<div align="center">
<img src="web/src/settings_2.png" width="350" alt="settings_2">
</a>
</div>

</br>
As the interface for managing settings related to API services and advanced configurations, it allows users to manage and configure settings for different types of API services:

&emsp;&emsp; Ollama API: Here, users can set and view the address for the Ollama API service, check its status, refresh and select available models.

&emsp;&emsp; LLMs API: This part lets users view and manage settings for various large language models APIs.

&emsp;&emsp; Embedding Models: Users can choose and configure embedding models, enabling re-ranking capabilities and selecting specific re-ranker models.

&emsp;&emsp; Show Advanced Settings Toggle: Allows users to view or hide advanced configuration options.

&emsp;&emsp; Top K: Adjusts the parameter for how many top results to consider in a process (range from 0 to 10).

&emsp;&emsp; System Prompt: Where users can customize the default prompt for the system.

&emsp;&emsp; Chat Mode: Provides options for how chat interactions appear (e.g., compact or full, default to be compact).

These interfaces provide comprehensive control over the application’s functionalities, enabling users to tailor the behavior of APIs and other system components according to their specific needs or preferences.




</br></br>

## Choose your preferred LLM

<div align="center">
<img src="web/src/choose_your_llms.png" width="350" alt="choose_your_llms">
</a>
</div>

</br>
As the final step for finishing the configuration, choose the LLM you like the most and you are all set! Have fun!