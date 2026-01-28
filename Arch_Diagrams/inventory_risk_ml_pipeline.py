"""
Inventory Risk ML Pipeline Architecture Diagram Generator
Generates PNG, DOT, and Draw.io format diagrams

Architecture Flow:
SAP BDC (Data Sources) → Delta Sharing → Databricks ML Platform →
Delta Sharing (Write-Back) → SAP BDC (ML Results) → Consumers
"""

import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.compute import FunctionApps
from diagrams.azure.web import AppServices
from diagrams.onprem.analytics import Databricks, Spark, Powerbi
from diagrams.onprem.database import MSSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users

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
data_sources_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#FFF9C4",  # Light Yellow
    "style": "rounded",
    "margin": "25"
}

source_tables_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#FFF59D",  # Darker Yellow
    "style": "rounded",
    "margin": "15"
}

databricks_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#FFF3E0",  # Light Orange
    "style": "rounded",
    "margin": "25"
}

feature_store_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#E8F5E9",  # Light Green
    "style": "rounded",
    "margin": "15"
}

model_registry_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#E3F2FD",  # Light Blue
    "style": "rounded",
    "margin": "15"
}

model_serving_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#F3E5F5",  # Light Purple
    "style": "rounded",
    "margin": "15"
}

ml_results_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#E8F5E9",  # Light Green
    "style": "rounded",
    "margin": "25"
}

consumers_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#E3F2FD",  # Light Blue
    "style": "rounded",
    "margin": "25"
}

# Create the diagram
with Diagram(
    "Inventory Risk ML Pipeline Architecture",
    filename="diagrams/inventory_risk_ml_pipeline",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr
):

    # ============================================
    # LAYER 1: DATA SOURCES (SAP BDC)
    # ============================================
    with Cluster("DATA SOURCES", graph_attr=data_sources_cluster_attr):
        with Cluster("SAP BDC (Business Data Cloud)", graph_attr=source_tables_cluster_attr):
            # Primary source tables
            stock_status = MSSQL("stock_status_v2")
            review_dc = MSSQL("review_dc")
            review_plant = MSSQL("review_plant")
            review_vendors = MSSQL("review_vendors")

            # Location and production sources
            location_source = MSSQL("location_source")
            production_source = MSSQL("production_source")

            # Lag tables
            lag_review_dc = MSSQL("lag_1_review_dc")
            lag_review_plant = MSSQL("lag_1_review_plant")

    # Delta Sharing connector (Source → Databricks)
    delta_sharing_in = DataLakeStorage("Delta Sharing\n(Zero-Copy Read)")

    # ============================================
    # LAYER 2: SAP DATABRICKS (ML PLATFORM)
    # ============================================
    with Cluster("SAP DATABRICKS (ML Platform)", graph_attr=databricks_cluster_attr):

        # Feature Store
        with Cluster("FEATURE STORE", graph_attr=feature_store_cluster_attr):
            ml_features = DataLakeStorage("ml_features\n(Delta Table)")
            feature_refresh = Server("Daily Refresh\n(22 Features)")

        # Model Registry
        with Cluster("MODEL REGISTRY", graph_attr=model_registry_cluster_attr):
            risk_classifier = MachineLearningServiceWorkspaces("Risk Classifier\n(XGBoost)")
            early_warning = MachineLearningServiceWorkspaces("Early Warning\n(LSTM)")
            severity_scorer = MachineLearningServiceWorkspaces("Severity Scorer\n(LightGBM)")

        # Model Serving
        with Cluster("MODEL SERVING", graph_attr=model_serving_cluster_attr):
            rest_api = FunctionApps("REST API\n(/invocations)")
            low_latency = Server("Low Latency\n(<500ms)")

        # Batch Scoring Job
        batch_job = Spark("BATCH SCORING JOB\nFeatures → Models → Predictions\n(Daily at 3 AM UTC)")

        # Internal connections within Databricks
        ml_features >> Edge(style="dotted") >> feature_refresh
        ml_features >> Edge(label="input", style="dotted") >> batch_job
        risk_classifier >> Edge(label="score", style="dotted") >> batch_job
        early_warning >> Edge(label="score", style="dotted") >> batch_job
        severity_scorer >> Edge(label="score", style="dotted") >> batch_job
        rest_api >> Edge(style="dotted") >> low_latency

    # Delta Sharing connector (Databricks → Results)
    delta_sharing_out = DataLakeStorage("Delta Sharing\n(Write-Back)")

    # ============================================
    # LAYER 3: SAP BDC (ML RESULTS)
    # ============================================
    with Cluster("SAP BDC (ML Results)", graph_attr=ml_results_cluster_attr):
        with Cluster("ml_predictions (Data Product)", graph_attr=source_tables_cluster_attr):
            risk_class = DatabaseForPostgresqlServers("Risk Classification\n(normal/understock/\noverstock)")
            severity = DatabaseForPostgresqlServers("Severity Score\n(0-100)")
            early_warn = DatabaseForPostgresqlServers("Early Warning\n(weeks ahead)")
            shap_explain = DatabaseForPostgresqlServers("SHAP Explainability\n(top 3 factors)")

    # Data Product Subscription connector
    data_product_sub = LogAnalyticsWorkspaces("Data Product\nSubscription")

    # ============================================
    # LAYER 4: CONSUMERS
    # ============================================
    with Cluster("CONSUMERS", graph_attr=consumers_cluster_attr):
        sap_btp = AppServices("SAP BTP App\n(Flask API + Agents)")
        sap_sac = Powerbi("SAP Analytics Cloud\n(Dashboards)")
        sap_s4hana = Server("SAP S/4HANA\n(ERP Integration)")

    # ============================================
    # DATA FLOW CONNECTIONS
    # ============================================

    # Source tables → Delta Sharing (input)
    stock_status >> Edge(color="#9C27B0", style="bold") >> delta_sharing_in
    review_dc >> Edge(color="#9C27B0") >> delta_sharing_in
    review_plant >> Edge(color="#9C27B0") >> delta_sharing_in
    review_vendors >> Edge(color="#9C27B0") >> delta_sharing_in
    location_source >> Edge(color="#9C27B0") >> delta_sharing_in
    production_source >> Edge(color="#9C27B0") >> delta_sharing_in
    lag_review_dc >> Edge(color="#9C27B0") >> delta_sharing_in
    lag_review_plant >> Edge(color="#9C27B0") >> delta_sharing_in

    # Delta Sharing → Feature Store
    delta_sharing_in >> Edge(label="Zero-Copy\nRead", color="#9C27B0", style="bold") >> ml_features

    # Batch Job → Delta Sharing (output)
    batch_job >> Edge(label="Daily\nPredictions", color="#4CAF50", style="bold") >> delta_sharing_out

    # Delta Sharing → ML Results
    delta_sharing_out >> Edge(label="Write-Back", color="#4CAF50", style="bold") >> risk_class
    delta_sharing_out >> Edge(color="#4CAF50") >> severity
    delta_sharing_out >> Edge(color="#4CAF50") >> early_warn
    delta_sharing_out >> Edge(color="#4CAF50") >> shap_explain

    # ML Results → Data Product Subscription
    risk_class >> Edge(color="#E91E63") >> data_product_sub
    severity >> Edge(color="#E91E63") >> data_product_sub
    early_warn >> Edge(color="#E91E63") >> data_product_sub
    shap_explain >> Edge(color="#E91E63") >> data_product_sub

    # Data Product Subscription → Consumers
    data_product_sub >> Edge(label="Subscribe", color="#E91E63", style="bold") >> sap_btp
    data_product_sub >> Edge(label="Subscribe", color="#E91E63", style="bold") >> sap_sac
    data_product_sub >> Edge(label="Subscribe", color="#E91E63", style="bold") >> sap_s4hana

    # REST API → Consumers (direct API access)
    rest_api >> Edge(label="REST API", color="#2196F3", style="dashed") >> sap_btp

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/inventory_risk_ml_pipeline.dot",
        "-o",
        "diagrams/inventory_risk_ml_pipeline.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/inventory_risk_ml_pipeline.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\nGenerated files:")
print("  - diagrams/inventory_risk_ml_pipeline.png")
print("  - diagrams/inventory_risk_ml_pipeline.dot")
print("  - diagrams/inventory_risk_ml_pipeline.drawio")
print("\n📊 Architecture Flow:")
print("  1. DATA SOURCES: SAP BDC tables (stock_status, review_dc, etc.)")
print("  2. Delta Sharing (Zero-Copy Read) → Databricks")
print("  3. DATABRICKS ML: Feature Store → Model Registry → Batch Scoring")
print("  4. Delta Sharing (Write-Back) → SAP BDC ML Results")
print("  5. CONSUMERS: BTP App, Analytics Cloud, S/4HANA via Data Product Subscription")
print("\n🤖 ML Models:")
print("  • Risk Classifier (XGBoost): normal/understock/overstock")
print("  • Early Warning (LSTM): 1-4 week predictions")
print("  • Severity Scorer (LightGBM): 0-100 score")
print("  • SHAP Explainability: Top 3 contributing factors")
