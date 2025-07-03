from fastapi import FastAPI, UploadFile, File
from langgraph_runner import get_langgraph_app, MetadataInput
from utils.helpers import parse_excel_to_table_data
import pandas as pd
import tempfile
# app/main.py

from fastapi import FastAPI, Depends
from security import get_api_key
from services.embedding_service import load_vector_store
import shutil



app = FastAPI()
workflow = get_langgraph_app()

vector_store, embeddings = load_vector_store()

@app.post("/generate_metadata/")
async def generate_metadata(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key)
):
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Now read Excel from tmp_path
    table_data = parse_excel_to_table_data(tmp_path)
    input_data = {"table_data": table_data}

    result = workflow.invoke(input_data)
    return result["table_data"]


from fastapi import FastAPI
from models.schema import SourceColumnRecord, MappingResult
from services.embedding_service import load_vector_store
from services.metadata_service import match_source_to_target
from typing import List

vector_store, embeddings = load_vector_store()

# @app.post("/generate-mappings", response_model=List[MappingResult])
# def generate_mappings(records: List[SourceColumnRecord]):
#     input_records = [record.dict() for record in records]
#     results = match_source_to_target(input_records, vector_store, embeddings)
#     return results

from io import BytesIO
from services.embedding_service import load_vector_store
from services.metadata_service import match_source_to_target

@app.post("/generate_mappings_excel")
async def generate_mappings_excel(file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    # Read Excel file
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), sheet_name="DataDictionaryTemplate")

    required_columns = ["source_table", "source_column", "source_data_type", "source_column_description"]
    if not all(col in df.columns for col in required_columns):
        return {"error": f"Missing columns in sheet. Required: {required_columns}"}

    # Prepare input data
    input_records = df[required_columns].dropna().to_dict(orient="records")

    # Load FAISS vector store and embeddings
    vector_store, embeddings = load_vector_store()

    # Run metadata matching logic
    results = match_source_to_target(input_records, vector_store, embeddings)

    return results