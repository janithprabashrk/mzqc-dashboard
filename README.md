# mzQC Dashboard

## Overview

The mzQC Dashboard is a Streamlit-based web application designed to visualize mass spectrometry quality control metrics from mzQC files. This tool provides an interactive interface to explore and analyze various quality metrics, metadata, and run summaries from mzQC files.

## Features

- **File Upload**: Upload your mzQC JSON files for visualization.
- **Example File**: Use a built-in example file to explore the dashboard's features.
- **Metadata Display**: View detailed metadata about the mzQC file.
- **Sample Information**: Display information about the sample used in the mzQC file.
- **Quality Metrics**: Visualize various quality metrics using interactive charts and tables.
- **Run Summary**: Get a quick overview of the run summary including total peptides, total proteins, and run duration.
- **Customizable Charts**: Choose from different color schemes for the charts.
- **Summary Statistics**: View summary statistics for numeric metrics.

## Installation

To run the mzQC Dashboard locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/mzqc-dashboard.git
    cd mzqc-dashboard
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Upload an mzQC File**: Use the file uploader in the sidebar to upload your mzQC JSON file.
2. **Explore the Data**: Navigate through the different sections to view metadata, sample information, quality metrics, and run summary.
3. **Customize the Display**: Use the sidebar options to toggle the display of metadata, raw metrics table, and run summary. Choose a color scheme for the charts.

## Example

An example mzQC file (`example_mzQC.json`) is included in the repository. You can use this file to explore the features of the dashboard without needing to upload your own mzQC file.

## Dependencies

- Streamlit
- Pandas
- Plotly
- NumPy
- Statsmodels

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Developed by Janith Prabash R.K.
- Special thanks to the contributors of the libraries used in this project.

## Contact

For any questions or inquiries, please contact Janith Prabash R.K. at janithprabash944ugc@gmail.com

## Live Demo

You can access the live demo of the mzQC Dashboard at the following link:
[https://mzqc-dashboard-by-janith-prabash-3ddebeaawhqfz88w8qgxan.streamlit.app/](https://mzqc-dashboard-by-janith-prabash-3ddebeaawhqfz88w8qgxan.streamlit.app/)

---

<div style="text-align: center">
    <small>mzQC Dashboard - Developed by Janith Prabash R.K.</small>
    <br>
    <small>A visualization tool for mass spectrometry quality control metrics</small>
</div>
