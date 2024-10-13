# Create LLM with API compatible with OpenAI
from llama_index.core import Settings
from langchain_openai import ChatOpenAI
from llama_index.llms.langchain import LangChainLLM

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
        print(f"An error occurred while verifying the LLM API: {type(e).__name__}: {e}")
        return False
