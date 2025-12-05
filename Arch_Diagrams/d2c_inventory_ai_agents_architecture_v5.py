#!/usr/bin/env python3
"""
D2C Inventory Optimization with AI Agents - Architecture Diagram
Version 5: Abstract Client Presentation Version

Key Changes in V5:
- More abstract AI Agent representation (simplified details)
- Replaced Action & Oversight with email notification to Inventory Manager
- Clean left-to-right flow inside Databricks
- Maintained numbered sequences on directions
- Client-presentation ready (not overly detailed)
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.storage import DataLakeStorage
from diagrams.onprem.analytics import Spark
from diagrams.custom import Custom
import subprocess

# Color palette (simplified for client presentation)
COLOR_SOURCE = "#4285F4"           # Blue - Data Sources
COLOR_INTEGRATION = "#9C27B0"      # Purple - Integration
COLOR_DATABRICKS = "#FF6F00"       # Orange - Databricks
COLOR_AGENT = "#E91E63"            # Pink - AI Agent
COLOR_NOTIFICATION = "#00BCD4"     # Cyan - Notifications
COLOR_FEEDBACK = "#F44336"         # Red - Feedback

# Graph attributes for clean left-to-right flow
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "rankdir": "LR",
    "compound": "true",
    "splines": "ortho",
    "nodesep": "1.0",
    "ranksep": "2.0"
}

# Cluster styles
source_cluster_attr = {
    "bgcolor": "#E3F2FD",
    "fontsize": "14",
    "fontcolor": COLOR_SOURCE,
    "penwidth": "2.5",
    "style": "rounded"
}

integration_cluster_attr = {
    "bgcolor": "#F3E5F5",
    "fontsize": "14",
    "fontcolor": COLOR_INTEGRATION,
    "penwidth": "2.5",
    "style": "rounded"
}

databricks_cluster_attr = {
    "bgcolor": "#FFF3E0",
    "fontsize": "14",
    "fontcolor": COLOR_DATABRICKS,
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
    "D2C Inventory Optimization - AI Agents (v5 - Client Presentation)",
    filename="diagrams/d2c_inventory_ai_agents_v5",
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
        external_source = APIManagement("External Data\n(Market Trends)")

    # ========================================================================
    # DATA INTEGRATION
    # ========================================================================
    with Cluster("Data Integration", graph_attr=integration_cluster_attr):
        data_ingestion = ServiceBus("Data Ingestion")
        delta_lake = DataLakeStorage("Delta Lake\n(Data Storage)")

    # ========================================================================
    # CENTER: DATABRICKS PLATFORM (Clean Left-to-Right Flow)
    # ========================================================================
    with Cluster("Databricks AI Platform", graph_attr=databricks_cluster_attr):

        # Sub-components in left-to-right order
        feature_store = Spark("Feature\nEngineering")
        ml_models = MachineLearningServiceWorkspaces("Demand\nForecasting")

        # AI Agent (Abstract - Simplified)
        with Cluster("AI Agent", graph_attr=agent_cluster_attr):
            agent_engine = Databricks("Recommendation\nEngine")

    # ========================================================================
    # RIGHT: NOTIFICATION (Replaced Action & Oversight)
    # ========================================================================
    email_notification = ServiceBus("Email Notification\n(Inventory Manager)")

    # ========================================================================
    # FEEDBACK LOOP (Abstract)
    # ========================================================================
    feedback = APIManagement("Continuous\nLearning")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT with Numbered Steps
    # ========================================================================

    # STEP 1-2: SOURCE → INTEGRATION
    sap_source >> Edge(label="[1] extract", color=COLOR_SOURCE, style="bold") >> data_ingestion
    external_source >> Edge(label="[2] ingest", color=COLOR_SOURCE, style="bold") >> data_ingestion

    # STEP 3: INTEGRATION → DELTA LAKE
    data_ingestion >> Edge(label="[3] store", color=COLOR_INTEGRATION, style="bold") >> delta_lake

    # STEP 4-6: DELTA LAKE → DATABRICKS (Clean Left-to-Right)
    delta_lake >> Edge(label="[4] load", color=COLOR_DATABRICKS, style="bold") >> feature_store
    feature_store >> Edge(label="[5] features", color=COLOR_DATABRICKS, style="bold") >> ml_models
    ml_models >> Edge(label="[6] forecast", color=COLOR_DATABRICKS, style="bold") >> agent_engine

    # STEP 7: AI AGENT → EMAIL NOTIFICATION
    agent_engine >> Edge(label="[7] recommend", color=COLOR_NOTIFICATION, style="bold") >> email_notification

    # STEP 8: EMAIL → SAP (Manager approves and executes)
    email_notification >> Edge(label="[8] execute", color=COLOR_NOTIFICATION, style="bold") >> sap_source

    # STEP 9-10: FEEDBACK LOOP (Abstract)
    sap_source >> Edge(label="[9] results", color=COLOR_FEEDBACK, style="dashed") >> feedback
    feedback >> Edge(label="[10] retrain", color=COLOR_FEEDBACK, style="dashed") >> ml_models

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io format using absolute path
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v5.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v5.drawio")

    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v5.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Draw.io conversion failed: {e}")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 5 - Abstract Client Presentation):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v5.png")
print("  - diagrams/d2c_inventory_ai_agents_v5.dot")
print("  - diagrams/d2c_inventory_ai_agents_v5.drawio")

print("\n" + "="*80)
print("📊 D2C Inventory Optimization - V5 ARCHITECTURE (CLIENT PRESENTATION):")
print("="*80)

print("\n🔵 DATA SOURCES")
print("  • SAP ECC (Inventory & Sales)")
print("  • External Data (Market Trends)")

print("\n🟣 DATA INTEGRATION")
print("  [1-2] Sources → Data Ingestion")
print("  [3] Ingestion → Delta Lake (Data Storage)")

print("\n🟠 DATABRICKS AI PLATFORM (Clean Left-to-Right Flow)")
print("  [4] Delta Lake → Feature Engineering")
print("  [5] Features → Demand Forecasting")
print("  [6] Forecasting → AI Agent (Recommendation Engine)")

print("\n🔵 EMAIL NOTIFICATION")
print("  [7] AI Agent → Email Notification (Inventory Manager)")
print("  [8] Manager Approval → Execute in SAP ECC")

print("\n🔴 CONTINUOUS LEARNING")
print("  [9] SAP Results → Feedback Loop")
print("  [10] Feedback → Retrain Demand Forecasting Models")

print("\n" + "="*80)
print("✨ Version 5 Key Features (Client Presentation Ready):")
print("="*80)
print("  ✓ Abstract AI Agent representation (simplified for client)")
print("  ✓ Email notification replaces complex Action & Oversight")
print("  ✓ Clean left-to-right flow inside Databricks")
print("  ✓ 10 numbered steps for clear traceability")
print("  ✓ Simple, high-level architecture (not overly detailed)")
print("  ✓ Professional presentation-ready design")
print("="*80)
