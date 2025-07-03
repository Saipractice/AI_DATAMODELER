import numpy as np
import pandas as pd

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


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




def enforce_consistent_metadata(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("TableName")
    for table_name, group in grouped:
        base_classification = group["SecurityClassification"].mode()[0]
        base_domain = group["Domain"].mode()[0]
        base_subdomain = group["SubDomain"].mode()[0]
        base_description = group["TableDescription"].mode()[0]

        for idx in group.index:
            col_name = df.loc[idx, "ColumnName"]
            if "name" in col_name or "id" in col_name:
                continue  # allow exception for PII/identifier if needed
            df.loc[idx, "SecurityClassification"] = base_classification
            df.loc[idx, "Domain"] = base_domain
            df.loc[idx, "SubDomain"] = base_subdomain
            df.loc[idx, "TableDescription"] = base_description
    return df