"""
D2C Inventory Optimization with AI Agents - Architecture Diagram Generator - V2
Generates PNG, DOT, and Draw.io format diagrams

Version 2 Features:
- NUMBERED FLOW SEQUENCES on all directional arrows
- Clear step-by-step data flow visualization
- Enhanced readability with sequential numbering

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
    "D2C Inventory Optimization with AI Agents - v2 (Numbered Flow)",
    filename="diagrams/d2c_inventory_ai_agents_v2",
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
    # DATA FLOW CONNECTIONS WITH NUMBERED SEQUENCES
    # ============================================================================

    # STEP 1: SAP ECC → Data Ingestion (SENSE)
    sap_inventory >> Edge(label="[1a] extract", color="#4285F4", style="bold") >> sap_bdc
    sap_sales >> Edge(label="[1b] extract", color="#4285F4", style="bold") >> sap_bdc
    sap_master >> Edge(label="[1c] extract", color="#4285F4", style="bold") >> sap_bdc

    # STEP 1: External Sources → Data Ingestion (SENSE)
    external_weather >> Edge(label="[1d] API", color="#34A853", style="bold") >> external_apis
    external_social >> Edge(label="[1e] API", color="#34A853", style="bold") >> external_apis
    external_economic >> Edge(label="[1f] API", color="#34A853", style="bold") >> external_apis

    # STEP 2: Data Ingestion → Streaming (INGEST)
    sap_bdc >> Edge(label="[2a] stream", color="#4285F4", style="bold") >> streaming
    external_apis >> Edge(label="[2b] stream", color="#34A853", style="bold") >> streaming

    # STEP 3: Streaming → Delta Lake (STORE)
    streaming >> Edge(label="[3] ingest to\nraw layer", color="#9C27B0", style="bold") >> raw_data
    raw_data >> Edge(label="[4] transform\n& clean", color="#9C27B0", style="bold") >> transformed_data

    # STEP 5: Delta Lake → Feature Engineering (PREPARE)
    transformed_data >> Edge(label="[5] load for\nprocessing", color="#FF9800", style="bold") >> data_cleaning
    data_cleaning >> Edge(label="[6] create\nfeatures", color="#FF9800") >> feature_creation
    feature_creation >> Edge(label="[7] validate\nquality", color="#FF9800") >> data_validation
    data_validation >> Edge(label="[8] store\nfeatures", color="#FF9800", style="bold") >> feature_store

    # STEP 9-12: Feature Store → ML Training (TRAIN)
    feature_store >> Edge(label="[9] load\nfeatures", color="#FF9800", style="bold") >> ml_training
    ml_training >> Edge(label="[10] evaluate\nmodel", color="#FF9800") >> ml_evaluation
    ml_evaluation >> Edge(label="[11] tune\nparameters", color="#FF9800") >> hyperparameter
    hyperparameter >> Edge(label="[12] register\nmodel", color="#FF9800", style="bold") >> ml_registry

    # STEP 13: ML Model → AI Agent (THINK - Deploy)
    ml_registry >> Edge(label="[13] deploy\nmodel", color="#9C27B0", style="bold") >> demand_forecast
    transformed_data >> Edge(label="[14] current\ninventory", color="#4285F4", style="bold") >> allocation_logic

    # STEP 15-17: AI Agent Internal Flow (THINK - Process)
    demand_forecast >> Edge(label="[15] generate\nforecast", color="#9C27B0", style="bold") >> allocation_logic
    allocation_logic >> Edge(label="[16] optimize\nallocation", color="#9C27B0", style="bold") >> optimization
    optimization >> Edge(label="[17] create\nrecommendations", color="#9C27B0", style="bold") >> recommendation_engine

    # STEP 18: AI Agent → Visualization (VISUALIZE)
    recommendation_engine >> Edge(label="[18a] publish\nresults", color="#673AB7", style="bold") >> sac
    recommendation_engine >> Edge(label="[18b] publish\nresults", color="#673AB7", style="bold") >> powerbi
    ml_evaluation >> Edge(label="[18c] publish\nmetrics", color="#673AB7") >> metrics

    # STEP 19: Visualization → Human Oversight (REVIEW)
    sac >> Edge(label="[19a] review\ndashboard", color="#E91E63", style="bold") >> inventory_manager
    powerbi >> Edge(label="[19b] review\ndashboard", color="#E91E63", style="bold") >> inventory_manager
    recommendation_engine >> Edge(label="[19c] review\nrecommendations", color="#E91E63", style="bold") >> inventory_manager

    # STEP 20-21: Human Oversight → SAP ECC (ACT)
    inventory_manager >> Edge(label="[20] approve\nadjustments", color="#4CAF50", style="bold") >> sap_bdc
    sap_bdc >> Edge(label="[21] create\ntransfer orders", color="#4CAF50", style="bold") >> sap_inventory

    # STEP 22: Feedback Loop - SAP ECC → Feedback (LEARN)
    sap_inventory >> Edge(label="[22a] actual\ninventory", color="#F44336", style="bold") >> feedback_data
    sap_sales >> Edge(label="[22b] actual\nsales", color="#F44336", style="bold") >> feedback_data

    # STEP 23-26: Feedback → Learning (IMPROVE)
    feedback_data >> Edge(label="[23] analyze\nperformance", color="#F44336", style="bold") >> ab_testing
    feedback_data >> Edge(label="[24] retrain\nmodel", color="#F44336", style="bold") >> ml_training
    ml_registry >> Edge(label="[25] explain\npredictions", color="#F44336") >> explainability
    explainability >> Edge(label="[26] provide\ninsights", color="#F44336") >> inventory_manager

    # STEP 27: Monitoring Metrics
    ab_testing >> Edge(label="[27] track\nperformance", color="#673AB7") >> metrics

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/d2c_inventory_ai_agents_v2.dot",
        "-o",
        "diagrams/d2c_inventory_ai_agents_v2.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/d2c_inventory_ai_agents_v2.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\n" + "="*80)
print("Generated files (Version 2 - Numbered Flow):")
print("="*80)
print("  - diagrams/d2c_inventory_ai_agents_v2.png")
print("  - diagrams/d2c_inventory_ai_agents_v2.dot")
print("  - diagrams/d2c_inventory_ai_agents_v2.drawio")

print("\n" + "="*80)
print("📊 D2C Inventory Optimization Architecture - NUMBERED FLOW SEQUENCE:")
print("="*80)
print("\n🔵 PHASE 1: SENSE (Data Collection)")
print("  [1a-c] SAP ECC → SAP BDC Connector (inventory, sales, master data)")
print("  [1d-f] External Sources → APIs (weather, social, economic)")
print("\n🟡 PHASE 2: INGEST (Data Streaming)")
print("  [2a-b] SAP BDC + External APIs → Spark Structured Streaming")
print("\n🟢 PHASE 3: STORE (Data Lake)")
print("  [3] Streaming → Delta Lake Raw Layer")
print("  [4] Raw → Transformed Data Layer")
print("\n🟠 PHASE 4: PREPARE (Feature Engineering)")
print("  [5] Transformed Data → Data Cleaning")
print("  [6] Cleaning → Feature Creation")
print("  [7] Features → Quality Validation")
print("  [8] Validated → Feature Store")
print("\n🟠 PHASE 5: TRAIN (ML Model Development)")
print("  [9] Feature Store → ML Training (ARIMA, Prophet, LSTM)")
print("  [10] Training → Model Evaluation (MAE, RMSE)")
print("  [11] Evaluation → Hyperparameter Tuning")
print("  [12] Tuning → MLflow Model Registry")
print("\n🟣 PHASE 6: THINK (AI Agent Processing)")
print("  [13] Model Registry → Deploy to Demand Forecast Engine")
print("  [14] Current Inventory Data → Allocation Logic")
print("  [15] Demand Forecast → Allocation Logic")
print("  [16] Allocation Logic → Optimization Algorithm")
print("  [17] Optimization → Recommendation Engine")
print("\n🟣 PHASE 7: VISUALIZE (Reporting)")
print("  [18a-c] Recommendations → SAP Analytics Cloud / Power BI / Metrics")
print("\n🔴 PHASE 8: ACT (Human Oversight & Execution)")
print("  [19a-c] Dashboards → Inventory Manager (Review)")
print("  [20] Manager → Approve Adjustments")
print("  [21] SAP BDC → Create Transfer Orders in SAP ECC")
print("\n🔴 PHASE 9: LEARN (Feedback Loop)")
print("  [22a-b] Actual Results → Feedback Data")
print("  [23] Feedback → A/B Testing Analysis")
print("  [24] Feedback → Retrain ML Model")
print("  [25] Model → Explainability (SHAP, LIME)")
print("  [26] Explainability → Insights to Manager")
print("  [27] A/B Testing → Performance Metrics")

print("\n" + "="*80)
print("✨ Version 2 Key Features:")
print("="*80)
print("  ✓ 27 numbered flow steps for complete traceability")
print("  ✓ Clear sequential visualization of data flow")
print("  ✓ Color-coded by architecture phase")
print("  ✓ Bold arrows for major data flow paths")
print("  ✓ Sub-steps (a, b, c) for parallel operations")
print("  ✓ Easy to follow end-to-end process")
print("="*80)
