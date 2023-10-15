# This is the app.py file.

import streamlit as st
from modules.data_processing import process_data
from modules.streamlit_logger import StreamlitMemoryHandler
import logging

# Set up custom logging handler
logger = logging.getLogger()
# Check if StreamlitMemoryHandler is already in logger's handlers
if not any(isinstance(h, StreamlitMemoryHandler) for h in logger.handlers):
    handler = StreamlitMemoryHandler(st.session_state)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
else:
    # If the handler is already there, clear other handlers to avoid duplicates
    logger.handlers = [
        h for h in logger.handlers if isinstance(h, StreamlitMemoryHandler)
    ]


# Main App
def main():
    st.title("Supply Chain Optimization App")

    # Initialize 'logs' in session state if not already present
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    # Initialize 'processed_df' in session state if not already present
    if "processed_df" not in st.session_state:
        st.session_state.processed_df = None

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
                st.session_state.processed_df = process_data(df, uploaded_file.name)
                if st.session_state.processed_df is not None:
                    st.write(st.session_state.processed_df.head())
                else:
                    st.error(
                        "The uploaded dataset couldn't be processed correctly. Please check the logs for more details."
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Failed to process the uploaded file: {e}")
        elif st.session_state.processed_df is not None:
            st.write(st.session_state.processed_df.head())

    elif tab == "View Logs":
        # Display Logs
        st.header("Logs")
        # Display logs from session state
        if "logs" in st.session_state:
            # Concatenate logs and display in a text area
            st.text_area(
                "Logs", "\n".join(st.session_state.logs), height=800, max_chars=None
            )

            # Provide a button to download the logs as a .log file
            log_content = "\n".join(st.session_state.logs)
            st.download_button(
                label="Download Logs",
                data=log_content,
                file_name="logs.log",
                mime="text/plain",
            )


if __name__ == "__main__":
    main()
