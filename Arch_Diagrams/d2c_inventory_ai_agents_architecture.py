"""
D2C Inventory Optimization with AI Agents - Architecture Diagram Generator
Generates PNG, DOT, and Draw.io format diagrams

Architecture Components:
- SAP ECC (Source System)
- Data Ingestion & Storage (Delta Lake)
- Databricks (AI/ML Processing)
- AI Agent (Inventory Optimization Logic)
- Feedback Loop & Continuous Learning
"""

import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.storage import StorageAccounts, DataLakeStorage, BlobStorage
from diagrams.azure.analytics import LogAnalyticsWorkspaces, Databricks as AzureDatabricks
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.integration import ServiceBus, EventGridDomains
from diagrams.onprem.analytics import Databricks, Spark
from diagrams.onprem.database import Mssql
from diagrams.onprem.compute import Server
from diagrams.onprem.client import User
from diagrams.azure.devops import ApplicationInsights
from diagrams.programming.framework import React

# Graph attributes for clean layout
graph_attr = {
    "splines": "ortho",
    "nodesep": "1.0",
    "ranksep": "1.5",
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "compound": "true"
}

# Cluster attributes for different layers
sap_ecc_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E3F2FD",  # Light Blue - SAP
    "style": "rounded",
    "margin": "20"
}

ingestion_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF9C4",  # Light Yellow - Data Ingestion
    "style": "rounded",
    "margin": "20"
}

storage_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E8F5E9",  # Light Green - Storage
    "style": "rounded",
    "margin": "20"
}

databricks_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF3E0",  # Light Orange - Databricks
    "style": "rounded",
    "margin": "25"
}

feature_eng_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#FFE0B2",  # Lighter Orange
    "style": "rounded",
    "margin": "15"
}

ml_model_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#FFCC80",  # Medium Orange
    "style": "rounded",
    "margin": "15"
}

ai_agent_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#F3E5F5",  # Light Purple - AI Agent
    "style": "rounded",
    "margin": "20"
}

visualization_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E1BEE7",  # Medium Purple - Visualization
    "style": "rounded",
    "margin": "20"
}

feedback_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFEBEE",  # Light Red - Feedback
    "style": "dashed",
    "margin": "15"
}

# Create the diagram
with Diagram(
    "D2C Inventory Optimization with AI Agents Architecture",
    filename="diagrams/d2c_inventory_ai_agents",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr
):

    # SAP ECC Source System
    with Cluster("SAP ECC\n(Source System)", graph_attr=sap_ecc_cluster_attr):
        sap_inventory = Mssql("Inventory Data\n(D2C, Prime, General)")
        sap_sales = Mssql("Sales Orders\n& Shipping Data")
        sap_master = Mssql("Master Data\n(Products, Plants)")

    # External Data Sources
    external_weather = Server("Weather Data")
    external_social = Server("Social Media\nTrends")
    external_economic = Server("Economic\nIndicators")

    # Data Ingestion Layer
    with Cluster("Data Ingestion & Integration", graph_attr=ingestion_cluster_attr):
        sap_bdc = ServiceBus("SAP BDC\nConnector")
        external_apis = EventGridDomains("External\nAPIs")
        streaming = ServiceBus("Spark Structured\nStreaming")

    # Cloud Storage Layer
    with Cluster("Delta Lake\n(Data Lake Storage)", graph_attr=storage_cluster_attr):
        raw_data = DataLakeStorage("Raw Data\nLayer")
        transformed_data = DataLakeStorage("Transformed\nData Layer")
        feature_store = BlobStorage("Feature Store\n(Reusable Features)")

    # Databricks Processing & ML
    with Cluster("Databricks\n(AI/ML Processing Engine)", graph_attr=databricks_cluster_attr):

        # Feature Engineering
        with Cluster("Feature Engineering\n& Data Preparation", graph_attr=feature_eng_cluster_attr):
            data_cleaning = Spark("Data Cleaning\n& Aggregation")
            feature_creation = Spark("Feature Creation\n(Seasonality, Trends)")
            data_validation = ApplicationInsights("Data Quality\nValidation")

        # ML Model Training
        with Cluster("Demand Forecasting Model", graph_attr=ml_model_cluster_attr):
            ml_training = MachineLearningServiceWorkspaces("Model Training\n(ARIMA, Prophet, LSTM)")
            ml_evaluation = MachineLearningServiceWorkspaces("Model Evaluation\n(MAE, RMSE)")
            ml_registry = DatabaseForPostgresqlServers("MLflow\nModel Registry")
            hyperparameter = MachineLearningServiceWorkspaces("Hyperparameter\nTuning (Hyperopt)")

        # AI Agent
        with Cluster("AI Agent\n(Inventory Optimization Logic)", graph_attr=ai_agent_cluster_attr):
            demand_forecast = MachineLearningServiceWorkspaces("Demand Forecast\nEngine")
            allocation_logic = Server("Inventory Allocation\nLogic")
            optimization = Server("Optimization Algorithm\n(Linear Programming)")
            recommendation_engine = ServiceBus("Recommendation\nEngine")

    # Visualization & Reporting
    with Cluster("Reporting & Visualization", graph_attr=visualization_cluster_attr):
        sac = LogAnalyticsWorkspaces("SAP Analytics\nCloud")
        powerbi = LogAnalyticsWorkspaces("Power BI\nDashboards")
        metrics = ApplicationInsights("Performance Metrics\n(Forecast Accuracy)")

    # Human Oversight
    inventory_manager = User("Inventory Manager\n(Human Oversight)")

    # Feedback Loop
    with Cluster("Feedback & Continuous Learning", graph_attr=feedback_cluster_attr):
        feedback_data = DataLakeStorage("Feedback Data\n(Actual Sales & Inventory)")
        ab_testing = ApplicationInsights("A/B Testing\n& Performance Tracking")
        explainability = MachineLearningServiceWorkspaces("Model Explainability\n(SHAP, LIME)")

    # ============================================================================
    # DATA FLOW CONNECTIONS
    # ============================================================================

    # SAP ECC → Data Ingestion
    sap_inventory >> Edge(label="extract", color="#4285F4") >> sap_bdc
    sap_sales >> Edge(label="extract", color="#4285F4") >> sap_bdc
    sap_master >> Edge(label="extract", color="#4285F4") >> sap_bdc

    # External Sources → Data Ingestion
    external_weather >> Edge(label="API", color="#34A853") >> external_apis
    external_social >> Edge(label="API", color="#34A853") >> external_apis
    external_economic >> Edge(label="API", color="#34A853") >> external_apis

    # Data Ingestion → Streaming
    sap_bdc >> Edge(label="data stream", color="#4285F4") >> streaming
    external_apis >> Edge(label="data stream", color="#34A853") >> streaming

    # Streaming → Delta Lake
    streaming >> Edge(label="ingest", color="#9C27B0", style="bold") >> raw_data
    raw_data >> Edge(label="transform", color="#9C27B0") >> transformed_data

    # Delta Lake → Feature Engineering
    transformed_data >> Edge(label="load", color="#FF9800") >> data_cleaning
    data_cleaning >> Edge(label="clean", style="dotted") >> feature_creation
    feature_creation >> Edge(label="validate", style="dotted") >> data_validation
    data_validation >> Edge(label="store", color="#FF9800") >> feature_store

    # Feature Store → ML Training
    feature_store >> Edge(label="features", color="#FF9800", style="bold") >> ml_training
    ml_training >> Edge(label="evaluate", style="dotted") >> ml_evaluation
    ml_evaluation >> Edge(label="tune", style="dotted") >> hyperparameter
    hyperparameter >> Edge(label="register", color="#FF9800") >> ml_registry

    # ML Model → AI Agent
    ml_registry >> Edge(label="deploy model", color="#9C27B0", style="bold") >> demand_forecast
    transformed_data >> Edge(label="current inventory", color="#4285F4") >> allocation_logic

    # AI Agent Internal Flow
    demand_forecast >> Edge(label="forecast", style="dotted") >> allocation_logic
    allocation_logic >> Edge(label="optimize", style="dotted") >> optimization
    optimization >> Edge(label="recommendations", style="dotted") >> recommendation_engine

    # AI Agent → Visualization
    recommendation_engine >> Edge(label="results", color="#673AB7") >> sac
    recommendation_engine >> Edge(label="results", color="#673AB7") >> powerbi
    ml_evaluation >> Edge(label="metrics", color="#673AB7", style="dashed") >> metrics

    # Visualization → Human Oversight
    sac >> Edge(label="review", color="#E91E63") >> inventory_manager
    powerbi >> Edge(label="review", color="#E91E63") >> inventory_manager
    recommendation_engine >> Edge(label="recommendations", color="#E91E63", style="bold") >> inventory_manager

    # Human Oversight → SAP ECC (Action)
    inventory_manager >> Edge(label="approve\nadjustments", color="#4CAF50", style="bold") >> sap_bdc
    sap_bdc >> Edge(label="create\ntransfer orders", color="#4CAF50", style="bold") >> sap_inventory

    # Feedback Loop - SAP ECC → Feedback
    sap_inventory >> Edge(label="actual inventory\n& sales", color="#F44336", style="dashed") >> feedback_data
    sap_sales >> Edge(label="actual sales", color="#F44336", style="dashed") >> feedback_data

    # Feedback → Learning
    feedback_data >> Edge(label="analyze", color="#F44336") >> ab_testing
    feedback_data >> Edge(label="retrain", color="#F44336", style="bold") >> ml_training
    ml_registry >> Edge(label="explain", color="#F44336", style="dashed") >> explainability
    explainability >> Edge(label="insights", color="#F44336") >> inventory_manager

    # Monitoring Metrics
    ab_testing >> Edge(label="performance", color="#673AB7", style="dashed") >> metrics

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/d2c_inventory_ai_agents.dot",
        "-o",
        "diagrams/d2c_inventory_ai_agents.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\n" + "="*80)
print("Generated files:")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents.png")
print("  - diagrams/d2c_inventory_ai_agents.dot")
print("  - diagrams/d2c_inventory_ai_agents.drawio")

print("\n" + "="*80)
print("📊 D2C Inventory Optimization Architecture Flow:")
print("="*80)
print("  1. SENSE: SAP ECC + External Data → Data Ingestion (SAP BDC, APIs)")
print("  2. STORE: Streaming → Delta Lake (Raw → Transformed → Feature Store)")
print("  3. PREPARE: Feature Engineering (Cleaning, Aggregation, Validation)")
print("  4. TRAIN: ML Model Training (ARIMA, Prophet, LSTM) → MLflow Registry")
print("  5. THINK: AI Agent (Demand Forecast + Allocation Logic + Optimization)")
print("  6. VISUALIZE: SAP Analytics Cloud / Power BI (Dashboards & Metrics)")
print("  7. ACT: Human Oversight → Approve → SAP ECC (Inventory Adjustments)")
print("  8. LEARN: Feedback Loop (Actual Sales & Inventory → Retrain Model)")
print("  9. IMPROVE: A/B Testing + Model Explainability (SHAP, LIME)")

print("\n" + "="*80)
print("🎯 Key Architecture Components:")
print("="*80)
print("  • SAP ECC: Source system (inventory, sales, master data)")
print("  • SAP BDC: Data extraction connector")
print("  • Delta Lake: Scalable, ACID-compliant data storage")
print("  • Databricks: AI/ML processing engine")
print("  • Feature Store: Reusable features for ML")
print("  • MLflow: Model tracking and registry")
print("  • AI Agent: Inventory optimization logic with linear programming")
print("  • SAP Analytics Cloud / Power BI: Visualization and reporting")
print("  • Human Oversight: Inventory manager approval workflow")
print("  • Feedback Loop: Continuous learning and improvement")

print("\n" + "="*80)
print("🤖 AI Agent Capabilities:")
print("="*80)
print("  1. SENSE: Monitor inventory, sales, forecasts, external signals")
print("  2. THINK: Predict demand, identify optimal allocation actions")
print("  3. ACT: Generate recommendations (allocate, return, adjust)")
print("  4. LEARN: Adapt to changing conditions via feedback loop")

print("\n" + "="*80)
print("📈 Optimization Objectives:")
print("="*80)
print("  • Maximize D2C channel fill rate and service levels")
print("  • Minimize stockouts and excess inventory costs")
print("  • Optimize allocation across D2C, Prime, and General pools")
print("  • Enable real-time adjustments based on demand signals")
print("  • Continuous improvement through ML model retraining")
print("="*80)
