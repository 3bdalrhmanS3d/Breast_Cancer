# Project Overview

This project provides a comprehensive tool for analyzing, processing, and visualizing datasets using a user-friendly Streamlit web application. The tool supports a wide range of features, including uploading datasets, inspecting data, visualizing distributions, and identifying relationships between variables.

## Features
- Upload datasets in CSV format.
- View raw data and basic dataset information (number of rows, columns, and column details).
- Visualize density plots for numeric columns.
- Generate correlation heatmaps for numeric data.
- Create various types of plots, including histograms, boxplots, density plots, and count plots.
- Handle categorical and numeric columns separately with proper error management.
- Display frequency tables and unique values for categorical columns.
- **Preview analyzed data**: Display processed and analyzed datasets after applying transformations or visualizations.

## Requirements
- Python 3.x
- Libraries:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - streamlit

## Usage
1. Install the required libraries using pip:
   ```bash
   pip install pandas numpy matplotlib seaborn streamlit
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run App.py
   ```
3. Upload a dataset in CSV format and explore the analysis and visualizations.

## Files
- `streamlit_script.py`: The main script for data analysis and visualization.
- `requirements.txt`: Contains a list of dependencies for the project.

## Example Outputs
1. **Raw Dataset View**: View the uploaded dataset in a table format.
2. **Basic Information**:
   - Number of rows and columns.
   - Data types and null counts for each column.
3. **Visualizations**:
   - Histograms and density plots for numeric columns.
   - Count plots and frequency tables for categorical columns.
   - Correlation heatmaps showing relationships between numeric variables.
4. **Analyzed Data Preview**:
   - Display the data after transformations, such as handling missing values, encoding categorical variables, or creating new features.

## Future Enhancements
- Add support for additional file formats (e.g., Excel, JSON).
- Implement advanced preprocessing features like handling missing values and outlier detection.
- Include machine learning visualizations (e.g., feature importance, decision boundaries).

This project serves as a flexible and interactive tool for exploratory data analysis (EDA) and dataset inspection.
