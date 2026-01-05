# Architecture Diagrams Generator using Python and AI

# Watch the Video for Step by Step Details

[![Video Title](https://img.youtube.com/vi/m7EuZ7GhinE/0.jpg)](https://www.youtube.com/watch?v=m7EuZ7GhinE)




Let me provide one-liner descriptions for all 21 sequence numbers in the V9 architecture diagram: V9 Architecture - Sequence Number Descriptions: Data Sources → Ingestion (Steps 1-3):
[1] CDC - Change Data Capture from SAP ECC using Airbyte for real-time data replication
[2] Batch - Scheduled batch data extraction from SAP BW via REST API
[3] Stream - Real-time streaming data ingestion from external APIs via Kafka
Ingestion → Databricks Platform (Step 4):
[4] ingest - Load raw data from all ingestion sources into Delta Lake storage
Delta Lake → Unity Catalog → Data Tables (Steps 5-6):
[5] govern - Apply data governance policies and access controls via Unity Catalog
[6] organize - Structure governed data into queryable tables (Inventory, Sales, Forecast)
Delta Lake → Vector Search (Step 7):
[7] embed - Create vector embeddings from data for semantic search capabilities
User Query → Agent (Steps 8-10):
[8] query - Inventory Manager submits natural language question via Digital Assistant
[9] request - Digital Assistant forwards user query to Agent API
[10] - Agent API routes request to Agent Orchestrator for processing
Agent Pipeline (Steps 11-12):
[11] plan - Agent Orchestrator analyzes query and creates execution plan via Query Planner
[12] execute - Query Planner sends execution instructions to Tool Executor
Tool Executor → Tools (Steps 13-14):
[13] SQL - Tool Executor activates SQL Tool for structured data queries
[14] search - Tool Executor activates Vector Tool for knowledge base retrieval
Tools → Data Access (Steps 15-16):
[15] query - SQL Tool executes database queries against Data Tables
[16] retrieve - Vector Tool performs semantic search on Vector Search index
Results → LLM Interpretation (Steps 17-18):
[17] results - Query results and retrieved knowledge returned to Response Generator
[18] interpret - Response Generator sends results to LLM Serving for natural language interpretation
LLM → User Notification (Steps 19-21):
[19] response - LLM generates human-readable response sent back to Agent API
[20] notify - Agent API triggers Notification Service to prepare email
[21] email - Email notification with interpreted results delivered to Inventory Manager

---

## V10 Architecture - D2C Inventory AI Agents (Databricks)
Full Databricks-based agentic AI architecture with Mosaic AI Agent Framework.

---

## V11 Architecture - Hybrid Azure AI Foundry + Databricks

### Overview
V11 migrates the Agentic AI layer from Databricks Mosaic AI to **Azure AI Foundry** while keeping **Databricks for the data layer** (Delta Lake, SQL queries, Unity Catalog).

### Key Changes from V10
| Component | V10 (Databricks) | V11 (Hybrid) |
|-----------|-----------------|--------------|
| Agent Framework | Mosaic AI Agent Framework | Azure AI Foundry Prompt Flow |
| LLM | Databricks Foundation Models | Azure OpenAI (GPT-4) |
| Vector Search | Databricks Vector Search | Azure AI Search |
| Data Layer | Databricks | Databricks (unchanged) |
| Governance | Unity Catalog | Unity Catalog (unchanged) |

### Dual Entry Points
1. **Interactive (Real-time)**: Digital Assistant UI (Chatbot) → Agent API → Chat Response
2. **Batch (Scheduled)**: Batch Scheduler (Azure Functions) → Agent API → Email Report

### Architecture Flow
```
Data Layer (Databricks - unchanged):
[1-7] SAP ECC → Data Factory → Delta Lake → Unity Catalog → Lakehouse

Entry Points:
[8a] Digital Assistant (Interactive) OR [8b] Batch Scheduler (Scheduled)
[9] Agent API routes to Azure AI Foundry

AI Processing (Azure AI Foundry):
[10] Prompt Flow Orchestrator
[11] GPT-4 Query Planner
[12] Tool Executor Node
[13] Databricks SQL Connector → Databricks SQL Warehouse
[14] Azure AI Search (RAG)
[15-17] Results aggregation
[18] Azure OpenAI (GPT-4) response generation

Response:
[19] Agent API returns response
[20] Chat Response (interactive) OR Email Report (batch)
```

### Reference Links
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Prompt Flow](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/prompt-flow)
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)
- [Databricks SQL](https://docs.databricks.com/en/sql/index.html)

