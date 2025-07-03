from pydantic import BaseModel
from langgraph.graph import StateGraph
from openai import OpenAI
from prompt import DOMAIN_SUBDOMAIN_PROMPT_TEMPLATE
from utils import log
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Define a Pydantic model manually
class MetadataInput(BaseModel):
    table_data: list[dict]

def run_metadata_agent(table_data: list[dict]):
    log.info("Creating LangGraph workflow")

    def generate_metadata_fn(state):
        enriched = []
        for row in state.table_data:  # ✅ Access as attribute, not dictionary
            prompt = DOMAIN_SUBDOMAIN_PROMPT_TEMPLATE.format(
                table_name=row["TableName"],
                column_name=row["ColumnName"],
                Sample_Data=row.get("SubjectArea", "")  # ✅ Use Sample_Data to match template
            )
            log.info(f"Calling OpenAI with row: {row}")
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    timeout=10
                )
                text = response.choices[0].message.content.strip()
                row.update(json.loads(text))  # ✅ Safe JSON parsing instead of eval()
            except Exception as e:
                log.error(f"Failed to enrich metadata: {e}")
            enriched.append(row)
        return {"table_data": enriched}

    # ✅ Pass schema to StateGraph using the real Pydantic class
    graph = StateGraph(state_schema=MetadataInput)
    graph.add_node("generate", generate_metadata_fn)
    graph.set_entry_point("generate")
    graph.set_finish_point("generate")

    app = graph.compile()
    final_state = app.invoke({"table_data": table_data})
    return final_state.table_data  # ✅ Access as attribute, not dictionary
