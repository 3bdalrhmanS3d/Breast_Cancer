import streamlit as st
import pandas as pd
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
    st.write("Dataset Columns:", df.columns.tolist())

    # Preprocessing Options
    st.subheader("Preprocessing and Cleaning")
    if st.checkbox("Show Missing Values"):
        st.write("Missing Values in Each Column:")
        st.dataframe(df.isnull().sum())

    if st.checkbox("Drop Missing Values"):
        df.dropna(inplace=True)
        st.write("Missing values have been dropped.")
        st.dataframe(df)
    
    if st.checkbox("Handle Duplicates"):
        df.drop_duplicates(inplace=True)
        st.write("Duplicates have been removed.")
        st.dataframe(df)

    # Correlation Matrix
    if st.checkbox("Show Correlation Heatmap"):
        st.write("### Correlation Matrix Heatmap")
        plt.figure(figsize=(8, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)

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
    
    else:
        # Bar Plot for Categorical Columns
        st.write(f"### Count Plot of {column}")
        plt.figure(figsize=(8, 4))
        sns.countplot(x=df[column])
        plt.xticks(rotation=45)
        st.pyplot(plt)
