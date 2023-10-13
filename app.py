import streamlit as st
from modules.data_processing import process_data
from modules.streamlit_logger import StreamlitMemoryHandler
import logging

# Set up custom logging handler
logger = logging.getLogger()
handler = StreamlitMemoryHandler(st.session_state)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Main App
def main():
    st.title("Supply Chain Optimization App")

    # Tab-like sections using st.radio
    tab = st.radio("Go to", ["Upload Dataset", "View Logs"])

    if tab == "Upload Dataset":
        # Upload Dataset
        st.header("Upload Dataset")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

        if uploaded_file:
            import pandas as pd

            try:
                df = pd.read_csv(uploaded_file)
                processed_df = process_data(df)
                st.write(
                    processed_df.head()
                )  # Display the first few rows of the processed dataframe
            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Failed to process the uploaded file: {e}")

    elif tab == "View Logs":
        # Display Logs
        st.header("Logs")
        # Display logs from session state
        if "logs" in st.session_state:
            for log in st.session_state.logs:
                st.text(log)


if __name__ == "__main__":
    main()
