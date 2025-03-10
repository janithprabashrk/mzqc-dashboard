import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

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

            # Handle numeric metrics
            if isinstance(metric_value, (int, float)):
                st.write(f"#### {metric_name}")
                # Use a colorful bar chart
                fig = px.bar(
                    x=[metric_name],
                    y=[metric_value],
                    labels={"x": "Metric", "y": "Value"},
                    color=[metric_name],
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                st.plotly_chart(fig)

            # Handle list-based metrics
            elif isinstance(metric_value, list):
                st.write(f"#### {metric_name}")
                if all(isinstance(item, (int, float)) for item in metric_value):
                    # Use a colorful line chart
                    fig = px.line(
                        y=metric_value,
                        labels={"y": "Value"},
                        color_discrete_sequence=px.colors.qualitative.Vivid
                    )
                    st.plotly_chart(fig)
                elif all(isinstance(item, dict) for item in metric_value):
                    # Use a scatter plot for list of objects
                    df = pd.DataFrame(metric_value)
                    fig = px.scatter(
                        df,
                        x=df.columns[0],
                        y=df.columns[1],
                        color=df.columns[1],
                        color_continuous_scale=px.colors.sequential.Viridis
                    )
                    st.plotly_chart(fig)

            # Handle nested objects
            elif isinstance(metric_value, dict):
                st.write(f"#### {metric_name}")
                df = pd.DataFrame.from_dict(metric_value, orient="index", columns=["Value"])
                # Use a colorful bar chart for nested objects
                fig = px.bar(
                    df,
                    x=df.index,
                    y="Value",
                    labels={"x": "Key", "y": "Value"},
                    color=df.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig)