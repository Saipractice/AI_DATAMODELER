from langgraph.graph import StateGraph
from pydantic import BaseModel
from openai import OpenAI
import logging
from prompt import PROMPT_TEMPLATE
from utils import parse_metadata_response
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


logger = logging.getLogger(__name__)

class MetadataInput(BaseModel):
    table_data: list[dict]

def generate_metadata_fn(state: MetadataInput):
    enriched_rows = []
    for row in state.table_data:
        prompt = PROMPT_TEMPLATE.format(
            TableName=row["TableName"],
            ColumnName=row["ColumnName"],
            SubjectArea=row.get("SubjectArea", "")
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4",
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