"""
SAP Business Data Cloud (BDC) to Databricks Architecture Diagram Generator
Generates PNG, DOT, and Draw.io format diagrams

Architecture Flow:
SAP Source Systems → SAP BDC/Datasphere → Delta Sharing → Databricks (ML) → Back to BDC
"""

import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.storage import StorageAccounts, DataLakeStorage
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.integration import APIManagement
from diagrams.onprem.analytics import Databricks, Spark
from diagrams.onprem.database import MSSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.custom import Custom

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

# Cluster attributes for different tiers
sap_source_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E3F2FD",  # Light Blue
    "style": "rounded",
    "margin": "20"
}

external_source_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF9C4",  # Light Yellow
    "style": "rounded",
    "margin": "20"
}

bdc_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#F3E5F5",  # Light Purple
    "style": "rounded",
    "margin": "25"
}

bdc_foundation_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#E1BEE7",  # Darker Purple
    "style": "rounded",
    "margin": "15"
}

bdc_datasphere_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#CE93D8",  # Medium Purple
    "style": "rounded",
    "margin": "15"
}

bdc_analytics_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#BA68C8",  # Deep Purple
    "style": "rounded",
    "margin": "15"
}

databricks_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF3E0",  # Light Orange
    "style": "rounded",
    "margin": "20"
}

ml_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E8F5E9",  # Light Green
    "style": "rounded",
    "margin": "20"
}

security_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFEBEE",  # Light Red
    "style": "dashed",
    "margin": "15"
}

# Create the diagram
with Diagram(
    "SAP Business Data Cloud to Databricks Architecture",
    filename="diagrams/sap_bdc_databricks",
    outformat=["png", "dot"],
    show=False,
    direction="LR",
    graph_attr=graph_attr
):

    # SAP Source Systems Cluster
    with Cluster("SAP S/4HANA Source Systems", graph_attr=sap_source_cluster_attr):
        sap_qm = Server("QM Module\n(Quality Management)")
        sap_mm = Server("MM Module\n(Materials Management)")
        sap_pp = Server("PP Module\n(Production Planning)")
        sap_plm = Server("PLM Module\n(Product Lifecycle)")
        sap_ariba = Server("SAP Ariba\n(Procurement)")

    # External Data Sources Cluster
    with Cluster("External Data Sources", graph_attr=external_source_cluster_attr):
        ext_fda = APIManagement("FDA APIs\n(Regulatory Data)")
        ext_ofac = APIManagement("OFAC\n(Sanctions List)")
        ext_epa = APIManagement("EPA\n(Environmental)")
        ext_nih = APIManagement("NIH\n(Clinical Trials)")
        ext_shelf = APIManagement("Shelf Life Data\n(Raw Materials)")

    # SAP BDC - Complete Architecture
    with Cluster("SAP Business Data Cloud (BDC)", graph_attr=bdc_cluster_attr):

        # BDC Foundation Services Layer
        with Cluster("BDC Foundation Services\n(Data Lifecycle Management)", graph_attr=bdc_foundation_cluster_attr):
            bdc_ingestion = APIManagement("Data Ingestion\n& Replication")
            bdc_hana_cloud = DatabaseForPostgresqlServers("HANA Cloud\n(Storage)")
            bdc_one_domain = StorageAccounts("One Domain Model\n(Unified Context)")

        # SAP Datasphere Layer (Core Integration & Modeling)
        with Cluster("SAP Datasphere\n(Integration & Semantic Layer)", graph_attr=bdc_datasphere_cluster_attr):
            datasphere_modeling = DatabaseForPostgresqlServers("Data Modeling\n& Relationships")
            datasphere_semantic = StorageAccounts("Semantic Layer\n(Business Context)")
            datasphere_catalog = LogAnalyticsWorkspaces("Data Products\nCatalog")

        # SAP Analytics Cloud Layer
        with Cluster("SAP Analytics Cloud (SAC)\n(Visualization & AI)", graph_attr=bdc_analytics_cluster_attr):
            sac_dashboards = LogAnalyticsWorkspaces("Dashboards\n& Reports")
            sac_ai = MachineLearningServiceWorkspaces("AI-Driven\nInsights")

        # Legacy Support
        bdc_bw4hana = MSSQL("SAP BW/4HANA\n(Legacy Warehouse)")

        # BDC Internal connections
        bdc_ingestion >> Edge(label="replicate", style="dotted") >> bdc_hana_cloud
        bdc_hana_cloud >> Edge(label="feeds", style="dotted") >> datasphere_modeling
        bdc_one_domain >> Edge(label="provides context", style="dotted") >> datasphere_semantic
        datasphere_modeling >> Edge(label="creates", style="dotted") >> datasphere_catalog
        datasphere_semantic >> Edge(label="enriches", style="dotted") >> datasphere_catalog
        datasphere_catalog >> Edge(label="powers", style="dotted") >> sac_dashboards
        sac_dashboards >> Edge(label="AI insights", style="dotted") >> sac_ai
        bdc_bw4hana >> Edge(label="legacy data", style="dashed") >> datasphere_modeling

    # Delta Sharing Connector (as a visual bridge)
    delta_sharing = DataLakeStorage("SAP BDC Connector\nfor Databricks\n(Delta Sharing)")

    # Databricks Workspace Cluster
    with Cluster("Databricks Workspace", graph_attr=databricks_cluster_attr):
        databricks = Databricks("Databricks\nLakehouse Platform")
        unity_catalog = LogAnalyticsWorkspaces("Unity Catalog\n(Governance)")
        delta_lake = DataLakeStorage("Delta Lake\n(Storage)")
        spark_engine = Spark("Spark\n(Compute)")

        # Databricks internal connections
        databricks >> Edge(label="manages", style="dotted") >> unity_catalog
        databricks >> Edge(label="stores", style="dotted") >> delta_lake
        databricks >> Edge(label="executes", style="dotted") >> spark_engine

    # ML Enrichment Layer
    with Cluster("ML & Data Enrichment", graph_attr=ml_cluster_attr):
        ml_feature = MachineLearningServiceWorkspaces("Feature Engineering\n& ML Models")
        ml_enriched = DataLakeStorage("Enriched Datasets\n(ML Outputs)")
        ml_analytics = LogAnalyticsWorkspaces("Custom Analytics\n& Insights")

        # ML internal connections
        ml_feature >> Edge(label="generates") >> ml_enriched
        ml_analytics >> Edge(label="analyzes") >> ml_enriched

    # Security & Governance Layer (overlay)
    with Cluster("Security & Governance", graph_attr=security_cluster_attr):
        security_mtls = Server("mTLS\nEncryption")
        security_oauth = Server("OAuth/OpenID\nAuthentication")

    # BDC Enriched Data Product (return path)
    bdc_enriched = DatabaseForPostgresqlServers("BDC Enriched\nData Products\n(for SAP Consumers)")

    # Main Data Flow: SAP Sources → BDC Foundation Services
    sap_qm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_mm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_pp >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_plm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_ariba >> Edge(label="Ariba API", color="#4285F4") >> bdc_ingestion

    # External Sources → BDC Foundation Services
    ext_fda >> Edge(label="REST API", color="#34A853") >> bdc_ingestion
    ext_ofac >> Edge(label="REST API", color="#34A853") >> bdc_ingestion
    ext_epa >> Edge(label="REST API", color="#34A853") >> bdc_ingestion
    ext_nih >> Edge(label="REST API", color="#34A853") >> bdc_ingestion
    ext_shelf >> Edge(label="REST API", color="#34A853") >> bdc_ingestion

    # Datasphere Catalog → Delta Sharing Connector
    datasphere_catalog >> Edge(label="SAP Data Products\n(zero-copy, live share)", color="#9C27B0", style="bold") >> delta_sharing

    # Delta Sharing → Databricks
    delta_sharing >> Edge(label="Delta Sharing Protocol\n(governed, semantic metadata)", color="#9C27B0", style="bold") >> databricks

    # Databricks → ML Enrichment
    databricks >> Edge(label="data engineering\n& blending", color="#FF9800") >> ml_feature
    delta_lake >> Edge(label="raw data", color="#FF9800") >> ml_feature

    # ML Enrichment → Back to Delta Sharing
    ml_enriched >> Edge(label="ML-enriched datasets\n(Delta Sharing back)", color="#4CAF50", style="bold") >> delta_sharing

    # Delta Sharing → BDC Enriched Data Products
    delta_sharing >> Edge(label="publish enriched data\n(semantic metadata preserved)", color="#4CAF50", style="bold") >> bdc_enriched

    # BDC Enriched → SAP Analytics Cloud and operational workflows
    bdc_enriched >> Edge(label="enriched data", color="#E91E63") >> datasphere_catalog
    datasphere_catalog >> Edge(label="for analytics", color="#E91E63", style="dashed") >> sac_dashboards

    # Security overlay connections (showing security is applied)
    security_mtls >> Edge(label="secures", style="dotted", color="red") >> delta_sharing
    security_oauth >> Edge(label="authenticates", style="dotted", color="red") >> delta_sharing

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/sap_bdc_databricks.dot",
        "-o",
        "diagrams/sap_bdc_databricks.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/sap_bdc_databricks.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\nGenerated files:")
print("  - diagrams/sap_bdc_databricks.png")
print("  - diagrams/sap_bdc_databricks.dot")
print("  - diagrams/sap_bdc_databricks.drawio")
print("\n📊 Architecture Flow:")
print("  1. SAP S/4HANA (QM, MM, PP, PLM) + External APIs → BDC Foundation Services")
print("  2. BDC Foundation (HANA Cloud) → SAP Datasphere (Semantic Layer)")
print("  3. SAP Datasphere → Data Products Catalog")
print("  4. Data Products Catalog → Delta Sharing → Databricks (zero-copy, governed)")
print("  5. Databricks → ML Enrichment (feature engineering, models)")
print("  6. ML Enriched Data → Delta Sharing → Back to SAP BDC")
print("  7. BDC Enriched Data Products → SAP Analytics Cloud (Dashboards & AI)")
print("\n🏗️ SAP BDC Architecture Layers:")
print("  • BDC Foundation Services: Data Ingestion, HANA Cloud, One Domain Model")
print("  • SAP Datasphere: Data Modeling, Semantic Layer, Data Products Catalog")
print("  • SAP Analytics Cloud: Dashboards, Reports, AI-Driven Insights")
print("  • SAP BW/4HANA: Legacy Warehouse Support")
