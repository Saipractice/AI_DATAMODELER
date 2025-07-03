from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from openai import AzureOpenAI  # ✅ Azure OpenAI client
import logging
import os

from prompts import Metadata_Prompt_Template
from utils.helpers import parse_metadata_response

# Load .env
load_dotenv()

USE_AZURE = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"

if USE_AZURE:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # This is the deployment name, not model ID
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = "gpt-4"  # fallback default



logger = logging.getLogger(__name__)

class MetadataInput(BaseModel):
    table_data: list[dict]

def generate_metadata_fn(state: MetadataInput):
    enriched_rows = []
    for row in state.table_data:
        prompt = Metadata_Prompt_Template.format(
            TableName=row["TableName"],
            ColumnName=row["ColumnName"],
            SubjectArea=row.get("SubjectArea", "")
        )
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            response_text = response.choices[0].message.content.strip()
            parsed = parse_metadata_response(response_text)
            row.update(parsed)
        except Exception as e:
            row["Error"] = f"OpenAI Error: {str(e)}"
        enriched_rows.append(row)
    return MetadataInput(table_data=enriched_rows)


def get_langgraph_app():
    graph = StateGraph(state_schema=MetadataInput)
    graph.add_node("generate", generate_metadata_fn)
    graph.set_entry_point("generate")
    graph.set_finish_point("generate")
    return graph.compile()


