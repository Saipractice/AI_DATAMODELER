# import logging
# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger("metadata-logger")


import pandas as pd

def parse_excel_to_table_data(file_path: str, sheet_name: str = "DRD") -> list[dict]:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    table_data = []
    for _, row in df.iterrows():
        table_name = str(row.get("TableName", "")).strip()
        column_name = str(row.get("ColumnName", "")).strip()
        subject_area = str(row.get("SubjectArea", "")).strip()
        
        if table_name and column_name:
            table_data.append({
                "TableName": table_name,
                "ColumnName": column_name,
                "SubjectArea": subject_area
            })
    return table_data


def parse_metadata_response(response_text: str) -> dict:
    result = {
        "Domain": "",
        "SubDomain": "",
        "SecurityClassification": "",
        "TableDescription": "",
        "ColumnDescription": ""
    }
    for line in response_text.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in result:
                result[key.strip()] = value.strip()
    return result