import re
from services.llm_reranker import rerank_with_llm
from utils.helpers import cosine_similarity

def build_query(record):
    return f"{record['source_table']} | {record['source_column']} | {record['source_data_type']} | {record['source_column_description']}"

def match_source_to_target(source_records, vector_store, embeddings):
    results = []

    for record in source_records:
        query = build_query(record)
        query_vector = embeddings.embed_query(query)
        matches = vector_store.similarity_search(query, k=3)
        match_texts = [m.page_content for m in matches]

        llm_result = rerank_with_llm(record, match_texts)
        match_number = re.search(r"Match:\s*(\d+)", llm_result)
        target_index = int(match_number.group(1)) - 1 if match_number else 0

        if target_index >= len(match_texts): continue

        match_string = match_texts[target_index]
        match_dict = {kv.split(":")[0].strip(): kv.split(":", 1)[1].strip() for kv in match_string.split(" | ") if ":" in kv}
        sim_score = cosine_similarity(query_vector, embeddings.embed_query(match_string))
        confidence_score = round(sim_score * 100, 2)

        results.append({
            "source_table": record["source_table"],
            "source_column": record["source_column"],
            "source_data_type": record["source_data_type"],
            "source_column_description": record["source_column_description"],
            "target_table": match_dict.get("TableName", ""),
            "target_column": match_dict.get("ColumnName", ""),
            "target_data_type": "Unknown",
            "target_column_description": match_dict.get("ColumnDescription", ""),
            "confidence_score": confidence_score,
            "match_type": "Best Match" if "Best Match" in llm_result else "Potential Match"
        })

    return results