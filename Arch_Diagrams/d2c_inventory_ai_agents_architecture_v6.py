#!/usr/bin/env python3
"""
D2C Inventory Optimization with AI Agents - Architecture Diagram
Version 6: Query-Based Agents (As-Is to Future State)

Major Architectural Shift in V6:
- NO ML training/forecasting - data is pre-processed with ML already applied
- Agents query pre-existing data tables (inventory, sales, forecasts)
- Agents interpret query results using LLM
- Email notification with digital assistant link for follow-up queries
- Left-to-right flow with numbered sequences
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers, SQLDatawarehouse
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.storage import DataLakeStorage, BlobStorage
from diagrams.azure.web import AppServices
from diagrams.onprem.client import Users
import subprocess

# Color palette
COLOR_SOURCE = "#4285F4"           # Blue - Data Sources
COLOR_DATA = "#9C27B0"             # Purple - Data Layer
COLOR_AGENT = "#E91E63"            # Pink - AI Agent
COLOR_NOTIFICATION = "#00BCD4"     # Cyan - Notifications
COLOR_USER = "#4CAF50"             # Green - User Interaction

# Graph attributes for left-to-right flow
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
    "fontsize": "14",
    "fontcolor": COLOR_SOURCE,
    "penwidth": "2.5",
    "style": "rounded"
}

data_cluster_attr = {
    "bgcolor": "#F3E5F5",
    "fontsize": "14",
    "fontcolor": COLOR_DATA,
    "penwidth": "2.5",
    "style": "rounded"
}

agent_cluster_attr = {
    "bgcolor": "#FCE4EC",
    "fontsize": "14",
    "fontcolor": COLOR_AGENT,
    "penwidth": "2.5",
    "style": "rounded"
}

with Diagram(
    "D2C Inventory Optimization - Query-Based AI Agents (v6)",
    filename="diagrams/d2c_inventory_ai_agents_v6",
    direction="LR",
    graph_attr=graph_attr,
    outformat=["png", "dot"],
    show=False
):

    # ========================================================================
    # LEFT: DATA SOURCES
    # ========================================================================
    with Cluster("Data Sources", graph_attr=source_cluster_attr):
        sap_source = DatabaseForPostgresqlServers("SAP ECC\n(Inventory & Sales)")
        external_source = APIManagement("External Data\n(Pre-Processed)")

    # ========================================================================
    # DATA LAYER (Pre-Processed with ML Already Applied)
    # ========================================================================
    with Cluster("Data Layer\n(ML Pre-Processed)", graph_attr=data_cluster_attr):
        delta_lake = DataLakeStorage("Delta Lake")

        # Pre-processed tables available for querying
        with Cluster("Available Tables"):
            inventory_table = SQLDatawarehouse("Inventory\nData")
            sales_table = SQLDatawarehouse("Sales\nData")
            forecast_table = SQLDatawarehouse("Forecast\nData")
            recommendation_table = SQLDatawarehouse("Recommendation\nData")

    # ========================================================================
    # CENTER: AI AGENT (Query & Interpret)
    # ========================================================================
    with Cluster("AI Agent (Databricks)", graph_attr=agent_cluster_attr):
        agent_query = Databricks("Agent Bricks\n(Query Engine)")
        agent_llm = FunctionApps("LLM\n(Interpret Results)")

    # ========================================================================
    # RIGHT: NOTIFICATION & USER INTERACTION
    # ========================================================================
    email_notification = ServiceBus("Email Notification\n(with Digital Assistant Link)")
    digital_assistant = AppServices("Digital Assistant\n(Follow-up Queries)")

    # User
    inventory_manager = Users("Inventory Manager")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT with Numbered Steps
    # ========================================================================

    # STEP 1-2: SOURCE → DATA LAYER (Pre-Processed)
    sap_source >> Edge(label="[1] load", color=COLOR_SOURCE, style="bold") >> delta_lake
    external_source >> Edge(label="[2] load", color=COLOR_SOURCE, style="bold") >> delta_lake

    # STEP 3: DELTA LAKE → TABLES (Data Organization)
    delta_lake >> Edge(label="[3] organize", color=COLOR_DATA, style="bold") >> inventory_table
    delta_lake >> Edge(label="", color=COLOR_DATA, style="dotted") >> sales_table
    delta_lake >> Edge(label="", color=COLOR_DATA, style="dotted") >> forecast_table
    delta_lake >> Edge(label="", color=COLOR_DATA, style="dotted") >> recommendation_table

    # STEP 4-5: USER QUERY → AGENT
    inventory_manager >> Edge(label="[4] query", color=COLOR_USER, style="bold") >> agent_query

    # STEP 6-7: AGENT QUERIES TABLES
    agent_query >> Edge(label="[5] SQL query", color=COLOR_AGENT, style="bold") >> inventory_table
    agent_query >> Edge(label="", color=COLOR_AGENT, style="dotted") >> sales_table
    agent_query >> Edge(label="", color=COLOR_AGENT, style="dotted") >> forecast_table
    agent_query >> Edge(label="", color=COLOR_AGENT, style="dotted") >> recommendation_table

    # STEP 8: QUERY RESULTS → LLM INTERPRETATION
    inventory_table >> Edge(label="[6] results", color=COLOR_AGENT, style="bold") >> agent_llm
    sales_table >> Edge(label="", color=COLOR_AGENT, style="dotted") >> agent_llm
    forecast_table >> Edge(label="", color=COLOR_AGENT, style="dotted") >> agent_llm
    recommendation_table >> Edge(label="", color=COLOR_AGENT, style="dotted") >> agent_llm

    # STEP 9: LLM → EMAIL NOTIFICATION
    agent_llm >> Edge(label="[7] send\nnotification", color=COLOR_NOTIFICATION, style="bold") >> email_notification

    # STEP 10: EMAIL → USER (with Digital Assistant Link)
    email_notification >> Edge(label="[8] notify", color=COLOR_NOTIFICATION, style="bold") >> inventory_manager

    # STEP 11: USER → DIGITAL ASSISTANT (Follow-up Queries)
    inventory_manager >> Edge(label="[9] follow-up", color=COLOR_USER, style="dashed") >> digital_assistant

    # STEP 12: DIGITAL ASSISTANT → AGENT (Loop)
    digital_assistant >> Edge(label="[10] query", color=COLOR_USER, style="dashed") >> agent_query

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io format using absolute path
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v6.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v6.drawio")

    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v6.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Draw.io conversion failed: {e}")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 6 - Query-Based AI Agents):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v6.png")
print("  - diagrams/d2c_inventory_ai_agents_v6.dot")
print("  - diagrams/d2c_inventory_ai_agents_v6.drawio")

print("\n" + "="*80)
print("📊 D2C INVENTORY OPTIMIZATION - V6 ARCHITECTURE (QUERY-BASED AGENTS):")
print("="*80)

print("\n🔵 DATA SOURCES")
print("  • SAP ECC (Inventory & Sales)")
print("  • External Data (Pre-Processed with ML)")

print("\n🟣 DATA LAYER (Pre-Processed Tables)")
print("  [1-2] Sources → Delta Lake (Load Pre-Processed Data)")
print("  [3] Delta Lake → Organize into Tables:")
print("      • Inventory Data")
print("      • Sales Data")
print("      • Forecast Data (ML Already Applied)")
print("      • Recommendation Data (ML Already Applied)")

print("\n🟡 USER INTERACTION")
print("  [4] Inventory Manager → Query Agent")
print("     Example: 'What are the optimal stock levels for next week?'")

print("\n🔴 AI AGENT (Query & Interpret)")
print("  [5] Agent Bricks → SQL Query to Tables")
print("  [6] Tables → Return Results to LLM")
print("  [7] LLM → Interpret Results & Generate Email")

print("\n🔵 NOTIFICATION & FOLLOW-UP")
print("  [8] Email → Inventory Manager")
print("      • Interpreted Results")
print("      • Link to Digital Assistant for Follow-up Queries")
print("  [9-10] Manager → Digital Assistant → Agent (Query Loop)")

print("\n" + "="*80)
print("✨ Version 6 Key Changes (Major Architecture Shift):")
print("="*80)
print("  ✓ NO ML training/forecasting - data is pre-processed")
print("  ✓ Agent queries existing tables (not building models)")
print("  ✓ LLM interprets query results (not making predictions)")
print("  ✓ Email notification with digital assistant link")
print("  ✓ User can follow up with more queries via digital assistant")
print("  ✓ 10 numbered steps for clear traceability")
print("  ✓ As-Is to Future State architecture")
print("="*80)
