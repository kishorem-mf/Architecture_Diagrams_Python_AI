"""
D2C Inventory AI Agents V11 - Hybrid Azure AI Foundry + Databricks Architecture
Generates PNG diagram for the hybrid agentic AI architecture
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import FunctionApps
from diagrams.azure.integration import APIManagement, LogicApps
from diagrams.azure.ml import MachineLearningServiceWorkspaces, CognitiveServices
from diagrams.azure.database import DataLake
from diagrams.azure.analytics import Databricks, SynapseAnalytics
from diagrams.azure.storage import BlobStorage
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.general import Resourcegroups
from diagrams.azure.security import KeyVaults
from diagrams.azure.devops import ApplicationInsights
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.custom import Custom
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.programming.flowchart import Action, Decision, Document
from diagrams.saas.chat import Slack

# Graph attributes
graph_attr = {
    "splines": "ortho",
    "nodesep": "0.6",
    "ranksep": "0.8",
    "fontsize": "12",
    "bgcolor": "white",
    "pad": "0.5",
    "compound": "true",
    "dpi": "150"
}

# Cluster styles
azure_ai_cluster = {
    "fontsize": "14",
    "bgcolor": "#E3F2FD",
    "style": "rounded",
    "margin": "20",
    "fontcolor": "#0078D4"
}

databricks_cluster = {
    "fontsize": "14",
    "bgcolor": "#FFF3E0",
    "style": "rounded",
    "margin": "20",
    "fontcolor": "#FF6F00"
}

app_layer_cluster = {
    "fontsize": "14",
    "bgcolor": "#E8F5E9",
    "style": "rounded",
    "margin": "15",
    "fontcolor": "#2E7D32"
}

data_sources_cluster = {
    "fontsize": "14",
    "bgcolor": "#F3E5F5",
    "style": "rounded",
    "margin": "15",
    "fontcolor": "#7B1FA2"
}

prompt_flow_cluster = {
    "fontsize": "13",
    "bgcolor": "#BBDEFB",
    "style": "rounded",
    "margin": "10"
}

# Create the diagram
with Diagram(
    "D2C Inventory AI Agents V11\nHybrid: Azure AI Foundry + Databricks",
    filename="diagrams/d2c_inventory_ai_agents_v11",
    outformat=["png", "pdf"],
    show=False,
    direction="LR",
    graph_attr=graph_attr
):

    # Data Sources
    with Cluster("Data Sources", graph_attr=data_sources_cluster):
        sap = PostgreSQL("SAP ECC\n(Inventory, Sales)")

    # Data Integration
    with Cluster("Data Integration\n(Azure)", graph_attr={"bgcolor": "#FCE4EC", "margin": "15"}):
        data_factory = SynapseAnalytics("Azure Data Factory\nIngestion Pipelines")

    # Databricks Platform (Data Layer)
    with Cluster("Databricks Platform\n(Data Layer)", graph_attr=databricks_cluster):
        delta_lake = DataLake("Delta Lake\n(Data Storage)")

        with Cluster("Data Assets"):
            lakehouse = Storage("Lakehouse\n(Tables)")
            unity_catalog = KeyVaults("Unity Catalog\n(Governance)")

        sql_warehouse = Databricks("Databricks SQL\nWarehouse")

    # Azure AI Foundry (Agentic AI)
    with Cluster("Azure AI Foundry\n(Agentic AI Layer)", graph_attr=azure_ai_cluster):

        with Cluster("Prompt Flow Pipeline", graph_attr=prompt_flow_cluster):
            orchestrator = Action("Orchestrator\nNode")
            planner = Decision("Planner\nNode")
            tool_executor = Action("Tool Executor\nNode")

        with Cluster("Tools"):
            sql_connector = Databricks("Databricks SQL\nConnector")
            ai_search = CognitiveServices("Azure AI Search\n(RAG)")

        azure_openai = MachineLearningServiceWorkspaces("Azure OpenAI\n(GPT-4)")
        response_node = Document("Response\nNode")

    # Application Layer
    with Cluster("Application Layer", graph_attr=app_layer_cluster):

        with Cluster("Entry Point 1: Interactive"):
            digital_assistant = Users("Digital Assistant\n(Chatbot)")

        with Cluster("Entry Point 2: Batch"):
            batch_scheduler = FunctionApps("Batch Scheduler\n(Azure Functions)")
            email_service = LogicApps("Email Service")

        agent_api = APIManagement("Agent API")

    # Business Users
    business_user = Users("Business User\n(Inventory Manager)")
    team_email = Slack("Team Email\nNotification")

    # Connections - Data Flow
    sap >> Edge(label="[1,2] extract", color="purple") >> data_factory
    data_factory >> Edge(label="[3,4] store", color="purple") >> delta_lake
    delta_lake >> Edge(label="[5] govern", color="orange") >> unity_catalog
    delta_lake >> Edge(label="[6] organize", color="orange") >> lakehouse

    # Connections - Entry Points
    business_user >> Edge(label="[8a] query", color="green") >> digital_assistant
    digital_assistant >> Edge(label="[9a] request", color="green") >> agent_api

    batch_scheduler >> Edge(label="[9b] batch", color="green", style="dashed") >> agent_api

    # Connections - AI Processing
    agent_api >> Edge(label="[10] route", color="blue") >> orchestrator
    orchestrator >> Edge(label="[11] plan", color="blue") >> planner
    planner >> Edge(label="[12] execute", color="blue") >> tool_executor

    tool_executor >> Edge(label="[13] SQL", color="blue") >> sql_connector
    tool_executor >> Edge(label="[14] search", color="blue") >> ai_search

    sql_connector >> Edge(label="[15] query", color="orange") >> sql_warehouse
    sql_warehouse >> Edge(color="orange", style="dashed") >> lakehouse

    ai_search >> Edge(label="[16] docs", color="blue") >> response_node
    sql_connector >> Edge(label="[17] results", color="blue") >> response_node

    response_node >> Edge(label="[18] interpret", color="blue") >> azure_openai
    azure_openai >> Edge(label="response", color="blue") >> agent_api

    # Connections - Response
    agent_api >> Edge(label="[19a] response", color="green") >> digital_assistant
    digital_assistant >> Edge(label="[20a] display", color="green") >> business_user

    agent_api >> Edge(label="[19b] insights", color="green", style="dashed") >> email_service
    email_service >> Edge(label="[20b] email", color="green", style="dashed") >> team_email

print("Generated files:")
print("  - diagrams/d2c_inventory_ai_agents_v11.png")
print("  - diagrams/d2c_inventory_ai_agents_v11.pdf")
