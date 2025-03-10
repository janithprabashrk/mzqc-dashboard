import streamlit as st
import pandas as pd
import json
import numpy as np
from datetime import datetime
import re

# Try importing Plotly with explicit error handling
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    st.error("Failed to import Plotly. Please make sure it's installed.")
    st.stop()

# Try importing statsmodels, but continue if not available
try:
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    st.warning("Statsmodels is not installed. Some trend line features will be disabled.")

# Set page configuration
st.set_page_config(
    page_title="mzQC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-header {
        color: #0D47A1;
        padding-top: 1rem;
    }
    .stExpander {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title of the app
st.markdown('<h1 class="main-header">mzQC File Visualizer</h1>', unsafe_allow_html=True)

# Sidebar for configuration and filtering
with st.sidebar:
    st.header("Configuration")
    
    # Example files option
    use_example = st.checkbox("Use Example File", value=False)
    
    # Color scheme
    color_scheme = st.selectbox(
        "Chart Color Scheme",
        options=["Plotly", "Viridis", "Plasma", "Blues", "Greens", "Reds"],
        index=0
    )
    
    # Display options
    st.subheader("Display Options")
    show_metadata = st.checkbox("Show Metadata", value=True)
    show_raw_metrics = st.checkbox("Show Raw Metrics Table", value=True)
    show_summary = st.checkbox("Show Run Summary", value=True)
    
    st.sidebar.info("Upload an mzQC file or use the example to visualize mass spectrometry quality control metrics.")

# Function to get color scheme
def get_color_scheme(scheme_name):
    schemes = {
        "Plotly": px.colors.qualitative.Plotly,
        "Viridis": px.colors.sequential.Viridis,
        "Plasma": px.colors.sequential.Plasma,
        "Blues": px.colors.sequential.Blues,
        "Greens": px.colors.sequential.Greens,
        "Reds": px.colors.sequential.Reds
    }
    return schemes.get(scheme_name, px.colors.qualitative.Plotly)

# Function to format dates
def format_date(date_str):
    try:
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
    except:
        return date_str

# Function to get category color
def get_category_color(category):
    colors = {
        "signal": "#2196F3",  # Blue
        "chromatography": "#4CAF50",  # Green
        "acquisition": "#FFC107",  # Amber
        "mass": "#9C27B0",  # Purple
        "identification": "#F44336",  # Red
        "sample preparation": "#FF9800"  # Orange
    }
    return colors.get(category.lower(), "#607D8B")  # Default gray

# Load example file if selected
if use_example:
    with open('example_mzQC.json', 'r') as f:
        mzqc_data = json.load(f)
    st.success("Example file loaded!")
else:
    # Upload mzQC file
    uploaded_file = st.file_uploader("Upload an mzQC file (JSON format):", type=["json"])
    
    if uploaded_file:
        try:
            # Load and parse the mzQC file
            mzqc_data = json.load(uploaded_file)
            st.success("File uploaded successfully!")
        except json.JSONDecodeError:
            st.error("Error: Invalid JSON file. Please upload a valid mzQC file.")
            st.stop()
    else:
        st.info("Please upload an mzQC file to continue.")
        st.stop()

# Process and display the data
if 'mzqc_data' in locals():
    
    # Display run summary at the top for quick overview
    if "runSummary" in mzqc_data and show_summary:
        run_summary = mzqc_data["runSummary"]
        
        # Create three columns for summary stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if "totalPeptides" in run_summary:
                st.metric("Total Peptides", f"{run_summary['totalPeptides']:,}")
            if "successfulRun" in run_summary:
                status = "✅ Success" if run_summary["successfulRun"] else "❌ Failed"
                st.metric("Run Status", status)
                
        with col2:
            if "totalProteins" in run_summary:
                st.metric("Total Proteins", f"{run_summary['totalProteins']:,}")
            if "statusMessage" in run_summary:
                st.info(f"Status: {run_summary['statusMessage']}")
                
        with col3:
            if "startTime" in run_summary and "endTime" in run_summary:
                start = datetime.fromisoformat(run_summary["startTime"].replace('Z', '+00:00'))
                end = datetime.fromisoformat(run_summary["endTime"].replace('Z', '+00:00'))
                duration = end - start
                minutes = duration.total_seconds() / 60
                st.metric("Run Duration", f"{minutes:.1f} minutes")
    
    # Display metadata in an expandable section
    if "metadata" in mzqc_data and show_metadata:
        with st.expander("Metadata", expanded=show_metadata):
            metadata = mzqc_data["metadata"]
            
            # Format metadata in a more readable way
            cols = st.columns(2)
            with cols[0]:
                if "creationDate" in metadata:
                    st.info(f"**Creation Date:** {format_date(metadata['creationDate'])}")
                if "version" in metadata:
                    st.info(f"**Version:** {metadata['version']}")
                if "description" in metadata:
                    st.info(f"**Description:** {metadata['description']}")
                
            with cols[1]:
                if "instrumentModel" in metadata:
                    st.info(f"**Instrument:** {metadata['instrumentModel']}")
                if "softwareVersion" in metadata:
                    st.info(f"**Software:** {metadata['softwareVersion']}")
                if "contactName" in metadata:
                    contact = f"{metadata.get('contactName', '')} ({metadata.get('contactOrganization', '')})"
                    st.info(f"**Contact:** {contact}")
    
    # Display sample info if available
    if "sampleInfo" in mzqc_data:
        with st.expander("Sample Information", expanded=show_metadata):
            sample_info = mzqc_data["sampleInfo"]
            
            # Format sample info in columns
            cols = st.columns(2)
            with cols[0]:
                if "sampleId" in sample_info:
                    st.info(f"**Sample ID:** {sample_info['sampleId']}")
                if "organism" in sample_info:
                    st.info(f"**Organism:** {sample_info['organism']}")
                
            with cols[1]:
                if "cellLine" in sample_info:
                    st.info(f"**Cell Line:** {sample_info['cellLine']}")
                if "collectionDate" in sample_info:
                    st.info(f"**Collection Date:** {format_date(sample_info['collectionDate'])}")
    
    # Extract and display quality metrics
    if "qualityMetrics" in mzqc_data:
        metrics = mzqc_data["qualityMetrics"]
        
        # Create a table view of metrics with improved formatting
        if show_raw_metrics:
            with st.expander("Raw Quality Metrics Table", expanded=False):
                # Convert metrics to a more displayable format
                display_metrics = []
                for metric in metrics:
                    display_metric = {
                        "Name": metric["name"],
                        "Description": metric["description"],
                        "Category": metric.get("category", ""),
                        "Unit": metric.get("unit", "")
                    }
                    
                    # Format value based on type
                    value = metric["value"]
                    if isinstance(value, (int, float)):
                        display_metric["Value"] = f"{value:,}"
                    elif isinstance(value, list):
                        if len(value) <= 3:
                            display_metric["Value"] = str(value)
                        else:
                            display_metric["Value"] = f"[{len(value)} items]"
                    elif isinstance(value, dict):
                        display_metric["Value"] = f"{{{len(value)} key-value pairs}}"
                    else:
                        display_metric["Value"] = str(value)
                        
                    display_metrics.append(display_metric)
                    
                metrics_df = pd.DataFrame(display_metrics)
                st.dataframe(metrics_df, use_container_width=True)
        
        # Group metrics by category
        categories = {}
        for metric in metrics:
            category = metric.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(metric)
        
        # Display visualizations by category
        st.markdown("## Metric Visualizations")
        
        # Create tabs for each category
        if categories:
            tabs = st.tabs(list(categories.keys()))
            
            for i, (category, category_metrics) in enumerate(categories.items()):
                with tabs[i]:
                    for metric in category_metrics:
                        metric_name = metric["name"]
                        metric_value = metric["value"]
                        metric_unit = metric.get("unit", "")
                        metric_description = metric.get("description", "")
                        
                        st.markdown(f"<h4 class='metric-header'>{metric_name}</h4>", unsafe_allow_html=True)
                        st.markdown(f"*{metric_description}*")
                        
                        # Handle different metric value types
                        if isinstance(metric_value, (int, float)):
                            # Use a gauge chart for single values
                            max_val = abs(metric_value) * 2 if metric_value != 0 else 100
                            
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=metric_value,
                                domain={"x": [0, 1], "y": [0, 1]},
                                title={"text": f"{metric_unit}"},
                                gauge={
                                    "axis": {"range": [0, max_val]},
                                    "bar": {"color": get_category_color(category)},
                                    "steps": [
                                        {"range": [0, max_val/2], "color": "lightgray"},
                                        {"range": [max_val/2, max_val], "color": "gray"}
                                    ]
                                }
                            ))
                            fig.update_layout(height=300)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Handle list-based metrics
                        elif isinstance(metric_value, list):
                            if all(isinstance(item, (int, float)) for item in metric_value):
                                # Create a more detailed line/bar chart
                                df = pd.DataFrame({
                                    "Index": range(len(metric_value)),
                                    "Value": metric_value
                                })
                                
                                # Use a bar chart if fewer than 10 items, otherwise line chart
                                if len(metric_value) < 10:
                                    fig = px.bar(
                                        df, 
                                        x="Index", 
                                        y="Value",
                                        labels={"Value": metric_unit},
                                        title=f"{len(metric_value)} data points",
                                        color_discrete_sequence=[get_category_color(category)]
                                    )
                                else:
                                    fig = px.line(
                                        df, 
                                        x="Index", 
                                        y="Value",
                                        labels={"Value": metric_unit},
                                        title=f"{len(metric_value)} data points",
                                        markers=True,
                                        color_discrete_sequence=[get_category_color(category)]
                                    )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif all(isinstance(item, dict) for item in metric_value):
                                # Enhanced scatter plot for list of objects
                                df = pd.DataFrame(metric_value)
                                
                                if len(df.columns) >= 2:
                                    x_col = df.columns[0]
                                    y_col = df.columns[1]
                                    
                                    fig = px.scatter(
                                        df,
                                        x=x_col,
                                        y=y_col,
                                        labels={x_col: f"{x_col} ({metric_unit})", y_col: f"{y_col} ({metric_unit})"},
                                        color_discrete_sequence=[get_category_color(category)],
                                        trendline="ols" if (len(df) > 2 and HAS_STATSMODELS) else None,
                                    )
                                    fig.update_traces(marker=dict(size=10))
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    if len(df) > 0:
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric(f"Mean {y_col}", f"{df[y_col].mean():.3f} {metric_unit}")
                                        with col2:
                                            st.metric(f"Max {y_col}", f"{df[y_col].max():.3f} {metric_unit}")
                        
                        # Handle nested objects (dictionaries)
                        elif isinstance(metric_value, dict):
                            df = pd.DataFrame.from_dict(metric_value, orient="index", columns=["Value"])
                            df.index.name = "Key"
                            df.reset_index(inplace=True)
                            
                            # Use a horizontal bar chart for better readability with many items
                            if len(df) > 5:
                                # Sort by value for better visualization
                                df = df.sort_values("Value", ascending=True)
                                
                                fig = px.bar(
                                    df,
                                    y="Key",
                                    x="Value",
                                    orientation='h',
                                    labels={"Value": f"Value ({metric_unit})", "Key": ""},
                                    color="Value",
                                    color_continuous_scale=get_color_scheme(color_scheme),
                                    height=max(300, len(df) * 25)  # Dynamic height based on items
                                )
                            else:
                                fig = px.bar(
                                    df,
                                    x="Key",
                                    y="Value",
                                    labels={"Value": f"Value ({metric_unit})", "Key": ""},
                                    color="Key",
                                    color_discrete_sequence=get_color_scheme(color_scheme)
                                )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Add table view for the data
                            with st.expander("View data table"):
                                st.dataframe(df, use_container_width=True)
                                
                                # Show summary statistics
                                if df["Value"].dtype in [np.float64, np.int64]:
                                    st.write("Summary statistics:")
                                    st.write(df["Value"].describe())
                        
                        st.markdown("---")
else:
    st.warning("No data available. Please upload an mzQC file.")

# Add footer
st.markdown("""
---
<div style="text-align: center">
    <small>mzQC Dashboard - Developed by Janith Prabash R.K.</small>
    <br>
    <small>A visualization tool for mass spectrometry quality control metrics</small>
</div>
""", unsafe_allow_html=True)