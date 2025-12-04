#!/usr/bin/env python3
"""
D2C Inventory Optimization with AI Agents - Architecture Diagram
Version 3: Generic, Left-to-Right Flow with AgentBricks

Key Changes in V3:
- Left-to-right flow direction (rankdir=LR)
- Simplified data ingestion and integration
- Demand forecasting and feature engineering inside Databricks
- Expanded AI Agent block with AgentBricks tools and capabilities
- Abstracted feedback and continuous learning
- Maintained numbered flow sequences
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.storage import StorageAccounts, DataLakeStorage
from diagrams.onprem.analytics import Spark
from diagrams.onprem.workflow import Airflow
from diagrams.custom import Custom
import subprocess

# Color palette
COLOR_SOURCE = "#4285F4"           # Blue - Data Sources
COLOR_INTEGRATION = "#9C27B0"      # Purple - Integration
COLOR_DATABRICKS = "#FF6F00"       # Orange - Databricks
COLOR_AGENT = "#E91E63"            # Pink - AI Agent
COLOR_ACTION = "#4CAF50"           # Green - Action/Execution
COLOR_FEEDBACK = "#F44336"         # Red - Feedback/Learning
COLOR_HUMAN = "#00BCD4"            # Cyan - Human Oversight

# Graph attributes for left-to-right flow
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "rankdir": "LR",  # LEFT TO RIGHT flow
    "compound": "true",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.5"
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

action_cluster_attr = {
    "bgcolor": "#E8F5E9",
    "fontsize": "14",
    "fontcolor": COLOR_ACTION,
    "penwidth": "2.5",
    "style": "rounded"
}

with Diagram(
    "D2C Inventory Optimization - AI Agents (v3 - Left-to-Right)",
    filename="diagrams/d2c_inventory_ai_agents_v3",
    direction="LR",
    graph_attr=graph_attr,
    outformat=["png", "dot"],
    show=False
):

    # ========================================================================
    # LEFT: DATA SOURCES
    # ========================================================================
    with Cluster("Data Sources", graph_attr=source_cluster_attr):
        sap_source = DatabaseForPostgresqlServers("SAP ECC\n(Inventory, Sales,\nMaster Data)")
        external_source = APIManagement("External APIs\n(Weather, Social,\nEconomic)")

    # ========================================================================
    # DATA INTEGRATION (Simplified)
    # ========================================================================
    with Cluster("Data Integration", graph_attr=integration_cluster_attr):
        data_connector = ServiceBus("Data Ingestion\nPipeline")
        delta_lake = DataLakeStorage("Delta Lake\n(Bronze/Silver/Gold)")

    # ========================================================================
    # DATABRICKS PLATFORM (Center - Main Processing)
    # ========================================================================
    with Cluster("Databricks Platform", graph_attr=databricks_cluster_attr):

        # Feature Engineering & Data Preparation (Inside Databricks)
        with Cluster("Feature Engineering &\nData Preparation"):
            feature_eng = Spark("Feature Store\n(Unified Features)")
            data_quality = FunctionApps("Data Quality\nValidation")

        # Demand Forecasting Models (Inside Databricks)
        with Cluster("Demand Forecasting\nModels"):
            ml_models = MachineLearningServiceWorkspaces("ML Models\n(ARIMA, Prophet,\nLSTM, XGBoost)")
            mlflow = Databricks("MLflow\nModel Registry")

        # AI Agent with AgentBricks (Expanded with tools and capabilities)
        with Cluster("AI Agent\n(Mosaic AI Agent Framework)", graph_attr=agent_cluster_attr):

            # AgentBricks Core
            agent_core = Databricks("Agent Bricks\n(Auto-Optimized)")

            # AgentBricks Tools Layer
            with Cluster("AgentBricks Tools"):
                vector_search = DataLakeStorage("Vector Search\n(Knowledge Base)")
                uc_functions = FunctionApps("UC Functions\n(Business Logic)")
                mcp_servers = ServiceBus("MCP Servers\n(External Tools)")

            # Agent Capabilities
            agent_reasoning = Databricks("Reasoning Engine\n(Multi-Model)")
            agent_optimization = FunctionApps("Optimization\n(Linear Programming)")
            agent_recommendation = APIManagement("Recommendation\nEngine")

    # ========================================================================
    # RIGHT: ACTION & HUMAN OVERSIGHT
    # ========================================================================
    with Cluster("Action & Oversight", graph_attr=action_cluster_attr):
        dashboard = Databricks("Analytics\nDashboard")
        inventory_manager = Custom("Inventory\nManager", "./icons/user.png") if False else FunctionApps("Inventory\nManager")
        execution = ServiceBus("Execution\nPipeline")

    # ========================================================================
    # FEEDBACK LOOP (Abstracted & Simplified)
    # ========================================================================
    feedback_loop = APIManagement("Feedback &\nContinuous Learning")

    # ========================================================================
    # DATA FLOW - LEFT TO RIGHT with Numbered Steps
    # ========================================================================

    # STEP 1-2: SOURCE → INTEGRATION
    sap_source >> Edge(label="[1] extract", color=COLOR_SOURCE, style="bold") >> data_connector
    external_source >> Edge(label="[2] ingest", color=COLOR_SOURCE, style="bold") >> data_connector

    # STEP 3: INTEGRATION → DELTA LAKE
    data_connector >> Edge(label="[3] store", color=COLOR_INTEGRATION, style="bold") >> delta_lake

    # STEP 4-5: DELTA LAKE → FEATURE ENGINEERING
    delta_lake >> Edge(label="[4] load", color=COLOR_DATABRICKS, style="bold") >> data_quality
    data_quality >> Edge(label="[5] validate", color=COLOR_DATABRICKS, style="bold") >> feature_eng

    # STEP 6-7: FEATURE ENGINEERING → ML MODELS
    feature_eng >> Edge(label="[6] features", color=COLOR_DATABRICKS, style="bold") >> ml_models
    ml_models >> Edge(label="[7] register", color=COLOR_DATABRICKS, style="bold") >> mlflow

    # STEP 8: MLFLOW → AGENT CORE
    mlflow >> Edge(label="[8] deploy", color=COLOR_AGENT, style="bold") >> agent_core

    # STEP 9-11: AGENTBRICKS TOOLS → AGENT CORE
    vector_search >> Edge(label="[9] knowledge", color=COLOR_AGENT, style="dotted") >> agent_core
    uc_functions >> Edge(label="[10] functions", color=COLOR_AGENT, style="dotted") >> agent_core
    mcp_servers >> Edge(label="[11] external", color=COLOR_AGENT, style="dotted") >> agent_core

    # STEP 12-14: AGENT INTERNAL FLOW
    agent_core >> Edge(label="[12] reason", color=COLOR_AGENT, style="bold") >> agent_reasoning
    agent_reasoning >> Edge(label="[13] optimize", color=COLOR_AGENT, style="bold") >> agent_optimization
    agent_optimization >> Edge(label="[14] recommend", color=COLOR_AGENT, style="bold") >> agent_recommendation

    # STEP 15: RECOMMENDATIONS → DASHBOARD
    agent_recommendation >> Edge(label="[15] visualize", color=COLOR_ACTION, style="bold") >> dashboard

    # STEP 16-17: HUMAN OVERSIGHT → EXECUTION
    dashboard >> Edge(label="[16] review", color=COLOR_HUMAN, style="bold") >> inventory_manager
    inventory_manager >> Edge(label="[17] approve", color=COLOR_ACTION, style="bold") >> execution

    # STEP 18: EXECUTION → SAP (Action)
    execution >> Edge(label="[18] execute", color=COLOR_ACTION, style="bold") >> sap_source

    # STEP 19-20: FEEDBACK LOOP (Abstracted & Simplified)
    sap_source >> Edge(label="[19] results", color=COLOR_FEEDBACK, style="dashed") >> feedback_loop
    feedback_loop >> Edge(label="[20] retrain", color=COLOR_FEEDBACK, style="dashed") >> ml_models

    # Additional feedback paths
    feedback_loop >> Edge(label="insights", color=COLOR_FEEDBACK, style="dotted") >> agent_core
    feedback_loop >> Edge(label="update", color=COLOR_FEEDBACK, style="dotted") >> feature_eng

print("✓ PNG and DOT files generated in diagrams/")

# Convert to Draw.io format using absolute path
try:
    import os
    dot_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v3.dot")
    drawio_path = os.path.abspath("diagrams/d2c_inventory_ai_agents_v3.drawio")

    subprocess.run([
        "graphviz2drawio",
        dot_path,
        "-o", drawio_path
    ], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v3.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Draw.io conversion failed: {e}")
except Exception as e:
    print(f"✗ Draw.io conversion error: {e}")

print("\n" + "="*80)
print("Generated files (Version 3 - Left-to-Right with AgentBricks):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v3.png")
print("  - diagrams/d2c_inventory_ai_agents_v3.dot")
print("  - diagrams/d2c_inventory_ai_agents_v3.drawio")

print("\n" + "="*80)
print("📊 D2C Inventory Optimization - V3 ARCHITECTURE:")
print("="*80)

print("\n🔵 LEFT: DATA SOURCES")
print("  • SAP ECC (Inventory, Sales, Master Data)")
print("  • External APIs (Weather, Social, Economic)")

print("\n🟣 DATA INTEGRATION (Simplified)")
print("  [1-2] Sources → Data Ingestion Pipeline")
print("  [3] Pipeline → Delta Lake (Bronze/Silver/Gold)")

print("\n🟠 CENTER: DATABRICKS PLATFORM")
print("  ")
print("  📦 Feature Engineering & Data Preparation:")
print("    [4-5] Delta Lake → Data Quality → Feature Store")
print("  ")
print("  🤖 Demand Forecasting Models:")
print("    [6-7] Features → ML Models → MLflow Registry")
print("  ")
print("  🧠 AI AGENT (Mosaic AI Agent Framework with AgentBricks):")
print("    [8] MLflow → Agent Bricks (Auto-Optimized)")
print("    ")
print("    AgentBricks Tools:")
print("      [9] Vector Search (Knowledge Base)")
print("      [10] UC Functions (Business Logic)")
print("      [11] MCP Servers (External Tools)")
print("    ")
print("    Agent Processing:")
print("      [12] Reasoning Engine (Multi-Model)")
print("      [13] Optimization (Linear Programming)")
print("      [14] Recommendation Engine")

print("\n🟢 RIGHT: ACTION & HUMAN OVERSIGHT")
print("  [15] Recommendations → Analytics Dashboard")
print("  [16] Dashboard → Inventory Manager (Review)")
print("  [17] Manager → Execution Pipeline (Approve)")
print("  [18] Execute → SAP ECC (Transfer Orders)")

print("\n🔴 FEEDBACK & CONTINUOUS LEARNING (Abstracted)")
print("  [19] SAP Results → Feedback Loop")
print("  [20] Feedback → Retrain ML Models")
print("  • Insights → Agent Core (Improvement)")
print("  • Updates → Feature Engineering (Refinement)")

print("\n" + "="*80)
print("✨ Version 3 Key Improvements:")
print("="*80)
print("  ✓ Left-to-right flow direction for better readability")
print("  ✓ Simplified data ingestion and integration layer")
print("  ✓ Feature engineering and demand forecasting inside Databricks")
print("  ✓ Expanded AI Agent with AgentBricks tools and capabilities:")
print("    - Vector Search for knowledge base retrieval")
print("    - UC Functions for business logic execution")
print("    - MCP Servers for external tool integration")
print("    - Multi-model reasoning engine")
print("    - Linear programming optimization")
print("  ✓ Abstracted feedback and continuous learning")
print("  ✓ 20 numbered flow steps for complete traceability")
print("  ✓ More generic and focused architecture")
print("="*80)
