"""
D2C Inventory AI Agents V12 - Abstracted Hybrid Architecture
Left-to-Right flow with simplified Prompt Flow representation
Generates PNG, PDF, and DOT (for Draw.io conversion)
"""

import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import FunctionApps
from diagrams.azure.integration import APIManagement, LogicApps
from diagrams.azure.ml import MachineLearningServiceWorkspaces, CognitiveServices
from diagrams.azure.database import DataLake
from diagrams.azure.analytics import Databricks, SynapseAnalytics
from diagrams.azure.storage import BlobStorage
from diagrams.azure.security import KeyVaults
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.storage import Storage
from diagrams.saas.chat import Slack

# Graph attributes for clean left-to-right layout
graph_attr = {
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.0",
    "fontsize": "12",
    "bgcolor": "white",
    "pad": "0.5",
    "compound": "true",
    "dpi": "150"
}

# Cluster styles with distinct colors
data_sources_cluster = {
    "fontsize": "14",
    "bgcolor": "#F3E5F5",
    "style": "rounded",
    "margin": "15",
    "fontcolor": "#7B1FA2"
}

data_integration_cluster = {
    "fontsize": "14",
    "bgcolor": "#FCE4EC",
    "style": "rounded",
    "margin": "15",
    "fontcolor": "#C2185B"
}

databricks_cluster = {
    "fontsize": "14",
    "bgcolor": "#FFF3E0",
    "style": "rounded",
    "margin": "20",
    "fontcolor": "#FF6F00"
}

azure_ai_cluster = {
    "fontsize": "14",
    "bgcolor": "#E3F2FD",
    "style": "rounded",
    "margin": "20",
    "fontcolor": "#0078D4"
}

app_layer_cluster = {
    "fontsize": "14",
    "bgcolor": "#E8F5E9",
    "style": "rounded",
    "margin": "15",
    "fontcolor": "#2E7D32"
}

# Create the diagram
with Diagram(
    "D2C Inventory AI Agents V12\nHybrid: Azure AI Foundry + Databricks (Abstracted)",
    filename="diagrams/d2c_inventory_ai_agents_v12",
    outformat=["png", "pdf", "dot"],
    show=False,
    direction="LR",
    graph_attr=graph_attr
):

    # ============================================
    # LEFT SIDE: Data Sources
    # ============================================
    with Cluster("Data Sources", graph_attr=data_sources_cluster):
        sap = PostgreSQL("SAP ECC\n(Inventory, Sales)")

    # ============================================
    # Data Integration
    # ============================================
    with Cluster("Data Integration", graph_attr=data_integration_cluster):
        data_factory = SynapseAnalytics("Azure Data Factory")

    # ============================================
    # CENTER-LEFT: Databricks Data Platform
    # ============================================
    with Cluster("Databricks Platform\n(Data Layer)", graph_attr=databricks_cluster):
        delta_lake = DataLake("Delta Lake")
        lakehouse = Storage("Lakehouse\nTables")
        unity_catalog = KeyVaults("Unity Catalog")
        sql_warehouse = Databricks("SQL Warehouse")

    # ============================================
    # CENTER-RIGHT: Azure AI Foundry (Abstracted)
    # ============================================
    with Cluster("Azure AI Foundry\n(Agentic AI Layer)", graph_attr=azure_ai_cluster):
        # Abstracted Agent Framework - single block instead of detailed nodes
        agent_framework = MachineLearningServiceWorkspaces("Agent Framework\n(Prompt Flow)")

        # Tools as simple blocks
        sql_connector = Databricks("SQL Connector")
        ai_search = CognitiveServices("AI Search\n(RAG)")

        # LLM
        azure_openai = MachineLearningServiceWorkspaces("Azure OpenAI\n(GPT-4)")

    # ============================================
    # RIGHT SIDE: Application Layer
    # ============================================
    with Cluster("Application Layer", graph_attr=app_layer_cluster):
        agent_api = APIManagement("Agent API")

        # Entry Point 1: Interactive
        digital_assistant = Users("Digital\nAssistant")

        # Entry Point 2: Batch
        batch_scheduler = FunctionApps("Batch\nScheduler")
        email_service = LogicApps("Email\nService")

    # ============================================
    # FAR RIGHT: End Users
    # ============================================
    business_user = Users("Business User\n(Inventory Manager)")
    team_email = Slack("Team Email")

    # ============================================
    # CONNECTIONS - Left to Right Flow
    # ============================================

    # Data Flow (Purple) - Steps 1-4
    sap >> Edge(label="[1] extract", color="purple") >> data_factory
    data_factory >> Edge(label="[2] ingest", color="purple") >> delta_lake

    # Data Organization (Orange) - Steps 3-6
    delta_lake >> Edge(label="[3] store", color="orange") >> lakehouse
    delta_lake >> Edge(label="[4] govern", color="orange") >> unity_catalog
    lakehouse >> Edge(label="[5] query", color="orange", style="dashed") >> sql_warehouse

    # AI Processing (Blue) - Steps 7-12
    sql_warehouse >> Edge(label="[6] data", color="blue") >> sql_connector
    sql_connector >> Edge(label="[7]", color="blue") >> agent_framework
    ai_search >> Edge(label="[8] docs", color="blue") >> agent_framework
    agent_framework >> Edge(label="[9] interpret", color="blue") >> azure_openai
    azure_openai >> Edge(label="[10] response", color="blue") >> agent_api

    # Interactive Flow (Green Solid) - Steps 11-14
    business_user >> Edge(label="[11] query", color="green") >> digital_assistant
    digital_assistant >> Edge(label="[12]", color="green") >> agent_api
    agent_api >> Edge(label="[13]", color="green") >> digital_assistant
    digital_assistant >> Edge(label="[14] display", color="green") >> business_user

    # Batch Flow (Green Dashed) - Steps 15-18
    batch_scheduler >> Edge(label="[15] batch", color="green", style="dashed") >> agent_api
    agent_api >> Edge(label="[16] insights", color="green", style="dashed") >> email_service
    email_service >> Edge(label="[17] email", color="green", style="dashed") >> team_email

print("Generated files:")
print("  - diagrams/d2c_inventory_ai_agents_v12.png")
print("  - diagrams/d2c_inventory_ai_agents_v12.pdf")
print("  - diagrams/d2c_inventory_ai_agents_v12.dot")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/d2c_inventory_ai_agents_v12.dot",
        "-o",
        "diagrams/d2c_inventory_ai_agents_v12.drawio"
    ], check=True)
    print("  - diagrams/d2c_inventory_ai_agents_v12.drawio")
except subprocess.CalledProcessError as e:
    print(f"Note: Could not convert to Draw.io format: {e}")
except FileNotFoundError:
    print("Note: graphviz2drawio not found. Install with: pip install graphviz2drawio")
    print("      Draw.io file not generated, but PNG/PDF/DOT are available.")
