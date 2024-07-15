# https://docs.llamaindex.ai/en/stable/examples/customization/prompts/completion_prompts/
# https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py
# https://docs.llamaindex.ai/en/stable/module_guides/models/prompts/usage_pattern/

from llama_index.core import PromptTemplate

text_qa_template_str = (
    "以下为上下文信息\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "请根据上下文信息回答我的问题或回复我的指令。前面的上下文信息可能有用，也可能没用，你需要从我给出的上下文信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。我的问题或指令是什么语种，你就用什么语种回复。\n"
    "问题：{query_str}\n"
    "你的回复： "
)


text_qa_template = PromptTemplate(text_qa_template_str)

refine_template_str = (
    "这是原本的问题： {query_str}\n"
    "我们已经提供了回答: {existing_answer}\n"
    "现在我们有机会改进这个回答 "
    "使用以下更多上下文（仅当需要用时）\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "根据新的上下文, 请改进原来的回答。"
    "如果新的上下文没有用, 直接返回原本的回答。\n"
    "改进的回答: "
)
refine_template = PromptTemplate(refine_template_str)
