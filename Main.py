import streamlit as st
import pandas as pd
import ollama
from io import StringIO
from HandlingSection import *

def main():
    # App Title
    st.title("Data Mining Analysis")
    
    # Dataset upload
    uploaded_file = st.sidebar.file_uploader("Upload your dataset", type=["csv", "xlsx"])
    df = None
    if uploaded_file is not None:
        if 'data' not in st.session_state :
            try:
                if uploaded_file.name.endswith('.csv'):
                    DataFromCSV = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    df = pd.read_csv(DataFromCSV)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)

                st.session_state['data'] = df
                st.sidebar.success("Dataset uploaded successfully!")

            except Exception as e:
                st.error("Error reading file: " + str(e))
        else:
            df = st.session_state['data'].copy()

    # Sidebar for navigation
    with st.sidebar:
        st.subheader("Navigation")
        menu = st.radio("Choose a task:", [
            "1. Dataset Info",
            "2. Describe Dataset",
            "3. Handle Missing Values",
            "4. Handle Duplicates",
            "5. Advanced Data Analysis",
            "6. Make Predictions",
            "7. Show All Chandes"
        ])

    # Dataset Info
    def display_dataset_info():
        st.markdown("### Dataset Information")
        dataset_info = {
        "Column Name": df.columns,
        "Non-Null Count": df.notnull().sum(),
        "Data Type": df.dtypes
        }

        dataset_info_df = pd.DataFrame(dataset_info).reset_index(drop=True)
        
        # Add memory usage
        memory_usage = df.memory_usage(deep=True).sum() / 1024 ** 2  # Convert to MB
        st.markdown(f"#### Total Memory Usage: {memory_usage:.2f} MB, Shape: { df.shape} .")
        
        styled_info = dataset_info_df.style.background_gradient(cmap="coolwarm")
        st.table(styled_info)
    
    def describe_dataset():
        """Display descriptive statistics for numeric and object columns separately."""
        st.markdown("### Descriptive Statistics")

        # Numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64'])
        if not numeric_cols.empty:
            st.markdown("#### Numeric Columns")
            styled_numeric = numeric_cols.describe().style.background_gradient(cmap="coolwarm")
            st.table(styled_numeric)
        else:
            st.warning("No numeric columns found in the dataset.")

        # Categorical columns
        object_cols = df.select_dtypes(include=['object'])
        if not object_cols.empty:
            st.markdown("#### Categorical Columns")
            styled_object = object_cols.describe().style.set_properties(**{'text-align': 'center'})
            st.table(styled_object)
        else:
            st.warning("No categorical columns found in the dataset.")
        
        n_rows = st.number_input("Number of rows to display", min_value=1, max_value=len(df), value=10)
        st.subheader(f"First {n_rows} rows of the dataset")
        st.table(df.head(n_rows))


    def handle_missing_values():
        columns = [col for col in df.columns]
        selected_column = st.selectbox("Select column to handle:", ["All Columns"] + columns)

        if selected_column == "All Columns":
            st.write("### Missing Values Analysis for All Columns")
            missing_value_analysis(df)
        else:
            if df[selected_column].dtype in ['int64', 'float64']:
                HandleNumericColumn(df,selected_column )
            elif df[selected_column].dtype == 'bool':
                HandleBooleanColumn(df, selected_column)
            else :
                handle_object_column(df, selected_column)

    def AdvancedDataAnalysis():
        numerical_columns = [col for col in df.select_dtypes(include=[float, int]).columns]
        analysis_type = st.selectbox("Select Analysis Type", ["Correlation Analysis", "Feature Importance", "Statistical Tests"])
        if analysis_type == "Correlation Analysis":
            features = st.multiselect("Select features for correlation analysis", numerical_columns )
            if features:
                correlation_analysis(df, features)
            
        elif analysis_type == "Feature Importance":
            target_column = st.selectbox("Select target column for feature importance analysis", numerical_columns)
            if target_column:
                feature_importance(df, target_column)
                
        elif analysis_type == "Statistical Tests":
            features = st.multiselect("Select two features for statistical test", numerical_columns )
            test_type = st.selectbox("Select test type", ["t-test"])
            significance_level = st.slider("Select significance level", 0.01, 0.10, 0.05)
            config = AnalysisConfig(significance_level=significance_level, test_type=test_type, features_to_include=features)
            if features:
                statistical_tests(df, config)

    # Handle Duplicates
    def handle_duplicates():
        st.subheader("Handle Duplicates")
        duplicates = df.duplicated().sum()
        st.write(f"Number of duplicate rows: {duplicates}")
        if duplicates > 0 and st.button("Remove Duplicates"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates removed!")
            st.write(f"Number of duplicate rows after removal: {df.duplicated().sum()}")


    # Chat with RAG
    def chat_with_rag():
        st.subheader("Chat with Dataset using RAG")

        def ollama_generate(query: str, model: str = "llama3.2:1b") -> str:
            """Generate a response using Ollama."""
            try:
                result = ollama.chat(model=model, messages=[{"role": "user", "content": query}])
                return result.get("message", {}).get("content", "No response content.")
            except Exception as e:
                return f"Error: {e}"

        # Function to chat with CSV using Ollama
        def chat_with_csv_ollama(df, prompt, model="llama3.2:1b", max_rows=10):
            """Chat with a CSV using Ollama."""
            # Summarize dataset: Include column names, row count, and sample rows
            summary = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.\n"
            column_info = "Columns:\n" + "\n".join([f"- {col} (type: {str(df[col].dtype)})" for col in df.columns])
            sample_data = f"Sample rows:\n{df.head(5).to_string(index=False)}"

            # Include data content (limit rows if necessary)
            data_content = f"The dataset:\n{df.head(max_rows).to_string(index=False)}"

            # Create the query
            query = f"""
            You are a data assistant. Here is the summary of the dataset:
            {summary}
            {column_info}
            {sample_data}

            {data_content}

            Based on this dataset, answer the following question:
            {prompt}
            """
            
            # Use the `ollama_generate` function to get the response
            return ollama_generate(query, model=model)

        # Initialize session state for query and response history
        if "conversation" not in st.session_state:
            st.session_state.conversation = []  # Stores the history as a list of dictionaries with roles and messages

        # App title
        st.title("ChatCSV powered by Ollama")

        # Upload CSV section
            

        if df is not None:
            # Read and display the CSV
            st.info("CSV Uploaded Successfully")
            
            st.dataframe(df, use_container_width=True)

            # Chat interface
            st.info("Chat Below")
            user_input = st.chat_input("Ask a question:")

            if user_input:
                # Add user query to the conversation
                st.session_state.conversation.append({"role": "user", "content": user_input})

                # Generate response from Ollama
                with st.spinner("Generating response..."):
                    assistant_response = chat_with_csv_ollama(df, user_input)

                # Add assistant response to the conversation
                st.session_state.conversation.append({"role": "assistant", "content": assistant_response})

            # Display the conversation
            for message in st.session_state.conversation:
                if message["role"] == "user":
                    st.chat_message("user").markdown(message["content"])
                elif message["role"] == "assistant":
                    # Check if the message contains code blocks
                    if "```" in message["content"]:
                        # Split by code blocks
                        code_blocks = message["content"].split("```")
                        for i, block in enumerate(code_blocks):
                            if i % 2 == 1:  # Odd indices are code blocks
                                st.code(block.strip(), language="python")  # Render as code
                            else:
                                if block.strip():  # Avoid rendering empty text
                                    st.chat_message("assistant").markdown(block.strip())
                    else:
                        st.chat_message("assistant").markdown(message["content"])

    # Task Navigation
    if df is not None:
        if menu == "1. Dataset Info":
            display_dataset_info()
        elif menu == "2. Describe Dataset":
            st.subheader("Dataset Description")
            describe_dataset()
        elif menu == "3. Handle Missing Values":
            handle_missing_values()
        elif menu == "4. Handle Duplicates":
            handle_duplicates()
        elif menu == "5. Advanced Data Analysis":
            AdvancedDataAnalysis()
        elif menu == "6. Make Predictions":
            predict_new_use_case(df)
        elif menu == "7. Show All Chandes":
            show_change_log()
        
        


    else:
        st.info("Upload a dataset to begin.")

    # Download modified dataset
    if df is not None:
        st.sidebar.download_button(
        label="Download Dataset with Modifications",
        data=df.to_csv(index=False),
        file_name=st.sidebar.text_input("Enter file name (with .csv extension):", value="modified_dataset.csv"),
        mime="text/csv"
    )

    
if __name__ == "__main__":
    main()