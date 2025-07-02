from fastapi import FastAPI, UploadFile, File
from langgraph_runner import get_langgraph_app, MetadataInput
from utils import parse_excel_to_table_data
import pandas as pd
import tempfile
# app/main.py

from fastapi import FastAPI, Depends
from security import get_api_key



app = FastAPI()
workflow = get_langgraph_app()

# @app.post("/generate_metadata/")
# async def generate_metadata(file: UploadFile = File(...)):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
#         tmp.write(await file.read())
#         tmp_path = tmp.name

#     table_data = parse_excel_to_table_data(tmp_path)
#     input_data = {"table_data": table_data}

#     result = workflow.invoke(input_data)
#     return result["table_data"]
# app/main.py


@app.post("/generate_metadata/")
async def generate_metadata(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    table_data = parse_excel_to_table_data(tmp_path)
    input_data = {"table_data": table_data}

    result = workflow.invoke(input_data)
    return result["table_data"]
