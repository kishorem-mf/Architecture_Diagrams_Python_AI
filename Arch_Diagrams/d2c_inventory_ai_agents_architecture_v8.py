#!/usr/bin/env python3
"""
D2C Inventory Optimization - Low-Level Technical Architecture
Version 8: Refined Technical Design (MLflow Registry Removed)

Key Changes in V8:
- Removed MLflow Model Registry (not needed - no model training)
- Kept LLM Serving for foundation models (natural language interpretation)
- Fixed Databricks internal flow to left-to-right direction
- Cleaner, more accurate technical architecture

Components:
- Data ingestion (CDC, batch, streaming)
- Unity Catalog governance
- Delta Lake medallion architecture
- Vector Search for knowledge retrieval
- Mosaic AI Agent Framework with tools
- LLM Serving (foundation models only)
- Digital Assistant integration
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks, EventHubs
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers, SQLDatawarehouse
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.storage import DataLakeStorage, BlobStorage
from diagrams.azure.web import AppServices
from diagrams.azure.security import KeyVaults
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.programming.framework import FastAPI
import subprocess

# Color palette
COLOR_SOURCE = "#4285F4"           # Blue
COLOR_INGESTION = "#9C27B0"        # Purple
COLOR_STORAGE = "#FF6F00"          # Orange
COLOR_GOVERNANCE = "#795548"       # Brown
COLOR_AGENT = "#E91E63"            # Pink
COLOR_SERVING = "#00BCD4"          # Cyan
COLOR_USER = "#4CAF50"             # Green

# Graph attributes
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "rankdir": "LR",
    "compound": "true",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "2.0"
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

databricks_cluster_attr = {
    "bgcolor": "#FFF3E0",
    "fontsize": "14",
    "fontcolor": COLOR_STORAGE,
    "penwidth": "3.0",
    "style": "rounded"
}

storage_cluster_attr = {
    "bgcolor": "#FFECB3",
    "fontsize": "12",
    "fontcolor": COLOR_STORAGE,
    "penwidth": "2.0",
    "style": "rounded"
}

governance_cluster_attr = {
    "bgcolor": "#EFEBE9",
    "fontsize": "12",
    "fontcolor": COLOR_GOVERNANCE,
    "penwidth": "2.0",
    "style": "rounded"
}

agent_cluster_attr = {
    "bgcolor": "#FCE4EC",
    "fontsize": "12",
    "fontcolor": COLOR_AGENT,
    "penwidth": "2.0",
    "style": "rounded"
}

serving_cluster_attr = {
    "bgcolor": "#E0F7FA",
    "fontsize": "12",
    "fontcolor": COLOR_SERVING,
    "penwidth": "2.0",
    "style": "rounded"
}

with Diagram(
    "D2C Inventory Optimization - Low-Level Technical Architecture (v8)",
    filename="diagrams/d2c_inventory_ai_agents_v8",
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
        sap_bw = DatabaseForPostgresqlServers("SAP BW\n(DWH)")
        external_api = APIManagement("External APIs\n(Market Data)")

    # ========================================================================
    # LAYER 2: DATA INGESTION
    # ========================================================================
    with Cluster("Data Ingestion Layer", graph_attr=ingestion_cluster_attr):
        kafka = EventHubs("Kafka/Event Hubs\n(Streaming)")
        airbyte = ServiceBus("Airbyte\n(CDC)")
        rest_api = APIManagement("REST API\n(Batch)")

    # ========================================================================
    # LAYER 3: DATABRICKS PLATFORM (Left-to-Right Internal Flow)
    # ========================================================================
    with Cluster("Databricks Platform", graph_attr=databricks_cluster_attr):

        # Unity Catalog (Governance)
        with Cluster("Unity Catalog", graph_attr=governance_cluster_attr):
            catalog = DatabaseForPostgresqlServers("Metastore")
            access_control = KeyVaults("RBAC")
            lineage = FunctionApps("Lineage")

        # Delta Lake (Left-to-Right: Bronze → Silver → Gold)
        with Cluster("Delta Lake\n(Medallion)", graph_attr=storage_cluster_attr):
            bronze = DataLakeStorage("Bronze\n(Raw)")
            silver = DataLakeStorage("Silver\n(Cleansed)")
            gold = DataLakeStorage("Gold\n(Aggregated)")

        # Spark Processing
        spark_streaming = Spark("Spark\nStreaming")
        spark_batch = Spark("Spark\nBatch")

        # Data Tables (Left-to-Right after Gold)
        with Cluster("Data Tables"):
            inventory_tbl = SQLDatawarehouse("Inventory")
            sales_tbl = SQLDatawarehouse("Sales")
            forecast_tbl = SQLDatawarehouse("Forecast")
            recommendation_tbl = SQLDatawarehouse("Recommendation")

        # Vector Search
        with Cluster("Vector Search"):
            embeddings = MachineLearningServiceWorkspaces("Embeddings")
            vector_index = BlobStorage("Vector Index")

        # Agent Framework (Left-to-Right: Orchestrator → Planner → Executor → Tools)
        with Cluster("Mosaic AI Agent Framework", graph_attr=agent_cluster_attr):
            agent_orchestrator = Databricks("Agent\nOrchestrator")

            with Cluster("Agent Pipeline"):
                query_planner = FunctionApps("Query\nPlanner")
                tool_executor = FunctionApps("Tool\nExecutor")
                response_gen = FunctionApps("Response\nGenerator")

            with Cluster("Agent Tools"):
                sql_tool = FunctionApps("SQL Tool")
                vector_tool = FunctionApps("Vector Tool")
                python_tool = FunctionApps("Python Tool")

        # LLM Serving (Foundation Models Only - NO MLflow)
        with Cluster("LLM Serving", graph_attr=serving_cluster_attr):
            llm_serving = Databricks("Foundation Models\n(GPT/Claude/Llama)")

    # ========================================================================
    # LAYER 4: APPLICATION & USER INTERFACE
    # ========================================================================
    with Cluster("Application Layer"):
        agent_api = FastAPI("Agent API")
        notification_service = ServiceBus("Notification\nService")
        digital_assistant = AppServices("Digital\nAssistant")
        email_client = ServiceBus("Email")

    # User
    inventory_manager = Users("Inventory\nManager")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT
    # ========================================================================

    # STEP 1-3: SOURCES → INGESTION
    sap_ecc >> Edge(label="[1] CDC", color=COLOR_SOURCE, style="bold") >> airbyte
    sap_bw >> Edge(label="[2] Batch", color=COLOR_SOURCE, style="bold") >> rest_api
    external_api >> Edge(label="[3] Stream", color=COLOR_SOURCE, style="bold") >> kafka

    # STEP 4-6: INGESTION → BRONZE
    airbyte >> Edge(label="[4]", color=COLOR_INGESTION, style="bold") >> bronze
    rest_api >> Edge(label="[5]", color=COLOR_INGESTION, style="bold") >> bronze
    kafka >> Edge(label="[6]", color=COLOR_INGESTION, style="bold") >> spark_streaming
    spark_streaming >> Edge(label="", color=COLOR_INGESTION, style="bold") >> bronze

    # STEP 7-8: BRONZE → SILVER → GOLD (Left-to-Right)
    bronze >> Edge(label="[7] cleanse", color=COLOR_STORAGE, style="bold") >> spark_batch
    spark_batch >> Edge(label="", color=COLOR_STORAGE, style="bold") >> silver
    silver >> Edge(label="[8] aggregate", color=COLOR_STORAGE, style="bold") >> gold

    # STEP 9: GOLD → UNITY CATALOG → TABLES (Left-to-Right)
    gold >> Edge(label="[9] govern", color=COLOR_GOVERNANCE, style="bold") >> catalog
    catalog >> Edge(label="[10]", color=COLOR_GOVERNANCE, style="bold") >> inventory_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> sales_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> forecast_tbl
    catalog >> Edge(label="", color=COLOR_GOVERNANCE, style="dotted") >> recommendation_tbl

    # STEP 11: VECTOR EMBEDDINGS
    gold >> Edge(label="[11] embed", color=COLOR_STORAGE, style="dashed") >> embeddings
    embeddings >> Edge(label="", color=COLOR_STORAGE, style="dashed") >> vector_index

    # STEP 12-14: USER QUERY → AGENT (Left-to-Right)
    inventory_manager >> Edge(label="[12] query", color=COLOR_USER, style="bold") >> digital_assistant
    digital_assistant >> Edge(label="[13]", color=COLOR_USER, style="bold") >> agent_api
    agent_api >> Edge(label="[14]", color=COLOR_USER, style="bold") >> agent_orchestrator

    # STEP 15-17: AGENT PIPELINE (Left-to-Right: Orchestrator → Planner → Executor)
    agent_orchestrator >> Edge(label="[15] plan", color=COLOR_AGENT, style="bold") >> query_planner
    query_planner >> Edge(label="[16] execute", color=COLOR_AGENT, style="bold") >> tool_executor

    # STEP 18-20: TOOL EXECUTOR → TOOLS
    tool_executor >> Edge(label="[17] SQL", color=COLOR_AGENT, style="bold") >> sql_tool
    tool_executor >> Edge(label="", color=COLOR_AGENT, style="dotted") >> vector_tool
    tool_executor >> Edge(label="", color=COLOR_AGENT, style="dotted") >> python_tool

    # STEP 21-22: TOOLS → DATA ACCESS
    sql_tool >> Edge(label="[18] query", color=COLOR_AGENT, style="bold") >> inventory_tbl
    sql_tool >> Edge(label="", color=COLOR_AGENT, style="dotted") >> sales_tbl
    sql_tool >> Edge(label="", color=COLOR_AGENT, style="dotted") >> forecast_tbl
    vector_tool >> Edge(label="[19] search", color=COLOR_AGENT, style="dashed") >> vector_index

    # STEP 23-24: RESULTS → RESPONSE GENERATOR → LLM
    inventory_tbl >> Edge(label="[20] results", color=COLOR_AGENT, style="bold") >> response_gen
    vector_index >> Edge(label="", color=COLOR_AGENT, style="dotted") >> response_gen
    response_gen >> Edge(label="[21] interpret", color=COLOR_SERVING, style="bold") >> llm_serving

    # STEP 25-28: LLM → USER
    llm_serving >> Edge(label="[22] response", color=COLOR_SERVING, style="bold") >> agent_api
    agent_api >> Edge(label="[23]", color=COLOR_USER, style="bold") >> notification_service
    notification_service >> Edge(label="[24] email", color=COLOR_USER, style="bold") >> email_client
    email_client >> Edge(label="[25] notify", color=COLOR_USER, style="bold") >> inventory_manager

    # GOVERNANCE (Background)
    access_control >> Edge(label="secure", color=COLOR_GOVERNANCE, style="dotted") >> catalog
    lineage >> Edge(label="track", color=COLOR_GOVERNANCE, style="dotted") >> spark_batch

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v8.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v8.drawio")
    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v8.drawio")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 8 - Refined Technical Architecture):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v8.png")
print("  - diagrams/d2c_inventory_ai_agents_v8.dot")
print("  - diagrams/d2c_inventory_ai_agents_v8.drawio")

print("\n" + "="*80)
print("📊 D2C INVENTORY OPTIMIZATION - V8 LOW-LEVEL TECHNICAL ARCHITECTURE:")
print("="*80)

print("\n🔵 LAYER 1: DATA SOURCES")
print("  • SAP ECC (ERP), SAP BW (DWH), External APIs")

print("\n🟣 LAYER 2: DATA INGESTION")
print("  [1-3] Airbyte (CDC), REST API (Batch), Kafka (Streaming)")

print("\n🟠 LAYER 3: DATABRICKS PLATFORM (LEFT-TO-RIGHT INTERNAL FLOW)")
print("  ")
print("  📦 Unity Catalog: [9] Metastore, RBAC, Lineage")
print("  ")
print("  💾 Delta Lake (Left-to-Right): [4-6] → Bronze → [7] Silver → [8] Gold")
print("  ")
print("  📊 Data Tables: [10] Inventory, Sales, Forecast, Recommendation")
print("  ")
print("  🔍 Vector Search: [11] Embeddings → Vector Index")
print("  ")
print("  🤖 Mosaic AI Agent Framework (Left-to-Right Pipeline):")
print("    [15] Agent Orchestrator → [16] Query Planner → Tool Executor")
print("    [17-19] Tools: SQL, Vector Search, Python REPL")
print("    [20-21] Results → Response Generator → LLM Serving")
print("  ")
print("  🚀 LLM Serving: Foundation Models (GPT/Claude/Llama)")
print("    ✓ NO MLflow Registry (no model training needed)")

print("\n🌐 LAYER 4: APPLICATION & USER INTERFACE")
print("  [12-14] User → Digital Assistant → Agent API")
print("  [22-25] API → Notification → Email → User")

print("\n" + "="*80)
print("✨ Version 8 Key Changes:")
print("="*80)
print("  ✓ REMOVED: MLflow Model Registry (not needed - no custom models)")
print("  ✓ KEPT: LLM Serving (foundation models for NL interpretation)")
print("  ✓ FIXED: Databricks internal flow is now left-to-right")
print("  ✓ Bronze → Silver → Gold (left-to-right)")
print("  ✓ Agent Orchestrator → Planner → Executor → Tools (left-to-right)")
print("  ✓ 25 numbered steps for complete flow traceability")
print("  ✓ Cleaner, more accurate technical architecture")
print("="*80)
