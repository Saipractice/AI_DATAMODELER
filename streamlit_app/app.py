import streamlit as st
import requests
import pandas as pd
from pathlib import Path
import sys
# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))
from utils.helpers import enforce_consistent_metadata
import os
from dotenv import load_dotenv
load_dotenv()

# ------------------ Page Configuration ------------------
st.set_page_config(
    page_title="AI Metadata Tools",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.title("🧭 Navigation")
    tool = st.radio("Choose Tool", ["📝 Metadata Generator", "🧠 Source to Target Mapper"])
    st.markdown("### 🔐 Configuration")
    api_key = st.text_input("Enter your API Key", type="password")
    st.markdown("---")
    st.image("assets/Infosys.png", width=130)
    st.markdown("👩‍💻 Partnered with **Infosys Technologies**")
    st.markdown("🔧 Built & Designed by **Sai Vineela**")

# ------------------ Top Branding ------------------
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg' width='40'/>
        <h1 style='display:inline; margin-left: 10px;'>AI Metadata Tools</h1>
        <p style='font-size:18px; margin-top: -10px; color: gray;'>Empowering Data Intelligence with AI and Elegance</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

BASE_URL = os.getenv("BASE_URL")
HEADERS = {"x-api-key": api_key}

# ------------------ Metadata Generator ------------------
if tool == "📝 Metadata Generator":
    st.subheader("📝 Generate Enriched Metadata")
    st.info("Upload an Excel file to generate domain, subdomain, description, and classification metadata.")

    uploaded_file = st.file_uploader("📎 Upload Excel file", type=["xlsx"], key="gen")

    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        try:
            preview_df = pd.read_excel(uploaded_file)
            st.markdown("### 📄 Preview of Uploaded File")
            st.dataframe(preview_df.head())
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

        if st.button("🚀 Generate Metadata"):
            if not api_key:
                st.error("Please enter your API Key in the sidebar.")
            else:
                with st.spinner("Processing with AI..."):
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
                            df_result = enforce_consistent_metadata(df_result)
                            st.success("✅ Metadata generated successfully!")
                            st.markdown("### 📊 Output Metadata")
                            st.dataframe(df_result, use_container_width=True)
                        else:
                            st.error(f"❌ API Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")

# ------------------ Source to Target Mapper ------------------
if tool == "🧠 Source to Target Mapper":
    st.subheader("🧠 AI Metadata Mapper")
    st.info("Upload a file to match source and target columns intelligently using AI.")

    uploaded_file = st.file_uploader("📎 Upload Excel file", type=["xlsx"], key="mapper")

    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        try:
            preview_df = pd.read_excel(uploaded_file,sheet_name="DataDictionaryTemplate")
            st.markdown("### 📄 Preview of Uploaded File")
            st.dataframe(preview_df.head())
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

        if st.button("🚀 Generate Mappings"):
            if not api_key:
                st.error("Please enter your API Key in the sidebar.")
            else:
                with st.spinner("Generating AI mappings..."):
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
                            st.markdown("### 📊 Output Mappings")
                            st.dataframe(df_result, use_container_width=True)
                        else:
                            st.error(f"❌ API Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")

# ------------------ Footer ------------------
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 0.9em; color: gray;'>
        🍏 AI Metadata Tools | © 2025 | Designed by <strong>Sai Vineela</strong> | Inspired by Apple • Powered by Infosys
    </div>
    """, unsafe_allow_html=True)