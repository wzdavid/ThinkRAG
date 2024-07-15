import os

STORAGE_DIR = "storage"  # directory to cache the generated index
DATA_DIR = "data"  # directory containing the documents to index
MODEL_DIR = "localmodels"  # directory containing the model files, use None if use remote model

# 模型运行设备。设为"auto"会自动检测(会有警告)，也可手动设定为 "cuda","mps","cpu","xpu" 其中之一。
LLM_DEVICE = "auto"
EMBEDDING_DEVICE = "auto"

# LLM相关配置

HISTORY_LEN = 3

MAX_TOKENS = 2048

TEMPERATURE = 0.7

OLLAMA_API_URL = "http://localhost:11434"

# 模型API配置，在环境变量中设置KEY
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

LLM_API_LIST = {
    # 智谱 API
    "Zhipu": {
        "api_key": ZHIPU_API_KEY,
        "api_base": "https://open.bigmodel.cn/api/paas/v4/",
        "models": ["glm-4","glm-4v","glm-3-turbo"],
        "provider": "智谱",
    },
    # 月之暗面 API
    "Moonshot": {
        "api_key": MOONSHOT_API_KEY,
        "api_base": "https://api.moonshot.cn/v1/",
        "models": ["moonshot-v1-8k","moonshot-v1-32k","moonshot-v1-128k"],
        "provider": "月之暗面",
    },
    # 深度求索 API
    "DeepSeek": {
        "api_key": DEEPSEEK_API_KEY,
        "api_base": "https://api.deepseek.com/v1/",
        "models": ["deepseek-chat","deepseek-coder"],
        "provider": "月之暗面",
    },
}

# 文本分割配置

DEFAULT_CHUNK_SIZE = 2048
DEFAULT_CHUNK_OVERLAP = 512
ZH_TITLE_ENHANCE = False # 中文标题加强

# 存储配置

MONGO_URI = "mongodb://localhost:27017"
REDIS_URI = "redis://localhost:6379"
ES_URI = "http://localhost:9200"

# 默认使用的向量数据库类型，包括 "es" 和 "chroma"
DEFAULT_VS_TYPE = "es"

# 聊天记录存储类型，包括"simple"和"redis"
DEFAULT_CHAT_STORE = "redis"
CHAT_STORE_FILE_NAME = "chat_store.json"
CHAT_STORE_KEY = "user1"

# 使用HuggingFace模型，配置国内镜像
HF_ENDPOINT = "https://hf-mirror.com" # 默认 "https://huggingface.co"

# 配置Embedding模型
DEFAULT_EMBEDDING_MODEL = "bge-small-zh-v1.5"
EMBEDDING_MODEL_PATH = {
    "bge-small-zh-v1.5": "BAAI/bge-small-zh-v1.5",
    "bge-base-zh-v1.5": "BAAI/bge-base-zh-v1.5",
    "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
    "bce-embedding-base_v1": "InfiniFlow/bce-embedding-base_v1",
}

# 配置Reranker模型
DEFAULT_RERANKER_MODEL = "bge-reranker-base"
RERANKER_MODEL_PATH = {
    "bge-reranker-large": "BAAI/bge-reranker-large",
    "bge-reranker-base": "BAAI/bge-reranker-base",
    "bce-reranker-base_v1": "InfiniFlow/bce-reranker-base_v1",
}

# 是否启用reranker模型
USE_RERANKER = True
RERANKER_MODEL_TOP_N = 2
RERANKER_MAX_LENGTH = 1024

# 开发还是生产环境
DEV_MODE = True

# 用于创建IndexManager
DEFAULT_INDEX_NAME = "knowledge_base"

# nltk 模型存储路径, 默认为项目根目录下的localmodels/nltk, 用于unstrucutred库
NLTK_DATA_PATH = os.path.join(os.getcwd(), MODEL_DIR, "nltk_data")