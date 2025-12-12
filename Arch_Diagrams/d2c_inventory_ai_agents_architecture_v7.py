#!/usr/bin/env python3
"""
D2C Inventory Optimization - Low-Level Technical Architecture
Version 7: Detailed Technical Design with All Components

Based on reference diagram - includes:
- Detailed data ingestion and streaming
- Unity Catalog governance layer
- Delta Lake with medallion architecture
- Vector Search for knowledge retrieval
- Mosaic AI Agent Framework components
- Model Serving and APIs
- Digital Assistant integration
- Comprehensive technical specifications
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks, SynapseAnalytics
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers, SQLDatawarehouse
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.analytics import EventHubs
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.storage import DataLakeStorage, BlobStorage
from diagrams.azure.web import AppServices
from diagrams.azure.security import KeyVaults
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.programming.framework import FastAPI
import subprocess

# Color palette for technical layers
COLOR_SOURCE = "#4285F4"           # Blue - Data Sources
COLOR_INGESTION = "#9C27B0"        # Purple - Ingestion
COLOR_STORAGE = "#FF6F00"          # Orange - Storage
COLOR_GOVERNANCE = "#795548"       # Brown - Governance
COLOR_AGENT = "#E91E63"            # Pink - Agent Framework
COLOR_SERVING = "#00BCD4"          # Cyan - Serving
COLOR_USER = "#4CAF50"             # Green - User Interface

# Graph attributes for detailed technical diagram
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "rankdir": "LR",
    "compound": "true",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "2.0",
    "pad": "0.5"
}

# Cluster styles
source_cluster_attr = {
    "bgcolor": "#E3F2FD",
    "fontsize": "13",
    "fontcolor": COLOR_SOURCE,
    "penwidth": "2.5",
    "style": "rounded"
}

ingestion_cluster_attr = {
    "bgcolor": "#F3E5F5",
    "fontsize": "13",
    "fontcolor": COLOR_INGESTION,
    "penwidth": "2.5",
    "style": "rounded"
}

storage_cluster_attr = {
    "bgcolor": "#FFF3E0",
    "fontsize": "13",
    "fontcolor": COLOR_STORAGE,
    "penwidth": "2.5",
    "style": "rounded"
}

governance_cluster_attr = {
    "bgcolor": "#EFEBE9",
    "fontsize": "13",
    "fontcolor": COLOR_GOVERNANCE,
    "penwidth": "2.5",
    "style": "rounded"
}

agent_cluster_attr = {
    "bgcolor": "#FCE4EC",
    "fontsize": "13",
    "fontcolor": COLOR_AGENT,
    "penwidth": "2.5",
    "style": "rounded"
}

serving_cluster_attr = {
    "bgcolor": "#E0F7FA",
    "fontsize": "13",
    "fontcolor": COLOR_SERVING,
    "penwidth": "2.5",
    "style": "rounded"
}

with Diagram(
    "D2C Inventory Optimization - Low-Level Technical Architecture (v7)",
    filename="diagrams/d2c_inventory_ai_agents_v7",
    direction="LR",
    graph_attr=graph_attr,
    outformat=["png", "dot"],
    show=False
):

    # ========================================================================
    # LAYER 1: DATA SOURCES
    # ========================================================================
    with Cluster("Data Sources", graph_attr=source_cluster_attr):
        sap_ecc = DatabaseForPostgresqlServers("SAP ECC\n(ERP)")
        sap_bw = DatabaseForPostgresqlServers("SAP BW\n(Data Warehouse)")
        external_api = APIManagement("External APIs\n(Weather, Market)")

    # ========================================================================
    # LAYER 2: DATA INGESTION & STREAMING
    # ========================================================================
    with Cluster("Data Ingestion Layer", graph_attr=ingestion_cluster_attr):
        kafka = EventHubs("Kafka/Event Hubs\n(Streaming)")
        airbyte = ServiceBus("Airbyte\n(CDC Connector)")
        rest_api = APIManagement("REST API\n(Batch Ingestion)")

    # ========================================================================
    # LAYER 3: DATABRICKS PLATFORM
    # ========================================================================
    with Cluster("Databricks Platform"):

        # Unity Catalog (Governance Layer)
        with Cluster("Unity Catalog\n(Data Governance)", graph_attr=governance_cluster_attr):
            catalog = DatabaseForPostgresqlServers("Metastore")
            access_control = KeyVaults("Access Control\n(RBAC)")
            lineage = FunctionApps("Data Lineage")

        # Delta Lake (Storage Layer)
        with Cluster("Delta Lake\n(Medallion Architecture)", graph_attr=storage_cluster_attr):
            bronze = DataLakeStorage("Bronze\n(Raw Data)")
            silver = DataLakeStorage("Silver\n(Cleansed)")
            gold = DataLakeStorage("Gold\n(Aggregated)")

        # Data Processing
        with Cluster("Data Processing"):
            spark_streaming = Spark("Spark Structured\nStreaming")
            spark_batch = Spark("Spark Batch\nProcessing")

        # Tables (Pre-Processed with ML)
        with Cluster("Data Tables\n(ML Pre-Processed)"):
            inventory_tbl = SQLDatawarehouse("Inventory\nTable")
            sales_tbl = SQLDatawarehouse("Sales\nTable")
            forecast_tbl = SQLDatawarehouse("Forecast\nTable")
            recommendation_tbl = SQLDatawarehouse("Recommendation\nTable")

        # Vector Search (Knowledge Base)
        with Cluster("Vector Search\n(Knowledge Retrieval)"):
            embeddings = MachineLearningServiceWorkspaces("Embeddings\nModel")
            vector_index = BlobStorage("Vector Index\n(FAISS/HNSW)")

        # Agent Framework (Mosaic AI)
        with Cluster("Mosaic AI Agent Framework", graph_attr=agent_cluster_attr):

            # Agent Orchestration
            agent_orchestrator = Databricks("Agent\nOrchestrator")

            # Agent Components
            with Cluster("Agent Components"):
                query_planner = FunctionApps("Query\nPlanner")
                tool_executor = FunctionApps("Tool\nExecutor")
                response_gen = FunctionApps("Response\nGenerator")

            # Tools
            with Cluster("Agent Tools"):
                sql_tool = FunctionApps("SQL Query\nTool")
                vector_tool = FunctionApps("Vector Search\nTool")
                python_tool = FunctionApps("Python REPL\nTool")

        # Model Serving
        with Cluster("Model Serving", graph_attr=serving_cluster_attr):
            llm_serving = Databricks("LLM Serving\n(Foundation Models)")
            mlflow_registry = Databricks("MLflow\nModel Registry")

    # ========================================================================
    # LAYER 4: API & APPLICATION LAYER
    # ========================================================================
    with Cluster("Application Layer"):
        agent_api = FastAPI("Agent API\n(REST/gRPC)")
        notification_service = ServiceBus("Notification\nService")

    # ========================================================================
    # LAYER 5: USER INTERFACE
    # ========================================================================
    with Cluster("User Interface"):
        digital_assistant = AppServices("Digital Assistant\n(Chatbot)")
        email_client = ServiceBus("Email Client")

    # User
    inventory_manager = Users("Inventory\nManager")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT (Low-Level Technical Flow)
    # ========================================================================

    # STEP 1-3: SOURCES → INGESTION
    sap_ecc >> Edge(label="[1] CDC", color=COLOR_SOURCE, style="bold") >> airbyte
    sap_bw >> Edge(label="[2] Batch", color=COLOR_SOURCE, style="bold") >> rest_api
    external_api >> Edge(label="[3] Stream", color=COLOR_SOURCE, style="bold") >> kafka

    # STEP 4-6: INGESTION → DELTA LAKE (Bronze)
    airbyte >> Edge(label="[4] ingest", color=COLOR_INGESTION, style="bold") >> bronze
    rest_api >> Edge(label="[5] ingest", color=COLOR_INGESTION, style="bold") >> bronze
    kafka >> Edge(label="[6] stream", color=COLOR_INGESTION, style="bold") >> spark_streaming
    spark_streaming >> Edge(label="", color=COLOR_INGESTION, style="bold") >> bronze

    # STEP 7-8: BRONZE → SILVER → GOLD (Data Processing)
    bronze >> Edge(label="[7] cleanse", color=COLOR_STORAGE, style="bold") >> spark_batch
    spark_batch >> Edge(label="", color=COLOR_STORAGE, style="bold") >> silver
    silver >> Edge(label="[8] aggregate", color=COLOR_STORAGE, style="bold") >> gold

    # STEP 9: GOLD → TABLES (Unity Catalog Governed)
    gold >> Edge(label="[9] organize", color=COLOR_GOVERNANCE, style="bold") >> catalog
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> inventory_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> sales_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> forecast_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> recommendation_tbl

    # STEP 10: CREATE VECTOR EMBEDDINGS
    gold >> Edge(label="[10] embed", color=COLOR_STORAGE, style="dashed") >> embeddings
    embeddings >> Edge(label="", color=COLOR_STORAGE, style="dashed") >> vector_index

    # STEP 11-12: USER QUERY → AGENT
    inventory_manager >> Edge(label="[11] query", color=COLOR_USER, style="bold") >> digital_assistant
    digital_assistant >> Edge(label="[12] request", color=COLOR_USER, style="bold") >> agent_api
    agent_api >> Edge(label="", color=COLOR_USER, style="bold") >> agent_orchestrator

    # STEP 13-15: AGENT ORCHESTRATION (Query Planning → Tool Execution)
    agent_orchestrator >> Edge(label="[13] plan", color=COLOR_AGENT, style="bold") >> query_planner
    query_planner >> Edge(label="[14] execute", color=COLOR_AGENT, style="bold") >> tool_executor

    # STEP 16-18: TOOL EXECUTION (SQL, Vector Search, Python)
    tool_executor >> Edge(label="[15] SQL", color=COLOR_AGENT, style="bold") >> sql_tool
    tool_executor >> Edge(label="[16] search", color=COLOR_AGENT, style="dotted") >> vector_tool
    tool_executor >> Edge(label="[17] compute", color=COLOR_AGENT, style="dotted") >> python_tool

    # STEP 19-21: TOOLS → DATA ACCESS
    sql_tool >> Edge(label="[18] query", color=COLOR_AGENT, style="bold") >> inventory_tbl
    sql_tool >> Edge(label="", color=COLOR_AGENT, style="dotted") >> sales_tbl
    sql_tool >> Edge(label="", color=COLOR_AGENT, style="dotted") >> forecast_tbl
    vector_tool >> Edge(label="[19] retrieve", color=COLOR_AGENT, style="dashed") >> vector_index

    # STEP 22-23: RESULTS → LLM INTERPRETATION
    inventory_tbl >> Edge(label="[20] results", color=COLOR_AGENT, style="bold") >> response_gen
    vector_index >> Edge(label="", color=COLOR_AGENT, style="dotted") >> response_gen
    response_gen >> Edge(label="[21] interpret", color=COLOR_SERVING, style="bold") >> llm_serving

    # STEP 24-26: RESPONSE → USER
    llm_serving >> Edge(label="[22] response", color=COLOR_SERVING, style="bold") >> agent_api
    agent_api >> Edge(label="[23] format", color=COLOR_USER, style="bold") >> notification_service
    notification_service >> Edge(label="[24] email", color=COLOR_USER, style="bold") >> email_client
    email_client >> Edge(label="[25] notify", color=COLOR_USER, style="bold") >> inventory_manager

    # GOVERNANCE & LINEAGE (Background processes)
    access_control >> Edge(label="RBAC", color=COLOR_GOVERNANCE, style="dotted") >> catalog
    lineage >> Edge(label="track", color=COLOR_GOVERNANCE, style="dotted") >> spark_batch

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io format
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v7.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v7.drawio")

    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v7.drawio")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 7 - Low-Level Technical Architecture):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v7.png")
print("  - diagrams/d2c_inventory_ai_agents_v7.dot")
print("  - diagrams/d2c_inventory_ai_agents_v7.drawio")

print("\n" + "="*80)
print("📊 D2C INVENTORY OPTIMIZATION - V7 LOW-LEVEL TECHNICAL ARCHITECTURE:")
print("="*80)

print("\n🔵 LAYER 1: DATA SOURCES")
print("  • SAP ECC (ERP System)")
print("  • SAP BW (Data Warehouse)")
print("  • External APIs (Weather, Market Data)")

print("\n🟣 LAYER 2: DATA INGESTION & STREAMING")
print("  [1-3] Sources → Ingestion Layer:")
print("      • Airbyte (CDC from SAP ECC)")
print("      • REST API (Batch from SAP BW)")
print("      • Kafka/Event Hubs (Real-time streams)")

print("\n🟠 LAYER 3: DATABRICKS PLATFORM")
print("  ")
print("  📦 Unity Catalog (Data Governance):")
print("    [9] Metastore, Access Control (RBAC), Data Lineage")
print("  ")
print("  💾 Delta Lake (Medallion Architecture):")
print("    [4-6] Ingestion → Bronze (Raw Data)")
print("    [7] Bronze → Silver (Cleansed)")
print("    [8] Silver → Gold (Aggregated)")
print("  ")
print("  📊 Data Tables (ML Pre-Processed):")
print("    • Inventory, Sales, Forecast, Recommendation Tables")
print("  ")
print("  🔍 Vector Search (Knowledge Retrieval):")
print("    [10] Embeddings Model → Vector Index (FAISS/HNSW)")
print("  ")
print("  🤖 Mosaic AI Agent Framework:")
print("    [11-15] Agent Orchestrator → Query Planner → Tool Executor")
print("    ")
print("    Agent Tools:")
print("      [16] SQL Query Tool")
print("      [17] Vector Search Tool")
print("      [18] Python REPL Tool")
print("    ")
print("    [18-20] Tools → Data Access (Tables, Vector Index)")
print("  ")
print("  🚀 Model Serving:")
print("    [21-22] LLM Serving (Foundation Models), MLflow Registry")

print("\n🌐 LAYER 4: APPLICATION LAYER")
print("  [23] Agent API (REST/gRPC)")
print("  [24] Notification Service")

print("\n👤 LAYER 5: USER INTERFACE")
print("  [11] Inventory Manager → Digital Assistant (Chatbot)")
print("  [25] Email Client → Inventory Manager")

print("\n" + "="*80)
print("✨ Version 7 Technical Specifications:")
print("="*80)
print("  ✓ 25+ numbered technical flow steps")
print("  ✓ Medallion architecture (Bronze → Silver → Gold)")
print("  ✓ Unity Catalog for data governance and RBAC")
print("  ✓ Vector Search with embeddings (FAISS/HNSW)")
print("  ✓ Detailed Mosaic AI Agent Framework components")
print("  ✓ Multiple agent tools (SQL, Vector Search, Python REPL)")
print("  ✓ Model serving with LLM foundation models")
print("  ✓ Comprehensive data lineage tracking")
print("  ✓ CDC, batch, and streaming ingestion patterns")
print("  ✓ Production-ready technical architecture")
print("="*80)
