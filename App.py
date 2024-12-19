import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Web App
st.title("Dataset Analysis, Preprocessing, and Visualization")

# File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    # Load Dataset
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Dataset:")
    st.dataframe(df)
    
    # Basic Info about Dataset
    st.subheader("Basic Dataset Information")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")
    
    # Show detailed dataset info
    st.text("Detailed Dataset Information:")
    df_info = df.dtypes.reset_index()
    df_info.columns = ["Column Name", "Data Type"]
    df_info["Null Count"] = df.isnull().sum().values
    st.dataframe(df_info)

    # Density Plots for All Numeric Columns
    st.subheader("Density Graphs for All Numeric Columns")
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        plt.figure(figsize=(20, 15))
        plotnumber = 1
        for column in numeric_columns:
            if plotnumber <= 30:  # Limiting to 30 plots
                ax = plt.subplot(5, 6, plotnumber)
                sns.kdeplot(df[column], shade=True)
                plt.xlabel(column)
            plotnumber += 1

        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No numeric columns found for density plots.")

    # Correlation Matrix
    st.subheader("Correlation Heatmap")

    try:
        # Select only numeric columns for correlation
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        
        if numeric_df.empty:
            st.warning("No numeric columns available for correlation heatmap.")
        else:
            # Calculate and plot correlation heatmap
            plt.figure(figsize=(20, 12))
            corr = numeric_df.corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, linewidths=1, annot=True, fmt=".2f", cmap='coolwarm')
            st.pyplot(plt)
    except Exception as e:
        st.error(f"Error generating correlation heatmap: {e}")


    # Visualization Options
    st.subheader("Data Visualization")
    column = st.selectbox("Select Column for Visualization", df.columns)

    if df[column].dtype in ['int64', 'float64']:
        # Histogram
        st.write(f"### Histogram of {column}")
        plt.figure(figsize=(8, 4))
        plt.hist(df[column], bins=30, color="skyblue")
        plt.xlabel(column)
        plt.ylabel("Count")
        st.pyplot(plt)

        # Boxplot
        st.write(f"### Boxplot of {column}")
        plt.figure(figsize=(8, 4))
        sns.boxplot(y=df[column])
        st.pyplot(plt)

        # Density Plot for Selected Column
        st.write(f"### Density Plot of {column}")
        plt.figure(figsize=(8, 4))
        sns.kdeplot(df[column], shade=True, color="green")
        plt.xlabel(column)
        st.pyplot(plt)

        # Line Plot for Trends
        st.write(f"### Line Plot of {column}")
        plt.figure(figsize=(8, 4))
        plt.plot(df[column], color="orange")
        plt.xlabel("Index")
        plt.ylabel(column)
        st.pyplot(plt)

    elif df[column].dtype == 'object':
        try:
            # Count Plot for Categorical Columns
            st.write(f"### Count Plot of {column}")
            plt.figure(figsize=(8, 4))
            sns.countplot(x=df[column], order=df[column].value_counts().index)
            plt.xticks(rotation=45)
            st.pyplot(plt)

            # Frequency Table
            st.write(f"### Frequency of {column}")
            freq_table = df[column].value_counts().reset_index()
            freq_table.columns = [column, "Count"]
            st.dataframe(freq_table)

            # Unique Values
            st.write(f"### Unique Values in {column}")
            unique_values = df[column].unique()
            st.write(unique_values)
        except Exception as e:
            st.error(f"Error visualizing column {column}: {e}")

    else:
        st.warning(f"The column {column} could not be visualized.")
