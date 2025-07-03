import streamlit as st
import pandas as pd
import requests

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="AI Metadata Tools", layout="wide", page_icon="🧠")

# ---------------------- Top Header -----------------------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <img src="https://img.icons8.com/clouds/100/brain.png" width="60"/>
            <h1 style="margin-bottom: 0;">AI Metadata Tools</h1>
            <p style="color: gray; margin-top: 0;">Empowered by LLMs · Built with <b>Openai , Huggingface and FAISS</b></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------- Sidebar ---------------------------
with st.sidebar:
    st.markdown("## 🔧 Settings", unsafe_allow_html=True)
    api_key_input = st.text_input("🔐 API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("API Key saved")
    tool = st.radio("🧰 Select Tool", ["Metadata Generator", "Metadata Mapper"])
    st.markdown("---")
    st.markdown("👩‍💻 Powered by **Infosys Technologies**", unsafe_allow_html=True)

api_key = st.session_state.get("api_key", "")
BASE_URL = "http://127.0.0.1:8000"
HEADERS = {"x-api-key": api_key}

# --------------------- Utility ---------------------------
def preview_excel(file, sheet_name=None):
    try:
        df = pd.read_excel(file, sheet_name=sheet_name) if sheet_name else pd.read_excel(file)
        st.markdown("### 📄 File Preview")
        st.dataframe(df.head(10), use_container_width=True)
        return df
    except Exception as e:
        st.error(f"❌ File error: {e}")
        return None

# --------------------- Tool 1: Metadata Generator ---------------------
if tool == "Metadata Generator":
    st.markdown("## 📝 Generate Enriched Metadata")
    st.info("Upload an Excel file to generate domain, subdomain, column descriptions, and security classification.")

    uploaded_file = st.file_uploader("📎 Upload Excel file (e.g., Testcase_1.xlsx)", type=["xlsx"], key="metadata_file")

    if uploaded_file:
        preview_excel(uploaded_file)

    if uploaded_file and st.button("🚀 Generate Metadata"):
        with st.spinner("Calling AI to generate metadata..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                }
                response = requests.post(f"{BASE_URL}/generate_metadata/", files=files, headers=HEADERS)
                if response.status_code == 200:
                    df_result = pd.DataFrame(response.json())
                    st.success("✅ Metadata generated successfully!")
                    st.dataframe(df_result, use_container_width=True)
                else:
                    st.error(f"❌ API Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# --------------------- Tool 2: Metadata Mapper ---------------------
elif tool == "Metadata Mapper":
    st.markdown("## 🔁 Generate Source-to-Target Mappings")
    st.info("Upload a metadata Excel file to generate AI-based source-to-target column mappings.")

    uploaded_file = st.file_uploader("📎 Upload Excel file (e.g., Testcase_1.xlsx)", type=["xlsx"], key="mapping_file")

    if uploaded_file:
        preview_excel(uploaded_file, sheet_name="DataDictionaryTemplate")

    if uploaded_file and st.button("🚀 Generate Mappings"):
        with st.spinner("Analyzing and matching columns..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                }
                response = requests.post(f"{BASE_URL}/generate_mappings_excel", files=files, headers=HEADERS)
                if response.status_code == 200:
                    df_result = pd.DataFrame(response.json())
                    st.success("✅ Mappings generated!")
                    st.dataframe(df_result, use_container_width=True)
                else:
                    st.error(f"❌ API Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# --------------------- Footer ---------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 | Developed  by <strong>Sai Vineela</strong>"
    "</div>",
    unsafe_allow_html=True
)