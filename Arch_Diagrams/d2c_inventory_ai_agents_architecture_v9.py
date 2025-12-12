#!/usr/bin/env python3
"""
D2C Inventory Optimization - Low-Level Technical Architecture
Version 9: Abstracted Databricks Components (Client Presentation Ready)

Key Changes in V9:
- Abstracted Delta Lake (no Bronze/Silver/Gold details)
- Abstracted Vector Search (single component)
- Abstracted Unity Catalog (single component)
- Abstracted Data Tables (single component)
- Maintained left-to-right flow direction
- Cleaner, more presentation-friendly architecture
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks, EventHubs
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers, SQLDatawarehouse
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.web import AppServices
from diagrams.azure.security import KeyVaults
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users
from diagrams.programming.framework import FastAPI
import subprocess

# Color palette
COLOR_SOURCE = "#4285F4"           # Blue
COLOR_INGESTION = "#9C27B0"        # Purple
COLOR_DATABRICKS = "#FF6F00"       # Orange
COLOR_AGENT = "#E91E63"            # Pink
COLOR_USER = "#4CAF50"             # Green

# Graph attributes
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "rankdir": "LR",
    "compound": "true",
    "splines": "ortho",
    "nodesep": "1.2",
    "ranksep": "2.5"
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
    "fontcolor": COLOR_DATABRICKS,
    "penwidth": "3.0",
    "style": "rounded"
}

agent_cluster_attr = {
    "bgcolor": "#FCE4EC",
    "fontsize": "13",
    "fontcolor": COLOR_AGENT,
    "penwidth": "2.5",
    "style": "rounded"
}

with Diagram(
    "D2C Inventory Optimization - Technical Architecture (v9 - Abstracted)",
    filename="diagrams/d2c_inventory_ai_agents_v9",
    direction="LR",
    graph_attr=graph_attr,
    outformat=["png", "dot"],
    show=False
):

    # ========================================================================
    # LAYER 1: DATA SOURCES
    # ========================================================================
    with Cluster("Data Sources", graph_attr=source_cluster_attr):
        sap_ecc = DatabaseForPostgresqlServers("SAP ECC")
        sap_bw = DatabaseForPostgresqlServers("SAP BW")
        external_api = APIManagement("External APIs")

    # ========================================================================
    # LAYER 2: DATA INGESTION
    # ========================================================================
    with Cluster("Data Ingestion", graph_attr=ingestion_cluster_attr):
        kafka = EventHubs("Streaming\n(Kafka)")
        airbyte = ServiceBus("CDC\n(Airbyte)")
        rest_api = APIManagement("Batch\n(REST API)")

    # ========================================================================
    # LAYER 3: DATABRICKS PLATFORM (Abstracted, Left-to-Right)
    # ========================================================================
    with Cluster("Databricks Platform", graph_attr=databricks_cluster_attr):

        # Abstracted Components (Left-to-Right Order)
        unity_catalog = KeyVaults("Unity Catalog\n(Governance)")
        delta_lake = DataLakeStorage("Delta Lake\n(Data Storage)")
        data_tables = SQLDatawarehouse("Data Tables\n(Inventory, Sales,\nForecast)")
        vector_search = MachineLearningServiceWorkspaces("Vector Search\n(Knowledge Base)")

        # Agent Framework (Left-to-Right Pipeline)
        with Cluster("Mosaic AI Agent Framework", graph_attr=agent_cluster_attr):
            agent_orchestrator = Databricks("Agent\nOrchestrator")
            query_planner = FunctionApps("Query\nPlanner")
            tool_executor = FunctionApps("Tool\nExecutor")

            # Agent Tools
            sql_tool = FunctionApps("SQL Tool")
            vector_tool = FunctionApps("Vector Tool")

            response_gen = FunctionApps("Response\nGenerator")

        # LLM Serving
        llm_serving = Databricks("LLM Serving\n(Foundation Models)")

    # ========================================================================
    # LAYER 4: APPLICATION & USER INTERFACE
    # ========================================================================
    with Cluster("Application Layer"):
        agent_api = FastAPI("Agent API")
        notification = ServiceBus("Notification")
        digital_assistant = AppServices("Digital\nAssistant")

    # User
    inventory_manager = Users("Inventory\nManager")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT (Simplified)
    # ========================================================================

    # STEP 1-3: SOURCES → INGESTION
    sap_ecc >> Edge(label="[1] CDC", color=COLOR_SOURCE, style="bold") >> airbyte
    sap_bw >> Edge(label="[2] Batch", color=COLOR_SOURCE, style="bold") >> rest_api
    external_api >> Edge(label="[3] Stream", color=COLOR_SOURCE, style="bold") >> kafka

    # STEP 4: INGESTION → DELTA LAKE
    airbyte >> Edge(label="[4] ingest", color=COLOR_INGESTION, style="bold") >> delta_lake
    rest_api >> Edge(label="", color=COLOR_INGESTION, style="dotted") >> delta_lake
    kafka >> Edge(label="", color=COLOR_INGESTION, style="dotted") >> delta_lake

    # STEP 5-6: DELTA LAKE → UNITY CATALOG → DATA TABLES (Left-to-Right)
    delta_lake >> Edge(label="[5] govern", color=COLOR_DATABRICKS, style="bold") >> unity_catalog
    unity_catalog >> Edge(label="[6] organize", color=COLOR_DATABRICKS, style="bold") >> data_tables

    # STEP 7: DELTA LAKE → VECTOR SEARCH
    delta_lake >> Edge(label="[7] embed", color=COLOR_DATABRICKS, style="dashed") >> vector_search

    # STEP 8-9: USER QUERY → AGENT
    inventory_manager >> Edge(label="[8] query", color=COLOR_USER, style="bold") >> digital_assistant
    digital_assistant >> Edge(label="[9] request", color=COLOR_USER, style="bold") >> agent_api
    agent_api >> Edge(label="[10]", color=COLOR_USER, style="bold") >> agent_orchestrator

    # STEP 11-13: AGENT PIPELINE (Left-to-Right)
    agent_orchestrator >> Edge(label="[11] plan", color=COLOR_AGENT, style="bold") >> query_planner
    query_planner >> Edge(label="[12] execute", color=COLOR_AGENT, style="bold") >> tool_executor

    # STEP 14-15: TOOL EXECUTOR → TOOLS
    tool_executor >> Edge(label="[13] SQL", color=COLOR_AGENT, style="bold") >> sql_tool
    tool_executor >> Edge(label="[14] search", color=COLOR_AGENT, style="dotted") >> vector_tool

    # STEP 16-17: TOOLS → DATA ACCESS
    sql_tool >> Edge(label="[15] query", color=COLOR_AGENT, style="bold") >> data_tables
    vector_tool >> Edge(label="[16] retrieve", color=COLOR_AGENT, style="dashed") >> vector_search

    # STEP 18-19: RESULTS → RESPONSE GENERATOR → LLM
    data_tables >> Edge(label="[17] results", color=COLOR_AGENT, style="bold") >> response_gen
    vector_search >> Edge(label="", color=COLOR_AGENT, style="dotted") >> response_gen
    response_gen >> Edge(label="[18] interpret", color=COLOR_AGENT, style="bold") >> llm_serving

    # STEP 20-22: LLM → USER
    llm_serving >> Edge(label="[19] response", color=COLOR_USER, style="bold") >> agent_api
    agent_api >> Edge(label="[20] notify", color=COLOR_USER, style="bold") >> notification
    notification >> Edge(label="[21] email", color=COLOR_USER, style="bold") >> inventory_manager

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v9.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v9.drawio")
    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v9.drawio")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 9 - Abstracted Components):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v9.png")
print("  - diagrams/d2c_inventory_ai_agents_v9.dot")
print("  - diagrams/d2c_inventory_ai_agents_v9.drawio")

print("\n" + "="*80)
print("📊 D2C INVENTORY OPTIMIZATION - V9 TECHNICAL ARCHITECTURE:")
print("="*80)

print("\n🔵 LAYER 1: DATA SOURCES")
print("  • SAP ECC, SAP BW, External APIs")

print("\n🟣 LAYER 2: DATA INGESTION")
print("  [1-3] CDC (Airbyte), Batch (REST API), Streaming (Kafka)")

print("\n🟠 LAYER 3: DATABRICKS PLATFORM (ABSTRACTED, LEFT-TO-RIGHT)")
print("  ")
print("  [4] Ingestion → Delta Lake (Data Storage)")
print("  [5-6] Delta Lake → Unity Catalog (Governance) → Data Tables")
print("  [7] Delta Lake → Vector Search (Knowledge Base)")
print("  ")
print("  🤖 Mosaic AI Agent Framework (Left-to-Right Pipeline):")
print("    [11] Agent Orchestrator → [12] Query Planner → Tool Executor")
print("    [13-14] SQL Tool, Vector Tool")
print("    [15-16] Query Data Tables, Retrieve from Vector Search")
print("    [17-18] Results → Response Generator → LLM Serving")
print("  ")
print("  🚀 LLM Serving (Foundation Models)")

print("\n🌐 LAYER 4: APPLICATION & USER INTERFACE")
print("  [8-10] User → Digital Assistant → Agent API")
print("  [19-21] API → Notification → User")

print("\n" + "="*80)
print("✨ Version 9 Key Changes (Abstracted for Client Presentation):")
print("="*80)
print("  ✓ ABSTRACTED: Delta Lake (no Bronze/Silver/Gold sub-components)")
print("  ✓ ABSTRACTED: Vector Search (single component)")
print("  ✓ ABSTRACTED: Unity Catalog (single component)")
print("  ✓ ABSTRACTED: Data Tables (single component)")
print("  ✓ MAINTAINED: Left-to-right flow direction")
print("  ✓ SIMPLIFIED: 21 numbered steps (reduced from 25)")
print("  ✓ CLEANER: Client presentation-ready architecture")
print("  ✓ FOCUSED: Core components without overwhelming detail")
print("="*80)
