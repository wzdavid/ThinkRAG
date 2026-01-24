# Create LLM with API compatible with OpenAI
from llama_index.core import Settings
from langchain_openai import ChatOpenAI
from llama_index.llms.langchain import LangChainLLM

def _classify_openai_error(e: Exception) -> str:
    msg = str(e)
    if "unsupported_country_region_territory" in msg:
        return "forbidden_region"
    if "Error code: 403" in msg or "403 Forbidden" in msg:
        return "forbidden_403"
    if "Error code: 401" in msg or "401 Unauthorized" in msg or "invalid_api_key" in msg:
        return "invalid_key"
    return "other"


def create_openai_llm(model_name:str, api_base:str, api_key:str, temperature:float = 0.5, system_prompt:str = None) -> ChatOpenAI:
    try:
        llm = LangChainLLM(
            llm=ChatOpenAI(
                openai_api_base=api_base, 
                openai_api_key=api_key,
                model_name=model_name,
                temperature=temperature,
            ),
            system_prompt=system_prompt,
        )
        Settings.llm = llm
        return llm
    except Exception as e:
        print(f"An error occurred while creating the OpenAI compatibale model: {type(e).__name__}: {e}")
        return None
    
def check_openai_llm(model_name, api_base, api_key) -> bool:
        # Make a simple API call to verify the key
    try:
        llm = ChatOpenAI(
            openai_api_base=api_base, 
            openai_api_key=api_key,
            model_name=model_name,
            timeout=5,
            max_retries=1
        )
        response = llm.invoke("Hello, World!")
        print(response)
        if response:
            return True
        else:
            return False
    except Exception as e:
        kind = _classify_openai_error(e)

        if kind in ("forbidden_region", "forbidden_403"):
            print(f"LLM API request forbidden (403). Region/policy may not be supported: {api_base}")
        elif kind == "invalid_key":
            print("Invalid API key (401).")
        else:
            print(f"Failed to verify LLM API: {e}")

        return False
