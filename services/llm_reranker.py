import os
import re
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI  # ✅ Azure LLM client
from prompts import mappings_prompt

# Load Azure OpenAI config from env vars
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize Azure Chat model
chat_model = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    deployment_name=AZURE_DEPLOYMENT,
    api_version=AZURE_API_VERSION,
    temperature=0.2
)

def rerank_with_llm(record, match_texts):
    prompt = mappings_prompt.format(
        source_column=record["source_column"],
        source_data_type=record["source_data_type"],
        source_column_description=record["source_column_description"],
        match_1=match_texts[0],
        match_2=match_texts[1],
        match_3=match_texts[2],
    )

    response = chat_model.invoke([HumanMessage(content=prompt)])
    return response.content.strip()



# Openai code

# from langchain.chat_models import ChatOpenAI
# from langchain.schema.messages import HumanMessage
# from config import OPENAI_API_KEY, MODEL_NAME
# from prompt import prompt
# chat_model = ChatOpenAI(model=MODEL_NAME, openai_api_key=OPENAI_API_KEY)

# def rerank_with_llm(record, matches):
#     if len(matches) < 3:
#         return "Insufficient matches"

#     prompt = prompt.format(
#             record=record,
#             matches=matches,
            
#         )
#     response = chat_model([HumanMessage(content=prompt)])
#     return response.content.strip()

