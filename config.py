import os

STORAGE_DIR = "storage"  # directory to cache the generated index
DATA_DIR = "data"  # directory containing the documents to index
MODEL_DIR = "localmodels"  # directory containing the model files, use None if use remote model
CONFIG_STORE_FILE = "config_store.json" # local storage for configurations

# The device that used for running the model. 
# Set it to 'auto' will automatically detect (with warnings), or it can be manually set to one of 'cuda', 'mps', 'cpu', or 'xpu'.
LLM_DEVICE = "auto"
EMBEDDING_DEVICE = "auto"

# LLM Settings

HISTORY_LEN = 3

MAX_TOKENS = 2048

TEMPERATURE = 0.1

TOP_K = 5

SYSTEM_PROMPT = "You are an AI assistant that helps users to find accurate information. You can answer questions, provide explanations, and generate text based on the input. Please answer the user's question exactly in the same language as the question or follow user's instructions. For example, if user's question is in Chinese, please generate answer in Chinese as well. If you don't know the answer, please reply the user that you don't know. If you need more information, you can ask the user for clarification. Please be professional to the user."

RESPONSE_MODE = [   # Configure the response mode of the query engine
            "compact",
            "refine",
            "tree_summarize",
            "simple_summarize",
            "accumulate",
            "compact_accumulate",
]
DEFAULT_RESPONSE_MODE = "simple_summarize"

OLLAMA_API_URL = "http://localhost:11434"

# Models' API configuration，set the KEY in environment variables
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

LLM_API_LIST = {
    # Ollama API
    "Ollama": {
        "api_base": OLLAMA_API_URL,
        "models": [],
        "provider": "Ollama",
    },
    # OpenAI API
    "OpenAI": {
        "api_key": OPENAI_API_KEY,
        "api_base": "https://api.openai.com/v1/",
        "models": ["gpt-4", "gpt-3.5", "gpt-4o"],
        "provider": "OpenAI",
    },
    # ZhiPu API
    "Zhipu": {
        "api_key": ZHIPU_API_KEY,
        "api_base": "https://open.bigmodel.cn/api/paas/v4/",
        "models": ["glm-4-plus", "glm-4-0520", "glm-4", "glm-4-air", "glm-4-airx", "glm-4-long", "glm-4-flashx", "glm-4-flash", "glm-4v-plus", "glm-4v"],
        "provider": "Zhipu",
    },
    # Moonshot API
    "Moonshot": {
        "api_key": MOONSHOT_API_KEY,
        "api_base": "https://api.moonshot.cn/v1/",
        "models": ["moonshot-v1-8k","moonshot-v1-32k","moonshot-v1-128k"],
        "provider": "Moonshot",
    },
    # DeepSeek API
    "DeepSeek": {
        "api_key": DEEPSEEK_API_KEY,
        "api_base": "https://api.deepseek.com/v1/",
        "models": ["deepseek-chat"],
        "provider": "DeepSeek",
    },
}

# Text splitter configuration

DEFAULT_CHUNK_SIZE = 2048
DEFAULT_CHUNK_OVERLAP = 512
ZH_TITLE_ENHANCE = False # Chinese title enhance

# Storage configuration

MONGO_URI = "mongodb://localhost:27017"
REDIS_URI = "redis://localhost:6379"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
ES_URI = "http://localhost:9200"

# Default vector database type, including "es" and "chroma"
DEFAULT_VS_TYPE = "es"

# Chat store type，including "simple" and "redis"
DEFAULT_CHAT_STORE = "redis"
CHAT_STORE_FILE_NAME = "chat_store.json"
CHAT_STORE_KEY = "user1"

# Use HuggingFace model，Configure domestic mirror
HF_ENDPOINT = "https://hf-mirror.com" # Default to be "https://huggingface.co"

# Configure Embedding model
DEFAULT_EMBEDDING_MODEL = "bge-small-zh-v1.5"
EMBEDDING_MODEL_PATH = {
    "bge-small-zh-v1.5": "BAAI/bge-small-zh-v1.5",
    "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
}

# Configure Reranker model
DEFAULT_RERANKER_MODEL = "bge-reranker-base"
RERANKER_MODEL_PATH = {
    "bge-reranker-base": "BAAI/bge-reranker-base",
    "bge-reranker-large": "BAAI/bge-reranker-large",
}

# Use reranker model or not
USE_RERANKER = False
RERANKER_MODEL_TOP_N = 2
RERANKER_MAX_LENGTH = 1024

# Evironment variable, default to be "development", set to "production" for production environment
THINKRAG_ENV = os.getenv("THINKRAG_ENV", "development")
DEV_MODE = THINKRAG_ENV == "development"

# For creating IndexManager
DEFAULT_INDEX_NAME = "knowledge_base"