import os

from dotenv import load_dotenv

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)

# from langchain_ollama import ChatOllama

load_dotenv()

_llm = None


def get_llm():

    global _llm

    if _llm:
        return _llm

    provider = os.getenv(
        "MODEL_PROVIDER",
        "huggingface"
    )

    # if provider == "huggingface":

    endpoint = HuggingFaceEndpoint(

        repo_id=os.getenv(
            "HF_MODEL",
            "Qwen/Qwen2.5-7B-Instruct"
        ),

        huggingfacehub_api_token=os.getenv(
            "HUGGINGFACEHUB_API_TOKEN"
        ),

        temperature=0.2,

        max_new_tokens=1024

    )

    _llm = ChatHuggingFace(
       llm=endpoint
    )

    # else:

    #     _llm = ChatOllama(

    #         model=os.getenv(
    #             "OLLAMA_MODEL",
    #             "qwen2.5:7b"
    #         )

    #     )

    return _llm