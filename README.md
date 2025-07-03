# AI Data Modeler
AI Data modeling LLM Application 

## 🎯 Project Overview

AI Data Modeler is an intelligent metadata enrichment and column mapping tool designed specifically for Retail and Consumer Packaged Goods (CPG) datasets. This application leverages Large Language Models (LLMs) to automatically generate comprehensive metadata and create intelligent source-to-target column mappings.

## 🏗️ Architecture

The project consists of two main components:

### Backend (FastAPI)
- **Main API Server**: [`main.py`](main.py) - FastAPI application with metadata generation endpoints
- **LangGraph Integration**: [`langgraph_runner.py`](langgraph_runner.py) - Orchestrates AI workflows
- **Security**: [`security.py`](security.py) - API key authentication and validation
- **Configuration**: [`config.py`](config.py) - Application settings and environment variables

### Frontend (Streamlit)
- **Primary Interface**: [`streamlit_app/app.py`](streamlit_app/app.py) - Main Streamlit application
- **Alternative Interface**: [`streamlit_app/app-v1.py`](streamlit_app/app-v1.py) - Alternative UI implementation

## 🚀 Key Features

### 1. **Metadata Generator** 📝
- **Domain Classification**: Automatically categorizes data into 6 domains (Sales, Finance, Customer, Product, Logistics, Inventory)
- **SubDomain Mapping**: Provides specific subdomain classifications (Order Management, Loyalty, Shipping, etc.)
- **Security Classification**: Assigns appropriate security levels (Confidential, Internal, Public, Restricted)
- **Rich Descriptions**: Generates contextual table and column descriptions
- **Consistency Enforcement**: Ensures metadata consistency across related columns

### 2. **Source-to-Target Mapper** 🧠
- **Intelligent Matching**: Uses AI to match source columns to target schema
- **FAISS Integration**: Leverages vector similarity search for accurate column matching
- **Confidence Scoring**: Provides match confidence levels (Best Match, Potential Match)
- **Batch Processing**: Handles large Excel files efficiently

## 🛠️ Technology Stack

### AI & ML
- **LangChain**: Framework for building LLM applications
- **LangGraph**: Workflow orchestration for complex AI tasks
- **OpenAI GPT-4**: Primary language model for metadata generation
- **Azure OpenAI**: Alternative LLM provider
- **Embedding Model**:BAAI/bge-small-en-v1.5
- **FAISS**: Vector similarity search for column matching

### Backend
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file processing

### Data Storage
- **FAISS Index**: Vector database for similarity search
- **CSV Files**: Data storage in [`Data`](Data) directory

## 🤖 AI Prompt Engineering

The system uses sophisticated prompt engineering defined in [`prompts.py`](prompts.py) to ensure accurate and consistent metadata generation:

### Metadata Generation Prompt

The **Metadata_Prompt_Template** is designed specifically for Retail and CPG datasets with the following capabilities:

#### Domain Classification
The AI categorizes data into 6 primary domains:
- **Sales**: Revenue, transactions, orders
- **Finance**: Financial records, accounting, billing
- **Customer**: Customer data, profiles, interactions
- **Product**: Product information, catalogs, specifications
- **Logistics**: Shipping, delivery, transportation
- **Inventory**: Stock levels, warehouse management

#### SubDomain Mapping
Each domain has specific subdomains for granular classification:
- **Customer → Loyalty**: Loyalty programs, customer retention metrics
- **Finance → Accounts Receivable**: Invoices, payments, outstanding balances
- **Inventory → Stock Levels**: Product availability, reorder thresholds
- **Logistics → Shipping**: Shipment tracking, delivery times, costs
- **Product → Product Catalog**: Product IDs, names, descriptions, categories
- **Sales → Order Management**: Orders, invoices, order items, payment status

#### Security Classification Rules
- **Confidential/Restricted**: Only for PII or sensitive financial fields
- **Internal**: Standard business data
- **Public**: Non-sensitive, publicly available information

#### Consistency Rules
- All columns in a table share the same Domain, SubDomain, and TableDescription
- Individual columns may have different SecurityClassification if they contain PII
- Descriptions are contextual and concise (max 20 words for tables)

### Column Mapping Prompt

The **mappings_prompt** handles intelligent source-to-target column matching:

#### Matching Process
1. **Source Analysis**: Examines source column name, data type, and description
2. **Candidate Retrieval**: Uses FAISS to find similar target columns
3. **AI Evaluation**: Ranks candidates using semantic understanding
4. **Confidence Scoring**: Classifies matches as "Best Match" or "Potential Match"

#### Example Prompt Structure
```
Source Column: customer_email
Data Type: VARCHAR
Description: Customer email address for communication

Retrieved Candidate Columns:
1. email_address | Customer primary email | VARCHAR
2. contact_email | Business contact email | VARCHAR  
3. notification_email | Email for notifications | VARCHAR

Output: Match: 1, Type: Best Match
```

### Prompt Engineering Best Practices

#### Domain-Specific Knowledge
- Built-in understanding of retail/CPG business terminology
- Context-aware classification based on industry standards
- Consistent taxonomy across different datasets

#### Error Prevention
- Explicit rules prevent inconsistent classifications
- Validation logic ensures data quality
- Clear output format requirements

#### Scalability
- Template-based approach for easy modification
- Configurable domain/subdomain mappings
- Extensible for additional business domains

## 📁 Project Structure

```
AI_DATAMODELER/
├── 📄 main.py                    # FastAPI backend server
├── 📄 langgraph_runner.py        # AI workflow orchestration
├── 📄 prompts.py                 # LLM prompt templates
├── 📄 config.py                  # Application configuration
├── 📄 security.py                # Authentication & security
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env                       # Environment variables
├── 📁 streamlit_app/
│   ├── 📄 app.py                 # Primary Streamlit interface
│   └── 📄 app-v1.py              # Alternative UI
├── 📁 assets/                    # Static assets (logos, images)
├── 📁 Data/                      # Data storage
│   ├── 📄 Silver_Table.csv       # Reference data
│   └── 📁 faiss_index/           # Vector search index
├── 📁 models/                    # Data models
├── 📁 services/                  # Business logic services
├── 📁 utils/                     # Utility functions
└── 📁 Testing/                   # Test files
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/Saipractice/AI_DATAMODELER.git
cd AI_DATAMODELER
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a [`.env`](.env) file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Azure OpenAI Configuration (Optional)
USE_AZURE_OPENAI=true
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# API Security
API_KEY=your_custom_api_key

# Application Settings
BASE_URL=http://127.0.0.1:8000 or Deployed URL
```

### 4. Start the Backend Server
```bash
uvicorn main:app --reload
```

### 5. Launch the Frontend
```bash
streamlit run streamlit_app/app.py
```

## 📖 Usage Guide

### Metadata Generation

1. **Upload Excel File**: Select an Excel file containing your dataset
2. **API Key**: Enter your API key in the sidebar
3. **Generate Metadata**: Click "🚀 Generate Metadata" to process
4. **Review Results**: Examine the generated metadata including:
   - Domain and SubDomain classifications
   - Security classifications
   - Table and column descriptions

### Source-to-Target Mapping

1. **Upload Mapping File**: Upload an Excel file with "DataDictionaryTemplate" sheet
2. **Generate Mappings**: Click "🚀 Generate Mappings" 
3. **Review Matches**: Analyze the AI-generated column mappings with confidence scores

## 🎯 Business Benefits

### For Data Teams
- **Automated Metadata**: Reduces manual metadata creation time by 80%
- **Consistency**: Ensures uniform metadata standards across datasets
- **Quality Assurance**: AI-powered validation reduces human errors

### For Organizations
- **Compliance**: Automated security classification supports governance
- **Discovery**: Rich metadata improves data discoverability
- **Integration**: Faster data onboarding and schema mapping

### For Retail & CPG Companies
- **Domain Expertise**: Built-in knowledge of retail/CPG data patterns
- **Scalability**: Handles large datasets efficiently
- **Standardization**: Consistent domain/subdomain taxonomy

## 🔐 Security Features

- **API Key Authentication**: Secure access control via [`security.py`](security.py)
- **Data Classification**: Automatic PII and sensitive data identification
- **Environment Variables**: Secure configuration management
- **Input Validation**: Comprehensive data validation using Pydantic

## 🤝 Integration Points

### API Endpoints
- **POST /generate_metadata/**: Generate metadata for uploaded Excel files
- **POST /generate_mappings_excel**: Create source-to-target mappings

### Data Sources
- **Excel Files**: Primary input format (.xlsx)
- **CSV Files**: Reference data in [`Data/Silver_Table.csv`](Data/Silver_Table.csv)
- **FAISS Index**: Vector database for similarity matching

## 📊 Example Use Cases

1. **Data Warehouse Onboarding**: Automatically classify and document new datasets
2. **Schema Migration**: Map columns between legacy and modern systems
3. **Compliance Reporting**: Generate metadata for regulatory requirements
4. **Data Catalog Management**: Populate enterprise data catalogs

## 🏢 Enterprise Ready

- **Production Ready**: FastAPI backend with proper error handling
- **Scalable**: Designed for enterprise-scale data processing
- **Maintainable**: Clean architecture with separation of concerns

## 🎨 User Experience

The application features an Apple-inspired design with:
- **Intuitive Navigation**: Clear tool selection and workflow
- **Real-time Feedback**: Progress indicators and status messages
- **Responsive Design**: Works across different screen sizes
- **Professional Branding**: Clean, modern interface

## 📈 Performance

- **Efficient Processing**: Optimized for large Excel files
- **Vector Search**: Fast similarity matching using FAISS
- **Async Operations**: Non-blocking API operations
- **Memory Management**: Efficient data handling

## 🔄 Development Workflow

1. **Backend Development**: Modify [`main.py`](main.py) and related files
2. **Frontend Updates**: Edit [`streamlit_app/app.py`](streamlit_app/app.py)
3. **Prompt Engineering**: Update templates in [`prompts.py`](prompts.py)
4. **Testing**: Use files in [`Testing`](Testing) directory

---


uvicorn main:app --reload

streamlit run streamlit_app/app.py

**© 2025 | Designed by Sai Vineela | Powered by Infosys Technologies**

For support or questions, please refer to the documentation or contact the development team.