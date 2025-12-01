"""
SAP Business Data Cloud (BDC) to Databricks Architecture Diagram Generator - Version 3
Generates PNG, DOT, and Draw.io format diagrams

Version 3 - Architecturally Accurate Based on SAP Official Documentation:
- Foundation Services is INSIDE SAP BDC (core component)
- BDC Connect as integration layer (implements Delta Sharing protocol)
- SAP Databricks inside BDC with ML & Data Enrichment
- Proper data product flow: Object Stores → BDC Connect → Consumption layers
- Bidirectional Delta Sharing
"""

import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.storage import StorageAccounts, DataLakeStorage
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.integration import APIManagement, ServiceBus
from diagrams.onprem.analytics import Databricks, Spark
from diagrams.onprem.database import MSSQL
from diagrams.onprem.compute import Server

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

# SAP BDC Main Cluster
bdc_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#F3E5F5",  # Light Purple
    "style": "rounded",
    "margin": "30"
}

# Foundation Services - Base layer of BDC (INSIDE BDC)
foundation_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#E1BEE7",  # Light Purple
    "style": "rounded",
    "margin": "15"
}

# SAP Datasphere Layer
datasphere_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#CE93D8",  # Medium Purple
    "style": "rounded",
    "margin": "15"
}

# BDC Connect - Integration Layer
bdc_connect_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#80DEEA",  # Teal/Cyan - connectivity layer
    "style": "rounded",
    "margin": "15"
}

# SAP Analytics Cloud Layer
sac_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#BA68C8",  # Deep Purple
    "style": "rounded",
    "margin": "15"
}

# SAP Databricks Layer (inside BDC)
sap_databricks_cluster_attr = {
    "fontsize": "12",
    "bgcolor": "#FFF3E0",  # Light Orange
    "style": "rounded",
    "margin": "15"
}

# ML Enrichment inside SAP Databricks
ml_cluster_attr = {
    "fontsize": "11",
    "bgcolor": "#FFE0B2",  # Lighter Orange
    "style": "rounded",
    "margin": "10"
}

security_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFEBEE",  # Light Red
    "style": "dashed",
    "margin": "15"
}

# Create the diagram
with Diagram(
    "SAP Business Data Cloud Architecture - v3 (Accurate)",
    filename="diagrams/sap_bdc_databricks_v3",
    outformat=["png", "dot"],
    show=False,
    direction="TB",  # Top to bottom for better layer visualization
    graph_attr=graph_attr
):

    # SAP Source Systems Cluster
    with Cluster("SAP S/4HANA Source Systems", graph_attr=sap_source_cluster_attr):
        sap_qm = Server("QM Module\n(Quality)")
        sap_mm = Server("MM Module\n(Materials)")
        sap_pp = Server("PP Module\n(Production)")
        sap_plm = Server("PLM Module\n(Lifecycle)")
        sap_ariba = Server("SAP Ariba\n(Procurement)")

    # External Data Sources Cluster
    with Cluster("External Data Sources", graph_attr=external_source_cluster_attr):
        ext_fda = APIManagement("FDA APIs")
        ext_ofac = APIManagement("OFAC")
        ext_epa = APIManagement("EPA")
        ext_nih = APIManagement("NIH")
        ext_shelf = APIManagement("Shelf Life")

    # SAP BDC - Complete Architecture
    with Cluster("SAP Business Data Cloud (BDC)", graph_attr=bdc_cluster_attr):

        # Layer 1: Foundation Services (Base Data Layer - INSIDE BDC)
        with Cluster("Foundation Services\n(Object Store / Data Lake)", graph_attr=foundation_cluster_attr):
            bdc_ingestion = APIManagement("Data Ingestion\n& Replication")
            bdc_hana_cloud = DatabaseForPostgresqlServers("HANA Cloud\nData Lake Files")
            bdc_one_domain = StorageAccounts("One Domain Model\n(Unified Context)")
            fos_data_products = DataLakeStorage("SAP Data Products\n(Object Store)")

            # Foundation internal connections
            bdc_ingestion >> Edge(label="replicate", style="dotted") >> bdc_hana_cloud
            bdc_hana_cloud >> Edge(label="store", style="dotted") >> fos_data_products
            bdc_one_domain >> Edge(label="context", style="dotted") >> fos_data_products

        # Layer 2: SAP Datasphere (Semantic & Modeling Layer)
        with Cluster("SAP Datasphere\n(Semantic & Modeling Layer)", graph_attr=datasphere_cluster_attr):
            datasphere_modeling = DatabaseForPostgresqlServers("Data Modeling\n& Relationships")
            datasphere_semantic = StorageAccounts("Semantic Layer\n(Business Context)")
            datasphere_object_store = DataLakeStorage("Custom Data Products\n(Object Store)")
            datasphere_catalog = LogAnalyticsWorkspaces("Data Products\nCatalog")

            # Datasphere internal connections
            fos_data_products >> Edge(label="feeds", style="dotted") >> datasphere_modeling
            datasphere_modeling >> Edge(label="creates", style="dotted") >> datasphere_object_store
            datasphere_semantic >> Edge(label="enriches", style="dotted") >> datasphere_catalog
            datasphere_object_store >> Edge(label="catalogs", style="dotted") >> datasphere_catalog

        # Layer 3: BDC Connect (Integration Layer - Delta Sharing)
        with Cluster("BDC Connect\n(Integration Layer)", graph_attr=bdc_connect_cluster_attr):
            bdc_connect = ServiceBus("Delta Sharing\nProtocol")
            connect_security = Server("Security:\nmTLS, OAuth")

            # BDC Connect connections
            bdc_connect >> Edge(label="secure", style="dotted") >> connect_security

        # Layer 4: Consumption Layers

        # SAP Analytics Cloud
        with Cluster("SAP Analytics Cloud (SAC)", graph_attr=sac_cluster_attr):
            sac_dashboards = LogAnalyticsWorkspaces("Dashboards\n& Reports")
            sac_ai = MachineLearningServiceWorkspaces("AI-Driven\nInsights")
            sac_dashboards >> Edge(label="AI", style="dotted") >> sac_ai

        # SAP Databricks with ML Enrichment
        with Cluster("SAP Databricks\n(ML & Analytics Platform)", graph_attr=sap_databricks_cluster_attr):
            databricks = Databricks("Databricks\nLakehouse")
            unity_catalog = LogAnalyticsWorkspaces("Unity Catalog")
            delta_lake = DataLakeStorage("Delta Lake")
            spark_engine = Spark("Spark Engine")

            # ML & Data Enrichment (inside SAP Databricks)
            with Cluster("ML & Data Enrichment", graph_attr=ml_cluster_attr):
                ml_feature = MachineLearningServiceWorkspaces("Feature Eng.\n& ML Models")
                ml_enriched = DataLakeStorage("Enriched\nDatasets")
                ml_analytics = LogAnalyticsWorkspaces("Custom\nAnalytics")

                ml_feature >> Edge(label="gen", style="dotted") >> ml_enriched
                ml_analytics >> Edge(label="analyze", style="dotted") >> ml_enriched

            # Databricks internal connections
            databricks >> Edge(label="manage", style="dotted") >> unity_catalog
            databricks >> Edge(label="store", style="dotted") >> delta_lake
            databricks >> Edge(label="compute", style="dotted") >> spark_engine
            databricks >> Edge(label="ML", style="dotted") >> ml_feature
            delta_lake >> Edge(label="data", style="dotted") >> ml_feature

        # Legacy Support
        bdc_bw4hana = MSSQL("SAP BW/4HANA\n(Legacy)")
        bdc_bw4hana >> Edge(label="legacy data", style="dashed") >> datasphere_modeling

    # Security & Governance Layer (overlay)
    with Cluster("Security & Governance", graph_attr=security_cluster_attr):
        security_layer = Server("Enterprise Security\nmTLS, OAuth, RBAC")

    # Enriched Data Products (return path)
    enriched_data_products = DataLakeStorage("Enriched Data Products\n(from ML)")

    # ============================================================================
    # DATA FLOW CONNECTIONS
    # ============================================================================

    # SOURCE SYSTEMS → FOUNDATION SERVICES
    sap_qm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_mm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_pp >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_plm >> Edge(label="CDS/RF", color="#4285F4") >> bdc_ingestion
    sap_ariba >> Edge(label="Ariba API", color="#4285F4") >> bdc_ingestion

    ext_fda >> Edge(label="REST", color="#34A853") >> bdc_ingestion
    ext_ofac >> Edge(label="REST", color="#34A853") >> bdc_ingestion
    ext_epa >> Edge(label="REST", color="#34A853") >> bdc_ingestion
    ext_nih >> Edge(label="REST", color="#34A853") >> bdc_ingestion
    ext_shelf >> Edge(label="REST", color="#34A853") >> bdc_ingestion

    # OBJECT STORES → BDC CONNECT (Data Products)
    fos_data_products >> Edge(label="SAP Data Products", color="#9C27B0", style="bold") >> bdc_connect
    datasphere_object_store >> Edge(label="Custom Data Products", color="#9C27B0", style="bold") >> bdc_connect

    # BDC CONNECT → CONSUMPTION LAYERS (Delta Sharing)
    bdc_connect >> Edge(label="Delta Sharing\n(zero-copy)", color="#9C27B0", style="bold") >> databricks
    bdc_connect >> Edge(label="data access", color="#673AB7") >> sac_dashboards

    # DATASPHERE → SAC (Direct connection for analytics)
    datasphere_catalog >> Edge(label="analytics", color="#673AB7", style="dashed") >> sac_dashboards

    # SAP DATABRICKS ML → ENRICHED DATA (Bidirectional flow back)
    ml_enriched >> Edge(label="ML enriched", color="#4CAF50", style="bold") >> enriched_data_products
    enriched_data_products >> Edge(label="share back\n(Delta Sharing)", color="#4CAF50", style="bold") >> bdc_connect

    # BDC CONNECT → DATASPHERE (Enriched data return)
    bdc_connect >> Edge(label="enriched products", color="#4CAF50") >> datasphere_catalog

    # Security overlay
    security_layer >> Edge(label="secures all connections", style="dotted", color="red") >> bdc_connect

print("✓ PNG and DOT files generated in diagrams/")

# Convert DOT to Draw.io format
try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/sap_bdc_databricks_v3.dot",
        "-o",
        "diagrams/sap_bdc_databricks_v3.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/sap_bdc_databricks_v3.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\n" + "="*70)
print("Generated files (Version 3 - Architecturally Accurate):")
print("="*70)
print("  - diagrams/sap_bdc_databricks_v3.png")
print("  - diagrams/sap_bdc_databricks_v3.dot")
print("  - diagrams/sap_bdc_databricks_v3.drawio")

print("\n" + "="*70)
print("📊 SAP BDC Architecture Flow (v3):")
print("="*70)
print("  1. Source Systems → Foundation Services (data ingestion)")
print("  2. Foundation Services → HANA Cloud → SAP Data Products (Object Store)")
print("  3. SAP Data Products → SAP Datasphere (semantic modeling)")
print("  4. Datasphere → Custom Data Products (Object Store) + Catalog")
print("  5. Both Object Stores → BDC Connect (Delta Sharing integration layer)")
print("  6. BDC Connect → SAP Databricks (zero-copy data access)")
print("  7. SAP Databricks → ML & Data Enrichment (feature eng, models)")
print("  8. ML Enriched Data → BDC Connect (share back via Delta Sharing)")
print("  9. BDC Connect → Datasphere Catalog (enriched data products)")
print(" 10. Datasphere Catalog → SAP Analytics Cloud (dashboards, AI insights)")

print("\n" + "="*70)
print("✅ Key Architectural Corrections in v3:")
print("="*70)
print("  ✓ Foundation Services INSIDE SAP BDC (per SAP official docs)")
print("  ✓ BDC Connect as integration layer (not standalone Delta Sharing box)")
print("  ✓ Delta Sharing represented as protocol within BDC Connect")
print("  ✓ Data Products from BOTH Object Stores flow through BDC Connect")
print("  ✓ SAP Databricks inside BDC with ML enrichment")
print("  ✓ Bidirectional Delta Sharing flow properly represented")
print("  ✓ Clear architectural layering matching SAP BDC structure")

print("\n" + "="*70)
print("🏗️ SAP BDC Layers (v3):")
print("="*70)
print("  Layer 1: Foundation Services (Object Store, HANA Cloud, Data Products)")
print("  Layer 2: SAP Datasphere (Modeling, Semantic, Custom Products, Catalog)")
print("  Layer 3: BDC Connect (Delta Sharing integration layer)")
print("  Layer 4: Consumption (SAP Analytics Cloud, SAP Databricks, BW/4HANA)")
print("="*70)
