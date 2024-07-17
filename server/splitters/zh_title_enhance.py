# Chinese title enhance
# Source：LangchainChatChat, QAnything

from llama_index.core.schema import BaseNode # modified based on Document in Langchain
from typing import List
import re


def under_non_alpha_ratio(text: str, threshold: float = 0.5):
    """Checks if the proportion of non-alpha characters in the text snippet exceeds a given
    threshold. This helps prevent text like "-----------BREAK---------" from being tagged
    as a title or narrative text. The ratio does not count spaces.

    Parameters
    ----------
    text
        The input string to test
    threshold
        If the proportion of non-alpha characters exceeds this threshold, the function
        returns False
    """
    if len(text) == 0:
        return False

    alpha_count = len([char for char in text if char.strip() and char.isalpha()])
    total_count = len([char for char in text if char.strip()])
    try:
        ratio = alpha_count / total_count
        return ratio < threshold
    except:
        return False


def is_possible_title(
        text: str,
        title_max_word_length: int = 20,
        non_alpha_threshold: float = 0.5,
) -> bool:
    """Checks to see if the text passes all of the checks for a valid title.

    Parameters
    ----------
    text
        The input text to check
    title_max_word_length
        The maximum number of words a title can contain
    non_alpha_threshold
        The minimum number of alpha characters the text needs to be considered a title
    """

    # If the text length is zero, it is not a title
    if len(text) == 0:
        print("Not a title. Text is empty.")
        return False

    # If the text has punctuation, it is not a title
    ENDS_IN_PUNCT_PATTERN = r"[^\w\s]\Z"
    ENDS_IN_PUNCT_RE = re.compile(ENDS_IN_PUNCT_PATTERN)
    if ENDS_IN_PUNCT_RE.search(text) is not None:
        return False

    # The text length must not exceed the set value, which is set to be 20 by default.
    # NOTE(robinson) - splitting on spaces here instead of word tokenizing because it
    # is less expensive and actual tokenization doesn't add much value for the length check
    if len(text) > title_max_word_length:
        return False

    # The ratio of numbers in the text should not be too high, otherwise it is not a title.
    if under_non_alpha_ratio(text, threshold=non_alpha_threshold):
        return False

    # NOTE(robinson) - Prevent flagging salutations like "To My Dearest Friends," as titles
    if text.endswith((",", ".", "，", "。")):
        return False

    if text.isnumeric():
        print(f"Not a title. Text is all numeric:\n\n{text}")  # type: ignore
        return False

    # "The initial characters should contain numbers, typically within the first 5 characters by default."
    if len(text) < 5:
        text_5 = text
    else:
        text_5 = text[:5]
    alpha_in_text_5 = sum(list(map(lambda x: x.isnumeric(), list(text_5))))
    if not alpha_in_text_5:
        return False

    return True


def zh_title_enhance(docs: List[BaseNode]) -> List[BaseNode]: # modified based on Document in Langchain
    title = None
    if len(docs) > 0:
        for doc in docs:
            if is_possible_title(doc.text): # modified based on doc.page_content in Langchain
                doc.metadata['category'] = 'cn_Title'
                title = doc.text
            elif title:
                doc.text = f"下文与({title})有关。{doc.text}"
        return docs
    else:
        print("文件不存在")

# The following is an encapsulation based on LlamaIndex

import re
from llama_index.core.schema import TransformComponent

class ChineseTitleExtractor(TransformComponent):
    def __call__(self, nodes, **kwargs):
        nodes = zh_title_enhance(nodes)
        return nodes