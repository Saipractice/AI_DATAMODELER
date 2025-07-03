from pydantic import BaseModel
from typing import List

class SourceColumnRecord(BaseModel):
    source_table: str
    source_column: str
    source_data_type: str
    source_column_description: str

class MappingResult(BaseModel):
    source_table: str
    source_column: str
    source_data_type: str
    source_column_description: str
    target_table: str
    target_column: str
    target_data_type: str
    target_column_description: str
    confidence_score: float
    match_type: str