import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Title of the app
st.title("mzQC File Visualizer")

# Upload mzQC file
uploaded_file = st.file_uploader("Upload an mzQC file (JSON format):", type=["json"])

if uploaded_file:
    # Load and parse the mzQC file
    mzqc_data = json.load(uploaded_file)
    st.write("### File uploaded successfully!")

    # Display metadata
    if "metadata" in mzqc_data:
        st.write("### Metadata")
        st.json(mzqc_data["metadata"])

    # Extract quality metrics
    if "qualityMetrics" in mzqc_data:
        st.write("### Quality Metrics")
        metrics = mzqc_data["qualityMetrics"]
        metrics_df = pd.DataFrame(metrics)
        st.write(metrics_df)

        # Visualize metrics
        st.write("### Visualizations")
        for metric in metrics:
            metric_name = metric["name"]
            metric_value = metric["value"]

            # Choose plot type based on metric properties
            if isinstance(metric_value, (int, float)):
                # Create a bar plot for numeric metrics
                fig = px.bar(x=[metric_name], y=[metric_value], labels={"x": "Metric", "y": "Value"})
                st.plotly_chart(fig)
            elif isinstance(metric_value, list):
                # Create a line plot for list-based metrics
                fig = px.line(y=metric_value, labels={"y": "Value"})
                st.plotly_chart(fig)