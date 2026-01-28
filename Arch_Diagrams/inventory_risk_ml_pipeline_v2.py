"""
Inventory Risk ML Pipeline Architecture Diagram Generator (V2)
Left-to-Right layout with numbered flow arrows

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

# Graph attributes for clean layout (Left-to-Right)
graph_attr = {
    "splines": "polyline",  # Better for LR with labels
    "nodesep": "0.8",
    "ranksep": "2.0",  # More space for LR layout
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

# Create the diagram (Left-to-Right)
with Diagram(
    "Inventory Risk ML Pipeline Architecture",
    filename="diagrams/inventory_risk_ml_pipeline_v2",
    outformat=["png", "dot"],
    show=False,
    direction="LR",  # Left to Right
    graph_attr=graph_attr
):

    # ============================================
    # LAYER 1: DATA SOURCES (SAP BDC)
    # ============================================
    with Cluster("1. DATA SOURCES", graph_attr=data_sources_cluster_attr):
        with Cluster("SAP BDC (Business Data Cloud)", graph_attr=source_tables_cluster_attr):
            # Primary source tables (grouped for cleaner layout)
            stock_status = MSSQL("stock_status_v2")
            review_dc = MSSQL("review_dc")
            review_plant = MSSQL("review_plant")
            review_vendors = MSSQL("review_vendors")
            location_source = MSSQL("location_source")
            production_source = MSSQL("production_source")
            lag_review_dc = MSSQL("lag_1_review_dc")
            lag_review_plant = MSSQL("lag_1_review_plant")

    # Delta Sharing connector (Source → Databricks)
    delta_sharing_in = DataLakeStorage("Delta Sharing\n(Zero-Copy Read)")

    # ============================================
    # LAYER 2: SAP DATABRICKS (ML PLATFORM)
    # ============================================
    with Cluster("2. SAP DATABRICKS (ML Platform)", graph_attr=databricks_cluster_attr):

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
        batch_job = Spark("BATCH SCORING JOB\n(Daily 3 AM UTC)")

        # Internal connections within Databricks (no numbers - internal flow)
        ml_features >> Edge(style="dotted", color="gray") >> feature_refresh
        ml_features >> Edge(style="dotted", color="gray") >> batch_job
        risk_classifier >> Edge(style="dotted", color="gray") >> batch_job
        early_warning >> Edge(style="dotted", color="gray") >> batch_job
        severity_scorer >> Edge(style="dotted", color="gray") >> batch_job
        rest_api >> Edge(style="dotted", color="gray") >> low_latency

    # Delta Sharing connector (Databricks → Results)
    delta_sharing_out = DataLakeStorage("Delta Sharing\n(Write-Back)")

    # ============================================
    # LAYER 3: SAP BDC (ML RESULTS)
    # ============================================
    with Cluster("3. SAP BDC (ML Results)", graph_attr=ml_results_cluster_attr):
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
    with Cluster("4. CONSUMERS", graph_attr=consumers_cluster_attr):
        sap_btp = AppServices("SAP BTP App\n(Flask API + Agents)")
        sap_sac = Powerbi("SAP Analytics Cloud\n(Dashboards)")
        sap_s4hana = Server("SAP S/4HANA\n(ERP Integration)")

    # ============================================
    # DATA FLOW CONNECTIONS (NUMBERED)
    # ============================================

    # Step 1: Source tables → Delta Sharing (input)
    stock_status >> Edge(label="①", color="#9C27B0", style="bold") >> delta_sharing_in
    review_dc >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    review_plant >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    review_vendors >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    location_source >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    production_source >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    lag_review_dc >> Edge(label="①", color="#9C27B0") >> delta_sharing_in
    lag_review_plant >> Edge(label="①", color="#9C27B0") >> delta_sharing_in

    # Step 2: Delta Sharing → Feature Store
    delta_sharing_in >> Edge(label="② Zero-Copy Read", color="#9C27B0", style="bold") >> ml_features

    # Step 3: Batch Job → Delta Sharing (output)
    batch_job >> Edge(label="③ Daily Predictions", color="#4CAF50", style="bold") >> delta_sharing_out

    # Step 4: Delta Sharing → ML Results
    delta_sharing_out >> Edge(label="④", color="#4CAF50", style="bold") >> risk_class
    delta_sharing_out >> Edge(label="④", color="#4CAF50") >> severity
    delta_sharing_out >> Edge(label="④", color="#4CAF50") >> early_warn
    delta_sharing_out >> Edge(label="④", color="#4CAF50") >> shap_explain

    # Step 5: ML Results → Data Product Subscription
    risk_class >> Edge(label="⑤", color="#E91E63") >> data_product_sub
    severity >> Edge(label="⑤", color="#E91E63") >> data_product_sub
    early_warn >> Edge(label="⑤", color="#E91E63") >> data_product_sub
    shap_explain >> Edge(label="⑤", color="#E91E63") >> data_product_sub

    # Step 6: Data Product Subscription → Consumers
    data_product_sub >> Edge(label="⑥ Subscribe", color="#E91E63", style="bold") >> sap_btp
    data_product_sub >> Edge(label="⑥ Subscribe", color="#E91E63", style="bold") >> sap_sac
    data_product_sub >> Edge(label="⑥ Subscribe", color="#E91E63", style="bold") >> sap_s4hana

    # Step 7: REST API → BTP App (direct API access - optional path)
    rest_api >> Edge(label="⑦ REST API (Optional)", color="#2196F3", style="dashed") >> sap_btp

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/inventory_risk_ml_pipeline_v2.dot",
        "-o",
        "diagrams/inventory_risk_ml_pipeline_v2.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/inventory_risk_ml_pipeline_v2.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\nGenerated files:")
print("  - diagrams/inventory_risk_ml_pipeline_v2.png")
print("  - diagrams/inventory_risk_ml_pipeline_v2.dot")
print("  - diagrams/inventory_risk_ml_pipeline_v2.drawio")
print("\n📊 Numbered Data Flow (Left → Right):")
print("  ① SAP BDC Source Tables → Delta Sharing")
print("  ② Delta Sharing (Zero-Copy Read) → Feature Store")
print("  ③ Batch Scoring Job → Delta Sharing (Write-Back)")
print("  ④ Delta Sharing → ML Predictions Table")
print("  ⑤ ML Predictions → Data Product Subscription")
print("  ⑥ Data Product Subscription → Consumers (BTP, SAC, S/4HANA)")
print("  ⑦ REST API → BTP App (Optional real-time path)")
print("\n🤖 ML Models:")
print("  • Risk Classifier (XGBoost): normal/understock/overstock")
print("  • Early Warning (LSTM): 1-4 week predictions")
print("  • Severity Scorer (LightGBM): 0-100 score")
print("  • SHAP Explainability: Top 3 contributing factors")
